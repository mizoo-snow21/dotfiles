---
name: word-clipboard
description: Use when content needs to land in a Microsoft Word document with formatting intact — pasting tables, headings, or Japanese text into an open Word doc via the macOS clipboard, editing a document in Word for the web / Word Online (OneDrive or SharePoint) through the browser, or patching an existing .docx directly. Trigger on Wordに貼り付け, Word文書に反映・更新, Word Online, Word for the web, OneDrive上のdocxを直す, 目次を更新, クリップボード経由でWordへ, RTF, docx patching, or any deliverable whose final destination is a Word document, even if the user only says "Wordに入れて". Also read it before deciding how to deliver a multi-part change to a Word document — it covers choosing a route per item and checking file ownership before committing to a file swap.
---

# Word Clipboard / Docx Delivery

Two verified routes for getting generated content into Microsoft Word on macOS. Both were proven in production (2026-07-23/24, D365 manual work); the pitfalls below were hit for real.

## Choose the route

| Situation | Route |
|---|---|
| User has the Word doc open / manages it themselves; you hand over a fragment (a chapter, a table) for them to ⌘V | **Route A: clipboard as RTF** |
| You must update a `.docx` file programmatically (replace a table, renumber cross-references) without the user pasting anything | **Route B: patch the docx** |
| The document lives in Word for the web (OneDrive/SharePoint) and you are driving the browser yourself | **Route C: edit in Word Online** |

Rule of thumb: interactive handoff → A. File-in, file-out → B. You are at the keyboard in the browser → C.

### Pick the route per item, not per job

This is the expensive lesson from 2026-08-06. A job usually contains several independent changes. When one of them turns out to be impossible on the route you started with, the reflex is to move the *whole job* to another route. Resist it — re-check each remaining item separately, because most of them are still doable the easy way.

What happened: four changes were requested (TOC depth, restructure a part, add two chapters, move a chapter). The TOC depth change cannot be saved in Word Online, so everything got rerouted to "patch the docx locally and swap the file." Only after the local work was finished did the file turn out to be owned by someone else and unswappable. Hours went into a local HTTP receiver, blob downloads, a base64 round-trip and a REST API — while three of the four changes could have been done in ten minutes by pasting, a route already proven in the same document days earlier. Going back to it only happened because the user insisted.

Two habits prevent the repeat:

- **Before choosing a route that ends in replacing the file, confirm you can actually replace it.** Owner and write permission is a 30-second check (OneDrive 共有 view shows "◯◯ さんのファイル"; a shared item's context menu has no upload/replace entry). Do it first, not after the work.
- **When a route dies, re-list the remaining items and ask which ones the original route still handles.** Blocked ≠ blocked for everything.

## Route A: HTML → RTF → clipboard

Word pastes RTF as real structure (table cells, heading styles). Plain text via `pbcopy` loses all of it — that is the failure this route exists to avoid.

### 1. Author HTML — charset declaration is NOT optional

```html
<html><head><meta charset="utf-8"></head><body>
<h2>章タイトル</h2>
<p>本文。</p>
<table border="1">
  <tr><th>項目</th><th>値</th></tr>
  <tr><td>売上</td><td>100</td></tr>
</table>
</body></html>
```

**Why the meta tag matters:** without it, `textutil` reads the file as Latin-1. Japanese text silently becomes mojibake **that still looks plausible at the byte level** — the UTF-8 bytes get re-encoded faithfully, so a naive byte check passes while Word renders garbage. Verified 2026-07-25: same input with and without the tag produces clean vs. corrupted round-trips. If you cannot control the HTML head, pass `-inputencoding UTF-8` to textutil instead; either fix alone is sufficient.

### 2. Convert

```bash
textutil -convert rtf in.html -output out.rtf
# (or: textutil -inputencoding UTF-8 -convert rtf in.html -output out.rtf)
```

### 3. Verify BEFORE touching the clipboard — no Word needed

```bash
# Table structure: one \trowd per table row (header row included).
# 12-row table + header = 13. Count mismatch = table was flattened.
grep -c 'trowd' out.rtf

# Encoding: round-trip through Apple's own decoder. Output must be readable
# Japanese — mojibake here means Word will show mojibake too.
textutil -convert txt out.rtf -stdout
```

Both checks are cheap and deterministic. Do not skip the round-trip: the mojibake failure mode passes every byte-level inspection.

### 4. Place on clipboard as RTF class

Two equivalent commands — both empirically place the same `«class RTF »` flavor (verified 2026-07-25, macOS 26.5.2, byte-identical clipboard info):

```bash
# simpler:
pbcopy -Prefer rtf < out.rtf

# alternative (AppleScript route, also production-verified 2026-07-24):
osascript -e 'set the clipboard to (read (POSIX file "'"$PWD"'/out.rtf") as «class RTF »)'
```

The trap is **plain `pbcopy < out.rtf` without `-Prefer rtf`** — that puts the RTF *source code* on the clipboard as plain text, and Word pastes the markup literally. In the osascript form, note the trailing space inside `«class RTF »`: the class code is the 4 characters `RTF␣`.

Confirm what actually landed:

```bash
osascript -e 'clipboard info' | grep -o '«class RTF », [0-9]*'
# → «class RTF », 27591   (class present + plausible byte size)
```

Then tell the user to ⌘V in Word. If Word's paste looks wrong despite passing checks, use paste-special (形式を選択して貼り付け → リッチテキスト).

The clipboard is shared machine state — do the placement (step 4) **last**, immediately before telling the user to paste, so nothing you or they do in between overwrites it.

### Scale reference

Production run: full chapter (heading + intro + 13-row × 5-col table + notes) → 27,591 bytes of RTF, table intact.

## Route B: patch the .docx directly

Use `python-docx` (`pip install python-docx`; import name is `docx`). Approach verified 2026-07-23 (5-row table → 12-row replacement + cross-reference renumbering in a Japanese manual):

0. **Check what kind of document you're editing first.** python-docx text replacement is safe only for plain-prose docs. Scan for structures it will silently damage: tracked changes (`w:ins`/`w:del`), real Word cross-reference fields (`w:fldSimple`, `w:instrText` — REF/SEQ fields won't follow a text rename), hyperlinks and bookmarks in the paragraphs you touch. If present, stop and tell the user those parts need Word itself (or accept-changes first); don't text-patch over them.
1. **Locate anchors by content, not index** — find the target table by its header-cell text, paragraphs by leading text. Index positions shift between document versions.
2. **Replace surgically, at run level** — never assign `paragraph.text` (it collapses all runs into one, destroying bold/color/links in that paragraph). Edit `run.text` for the run(s) containing the target string; when a match spans runs, rebuild only that paragraph and copy each run's formatting. For tables you own outright, rebuilding the whole table is fine — copy border/bold settings from the old one.
3. **Renumber cross-references with exact-token boundaries, high→low** — two separate hazards: (a) low→high order cascades (10→11, then 11→12 turns the original 10 into 12) — go highest first; (b) substring hits — a plain replace of `点1` also matches inside `点10`/`点11` *even after* high→low reordering. Match the full token with its delimiters (e.g. regex `点1(?=[）。、\s]|$)`), never a bare substring.
4. **Save to a new filename** (`_new.docx`), never overwrite the user's file — they diff and swap themselves.
5. Verify by reading the saved file back with python-docx: row counts, the replaced text present, the old text absent — and re-scan for the step-0 structures to confirm none were touched.

## Route C: edit in Word Online yourself

Word for the web accepts synthetic clicks, typing and ⌘V, so you can do most editing without involving the user. (Excel Online does not — its grid ignores both CDP events and real OS-level events from `cliclick`. Verified 2026-08-04.) The clipboard payload here is **HTML placed as `«data HTML»`**, not RTF:

```bash
HEX=$(xxd -p page.html | tr -d '\n')
osascript -e "set the clipboard to «data HTML${HEX}»"
```

### Match the destination's formatting explicitly

Word for the web does **not** inherit the surrounding document's look when it pastes HTML — it applies its own paste defaults. Leaving font and spacing unspecified produced three separate rounds of "wrong size" / "wrong line spacing" feedback. Measure the target document and write the values into the HTML.

```bash
# run/paragraph properties actually in use, straight from the docx
python3 -c "
import zipfile,re
x=zipfile.ZipFile('doc.docx').read('word/document.xml').decode()
print(re.findall(r'<w:sz w:val=\"(\d+)\"',x)[:5])          # half-points: 21 = 10.5pt
print(re.findall(r'<w:spacing[^>]*/>',x)[:5])              # before/after in twips (240 = 12pt)
"
```

Typical result for a doc assembled this way: body 10.5pt with before/after 240, H1 16pt (style default 280/80), H2 14pt 299/299, H3 12pt 281/281, list items and table cells 0/0. Write those as inline `font-family`/`font-size`/`margin-top`/`margin-bottom`.

**Measure the range you are replacing, not the whole file.** Aggregating `w:spacing` across a 46-page manual reported body paragraphs as 0/0, because other parts of the document carry hundreds of genuinely 0/0 paragraphs. The section actually being replaced used 240/240, so the paste came out visibly tighter than its neighbours. Walk `body` and print style + spacing + text for the element range you are about to overwrite, then read the values off *those* lines.

Also decide spacing per *kind* of paragraph rather than applying one value to everything. A run of `**label** value` lines is a definition block and reads as one unit at 0/0, while the prose paragraphs around it need the document's 240/240 — the gap above and below each block then comes from the neighbouring heading's own margin.

Do **not** add `line-height` when the document has no `w:line` setting — specifying it introduces a line-spacing override the surrounding text doesn't have.

### Things that break, and what fixes them

- **A heading pasted at the start of a range loses its outline level and vanishes from the TOC**, even though the styles gallery still says "Heading 1". Re-applying the style does nothing. Fix: select the heading → styles dropdown → **Clear Formatting of Selection** → apply the heading style again → update the TOC.
- **Pasting at the start of a heading merges the first block into the preceding paragraph** and drops its heading style. Fix: put the cursor at the join → Return → re-apply the heading level (⌘⌥1/2/3). The split often lands one character off, leaving a stray character at the end of the previous paragraph. Repair that with shift+Left → Delete and retype the character at the heading's start; ⌘X → click → ⌘V mis-lands because the click coordinate shifts.
- **The TOC field's structure cannot be saved.** Changing "Show headings up to", or deleting the TOC, produces "Couldn't save automatically" and drops the session to Viewing every time (4/4 attempts, 2026-08-06, with no other session open). Updating the TOC saves fine. So depth changes need desktop Word or a docx patch of the field switch — `TOC \o "1-3"` → `\o "1-2"` in `word/document.xml`, exactly one occurrence; the many `TOC1`/`TOC2`/`TOC3` hits are paragraph-style references and must not be touched.
- **Updating the TOC while the document is still paginating writes `2` as every page number.** Confirmed 2026-08-07: the entry text updates correctly, but every number collapses to 2 and reloading does not repair it — the wrong numbers are now stored in the field. The page counter in the status bar is the tell; it drifts (26 → 46 → 26) while Word lays the document out. Reload, watch the counter until it stops moving, *then* update — the second update wrote 1/2/3/4/5/5/7/8… correctly. So: never update the TOC as the last action after a large paste; give the layout time first.
- **Moving a chapter between parts is best done inside Word** (select → ⌘X → navigate → ⌘V). It carries the document's own formatting, so none of the HTML-paste formatting problems apply.

### Replacing a whole section without disturbing its heading

Leave the section's own heading out of both the selection and the payload — start the range at the first *body* paragraph and let the existing heading stand. Click at its start, `Home`, scroll, then shift+click at the end of the last cell of the closing table; the status bar's "N of M words" confirms a range was taken, and scrolling back to zoom on the heading confirms it stayed unselected (white, not grey). Scroll in a call *after* the one that set the caret — Word scrolls back to the caret at the end of a batch and silently undoes a scroll issued in the same one.

Even so, the first pasted block merges into that preceding heading (the failure above). The repair that worked: click just left of the merged text, `shift+Right` and zoom to see which character got selected, walk over with `Right`/`shift+Right` until the selection is the single character before the join — a **space Word inserts at the seam** — `Delete` it, press `Return`, then set the new second paragraph back to Normal from the styles dropdown, since splitting a Heading 1 leaves both halves Heading 1. Once the body paragraph exists as its own paragraph, re-pasting over the same range does *not* merge again, so an iteration on formatting costs nothing extra.

### Getting bytes in and out of the page

When you need the live file locally (or a patched file back into the page) and Graph/download paths are unavailable, the clipboard bridges both directions. The browser window must be frontmost or `navigator.clipboard.readText()` throws `NotAllowedError: Document is not focused`.

```js
// page → local: fetch the file and park it on the clipboard as base64
const r = await fetch(downloadUrl, {credentials:'include'});
const b = new Uint8Array(await r.arrayBuffer());
let s=''; for (let i=0;i<b.length;i+=0x8000) s+=String.fromCharCode.apply(null,b.subarray(i,i+0x8000));
await navigator.clipboard.writeText(btoa(s));
```

`http://localhost` receivers do not work — an HTTPS page is blocked from reaching them by mixed-content rules.

The SharePoint REST API is reachable with the shared session (`/_api/contextinfo` returns a form digest; `GetFileById('<guid>')` returns 200), so a `PUT` to `GetFileById(...)/$value` is the theoretical overwrite path — but expect the harness to refuse to issue it. Treat file replacement as the user's action, and prefer editing in place.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| HTML without `<meta charset="utf-8">` | Silent mojibake that byte-level checks miss | meta tag or `-inputencoding UTF-8` (step 1) |
| Plain `pbcopy < out.rtf` (no `-Prefer rtf`) | Word pastes RTF source as plain text | `pbcopy -Prefer rtf` or osascript `«class RTF »` (step 4) |
| Converting to .docx with `textutil` as the paste payload | `textutil -convert docx` **silently flattens every table** to paragraphs (zero `w:tbl` — confirmed by two independent runs inspecting `word/document.xml`) | the payload is RTF, always; .docx output needs Route B |
| Verifying with "bytes look like valid UTF-8" | Passes on corrupted output | round-trip via `textutil -convert txt` (step 3) |
| Skipping `trowd` count | Flattened table discovered only after paste | count = rows + header (step 3) |
| docx: locating table by index | Patch lands on the wrong table next revision | anchor by header text (Route B-1) |
| docx: renumbering low→high | Cascading replacements corrupt every number | high→low (Route B-3) |
| Rerouting the whole job because one item is blocked | Days of detour for work that was already possible | re-list the remaining items per route ("Pick the route per item") |
| Building a file swap before checking who owns the file | Finished work that cannot be delivered | confirm owner + write permission first |
| Word Online: pasting HTML with no font/spacing declared | Pasted block visibly differs from surrounding text | measure the docx and inline the values (Route C) |
| Word Online: reporting a paste as done without looking | The heading-merge and outline-level failures are invisible from the tool result | screenshot after every paste; check the TOC picks the heading up |
