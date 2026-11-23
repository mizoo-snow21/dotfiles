# pi 用の指示

計画・実装・レビュー・デバッグの進め方は pstack（`poteto-mode`）が決める。このファイルには、進め方に関係なく常に守ることだけを書く。Claude Code 用のルール（`~/.claude/CLAUDE.md`）は pi では読み込まない。

## 返答

ユーザーへの返答は日本語で書く。

## 安全

- コードを書く前に、main から作業ブランチを切る（`feat/<名前>`、`fix/<名前>`）。
- force-push・削除・上書きは、実行する内容を先に見せてからフォアグラウンドで実行する。
- 自分のリポジトリ（`mizoo-snow21/*`）では、commit・push・PR 作成・マージ・マージ済みブランチの削除まで、確認を待たずに続けて進める。削除するものは実行と同じ返答で示す。
- 作業ブランチでは既存のモデルだけを使う。マイグレーション・テーブル・カラム・スキーマファイルが必要になったら、手を止めて提案する。
- 作業の退避はコミットで行う。`git stash` は他のセッションの退避と混ざるので使わない。
- 次の操作は、対応する skill を読んでから行う。

| 操作 | skill |
|---|---|
| force-push、merge、rebase、作業ツリーの書き換え、コミットのステージ、worktree の追加・削除、ブランチがマージ済み・プッシュ済みかの判断 | `git-safety` |
| 秘密情報・認証情報・API キーの取得 | `secret-handling` |
| 本番の複数レコードの一括処理、本番の共有リソースの変更 | `bulk-production-ops` |

## 実行と報告

- 手の届くコマンドは自分で実行する。ブロックされたら、何に止められたかを伝えて実行してよいか尋ねる。`! <command>` を渡すのは、対話ログインなどユーザーの手が要るときだけ。
- コミット・PR・デプロイ・削除の完了報告は、同じターンで実物を確認し（`git log -1`、`gh pr view <n>`、`ls`）、コミットハッシュか PR の URL を添える。
- 動いている UI について報告するときは、操作のたびに画面を取り直し、その表示だけを根拠にする。小さな文字・数字・チェック状態は拡大して読む。
- バックグラウンドで起動したものは、起動時に何をいくつ起動したかを伝え、結果が届くたびに要点を報告する。

## コードを調べる道具

問いに答えられる一番狭い道具を選ぶ。

- シンボルの定義・参照・型・診断: pi-lens（`symbol_search`、`read_symbol`、`lens_diagnostics`、`lsp_navigation`）
- リポジトリ全体の構造・実行フロー・変更の影響範囲: GitNexus（`gitnexus-impact-analysis` skill）
- 場所が分かっているファイル: read
- 文字列・設定・ログ・コメント: rg

## Python

- 依存・環境・実行は uv で扱う（`uv add` / `uv remove` / `uv sync` / `uv run`）。単体スクリプトは inline metadata か `--script` を使う。
- プロジェクトの Python の版は `uv python pin <版>` で決める（`.python-version` に書かれる）。mise の python はプロジェクト外の既定だけに使う。

## UI/UX

- 説明はレイアウトに任せ、補助ラベルや説明文は足さない。
- どの要素もユーザーの目的に役立つものだけにする。スローガン、装飾、入れ子のカード、情報の繰り返しは置かない。
- 説明文は異常な状態か必要な操作にだけ出し、補足は折りたたみの奥に置く。
- 既存の画面に揃える。足すより削る。一部を変えるためにページ全体を作り直さない。

## 進め方以外の skill

| 場面 | skill |
|---|---|
| GitHub issue の作成・更新 | `github-issues` |
| ローカルの UI・フロントエンドの確認、スクリーンショット | `webapp-testing` |
| PR や issue に画像を貼る | `github-pr-attachments` |
| Word 文書に入る内容 | `word-clipboard` |
| セッションの締め・引き継ぎ | `handover` |
| skill の新規作成・評価 | `skill-creator` |
| CLAUDE.md・AGENTS.md・SKILL.md の文章の編集 | `writing-for-agents` |

## pi 固有

- bash は rtk 拡張が自動で rtk 経由に書き換え、出力を圧縮する。レビューやデバッグで差分・ログを精読するときは `rtk proxy git diff` / `rtk proxy git show` のように `rtk proxy` を付けて全文を読む。
- skill が Claude Code 専用の機能（Claude in Chrome、Artifact、WebSearch / WebFetch、memory、`~/.claude/rules/`）を指すときは、bash で代替するか、その手順を飛ばす。
