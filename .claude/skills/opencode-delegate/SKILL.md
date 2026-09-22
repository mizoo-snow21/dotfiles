---
name: opencode-delegate
description: Default implementer — delegate implementation tasks to the opencode CLI in headless mode, and document reviews when codex is unavailable. Use whenever implementation is dispatched (SDD step 2), when the user says "opencode" / "opencodeで実装" / "opencodeに投げて", or when a review needs a reviewer other than codex. Read this before writing any `opencode run` command — the headless permission trap, the model roster, and the skill-visibility differences are here.
---
# opencode Delegate

Claude Code plans, reviews, and owns git. opencode writes the code.

**opencode is the default implementer** (user directive, 2026-09-22). Cursor is the fallback when
opencode is blocked — insufficient balance, the per-model China opt-in gate, or a model that will
not answer. Probe before concluding opencode is down; the failure modes are per-model and the paid
and free halves fail independently.

This skill carries **only the opencode-specific deltas**. Prompt construction, the verify/commit
steps, and the forbidden list are identical to `cursor-delegate` — load that skill for the shared
workflow rather than duplicating it here, so the two never drift apart.

Everything below was verified against opencode **v2.0.14** on 2026-09-22 by real dispatches. v2 is
a different package from the 1.x line (`@opencode/cli`; the official curl installer puts it in
`~/.opencode/bin` and `opencode upgrade` keeps it current — it lives in neither mise nor brew).
Commands remembered from 1.x will not run as-is:

| 1.x habit | v2 |
|---|---|
| `opencode run --dir <project> …` | `cd <project>` first — there is no `--dir`; the working directory is the project |
| `"permission":{"external_directory":{"<glob>":"allow"}}` | `"permissions":[{"action":"external_directory","resource":"<glob>","effect":"allow"}]` — an ordered array of rules |
| `--variant high` | `-m provider/model#high` |
| `opencode debug skill`, `opencode agent list` | skills: a throwaway dispatch (below); agents: `opencode debug agents` |
| a private server per command | `--standalone` on every headless run — v2 otherwise attaches to one shared background service |

**Default model: `opencode-go/deepseek-v4.1-flash`** — for implementation, fix rounds, and
document review alike (user directive, 2026-09-15, superseding the 2026-08-15 `glm-5.3`
default). One model everywhere means one set of quirks to learn instead of four; deviate only
for a reason you can name. `glm-5.3` is the standing second choice when deepseek is blocked.

## What opencode already knows

| Auto-loaded | Notes |
|---|---|
| `AGENTS.md` | Project root, plus global `<config dir>/AGENTS.md`. Verified on 1.x: a passphrase in `AGENTS.md` came back without the agent reading any file |
| `~/.claude/skills/*/SKILL.md`, `~/.agents/skills/*/SKILL.md` | Registered as **real skills**, not just files — all 109 of them on 2026-09-22. Unlike Cursor, opencode sees the *whole* `~/.claude/skills` pool. Confirm with a throwaway `--agent plan` dispatch: "list the exact names of every skill available to you" |
| `.opencode/skill(s)/`, `<config dir>/skill(s)/` | opencode-native skills |
| `opencode.json(c)` | Project (walks up to worktree root) then global `<config dir>/opencode.jsonc` — deep-merged, project wins |

The config dir is `~/.config/opencode` (tracked in dotfiles) unless `OPENCODE_CONFIG_DIR` says
otherwise — and **Orca sets it** to its own hooks directory for every terminal it hosts, so a
dispatch from an Orca-hosted session reads Orca's `AGENTS.md` and plugins, not the user's
(`opencode debug paths` shows which). Skills and `OPENCODE_CONFIG_CONTENT` are unaffected; the
global rtk plugin is the main thing that goes missing.

**Invisible: `CLAUDE.md`, and every plugin skill under `~/.claude/plugins/` (superpowers, ponytail).**
That second group is the one that bites, because those skills look invocable from this
session. The agent will happily *try* — an unregistered name fails loudly with
`Skill "superpowers:test-driven-development" not found. Available skills: …`, and the run
derails from there.

So: **registered skill → name it in the prompt** ("use the `codex-review` skill first").
**Plugin skill → absolute path + read-first instruction, and grant the permission below**,
or the read is rejected and the dispatch dies.

## The headless permission trap

Any file read **outside the working directory** raises an `external_directory` permission
request, and headless runs auto-reject it:

```
! permission requested: external_directory (/Users/mizoo/.claude/plugins/cache/…/test-driven-development/*); auto-rejecting
```

Observed consequence, on 1.x and v2 alike: the agent stops there and changes **zero files**. The
dispatch looks like it ran, and nothing happened.

Fix by injecting a scoped permission for that dispatch — not `--auto`, which approves
everything the agent asks for:

```bash
# ~/.claude is a symlink to ~/dotfiles/.claude and opencode matches on the resolved
# path, so allow both spellings. `external_directory` alone is enough — no `read` rule needed.
export OPENCODE_CONFIG_CONTENT='{"permissions":[
  {"action":"external_directory","resource":"'"$HOME"'/.claude/plugins/**","effect":"allow"},
  {"action":"external_directory","resource":"'"$HOME"'/dotfiles/.claude/plugins/**","effect":"allow"}]}'
```

Scoped to the plugin cache, this only buys read access to skill files the prompt already
points at. Widen it only for a path the task genuinely needs; a permanent version belongs in
`~/.config/opencode/opencode.jsonc`.

**The same trap fires on a mistyped path, and it kills the whole run.** Observed 2026-08-15:
mid-review the agent reached for
`/Users/mizoo/mc-morisumorisatei-bit/…` — one letter off from the real
`mc-mitsumorisatei-bit` — which lands outside the working directory, raises
`external_directory`, auto-rejects, and ends the dispatch with the review half-written. Three
defences:

- **Give paths in the prompt relative to the working directory**, not absolute. The agent then
  has nothing to mistype a prefix onto. (Plugin skills under `~/.claude/plugins/` are the
  exception — those must stay absolute, which is exactly why they need the permission above.)
- **Tell the implementer to keep scratch files inside the project** (`test-results/` or similar)
  and to pass relative paths instead of `cd`-ing. Observed 2026-09-16: a T8 dispatch died at
  `cd /tmp && curl …` — `/tmp/*` raised `external_directory`, auto-rejected, and the run ended
  with nothing written.
- **Add the project root itself to `external_directory`** when the run reads widely inside it.
  It costs nothing (the agent already has access to that tree) and converts a typo from a fatal
  rejection into a harmless failed read the agent can recover from.

**`external_directory` grants writes, not just reads — and the working directory stops being a
boundary.** Observed 2026-09-15: a run started in `<repo>/.worktrees/t7-e2e`, holding
`<repo>/**` allow, wrote its deliverable into the **main** checkout instead of the worktree.
Both trees matched the glob, so nothing was rejected and nothing was logged. The damage is to
your own judgement: `git status` in the worktree showed no work, the task looked abandoned, and
the implementer's truthful "tests pass" report read as a fabrication. **Check every tree the
glob covers before concluding a run produced nothing.** Scope the grant to the paths the run
must read (the plugin cache, a sibling spec) and leave the write target to the working
directory, or accept that the whole glob is the write surface.

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

cd "<project-dir>"                  # v2 has no --dir: the working directory is the project
opencode run --standalone \
  -m opencode-go/deepseek-v4.1-flash \
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
  `external_directory` permission above. This is the opposite of `~/.claude/skills/*`, which
  opencode registers as real skills you can name.
- **`--standalone`** gives the dispatch a private server. Without it v2 attaches every command to
  one shared background service (`opencode service`), so parallel dispatches and a stale service
  would share state; every fact in this skill was verified on the standalone path.
- `< /dev/null` on every invocation, so a backgrounded run can never block on stdin.
- `--agent build` is the implementer (permissions `*: allow`). `--agent plan` is read-only —
  useful for a look-before-you-leap pass. `opencode debug agents` shows the rest.
- Report `$TITLE` alongside the task; it is the handle for the fix round.

## Models

`opencode models` lists what the **active credential** exposes, not the full catalog
(`opencode auth list` shows which: here a single **OpenCode Go** entry → the `opencode-go/*`
half). 30 `opencode-go/*` ids on 2026-09-22, up from 19 in August — the list is the
environment's job, so read it with `opencode models | grep opencode-go` and probe a candidate
with one throwaway `--agent plan` dispatch before relying on it. A model missing from an older
note is not evidence it is unavailable.

**`deepseek-v4.1-flash` is the default for everything** (user directive, 2026-09-15) —
implementation, fix rounds, and document review. It carried real work on 2026-09-15: a 216-line
frontend spec review and a full E2E task. `glm-5.3` is the second choice, and earned it — on
2026-08-15 it reviewed a 1,500-line plan by **re-running the measurements itself** instead of
trusting the document's numbers, and found a real defect nine prior rounds had missed.

- **The paid and free halves fail independently.** When the workspace balance runs out, every
  `opencode-go/*` model returns `Insufficient balance` while `opencode/*` keeps answering
  (`nemotron-3-ultra-free`, `big-pickle`, `muse-spark-*` — all verified 2026-09-15). So
  "opencode is down" is a claim about one half; probe the other before reaching for another CLI.
- **The China opt-in gate is real and independent of the balance.** Verified 2026-09-16 after
  the balance was restored: `glm-5.3`, `kimi-k3` and `deepseek-v4-flash-vision-exp` all answer
  on the same credential, while `deepseek-v4.1-flash`, `deepseek-v4-flash` and `deepseek-v4-pro`
  all return "only available hosted in China and requires explicit opt in". **The gate is
  per-model and set server-side by OpenCode** — the mainline DeepSeek ids were moved behind it
  between 02:17 and 09:04 on 2026-09-15, mid-session, with nothing changed locally. The catalog
  cache carries no region field, so there is no way to predict it; probe. Clearing it is a
  one-click opt-in on the workspace page in the error message, which only the account owner can do.
- **Do not explain one failure with the other.** An earlier version of this note claimed the
  opt-in message was the balance wearing a different mask. It is not, and saying so sent the
  user to the wrong fix.
- **Disabling models on the OpenCode dashboard does not reach the CLI.** After the user turned
  several off, all still appeared in `opencode models` and all still answered. Probe, don't
  infer from the web UI.
- `-m provider/model#high` / `#max` raises reasoning effort where the provider supports it.
  Spend it on multi-step refactors, not as a general "be careful" knob.
- `opencode/*-free` models exist for throwaway experiments, not for work you intend to keep.

### `gpt-5.6-sol` is reachable, just not on this plan

The catalog cache (`~/.cache/opencode/models.json`) carries `gpt-5.6-sol` under the `openai`,
`github-copilot` and `openrouter` providers — but **not** under `opencode-go`, so
`--model opencode-go/gpt-5.6-sol` returns a 500. Adding an OpenAI / Copilot / OpenRouter
credential with `opencode auth login` would make `--model openai/gpt-5.6-sol` work. Until then
sol lives only in the codex CLI, and when codex hits its usage limit the review still has to
run — that is what the deepseek default is for.

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
opencode session list --standalone --format json   # scoped to the working directory: id, title, directory
# or dispatch with --format json — every event carries "sessionID"
```

```bash
# Fix round — same session, explicit model each time (resuming does not restore it)
cd "<project-dir>"
opencode run --standalone -s "$SID" -m opencode-go/deepseek-v4.1-flash "$(cat <<'EOF'
...review findings to fix, referencing the original task...
EOF
)" < /dev/null
```

`-c/--continue` targets *the most recent* session, which is ambiguous the moment two
dispatches run in parallel — use `-s "$SID"`. A session is bound to the directory it was created
in (`session list` prints it): once that worktree is removed, `-s` fails at once with
`UnknownError … Unexpected server error` (observed 2026-09-16) — start a fresh session in the
new tree instead of retrying. `--fork` branches a session when you want to try a second
approach without losing the first.

`--format json` is also where per-step token and cost figures show up (1.x behaviour, not
re-checked on v2) — the cheapest way to see what a dispatch actually spent.

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
