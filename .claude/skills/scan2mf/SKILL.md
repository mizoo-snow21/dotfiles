---
name: scan2mf
description: Read scanned paper receipts out of a Google Drive folder, skip the ones already booked, and take the rest into Money Forward — upload to クラウドBox, match against card transactions, journalize, attach. Trigger on レシート確認して / スキャンした領収書お願い / 紙の領収書マネフォに入れて / 経費登録して, whenever the user pastes a Drive folder link, and whenever they mention scanned receipts, レシート画像, 紙の領収書, or 領収書フォルダ — ask for the folder link if they did not give one. Email-borne PDF receipts are a different job — use mail2mf for those.
---

# scan2mf — Drive のスキャン領収書 → マネーフォワード

Paper receipts photographed or scanned into a Drive folder, handed over as a link. The job is
to read them, work out which ones are already in the books, and take only the remainder
through to a journal with its evidence attached.

Money Forward access reuses mail2mf's script: `~/.claude/skills/mail2mf/scripts/mf_api.py`
(`upload`, `list-box --name`, `transactions`). Journals and transactions come from the
`mcp__mfc_ca__*` tools. Read mail2mf's **"Journalizing & attaching evidence"** section before
you write anything to the ledger — the account-selection traps, the 一括登録 warning, the
`postJournals` gross-amount rule and the UI attach procedure all live there and are not
repeated here.

## 1. Enumerate the files

Ask the user for the folder link if they haven't given one — receipts usually accumulate in a
single standing folder, so it's worth asking whether it's the same one as last time rather than
making them dig up the URL.

That folder typically sits in a personal account the Drive MCP cannot see, so `search_files`
with `parentId` comes back empty even though `get_file_metadata` on the folder id works. Don't
conclude the folder is empty. Ask the user to set 一般的なアクセス to
**リンクを知っている全員（閲覧者）** — sharing is normally off, so expect to ask each time — then
read the file ids out of Drive's plain listing view in the browser:

```
https://drive.google.com/embeddedfolderview?id=<FOLDER_ID>#list
```

`read_page` with `filter: "interactive"` gives one `/file/d/<ID>/view` href per row. The list
lazy-loads, so scroll to the bottom and read again, then union both passes — a first read that
stops short looks exactly like a complete one. Cross-check the count against `get_page_text`
on the same page before moving on.

Say plainly that link sharing exposes the receipts to anyone holding the URL, and remind the
user to set it back to 制限付き once you're done reading.

## 2. Read each receipt

`read_file_content` on the file id returns Drive's OCR text, which handles photographed
receipts that have no text layer at all. Pull out 日付 / 金額 / 店名 / 登録番号(T+13桁) /
支払方法.

Two things are worth distrusting in that text:

- **A file that returns no usable text** is an image-only scan Drive couldn't read. Download it
  (`download_file_content` → base64, or `curl -sL "https://drive.google.com/uc?export=download&id=<ID>"`
  while link sharing is on), confirm with `pdftotext -layout f.pdf - | tr -d '[:space:]' | wc -c`
  returning 0, render with `pdftoppm -png -r 300 -f 1 -l 1 f.pdf out`, and read the PNG.
- **登録番号 and long digit strings are where OCR fails quietly.** One receipt's number came
  back as `170105010230` — wrong length, silently. Crop and magnify that line (`pdftoppm -r 500`,
  then crop; thermal receipts often print it sideways so rotate) and read it digit by digit
  before you record it. A T-number is 13 digits after the T.

Record the **printed** payment method too. A receipt saying 現金支払 is cash even if the user
remembers paying by app — two taxi receipts printed 現金支払 while the user believed they were
GO card payments, and no card charge existed for either amount.

## 3. Drop the ones already booked

Most of a long-lived receipt folder is already in the ledger. Filenames cannot tell you which:
MF's own uploads are named by a different scheme (`PXL_…jpg`, `電帳法_8_2607310735.pdf`) than the
scanner's (`スキャン_20260731-0927.pdf`), and the timestamps don't line up either.

Match on content instead. Pull journals covering the whole span of receipt dates
(`getJournals`, widen to the earliest printed date) and treat a receipt as already booked when
a journal exists with **the same amount and a transaction date within ±3 days**. In one run this
retired 18 of 28 receipts, every one of them already carrying its evidence. Report what you
skipped and why, so the user can see the judgement rather than just the survivors.

## 4. Find each remaining receipt's payment

Query `getTransactions` across **all** connected accounts for a window spanning the receipt
dates, then pair on **amount and date**. Resist matching by merchant name: the card descriptor
and the shop name routinely disagree — `Wolfgang's Steakhouse 虎ノ門` bills as
`ウルフギャング ステーキハウス丸の内`, `株式会社WOOC` as `IIOFFICE`. Name matching also hides
charges that are present, which is worse than finding nothing.

Query by amount rather than by name when hunting a specific receipt (`side` + `value_min` /
`value_max`), and search every account before declaring a receipt unmatched — a per-card query
will miss a charge that landed on a different card.

Three outcomes, and they need different handling:

- **Card charge found** → journalize from the feed so the entry links to the transaction.
- **Printed 現金** → no charge will ever appear; a manual journal is the only route.
- **Nothing found and not cash** → the feed may simply not have caught up. Check how far the
  account has actually synced (the newest transaction date for that account) before calling it
  missing, and leave it pending rather than inventing an entry.

Watch for a receipt total that exceeds the card charge. Points cover the gap — a ¥15,072 meal
settled as ¥12,072 on the card plus ¥3,000 of ホットペッパー points. Book the charge, and raise the
difference with the user rather than silently booking either figure as the expense.

## 5. Upload, journalize, attach

Upload only the receipts that survived step 3, checking each name against Box first
(`list-box --name`, which is an exact-name server-side search — the endpoint caps `limit` at 100
and cannot page, so an inventory scan proves nothing). Give files a self-describing name like
`20260803_wolfgangs_76549.pdf`; you will be matching them by eye in the attach dialog later.

Then journalize per mail2mf's rules — card charges through 連携サービスから入力, cash through
`postJournals` (借 旅費交通費 / 貸 事業主借, gross amounts on both sides) — and attach each Box
file to its journal via 仕訳帳 → 証憑 paperclip → クラウドBoxから選択 → filter by filename → 添付.

Verify through the API, not the screen: re-read the journal and confirm `voucher_file_ids` holds
the id you meant, that the computed `tax_value` equals the tax printed on the receipt, and that
no file got attached twice. The tax check is the strongest signal you picked the right 税区分 —
¥800 → 72, ¥76,549 → 6,959, both matching their receipts exactly.

## Report

Close with a table of what was booked (仕訳No / 日付 / 金額 / 借方 / 消費税 / 支払手段), a list of
what was skipped as already-booked, and a list of what is still pending with the reason
(feed not synced, ambiguous match, amount discrepancy). Then remind the user to revoke the
Drive link sharing.
