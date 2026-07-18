# mail2mf skill 設計書

日付: 2026-07-18
ステータス: codex レビュー(gpt-5.6-sol)通過済み・ユーザーレビュー待ち

## 目的

Mac の Mail.app に届く決済系メール(領収書・請求書などの PDF 付き)から PDF を抽出し、
マネーフォワード クラウドBox にアップロードして、MF 内蔵の OCR・仕訳候補・自動照合に乗せる。
さらに決済明細(連携サービス明細)との突合レポートを出力する。
`/mail2mf` skill として提供し、ユーザーが任意のタイミングで実行する。

## 背景と技術的制約(調査済み・動作確認済み)

- クラウド会計の API / MCP には**仕訳へ証憑ファイルを添付するフィールドが存在しない**
  (証憑添付 API はクラウド会計Plus 専用)。PDF が仕訳に紐付く唯一のルートは
  **クラウドBox 経由の MF 内蔵連携**(OCR → 仕訳候補 → 承認時に証憑添付)。
  よって本 skill は「Box アップまで自動 + 突合レポート」を守備範囲とし、仕訳作成は行わない。
- MF 公式ベータ MCP(`mfc_ca`)は Claude Code の動的登録クライアントに
  `mfc/accounting/transaction.read` を付与しないため接続不可(2026-07-18 実測)。
  対策として**自前の OAuth クライアントを DCR 登録済み**(client_name: `mail-pdf-to-mf`、
  会計12 + Box 2 の全14スコープ付与を確認)。このトークンで MCP エンドポイントの
  initialize / tools/call が通ることを確認済み。
- Box API: `POST https://api.box.moneyforward.com/v1/files`(multipart、
  スコープ `mfc/box/files.write`)。`GET /v1/files` で一覧取得。**実トークンで 200 確認済み**。
- 決済明細の取得: MCP ツール `mfc_ca_getTransactions`(連携サービス明細)。
- 認証情報(client_id / client_secret / refresh_token)は macOS Keychain の
  service `mail2mf-mfc`(account: `mizoo`)に JSON で保存済み。

## 構成

```
~/.claude/skills/mail2mf/        # dotfiles リポジトリで管理(.claude/skills/ 配下)
├── SKILL.md                     # ワークフロー定義(Claude への手順指示)
└── scripts/
    ├── scan_mail.py             # Mail.app スキャン → PDF付きメール候補を JSON 出力
    └── mf_api.py                # 認証リフレッシュ / Box アップロード / 明細取得
```

- 実行状態: `~/.local/state/mail2mf/state.json`(アップロード済み管理・前回実行時刻)
- PDF 一時保存: `~/.local/state/mail2mf/downloads/`
- 秘匿情報: Keychain のみ。リポジトリ・state に平文保存しない。

## 実行フロー(SKILL.md が Claude に指示する手順)

1. **スキャン**: `scan_mail.py scan --since <日付>` を実行。
   初回(state なし)は既定で過去3ヶ月、以降は前回スキャン時刻以降。ユーザーが期間を
   指定した場合はそれを優先。さらに state.json の `failed`(過去の失敗分)を期間に
   かかわらず候補へ再投入する。出力は JSON(message_id, 受信日時, 差出人, 件名,
   PDF 添付ファイル名の配列, 本文プレビュー先頭1000文字, 本文から正規表現で拾った
   金額候補の配列)。PDF 添付のあるメールのみ機械抽出する。
2. **判定**: 候補一覧を Claude が読み、決済系(領収書・請求書・利用明細等)か否かを
   意味的に分類。**分類結果を表で提示し、ユーザーの承認を得てから**次へ進む
   (毎回必須。誤アップロード防止のゲート)。
3. **抽出・リネーム**: `scan_mail.py extract --out <dir> <message_id>...` で承認された
   メールの PDF 添付を AppleScript(`save attachment`)経由で `downloads/` に保存し、
   保存済みパスの JSON を返す。ファイル名は
   `YYYYMMDD_<差出人ドメイン>_<元ファイル名>_<hash8>.pdf`。`hash8` は添付キー
   (後述: `<message_id>/<添付順位>-<添付名>`)の sha256 先頭8文字で、同一メール内の
   同名添付を含め衝突を決定的に回避する(同一添付は常に同名になるため、
   Box 側 file_name 照合による重複スキップも安全)。
4. **アップロード**: `mf_api.py upload <file>...` で Box へ。重複防止は二段:
   state.json の添付キー記録と、Box 側 `GET /v1/files` の file_name 照合。
5. **突合レポート**: `mf_api.py transactions --from <日付> --to <日付>` で決済明細を取得し、
   Claude がスキャン JSON のメール由来情報(日付・差出人・金額候補)と突合して
   「対応あり / **証憑なし決済** / 明細なし証憑」の3分類 Markdown レポートを会話内に出力。
6. **state 更新**: 成功・失敗を**1件ずつ**確定する(下記「state と再試行」)。

仕訳の確定は MF 画面(仕訳候補の承認)で行う。skill はレポート末尾で該当画面への
導線を案内する。

## state と再試行

`~/.local/state/mail2mf/state.json` の構造と更新規則:

```json
{
  "last_scan": "2026-07-18T20:00:00+09:00",
  "pending":   { "<添付キー>": {"subject": "...", "sender": "...", "date": "..."} },
  "uploaded":  { "<添付キー>": {"file_id": "...", "at": "..."} },
  "failed":    { "<添付キー>": {"error": "...", "at": "..."} },
  "discarded": { "<添付キー>": {"at": "..."} }
}
```

**添付キー** = `<message_id>/<添付順位>-<添付名>`(添付順位は AppleScript が返す
mail attachment の並び順で 1 始まり)。同一メール内に同名添付が複数あっても
キーが衝突しない。1添付=1エントリ。ライフサイクルは `pending → uploaded | failed`。

- **スキャン時**: 発見した候補(PDF 添付のある全メールの全添付)をまず `pending` に
  追記して state を書き出し、**その後で** `last_scan` をスキャン実行時刻に進める。
  この順序により、直後にクラッシュしても候補は `pending` に残っており、期間フィルタに
  かかわらず次回の候補一覧に再掲される(取りこぼしゼロ)。
- **アップロード時**: 1件成功するごとに `pending` から `uploaded` へ移して即座に
  state を書き出す(チェックポイント)。失敗は `failed` へ移す。
- **次回スキャン時**: `pending` と `failed`(permanent 以外)の全件を期間フィルタと
  無関係に候補一覧へ再掲する(失敗分は失敗理由を添えて表示)。ユーザーが「非決済」と
  判定した候補は `pending` から `discarded` へ移す(墓標)。`discarded` にあるキーは
  期間が重なる再スキャンでも候補に再登場しない。
- 402/413 など再試行しても無意味なものは `failed` に `permanent: true` を付け、
  候補への自動再投入はせずレポートにのみ記載する。

## スクリプト仕様

共通: Python 3 標準ライブラリのみ(外部依存ゼロ)。エラーは stderr + 非0終了。

### scan_mail.py

- `--since <ISO日付>` 必須。Mail.app の受信トレイを AppleScript(osascript)で
  `date received >= since` フィルタ付き走査し、PDF 添付を持つメールのみ JSON Lines 出力。
- 受信トレイ約14万通のため、AppleScript の `whose` 句でフィルタして転送量を抑える。
  それでも遅い場合がある(実測次第)。改善余地は Envelope Index(SQLite)直読みだが、
  フルディスクアクセス権限が必要になるため v1 では採用しない(ponytail: 既知の天井)。

### mf_api.py

サブコマンド:

- `refresh` — Keychain から資格情報を読み、`POST https://api.biz.moneyforward.com/token`
  (grant_type=refresh_token)でアクセストークン取得。refresh_token がローテートされた
  場合は Keychain を更新。アクセストークンはプロセス内のみで保持(ディスク保存しない)。
- `upload <file>...` — Box へ multipart POST。201 の file_id を stdout に返す。
- `list-box [--limit N]` — Box ファイル一覧(重複チェック用)。
- `transactions --from <date> --to <date>` — MCP エンドポイントに JSON-RPC で
  initialize → `mfc_ca_getTransactions` を呼び、明細 JSON を返す。
- `auth-url` — 再認可用の authorize URL を生成(PKCE S256)。生成した
  `code_verifier` と `state` は Keychain の service `mail2mf-mfc-pkce` に一時保存する
  (ディスク平文には置かない)。
- `auth-exchange <callback_url>` — コールバック URL から `code` と `state` を取り出し、
  Keychain の一時エントリと `state` が一致することを検証(不一致は中断・エントリ破棄)。
  一致したら保存済み `code_verifier` でトークン交換し、`mail2mf-mfc` を更新、
  一時エントリを削除する。トークン完全失効時の復旧路。

## エラー処理

- refresh が `invalid_grant`(失効)→ `auth-url` による再認可手順を Claude が案内
  (URL 提示 → ユーザーがブラウザで許可 → localhost コールバック URL を貼り付け →
  `auth-exchange`)。
- Box 429 → `Retry-After` に従い1回リトライ。402(容量超過)/413(サイズ超過)は
  該当ファイルをスキップしてレポートに記載。
- Mail.app のオートメーション権限エラー → システム設定の該当画面を案内。
- 明細取得失敗時はアップロードまでで完了とし、レポートは「突合スキップ」と明記。

## テスト(TDD、Cursor 実装)

- scan_mail.py: AppleScript 出力パーサの単体テスト(フィクスチャ文字列)。
- mf_api.py: HTTP 層をモックした refresh(ローテーション含む)/ upload / transactions の
  単体テスト。state 重複判定のテスト。
- E2E スモーク: 実 Box へ 1 ファイルアップロードし一覧で確認(手動・実装完了時に1回)。

## セキュリティ

- 秘匿情報は Keychain のみ(service `mail2mf-mfc`)。ログ・stdout にトークンを出さない。
- アップロード前のユーザー承認を必須ゲートとする。
- アップロードは追加のみ(削除 API は実装しない)。

## 実装フロー

CLAUDE.md の SDD に従う: 本ブランチ `feat/mail2mf-skill` 上で、writing-plans →
Cursor(`cursor-grok-4.5-medium-fast`)+ TDD で実装 → タスクレビュー → ブランチレビュー。

## スコープ外(YAGNI)

- 仕訳の自動作成(API 制約により証憑が添付されず、MF 仕訳候補と二重化するため)
- PDF 本文の OCR / 金額抽出(MF 側 OCR が本命。メール本文からの抽出のみ)
- launchd 等による定期実行(必要になったら追加)
- Mail.app 以外のメールソース(Gmail API 等)
