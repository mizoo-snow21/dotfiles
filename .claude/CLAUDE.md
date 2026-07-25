## Skill Routing

**手順はここからロードする。この文書は「いつ・何を・ローカル差分」だけを持ち、「どうやって」は持たない。**
表にあるスキルは、記憶で手順を再現せず必ず `Skill` ツールでロードする。
スキルが未登録・破損していてロードできない場合は、**記憶で代替せず作業を止めてユーザーに復旧を報告する**（古い手順で走ると、この文書がスキルを潰していた元の問題に戻る）。

| トリガ | Skill |
|---|---|
| plan / spec / todo / issue body / PR body をユーザーに見せる前 | `codex-review` |
| 実装を Cursor に投げる | `cursor-delegate` |
| 実装・バグ修正のコードを書く前 | `superpowers:test-driven-development` |
| バグ・テスト失敗・想定外の挙動（修正案を出す前） | `superpowers:systematic-debugging` |
| 機能を作る・仕様を決める前 | `superpowers:brainstorming` |
| **仕様・要件をタスクに分解する / 計画を書く**（着手前） | `superpowers:writing-plans` |
| 分解済みタスクをこのセッションで回す（実装＋タスクレビュー） | `superpowers:subagent-driven-development` |
| 書かれた計画を別セッションで実行する（レビュー関門つき） | `superpowers:executing-plans` |
| 独立したタスクが2件以上あり並列に回せる | `superpowers:dispatching-parallel-agents` |
| ブランチ単位のレビュー（PR 前） | `superpowers:requesting-code-review` |
| レビュー指摘を受け取ったとき | `superpowers:receiving-code-review` |
| 完了 / 修正済み / テスト通過を宣言する前 | `superpowers:verification-before-completion` |
| ブランチを畳む | `superpowers:finishing-a-development-branch` |
| GitHub issue / PR の作成・更新 | `github-issues` |
| ローカル UI/frontend の確認・スクリーンショット | `webapp-testing` |
| コンテンツを Word 文書へ（貼り付け・docx 更新） | `word-clipboard` |
| Task 表示が壊れた / Task ツールが見つからない | `task-display-triage` |
| 変更の影響範囲を知りたい | `gitnexus-impact-analysis` |
| セッションを畳む・引き継ぐ | `handover` |

- **「同じコマンドをずっと打っている」は手順が変わっていない証拠にならない。** 行動の**種類**が変わったら（調査→実装、閲覧→作成、編集→公開）この表を引き直す。ツールが同じでも別種の行動なら別のスキルが要る
- 機械の外に出るもの（GitHub issue、PR、コメント、公開文書、外部メッセージ）を作る前は、**最初のコマンドを打つ前に**表を確認する。後からではない
- 例: `gh issue view` / `comment` / `edit` を一日中打っていても `gh issue create` は別種の行動 — `github-issues` を必ずロードする

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
- 創作的な作業（機能追加・コンポーネント作成・挙動変更）の前に `Skill(superpowers:brainstorming)` — plan mode に入る前に
- **タスク分解は自分の勘でやらない。`Skill(superpowers:writing-plans)` に従う**（粒度・刻み方・タスク間の契約はすべてスキルが規定している）
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
- **トリガ**: implementation plan / spec / todo ドキュメント、および外部に出る文書（issue body / PR body）を、ユーザーに見せる前・作成する前
- **手順**: `Skill(codex-review)`（文書レビューもスキル側でカバー済み）
- **ローカル方針**: 作成済みの issue / PR に直しが要るときは **in-place 編集**。create → close → reopen の churn は監査文脈を壊すので避ける

### 4. Verification Before Done
- 完了・修正済み・テスト通過を宣言する前に `Skill(superpowers:verification-before-completion)`
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
- **修正案を出す前に `Skill(superpowers:systematic-debugging)`。Autonomous とは「ユーザーの手を借りない」であって「手順を飛ばしてよい」ではない** — 原因を特定してから直す
- その上で: バグ報告・エラー・失敗テスト・落ちた CI を渡されたら、やり方を聞き返さずに直しきる
- ユーザーのコンテキストスイッチをゼロにする

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
   ├─ Skill load (mandatory, at task start) — Skill Routing の表を引く
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

**コマンド・フラグ・モデル id・プロンプト構成・禁止事項の一覧は `Skill(cursor-delegate)`。** 以下はスキルに無いローカル方針だけ。

- **実装は必ず Cursor 経由**（quota 切れ時は codex CLI へフォールバック、手順はスキル側）— Claude Code のサブエージェントに実装コードを書かせない。Claude Code は計画・レビュー・調査のみ
- **1 task = 1 fresh session** — 複数タスクを1回の invocation にまとめない
- **TDD を implementer セッションの外に出さない** — テストと実装を別タスクに割らない。dispatch 前に `Skill(superpowers:test-driven-development)` をロードし、**その本文をプロンプトに埋め込む**（Cursor は Claude Code のスキルを読めないので、名前で参照しただけの制約は届かない）。要約での代用は不可。ロードできないなら dispatch せず復旧する
- **Split by round: Grok writes it, Composer fixes it** (user directive, 2026-07-25) — 初回実装は Grok、レビュー修正ラウンドは Composer 2.5
- **レビュー指摘は Claude Code で直さず implementer セッションに差し戻す** — 束縛するルールは「実装した本人が自分の仕事を直す」であって特定の CLI ではない
- **プロンプトはインラインの heredoc で渡す** — `/tmp/cursor-*.md` に Write して `cat |` で流す形は禁止（遅い）。codex 自動レビューは spec / plan 文書のみが対象で、Cursor プロンプトは対象外

- **Run impact analysis before dispatch (projects with an impact tool such as GitNexus)** — "impact before editing" cannot be followed literally when the edit is delegated: Cursor does the editing, has no impact tool, and a diff only exists after the fact. Instead, **before dispatching to Cursor**, run impact analysis on the symbols the plan names and record the blast radius in the plan (no code has changed yet, so this genuinely is "before the edit"). HIGH/CRITICAL is a pre-dispatch gate: rethink the approach or get user approval. When you can, embed the blast radius in the Cursor prompt with a concrete instruction not to break the callers' contracts.
  - **Catching symbols the plan did not foresee (mandatory)**: pre-dispatch impact only covers what the plan predicted. After Cursor returns and before committing, reconcile the symbols actually changed against the set you already assessed, and re-run impact on anything unassessed. Never commit unassessed changes. If the spread is wider than expected, or HIGH/CRITICAL appears, fold it back into the plan (re-dispatch) or send the work back.
  - **A fresh index is a precondition** — impact tools read an index, so stale data gives wrong answers. Re-index before a planning batch. ツールの使い方は `Skill(gitnexus-impact-analysis)` / `Skill(gitnexus-cli)`

### Two-Stage Review (MANDATORY)

手順・テンプレート本文・reviewer に渡す材料はすべてスキル側にある。ここはローカル方針のみ。

- **Stage 1: Task Review（タスクごとに1回）** — `Agent(task-reviewer)` を dispatch（専用 agent 定義。テンプレは agent 自身が `superpowers:subagent-driven-development` からロードする）。渡すもの: task brief / implementer 報告 / diff package / named risks。タスクをコミットする前に合格が要る。全タスク完了後にまとめてやらない
- **Stage 2: Branch Review（ブランチごとに1回・PR 前）** — `Agent(branch-reviewer)` を dispatch（テンプレは `superpowers:requesting-code-review` から自動ロード）。渡すもの: BASE_SHA / HEAD_SHA / 何を実装したか（plan 参照）。PR 作成前に合格（Yes / With fixes）が要る
- **両ステージは別々のサブエージェント** — 統合しない、インラインでやらない、飛ばさない
- **Reviewer model**: task-reviewer は定義で **sonnet** 固定（最新ミドル層の意。新モデルが出たら定義を読み替える）。branch-reviewer は `inherit` — セッションが最上位モデルで走っていないときだけ、dispatch 時に model で最上位を明示する
- **UI/frontend を触ったタスクは diff レビューだけでは不十分** — superpowers の reviewer テンプレートはどちらも read-only / diff ベースで、実装者が回したテストをあえて再実行しない。実際に動かさないと出ないバグは原理的に捕まらない。`Skill(webapp-testing)` で実ブラウザに載せて確認してから Quality Review を通す。ロジックのみのタスクは read-only レビューのままでよい
- **UI/frontend の PR はスクリーンショットを証跡として添付する** — `docs/pr-evidence/pr-<issue>/` にコミットして PR 本文に埋める。diff と unit test では実際に描画されることを証明できない。コミット前に各画像の機微情報を確認: 合成・テストデータのみを使い、実顧客データ・秘密情報・内部 URL は伏せる（画像は git 履歴に永久に残る）
- **埋め込み画像は絶対 blob URL を使い、実際に描画されることを目視確認する**（user directive, 2026-07-25）— `![x](docs/pr-evidence/...)` のようなリポジトリ相対パスは GitHub で**描画されず**、黙ってリンク切れになる。ファイルはコミット済みなのに証跡が見えない PR が出来上がる。`https://github.com/<owner>/<repo>/blob/<branch>/<path>?raw=true` を使い、**PR ページをブラウザで開いて目で見てから**「証跡を添付した」と報告する。raw URL が 200 を返すことは PR 本文が描画される証明にならない。エントリポイント → 操作 → 結果 → リロード後の永続化まで、レビュアーが手で再現せずに済む粒度で1ステップ1枚を揃える

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
- **Real-time task display uses the Task tools (TodoWrite is retired).** At the start of any multi-step work, load them with `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")`, create tasks with TaskCreate, and flip status to in_progress / completed as work proceeds so the TUI task list stays live. **A markdown checklist is NOT an acceptable substitute (user directive, 2026-07-23) — never silently degrade to plain-text task lists.** If the Task tools are missing or the display breaks, report it to the user as a blocker and run `Skill(task-display-triage)` — the diagnostic order (kill-switch check, env, version, what needs user approval) lives there.
- **Which browser tool: local UI/frontend dev → `Skill(webapp-testing)` (Playwright); real logged-in browser / external sites → Claude in Chrome.** For screenshots, DOM/console inspection, or driving the app under development (localhost / the code in this repo), invoke **`webapp-testing`** — do NOT default to Claude-in-Chrome just because the word "screenshot" was used. Reserve Claude in Chrome for tasks that genuinely need the user's real browser session (authenticated sites, external pages) or when "Chrome" is explicitly requested. The trap: Claude-in-Chrome's MCP tools are always loaded and prominent, so "take a screenshot" drifts to them by default even though webapp-testing is the right tool for dev work.

## Git Safety

- git commands that branch on success/failure (rebase / merge / cherry-pick) must not be judged through a pipe — a trailing `tail`/`head` returns exit 0 and hides the real failure. Use `cmd; rc=$?` and check `$rc` directly.
- Before any force-push or merge, guard explicitly: `git diff --check` (conflict markers), `git status --porcelain | grep -E '^(UU|AA|DD)'` (unresolved paths), and for an in-progress rebase test that the resolved dir actually exists — `test -d "$(git rev-parse --git-path rebase-merge)" -o -d "$(git rev-parse --git-path rebase-apply)"` (works in linked worktrees where `.git` is a file; `--git-path` only prints a path, so you must `test -d` it, not just run it). Never force-push with an unresolved conflict or an in-progress rebase.

## Secret Handling

- Never guess secret names or scan/enumerate multiple secrets (reads as credential-scanning and gets denied). Derive the canonical secret ID and field name from the project's own config first — `rg -n "SECRET_NAME|secretName" scripts/ infrastructure/` or the CDK/Terraform constructs — then fetch that single entry.
- Never print a secret value; validate format by regex only. Write it to the target (`.env.local` etc.) without echoing.
