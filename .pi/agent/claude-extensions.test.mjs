// node --test .pi/agent/claude-extensions.test.mjs  (Node 22.6+: TS は strip されて読める)
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { loadHooks, skillNamesFromPath } from "./extensions/claude-hooks.ts";

test("loadHooks keeps gate scripts, drops rtk/orca, anchors matchers, defaults to Claude's 600s", () => {
  const dir = mkdtempSync(join(tmpdir(), "cc-"));
  const settings = join(dir, "settings.json");
  writeFileSync(settings, JSON.stringify({ hooks: { PreToolUse: [
    { matcher: "Bash", hooks: [{ type: "command", command: "gate.sh", timeout: 10 }, { type: "command", command: "rtk hook claude" }] },
    { matcher: "Grep|Glob|Bash", hooks: [{ type: "command", command: "node gitnexus.cjs" }] },
    { hooks: [{ type: "command", command: "~/.orca/agent-hooks/claude-hook.sh" }] },
  ] } }));
  const hooks = loadHooks("PreToolUse", settings);
  assert.deepEqual(hooks.map((h) => [h.command, h.timeoutMs]), [["gate.sh", 10_000], ["node gitnexus.cjs", 600_000]]);
  assert.ok(hooks[1].matcher.test("Glob") && !hooks[1].matcher.test("Globber"));
});

test("skillNamesFromPath names the skill directory of a SKILL.md and nothing else", () => {
  assert.deepEqual(skillNamesFromPath("/Users/me/.claude/skills/opencode-delegate/SKILL.md"), ["opencode-delegate"]);
  assert.deepEqual(skillNamesFromPath("/Users/me/.pi/agent/git/github.com/obra/superpowers/skills/test-driven-development/SKILL.md"), ["test-driven-development"]);
  assert.deepEqual(skillNamesFromPath("/x/skills/why/README.md"), []);
});
