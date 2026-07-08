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
- Use GPT-5.5  for these reviews
- Explicitly tell codex to ignore nitpicks and only call out critical issues
- Update the document and re-run the review until codex has no findings left
- If you are updating an existing review, resume the latest codex session so the prior context is preserved

```bash
# Initial review
codex exec "Review this document. Do not nitpick. Only point out critical issues: {document_full_path} (ref: {CLAUDE.md full_path})"

# Follow-up review after updates
codex exec resume --last "The document was updated. Review it again. Do not nitpick. Only point out critical issues: {document_full_path} (ref: {CLAUDE.md full_path})"
```

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
   │   ├─ Skill("superpowers:subagent-driven-development") — implementer / spec-reviewer / code-quality-reviewer templates
   │   ├─ Skill("superpowers:test-driven-development") — TDD body to embed into Cursor prompt
   │   └─ Skill("superpowers:requesting-code-review") — code-reviewer template
   │
   ├─ Implement (Cursor only — mandatory)
   │   ├─ TDD: write test → confirm failure → implement → confirm pass
   │   │   (Cursor prompt MUST embed the content of superpowers:test-driven-development, not just the 5-line summary)
   │   └─ 1 task = 1 fresh Cursor session (no batching)
   │
   ├─ Spec Review (superpowers:subagent-driven-development spec-reviewer-prompt)
   │   └─ ❌ → send fixes back to Cursor → re-review
   │
   └─ Quality Review (superpowers:requesting-code-review)
       └─ ❌ → send fixes back to Cursor → re-review

3. After all tasks
   └─ superpowers:finishing-a-development-branch
```

### Branching Rules
- **Never work directly on main/master** — always create a feature branch before writing any code
- Branch naming: `feat/<feature-name>`, `fix/<bug-name>`, etc.
- Commit early and often on the feature branch
- Only merge to main after all reviews pass and `finishing-a-development-branch` is complete

### Cursor Implementation Rules (Non-Negotiable)
- **Model: default `composer-2.5`** — invoke with `cursor agent --model composer-2.5`. Pass `--model` explicitly in scripts and prompts for reproducibility. Never pass Codex models (e.g. `gpt-5.3-codex-high`) — Codex is reviewer-side only (see Agent Roles)
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
- **Pass Cursor prompts inline (do NOT write to .md files)** — dispatch via heredoc directly. The pattern of `Write` to `/tmp/cursor-*.md` then `cat | cursor-agent` is forbidden (slows down execution). Codex auto-review is reserved for spec / plan documents only, not Cursor prompts. Inline prompts must still embed all mandatory CLAUDE.md requirements (reference files, TDD block, `--model composer-2.5-fast`).
  - Example: `cursor agent -p --trust --model composer-2.5-fast "$(cat <<'EOF' ...prompt body... EOF)"`

### Two-Stage Review (superpowers skills — MANDATORY per task)
- **Run per task** — never batch reviews after all tasks are done
- **Spec Review** (Stage 1):
  1. Invoke `Skill` tool with `superpowers:subagent-driven-development` to load the spec-reviewer-prompt template
  2. Following the loaded template, dispatch a spec reviewer subagent via `Agent` tool (`subagent_type: "general-purpose"`)
  3. Provide: full spec requirements text, file paths to review, "Do Not Trust the Report" instructions
  4. Must pass ✅ before proceeding to Stage 2
- **Quality Review** (Stage 2):
  1. Invoke `Skill` tool with `superpowers:requesting-code-review` to load the code-reviewer template
  2. Following the loaded template, dispatch a code reviewer subagent via `Agent` tool (`subagent_type: "superpowers:code-reviewer"`)
  3. Provide: BASE_SHA, HEAD_SHA, what was implemented, plan reference
  4. Must pass ✅ (or "With fixes") before committing
- **Both stages are separate subagents** — never combine, never do inline, never skip
- **Order is strict** — Spec Review first, Quality Review second. Never reverse.
- **Always invoke the Skill tool first** — load the template before dispatching the Agent subagent

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
