# mail2mf skill 設計書

日付: 2026-07-18(2026-07-19 スキャン/抽出方式を改訂)
ステータス: 実装中。スキャン/抽出を AppleScript から Envelope Index(SQLite)+ .emlx 直読みへ改訂

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
- **メールのスキャンは Mail.app の Envelope Index(SQLite)直読み**で行う(2026-07-19 改訂)。
  当初の AppleScript(JXA)`whose` フィルタは、実機の受信トレイ約14万通に対して
  Mail 側のフィルタ評価が重く AppleEvent タイムアウト(-1712)で完走しないことを実測で確認。
  Envelope Index を読めば日付・差出人・件名・添付名が index 済みで数 ms で絞れる。
  DB: `~/Library/Mail/V10/MailData/Envelope Index`。**ロックする read-only 接続**
  (`file:<path>?mode=ro`, uri=True)でライブ DB を直接開く。WAL モードの SQLite は
  リーダーに(直近コミット時点の)一貫スナップショットを返し、ライター(Mail)を
  ブロックしない。`immutable=1`(WAL 無視で取りこぼしの恐れ)や、本体と `-wal`/`-shm` を
  個別コピーする方式(非アトミックで不整合になり得る)は使わない。`last_scan` の前進は
  **読み取りが正常完了した後にのみ**行う。**フルディスクアクセス(FDA)権限が必要**
  (端末アプリに付与。付与済み前提)。
- **PDF 実体は Mail がダウンロード済みの `.emlx` からのみ抽出できる**。実機では添付を
  自動 DL しない設定のため候補が全て `.partial.emlx`(本体未 DL、`X-Apple-Content-Length`
  だけ在る)であることを実測。よって抽出は「Mail に先に DL させて disk から取る」方式:
  対象メールを Mail で開く/選択して DL 済みにする(または Mail 設定で添付を全 DL)→
  `.partial.emlx` が full `.emlx` になった後、Python が `.emlx` を直接パースして PDF を取り出す。
  未 DL の添付は抽出時に「Mail で DL してから再実行」と明示する(Apple Events は使わない)。

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

1. **スキャン**: `scan_mail.py scan [--since <日付>]` を実行。
   初回(state なし・`--since` なし)は既定で**今年の1月1日**から、以降は前回スキャン
   時刻以降。ユーザーが期間を指定した場合はそれを優先。さらに state.json の `pending` と
   `failed`(permanent 以外)を期間にかかわらず候補へ再投入する。Envelope Index を
   `date_received >= cutoff` かつ PDF 添付ありで絞り、各メッセージの `.emlx` を読んで
   RFC Message-ID・本文プレビュー・PDF パート一覧を得る。出力は JSON(`since` と
   `candidates` 配列: message_id〔RFC〕, 受信日時, 差出人, 件名, PDF 添付名+添付順位,
   本文から正規表現で拾った金額候補)。Gmail のラベル重複は RFC Message-ID で dedup する。
2. **判定**: 候補一覧を Claude が読み、決済系(領収書・請求書・利用明細等)か否かを
   意味的に分類。**分類結果を表で提示し、ユーザーの承認を得てから**次へ進む
   (毎回必須。誤アップロード防止のゲート)。
3. **抽出・リネーム**: `scan_mail.py extract --out <dir> <message_id>...` で承認された
   メールの PDF 添付を、対応する `.emlx`(scan 時に state へ記録した path)を Python で
   パースして `downloads/` に保存し、保存済みパスの JSON を返す。ファイル名は
   `YYYYMMDD_<差出人ドメイン>_<元ファイル名>_<hash8>.pdf`。`hash8` は添付キー
   (後述: `<message_id>/<添付順位>-<添付名>`)の sha256 先頭8文字で、同一メール内の
   同名添付を含め衝突を決定的に回避する(同一添付は常に同名になるため、
   Box 側 file_name 照合による重複スキップも安全)。**PDF パートに実体が無い場合
   (`.partial.emlx` = Mail 未 DL)は抽出せず、「Mail で対象メールを開いて DL してから
   再実行」というエラーを返す**(該当添付は failed〔非 permanent〕として再試行対象に残る)。
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
  "pending":   { "<添付キー>": {"subject": "...", "sender": "...", "date": "...", "amounts": []} },
  "uploaded":  { "<添付キー>": {"file_id": "...", "at": "..."} },
  "failed":    { "<添付キー>": {"error": "...", "at": "..."} },
  "discarded": { "<添付キー>": {"at": "..."} },
  "sources":   { "<message_id>": <ROWID(整数)> }
}
```

**添付キー** = `<message_id>/<添付順位>-<添付名>`。`message_id` は RFC Message-ID
(`.emlx` ヘッダ由来。無い場合は `rowid:<ROWID>` を代用)。添付順位は `.emlx` の MIME
パートを walk した順で、ファイル名を持つパート中の 1 始まり。同一メール内に同名添付が
複数あってもキーが衝突しない。1添付=1エントリ。ライフサイクルは `pending → uploaded | failed`。

**sources**: `message_id` → Envelope Index の **ROWID(安定キー)**。scan 時に記録する。
`.emlx` の絶対パスは保存しない — `.partial.emlx` は DL 後に full `.emlx` へ名前が変わり
path が陳腐化するため。extract は毎回 `build_emlx_index()` で ROWID→現在の `.emlx` パスを
再解決する(full を partial より優先)。scan と extract は別プロセスなので state が受け渡し役。

- **スキャン時**: 発見した候補(PDF 添付のある全メールの全添付)をまず `pending` に
  追記し、その message_id → `.emlx` path を `sources` に記録して state を書き出し、
  **その後で** `last_scan` をスキャン実行時刻に進める。
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

Mail の実データ源: `~/Library/Mail/V10`。Envelope Index(`MailData/Envelope Index`)を
`sqlite3` の**ロックする read-only 接続**(`file:<path>?mode=ro`, uri=True)でライブ DB を
直接開く(WAL 一貫スナップショット。`immutable=1` や個別ファイルコピーは不可)。
`last_scan` は読み取りが正常完了した後にのみ前進させる。以下の表を使う:
`messages`(ROWID, sender→addresses.ROWID, subject→subjects.ROWID, date_received〔epoch〕,
deleted), `attachments`(message→messages.ROWID, name), `addresses`(address), `subjects`(subject)。

サブコマンド:

- `scan [--since <ISO日付>] [--state PATH]` — cutoff を決め(`--since` > state.last_scan >
  既定=今年1/1)、**添付を持つメッセージ**を次の SQL で引く(PDF 判定は名前でなく
  `.emlx` の MIME で行うため、拡張子 `.pdf` でない `application/pdf` も取りこぼさない):
  ```sql
  SELECT DISTINCT m.ROWID, m.date_received, ad.address, s.subject
  FROM messages m
  JOIN attachments a ON a.message = m.ROWID
  LEFT JOIN addresses ad ON ad.ROWID = m.sender
  LEFT JOIN subjects  s ON s.ROWID = m.subject
  WHERE m.date_received >= :cutoff AND m.deleted = 0;
  ```
  各 ROWID について `.emlx` を `build_emlx_index()`(後述)で解決し `read_emlx()` でパース、
  `emlx_message_id()`(RFC Message-ID)・本文プレビュー(text/plain 先頭1000字)・
  `pdf_parts()`(ファイル名を持つパート中 PDF のみ、1始まり index + 名前)を得る。
  PDF パートが無いメッセージは候補にしない。`.emlx` が未在/解析不可のメッセージは skip し、
  その受信時刻まで last_scan を巻き戻して次回再スキャン(添付順位を DB 名から捏造しない)。
  RFC Message-ID で dedup(Gmail ラベル重複対策、先勝ち)。`build_candidates()`(Task 5)に
  渡して pending 追記・`sources` 記録 → save → last_scan は**クエリ前に捕捉した scan_started**
  へ前進(未解決があればさらに巻き戻し)→ 候補 JSON(`{"since":..., "candidates":[...]}`)を stdout。
- `extract --out DIR [--state PATH] <message_id>...` — `plan_extract_targets()`(Task 5)で
  対象添付を得、各 message_id を `sources` の ROWID 経由で現在の `.emlx` へ再解決し
  `read_emlx()`→`pdf_parts()`。実体があれば `final_name()` で `--out` に保存し
  `{"<添付キー>": "<保存パス>"}` を stdout。**実体が無い(partial)/ ROWID が sources に
  無い / `.emlx` が見つからない場合は該当添付を skip し stderr にメッセージ+非0終了**
  (Mail で DL してから再実行する旨)。
- `mark` / `discard` — Task 5 のまま。

内部関数(純粋部は単体テスト対象):
- `build_emlx_index(mail_root) -> {ROWID(str): path}` — `os.walk` で `<ROWID>.emlx` /
  `<ROWID>.partial.emlx` を1回で index 化。full を partial より優先。
- `read_emlx(path) -> email.message.Message` — 先頭行(本文バイト数)を除き
  `email.message_from_bytes` でパース。
- `emlx_message_id(msg) -> str` / `pdf_parts(msg) -> [(index, name, payload|None)]`
  (`payload=None` は未 DL)。
- FDA 権限なしで Envelope Index が開けない/読めない場合は、システム設定 > プライバシーと
  セキュリティ > フルディスクアクセス で端末アプリに許可する旨の明確な SystemExit。

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
- FDA 権限なしで Envelope Index を開けない → システム設定 > プライバシーとセキュリティ >
  フルディスクアクセス で端末アプリに許可する旨を案内(明確な SystemExit)。
- 添付が未 DL(partial)→ 該当添付を skip し「Mail で対象メールを開いて DL 後に再実行」を
  案内、failed(非 permanent)として再試行対象に残す。
- 明細取得失敗時はアップロードまでで完了とし、レポートは「突合スキップ」と明記。

## テスト(TDD、Cursor 実装)

- scan_mail.py(実 Mail.app / 実 SQLite / 実 FS を使わず、すべてフィクスチャで):
  - Envelope Index クエリ: 一時 SQLite に `messages`/`attachments`/`addresses`/`subjects` の
    最小スキーマを作り、cutoff・PDF 絞り込み・deleted 除外・join を検証。
  - `build_emlx_index()`: 一時ディレクトリに `<ROWID>.emlx` と `<ROWID>.partial.emlx` を
    置き、full 優先・ROWID→path 解決を検証。
  - `read_emlx()` / `emlx_message_id()` / `pdf_parts()`: 先頭バイト数行付きの `.emlx`
    フィクスチャ(base64 PDF パート + partial パート)で、RFC Message-ID 抽出・PDF パート
    列挙・partial(payload=None)判定を検証。
  - `extract`: sources の ROWID を一時 `.emlx` に再解決し、full なら保存・partial なら
    skip+非0、sources 欠落や未検出も非0 を検証(実体保存は一時 FS で確認)。
  - 純粋ロジック(state/amounts/candidates)は Task 5 の既存テストで担保。
- mf_api.py: HTTP 層をモックした refresh(ローテーション含む)/ upload / transactions の
  単体テスト。state 重複判定のテスト。
- E2E スモーク: 実 Box へ 1 ファイルアップロードし一覧で確認(合成 PDF・要ユーザー承認・
  実装完了時に1回)。実 Envelope Index からの scan もこの段で1回確認する。

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
