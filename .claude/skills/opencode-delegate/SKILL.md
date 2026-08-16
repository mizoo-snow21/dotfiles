---
name: opencode-delegate
description: Delegate implementation tasks and document reviews to the opencode CLI in headless mode — default model `opencode-go/glm-5.3`. Use when the user says "opencode", "opencode go", "opencodeで実装", "opencodeに投げて", "opencodeに実装させて", or wants an implementer or reviewer other than Cursor/Codex — including when codex is out of quota and a review still has to happen. Read this before writing any `opencode run` command — the headless permission trap, the model roster, and the skill-visibility differences are here.
---

# opencode Delegate

Claude Code plans, reviews, and owns git. opencode writes the code.

This skill carries **only the opencode-specific deltas**. Prompt construction, the
verify/commit steps, and the forbidden list are identical to `cursor-delegate` —
load that skill for the shared workflow rather than duplicating it here, so the two
never drift apart.

Everything below was verified against opencode **1.18.14** on 2026-08-07.

**Default model: `opencode-go/glm-5.3`** — for implementation, fix rounds, and document
review alike (user directive, 2026-08-15, superseding the 2026-08-07 `kimi-k3` default:
glm is the cheaper model and these runs are long). One model everywhere means one set of
quirks to learn instead of four; deviate only for a reason you can name.

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

**The same trap fires on a mistyped path, and it kills the whole run.** Observed 2026-08-15:
mid-review the agent reached for
`/Users/mizoo/mc-morisumorisatei-bit/…` — one letter off from the real
`mc-mitsumorisatei-bit` — which lands outside `--dir`, raises `external_directory`,
auto-rejects, and ends the dispatch with the review half-written. Two defences:

- **Give paths in the prompt relative to `--dir`**, not absolute. The agent then has nothing
  to mistype a prefix onto. (Plugin skills under `~/.claude/plugins/` are the exception —
  those must stay absolute, which is exactly why they need the permission above.)
- **Add the project root itself to `external_directory`** when the run reads widely inside it.
  It costs nothing (the agent already has `--dir` access to that tree) and converts a typo
  from a fatal rejection into a harmless failed read the agent can recover from.

## Dispatch

```bash
# Fail-closed: no TDD skill, no dispatch (per CLAUDE.md). No fallback, no summary.
TDD=$(ls -d ~/.claude/plugins/cache/superpowers-marketplace/superpowers/*/skills/test-driven-development/SKILL.md 2>/dev/null | sort -V | tail -1)
test -r "$TDD" || { echo "STOP: TDD skill not found — do not dispatch" >&2; exit 1; }

# Best-effort: ponytail governs implementation style, not correctness, so a missing file
# drops the line and dispatch continues.
PONY=$(ls -d ~/.claude/plugins/cache/ponytail/ponytail/*/skills/ponytail/SKILL.md 2>/dev/null | sort -V | tail -1)

# Resolve both to real paths — paste them into the prompt literally.
python3 -c 'import os,sys;[print(os.path.realpath(p)) for p in sys.argv[1:] if p]' "$TDD" "$PONY"

TITLE="t3-fix-add-$(date +%H%M)"   # unique — this is how you find the session later

opencode run --dir "<project-dir>" \
  -m opencode-go/glm-5.3 \
  --agent build \
  --title "$TITLE" \
  "$(cat <<'EOF'
最初に <resolved TDD SKILL.md path> を読み、その RED-GREEN-REFACTOR に厳密に従うこと。
failing test を確認する前に実装コードを書かない。読了後、手順の要点を3行で復唱してから
着手すること。完了時に変更ファイル一覧を報告すること。
実装方針は <resolved ponytail SKILL.md path> にも従うこと（最小の変更で動くものを書く）。

## Task / Background / Target files / Test requirements / Forbidden
...（cursor-delegate の prompt テンプレートと同じ）
EOF
)" < /dev/null
```

- **Quoted heredoc** (`'EOF'`) so `$`, backticks and quotes in pasted constraints survive.
  It also means `$TDD` / `$PONY` will *not* expand — write the resolved absolute paths in
  literally.
- **TDD is fail-closed, ponytail is not.** TDD decides whether the code is *correct*, so a
  missing skill file stops the dispatch. ponytail decides whether it is *lean*, and shipping
  slightly over-built code beats blocking on a style reference — drop the line and continue.
- Both are plugin skills under `~/.claude/plugins/`, which opencode cannot see, so neither
  responds to a name invocation. Only the absolute path works, and reading it needs the
  `external_directory` permission below. This is the opposite of `~/.claude/skills/*`, which
  opencode registers as real skills you can name.
- `< /dev/null` on every invocation, so a backgrounded run can never block on stdin.
- `--agent build` is the implementer (permission `*: allow`). `--agent plan` is read-only —
  useful for a look-before-you-leap pass. `opencode agent list` shows the rest.
- Report `$TITLE` alongside the task; it is the handle for the fix round.

## Models

`opencode models` lists what the **active credential** exposes, not the full catalog
(`opencode auth list` shows which: here a single **OpenCode Go** entry → the `opencode-go/*`
half). Use `opencode-go/glm-5.3` unless something below applies.

Roster verified 2026-08-07 by sending a trivial prompt to all 18 `opencode-go` models —
17 answered. Working: `kimi-k3`, `kimi-k2.7-code`, `kimi-k2.6`, `grok-4.5`, `gpt-5.6-luna`,
`glm-5.2`, `glm-5.1`, `qwen3.8-max`, `qwen3.7-max`, `qwen3.7-plus`, `qwen3.6-plus`,
`deepseek-v4-pro`, `minimax-m3`, `minimax-m2.7`, `mimo-v2.5-pro`, `mimo-v2.5`, `hy3`.

**The roster grows — re-probe instead of trusting this list.** On 2026-08-15 `opencode models`
showed **19** `opencode-go` entries, and the new one is **`glm-5.3`**, verified by dispatch
(`--agent plan`, trivial prompt, answered). It was not in the 2026-08-07 roster above.
A model missing from this section is not evidence it is unavailable; `opencode models | grep <name>`
then one throwaway dispatch settles it in seconds.

**`glm-5.3` is now the default for everything** (user directive, 2026-08-15) — implementation,
fix rounds, and document review. It is the cheaper model, and these runs are long enough for
that to matter. `kimi-k3` remains in the roster; reach for it only when you can name a reason
glm fell short on the task at hand.

Verified on a real job (2026-08-15): glm-5.3 reviewed a 1,500-line implementation plan and,
rather than taking its factual claims on trust, **re-ran the measurements itself** — row counts,
annotation breakdowns, scoring-target totals — and confirmed each one before reporting. It found
a real defect nine rounds of prior review had missed. It is not a downgrade for review work.

- **`deepseek-v4-flash` is the one failure** — "only available hosted in China and requires…".
  A region opt-in, not a broken credential; the others in that family answer fine.
- **Disabling models on the OpenCode dashboard does not reach the CLI.** After the user turned
  several off, all 18 still appeared in `opencode models` and all still answered. Probe, don't
  infer from the web UI.
- `--variant high` / `max` raises reasoning effort where the provider supports it. Spend it
  on multi-step refactors, not as a general "be careful" knob.
- `opencode/*-free` models exist for throwaway experiments, not for work you intend to keep.

### `gpt-5.6-sol` is reachable, just not on this plan

The catalog cache (`~/.cache/opencode/models.json`) carries `gpt-5.6-sol` under the `openai`,
`github-copilot` and `openrouter` providers — but **not** under `opencode-go`, so
`--model opencode-go/gpt-5.6-sol` returns a 500. Adding an OpenAI / Copilot / OpenRouter
credential with `opencode auth login` would make `--model openai/gpt-5.6-sol` work. Until then
sol lives only in the codex CLI, and when codex hits its usage limit the review still has to
run — that is what the glm-5.3 default is for.

## Document review

The same dispatch works for reviewing a document (a plan, a spec, a manual chapter) when
`codex-review`'s sol is unavailable. Two differences from an implementation dispatch:

- `--agent plan` instead of `build` — the reviewer has no business editing files, and read-only
  removes the whole class of "the reviewer helpfully fixed it" surprises.
- Put the file **path** in the prompt and let the agent read it, rather than pasting the
  contents. A 3,000-line paste crowds out the reasoning you are paying for.

Give it the original requirements alongside the draft; without them a reviewer cannot tell a
deliberate omission from a dropped requirement. Running two different models over the same
document is cheap and their findings overlap only partly — worth it when the document is
going somewhere you cannot easily take it back from.

## Sessions

There is no `create-chat`; the id only exists after the first turn. Two ways to get it:

```bash
opencode session list | grep "$TITLE"       # id + title + updated
# or dispatch with --format json and read .sessionID off any event
```

```bash
# Fix round — same session, explicit model each time (resuming does not restore it)
opencode run --dir "<project-dir>" -s "$SID" -m opencode-go/glm-5.3 "$(cat <<'EOF'
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
