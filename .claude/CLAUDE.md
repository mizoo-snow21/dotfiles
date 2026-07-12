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

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution

### 3. Plan / Todo Review Loop
- Before showing any implementation plan, spec, or todo document to the user, review it with codex
- Apply this to plan-style and todo-style docs in general, not just a single filename
- Use GPT-5.6 Sol (`-m gpt-5.6-sol`) for these reviews
- Explicitly tell codex to ignore nitpicks and only call out critical issues
- Update the document and re-run the review until codex has no findings left
- If you are updating an existing review, resume the latest codex session so the prior context is preserved

```bash
# Initial review
codex exec "Review this document. Do not nitpick. Only point out critical issues: {document_full_path} (ref: {CLAUDE.md full_path})" < /dev/null

# Follow-up review after updates
codex exec resume --last "The document was updated. Review it again. Do not nitpick. Only point out critical issues: {document_full_path} (ref: {CLAUDE.md full_path})" < /dev/null
```

- **`< /dev/null` は必須**: stdin を閉じないと、バックグラウンド実行時に codex が stdin のパイプ待ちで永久にハングする（2026-07-09 実測: バックグラウンド化で 100% ハング・フォアグラウンド再実行で毎回 1〜3 分完了）。`codex exec` を呼ぶ**すべて**のコマンドに付けること

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

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
- **Model: default `grok-4.5-fast-high`**（Cursor Grok 4.5 Medium Fast） — invoke with `cursor agent --model grok-4.5-fast-high`. Pass `--model` explicitly in scripts and prompts for reproducibility. Never pass Codex models (e.g. `gpt-5.3-codex-high`) — Codex is reviewer-side only (see Agent Roles)
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
- **Pass Cursor prompts inline (do NOT write to .md files)** — dispatch via heredoc directly. The pattern of `Write` to `/tmp/cursor-*.md` then `cat | cursor-agent` is forbidden (slows down execution). Codex auto-review is reserved for spec / plan documents only, not Cursor prompts. Inline prompts must still embed all mandatory CLAUDE.md requirements (reference files, TDD block, `--model grok-4.5-fast-high`).
  - Example: `cursor agent -p --trust --model grok-4.5-fast-high "$(cat <<'EOF' ...prompt body... EOF)"`

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
  5. **If the task touches UI/frontend**: both superpowers reviewer templates are read-only, diff-based (they explicitly avoid re-executing tests the implementer already ran), so they cannot catch bugs that only surface by actually running the UI. For UI/frontend tasks, also drive the change in a real browser (e.g. via `web-devloop-tester`) before marking Quality Review passed — do not rely on diff-reading alone. Logic-only tasks keep the standard read-only review.
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

- **No background execution**: Do not use Bash with `run_in_background` or async Agent/Workflow — they hide work status. Run long-running processes in the foreground and show progress incrementally.
