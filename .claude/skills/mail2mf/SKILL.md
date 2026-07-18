---
name: mail2mf
description: Mail.app の決済系メール(PDF 証憑付き)をマネーフォワード クラウドBox へアップロードし、決済明細との突合レポートを出す。「決済メールをマネフォに」「証憑アップロード」「mail2mf」等で起動。
---

# mail2mf — 決済メール証憑 → クラウドBox 連携

スクリプト: このファイルと同じディレクトリの `scripts/scan_mail.py` と `scripts/mf_api.py`。
以降 `SKILL_DIR` = このファイルのあるディレクトリ。

スキャンは Envelope Index(SQLite)を read-only で直読み(Apple Events 不使用・高速)。
抽出は AppleScript(`osascript`)で Mail に添付を save させる(未 DL の添付も自動 DL される・
Gmail のラベル重複も回避)。**フルディスクアクセス(FDA)権限が必要**。
認証情報は macOS Keychain(`mail2mf-mfc`)。

## 手順

### 1. スキャン

```bash
python3 "$SKILL_DIR/scripts/scan_mail.py" scan
```

- 既定範囲は今年の1月1日から(state があれば前回スキャン以降)。ユーザーが期間を
  指定した場合のみ `--since YYYY-MM-DD` を付ける。
- 出力 JSON の `candidates` が空なら「新しい候補なし」と報告して手順 4 へ。

### 2. 判定と承認(必須ゲート)

candidates の各件を**意味的に**分類する: 決済系(領収書・請求書・利用明細・
注文確認に伴う適格請求書など)か、非決済(広告・物件情報・ニュースレター等)か。
金額候補(`amounts`)・件名・差出人を根拠に判断する。

- 結果を表で提示: | 判定 | 件名 | 差出人 | 日付 | 金額候補 | status |
- `status` が `failed_retry` の行は失敗理由も表示する。
- **ユーザーの承認を得るまでアップロードしない。**
- 非決済と判定されユーザーが同意した候補は pending から除去:
  `python3 "$SKILL_DIR/scripts/scan_mail.py" discard <key>...`

### 3. 抽出とアップロード

承認された候補について message_id ごとに:

```bash
python3 "$SKILL_DIR/scripts/scan_mail.py" extract --out ~/.local/state/mail2mf/downloads "<message_id>" ...
python3 "$SKILL_DIR/scripts/mf_api.py" upload <保存されたファイル>...
```

- extract は AppleScript で Mail に添付を save させる(1メッセージ ~50s。未 DL 本体も
  自動 DL される)。**Mail.app が起動している必要がある**。extract がエラー(非0)を返す
  のは「メッセージが Mail 内で見つからない/対象添付が無い/タイムアウト」の場合で、
  その添付は failed(非 permanent)として残り再試行対象。Mail を起動して再実行すればよい。
- upload の結果 JSON を見て 1 件ずつ state を確定する:
  - 成功: `scan_mail.py mark --key "<key>" --uploaded <file_id>`
    (証憑メタ〔金額・日付・差出人・件名〕は uploaded エントリに保存され、後日の突合に使える)
  - 失敗: `scan_mail.py mark --key "<key>" --failed "<error>"`(402/413 は `--permanent` 付き)
- アップロード前に必要なら `mf_api.py list-box --limit 200` で同名ファイルの有無を確認し、
  既に存在するものはアップロードせず mark --uploaded で消し込む(file_id は一覧のもの)。

### 4. 突合レポート

```bash
python3 "$SKILL_DIR/scripts/mf_api.py" transactions --from <期間開始> --to <今日>
```

明細(決済)とアップロード済み証憑を突合し、Markdown レポートを出す。証憑側は
state.json の `uploaded` エントリ(各キーに保存された金額・日付・差出人・件名)を証憑集合と
みなす(今回アップ分だけでなく過去にアップ済みの分も含めて突合できる):

- **対応あり**: 明細と証憑が金額±0・日付±3日で一致(取引内容と差出人の意味一致も加味)
- **証憑なし決済**: 対応する証憑が見つからない明細(`journalizing_statuses` が
  `none` のものは「未仕訳」と明記)
- **明細なし証憑**: どの明細とも一致しない証憑

レポート末尾に必ず添える案内:
「仕訳の確定はマネーフォワード クラウド会計の [自動で仕訳 > 連携サービスから入力] と
[クラウドBox の仕訳候補] 画面で承認してください。証憑の添付はこのルートでのみ行われます。」

### 5. エラー対応

- `refresh token expired` → `mf_api.py auth-url` で URL を生成しユーザーに提示 →
  ブラウザで許可後、`localhost:3118` のエラーページの URL を貼ってもらい
  `mf_api.py auth-exchange "<callback_url>"`。
- Envelope Index が開けない/フルディスクアクセス未許可 → システム設定 > プライバシーと
  セキュリティ > フルディスクアクセス で端末アプリ(Ghostty 等)に許可するよう案内。
- extract がメッセージ未検出/タイムアウトで失敗 → Mail.app が起動しているか確認し再実行。
  該当添付は failed(非 permanent)で残るので再試行対象。
- MCP/明細取得の失敗 → アップロードまでで完了とし、レポートは「突合スキップ」と明記。

## 注意

- 実行状態は `~/.local/state/mail2mf/state.json`(pending/uploaded/failed/discarded/sources/skipped)。
  手順 4 の突合ではこの `uploaded` を証憑集合として読む。
- 秘匿情報は Keychain(`mail2mf-mfc`)。トークンや client_secret を表示・保存しない。
- Box への削除操作は存在しない(アップロードのみ)。誤アップは MF 画面から削除してもらう。
