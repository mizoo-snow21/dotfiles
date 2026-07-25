---
name: word-clipboard
description: Use when content needs to land in a Microsoft Word document with formatting intact — pasting tables, headings, or Japanese text into an open Word doc via the macOS clipboard, or patching an existing .docx directly. Trigger on Wordに貼り付け, Word文書に反映・更新, クリップボード経由でWordへ, RTF, docx patching, or any deliverable whose final destination is a Word document, even if the user only says "Wordに入れて".
---

# Word Clipboard / Docx Delivery

Two verified routes for getting generated content into Microsoft Word on macOS. Both were proven in production (2026-07-23/24, D365 manual work); the pitfalls below were hit for real.

## Choose the route

| Situation | Route |
|---|---|
| User has the Word doc open / manages it themselves; you hand over a fragment (a chapter, a table) for them to ⌘V | **Route A: clipboard as RTF** |
| You must update a `.docx` file programmatically (replace a table, renumber cross-references) without the user pasting anything | **Route B: patch the docx** |

Rule of thumb: interactive handoff → A. File-in, file-out → B.

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
