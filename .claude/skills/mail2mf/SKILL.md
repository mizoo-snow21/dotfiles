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
# Span the WHOLE evidence set, not just the latest scan window. Start 3 days BEFORE the
# earliest uploaded-evidence date (min of state `uploaded[*].date` minus 3 days, so the
# ±3-day match rule can still reach transactions that predate the evidence; fall back to
# the fiscal-year start), through today. Using the scan range here would falsely flag
# older evidence (uploaded in past runs) as unmatched.
python3 "$SKILL_DIR/scripts/mf_api.py" transactions --from <earliest evidence date − 3d> --to <today>
```

Reconcile transactions (payments) against uploaded evidence and output a Markdown
report. The evidence set is the state file's `uploaded` entries (each carries amount /
date / sender / subject), so evidence uploaded in past runs is included too — which is
why the query window above must cover all of them.

Match **one-to-one**: consume each transaction and each evidence item at most once.
Payment emails are full of identical amounts (six PROGRIT charges of ¥21,780, several
Anthropic $110), so amount alone is not a key.

- **Matched**: a *unique* transaction↔evidence pair agreeing on amount ±0 and date
  ±3 days. When candidates collide on amount+date, disambiguate by receipt number /
  exact payment date / vendor before pairing; if still ambiguous, list them under
  "needs manual matching" instead of auto-pairing.
- **Payments without evidence**: transactions left unpaired
  (mark those with `journalizing_statuses: none` as "未仕訳" / not yet journalized)
- **Evidence without payment**: evidence left unpaired

End the report by pointing the user to the next step. Attaching evidence and creating
journals is a separate, opt-in phase — see **"Journalizing & attaching evidence"** below.
(Note: a Box file can be attached to *any* existing journal from the 仕訳帳 paperclip, not
only through the auto-journal candidate screens.)

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

## Journalizing & attaching evidence

Steps 1–4 stop at the report. This phase (attaching evidence to journals, or creating
journals) is **opt-in** — only when the user asks. Every account-changing action here is
financial: do it in the foreground and confirm before writing. Learned the hard way:

**Trust the PDF's printed date, not the email date.** Vendors (Stripe) re-send old
receipts in batches, so the email date can be months off — even a different tax year. Read
the printed payment date (`pdftotext -layout <receipt>.pdf | grep 支払い日`) and use it to
match the receipt to the right charge and to catch resent-receipt cases. It is *not*
automatically the journal's 計上日: expense recognition follows the accounting method
(発生主義 = delivery/service completion) and the journal date should line up with the card
charge you attach to. (Real case: five PROGRIT receipts for 2025-03…07 were all re-emailed
on 2026-02-25; dating the journals by email put them in the wrong fiscal year and they had
to be deleted.)

**Find the existing card journal before creating anything.** A connected business card
already auto-journalizes each charge (借 expense / 貸 未払金). Search 仕訳帳 by **amount**
(値 filter) — the card descriptor (摘要) for one vendor changes over time (Anthropic =
"CLAUDE.AI SUBSCRIPTION" early, "ANTHROPIC* CLAUDE SUB" later), so a vendor-name filter
silently misses rows. Attach evidence to that journal. Create a manual entry
(借 expense / 貸 事業主借) only for charges the feed never captured — and re-check by amount
first so you don't duplicate a fed charge.

**Let the JCT number *flag* the invoice class — it does not decide it.** Extract any
number: `pdftotext -layout <pdf> | grep -Eo 'T[0-9]{13}'`. A T-number on the receipt is a
strong signal the vendor is registered (often → 課仕10%適格, full credit; e.g. Anthropic
T7700150134388, O'Reilly T7011101004246); its absence on a foreign receipt is a signal it
may be non-qualified (often → 課仕10% 80%控除 経過措置; e.g. Anomaly, VoiceInk/Polar). This is
only a starting heuristic: a registration number alone doesn't settle invoice
eligibility, and foreign / digital-service purchases (電気通信利用役務, reverse-charge,
whether it's even a 国内取引) can need an entirely different consumption-tax treatment.
Surface the number and your guess, and confirm the actual 税区分 with the user / their
税理士 rather than setting it blindly. The number lives on the retained receipt, not in a
per-journal field; MF card auto-journals default 課仕10% to 適格, so foreign/unregistered
vendors are the ones to review.

**Attaching (UI):** 仕訳帳 → paperclip in the 証憑 column → panel → ファイルを追加 →
クラウドBoxから選択 → filter (substring match; use the receipt number e.g. `2235-8792` or the
date prefix `20260708`) → tick → 添付. The user wants the **領収書 only** — detach any
請求書/Invoice via the file's ⋮ → 添付解除 (no confirm dialog). The "仕訳への添付=未添付"
filter hides already-attached files (prevents double-assignment) but also hides a
mis-attached one, so always verify each journal's attached receipt matches on date+amount
(a July-7 receipt once sat on the July-8 journal while July-7 was empty).

**Deleting a journal** fires a native `confirm()` that freezes the browser extension. Only
after the user approves exactly which 取引No to delete, inject `window.confirm = () => true`
(javascript tool), then delete one at a time in the foreground; re-inject after any page
navigation.

**Not every payment email is an expense — classify direction.** A 支払通知書 from a client is
*sales*, not expense, evidence. If it carries **your** 登録番号, the required 適格請求書 fields
(取引年月日・内容・税率ごとの対価と消費税額 …) and you've confirmed it (相手方の確認), it can stand
in as your self-billed qualified invoice (支払通知書/仕入明細書方式) so you needn't issue a
separate one — but verify those conditions rather than assuming; a payment notice is not
automatically a compliant qualified invoice. Book it as sales (借 売掛金 / 貸 sales account)
at the supply's actual 税区分 — commonly 課税売上10%, but confirm it isn't 軽減8%, 非課税,
免税(輸出), or 対象外 before posting — and keep it in Box (電帳法, 授受区分 = 受領). 見積書/契約書 are not evidence; personal
buys are skipped. Recognize 売上 on 発生主義 (役務提供完了), not on receipt — but first check
how the book already records sales: this user's bank feed auto-posts 借 普通預金 / 貸 売上金
at receipt, so a manual 売掛金 accrual would double-count at payment. Match the book's
existing sales account name (here **売上金**, not 売上高).

## Notes

- Runtime state: `~/.local/state/mail2mf/state.json`
  (pending/uploaded/failed/discarded/sources/skipped). Step 4 reads `uploaded` as the
  evidence set.
- Secrets stay in the Keychain (`mail2mf-mfc`). Never display or store tokens or the
  client_secret.
- There is no delete operation for Box (upload only). If something is uploaded by
  mistake, the user removes it in the MF Box UI.
