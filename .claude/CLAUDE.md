## Skill Routing

**Procedures are loaded from here. This document holds only "when, what, and local deltas" — never "how".**
For any skill in the table, load it with the `Skill` tool; never reproduce its procedure from memory.
If a skill is unregistered or broken and cannot be loaded, **do not substitute from memory — stop the work and report the breakage to the user** (running on a stale procedure recreates the original problem this document once caused by shadowing skills).

| Trigger | Skill |
|---|---|
| Before showing an implementation plan / spec / todo doc to the user | `codex-review` |
| Dispatching implementation to Cursor | `cursor-delegate` |
| Before writing implementation or bugfix code | `superpowers:test-driven-development` |
| Bug / test failure / unexpected behavior (before proposing a fix) | `superpowers:systematic-debugging` |
| Before building a feature or deciding a spec | `superpowers:brainstorming` |
| **Breaking a spec / requirements into tasks / writing a plan** (before starting) | `superpowers:writing-plans` |
| Running already-decomposed tasks in this session (implementation + task review) | `superpowers:subagent-driven-development` |
| Executing a written plan in a separate session (with review gates) | `superpowers:executing-plans` |
| 2+ independent tasks that can run in parallel | `superpowers:dispatching-parallel-agents` |
| Branch-level review (before PR) | `superpowers:requesting-code-review` |
| Receiving code-review feedback | `superpowers:receiving-code-review` |
| Before declaring done / fixed / tests passing | `superpowers:verification-before-completion` |
| Wrapping up a branch | `superpowers:finishing-a-development-branch` |
| Creating or updating GitHub issues / PRs | `github-issues` |
| Checking local UI/frontend, screenshots | `webapp-testing` |
| Content bound for a Word document (paste / docx update / Word Online 上の編集) | `word-clipboard` |
| Task display broken / Task tools missing | `task-display-triage` |
| Assessing the blast radius of a change | `gitnexus-impact-analysis` |
| **本番の多数レコードへ一括処理を仕掛ける**（再処理 / バックフィル / 一括再分類） | `bulk-production-ops` |
| Closing out or handing over a session | `handover` |
| 有力案が2つ以上あって机上では決め手がない（設計・UI・アルゴリズム） | `pstack:arena` |
| **なぜこうなっているか**（設計判断の由来 / リグレッションの発端 / ポストモーテム） | `pstack:why` |
| PR を green まで見届ける（CI 赤・レビューコメント対応を再プロンプトなしで） | `pstack:babysit` |
| 長時間の自律実行 / ユーザーが席を外す間の作業（`/loop`・「寝てる間に」） | `pstack:show-me-your-work` |

- **"I've been typing the same command all along" is NOT evidence the procedure hasn't changed.** When the *kind* of action changes (investigate → implement, view → create, edit → publish), re-consult this table. Same tool, different kind of action → a different skill applies.
- Before creating anything that leaves the machine (GitHub issue, PR, comment, public document, external message), check the table **before typing the first command** — not after.
- Example: you can run `gh issue view` / `comment` / `edit` all day, but `gh issue create` is a different kind of action — always load `github-issues`.
- **pstack の SessionStart フックは意図的に無効化してある**（`scripts/install-claude-plugins.sh` が後処理で外す）。`pstack:poteto-mode` を非自明タスクの既定入り口にすると、この表と入り口が二重になり、実装の担い手（Cursor か poteto-agent か）とレビュー段数が食い違うため。表に無い `pstack:*`（`architect` / `figure-it-out` / `deslop` 等）はユーザーが名指ししたときや必要と判断したときに使ってよいが、**入り口は常にこの表**。プラグイン更新でフックが復活するので、更新後はスクリプトを再実行する

## Code Intelligence Routing

Choose the narrowest tool that answers the question correctly.

- Use LSP first for symbol definitions, references, type information,
  diagnostics, and symbol resolution.
- Use GitNexus for repository-wide architecture, execution flows,
  dependency analysis, and change impact analysis.
- Use Read for understanding a known file.
- Use Grep/Glob/rg for literal text, config, logs, comments,
  and exploratory text search.

Do not use grep as a substitute for LSP when the target is a resolvable code symbol.
LSP-first navigation does not replace GitNexus impact analysis when repository-wide
blast radius is non-trivial.

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
- Before any creative work (adding features, creating components, changing behavior): `Skill(superpowers:brainstorming)` — before entering plan mode
- **Never decompose tasks by gut feel. Follow `Skill(superpowers:writing-plans)`** (granularity, slicing, and inter-task contracts are all defined by the skill)
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
- **Trigger**: implementation plan / spec / todo documents — before showing to the user
- **issue body / PR body は対象外** (user directive, 2026-08-22)。codex の利用上限が厳しいため、レビューの価値が最も高い文書に絞る。外部公開物の事実確認が要るときは Fable などの subagent に出す
- **Procedure**: `Skill(codex-review)` (document review is covered by the skill)
- **codex の上限に当たったときのフォールバックは `pstack:interrogate`**（4モデルの敵対的レビュー）。codex の代替であって追加ゲートではない — 両方は回さない
- **Local policy**: when an already-created issue / PR needs fixing, **edit in place**. The create → close → reopen churn destroys audit context — avoid it

### 4. Verification Before Done
- Before declaring done / fixed / tests passing: `Skill(superpowers:verification-before-completion)`
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
- **Before proposing any fix: `Skill(superpowers:systematic-debugging)`. "Autonomous" means "without the user's hands" — NOT "allowed to skip steps"** — identify the cause, then fix
- On that basis: when handed a bug report, error, failing test, or red CI, fix it end-to-end without asking how
- Reduce the user's context switching to zero

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

2. Per task (independent tasks run in parallel — see Parallel Implementation Rule):
   ├─ Fan-out decision — `superpowers:dispatching-parallel-agents`
   ├─ Skill load (mandatory, at task start) — consult the Skill Routing table
   ├─ Implement (Cursor only — mandatory)
   │   ├─ TDD: write test → confirm failure → implement → confirm pass
   │   └─ 1 task = 1 fresh Cursor session (no batching)
   └─ Task Review (superpowers:subagent-driven-development)
       └─ ❌ → send fixes back to Cursor → re-review

3. After all tasks (per branch, before PR)
   ├─ Branch Review (superpowers:requesting-code-review) — one whole-branch merge review
   │   └─ ❌ → send fixes back to Cursor → re-review
   └─ superpowers:finishing-a-development-branch
```

### Branching Rules
- **Never work directly on main/master** — always create a feature branch before writing any code
- Branch naming: `feat/<feature-name>`, `fix/<bug-name>`, etc.
- Commit early and often on the feature branch
- Only merge to main after all reviews pass and `finishing-a-development-branch` is complete

### Cursor Implementation Rules (Non-Negotiable)

**Commands, flags, model ids, prompt structure, and the forbidden list all live in `Skill(cursor-delegate)`.** Below is only local policy the skill does not carry.

- **Implementation always goes through Cursor** (on quota exhaustion, fall back to the codex CLI; procedure lives in the skill) — never let a Claude Code subagent write implementation code. Claude Code does planning, review, and investigation only
  - **`pstack:arena` は例外ではない。** arena の N 個の候補は**捨てるプロトタイプ**であり、比較して設計を決めるための道具。勝った案は仕様として Cursor に渡し直す — arena が書いたコードをそのまま本番ブランチに載せない
- **1 task = 1 fresh session** — never batch multiple tasks into one invocation
- **Parallel Implementation Rule — independent tasks run in parallel, dependent ones stay ordered** (user directive, 2026-08-08). `superpowers:subagent-driven-development` lists "dispatch multiple implementation subagents in parallel" as a Red Flag, but its stated reason is conflicts — so **this local rule overrides it only where conflict is structurally impossible**. Dispatch in parallel only when ALL of the following hold:
  1. **Disjoint file sets** — declared per task in the plan, and the pre-dispatch impact analysis blast radii do not overlap either
  2. **No ordering dependency and no shared-contract change** — tasks touching proto / migrations / shared env / shared entities always run serially
  3. **1 task = 1 worktree** (`superpowers:using-git-worktrees`) — one working tree means one HEAD, so committing task A moves the BASE..HEAD range task B's review is scoped to, and any `git add -A` sweeps another session's half-written files
  4. **Each worktree gets its own test-environment namespace** — container project name, host ports, database. A separate directory does NOT separate fixed ports; two `make e2e` runs collide regardless of how disjoint the source files are. For the web dev server, start it through portless (`portless run pnpm dev` inside the worktree) — each worktree gets its own `https://<worktree>.<project>.localhost` and a free port, so 3000 is never contended; a bare `pnpm dev` still takes 3000. portless does not separate DB / containers / auth-callback URLs pinned to `localhost:3000` — those still need their own namespace
  Miss any one of them and it runs serially. Even in parallel, Task Review is one dispatch per task (never batched), and announce how many sessions were dispatched at launch
- **Never let TDD leave the implementer session** — do not split tests and implementation into separate tasks. Before dispatch, load `Skill(superpowers:test-driven-development)` (so the orchestrator knows the procedure), then **resolve the absolute path of the TDD SKILL.md and put a mandatory instruction in the prompt: "Read this file first, recite its key points, then start"** (path resolution and the fail-closed guard are in `Skill(cursor-delegate)`; skills are symlink-shared, so Cursor/Codex can read them as files). A name-only reference or a summary is NOT a substitute. If the path cannot be resolved or the file is unreadable, do NOT dispatch — stop and recover
- **Route the Cursor model by difficulty** (user directive, 2026-08-23, superseding the 2026-08-20 "`composer-2.5-fast` only" rule)
  - **Low–medium**: `composer-2.5-fast` — mechanical edits, adding a field, straightforward test additions, single-file changes whose blast radius is obvious
  - **High**: `cursor-grok-4.6-high-fast` — concurrency and race conditions, state-management refactors, contract changes spanning files, shared-component changes, **any re-implementation after a task was sent back**
  - Decide before dispatch, not mid-task. Raising the tier does not replace verification. Details in `Skill(cursor-delegate)` → Model routing
- **Review findings are NOT fixed by Claude Code — send them back to the implementer session.** The binding rule is "whoever implemented it fixes their own work", not any particular CLI
- **Pass prompts as inline heredocs** — Writing to `/tmp/cursor-*.md` and piping via `cat |` is forbidden (slow). The codex auto-review hook targets spec / plan documents only; Cursor prompts are out of its scope

- **Run impact analysis before dispatch, scoped to non-obvious blast radius (projects with an impact tool such as GitNexus)** — "impact before editing" cannot be followed literally when the edit is delegated: Cursor does the editing, has no impact tool, and a diff only exists after the fact. Instead, **before dispatching to Cursor**, resolve the target symbol and its direct references with LSP first (see Code Intelligence Routing). Escalate to GitNexus for repository-wide blast radius when the change touches **shared symbols, public interfaces, cross-module behavior, multiple callers, or any other case where blast radius isn't obvious** — record the blast radius in the plan (no code has changed yet, so this genuinely is "before the edit"). Skip the GitNexus pass when LSP shows the change is local, non-symbol, or isolated with an obvious blast radius. HIGH/CRITICAL is a pre-dispatch gate: rethink the approach or get user approval. When you can, embed the blast radius in the Cursor prompt with a concrete instruction not to break the callers' contracts.
  - **Catching symbols the plan did not foresee (mandatory)**: pre-dispatch impact only covers what the plan predicted. After Cursor returns and before committing, reconcile the symbols actually changed against the set you already assessed, and re-run impact on anything unassessed. Never commit unassessed changes. If the spread is wider than expected, or HIGH/CRITICAL appears, fold it back into the plan (re-dispatch) or send the work back.
  - **A fresh index is a precondition** — impact tools read an index, so stale data gives wrong answers. Re-index before a planning batch. Tool usage: `Skill(gitnexus-impact-analysis)` / `Skill(gitnexus-cli)`

### Two-Stage Review (MANDATORY)

Procedures, template bodies, and the material handed to reviewers all live in the skills. This section is local policy only.

- **Stage 1: Task Review (once per task)** — dispatch `Agent(task-reviewer)` (dedicated agent definition; the agent loads its template itself from `superpowers:subagent-driven-development`). Hand it: task brief / implementer report / diff package / named risks. A pass is required before committing the task. Never batch reviews after all tasks are done
- **Stage 2: Branch Review (once per branch, before PR)** — dispatch `Agent(branch-reviewer)` (template auto-loads from `superpowers:requesting-code-review`). Hand it: BASE_SHA / HEAD_SHA / what was implemented (reference the plan). A pass (Yes / With fixes) is required before creating the PR
- **The two stages are separate subagents** — never merge them, never do them inline, never skip them
- **Reviewer model**: task-reviewer is pinned to **sonnet** in its definition (meaning "current mid-tier"; reinterpret when new models ship). branch-reviewer is `inherit` — only when the session is not running on the top-tier model, pass the top-tier model explicitly at dispatch
- **A diff review alone is NOT sufficient for tasks that touched UI/frontend** — both superpowers reviewer templates are read-only / diff-based and deliberately do not re-run the implementer's tests. Bugs that only appear at runtime are structurally invisible to them. Put the change in a real browser via `Skill(webapp-testing)` and verify before passing Quality Review. Logic-only tasks may keep the read-only review
- **UI/frontend PRs attach screenshots as evidence** — a diff plus unit tests cannot prove it actually renders. Upload images via `Skill(github-pr-attachments)` (GitHub's `user-attachments` store) and embed the returned `https://github.com/user-attachments/assets/<uuid>` URL. **Do not commit evidence images to the repo** — they would live in git history forever, and `blob/<branch>/<path>?raw=true` breaks when the ref contains `/` or the branch is deleted. Before uploading, check every image for sensitive content: synthetic/test data only; mask real customer data, secrets, and internal URLs. Prefer a cropped element screenshot over a full-page one — full-page captures usually include the signed-in user's name in the sidebar. Attachments cannot be deleted through that endpoint
- **Confirm the images actually render before reporting "evidence attached"** (user directive, 2026-07-25; method updated 2026-08-12) — an asset URL returning 200 proves the file exists, not that the body renders. Ask GitHub for the rendered HTML: `gh api repos/OWNER/REPO/pulls/N -H "Accept: application/vnd.github.html+json" --jq '.body_html' | grep -oE '<img[^>]*src="[^"]*"'`. A real `private-user-images.githubusercontent.com/…?jwt=…` src means it renders; an empty `src` or no `<img>` means the Markdown was malformed or sanitized. Opening the PR in a browser is still the strongest check when one is available. Cover entry point → action → result → persistence after reload, one image per step, at a granularity that spares the reviewer manual reproduction

### No-Skip Rule
- **"I'm in a hurry", "user is sleeping", "it's a simple task" are NOT valid reasons to skip any step**
- If you cannot follow the workflow, tell the user BEFORE starting — never silently skip
- The only sanctioned lighter path is the **Minor fixes exception** (user directive, 2026-07-06 — see Plan Node Default): it is a pre-declared route with its own gates (announce "implementing directly", TDD, tests + lightweight review), not a skip. Anything outside its criteria takes the full flow

## Handling Pending Suggestions

At the start of a session, if the working project's CLAUDE.md contains a `<!-- PENDING_SUGGESTIONS_START -->` section:
1. Summarize and present the suggestions to the user
2. Ask the user whether to apply them
3. If accepted: merge the suggestions into the appropriate section of CLAUDE.md and remove the Pending section
4. If not needed: remove the Pending section

## Execution / Visibility

- **No *silent* background work** (not no background): you may launch subagents and Cursor in the background and in parallel, but at launch announce what you dispatched and how many, then report each result's key points as its task-notification arrives. Never fire-and-forget, and never block silently for minutes with no output.
- **Cursor delegation is the default implementation path** (see SDD). Independent tasks may run as multiple Cursor sessions in parallel (conditions in the SDD Parallel Implementation Rule: disjoint files, no shared contracts, 1 task = 1 worktree, separate test-environment namespace). If the harness auto-backgrounds a long run, that's fine as long as you wait for completion and report the result.
- **Never truncate a delegated agent's reply, and check what you demanded from it** (2026-08-13). Redirect the dispatch to a log file; do not pipe it through `head`/`tail`. A required read-back (TDD skill recitation etc.) arrives at the *start* of the reply, so truncating destroys the only proof the constraint landed — and then you can neither confirm it was followed nor honestly claim it was violated. **A verification you never look at is not a control.** If the read-back is absent, or generic enough to have been written without opening the file, send the task back rather than accepting the work. Applies equally to the codex fallback. Procedure: `Skill(cursor-delegate)` → "Capture the whole reply, then check the read-back".
- **Destructive operations (force-push / delete / overwrite) and changes needing user judgment run in the foreground** and are shown before executing.
- **Browser automation (Claude-in-Chrome): reuse one tab per session.** Navigate within the existing tab instead of opening new ones, and don't call `tabs_context_mcp createIfEmpty` repeatedly. Close tabs you opened with `tabs_close_mcp` when the work is done. **Why:** when the tab group drops mid-session, recreating it spawns a fresh tab and orphans the old one (outside the current group → not API-closable), so orphan "Claude" tabs pile up and clutter the user's browser. Minimize group recreation and clean up as soon as extra tabs appear.
- **Real-time task display uses the Task tools (TodoWrite is retired).** At the start of any multi-step work, load them with `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")`, create tasks with TaskCreate, and flip status to in_progress / completed as work proceeds so the TUI task list stays live. **A markdown checklist is NOT an acceptable substitute (user directive, 2026-07-23) — never silently degrade to plain-text task lists.** If the Task tools are missing or the display breaks, report it to the user as a blocker and run `Skill(task-display-triage)` — the diagnostic order (kill-switch check, env, version, what needs user approval) lives there.
- **共有文書（OneDrive/SharePoint のWord等）は、ブラウザ上で直接編集して仕上げるのが既定**（user directive, 2026-08-06）。ローカルにダウンロードして直しファイルごと差し替える経路は、所有者と書き込み権限を確認したうえでの例外。1項目が詰まっても案件ごと別ルートに移さず、項目単位でルートを選び直す（詳細は `Skill(word-clipboard)` の Route C）
- **Which browser tool: local UI/frontend dev → `Skill(webapp-testing)` (Playwright); real logged-in browser / external sites → Claude in Chrome.** For screenshots, DOM/console inspection, or driving the app under development (localhost / the code in this repo), invoke **`webapp-testing`** — do NOT default to Claude-in-Chrome just because the word "screenshot" was used. Reserve Claude in Chrome for tasks that genuinely need the user's real browser session (authenticated sites, external pages) or when "Chrome" is explicitly requested. The trap: Claude-in-Chrome's MCP tools are always loaded and prominent, so "take a screenshot" drifts to them by default even though webapp-testing is the right tool for dev work.

## Worktree の後始末

worktree は使い終わったら残さない。`~/.claude/bin/worktree-reap.sh` が SessionStart で自動実行され、
**untracked を退避してから削除**する（退避先 `~/.local/state/claude/worktree-attic/`、30日で失効。
dotfiles リポジトリの中に置くと `git clean -fdx` で退避データごと消えるため外に出している）。

- **恒久的な成果物を worktree 内に untracked のまま置かない。** attic は事故回収層であって保管場所ではない。
  知見（`tasks/lessons.md` 等）・測定スクリプト・調査メモは、**リポジトリにコミットするか、
  worktree の外**（`~/.claude/artifacts/<repo>/<issue>/` など）へ書く。
  実例: 2026-08-22 に `tasks/lessons.md` へ 161 行の知見が untracked で溜まり、
  worktree 削除で失いかけた（main 側に未反映だった）
- **マージ済みの判定に `git branch --merged` / `git merge-base --is-ancestor` を使わない。**
  squash merge のリポジトリでは、マージ済みでもブランチのコミットが main の祖先にならない。
  `gh pr list --head <branch> --state merged` を使う
- **`git worktree add -b X origin/main` は upstream を `origin/main` に設定する。**
  「upstream がある」は push 済みを意味しない。push 済みの判定は upstream が `origin/<自分のブランチ名>`
  であることを確認する。ここを誤ると未 push の作業ブランチを消す
- 削除は `git worktree remove`（`rm -rf` + `prune` ではない）。使用中プロセスの有無も確認する

## Git Safety

- git commands that branch on success/failure (rebase / merge / cherry-pick) must not be judged through a pipe — a trailing `tail`/`head` returns exit 0 and hides the real failure. Use `cmd; rc=$?` and check `$rc` directly.
- Before any force-push or merge, guard explicitly: `git diff --check` (conflict markers), `git status --porcelain | grep -E '^(UU|AA|DD)'` (unresolved paths), and for an in-progress rebase test that the resolved dir actually exists — `test -d "$(git rev-parse --git-path rebase-merge)" -o -d "$(git rev-parse --git-path rebase-apply)"` (works in linked worktrees where `.git` is a file; `--git-path` only prints a path, so you must `test -d` it, not just run it). Never force-push with an unresolved conflict or an in-progress rebase.

## Secret Handling

- Never guess secret names or scan/enumerate multiple secrets (reads as credential-scanning and gets denied). Derive the canonical secret ID and field name from the project's own config first — `rg -n "SECRET_NAME|secretName" scripts/ infrastructure/` or the CDK/Terraform constructs — then fetch that single entry.
- Never print a secret value; validate format by regex only. Write it to the target (`.env.local` etc.) without echoing.

@RTK.md
