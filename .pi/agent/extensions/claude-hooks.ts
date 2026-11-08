// Claude Code の hooks (~/.claude/settings.json の PreToolUse / PostToolUse) を pi のツール呼び出しで実行する。
// 同じスクリプトを同じ JSON 契約（stdin に tool_name / tool_input / cwd / transcript_path）で呼ぶので、
// ゲートやレビューフックの本体は Claude Code と 1 か所のまま。
// transcript_path は拡張が書くセッション別ファイル。SKILL.md の read が成功した時点で
// `{"name":"Skill","input":{"skill":"<name>"}}` を 1 行追記する（gate スクリプトの grep と同じ形）。
// pi のセッションファイルは呼び出しを実行前に記録するので、ここでは使わない。
// 対象外: `rtk hook claude`（extensions/rtk.ts が担当）と Orca のフック（orca-*.ts が担当）。
import { spawn } from "node:child_process";
import { appendFileSync, closeSync, existsSync, mkdirSync, openSync, readdirSync, readFileSync, statSync, unlinkSync } from "node:fs";
import { homedir } from "node:os";
import { basename, dirname, join } from "node:path";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const SETTINGS = join(homedir(), ".claude/settings.json");
const MARKER_DIR = join(homedir(), ".pi/agent/claude-hooks");
const MARKER_TTL_MS = 7 * 24 * 60 * 60 * 1000;
const SKIP = /rtk hook claude|orca/;
const DEFAULT_TIMEOUT_SEC = 600; // Claude Code の既定（hooks docs）
// pi tool → Claude Code tool。ls は対応物なし。
const TOOL_NAME: Record<string, string> = { bash: "Bash", read: "Read", write: "Write", edit: "Edit", grep: "Grep", find: "Glob" };

type Hook = { matcher: RegExp | null; command: string; timeoutMs: number };
type HookOutput = { status: number | null; stdout: string; stderr: string };

export function loadHooks(event: "PreToolUse" | "PostToolUse", settingsPath = SETTINGS): Hook[] {
  if (!existsSync(settingsPath)) return [];
  const entries = JSON.parse(readFileSync(settingsPath, "utf8")).hooks?.[event] ?? [];
  const hooks: Hook[] = [];
  for (const entry of entries) {
    const matcher = entry.matcher && entry.matcher !== "*" ? new RegExp(`^(${entry.matcher})$`) : null;
    for (const h of entry.hooks ?? []) {
      if (h.type !== "command" || SKIP.test(h.command)) continue;
      hooks.push({ matcher, command: h.command, timeoutMs: (h.timeout ?? DEFAULT_TIMEOUT_SEC) * 1000 });
    }
  }
  return hooks;
}

// Claude Code の hook 入力。tool_input は Claude 側の引数名に寄せる（path → file_path）。
export function toClaudePayload(toolName: string, input: Record<string, unknown>, extra: Record<string, unknown>) {
  const claudeTool = TOOL_NAME[toolName];
  if (!claudeTool) return null;
  const tool_input: Record<string, unknown> = { ...input };
  if (typeof input.path === "string") tool_input.file_path = input.path;
  return { tool_name: claudeTool, tool_input, ...extra };
}

// SKILL.md の read を Skill ロードとみなす。gate が見る名前（opencode-delegate / cursor-delegate / github-issues）に plugin 接頭辞は無い。
export function skillNamesFromPath(path: string): string[] {
  return basename(path) === "SKILL.md" ? [basename(dirname(path))] : [];
}

function run(command: string, payload: unknown, timeoutMs: number, cwd: string): Promise<HookOutput> {
  return new Promise((done) => {
    // detached: タイムアウト時に sh だけでなく孫プロセス（codex 等）ごと止めるため
    const child = spawn("/bin/sh", ["-c", command], { cwd, env: { ...process.env, CLAUDE_PROJECT_DIR: cwd }, detached: true });
    let stdout = "";
    let stderr = "";
    const kill = () => {
      try {
        if (child.pid) process.kill(-child.pid, "SIGKILL");
        else child.kill("SIGKILL");
      } catch {}
    };
    const timer = setTimeout(kill, timeoutMs);
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("close", (status) => { clearTimeout(timer); done({ status, stdout, stderr }); });
    child.on("error", () => { clearTimeout(timer); done({ status: 1, stdout, stderr }); });
    child.stdin.end(JSON.stringify(payload));
  });
}

function hookOutput(out: HookOutput): Record<string, string | undefined> {
  try {
    return JSON.parse(out.stdout)?.hookSpecificOutput ?? {};
  } catch {
    return {};
  }
}

function pruneMarkers() {
  try {
    for (const f of readdirSync(MARKER_DIR)) {
      const p = join(MARKER_DIR, f);
      if (f.endsWith(".jsonl") && Date.now() - statSync(p).mtimeMs > MARKER_TTL_MS) unlinkSync(p);
    }
  } catch {}
}

export default function claudeHooks(pi: ExtensionAPI) {
  const pre = loadHooks("PreToolUse");
  const post = loadHooks("PostToolUse");
  const pendingContext = new Map<string, string[]>(); // toolCallId → PreToolUse の additionalContext

  // ゲートは transcript が無いと fail-open（Claude では常に存在する）なので、空でも必ず作っておく
  const common = (ctx: { cwd: string; sessionManager: { getSessionId(): string } }) => {
    const sessionId = ctx.sessionManager.getSessionId();
    const transcript_path = join(MARKER_DIR, `${sessionId}.jsonl`);
    mkdirSync(MARKER_DIR, { recursive: true });
    closeSync(openSync(transcript_path, "a"));
    return { session_id: sessionId, cwd: ctx.cwd, transcript_path };
  };

  pi.on("session_start", async () => pruneMarkers());

  pi.on("tool_call", async (event, ctx) => {
    const payload = toClaudePayload(event.toolName, event.input as Record<string, unknown>, { ...common(ctx), hook_event_name: "PreToolUse" });
    if (!payload) return;
    for (const hook of pre) {
      if (hook.matcher && !hook.matcher.test(payload.tool_name)) continue;
      const out = await run(hook.command, payload, hook.timeoutMs, ctx.cwd);
      const specific = hookOutput(out);
      if (out.status === 2) return { block: true, reason: out.stderr.trim() || `blocked by ${hook.command}` };
      if (specific.permissionDecision === "deny") return { block: true, reason: specific.permissionDecisionReason ?? `blocked by ${hook.command}` };
      if (specific.additionalContext) pendingContext.set(event.toolCallId, [...(pendingContext.get(event.toolCallId) ?? []), specific.additionalContext]);
    }
  });

  pi.on("tool_result", async (event, ctx) => {
    const base = common(ctx);
    const input = event.input as Record<string, unknown>;
    // 成功した read だけを Skill ロードとして記録する（呼び出しだけでは読めていない）
    if (event.toolName === "read" && !(event as { isError?: boolean }).isError && typeof input.path === "string") {
      const names = skillNamesFromPath(input.path);
      if (names.length) appendFileSync(base.transcript_path, names.map((n) => `${JSON.stringify({ name: "Skill", input: { skill: n } })}\n`).join(""));
    }
    const extra = pendingContext.get(event.toolCallId) ?? [];
    pendingContext.delete(event.toolCallId);
    const payload = toClaudePayload(event.toolName, input, { ...base, hook_event_name: "PostToolUse", tool_response: event.content });
    if (payload) {
      for (const hook of post) {
        if (hook.matcher && !hook.matcher.test(payload.tool_name)) continue;
        const out = await run(hook.command, payload, hook.timeoutMs, ctx.cwd);
        const specific = hookOutput(out);
        if (specific.additionalContext) extra.push(specific.additionalContext);
        else if (out.status === 2 && out.stderr.trim()) extra.push(out.stderr.trim());
      }
    }
    if (!extra.length) return;
    return { content: [...event.content, { type: "text" as const, text: `\n[claude-hooks]\n${extra.join("\n")}` }] };
  });
}
