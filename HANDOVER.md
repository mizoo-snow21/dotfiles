# HANDOVER

作成: 2026-08-12（Headroom の導入・実測・撤去と、その過程で見つかった Cursor 設定の問題）

## Current Objective

完了。追加作業は残っていない。このドキュメントは「なぜ Headroom を入れて消したか」と
「Cursor 設定まわりで何を直したか」を次回に渡すためのもの。

## Completed

**Headroom（トークン圧縮プロキシ）: 導入 → 実測 → 撤去**

- デスクトップ版 cask を導入したが、セットアップウィザード完了前に削除（OSS CLI 版に切替）
- OSS CLI 版を mise（`pipx:headroom-ai`, extras=all）で導入し、launchd 常駐プロキシ
  `127.0.0.1:8787` を立てて Claude Code / Codex を配線（`5cfea96`）
- 実測の結果、割に合わないと判断して完全撤去（`dafc192`）
- `ENABLE_TOOL_SEARCH` のみ復活（`7031077`）

**Cursor 設定の修復（Headroom 調査の副産物）**

- `~/.cursor/cli-config.json` の allowlist から消えていた `Shell(rtk)` を復元
- `install.sh` の `.cursor` リンクを `commands/` `rules/` だけに縮小（`4a1e087`）
- `~/.cursor/commands` `~/.cursor/rules` を dotfiles への symlink 化（実機に適用済み）
- `~/.cursor` の残骸（`cli-config.json.bad` + `.tmp` × 7）を削除

## In Progress / Not Finished

なし。ただし **Claude Code を一度終了して再起動するまで、現行セッションは
`ANTHROPIC_BASE_URL` を環境にキャッシュしたまま**（設定ファイル上は既に消えている）。

## Decisions

- **Headroom を継続しない**: 実測（210リクエスト / 15分）でメッセージ圧縮は **0.7%**、
  圧縮由来の節約 $0.31 に対し、プレフィックスキャッシュ由来の節約が **$76.96**。
  全リクエストに平均 **217ms**（p95 718ms）の遅延が乗る。0.5% の削減の対価として
  「故障点1つ（8787 が落ちると Claude Code と Codex が両方止まる）＋ 保守対象6つ ＋
  `/remote-control` の無効化」は割に合わない。
- **`--mode cache` は正解だが、正解ゆえに圧縮がほぼ効かない**: 過去ターンを凍結して
  キャッシュを守る＝書き換え対象が最新ターンだけになる。`token` モードは 25〜35% 削るが
  キャッシュを飛ばすので純損（キャッシュ読みは通常入力の 1/10 価格）。
- **効かない構造的理由は rtk との競合**: rtk が PreToolUse フックで、コンテキストに
  入る前に先に削っている。Headroom は削り済みの中身を見ることになる。上流で削るほうが
  優れている（キャッシュとも干渉しない）。
- **`ENABLE_TOOL_SEARCH` だけ残した**: Headroom が自分の成果として計上していた
  「ツールスキーマ 664k 削減」は Claude Code 側の機能。導入前から有効だった（＝Headroom の
  増分ではない）が、env var があるほうが確実なので残す。
- **`~/.cursor` 全体の symlink 化は却下**: 下記 Pitfalls 参照。

## Pitfalls / Lessons

- **Cursor は `cli-config.json` を temp + rename で書く。したがってこのファイルを
  symlink にしてはいけない** — rename はパスを置き換えるので、Cursor が1回書いた時点で
  symlink が実ファイルに戻る。「管理しているつもり」だけが残る。
  ディレクトリの symlink（`commands/` `rules/` `skills/`）は書き込みが通り抜けるので安全。
- **`~/.cursor` を丸ごと `backup_and_link` に渡してはいけない** — `rm -rf` してから
  張るので `chats/` `projects/` `agents/` `plans/` が消える。2025-10-17 に追加された
  この行は一度も走っていなかった（`~/.cursor` の inode 誕生時刻が 2025-08-29 のまま）ため
  たまたま無事だった。`4a1e087` で縮小済み。
- **`Shell(rtk)` が消えた原因は末尾カンマの手編集**（Headroom でも install.sh でもない）。
  `cli-config.json.bad` に `["Shell(ls)", "Shell(rtk)", "Shell(git)", "Shell(pytest)",
  "Shell(uv)",]` が残っていた。Cursor が読めずに初期設定を作り直し、巻き添えで全部消えた。
  → **この種のファイルは JSON 妥当性を確認してからアトミックに差し替えること**
  （`install.sh` の python ブロックは `json.dumps` なので安全）。
- **Cursor は起動しっぱなしになりやすい**: 8/8 21:44 から4日間、フォルダ未オープンの
  空ウィンドウ（`[8:empty-window]`）が動き続けていた。設定を書き換える前に
  `pgrep -f Cursor.app` を必ず確認する。起動中に書くと終了時に上書きされる。
- **`grep -c` を `pgrep -f` の代わりに使うと誤検知する**: Cursor ヘルパーは環境変数 PATH に
  ツールのパスを含むため、`pgrep -f headroom` が Cursor を拾う。実体の有無は
  実行ファイルパスで判定すること。
- **シェルのダブルクォート内で `$HOME` / `$PATH` を含む文字列を grep すると展開されて
  偽陰性になる**。実際にこの確認で「PATH export が消えた」と誤報告した。

## Verification

**検証済み（実測 / コマンド出力で確認）**

- Headroom 痕跡ゼロ: `~/.claude/settings.json` / `.zshrc` / `.zprofile` /
  `~/.codex/config.toml` / `AGENTS.md` / `hooks.json` / `~/.cursor/cli-config.json` すべて 0件
- dotfiles repo 全ファイル（gitignore 対象含む）に headroom 参照なし
  ※ `debugpy` の C ヘッダにある `int recursion_headroom;` は無関係
- port 8787 free / LaunchAgent なし / プロセスなし / `/Applications/Headroom.app` なし
- `~/.codex/config.toml` と `.config/mcp/codex.config.toml.local` がバイト単位一致
  （後者は gitignore 対象で見落としやすい。最後に発見して除去した）
- rtk 0.45.0 稼働 / claude hook 1件 / cursor allowlist `["Shell(ls)", "Shell(rtk)"]`
- `install.sh` `bash -n` OK / `.zshrc` `zsh -n` OK / TOML 2ファイル妥当
- 作業ツリークリーン、`main...origin/main` 同期

**未検証**

- `Shell(rtk)` が Cursor の書き込みサイクルを越えて残るか。追加後に Cursor が
  `cli-config.json` を書き戻していないため、永続性は未確認。
- headless の `cursor-agent` で allowlist が実際に効くか。`approvalMode = "allowlist"`
  かつ 8/8〜8/12 は `Shell(rtk)` 不在でも委譲が成功していたため、`--trust` が承認を
  迂回している可能性が高いが、実験していない。

## Next Steps

1. Claude Code を再起動して `ANTHROPIC_BASE_URL` のキャッシュを落とす
2. （任意）`~/.cursor/rules/ponytail.mdc` が `alwaysApply: true` なので、今後 Cursor の
   全セッションに ponytail が効く。意図と違えば `rules` のリンクを外す
3. Headroom を再検討する気になったら、まず判断材料は上の Decisions を読む。
   再導入するなら `uv tool install --python 3.13 "headroom-ai[all]"`、
   撤去は `headroom install remove` → `headroom unwrap claude` → `headroom unwrap codex`
   （`unwrap` はツールごとに1コマンド。まとめ書き不可）

## Important Files

- `install.sh`: 89〜95行目付近の `backup_and_link`。`.cursor` は commands/rules のみ
- `.config/mise/config.toml`: ツール定義。pipx バックエンドの extras は
  `{ version = "latest", extras = "all" }` 形式（`pipx:pkg[all]` 記法は無視される）
- `.config/mcp/codex.config.toml.local`: gitignore 対象。grep から漏れるので注意
- `.claude/settings.json`: rtk フックと `ENABLE_TOOL_SEARCH` の在処
- `~/.cursor/cli-config.json`: dotfiles 管理外（symlink 不可のため）。allowlist はここ

## 関連コミット

```
7031077 chore(claude): ENABLE_TOOL_SEARCH を戻す
dafc192 chore: Headroom OSS の導入設定を取り除く
4a1e087 fix(install): .cursor を丸ごとリンクせず commands/rules だけに絞る
5cfea96 feat(headroom): OSS CLI 版の Headroom を導入する
```
