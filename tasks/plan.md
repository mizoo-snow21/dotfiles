# pi: Claude Code 設定をネイティブ機構で共有する Implementation Plan

> **For agentic workers:** Minor fixes 例外で Claude Code が直接実施する（設定ファイルと小スクリプトのみ、schema / API 契約なし）。Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Claude Code のグローバル指示・skills・agents・hooks・MCP・plugins を、pi 1.5.0 が公式に持つ機構だけで読ませ、実体はすべて dotfiles で管理する。変換層は pi-subagents が解決できない agents の frontmatter と、hooks を呼ぶ拡張の 2 つだけに絞る。

**Architecture:** pi は agent dir の `CLAUDE.md` を context file として読む（`AGENTS.md` があるとそちらが優先され 1 つだけ）ので、`~/.pi/agent/CLAUDE.md` を `dotfiles/.claude/CLAUDE.md` への symlink にし、拡張 `claude-context.ts` を廃止する。pi 固有の読み替えは `APPEND_SYSTEM.md` へ。hooks 拡張は Claude の hook スクリプトを同じ JSON 契約で呼ぶ。gate が見る `transcript_path` には、SKILL.md の read が**成功した**ときだけ拡張が追記するセッション別ファイルを渡す（pi のセッションファイルは呼び出しを実行前に記録するので使えない）。agents は生成スクリプトを残すが、生成物は `~/.pi/agent/agents/` に直接書いて git 管理しない（`rtk.ts` と同じ扱い）。MCP は `~/.claude.json` を正本とし、既存の `setup-claude-code-mcp.sh` の末尾で pi の `mcp.json` へ jq で写す（一時ファイルに書いて `mv`。古い symlink を辿らない）。

**Tech Stack:** pi 1.5.0（context files / APPEND_SYSTEM.md / extensions / mcp.json）、pi-subagents 0.87、bash、jq、python3、Node 26（`node --test` で TS 直読み）

## Global Constraints

- dotfiles（公開リポジトリ `mizoo-snow21/dotfiles`）に内部エンドポイント URL・テナント ID・API キー・`.git/info/exclude` 対象の内容（（非公開 agent） 等）を置かない
- `~/.pi/agent/settings.json` は dotfiles で管理しない（pi が deviceId を書く。README 記載）。packages の一覧は install.sh の pi 節が正本
- pi-lens（LSP）と GitNexus は併用する。分担は CLAUDE.md の Code Intelligence Routing どおり（シンボル解決は LSP、リポジトリ全体の構造・影響範囲は GitNexus）
- `~/.pi/agent/` への配置は `install.sh` の `backup_and_link` か、install.sh から呼ぶ生成スクリプトで行う
- `~/.claude/agents/*.md`、`~/.claude/CLAUDE.md`、`~/.claude/bin/*-gate.sh` は変更しない
- Claude の PreToolUse / PostToolUse hooks は codex 系（codex-review-plan / codex-foreground-guard）も含め pi でも全部動かす（pi の既定モデルは後で Claude に切り替える予定なので、codex-review は別系統レビューとして成立する）。SessionStart の `worktree-reap.sh` は Claude 側のセッション開始で回るので pi にはつながない
- 元の `dotfiles/.pi/agent/AGENTS.md` にあった rtk の注意（`rtk proxy git diff` を使う）は pi に残す

## 一次資料・実測で確定した前提（再調査不要）

- pi は agent dir で `AGENTS.override.md → AGENTS.md → AGENTS.MD → CLAUDE.md → CLAUDE.MD` の順に探し最初の 1 つだけ読む（`dist/core/resource-loader.js` `loadContextFileFromDir`）。`@path` import は解釈しない。context file は構造化セクションとして session JSONL に記録される（`before_agent_start` の systemPrompt 上書きは記録されない）
- `APPEND_SYSTEM.md` は `<addendum>` として context file より前に載る。trust 済みプロジェクトの `.pi/APPEND_SYSTEM.md` があると user 側は置き換わる
- pi-subagents: `model: sonnet` は起動失敗、`tools: Read, Grep` の大文字名は strict allowlist に一致せず起動エラー（`requested unavailable child tools`。実測では子のツールが空のまま終了）。frontmatter の `|` ブロック・`#` コメント・`- item` は pi-subagents 自身が解釈する。`skills:` が解決されると `read` は自動で子に付く。custom agent は既定で context files を受け取らない。生成済み agent の `skills:` により子のプロンプトに SKILL.md のパスが渡る
- gpt-6.1-sol では新しいセッションに最初 `subagents_enable` だけが載り、呼ぶと次のリクエストから `subagent` が使える
- pi の session JSONL は assistant message（その中の全ツール呼び出し）を**実行前に**記録する（extensions.md: `tool_call` 時点で sessionManager は現在の assistant message まで同期済み）。同じ message に `read SKILL.md` と `bash opencode run` が並ぶと、read の実行前に呼び出しだけが記録される。したがってセッションファイルを gate の `transcript_path` に使うと「読む前に通る」（codex 敵対的レビューの指摘、フィクスチャで再現済み）。**Skill ロードの判定は read の `tool_result` が成功したときに拡張が記録する**
- Claude Code の hook timeout 既定は 600 秒（公式 hooks docs）。`~/.claude/bin/*-gate.sh` は `transcript_path` が無いと fail-open
- pi の mcp.json は Claude の `mcpServers` 形式（`type: stdio/http` 付き）を無変換で読む（pi 公式 docs mcp.md「Copy the existing mcpServers entry」、pi の `loadMcpConfig` を `~/.claude.json` に適用して errors 0 を実測）。`pi mcp list` は未接続サーバーがあると exit 1
- pi の bash ツールは stdin を閉じて起動し、`run_in_background` は無い（codex-foreground-guard は毎回 `< /dev/null` を要求するだけで害は無い）

---

### Task 1: グローバル指示を pi ネイティブの context file に切り替える

**Files:**
- Delete: `dotfiles/.pi/agent/AGENTS.md`（git 追跡中・未コミット変更あり）
- Delete: `dotfiles/.pi/agent/extensions/claude-context.ts`（未追跡）
- Create: `dotfiles/.pi/agent/APPEND_SYSTEM.md`
- Modify: `dotfiles/.pi/agent/claude-extensions.test.mjs`（`resolveImports` の import と test を除去）
- Modify: `dotfiles/install.sh` pi 節（現在 `backup_and_link "$DOTFILES_DIR/.pi/agent/AGENTS.md"` と `mcp.json` の行）

**Interfaces:**
- Produces: `~/.pi/agent/CLAUDE.md -> dotfiles/.claude/CLAUDE.md`、`~/.pi/agent/APPEND_SYSTEM.md -> dotfiles/.pi/agent/APPEND_SYSTEM.md`

- [ ] **Step 1: 失敗する確認（現状: AGENTS.md が読まれ、CLAUDE.md は記録されない）**

```bash
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t1; mkdir -p $D && cd $D && pi -p "reply with just: ok" >/dev/null 2>&1
S=$(ls -t ~/.pi/agent/sessions/*/*.jsonl | head -1); grep -c 'Skill Routing' "$S"; grep -c 'Exception: reviewing code' "$S"
```
Expected: `0` と `1`

- [ ] **Step 2: APPEND_SYSTEM.md を作る**

内容（契約。これ以外は書かない）:
1. `# pi 固有の指示`
2. `## Exception: reviewing code` — 旧 AGENTS.md の節をそのまま移す
3. `## Claude Code との対応` — 「この後に載る `CLAUDE.md`（`/Users/mizoo/.pi/agent/CLAUDE.md`、実体は `~/.claude/CLAUDE.md`）は Claude Code 向けに書かれている。pi では次のように読み替える」として 4 項目:
   - `Skill(name)` / `Skill(plugin:name)` → その skill の `SKILL.md` を read する。pi の skill 名に plugin 接頭辞は無い。gate hook もこの read を「ロード済み」と判定する
   - `Agent(type)` → `subagent` ツールで `agent: "<type>"`。`subagent` が無ければ先に `subagents_enable` を呼ぶ（モデルにより最初はローダーだけが載る）。CLAUDE.md の Agent 指示は委譲の明示的な許可とみなす。`model:` による振り分けは無く default model を継承する   - LSP は pi-lens: 診断は `lens_diagnostics`、シンボル検索は `symbol_search` / `read_symbol`、定義・参照は `lsp_navigation`（既定無効。`pi_lens_activate_tools` で有効化すると次ターンから使える）。MCP ツール（`mcp__<server>__<tool>`）は直接は宣言されず、codemode / tool_search 経由で呼ぶ
   - pi に無いもの: Claude in Chrome（ローカル UI は webapp-testing、外部サイトの操作は不可）、Artifact、claude.ai コネクタ（Docs / Drive）、memory、Workflow、EnterPlanMode、`~/.claude/rules/`、WebSearch / WebFetch。該当する手順は飛ばすか bash で代替する

書かないもの（Opus レビューで削除）: agent 名の列挙（`advertise` と重複）、hooks の一覧（運用者向け、README へ）、`/skill:name`（ユーザー用コマンド）、同名 skill の例、`@RTK.md` の注記（`rtk proxy` は Exception 節にある）

- [ ] **Step 3: 旧 AGENTS.md の内容が移っていることを確認してから消す**

```bash
cd ~/dotfiles && grep -c 'Exception: reviewing code' .pi/agent/APPEND_SYSTEM.md && grep -c 'Claude Code との対応' .pi/agent/APPEND_SYSTEM.md
```
Expected: `1` と `1`。それを見てから（`-f` は使わない。作業ツリーの変更は APPEND に移したので追跡版に戻してから消す）:
```bash
cd ~/dotfiles && git restore .pi/agent/AGENTS.md && git rm -q .pi/agent/AGENTS.md && rm .pi/agent/extensions/claude-context.ts && rm ~/.pi/agent/extensions/claude-context.ts ~/.pi/agent/AGENTS.md
```
Expected: エラーなし。`git status --short .pi/agent/AGENTS.md` が `D `
`claude-extensions.test.mjs`: `import { resolveImports } …` 行と `test("resolveImports …")` ブロックを削除

- [ ] **Step 4: install.sh のリンク行を差し替える**

pi 節の `backup_and_link "$DOTFILES_DIR/.pi/agent/AGENTS.md" …` と `backup_and_link "$DOTFILES_DIR/.pi/agent/mcp.json" …` の 2 行を次に置き換える（`skills` と `extensions/*.ts` の行は維持。`agents` の行は Task 3 で差し替える）:
```bash
backup_and_link "$DOTFILES_DIR/.claude/CLAUDE.md" "$HOME/.pi/agent/CLAUDE.md"          # pi は agent dir の CLAUDE.md を context file として読む。AGENTS.md があるとそちらだけが読まれるので置かない
backup_and_link "$DOTFILES_DIR/.pi/agent/APPEND_SYSTEM.md" "$HOME/.pi/agent/APPEND_SYSTEM.md"
```
節頭のコメントの「pi install で入れる」4 行は Task 5 で節に置き換えるので、ここでは `mcp.json` の記述を「`~/.claude.json` から `scripts/setup-claude-code-mcp.sh` が写す（ローカル）」に直すだけ

- [ ] **Step 5: ローカルに適用する**

```bash
ln -sfn ~/dotfiles/.claude/CLAUDE.md ~/.pi/agent/CLAUDE.md && ln -sfn ~/dotfiles/.pi/agent/APPEND_SYSTEM.md ~/.pi/agent/APPEND_SYSTEM.md && ls -la ~/.pi/agent | grep -E 'CLAUDE|APPEND|AGENTS'
```
Expected: CLAUDE.md と APPEND_SYSTEM.md の symlink、AGENTS.md なし

- [ ] **Step 6: 確認が反転することを見る**

Step 1 と同じコマンド。Expected: `Skill Routing` が `1` 以上、`Exception: reviewing code` が `1`
```bash
cd ~/dotfiles && node --test .pi/agent/claude-extensions.test.mjs 2>&1 | grep -E '^ℹ (pass|fail)'
```
Expected: `pass 3` / `fail 0`

---

### Task 2: hooks 拡張 — Skill ロードの記録を read の成功時に移し、タイムアウトを Claude と揃える

**Files:**
- Modify: `dotfiles/.pi/agent/extensions/claude-hooks.ts`
- Modify: `dotfiles/.pi/agent/claude-extensions.test.mjs`（`toClaudePayload` の test を除去。残るのは `loadHooks` と `skillNamesFromPath` の 2 本）
- gate スクリプト（`~/.claude/bin/*-gate.sh`）は**変更しない**

**Interfaces:**
- Produces: hook 入力の `transcript_path` = `~/.pi/agent/claude-hooks/<sessionId>.jsonl`。空でも必ず存在する（gate は無いと fail-open）。行形式は gate の grep に合わせた `{"name":"Skill","input":{"skill":"<name>"}}` で、**read の `tool_result` が成功（`isError` でない）したときだけ**追記する

- [ ] **Step 1: 失敗する確認（現状: `tool_call` 時点で記録しているので、read が失敗しても gate が通る）**

```bash
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t2x; mkdir -p $D && cd $D && pi -p "Step 1: use the read tool to read /nonexistent/opencode-delegate/SKILL.md (it will fail; that is expected, do not retry).
Step 2: use the bash tool to run exactly: opencode run --help
Report in one line whether the bash call in step 2 was blocked or succeeded." 2>&1 | tail -1
```
Expected（現状）: succeeded ＝ 読めていないのに通る（これが直す対象）

- [ ] **Step 2: 拡張を直す**

契約（`claude-hooks.ts`）:
- `tool_call` から SKILL.md の判定と追記を削除。代わりに `tool_result` の先頭で `event.toolName === "read" && !event.isError` のとき `skillNamesFromPath(event.input.path)` を `transcript_path` に追記する（1 名 = 1 行）
- `skillNamesFromPath` は plugin 接頭辞の分岐を削除し、`basename(path) === "SKILL.md"` なら `[basename(dirname(path))]`、それ以外は `[]`（gate が見る 3 名はどれも接頭辞なし）
- `common()` は従来どおり marker ファイルを `mkdirSync` + `openSync(…, "a")` で必ず作る（fail-open 防止）
- `session_start` で `MARKER_DIR` 内の 7 日より古い `.jsonl` を削除する（溜まり続けないように。3 行程度）
- `DEFAULT_TIMEOUT_SEC = 600`（Claude Code の既定。「Claude Code の既定と同じ」のコメントは 60 が誤りだったので直す）
- `run()` は `spawn(..., { detached: true })` で起動し、タイムアウト時は `process.kill(-child.pid, "SIGKILL")` でプロセスグループごと止める（`child.pid` が無ければ `child.kill`）
- 先頭コメントを「transcript_path は拡張が書くセッション別ファイル。SKILL.md の read が成功した時点で記録する（pi のセッションファイルは呼び出しを実行前に記録するので使わない）」に直す
- 他（`loadHooks` / `toClaudePayload` / `tool_result` の additionalContext 追記 / SKIP）は変えない

- [ ] **Step 3: テストを直して通す**

`claude-extensions.test.mjs`: `toClaudePayload` の test と import を削除。`loadHooks` の既定タイムアウトの期待値を `60_000` → `600_000`（`timeout: 10` 側の `10_000` はそのまま）。`skillNamesFromPath` の test は接頭辞ケースを「`["test-driven-development"]` のみ」に直す。
```bash
cd ~/dotfiles && node --test .pi/agent/claude-extensions.test.mjs 2>&1 | grep -E '^ℹ (pass|fail)'
```
Expected: `pass 2` / `fail 0`

- [x] **Step 4: Step 1 の確認が反転する（read 失敗 → marker に記録されない）**

実施メモ: 「read 失敗後に必ず `opencode run --help` を叩け」と強制するプロンプトはモデルが従わない／長考するので、判定を 2 段に分けた。(a) read 失敗 + `echo hi` のセッションで marker ファイルが 0 バイトであること（session id は `~/.pi/agent/sessions/<cwd>/…_<id>.jsonl` の `<id>`）。(b) marker が空なら gate が拒否することは Step 5 の未ロード経路で確認済み。
```bash
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t2w; mkdir -p $D && cd $D && pi -p "Step 1: use the read tool to read /nonexistent/opencode-delegate/SKILL.md (it fails; expected, do not retry).
Step 2: use the bash tool to run exactly: echo hi
Reply with one line: whether step 1 failed and what step 2 printed." >/dev/null 2>&1
S=$(ls -t ~/.pi/agent/sessions/*t2w*/*.jsonl | head -1); ID=$(basename "$S" .jsonl | sed 's/.*_//'); wc -c < ~/.pi/agent/claude-hooks/$ID.jsonl; grep -c '"name":"read"' "$S"; grep -c '"name":"bash"' "$S"
```
Expected / 実測: `0`、read と bash がそれぞれ 1 以上（実測 0 / 2 / 2）。
注記: 検証中に pi を複数並行で走らせた時間帯に、全拡張ロード時だけ起動がハングした（`--mode json` でイベント 0 件）。拡張を単独・組み合わせでロードし直すとすべて正常、その後 default 構成でも 16 秒で完了したので一過性（MCP サーバー起動の競合が濃厚）と判断。拡張の欠陥ではない

- [ ] **Step 5: 未ロードは拒否、読了後は許可**

```bash
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t2a; mkdir -p $D && cd $D && pi -p "Use the bash tool to run exactly this command: opencode run --help
Then report the tool result text verbatim, nothing else." 2>&1 | grep -c 'Skill(opencode-delegate) をロードすること'
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t2b; mkdir -p $D && cd $D && pi -p "Step 1: use the read tool to read /Users/mizoo/.claude/skills/opencode-delegate/SKILL.md (first 20 lines only).
Step 2: use the bash tool to run exactly: opencode run --help
Report in one line whether the bash call in step 2 was blocked or succeeded." 2>&1 | tail -1
cat "$(ls -t ~/.pi/agent/claude-hooks/*.jsonl | head -1)"
```
Expected: `1`、succeeded、marker に `{"name":"Skill","input":{"skill":"opencode-delegate"}}` が 1 行

---

### Task 3: agents 生成を縮小し、生成物を git 管理から外す

**Files:**
- Modify: `dotfiles/scripts/claude-agents-to-pi.py`
- Delete: `dotfiles/.pi/agent/agents/`（未追跡、9 ファイル。`（非公開 agent）.md` は本人情報を含む）と `~/.pi/agent/agents` symlink
- Modify: `dotfiles/install.sh` pi 節（`backup_and_link … agents` の行）

**Interfaces:**
- Produces: `~/.pi/agent/agents/*.md`（7 本: branch-reviewer / demo-producer / investigate-deep / investigate-low / judge / task-reviewer / verify。ローカル、install.sh が生成）

- [ ] **Step 1: 失敗する確認（現状: 生成物が repo 内にあり、（非公開 agent） が含まれる）**

```bash
cd ~/dotfiles && ls .pi/agent/agents | wc -l && git check-ignore -q .pi/agent/agents/<非公開 agent のファイル名>.md; echo "ignored=$?"
```
Expected: `9` と `ignored=1`（除外されていない = コミットされうる）

- [ ] **Step 2: 生成スクリプトを行単位の置換に書き直す**

契約（`scripts/claude-agents-to-pi.py`、python3 標準ライブラリのみ）:
- `SRC = ~/.claude/agents`、`DST = sys.argv[1] if given else ~/.pi/agent/agents`
- `EXCLUDE = {"receipt-pipeline"}` — 理由をコメントに: claude.ai Drive コネクタ前提で pi では動かず、本番帳簿に書く
- 非公開の agent（`.git/info/exclude` 対象）は**名前を書かずに**除外する: `git_excluded(path)` が `path.resolve()`（`~/.claude` は symlink なので realpath に直す。symlink 経由の絶対パスは worktree 外扱いで判定が効かない）してから `git -C <dir> check-ignore -q <file>` を実行し、returncode 0 なら生成しない。git 管理外なら False。公開スクリプトに非公開 agent の名前や用途の手がかりを残さないため
- frontmatter は `split()` で切り出し、**行単位**で変換（YAML パーサは持たない。`|` ブロック・コメント・リストは pi-subagents が解釈する）:
  - `model:` 行、`color:` 行 → 削除
  - `tools:` 行 → 値を `,` で分割し `{"Read":"read","Grep":"grep","Glob":"find","Bash":"bash","Write":"write","Edit":"edit"}` で写像（未知名は落とす。`"*"` なら行ごと削除）
  - `skills:` ブロックの `- plugin:name` 項目 → `- name`
  - 先頭に `# generated by scripts/claude-agents-to-pi.py from <src> — edit the source, then re-run` と `advertise: true` を追加
  - それ以外の行（`name` / `description` のブロック含む）はそのまま
- 本文はそのまま
- `DST` を `mkdir -p` し、EXCLUDE と `git_excluded()` に該当しないものを書く。書いた名前を 1 行ずつ出力

- [ ] **Step 3: 生成物を repo から外し、ローカルに生成する**

```bash
cd ~/dotfiles && rm -rf .pi/agent/agents && rm ~/.pi/agent/agents && python3 scripts/claude-agents-to-pi.py && ls ~/.pi/agent/agents | wc -l && grep -L 'advertise: true' ~/.pi/agent/agents/*.md | wc -l && grep -l -E '^(model|color):' ~/.pi/agent/agents/*.md | wc -l && grep -c 'description: |' ~/.pi/agent/agents/demo-producer.md
```
Expected: `7`、`0`、`0`、`1`（ブロック記法がそのまま残る）

- [ ] **Step 4: install.sh の agents 行を生成呼び出しに差し替える**

`backup_and_link "$DOTFILES_DIR/.pi/agent/agents" "$HOME/.pi/agent/agents"` を次に置き換える:
```bash
python3 "$DOTFILES_DIR/scripts/claude-agents-to-pi.py"   # ~/.pi/agent/agents/ を .claude/agents から生成（pi-subagents 用。生成物は追跡しない。元を直したら再実行）
```

- [ ] **Step 5: pi-subagents で 7 本が見え、2 本が消えたことを確認**

```bash
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t3; mkdir -p $D && cd $D && pi -p "Call the subagents_enable tool. Then call the subagent tool with {\"action\":\"list\"}. Reply with only the comma-separated list of agent names it returned." 2>&1 | tr ',' '\n' | sed 's/^ *//' > $D/list.txt; grep -c -x -E 'branch-reviewer|demo-producer|investigate-deep|investigate-low|judge|task-reviewer|verify' $D/list.txt; grep -c -E 'receipt' $D/list.txt
```
Expected: `7` と `0`

---

### Task 4: MCP は `~/.claude.json` を正本にして pi へ写す

**Files:**
- Modify: `dotfiles/scripts/setup-claude-code-mcp.sh`（末尾 `claude mcp list` の前）

**Interfaces:**
- Produces: `~/.pi/agent/mcp.json` = `{"mcpServers": <~/.claude.json の .mcpServers>}`（ローカル。pi 専用エントリは持たない）

- [ ] **Step 1: 失敗する確認（現状: 2 つのファイルが独立）**

```bash
diff <(jq -S .mcpServers ~/.claude.json) <(jq -S .mcpServers ~/.pi/agent/mcp.json) >/dev/null; echo "same=$?"
```
Expected: `same=1`（pi 側は `type` を削り `description` を足した別物）

- [ ] **Step 2: スクリプト末尾に pi への反映を足す**

契約: `claude mcp list` の直前に追加。**一時ファイルに書いて `mv` で置き換える**（`>` は既存の symlink を辿る。未コミットの install.sh を走らせた環境には `~/.pi/agent/mcp.json → dotfiles/.pi/agent/mcp.json` が残りうるので、辿ると内部 URL が公開リポジトリに書かれる — codex 敵対的レビューの指摘）
```bash
# pi は Claude Code の mcpServers 形式をそのまま読む（pi docs mcp.md: "Copy the existing mcpServers entry"）。
# ~/.claude.json を正本にして丸ごと写す。pi 専用のエントリは持たない。
# 一時ファイル + mv: 旧 install.sh が張った symlink が残っていても辿らず置き換える（dotfiles に秘密が落ちない）。
# `pi mcp list` は未接続サーバー（mfc_ca はサインイン前）があると exit 1 するのでここでは呼ばない。
if command -v pi &> /dev/null && command -v jq &> /dev/null; then
    mkdir -p "$HOME/.pi/agent"
    pi_mcp_tmp=$(mktemp "$HOME/.pi/agent/mcp.json.XXXXXX")
    jq '{mcpServers}' "$HOME/.claude.json" > "$pi_mcp_tmp" && mv -f "$pi_mcp_tmp" "$HOME/.pi/agent/mcp.json"
    echo "✅ Copied mcpServers to pi: ~/.pi/agent/mcp.json (run 'pi mcp login mfc_ca' once for OAuth)"
fi
```
加えて `dotfiles/.gitignore` に `.pi/agent/mcp.json` を追加（多重防御。dotfiles 側にこのファイルが現れても追跡されない）

- [ ] **Step 3: symlink が残っている状況を再現して、辿らないことを確認する**

```bash
T=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t4; mkdir -p $T/repo $T/agent && : > $T/repo/mcp.json && ln -sfn $T/repo/mcp.json $T/agent/mcp.json
tmp=$(mktemp $T/agent/mcp.json.XXXXXX) && jq '{mcpServers}' ~/.claude.json > "$tmp" && mv -f "$tmp" $T/agent/mcp.json
test -L $T/agent/mcp.json; echo "still-symlink=$?"; wc -c < $T/repo/mcp.json
```
Expected: `still-symlink=1`（通常ファイルに置き換わった）、`0`（リポジトリ側は空のまま）

- [ ] **Step 4: 本番の反映と一致確認**

```bash
bash -c 'tmp=$(mktemp ~/.pi/agent/mcp.json.XXXXXX) && jq "{mcpServers}" ~/.claude.json > "$tmp" && mv -f "$tmp" ~/.pi/agent/mcp.json' && diff <(jq -S .mcpServers ~/.claude.json) <(jq -S .mcpServers ~/.pi/agent/mcp.json) >/dev/null; echo "same=$?"; grep -c 'mcp.json' ~/dotfiles/.gitignore; pi mcp list 2>&1 | grep -cE '^[a-z_-]+: (connected|needs sign-in)'
```
Expected: `same=0`、`1`、`4`（ms365 は npx の初回取得で遅いことがある。`connecting` のときは再実行）

- [ ] **Step 5: 秘密情報がリポジトリに無いことを確認（値は plan に書かない）**

```bash
cd ~/dotfiles && git grep -n -iE 'moneyforward' -- . ':!tasks/plan.md'; echo "exit=$?"; git grep -n -F "$(jq -r '.mcpServers.ms365.env.MS365_MCP_TENANT_ID' ~/.claude.json)" -- . ; echo "exit=$?"
```
Expected: テナント ID は出力なし `exit=1`（実測どおり）。URL の grep は **この plan 以前から** `.claude/skills/mail2mf/scripts/mf_api.py:33`（`MCP_URL` 定数）と `.codex/rules/default.rules:18`（`claude mcp add … mfc_ca <URL>` の allow ルール）に mfc_ca の内部 URL が含まれていた（`mail2mf/SKILL.md:583` の `box.moneyforward.com` は公開 Web UI の URL で対象外）。ユーザー指示で対応済み: `mf_api.py` は `mcp_url()` が `MFC_CA_MCP_URL` → `~/.claude.json` の `mcpServers.mfc_ca.url` の順で解決し（テスト 2 件追加、既存 suite も OK）、codex rule は URL 引数を落とした prefix に。追跡ファイルの worktree から URL は消えたが、**git 履歴 4 コミットには残る**（履歴書き換えはユーザー判断）

---

### Task 5: install.sh に pi packages の節を足し、README を更新する

**Files:**
- Modify: `dotfiles/install.sh`（Codex Plugins Setup 節の後に pi 節。pi 節頭のコメントから `pi install` 4 行を削る）
- Modify: `dotfiles/README.md`（`.pi` の行）

- [ ] **Step 1: 失敗する確認**

```bash
grep -c 'pi install' ~/dotfiles/install.sh
```
Expected: `1`（コメント内の 1 回だけ。実行する行は無い）

- [ ] **Step 2: Claude plugins 節と同型の任意節を追加**

契約: 見出し `pi Packages Setup`、`command -v pi` があるときだけ `read -p "Do you want to install pi packages now? (y/N): "`、y なら次を 1 つずつ `pi install`（pi は source で同一性を判定するので再実行は冪等）:
`git:github.com/obra/superpowers`、`git:github.com/DietrichGebert/ponytail`、`npm:pi-subagents`、`npm:pi-lens`（LSP 診断・定義・参照。Claude Code の typescript-lsp / pyright-lsp / gopls-lsp プラグインに相当。GitNexus はリポジトリ全体の構造・影響範囲で役割が別）
Claude plugins 節と同じく skip 時は「later with: pi install …」を echo

- [ ] **Step 2b: pi-lens をローカルに入れて LSP が動くことを確認**

```bash
cd ~ && pi install npm:pi-lens 2>&1 | tail -2
D=/private/tmp/claude-501/-Users-mizoo/a2505664-6f09-45fe-b8e7-160175d65c49/scratchpad/t5; mkdir -p $D && cd $D && printf 'const n: number = "x";\nexport {};\n' > bad.ts && pi -p "Run LSP diagnostics on ./bad.ts using the lens diagnostics tool and report the first diagnostic message in one line." 2>&1 | tail -3
```
Expected: `Installed npm:pi-lens`、診断に `Type 'string' is not assignable to type 'number'` 相当の文言。pi-lens は `typescript-language-server` / `pyright` / `gopls` を自動導入する（docs/dependencies.md）ので PATH の事前準備は不要。失敗時は `/lens-health` で原因を見る（推測で設定しない）
実施メモ: `bad.ts` だけのディレクトリでは 2 回とも「LSP check timed out」で tsls も入らなかった。`package.json` と `tsconfig.json` を置いた TS プロジェクト形にすると 37 秒で `bad.ts:1:7 — Type 'string' is not assignable to type 'number'.` を返し、tsls は `~/.pi-lens/tools/node_modules/` に入った。言語サーバーの自動導入はプロジェクト検出が前提

- [ ] **Step 2c: pi-lens の既定機能はそのまま受け入れる（ユーザー判断）**

pi-lens は既定で Biome / Ruff による自動フォーマット、autofix、書き込みのたびのテスト実行、read-before-edit ガードが有効（docs/features.md）。LSP だけに絞る設定（`~/.pi-lens/config.json`）は作らず、既定のまま使う。Claude 側の python-quality hook（PostToolUse）と Python の整形が二重に走りうる点は README に 1 行注記する

- [ ] **Step 3: README の `.pi` 行を書き直す**

内容: `CLAUDE.md`（`.claude/CLAUDE.md` への symlink、pi の context file）、`APPEND_SYSTEM.md`（pi 固有の読み替え）、`skills/`（`.claude/skills` への symlink）、`extensions/claude-hooks.ts`（Claude の PreToolUse / PostToolUse hooks を同じスクリプトで実行。foreground の子エージェントには掛からない）。ローカルで追跡しないもの: `agents/`（`scripts/claude-agents-to-pi.py` が生成）、`mcp.json`（`setup-claude-code-mcp.sh` が `~/.claude.json` から写す）、`settings.json`（deviceId）、`extensions/rtk.ts`（rtk init）。packages は install.sh の pi 節。pi-lens は既定設定のまま（自動フォーマット・autofix・書き込み時テスト込み。Python は Claude 側の python-quality hook と整形が二重になりうる）

- [ ] **Step 4: 構文確認**

```bash
bash -n ~/dotfiles/install.sh && echo ok && grep -c 'pi install' ~/dotfiles/install.sh
```
Expected: `ok` と `2`（for ループ 1 行 + skip 時の案内 1 行。実測 2）

---

### Task 6: コミット（ユーザー確認後）

**Files:** 上記の変更ファイルのみ（パス指定。他の未コミット差分は含めない）

- [ ] **Step 1: 差分を見せる**

```bash
cd ~/dotfiles && git status --short -- .pi .gitignore install.sh README.md scripts/claude-agents-to-pi.py scripts/setup-claude-code-mcp.sh
```
Expected: `.pi/agent/agents/` と `mcp.json` が含まれないこと、`.claude/bin/` に変更が無いこと

- [ ] **Step 2: ユーザーの GO を得てからコミット**

```bash
cd ~/dotfiles && git add .pi/agent/APPEND_SYSTEM.md .pi/agent/extensions/claude-hooks.ts .pi/agent/claude-extensions.test.mjs .gitignore install.sh README.md scripts/claude-agents-to-pi.py scripts/setup-claude-code-mcp.sh && git commit -m "pi: Claude Code の設定を pi ネイティブ機構で共有

- CLAUDE.md を context file として symlink、AGENTS.md と claude-context.ts を廃止
- pi 固有の読み替えは APPEND_SYSTEM.md へ
- hooks 拡張は Claude の hook を同じ契約で実行。Skill ロードは read 成功時に記録
- agents は .claude/agents から install 時に生成（追跡しない。Claude 専用の 2 本は除外）
- MCP は ~/.claude.json を正本に setup-claude-code-mcp.sh が pi へ写す（tmp + mv）
- install.sh に pi packages の節（pi-lens 含む）

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## 見送り（理由つき）

- `~/.claude/rules/*.md`: pi に相当機構なし。公式 example `claude-rules.ts` はプロジェクト側のみ・`paths:` 非対応。2 本とも `paths:` 付きで task-management は Claude の Task ツール前提
- AGENTS.md 正本化（Claude 公式の他ツール共有形）: codex の `~/.codex/AGENTS.md` にも 35KB が載り codex-review の挙動が変わりうる。ユーザー判断で CLAUDE.md 正本
- `~/.claude.json` を pi の mcp.json に symlink: pi が `/mcp` 操作で書き戻すため不可。jq で写す
- gate の `transcript_path` に pi のセッションファイルを渡す（Opus 提案）: pi は assistant message 内の全呼び出しを実行前に記録するため、同じ message に read と bash が並ぶと読む前に通る（codex 敵対的レビューで再現）。拡張が read 成功時に記録する方式を維持
- agents の無変換配置: `agentOverrides` で可能だが settings.json が dotfiles 非追跡なので採らない
- 子エージェントへの CLAUDE.md 継承: reviewer / judge の本文は自身のテンプレートで完結し、所在は `skills:` 経由で届く（ユーザー判断）
- `model:` → `thinking:` の写像: 効き方が未検証。後で必要なら 1 行
- pstack: ユーザー判断で pi / Claude Code / Codex のすべてからアンインストール済み（2026-11-08）。CLAUDE.md の pstack 行は削除し、codex 上限時の fallback は `Agent(judge)` に変更
- investigate-deep の `WebSearch` / `WebFetch`: pi core に web ツールが無く、tools の写像で落ちる。必要になったら pi-web-access 等の package を別途
- 子エージェントへの skill の渡し方の差: Claude Code は `skills:` の全文を起動時に注入するが、pi-subagents は名前・説明・location だけを渡し、子が read する。reviewer 本文の「Skill(...) をロード」は、子のプロンプトにある `<available_skills>` の指示（read で読め）で足りると判断。動かなければ APPEND 相当の 1 行を生成スクリプトで本文の先頭に足す
- 別解 `pi-code`（npm 1.7.0、約 8.8k DL/月）: Claude の hooks / `~/.claude/rules`（`paths:` 対応）/ `@import` / agents（`sonnet` 等の別名解決）/ `~/.claude.json` を 1 パッケージで読む。採らない理由: 独自の `subagent` ツールを登録するので pi-subagents と併用できない、hooks の transcript が pi のセッションファイル（codex が指摘した「実行前に通る」方式）、pi のネイティブ機構より互換層を優先する設計。将来 pi-subagents をやめるなら再評価
- pi の既定モデルを Anthropic に切り替えるときの注意: サブスク認証は追加課金になりうる（pi settings の `warnings.anthropicExtraUsage`）。subagent 1 体ごとに加算される
- hooks の SKIP 追加（codex-review-plan / codex-foreground-guard）: pi の既定モデルを Claude に切り替える予定なので codex-review は別系統レビューとして残す。foreground-guard は `< /dev/null` を要求するだけで害が無い
- pi の既定モデルの Claude への切り替え（`/login anthropic` → settings の `defaultProvider` / `defaultModel`）: この plan の後にユーザーが行う
- pi-subagents は `~/.agents` を user agent dir としても読み、`create` の書き込み先にもする（公開 dotfiles 配下）。pi から agent を作らない限り影響なし — 注意点として記録のみ
