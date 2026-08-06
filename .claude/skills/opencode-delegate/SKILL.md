---
name: opencode-delegate
description: Delegate implementation tasks to the opencode CLI (OpenCode Go models — grok-4.5, kimi-k3, glm-5.2 …) in headless mode. Use when the user says "opencode", "opencode go", "opencodeで実装", "opencodeに投げて", "opencodeに実装させて", or wants an implementer other than Cursor/Codex. Read this before writing any `opencode run` command — the headless permission trap and the skill-visibility differences are here.
---

# opencode Delegate

Claude Code plans, reviews, and owns git. opencode writes the code.

This skill carries **only the opencode-specific deltas**. Prompt construction, the
verify/commit steps, and the forbidden list are identical to `cursor-delegate` —
load that skill for the shared workflow rather than duplicating it here, so the two
never drift apart.

Everything below was verified against opencode **1.18.14** on 2026-08-07.

## What opencode already knows

| Auto-loaded | Notes |
|---|---|
| `AGENTS.md` | Project root, plus global `~/.config/opencode/AGENTS.md`. Verified: a passphrase in `AGENTS.md` came back without the agent reading any file |
| `~/.claude/skills/*/SKILL.md`, `~/.agents/skills/*/SKILL.md` | Registered as **real skills**, not just files. Unlike Cursor, opencode sees the *whole* `~/.claude/skills` pool. Confirm with `opencode debug skill` |
| `.opencode/skill(s)/`, `~/.config/opencode/skill(s)/` | opencode-native skills |
| `opencode.json(c)` | Project (walks up to worktree root) then global `~/.config/opencode/` — deep-merged, project wins |

**Invisible: `CLAUDE.md`, and every plugin skill under `~/.claude/plugins/` (superpowers, ponytail).**
That second group is the one that bites, because those skills look invocable from this
session. The agent will happily *try* — an unregistered name fails loudly with
`Skill "superpowers:test-driven-development" not found. Available skills: …`, and the run
derails from there.

So: **registered skill → name it in the prompt** ("use the `codex-review` skill first").
**Plugin skill → absolute path + read-first instruction, and grant the permission below**,
or the read is rejected and the dispatch dies.

## The headless permission trap

Any file read **outside `--dir`** raises an `external_directory` permission request, and
headless runs auto-reject it:

```
! permission requested: external_directory (/Users/mizoo/dotfiles/.claude/plugins/…); auto-rejecting
✗ Read …/test-driven-development/SKILL.md failed
```

Observed consequence: the agent stopped there and changed **zero files**. The dispatch looks
like it ran, and nothing happened.

Fix by injecting a scoped permission for that dispatch — not `--auto`, which approves
everything the agent asks for:

```bash
# ~/.claude is a symlink to ~/dotfiles/.claude and opencode matches on the resolved
# path, so allow both spellings.
export OPENCODE_CONFIG_CONTENT='{"$schema":"https://opencode.ai/config.json","permission":{"external_directory":{"'"$HOME"'/.claude/plugins/**":"allow","'"$HOME"'/dotfiles/.claude/plugins/**":"allow"}}}'
```

Scoped to the plugin cache, this only buys read access to skill files the prompt already
points at. Widen it only for a path the task genuinely needs; a permanent version belongs in
`~/.config/opencode/opencode.jsonc` (restart required — config is not hot-reloaded).

## Dispatch

```bash
# Fail-closed: no TDD skill, no dispatch (per CLAUDE.md). No fallback, no summary.
TDD=$(ls -d ~/.claude/plugins/cache/superpowers-marketplace/superpowers/*/skills/test-driven-development/SKILL.md 2>/dev/null | sort -V | tail -1)
test -r "$TDD" || { echo "STOP: TDD skill not found — do not dispatch" >&2; exit 1; }
python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$TDD"   # paste this path into the prompt

TITLE="t3-fix-add-$(date +%H%M)"   # unique — this is how you find the session later

opencode run --dir "<project-dir>" \
  -m opencode-go/grok-4.5 \
  --agent build \
  --title "$TITLE" \
  "$(cat <<'EOF'
最初に <resolved TDD SKILL.md path> を読み、その RED-GREEN-REFACTOR に厳密に従うこと。
failing test を確認する前に実装コードを書かない。読了後、手順の要点を3行で復唱してから
着手すること。完了時に変更ファイル一覧を報告すること。

## Task / Background / Target files / Test requirements / Forbidden
...（cursor-delegate の prompt テンプレートと同じ）
EOF
)" < /dev/null
```

- **Quoted heredoc** (`'EOF'`) so `$`, backticks and quotes in pasted constraints survive.
  It also means `$TDD` will *not* expand — write the resolved absolute path in literally.
- `< /dev/null` on every invocation, so a backgrounded run can never block on stdin.
- `--agent build` is the implementer (permission `*: allow`). `--agent plan` is read-only —
  useful for a look-before-you-leap pass. `opencode agent list` shows the rest.
- Report `$TITLE` alongside the task; it is the handle for the fix round.

## Models

`opencode models` is the source of truth; `opencode providers list` shows which credential
is active (here: **OpenCode Go** → the `opencode-go/*` half of the list).

- Default first implementation: `opencode-go/grok-4.5` — it completed a full RED→GREEN TDD
  round in ~22s on the smoke test.
- `--variant high` / `max` raises reasoning effort where the provider supports it. Spend it
  on multi-step refactors, not as a general "be careful" knob.
- Some `opencode-go` models are China-hosted and error out until opted in on the workspace
  page (`deepseek-v4-flash` did). Fail fast, but wasted round-trip — prefer a model you have
  already run.
- `opencode/*-free` models exist for throwaway experiments, not for work you intend to keep.

## Sessions

There is no `create-chat`; the id only exists after the first turn. Two ways to get it:

```bash
opencode session list | grep "$TITLE"       # id + title + updated
# or dispatch with --format json and read .sessionID off any event
```

```bash
# Fix round — same session, explicit model each time (resuming does not restore it)
opencode run --dir "<project-dir>" -s "$SID" -m opencode-go/grok-4.5 "$(cat <<'EOF'
...review findings to fix, referencing the original task...
EOF
)" < /dev/null
```

`-c/--continue` targets *the most recent* session, which is ambiguous the moment two
dispatches run in parallel — use `-s "$SID"`. `--fork` branches a session when you want to
try a second approach without losing the first.

`--format json` also reports `tokens` and `cost` per step, which is the cheapest way to see
what a dispatch actually spent.

## Forbidden items (include in every prompt)

- git commit / push / branch operations
- Creating or modifying files not related to the task
- Changing auth settings or secrets
- Adding or updating dependencies
- Running dev server / build / deploy
- Updating planning or progress tracking files

## Verify, then commit

Identical to `cursor-delegate` step 4 onward — `git status --porcelain` first (it catches the
new test files `git diff --stat` misses), scope-check every path, run the tests, revert
unexpected files one path at a time, never blanket `git checkout -- .`.
