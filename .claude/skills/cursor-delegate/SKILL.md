---
name: cursor-delegate
description: Delegate implementation tasks to Cursor CLI (Grok 4.5) in headless mode. Use when the user says "cursor", "composer", "cursorに実装させて", "cursorで実装", "delegate to cursor", or wants to offload coding work to Cursor's agent.
---

# Cursor Delegate

Claude Code handles planning, git operations, and review. Cursor handles coding (tests + implementation).

## What Cursor already knows

Per Cursor's rules documentation, the agent auto-loads:

| Auto-loaded | Notes |
|---|---|
| `.cursor/rules/*.mdc` | **`.mdc` only.** A plain `.md` dropped in that directory is ignored — it has no frontmatter for `description` / `globs` / `alwaysApply` |
| `AGENTS.md` | Project root, plus nested instances in subdirectories |
| `.cursor/skills/` (or `.agents/skills/`) | Agent Skills (SKILL.md, agentskills.io standard). Only name/description load at startup; the body is pulled when the agent decides it matches. On this machine `.cursor/skills` is a symlink to `~/.claude/skills` — shared with Claude Code |
| Cursor **User Rules** | Set in Cursor's own Customize menu — not a file in the repo |

**Still invisible: `CLAUDE.md`, and plugin skills that live under `~/.claude/plugins/` (superpowers etc.) — those are not in the symlinked skills dir.** And even for skills Cursor *can* see, auto-fire is probabilistic: in a one-shot headless run there is no guarantee the agent pulls the skill body. A constraint you referenced only by name is a constraint Cursor may never see, and the failure is silent: the work comes back looking complete and simply doesn't follow the rule.

So, before dispatching:

- Project conventions that live in `.cursor/rules` or `AGENTS.md` → Cursor has them, don't repeat them.
- **A required skill that lives in the synced dir (`.cursor/skills/` ← `~/.claude/skills/`) → invoke it by name in the prompt**: `/skill-name` for Cursor, `$skill-name` for Codex (both are official explicit-invocation syntax). Add "follow it before starting" so it's an instruction, not a mention.
- **A required skill that is NOT in the synced dir (plugin skills under `~/.claude/plugins/` — superpowers etc.) → resolve its absolute path and put a read-first instruction in the prompt** ("最初にこのファイルを読み、従うこと" + a short read-back requirement). Cursor reads files, so this is equivalent to pasting the body, but the prompt stays short and the implementer always gets the *current* version of the skill instead of a paste-time snapshot. The TDD skill is the standing example.
- **Ad-hoc constraints that are not files → paste them as literal text.** Caller contracts from impact analysis, task-specific forbidden actions, blast-radius notes — these exist only in Claude Code's head, so they must go in verbatim.
- **Never dump the whole `CLAUDE.md`.** Most of it is Claude-Code-side orchestration — review workflows, skill routing, hook behavior, git safety, browser tool selection. Cursor executing those would be wrong, not just wasteful. Filter: *would the implementer need this rule while writing this code?* If no, it stays on Claude Code's side.
- If a project keeps its implementer-facing rules solely in `CLAUDE.md`, the durable fix is an `AGENTS.md` carrying just that subset so both agents read the same file — otherwise every dispatch has to re-paste.

Rule of thumb: *ambient conventions (`.cursor/rules` / `AGENTS.md`) → already loaded, don't repeat. Required skill in the synced dir → invoke by name (`/name` / `$name`). Required plugin skill → point at the absolute path. Exists only in Claude Code's context → paste it.*

## Responsibilities

| Owner | Work |
|-------|------|
| **Claude Code** | Identify the problem, decide what to fix, create branch |
| **Cursor** | Write tests + implementation independently using TDD. No git operations |
| **Claude Code** | Verify changes with `git diff --stat`, run tests, commit, review, push, create PR |

## Principles

1. **Let Cursor think** — Do NOT provide exact diffs or code snippets. Describe WHAT needs to be done at task level. Let Cursor figure out the implementation and tests
2. **Cursor codes only** — Git operations (commit, push, branch) are handled by Claude Code
3. **Cursor has *some* context** — it auto-loads `.cursor/rules/*.mdc`, `AGENTS.md`, and `.cursor/skills/` (see "What Cursor already knows"). Don't repeat those, but never rely on skill auto-fire for a required constraint: **synced skills the task requires get invoked by name (`/name` / `$name`), plugin skills get a read-first path instruction, and ad-hoc constraints (caller contracts, blast radius) get pasted verbatim.** `CLAUDE.md` stays invisible and its orchestration parts stay on Claude Code's side
4. **Out-of-scope changes are forbidden** — Files not related to the task should not be modified
5. **Discard unexpected changes per-file** — Use `git checkout -- <file>` for individual files

## Workflow

### 1. Claude Code prepares

```bash
# Verify clean working tree BEFORE switching branches.
# If output is non-empty, STOP — do not proceed. Ask the user to commit or
# stash their work first; otherwise it gets carried into the delegation
# branch and mistaken for Cursor's changes.
git status --short

# Only after the check passes: create branch (follow project naming conventions)
git checkout <base-branch> && git checkout -b <branch-name>
```

### 2. Claude Code constructs the prompt

Write task-level instructions. Do NOT write exact code diffs. Do NOT repeat what Cursor already auto-loads (`.cursor/rules/*.mdc`, `AGENTS.md`, `.cursor/skills/`). **Required synced skills go in as name invocations (`/name` / `$name`); required plugin skills go in as a read-first absolute path; ad-hoc constraints (caller contracts from impact analysis, task-specific forbidden actions) go in as pasted text.** Nothing else from `CLAUDE.md` goes in (see "What Cursor already knows"). Keep it concise otherwise.

Resolve the TDD skill path BEFORE writing the prompt:

```bash
# Fail-closed guard: exits nonzero so scripted flows cannot fall through to
# dispatch. Run session creation / dispatch ONLY after this succeeds.
TDD_PATH=$(ls -d ~/.claude/plugins/cache/superpowers-marketplace/superpowers/*/skills/test-driven-development/SKILL.md 2>/dev/null | sort -V | tail -1)
if ! test -r "$TDD_PATH"; then
  echo "STOP: TDD skill not found — do not dispatch" >&2
  exit 1
fi

# ponytail (implementation style). Best-effort: omit the line if missing.
PONY_PATH=$(ls -d ~/.claude/plugins/cache/ponytail/ponytail/*/skills/ponytail/SKILL.md 2>/dev/null | sort -V | tail -1)
```

If `$TDD_PATH` is empty or unreadable, do NOT dispatch — stop and report the broken skill (per CLAUDE.md). There is no fallback and a summary is not a substitute.

`$PONY_PATH` is NOT fail-closed — ponytail governs style, not correctness, so a missing file drops the line and dispatch continues. ponytail is a plugin skill and is not in the synced `~/.agents/skills` pool, so a name invocation (`$ponytail`) does nothing in Cursor; only the read-first path works.

```
## Task
[What needs to be done — goal level, no code snippets]

## Background
[Why this fix is needed]

## Target files (reference)
[Main files to change. Cursor may add more if needed]

## Test requirements
[What to test. Let Cursor decide how to write the tests]

## Implementation instructions
[REQUIRED — include verbatim, with $TDD_PATH already expanded to the absolute
path resolved in step 2:]

最初の行動として <TDD_PATH> を読み、その RED-GREEN-REFACTOR に厳密に従うこと。
failing test を確認する前に実装コードを書かない。読了後、手順の要点を3行で
復唱してから着手すること。完了時に変更ファイル一覧を報告すること。

[Include the next line too, with <PONY_PATH> expanded. Omit only if $PONY_PATH
was empty in step 2:]

次に <PONY_PATH> を読み、実装方針として従うこと（最小の変更・YAGNI・
stdlib / 既存依存優先。意図的な簡略化には `ponytail:` コメントを付ける）。

## Forbidden
- git commit / push / branch operations
- Creating or modifying files not related to the task
- Changing auth settings or secrets
- Adding or updating dependencies
- Running dev server / build / deploy
- Updating planning or progress tracking files
```

### 3. Run Cursor

```bash
# Mint the session id FIRST — every review-fix round needs it (see Session management)
CHAT_ID=$(cursor agent create-chat)

# Prompt goes through a QUOTED heredoc ('EOF', not EOF) — pasted constraints and
# code references contain $, backticks, and quotes that direct "<prompt>"
# substitution would let the shell expand. NOTE: quoted heredoc also means
# $TDD_PATH will NOT expand — write the resolved absolute path into the prompt
# text yourself before dispatching.
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model cursor-grok-4.5-medium \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body (Task / Background / Target files / Test requirements /
Implementation instructions with the resolved TDD + ponytail SKILL.md absolute
paths + read-first/read-back requirement / Forbidden)...
EOF
)"
```

Report `$CHAT_ID` alongside the task so it survives into the review round. There is no headless way to recover it afterwards.

- **First implementation of a task**: `--model cursor-grok-4.5-medium` — non-fast on purpose (user directive, 2026-07-28): fast variants likely burn the included pool ~2x faster, and headless dispatches don't need the speed. Escalate to `cursor-grok-4.5-high` only for complex refactoring or tricky multi-step debugging
- **Every review-fix round after that**: `--model composer-2.5-fast` (user directive, 2026-07-28: fix rounds are short, speed is worth it there) with `--resume <chatId>`, using the chat id recorded when the task was dispatched — not `--continue` (see Session management)
- Verify the exact id with `cursor agent models` before scripting it — ids change between Cursor releases and a wrong `--model` silently falls back
- Do NOT use `--yolo`. Use default approval-based execution

#### Model traps

- **`grok-4.5-fast-high` is not a high-effort model.** It is an old alias whose effort is medium despite "high" in the name (fast-tier sibling of `cursor-grok-4.5-medium`). Do not use it — the name reads as an escalation but buys nothing.
- **Escalation is `cursor-grok-4.5-high` (non-fast, per the 2026-07-28 directive), and it is not free of cost in time.** High effort spends more reasoning tokens. Escalate only when the extra reasoning is likely to save a review round-trip — complex refactoring, tricky multi-step debugging — not as a general "be more careful" knob.
- **Never pass a Codex model** (`gpt-5.3-codex-high` etc.) as a Cursor `--model`. Codex is the reviewer side. The one place codex appears as an implementer is the quota fallback below, where it runs as its own CLI, not as a Cursor model.

### 3b. Quota fallback: implement via the codex CLI when Cursor's quota is gone

Grok and Composer draw on the **same** Cursor plan quota, so when one hits its limit the other is normally gone too. (`--model auto` may still answer, but once implementation has moved to codex, that is no longer the sanctioned path.)

```bash
# Same quoted-heredoc rule as Cursor dispatch — the prompt carries the resolved
# TDD path + read-first instruction (write the path in literally; $ won't expand).
# Skills under ~/.codex/skills (symlinked from ~/.claude/skills) can also be
# invoked explicitly with $skill-name in the prompt — but the TDD skill is a
# plugin skill, NOT in that dir, so the absolute-path read-first instruction stays.
codex exec -m gpt-5.6-sol --sandbox workspace-write "$(cat <<'EOF'
...same prompt you would have given Cursor...
EOF
)" < /dev/null
# resume that implementer session for follow-ups (see Session management):
codex exec resume <IMPLEMENTER_SESSION_ID> -c sandbox_mode="workspace-write" "$(cat <<'EOF'
...follow-up instructions...
EOF
)" < /dev/null
```

- `< /dev/null` on **every** invocation — without it a backgrounded codex hangs forever on the stdin pipe.
- **Nothing else about the flow changes**: the TDD read-first path instruction still goes in the prompt, one task is still one fresh session, review fixes still go back to the same implementer session, and any impact / change-detection gates still apply.
- Return to the Grok-writes / Composer-fixes split as soon as the quota resets (monthly cycle).

### 4. Claude Code verifies

```bash
# Full inventory FIRST — this is the unconditional step.
# git diff --stat alone is NOT enough: it omits untracked files, and Cursor
# routinely creates new implementation/test files. Those must enter scope
# review and impact reconciliation too.
git status --porcelain   # every modified AND newly created path
git diff --stat          # size/shape of modifications to tracked files
# → Ensure no path (tracked or new) falls outside the task scope

# Run tests (use project's test command)
<project-test-command>

# If OK, commit
git add <changed-files>
git commit -m "<message>"
```

If unexpected files were changed:
```bash
# 1. Enumerate the diff and identify each unexpected path explicitly
git status --porcelain

# 2. Revert ONLY explicitly identified files, one path at a time,
#    after confirming each is task-unrelated and has no concurrent/user edits
git checkout -- <unexpected-file>
```
- NEVER blanket-revert: `git checkout -- .` and piping `git diff --name-only` into `git checkout` are forbidden — they permanently erase concurrent or user changes
- If unsure whether a change is safe to discard, prefer recoverable `git stash push -- <path>` over `git checkout --`

### 5. Claude Code reviews → push → PR

Follow the project's review workflow (e.g., spec review + quality review via subagents).

## Session management

**Mint the chat id yourself before dispatching, and address every follow-up to that id.**

```bash
# 1. Create the session up front — prints a UUID and nothing else
CHAT_ID=$(cursor agent create-chat)

# 2. First implementation into that session (quoted heredoc — same rule as step 3)
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model cursor-grok-4.5-medium \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body...
EOF
)"

# 3. Follow-ups (review fixes, etc.) — same id, Composer this time
# NOTE: resuming does NOT inherit the session model (CLI default wins) — always pass --model explicitly
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model composer-2.5-fast \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...findings to fix + reference to the original task...
EOF
)"
```

Why mint it instead of recovering it later: `cursor agent ls` is an **interactive TUI picker**, not a listing command. Run from a script it dies with `ERROR Raw mode is not supported on the current process.stdin` (verified 2026-07-25) — so there is no headless way to look up an id you failed to capture. `create-chat` is the only reliable handle.

`--continue` (and the bare `resume` subcommand, "Resume the latest chat session") both target *the most recent* session. `cursor agent --help` does not say whether "most recent" is scoped per workspace or globally, so with parallel dispatches you cannot tell from the flags alone which session you are about to write into. An explicit `--resume "$CHAT_ID"` removes the question entirely — use it, and treat `--continue` as acceptable only for a throwaway one-session interactive run.

## Default forbidden items (include in every Cursor prompt)

- git commit / push / branch operations
- Creating or modifying files not related to the task
- Changing auth settings or secrets
- Adding or updating dependencies
- Running dev server / build / deploy
- Updating planning or progress tracking files

## Key flags

| Flag | Purpose |
|------|---------|
| `-p` | Headless output (required for CLI execution) |
| `--trust` | Trust workspace (required for headless mode) |
| `--workspace <path>` | Working directory |
| `--model <model>` | Model selection (first round: cursor-grok-4.5-medium / fix rounds: composer-2.5-fast) |
| `--continue` | Continue previous session |
| `--resume <chatId>` | Resume specific session |
