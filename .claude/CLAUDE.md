## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

## Agent Roles

- **Claude (Right Brain)**: Primary for writing, design, and creative work. Strong on ideation, weak on rigor — always verify outputs before shipping.
- **Codex (Left Brain)**: Primary for coding, analysis, and review. Prickly but powerful once you learn to handle it — use for plan reviews, code reviews, and hard debugging.
- **Composer (Executor)**: Executes plans that Codex has signed off on. Use for mechanical implementation, scoped refactoring, and step-by-step task execution via `cursor-agent`. Give task-level instructions (what to do + target files + intent). Do NOT provide exact code diffs — let Cursor think.

## Workflow Orchestration

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity
- Investigation is read-only: commands that mutate the working tree (pull/generate/codegen scripts, edits) count as implementation — defer them until GO
- Minor fixes (few files, no schema / API-contract / shared-env blast radius) are a **sanctioned exception to the SDD Mandatory flow** (user directive, 2026-07-06): skip the plan doc + codex plan-review and go straight to foreground TDD after announcing "implementing directly" — but still run tests + a lightweight review before commit. Larger or destructive changes take the full SDD flow (plan → codex → zero findings → Cursor → two-stage review)

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution

### 3. Plan / Todo Review Loop
- Before showing any implementation plan, spec, or todo document to the user, review it with codex
- Apply this to plan-style and todo-style docs in general, not just a single filename
- Extend this to externally-published documents (issue / PR bodies): draft → codex review → zero findings → create, so it's right the first time. If a created item still needs changes, edit it in place (preserves audit context); avoid the create → close → reopen churn
- Use GPT-5.6 Sol (`-m gpt-5.6-sol`) for these reviews
- Explicitly tell codex to ignore nitpicks and only call out critical issues
- Update the document and re-run the review until codex has no findings left
- If you are updating an existing review, resume the latest codex session so the prior context is preserved

```bash
# Initial review
codex exec -m gpt-5.6-sol "Review this document. Do not nitpick. Only point out critical issues: {document_full_path} (ref: {CLAUDE.md full_path})" < /dev/null

# Follow-up review after updates
codex exec resume --last -m gpt-5.6-sol "The document was updated. Review it again. Do not nitpick. Only point out critical issues: {document_full_path} (ref: {CLAUDE.md full_path})" < /dev/null
```

- **`< /dev/null` は必須**: stdin を閉じないと、バックグラウンド実行時に codex が stdin のパイプ待ちで永久にハングする（2026-07-09 実測: バックグラウンド化で 100% ハング・フォアグラウンド再実行で毎回 1〜3 分完了）。`codex exec` を呼ぶ**すべて**のコマンドに付けること

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness
- Completion reports for artifact-producing steps (commit / PR / deploy / delete) must confirm the real artifact in the same turn (`git log -1`, `gh pr view <n>`, `ls`, exec log) and cite the real ID (commit hash / PR URL). No ID → no completion claim. After long loops or context compaction, don't trust your own prior self-report — re-check the real thing
- **When driving or inspecting a live UI (browser / desktop app), report only the actual rendered state — never from assumption, memory, a stale screenshot, or a name/keyword filter.** This is a recurring failure across projects (wrong "it's linked / it exists / it's done" claims from a glance or a partial filter). Concretely: (1) after every state-changing action, take a fresh screenshot / re-read the DOM and let the UI settle before claiming it worked; (2) for anything you're verifying, inspect the fine detail at pixel level — zoom in and read it character-by-character / digit-by-digit (lookalike kanji such as 高/金, checkbox ticked vs. empty, which exact row/cell is selected or highlighted, precise amounts and dates), never sign off from a shrunk-down overview; misreading small labels has already caused real errors; (3) to check whether a record exists or its state, query authoritatively (search by amount / ID, open the record) rather than trusting a name filter, which silently misses variant labels; (4) if a claim depends on UI state, confirm it in the UI in the same turn — no confirmation, no claim.

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

### 7. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

## SDD (Subagent-Driven Development) Flow

### Development Workflow (Mandatory)

```
0. Branch (before any code)
   └─ Create feature branch from main → work exclusively on this branch
   └─ Use superpowers:using-git-worktrees for isolation when appropriate

1. Plan (Claude)
   └─ Write plan → codex review → fix → re-review → zero findings

2. Per task (repeat for each task):
   ├─ **Skill load (mandatory, at task start)**
   │   ├─ Skill("superpowers:subagent-driven-development") — implementer / task-reviewer templates
   │   └─ Skill("superpowers:test-driven-development") — TDD body to embed into Cursor prompt
   │
   ├─ Implement (Cursor only — mandatory)
   │   ├─ TDD: write test → confirm failure → implement → confirm pass
   │   │   (Cursor prompt MUST embed the content of superpowers:test-driven-development, not just the 5-line summary)
   │   └─ 1 task = 1 fresh Cursor session (no batching)
   │
   └─ Task Review (superpowers:subagent-driven-development task-reviewer-prompt —
      spec compliance + code quality を1レビューで判定。superpowers 6.x で spec-reviewer が統合された)
       └─ ❌ → send fixes back to Cursor → re-review

3. After all tasks (per branch, before PR)
   ├─ Branch Review (superpowers:requesting-code-review code-reviewer — whole-branch merge review を1回)
   │   └─ ❌ → send fixes back to Cursor → re-review
   └─ superpowers:finishing-a-development-branch
```

### Branching Rules
- **Never work directly on main/master** — always create a feature branch before writing any code
- Branch naming: `feat/<feature-name>`, `fix/<bug-name>`, etc.
- Commit early and often on the feature branch
- Only merge to main after all reviews pass and `finishing-a-development-branch` is complete

### Cursor Implementation Rules (Non-Negotiable)
- **Model: default `cursor-grok-4.5-medium-fast`**（Cursor Grok 4.5 Medium Fast。旧エイリアス `grok-4.5-fast-high` と同一実体 — 名前に high とあるが effort は medium なので使わない） — invoke with `cursor agent --model cursor-grok-4.5-medium-fast`. Pass `--model` explicitly in scripts and prompts for reproducibility. Never pass Codex models (e.g. `gpt-5.3-codex-high`) — Codex is reviewer-side only (see Agent Roles)
- **Effort escalation (per task)**: keep `cursor-grok-4.5-medium-fast` as the default. Escalate to `--model cursor-grok-4.5-high-fast` only for tasks involving complex refactoring or tricky multi-step debugging. Per-token price is the same (fast tier); high effort just consumes more reasoning tokens, so escalate only when it is likely to save review round-trips
- **All implementation MUST go through Cursor** — Claude Code subagents must NOT write implementation code. Claude Code is for planning, review, and research only
- **TDD stays inside Cursor** — never split tests and implementation into separate tasks. Before each Cursor dispatch, load `superpowers:test-driven-development` via the Skill tool and **embed its content** into the Cursor prompt (not just the 5-line summary below). The 5-line block is a minimum fallback, not a substitute:
  ```
  ## Implementation instructions
  Implement using TDD:
  1. Write failing tests first
  2. Confirm tests fail
  3. Write implementation code
  4. Confirm tests pass
  5. Report list of changed files
  ```
- **Fresh Cursor session per task** — never implement multiple tasks in a single Cursor invocation
- **Route review fixes back to Cursor** — when two-stage review finds issues, don't fix them in Claude Code. Send fixes to Cursor via `--continue` and re-review
- **Pass Cursor prompts inline (do NOT write to .md files)** — dispatch via heredoc directly. The pattern of `Write` to `/tmp/cursor-*.md` then `cat | cursor-agent` is forbidden (slows down execution). Codex auto-review is reserved for spec / plan documents only, not Cursor prompts. Inline prompts must still embed all mandatory CLAUDE.md requirements (reference files, TDD block, an explicit `--model` — `cursor-grok-4.5-medium-fast` by default, or `cursor-grok-4.5-high-fast` when the effort-escalation rule applies).
  - Example: `cursor agent -p --trust --model cursor-grok-4.5-medium-fast "$(cat <<'EOF' ...prompt body... EOF)"`

- **Impact 分析は dispatch 前に（GitNexus 等 impact ツールのあるプロジェクト）** — 「編集前に impact 必須」は Cursor 委譲では字義通り守れない（Cursor が編集主体で impact を持たず、diff が出た後にしか回せない）。代わりに **Cursor に dispatch する前**に plan が名指しした対象シンボルへ `impact({target, direction:"upstream"})` を回し blast radius を plan に記録する（この時点でコード未変更＝実質「編集前」）。HIGH/CRITICAL は dispatch 前のゲート（方針見直し or ユーザー承認）。可能なら blast radius を Cursor プロンプトに埋め込み「呼び出し元の契約を壊すな」と具体指示する。
  - **計画外シンボルの取りこぼし対策（必須）**: pre-dispatch impact は plan が予見したシンボルしかカバーしない。Cursor 返却後・commit 前に `detect_changes()` で実際に変更されたシンボルを impact 済み集合と突き合わせ、未評価の差分があれば改めて `impact()` を回す。評価せず commit しない。想定外の広がり／HIGH・CRITICAL が出たら plan に取り込み直す（再 dispatch）か差し戻す。
  - **インデックス鮮度が前提**: impact/detect_changes はインデックスを読むため古いと不正確。planning バッチ前に再インデックス（例: `node .gitnexus/run.cjs analyze`）してから回す。

### Two-Stage Review (superpowers skills — MANDATORY。superpowers 6.x 構成)
- **Stage 1: Task Review（タスクごとに1回）** — never batch after all tasks are done
  1. Invoke `Skill` tool with `superpowers:subagent-driven-development` to load the **task-reviewer-prompt** template（6.x で spec-reviewer と code-quality-reviewer が統合された。spec compliance = Part 1 / code quality = Part 2 を同一レビューで判定）
  2. Following the loaded template, dispatch a task reviewer subagent via `Agent` tool (`subagent_type: "general-purpose"`)
  3. Provide: task brief / implementer report / diff package の3点 + "Do Not Trust the Report" instructions + タスク固有の named risks
  4. Must pass ✅（Approved）before committing the task
- **Stage 2: Branch Review（ブランチごとに1回・PR 前）**:
  1. Invoke `Skill` tool with `superpowers:requesting-code-review` to load the code-reviewer template
  2. Following the loaded template, dispatch a code reviewer subagent via `Agent` tool (`subagent_type: "general-purpose"`)
  3. Provide: BASE_SHA, HEAD_SHA（ブランチ全体）, what was implemented, plan reference
  4. Must pass ✅ (or "With fixes") before creating the PR
  5. **If the task touches UI/frontend**: both superpowers reviewer templates are read-only, diff-based (they explicitly avoid re-executing tests the implementer already ran), so they cannot catch bugs that only surface by actually running the UI. For UI/frontend tasks, also drive the change in a real browser via the `webapp-testing` skill (Playwright: launch the local app, screenshot, check DOM/logs) before marking Quality Review passed — do not rely on diff-reading alone. Logic-only tasks keep the standard read-only review.
  6. **Attach the screenshot to the PR as evidence (UI/frontend PRs).** For any PR that changes UI/frontend behavior, commit at least one real-browser screenshot under `docs/pr-evidence/pr-<issue>/` and embed it in the PR body — diffs and unit tests alone cannot prove the change actually renders correctly. Before committing, review each image for sensitive data: use synthetic/test data only, and redact any real customer content, secrets/tokens, or internal URLs (committed images live permanently in git history).
- **Both stages are separate subagents** — never combine, never do inline, never skip
- **Always invoke the Skill tool first** — load the template before dispatching the Agent subagent（Skill ツールに未登録の場合はプラグインキャッシュのテンプレートファイルを直接 Read して従う）
- **Reviewer model**: Task Review defaults to **sonnet** (the latest mid-tier model in the harness; when new models ship, reinterpret as "default = latest mid-tier"). Branch Review follows the superpowers default — the most capable available model, always specified explicitly in the dispatch
### No-Skip Rule
- **"I'm in a hurry", "user is sleeping", "it's a simple task" are NOT valid reasons to skip any step**
- If you cannot follow the workflow, tell the user BEFORE starting — never silently skip

## Handling Pending Suggestions

At the start of a session, if the working project's CLAUDE.md contains a `<!-- PENDING_SUGGESTIONS_START -->` section:
1. Summarize and present the suggestions to the user
2. Ask the user whether to apply them
3. If accepted: merge the suggestions into the appropriate section of CLAUDE.md and remove the Pending section
4. If not needed: remove the Pending section

## Execution / Visibility

- **No *silent* background work** (not no background): you may launch subagents and Cursor in the background and in parallel, but at launch announce what you dispatched and how many, then report each result's key points as its task-notification arrives. Never fire-and-forget, and never block silently for minutes with no output.
- **Cursor delegation is the default implementation path** (see SDD). Independent tasks may run as multiple Cursor sessions in parallel (1 task = 1 fresh session; keep dependent tasks ordered). If the harness auto-backgrounds a long run, that's fine as long as you wait for completion and report the result.
- **Destructive operations (force-push / delete / overwrite) and changes needing user judgment run in the foreground** and are shown before executing.
- **Browser automation (Claude-in-Chrome): reuse one tab per session.** Navigate within the existing tab instead of opening new ones, and don't call `tabs_context_mcp createIfEmpty` repeatedly. Close tabs you opened with `tabs_close_mcp` when the work is done. **Why:** when the tab group drops mid-session, recreating it spawns a fresh tab and orphans the old one (outside the current group → not API-closable), so orphan "Claude" tabs pile up and clutter the user's browser. Minimize group recreation and clean up as soon as extra tabs appear.

## Git Safety

- git commands that branch on success/failure (rebase / merge / cherry-pick) must not be judged through a pipe — a trailing `tail`/`head` returns exit 0 and hides the real failure. Use `cmd; rc=$?` and check `$rc` directly.
- Before any force-push or merge, guard explicitly: `git diff --check` (conflict markers), `git status --porcelain | grep -E '^(UU|AA|DD)'` (unresolved paths), and for an in-progress rebase test that the resolved dir actually exists — `test -d "$(git rev-parse --git-path rebase-merge)" -o -d "$(git rev-parse --git-path rebase-apply)"` (works in linked worktrees where `.git` is a file; `--git-path` only prints a path, so you must `test -d` it, not just run it). Never force-push with an unresolved conflict or an in-progress rebase.

## Secret Handling

- Never guess secret names or scan/enumerate multiple secrets (reads as credential-scanning and gets denied). Derive the canonical secret ID and field name from the project's own config first — `rg -n "SECRET_NAME|secretName" scripts/ infrastructure/` or the CDK/Terraform constructs — then fetch that single entry.
- Never print a secret value; validate format by regex only. Write it to the target (`.env.local` etc.) without echoing.
