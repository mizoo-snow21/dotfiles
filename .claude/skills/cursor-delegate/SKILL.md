---
name: cursor-delegate
description: Delegate implementation tasks to Cursor CLI (Grok 4.5 Fast) in headless mode. Use when the user says "cursor", "composer", "cursorに実装させて", "cursorで実装", "delegate to cursor", or wants to offload coding work to Cursor's agent.
---

# Cursor Delegate

Claude Code handles planning, git operations, and review. Cursor handles coding (tests + implementation).

## What Cursor already knows

Per Cursor's rules documentation, the agent auto-loads exactly three things:

| Auto-loaded | Notes |
|---|---|
| `.cursor/rules/*.mdc` | **`.mdc` only.** A plain `.md` dropped in that directory is ignored — it has no frontmatter for `description` / `globs` / `alwaysApply` |
| `AGENTS.md` | Project root, plus nested instances in subdirectories |
| Cursor **User Rules** | Set in Cursor's own Customize menu — not a file in the repo |

**Everything else is invisible to Cursor, including `CLAUDE.md` and `~/.claude/skills/`.** Neither appears in Cursor's auto-load list. This is the trap: Claude Code's rules feel like ambient project context, but from Cursor's side they are just files nobody opened.

So, before dispatching:

- Project conventions that live in `.cursor/rules` or `AGENTS.md` → Cursor has them, don't repeat them.
- **Implementer-relevant constraints that live only in `CLAUDE.md` or a Claude Code skill → paste them into the prompt as literal text.** The TDD body is the standing example; coding conventions, caller contracts from impact analysis, and task-specific forbidden actions also qualify. A constraint you referenced by name is a constraint Cursor never saw, and the failure is silent: the work comes back looking complete and simply doesn't follow the rule.
- **Never dump the whole `CLAUDE.md`.** Most of it is Claude-Code-side orchestration — review workflows, skill routing, hook behavior, git safety, browser tool selection. Cursor executing those would be wrong, not just wasteful. Filter: *would the implementer need this rule while writing this code?* If no, it stays on Claude Code's side.
- If a project keeps its implementer-facing rules solely in `CLAUDE.md`, the durable fix is an `AGENTS.md` carrying just that subset so both agents read the same file — otherwise every dispatch has to re-paste.

Rule of thumb: *`.cursor/rules` or `AGENTS.md` → Cursor has it. Under `.claude/` → paste the parts the implementer needs, and only those.*

## Responsibilities

| Owner | Work |
|-------|------|
| **Claude Code** | Identify the problem, decide what to fix, create branch |
| **Cursor** | Write tests + implementation independently using TDD. No git operations |
| **Claude Code** | Verify changes with `git diff --stat`, run tests, commit, review, push, create PR |

## Principles

1. **Let Cursor think** — Do NOT provide exact diffs or code snippets. Describe WHAT needs to be done at task level. Let Cursor figure out the implementation and tests
2. **Cursor codes only** — Git operations (commit, push, branch) are handled by Claude Code
3. **Cursor has *some* context** — it auto-loads `.cursor/rules/*.mdc` and `AGENTS.md` only (see "What Cursor already knows"). Don't repeat those. Do paste the **implementer-relevant** constraints that live only in `CLAUDE.md` or a Claude Code skill (TDD body, coding conventions, caller contracts) — Cursor cannot see either file, and the orchestration parts stay on Claude Code's side
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

Write task-level instructions. Do NOT write exact code diffs. Do NOT repeat what Cursor already auto-loads (`.cursor/rules/*.mdc`, `AGENTS.md`). **Do paste, verbatim, the implementer-relevant constraints that live only in `CLAUDE.md` or a Claude Code skill** — the full TDD body always, plus coding conventions and caller contracts when the task touches them. Nothing else from `CLAUDE.md` goes in (see "What Cursor already knows"). Keep it concise otherwise.

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
[REQUIRED: load Skill(superpowers:test-driven-development) and paste its full
body here. There is no fallback — a summary is not a substitute, and if the
skill cannot be loaded, do NOT dispatch: stop and report the broken skill
(per CLAUDE.md). End the pasted body with: "Report list of changed files".]

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

# Prompt goes through a QUOTED heredoc ('EOF', not EOF) — the TDD body pasted into
# the prompt contains $, backticks, and quotes that direct "<prompt>" substitution
# would let the shell expand.
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model cursor-grok-4.5-medium-fast \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body (Task / Background / Target files / Test requirements /
Implementation instructions with full TDD body / Forbidden)...
EOF
)"
```

Report `$CHAT_ID` alongside the task so it survives into the review round. There is no headless way to recover it afterwards.

- **First implementation of a task**: `--model cursor-grok-4.5-medium-fast` (escalate to `cursor-grok-4.5-high-fast` only for complex refactoring or tricky multi-step debugging)
- **Every review-fix round after that**: `--model composer-2.5` with `--resume <chatId>`, using the chat id recorded when the task was dispatched — not `--continue` (see Session management)
- Verify the exact id with `cursor agent models` before scripting it — ids change between Cursor releases and a wrong `--model` silently falls back
- Do NOT use `--yolo`. Use default approval-based execution

#### Model traps

- **`grok-4.5-fast-high` is not a high-effort model.** It is an old alias for the same underlying model as `cursor-grok-4.5-medium-fast`, and its effort is medium despite "high" in the name. Do not use it — the name reads as an escalation but buys nothing.
- **Escalation is `cursor-grok-4.5-high-fast`, and it is not free of cost in time.** Per-token price is identical (same fast tier); high effort just spends more reasoning tokens. Escalate only when the extra reasoning is likely to save a review round-trip — complex refactoring, tricky multi-step debugging — not as a general "be more careful" knob.
- **Never pass a Codex model** (`gpt-5.3-codex-high` etc.) as a Cursor `--model`. Codex is the reviewer side. The one place codex appears as an implementer is the quota fallback below, where it runs as its own CLI, not as a Cursor model.

### 3b. Quota fallback: implement via the codex CLI when Cursor's quota is gone

Grok and Composer draw on the **same** Cursor plan quota, so when one hits its limit the other is normally gone too. (`--model auto` may still answer, but once implementation has moved to codex, that is no longer the sanctioned path.)

```bash
# Same quoted-heredoc rule as Cursor dispatch — the prompt embeds the TDD body.
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
- **Nothing else about the flow changes**: the TDD body still gets embedded in the prompt, one task is still one fresh session, review fixes still go back to the same implementer session, and any impact / change-detection gates still apply.
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
  --model cursor-grok-4.5-medium-fast \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body...
EOF
)"

# 3. Follow-ups (review fixes, etc.) — same id, Composer this time
# NOTE: resuming does NOT inherit the session model (CLI default wins) — always pass --model explicitly
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model composer-2.5 \
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
| `--model <model>` | Model selection (first round: cursor-grok-4.5-medium-fast / fix rounds: composer-2.5) |
| `--continue` | Continue previous session |
| `--resume <chatId>` | Resume specific session |
