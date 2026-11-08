# pi 固有の指示

## Exception: reviewing code

コードレビューやデバッグで差分・ログを精読するときは圧縮しないこと。
`rtk proxy git diff` / `rtk proxy git show` を使い、`rtk git diff` は使わない。
bash は rtk 拡張 (`extensions/rtk.ts`) が自動で rtk に書き換えるため、明示的に `rtk proxy` を付けないと圧縮される。

## Claude Code との対応

この後に載る `CLAUDE.md`（`~/.pi/agent/CLAUDE.md`、実体は `~/.claude/CLAUDE.md`）は Claude Code 向けに書かれている。pi では次のように読み替える。

- `Skill(name)` / `Skill(plugin:name)` → その skill の `SKILL.md` を read する。pi の skill 名に plugin 接頭辞は無い。gate hook もこの read を「ロード済み」と判定する
- `Agent(type)` → `subagent` ツールで `agent: "<type>"`。`subagent` が無ければ先に `subagents_enable` を呼ぶ（モデルにより最初はローダーだけが載る）。CLAUDE.md の Agent 指示は委譲の明示的な許可とみなす。`model:` による振り分けは無く default model を継承する
- LSP は pi-lens: 診断は `lens_diagnostics`、シンボル検索は `symbol_search` / `read_symbol`、定義・参照は `lsp_navigation`（既定無効。`pi_lens_activate_tools` で有効化すると次ターンから使える）。MCP ツール（`mcp__<server>__<tool>`）は直接は宣言されず、codemode / tool_search 経由で呼ぶ
- pi に無いもの: Claude in Chrome（ローカル UI は webapp-testing、外部サイトの操作は不可）、Artifact、claude.ai コネクタ（Docs / Drive）、memory、Workflow、EnterPlanMode、`~/.claude/rules/`、WebSearch / WebFetch。該当する手順は飛ばすか bash で代替する
