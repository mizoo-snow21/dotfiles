---
name: mail2mf
description: Upload payment-related email evidence (PDF receipts/invoices) from Mail.app to Money Forward Cloud Box and reconcile against payment transactions. Trigger on "決済メールをマネフォに", "証憑アップロード", "mail2mf", "upload receipts to Money Forward", etc.
---

# mail2mf — Payment email evidence → Money Forward Cloud Box

Scripts live next to this file: `scripts/scan_mail.py` and `scripts/mf_api.py`.
Below, `SKILL_DIR` = the directory containing this file.

Scanning reads Mail's Envelope Index (SQLite) directly, read-only (no Apple Events — fast
even on huge inboxes). Extraction opens each message via a `message://` URL so Mail
auto-downloads the attachments, then picks them up from `Attachments/<ROWID>/`
(works for not-yet-downloaded and archived mail; ~15s per message).
**Full Disk Access (FDA) is required** for the terminal app.
Credentials live in the macOS Keychain (service `mail2mf-mfc`).

## Procedure

### 1. Scan

```bash
python3 "$SKILL_DIR/scripts/scan_mail.py" scan
```

- Default range is January 1 of the current year (or since the last scan when state
  exists). Add `--since YYYY-MM-DD` only when the user specifies a range.
- If the output JSON's `candidates` is empty, report "no new candidates" and go to step 4.

### 2. Classify and get approval (mandatory gate)

Classify each candidate **semantically**: payment-related (receipt, invoice, usage
statement, qualified invoice attached to an order confirmation, …) vs. non-payment
(ads, real-estate listings, newsletters, …). Base the judgment on the amount
candidates (`amounts`), subject, and sender.

- Present the result as a table: | verdict | subject | sender | date | amounts | status |
- For rows with `status: failed_retry`, also show the failure reason.
- **Never upload before the user approves.**
- For candidates judged non-payment that the user agrees to drop, remove them from
  pending: `python3 "$SKILL_DIR/scripts/scan_mail.py" discard <key>...`

### 3. Extract and upload

For each approved message_id:

```bash
python3 "$SKILL_DIR/scripts/scan_mail.py" extract --out ~/.local/state/mail2mf/downloads "<message_id>" ...
python3 "$SKILL_DIR/scripts/mf_api.py" upload <saved files>...
```

- Extraction opens the message via `message://` so Mail auto-downloads the attachment
  bodies, then polls `Attachments/<ROWID>/` (~15s per message, 90s timeout; `open`
  launches Mail automatically). On failure (non-zero exit), the stderr message tells
  you what to do — the scripts emit these literal Japanese strings:
  - `sources に ... がありません(再スキャンしてください)` → run `scan` again
  - `Attachments バケットを解決できません` / `Attachments 照合タイムアウト/曖昧` →
    usually resolved by re-running; if it persists, open that mail in Mail.app, then retry
  - `Mail で該当メール(件名)を開いてから再実行してください` → rare mail without an
    RFC Message-ID; open it manually in Mail.app as instructed, then retry
  In all cases the attachment stays in `failed` (non-permanent) and will be retried.
- Duplicate check before upload (last line of defense if state is lost): filenames are
  deterministic (derived from the attachment key), so for each file to be uploaded run
  `mf_api.py list-box --name "<final_name>"` — a server-side exact-name search
  (`file_name` filter, verified against the real API; independent of pagination limits).
  On a hit, skip the upload and settle it with that file_id via `mark --uploaded`.
  **Mandatory for every file when the state is new or was rebuilt**; optional otherwise
  (the state's attachment-key record is the primary defense).
- Settle state one item at a time from the upload result JSON:
  - success: `scan_mail.py mark --key "<key>" --uploaded <file_id>`
    (evidence metadata — amount/date/sender/subject — is preserved on the uploaded
    entry for later reconciliation)
  - failure: `scan_mail.py mark --key "<key>" --failed "<error>"` (add `--permanent`
    for 402/413)

### 4. Reconciliation report

```bash
python3 "$SKILL_DIR/scripts/mf_api.py" transactions --from <range start> --to <today>
```

Reconcile transactions (payments) against uploaded evidence and output a Markdown
report. The evidence set is the state file's `uploaded` entries (each carries amount /
date / sender / subject), so evidence uploaded in past runs is included too:

- **Matched**: transaction and evidence agree on amount ±0 and date ±3 days
  (also weigh semantic match of description vs. sender)
- **Payments without evidence**: transactions with no matching evidence
  (mark those with `journalizing_statuses: none` as "未仕訳" / not yet journalized)
- **Evidence without payment**: evidence matching no transaction

Always end the report with this guidance:
「仕訳の確定はマネーフォワード クラウド会計の [自動で仕訳 > 連携サービスから入力] と
[クラウドBox の仕訳候補] 画面で承認してください。証憑の添付はこのルートでのみ行われます。」
(Journal entries are finalized in Money Forward Cloud Accounting's journal-candidate
screens; PDF attachment to journal entries happens only through that route.)

### 5. Error handling

- `refresh token expired` → generate a URL with `mf_api.py auth-url` and show it to the
  user → after they approve in the browser, have them paste the `localhost:3118` error
  page URL and run `mf_api.py auth-exchange "<callback_url>"`.
- Envelope Index unreadable / FDA not granted → tell the user to grant Full Disk Access
  to the terminal app (Ghostty etc.) in System Settings > Privacy & Security.
- Extraction failures → follow the stderr table in step 3 (rescan / retry / open the
  mail in Mail.app). The attachment stays in `failed` (non-permanent) for retry.
- Transactions/MCP fetch failure → finish at the upload stage and mark the report as
  "reconciliation skipped".

## Notes

- Runtime state: `~/.local/state/mail2mf/state.json`
  (pending/uploaded/failed/discarded/sources/skipped). Step 4 reads `uploaded` as the
  evidence set.
- Secrets stay in the Keychain (`mail2mf-mfc`). Never display or store tokens or the
  client_secret.
- There is no delete operation for Box (upload only). If something is uploaded by
  mistake, the user removes it in the MF Box UI.
