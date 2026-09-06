---
name: cursor-delegate
description: Delegate implementation tasks to Cursor CLI — headless, or as a visible Orca pane when this session runs inside Orca — routing to Composer 2.5 Fast or Grok 4.6 Fast by whether the task has a right answer and how complex it is. Use when the user says "cursor", "composer", "cursorに実装させて", "cursorで実装", "delegate to cursor", or wants to offload coding work to Cursor's agent.
---

# Cursor Delegate

Claude Code handles planning, git operations, and review. Cursor handles coding (tests + implementation).

## What Cursor already knows

Per Cursor's rules documentation, the agent auto-loads:

| Auto-loaded | Notes |
|---|---|
| `.cursor/rules/*.mdc` | **`.mdc` only.** A plain `.md` dropped in that directory is ignored — it has no frontmatter for `description` / `globs` / `alwaysApply` |
| `AGENTS.md` | Project root, plus nested instances in subdirectories |
| `.cursor/skills/` (or `.agents/skills/`) | Agent Skills (SKILL.md, agentskills.io standard). Only name/description load at startup; the body is pulled when the agent decides it matches. On this machine `.cursor/skills` is a symlink to `~/.agents/skills` — the skills-CLI shared pool, which is only a **subset** of `~/.claude/skills`. Skills that exist solely on the Claude Code side (self-written ones, plugin-backed ones) have no counterpart there |
| Cursor **User Rules** | Set in Cursor's own Customize menu — not a file in the repo |

**Still invisible: `CLAUDE.md`, plugin skills under `~/.claude/plugins/` (superpowers, ponytail), and every skill that exists only in `~/.claude/skills` with no `~/.agents/skills` counterpart.** That last group is the easy one to get wrong, because those skills are visible in this session and look name-invocable. Confirm with `ls ~/.agents/skills/<name>` before writing a name invocation into a prompt — a name Cursor cannot resolve is silently ignored. And even for skills Cursor *can* see, auto-fire is probabilistic: in a one-shot headless run there is no guarantee the agent pulls the skill body. A constraint you referenced only by name is a constraint Cursor may never see, and the failure is silent: the work comes back looking complete and simply doesn't follow the rule.

So, before dispatching:

- Project conventions that live in `.cursor/rules` or `AGENTS.md` → Cursor has them, don't repeat them.
- **A required skill that lives in the synced dir (`.cursor/skills/` ← `~/.agents/skills/`) → invoke it by name in the prompt**: `/skill-name` for Cursor, `$skill-name` for Codex (both are official explicit-invocation syntax). Add "follow it before starting" so it's an instruction, not a mention.
- **A required skill that is NOT in the synced dir (plugin skills under `~/.claude/plugins/` — superpowers etc.) → resolve its absolute path and put a read-first instruction in the prompt** ("最初にこのファイルを読み、従うこと" + a short read-back requirement — **which you must then read and check; see "Capture the whole reply"**). Cursor reads files, so this is equivalent to pasting the body, but the prompt stays short and the implementer always gets the *current* version of the skill instead of a paste-time snapshot. The TDD skill is the standing example.
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

1. **Let Cursor think** — describe WHAT needs to be done at task level and let Cursor figure out the implementation and tests. **This binds the plan document, not just the prompt**: the prompt is copied from a plan step, so a plan step carrying the implementation hands Cursor the same transcript. The only literals either one carries are the contracts Cursor cannot derive — API signatures, schema / migration DDL, exact config values, error strings the tests assert. The symptom of getting this wrong is a task review reporting the diff "matches the plan verbatim": that is a copyist, and the seams the plan never specified are the one surface nobody reasoned about (a regression landed there on 2026-09-03). Difficulty-based model routing is also dead weight when the task is transcription
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

Synced skills work the opposite way — the name invocation is all Cursor needs — but their auto-fire is not something to lean on. The `python-*` set came from an upstream marketplace and its descriptions read as topic labels ("Python code style, linting, formatting") rather than as situations, so none of the five has ever fired. They are reference material, not process, which is why they are pulled deliberately instead of pushed into every prompt:

| Situation | Invoke |
| --- | --- |
| Standing up a test suite — fixtures, `conftest.py`, mocking strategy, test layout | `$python-testing-patterns` — pytest mechanics only. It never touches RED-GREEN ordering, so it stacks on top of the TDD skill instead of competing with it |
| A **measured** slowdown to profile (cProfile, memory) | `$python-performance-optimization` |

`python-code-style`, `python-project-structure`, and `python-design-patterns` stay out of prompts. Linters and task review already surface everything they say, so they cost tokens without adding a constraint the review would have missed.

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

#### Route selection

Two transports for the same dispatch. The Bash tool runs as a child of whatever pane hosts
this session, so it inherits that pane's environment — which is how you can tell where you are
without asking the user.

```bash
ROUTE=A
if [ -n "$ORCA_PANE_KEY" ] && orca status --json 2>/dev/null | python3 -c \
  'import sys,json;d=json.load(sys.stdin);sys.exit(0 if d.get("ok") and d["result"]["runtime"]["reachable"] else 1)'
then ROUTE=B; fi
```

**Route B when both hold; Route A otherwise.** Route B puts the run in a visible tab the user
can watch and interrupt, and lets review-fix rounds reuse the live pane instead of a chat id.
Same prompt, same model routing, same read-back check either way — only the transport differs,
so when anything about B looks uncertain, A always works.

Both halves of the condition earn their place:

- **`ORCA_PANE_KEY`, not `TERM_PROGRAM`.** `TERM_PROGRAM` describes the terminal doing the
  drawing, so a multiplexer between you and Orca (tmux sets `TERM_PROGRAM=tmux`) overwrites it
  and the check silently degrades to Route A. The `ORCA_*` variables are set only by Orca and
  survive nesting.
- **`orca status` before creating anything.** The environment says the pane came from Orca; it
  does not say the runtime is answering right now. Without this, `worktree create` can succeed
  and `terminal create` then fail, leaving an orphan checkout to clean up. One cheap call up
  front turns that into a clean fall back to Route A.

#### Route A — headless (`cursor agent -p`)

```bash
# Route by difficulty FIRST (see Model routing), then mint the session id —
# every review-fix round needs both.
MODEL=composer-2.5-fast            # low–medium
# MODEL=cursor-grok-4.6-high-fast  # high: concurrency, state refactors, shared components, re-dispatch
CHAT_ID=$(cursor agent create-chat)

# Prompt goes through a QUOTED heredoc ('EOF', not EOF) — pasted constraints and
# code references contain $, backticks, and quotes that direct "<prompt>"
# substitution would let the shell expand. NOTE: quoted heredoc also means
# $TDD_PATH will NOT expand — write the resolved absolute path into the prompt
# text yourself before dispatching.
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model "$MODEL" \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body (Task / Background / Target files / Test requirements /
Implementation instructions with the resolved TDD + ponytail SKILL.md absolute
paths + read-first/read-back requirement / Forbidden)...
EOF
)"
```

Report `$CHAT_ID` alongside the task so it survives into the review round. There is no headless way to recover it afterwards.

#### Route B — Orca pane (`orca terminal`)

Inside Orca, launch Cursor as a real pane instead of a child process. The user sees the work
happen and can step in; you keep full programmatic control through the CLI.

```bash
MODEL=composer-2.5-fast   # same routing as Route A

# 1 task = 1 worktree. Orca creates the checkout and owns the tab.
orca worktree create --name <task-name> --repo path:<project-dir> --no-parent --json
# → result.worktree.id is "<repoId>::<worktreePath>"; copy that whole value.

orca terminal create --worktree id:<repoId>::<worktreePath> \
  --title "cursor: <task-name>" \
  --command "cursor agent --trust --model $MODEL" --json
# → result.terminal.handle

orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 60000 --json

# The prompt goes in as ONE argument. Embedded newlines survive: Orca delivers it as a
# bracketed paste, so a multi-line brief is not submitted line by line.
orca terminal send --terminal <handle> --enter --json --text "$(cat <<'EOF'
...same prompt body as Route A...
EOF
)"

orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 3600000 --json
orca terminal read --terminal <handle> --json          # read-back + completion report
orca terminal close --terminal <handle> --tab --json   # only after step 4 verification passes
```

Why each piece is there — all four checked against a live pane on 2026-08-31:

- **`--trust` is not optional.** A fresh worktree makes Cursor raise a "Workspace Trust
  Required" dialog and sit on it. Orca surfaces this as `blockedReason:
  "codex-trust-workspace"` so you are not blind, but nothing runs until it is answered.
- **Write the argv yourself in `--command`.** Orca's own launcher (`--agent cursor`) injects
  its configured default `--yolo`, which this skill forbids. An explicit command string
  bypasses that — confirmed with `ps`: the process carries exactly the argv you wrote.
- **`--for tui-idle` replaces the exit code.** A TUI agent does not exit when the task is
  done, so "finished" means the pane went quiet. That is weaker evidence than `$?`, which is
  why reading the pane afterwards is required here rather than merely useful.
- **`blockedReason` can be stale.** Immediately after the trust dialog was answered, the next
  `wait` still reported `codex-trust-workspace` although the pane had already moved on. Treat
  one `wait` result as a hint and confirm with `terminal read` before concluding anything
  about the pane's state.

**Review-fix rounds need no chat id.** The pane is still alive, so send the findings to the
same handle with another `terminal send`. This is where Route B is plainly better: in Route A
the chat id has to be threaded through by hand and cannot be recovered once lost.

**Parallel Claude sessions share one Orca runtime.** Handles are global, not scoped to the
session that made them: a bare `orca terminal list` returns panes belonging to other sessions,
and every Orca command that accepts `--terminal` treats it as *optional*, defaulting to "the
active terminal in the current worktree." In a worktree with two sessions in it that default is
a coin flip, and losing it means typing into someone else's agent. Two habits keep this safe,
and both are already in the block above:

- **Always pass `--terminal <handle>` explicitly**, using the handle you got back from
  `terminal create`. Never rely on the active-terminal default, and never match on a pane's
  title — Orca retitles an agent pane with whatever it is currently working on.
- **Address worktrees as `id:<repoId>::<path>`, never `active`.** `--name` also has to be
  unique across concurrently running dispatches, or two sessions collide on the same checkout.

Your own pane is identified by `$ORCA_TERMINAL_HANDLE`, which is useful for making sure a
handle you are about to write to is not the session you are running in.

**Orca does not isolate test environments.** A separate worktree is still one machine —
container project names, host ports, and databases collide exactly as before. Parallel
dispatch still needs its own namespace per worktree: `portless run` for dev servers, and a
separate database / compose project for anything else.

#### Capture the whole reply, then check the read-back

**Never pipe the dispatch through `head`/`tail`.** The read-back you demanded arrives at the
*start* of the reply, so `| tail -N` throws away the one artifact that proves the skill was
read — and leaves you unable to tell "the constraint was ignored" from "I deleted the evidence."
Truncating also makes you liable to assert a failure you cannot actually support.

Redirect to a file and read what you need from it:

```bash
LOG=<scratchpad>/cursor-<task>.log
cursor agent -p --trust --workspace "<project-dir>" --model "$MODEL" --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body...
EOF
)" > "$LOG" 2>&1
head -20 "$LOG"   # read-back
tail -40 "$LOG"   # completion report
```

**Route B reads the pane, not a log file.** `orca terminal read --terminal <handle> --json`
returns plain text, so the recitation is directly greppable. The default response is a bounded
tail, which is the wrong end — the read-back sits at the *top*. Page from `oldestCursor` and
follow `nextCursor` while `limited` is true so you actually see the opening of the reply.

**Then actually check it.** A read-back requirement you never verify is not a control — it is a
comment. Confirm the reply opens with the recitation and that it names the actual procedure
(RED before implementation, etc.) rather than restating your prompt. If it is missing, or generic
enough that it could have been written without opening the file, **send the task back**; do not
accept the work and do not report the skill as followed.

To make the check mechanical, require a fixed shape in the prompt:

```
## 出力の形式（必須）
応答の冒頭に、必ず次の 2 つをこの順で書くこと:
1. `## TDD 手順の復唱` — 読んだ SKILL.md の要点 3 行
2. `## ponytail 方針の復唱` — 要点 1 行
この 2 つが無い応答は差し戻す。
```

The same rule applies to the codex fallback in 3b.

- **Pick the model by difficulty** (user directive, 2026-08-23, replacing the 2026-08-20 "`composer-2.5-fast` only" rule). See **Model routing** below. Decide once per task and keep the same model for that task's review-fix rounds unless the findings themselves turn out to be the hard kind
- Review-fix rounds add `--resume <chatId>`, using the chat id recorded when the task was dispatched — not `--continue` (see Session management)
- Verify the exact id with `cursor agent models` before scripting it — ids change between Cursor releases and a wrong `--model` silently falls back
- Do NOT use `--yolo`. Use default approval-based execution

#### Model routing

Two sanctioned models. Both verified present in `cursor agent models`.

Route with two questions, in this order. Difficulty alone puts "simple but open-ended" and "complex but fully specified" in the same box, and they need opposite models.

1. **Does the task have a right answer?** The spec pins the output (a defined contract, a stated algorithm, a test that must pass) → stable. The implementer still decides shape — visual design, API surface, naming a new abstraction → exploratory.
2. **How complex is it?** Number of files, callers, and interacting states.

| Right answer? | Complexity | `--model` | What lands here |
| --- | --- | --- | --- |
| Yes | Low | `composer-2.5-fast` | Mechanical edits, adding a field, straightforward test additions, single-file changes whose blast radius is obvious, formatting, constant swaps |
| Yes | High | `cursor-grok-4.6-high-fast` | Concurrency and race conditions, state-management refactors, contract changes spanning files, shared-component changes |
| No | Any | `cursor-grok-4.6-high-fast` | UI the spec leaves open, a new module's public shape, review findings that need a judgement call |

**Any re-implementation after a task was sent back goes to `cursor-grok-4.6-high-fast`**, whichever cell the original task sat in.

**Write the choice into the task brief: the cell, the model, and the one-line reason** ("Yes / High → `cursor-grok-4.6-high-fast`: three callers of `X` plus interacting state"). Nothing enforces the branch, so the record is the enforcement — it puts the call in front of the reviewer and the user, and a cell you cannot name is a routing decision you did not make.

**Raising the tier does not replace verification.** Whatever the model, when a task adds a test, inject the bug it claims to catch and confirm it goes RED yourself. Ask for the actual passed/failed counts in the report.

#### Model traps

- **A bare `composer-2.5` (no `-fast`) in an old prompt or script is stale.** Replace it with `composer-2.5-fast`. `cursor-grok-*` ids are NO LONGER stale — see Model routing.
- **Answer both routing questions before dispatch, not mid-task.** Escalating because a task "feels hard" halfway through wastes the session's context. Judge from the task brief and the blast radius you already measured.
- **Never pass a Codex model** (`gpt-5.3-codex-high` etc.) as a Cursor `--model`. Codex is the reviewer side. The one place codex appears as an implementer is the quota fallback below, where it runs as its own CLI, not as a Cursor model.

### 3b. Quota fallback: implement via the codex CLI when Cursor's quota is gone

Every Cursor model draws on the **same** plan quota, so on `You're out of usage` switching tiers does not help. Go to codex.

```bash
# Same quoted-heredoc rule as Cursor dispatch — the prompt carries the resolved
# TDD path + read-first instruction (write the path in literally; $ won't expand).
# Skills under ~/.codex/skills (symlinked from ~/.claude/skills) can also be
# invoked explicitly with $skill-name in the prompt — but the TDD skill is a
# plugin skill, NOT in that dir, so the absolute-path read-first instruction stays.
codex exec -m gpt-6-astra --sandbox workspace-write "$(cat <<'EOF'
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
- Return to Cursor as soon as the quota resets (monthly cycle), routing by difficulty as usual.

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

**Route B has no session to manage** — the pane holds the conversation, so a follow-up is
another `orca terminal send` to the same handle. Everything below is Route A.

**Route A: mint the chat id yourself before dispatching, and address every follow-up to that id.**

```bash
# 1. Route by difficulty, then create the session up front (prints a UUID and nothing else)
MODEL=composer-2.5-fast   # or cursor-grok-4.6-high-fast — see Model routing
CHAT_ID=$(cursor agent create-chat)

# 2. First implementation into that session (quoted heredoc — same rule as step 3)
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model "$MODEL" \
  --resume "$CHAT_ID" \
  "$(cat <<'EOF'
...prompt body...
EOF
)"

# 3. Follow-ups (review fixes, etc.) — same id, same model
# NOTE: resuming does NOT inherit the session model (CLI default wins) — always pass --model explicitly
cursor agent -p --trust \
  --workspace "<project-dir>" \
  --model "$MODEL" \
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
| `--model <id>` | `composer-2.5-fast` or `cursor-grok-4.6-high-fast` — pick by difficulty (see Model routing) |
| `--continue` | Continue previous session |
| `--resume <chatId>` | Resume specific session |
