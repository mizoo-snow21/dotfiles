# Pattern Catalog — Forms & Controls

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

## Forms & Controls

### List Builder `PTN-087`
A source list and a target (chosen) list shown side by side or stacked, with Add/Remove
controls (or drag-and-drop) moving items between them; decide deliberately whether adding
removes from the source (depleting pool) or leaves it unchanged (mirrors something external).
When: beats a checkbox list when the source is too long to browse as checkboxes; avoid when
space is tight or the chosen set will be small. Trade-off: good visibility of both sets and
ordering support, at the cost of much more space than a single list. Ask: does adding an item
remove it from the source, and is that choice deliberate? (DI ch8)

### List-Building Control Variants `PTN-088`
For adding to a free-form list: an explicit Add/New button plus field (visible, busier), an
inline new-item row (compact, less discoverable), or drag-and-drop (space-efficient, needs real
skill to discover). For reordering: up/down buttons (visible, costs space) or drag-and-drop
reordering (compact, invisible unless discovered). Trade-off: each variant trades visibility of
the action against the space/clutter it costs. (DI ch8)

### Prefer Externally-Visible Knowledge Over Forced Recall `PTN-089`
When a user can't be expected to enumerate all valid options from memory, show the full set via
a chooser (dropdown, radio, list) rather than an open text field; conversely, for information
the user reliably knows and types quickly (own name, birthdate), a plain text field is fine and
a forced-choice control is unnecessary overhead. (DI ch8)

### Prefer Not Asking at All `PTN-090`
Wherever possible, avoid presenting a question at all — prefill known/inferable information,
supply good defaults, use autocompletion — rather than always adding a control and asking.
Exception: security-sensitive fields (passwords, credit-card numbers) must have
prefilling/autocomplete deliberately suppressed even at the cost of convenience. (DI ch8)

### Forgiving Format vs. Structured Format `PTN-091`
Forgiving Format is one free-text field accepting many formats/word orders, delegating
interpretation to the app; Structured Format is small, purpose-shaped sub-fields whose layout
mirrors the expected data structure. Favor Forgiving when input format/locale varies; favor
Structured only for a well-known, standardized, locale-independent format — verify it isn't
itself country-specific before hard-coding. If sub-fields auto-advance focus, that behavior
must be applied consistently across the whole application. Trade-off: Structured Format signals
shape clearly but costs more space and can reject legitimate values that don't fit; Forgiving
Format stays simple but depends on the app actually parsing well. (DI ch8; MI ch3)

### Fill-in-the-Blanks `PTN-092`
Embed controls inline within a sentence so each is a "blank" the user fills, and the completed
sentence itself expresses the action that will be performed. When: fits a small number of
inputs reducible to one natural sentence; avoid for products localized into languages with
substantially different word order/grammar. (DI ch8)

### Input Hints `PTN-093`
A short, visually de-emphasized example or explanation beside/below a field, distinct from its
label, clarifying expected content without a long label; keep brief (more than 1-2 sentences
gets skipped) and understated but not so faint it reads as accidental. Exception: a hint may
link to more detail, but don't rely on the linked page for critical information — most users
never follow it. (DI ch8)

### Input Prompt `PTN-094`
Pre-fill a field/dropdown with a short instructional phrase standing in for the value,
disappearing on entry and reappearing if cleared; because it's only present in the empty state,
it is not a substitute for a real, persistent label — removing the label strands a user who
later revisits the field to review or correct a value. When: applies when no good default
exists to prefill instead; avoid when a real default could be prefilled, or requiredness must
be communicated. Ask: if a user revisits this field later, is there still a persistent label
identifying what it is? (DI ch8)

### Password Strength Meter `PTN-095`
Give live feedback while typing a new password on how valid/strong it currently is, via a
discrete indicator, rather than only a pass/fail check on submit; never display the actual
password text in the meter's feedback, and never suggest concrete alternative passwords — only
generic strength guidance. (DI ch8)

### Autocompletion `PTN-096`
Predict likely input and offer it as a selectable, updating list, sourced from
history/dictionary/indexed content; explicit acceptance (a picked list) suits when the user may
not know what's needed, automatic inline-fill suits when a confident single guess can be
cheaply offered — the two can combine. Do: let users always disable suggestions, defaulting to
non-intrusive; never interrupt normal typing/backspacing; stop offering a repeatedly-rejected
suggestion; predict accurately or not at all. (DI ch8)

### Dropdown Chooser `PTN-097`
Generalize the dropdown concept: the opened panel isn't restricted to a flat text list — it can
host any rich sub-UI (grid, tree, calendar, color picker) while the closed control stays as
small as a field-plus-arrow; design the opened panel using already-familiar layouts, and
surface popular/recently-used items prominently. When: avoid when the value set is large enough
that even scrolling the popup becomes unwieldy. (DI ch8)

### Good Defaults `PTN-098`
Prefill every reasonable field with the value most likely to match what the user wants, cutting
total completion time even when some defaults are wrong. Exception: never default a security-,
privacy-, or consequence-sensitive field (password, gender, nationality, marketing opt-in, paid
upsell) — leave it blank/unchecked rather than presume; defaulting a paid upsell on is a
business-ethics problem, not just a UI one. Do: set defaults primarily when the page first
shows; don't silently override a value the user already typed. (DI ch8)

### Same-Page Error Messages `PTN-099`
Place validation feedback on the same page as the form — a summary near the top and a specific
message beside the offending control — instead of a modal dialog or separate error page; first
prevent whole classes of error via choosers/hints/defaults, then validate as early as possible
without a full reload. Do: mark required fields clearly and don't over-require; emphasize an
erroring field with color plus a non-color cue, since a meaningful fraction of users are
colorblind; show positive inline confirmation too, not only failures. (DI ch8)

### Checkbox for Selection / Mark-as-Done `PTN-110`
A native checkbox with a proper label is the correct, fully accessible control for a binary
selection state — including "mark as done" in a list — because checking really is designating
an item as selected/done, unlike a generic on/off setting. Ask: does this on/off interaction
mean "select/designate this item," or "switch a setting" (favor a true Toggle Button instead)?
(IC ch2; IC ch3)

### True Toggle Button `PTN-111`
For a generic two-state switch not tied to form submission or selection semantics, use
`<button type="button">` (never `type="submit"`) carrying an explicit
`aria-pressed="true"`/`"false"`, never omitted. (IC ch2)

### Don't Start From Zero `PTN-121`
Use whatever is already known about the user/context (platform, time of day, location, and
especially past behavior — the most valuable signal) to proactively adjust a component's
initial state, defaults, or copy, rather than always starting blank. Weigh against privacy:
skip a signal whose use could embarrass, endanger, or expose the user, preferring a plain
unpersonalized experience over a privacy-risking personalized one. Trade-off: personalization
improves relevance but increases privacy risk and data-collection burden. Ask: what do I
already know that could make the default more useful right now? Could this signal embarrass,
endanger, or expose the user if surfaced? (MI ch3; DI ch8)

### Predict the Next Step to Remove a Choice `PTN-123`
When a user's next likely action can be predicted from context, perform it automatically or
pre-fill it rather than presenting it as an explicit choice, chaining multiple
microinteractions into one smooth sequence. Ask: can I predict the user's next step confidently
enough to perform or pre-fill it rather than asking? (MI ch3)

### Sequence a Multi-Step Decision Coarse to Fine `PTN-124`
When a user must make several related decisions in sequence, order them from simple/broad
choices toward progressively more detailed ones — users decide quickly and confidently when
they can easily understand and compare what's in front of them. Ask: am I asking for the most
detailed distinction first, or building up to it from coarser choices? (MI ch3; DI ch4)
