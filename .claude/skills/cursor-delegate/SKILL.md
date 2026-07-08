---
name: cursor-delegate
description: Delegate implementation tasks to Cursor CLI (Composer 2.5) in headless mode. Use when the user says "cursor", "composer", "cursorに実装させて", "cursorで実装", "delegate to cursor", or wants to offload coding work to Cursor's agent.
---

# Cursor Delegate

Claude Code handles planning, git operations, and review. Cursor handles coding (tests + implementation).

## What Cursor already knows

Cursor automatically reads and applies:
- **CLAUDE.md** (project rules, design system, coding conventions)
- **~/.claude/skills/** (readable from Cursor's agent mode)
- **User rules** (attached to session)

Do NOT re-inject project constraints into the prompt. Cursor already has them.

## Responsibilities

| Owner | Work |
|-------|------|
| **Claude Code** | Identify the problem, decide what to fix, create branch |
| **Cursor** | Write tests + implementation independently using TDD. No git operations |
| **Claude Code** | Verify changes with `git diff --stat`, run tests, commit, review, push, create PR |

## Principles

1. **Let Cursor think** — Do NOT provide exact diffs or code snippets. Describe WHAT needs to be done at task level. Let Cursor figure out the implementation and tests
2. **Cursor codes only** — Git operations (commit, push, branch) are handled by Claude Code
3. **Cursor has context** — Cursor reads CLAUDE.md and project rules automatically. Don't duplicate them in the prompt
4. **Out-of-scope changes are forbidden** — Files not related to the task should not be modified
5. **Discard unexpected changes per-file** — Use `git checkout -- <file>` for individual files

## Workflow

### 1. Claude Code prepares

```bash
# Create branch (follow project naming conventions)
git checkout <base-branch> && git checkout -b <branch-name>

# Verify clean working tree
git status --short  # should be empty
```

### 2. Claude Code constructs the prompt

Write task-level instructions. Do NOT write exact code diffs. Do NOT repeat project rules. Keep it concise.

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
Implement using TDD:
1. Write tests
2. Confirm tests fail
3. Write implementation code
4. Confirm tests pass
5. Report list of changed files

## Forbidden
- git commit / push / branch operations
- Adding or updating dependencies
- Running dev server / build / deploy
```

### 3. Run Cursor

```bash
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model composer-2.5-fast \
  "<prompt>"
```

- Default to `--model composer-2.5-fast` unless user specifies otherwise
- Do NOT use `--yolo`. Use default approval-based execution

### 4. Claude Code verifies

```bash
# Check change scope
git diff --stat
# → Ensure no files outside the task scope were changed

# Run tests (use project's test command)
<project-test-command>

# If OK, commit
git add <changed-files>
git commit -m "<message>"
```

If unexpected files were changed:
```bash
# 1. Revert individual files
git checkout -- <unexpected-file>

# 2. Revert multiple unexpected files
git diff --name-only | grep -v '<expected-file>' | xargs git checkout --

# 3. Last resort (only if working tree was clean before delegation)
git checkout -- .
```

### 5. Claude Code reviews → push → PR

Follow the project's review workflow (e.g., spec review + quality review via subagents).

## Session management

```bash
# Follow-up instructions (fixes, etc.)
# NOTE: --continue does NOT inherit the session model (CLI default wins) — always pass --model explicitly
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model composer-2.5 \
  --continue \
  "<follow-up instructions>"

# List sessions
cursor agent ls
```

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
| `--model <model>` | Model selection (default: composer-2.5-fast) |
| `--continue` | Continue previous session |
| `--resume <chatId>` | Resume specific session |
