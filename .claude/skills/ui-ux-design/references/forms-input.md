# Forms, Input & Touch

Load when: deciding form length/structure, which field or control to use, how to label/hint/validate a field, how forgiving input parsing should be, what to default, or how to size and place touch targets and mobile input.

Contents: Form Scope & Structure · Field & Control Selection · Labels, Hints & Forgiving Input · Validation, Errors & Data Integrity · Specialized Forms: Passwords, Sign-in & Payment · Touch Targets & Interaction Reliability · Mobile Constraints & Accessibility

## Form Scope & Structure

### Minimize what you ask: omit, prefill, default, or justify every field
Before adding any field, try to omit, prefill, or default it; keep only fields the product truly needs, mark true optionality, and explain why any required field is needed.
- When: sign-up/registration and other data-collection forms; a confident default can be inferred from context, prior input, or majority behavior.
- Do: prefill known/inferable info; default so most users needn't touch the field; limit required sign-up fields to the true minimum (e.g. identifier + password); mark optional fields optional; explain why any required field is needed and how it's used.
- Avoid: fields kept only for database/marketing convenience; defaulting "because blank looks bad" without evidence; silently prefilling security-sensitive fields (passwords, card challenge/response); defaulting sensitive/personal/politically loaded fields or pre-checking a costly opt-in (e.g. marketing email).
- Exception: security-sensitive fields must never be silently prefilled; sensitive/personal/politically loaded fields should not be pre-selected.
- Trade-off: data collected vs conversion; an easily-skipped default may never "register," so a question meant to be consciously processed goes unnoticed.
- Ask: "Can this field be omitted, prefilled, or defaulted instead of asked?"
⟨di4-002, di4-021, uxp1-037⟩

### Match form language to the user's expertise, and explain the ask
Make sure users understand what's being asked and why, in vocabulary matched to their expertise, and verify with real usability testing even when the design feels confident.
- Do: plain language for novice/infrequent users; precise domain terms for experts; for long/effortful forms, explain why the info is needed and split into clearly titled sections; add tooltips for icon-only toolbar buttons; usability-test before shipping, regardless of designer confidence.
- Ask: "Would a first-time user understand why we're asking this, in their own vocabulary? Has this actually been tested with real users?"
⚖ Tension: simple vs precise vocabulary → tradeoffs-decision-points.md (label-d02)
⟨di4-001, di4-007⟩

### Don't let the underlying data model dictate form structure
Don't translate a database schema/object model directly into a form (one label + one control per field, top to bottom); use domain knowledge, visual conventions, implicit context, and direct manipulation to keep it economical and user-centered.
- Avoid: a form that's a 1:1 mirror of an internal object model, ballooning to dozens of raw fields.
- Exception: a property-sheet, one-row-per-attribute layout is fine when the user genuinely needs to inspect/set every raw property (e.g. a developer tool).
- Ask: "Does this form's structure come from what the user thinks they're doing, or from our internal data model?"
⟨di4-006⟩

### Form layout: label placement, gatekeeper forms, splitting long forms, and action prominence
Place labels above each control (more vertical space, accommodates long labels) or left-aligned at the form edge (more compact) — choose deliberately, since it measurably affects completion speed.
- Do: for "gatekeeper" forms standing between the user and a goal they already want (registration, checkout), put the form center stage, strip distractions, or present as a focused modal overlay; split long/multi-topic forms into titled sections or a wizard with a progress indicator (tabs are usually a poor grouping mechanism); give the completing action one prominent button and keep secondary actions (reset, help links) visually subdued; size each textarea to roughly match a typical answer's length, decided per field rather than one uniform size.
- Avoid: tabs as the default way to group a long form; a textarea sized the same regardless of expected content length.
- Ask: "Does this textarea's size match how much text a typical answer will contain?"
⚖ Tension: reveal steps vs disable steps → tradeoffs-decision-points.md (vh-d01)
⟨di4-023, uxp1-036⟩

### Quick reference
- Fill-in-the-Blanks: compose controls into a natural sentence/phrase (each control a fillable "blank," useful for search/filter conditions), sized and baseline-aligned to the surrounding text so the completed sentence itself describes the action. ⟨di4-014⟩

## Field & Control Selection

### Control choice signals what input is expected; weigh five contextual factors
A control's visible type/size tells the user what answer is expected — a control that looks unconstrained but isn't misleads users into out-of-range input that then gets rejected as a surprise. Choose deliberately among otherwise-equivalent controls.
- Do: use a slider/spin box instead of free text when the range is genuinely constrained; favor compact controls (radio-in-place, spinner) in tight spaces (toolbars, table cells); favor familiar low-skill controls (text fields, simple dropdowns) for general/novice audiences; allow denser controls (bare text fields for numeric ranges) for known-expert audiences; match what established apps already use for the same concept.
- Avoid: a plain text field that silently enforces a constrained range.
- Ask: "Does this control's visible shape honestly represent what input will be accepted, given space, audience, convention, and toolkit?"
⟨di4-008, di4-009⟩

### Choose choice-controls by cardinality and set size
Match control to option count and pick-count. Binary: checkbox (compact, unchecked meaning implicit) vs two radios (both visible, more space) vs a two-item dropdown (compact, one option visible at a time). Small one-of-N (2-3): show options directly, don't hide behind a dropdown. Large one-of-N: scrollable list, a tree/cascading list only if it genuinely aids findability, or a specialized picker; if a long dropdown is unavoidable, add type-ahead and order meaningfully. Many-of-N: explicit checkbox-list, not an unmarked multi-select box.
- Do: for a rich visual picker that shouldn't consume permanent space, use a Dropdown Chooser (button + trailing arrow opening a popup); to build a subset from a source list too long for checkboxes, use a List Builder (source/destination lists, add/remove/reorder, multi-select each side).
- Avoid: a dropdown for only 2-3 options; unmarked multi-select list boxes; random dropdown ordering; precise scrolling inside a small Chooser popup.
- Trade-off: checkbox saves space but hides the unselected meaning; tree/cascading list aids findability but costs space and is less familiar to novices; List Builder needs far more space but scales and keeps the full selection visible.
- Ask: "Would a directly-visible control serve better than a dropdown here? Would a user notice this list supports multi-select?"
⚖ Tension: show options vs hide behind menu → tradeoffs-decision-points.md (forms-d01)
⟨di4-010, di4-011, di4-019, di4-020, uxp1-024, uxp1-031⟩

### Prefer native/standard controls matched to the data type; never invent bespoke widgets
Never build a bespoke control when a standard one exists. Trigger device-native input UI matched to the data type (numeric keypad, native date/color picker) on desktop as well as mobile.
- Do: numeric field for year (never a decade-spanning dropdown; dropdowns OK for month/day; best is a native date input); use the same date-picker everywhere in a product; numeric input (not free text) when only integers are wanted; sliders only for qualitative/approximate settings, never for exact values.
- Avoid: inventing a bespoke control (custom color wheel, drag-and-drop volume knob) when a standard one exists; a scrolling-dropdown year field; a different/more complex date picker appearing deeper in a flow; free text accepting non-numeric input where only integers are wanted; a slider where an exact value is needed.
- Exception: a truly novel interaction that's genuine UX progress (e.g. pull-to-refresh when first invented) is a rare, deliberate exception.
- Ask: "Does a standard control already do what this custom widget is trying to do? Does every date-picker instance look and behave the same?"
⚖ Tension: convention vs departure → tradeoffs-decision-points.md (learn-d01)
⟨uxp1-024, uxp1-025, uxp1-026, uxp1-027, uxp1-028, uxp1-029, uxp1-030⟩

### Quick reference
- Structured Format: for truly fixed, universal formats (card numbers, phone within one system, license keys) use short segmented fields sized to hint at length, with auto-advancing focus and an input prompt (e.g. "dd/mm/yyyy") — never for formats varying by user/locale (names, addresses, international phone); inconsistent auto-advance can feel like unwanted system takeover for keyboard-only power users. ⟨di4-013⟩
- Autocompletion: predict likely completions from past entries, other users' values, or indexed/contextual data as a selectable list with optional auto-complete; default to not auto-applying without confirmation, never interfere with normal typing (typing through a wrong suggestion must produce exactly what was typed), and stop re-offering a repeatedly-rejected candidate. ⟨di4-018⟩
- Image/file upload: hand selection off to the device's native picker rather than a custom one, support batch upload when needed, offer inline crop/rotate so users don't need a separate tool, support standard formats (at least JPEG/PNG/GIF), always show upload progress, and consider an external avatar service or not requiring an image at all. ⟨uxp1-047⟩

## Labels, Hints & Forgiving Input

### Field labeling: a persistent real label, plus separate hint/prompt text — never placeholder-as-label
Give every field a real, persistent label above/beside it — screen readers announce labels, not placeholder text, so placeholder-only fields are effectively unlabeled, and sighted users forget a field's purpose once placeholder text vanishes on focus/fill.
- Do: for skimmable guidance when no default is needed, use an Input Hint (short phrase, visually subordinate to the label, ~2pt smaller — 1pt reads as a sizing mistake); for guidance needing active engagement where no good default exists, use an Input Prompt (text prefilled in the value position, e.g. "Choose a state") — start dropdown prompts with Select/Choose/Pick and text prompts with Type/Enter, ending in a noun; disable the forward action until a prompted field is filled, so it never needs an error message; re-show the prompt if cleared; keep the real label present even with a prompt.
- Avoid: placeholder text as the only label; load-bearing info (why needed, privacy) hidden only behind a rarely-clicked link; making prompt text itself a selectable dropdown value.
- Trade-off: always-visible hints add clutter on long forms; focus-triggered hints stay clean but need reserved layout space and go unseen until interaction; a hint can be skimmed past, a prompt cannot.
- Ask: "Does this field have a persistent label, or only placeholder text? If a hint/prompt is used, is the real label still present?"
⚖ Tension: progressive disclosure vs recognition → tradeoffs-decision-points.md (cog-d02)
⟨di4-015, di4-016, uxp1-089⟩

### Forgiving Format: accept real-world input variation, validate leniently, and be specific and humane about unavoidable errors
Accept text in whatever natural notation the user types (dates, names, addresses, phone, postal codes, card numbers) and interpret it programmatically instead of one rigid format or cultural convention. Don't over-engineer client-side validation where legitimate variety is too broad to enumerate (email TLDs, international phone) — use native input types plus autocomplete and confirm via a lightweight mechanism instead.
- Do: accept several common notations; echo the parsed/normalized value back for confirmation; accept accented characters, apostrophes, hyphens, multiple given names, non-default name order; free-text postal code validated server-side with autocomplete/auto-suggestion; `type="tel"`/`type="email"` with autocomplete, confirmed via a one-click emailed link rather than strict regex; when an error is truly unavoidable, flag it the instant it's recognized, naming the exact field, why, and how to fix it — never as though the user's identity is "wrong"; test extensively since apps interpret ambiguous input differently.
- Avoid: rejecting valid input over incidental formatting (spaces in a card number); enforcing one national postal-code format or fixed-length phone field; strict client regex beyond user@domain.tld; a country selector that wipes already-entered fields on change.
- Exception: when the format must be fully predictable for downstream processing, use Structured Format (short segmented fields) instead.
- Ask: "Would this field reject a legitimate real-world value just because it doesn't fit an assumed format?"
⟨di4-004, di4-005, di4-012, laws1-031, laws1-032, uxp1-040, uxp1-041, uxp1-042, uxp1-043⟩

## Validation, Errors & Data Integrity

### Validate inline, and explain errors in place, specifically, and without erasing data
Prevent errors before they happen where possible (dropdowns over free text for limited sets; hints/prompts/forgiving-format/autocomplete/defaults for free text; business-logic constraints built into controls so invalid combinations can't be selected). Validate each field as soon as it's completed, not only at submission.
- Do: prefer client-side validation, updating the loaded page rather than reloading; when only server-side validation is possible, name exactly which field(s) failed and suggest the likely fix instead of a vague "there was an input error"; show messages on the same page (a top summary plus, where space allows, a message beside the field), never a modal or separate results page; mark required fields with the word "required," not only a symbol; pair color with a non-color cue (general rule: typography-color-depth.md → Never convey meaning through color/motion alone); write plain, specific, polite error text.
- Avoid: waiting for full-form submission to reveal errors; modal/separate-page error display; vague generic errors with no field indication; symbol-only required markers; color-only error indication.
- Ask: "Is this error caught as the user finishes the field, or only after submitting the whole form? Does the error name the specific field and why?"
⟨di4-022, uxp1-038, uxp1-039⟩

### Never discard user-entered data
Never clear form data a user has already entered unless they explicitly signal abandonment (e.g. Cancel). Guard against any technical path that could redisplay the form — refresh, re-render, validation return — silently losing it; persist defensively so it survives redisplay.
- Ask: "If this page reloads or re-renders, does the user's entered data survive?"
⟨uxp1-048⟩

## Specialized Forms: Passwords, Sign-in & Payment

### Quick reference
- Password field UX: give live strength/validity feedback while typing (or on blur) with concrete advice, state requirements up front via a hint, mask by default but always offer a show-password toggle, never disable paste (password-manager users need it), and never require a "confirm password" field or display the password in plaintext or suggest alternates. ⟨di4-017, uxp1-050, uxp1-051⟩
- Checkout/payment forms: apply extra UX rigor since this is often the single most business-critical flow — concise feature lists, a clear purchase-button signifier, familiar pricing structures, a minimal order form with control over details, regular testing, only essential card fields (number/expiry/security code) with the number auto-grouped into 4s and stripped of manual spaces, explanatory text for the security code, and HTTPS throughout. ⟨uxp1-044, uxp1-045⟩
- Never live-reformat money mid-typing: don't auto-insert decimal digits into an amount while the user is still typing (a documented source of real financial errors, e.g. accidental over-bids) — let users type the decimal themselves, interpret a blank decimal as ".00" only once input is complete, and echo the final amount back for confirmation. ⟨uxp1-046⟩
- Forgot-password flow: label the entry point plainly "forgot password," not jargon like "reset password"; pre-fill the username/email from the failed attempt; send a one-click reset link tolerant of repeated clicks that expires on success or after a reasonable time; auto-sign-in after a successful reset; favor longer session lifetimes, since short auto-logout windows push users toward weaker, memorable passwords. ⟨uxp1-052, uxp1-053⟩
- Case-insensitive identifier matching: default usernames/emails/URLs to case-insensitive (only passwords stay case-sensitive), since users expect case not to matter the way email/DNS already don't — warn explicitly wherever case-sensitivity is unavoidable elsewhere. ⟨uxp1-006⟩

## Touch Targets & Interaction Reliability

### Never let UI elements shift right as the user is about to interact with them
Never let a control move, resize, or get covered right as the user is about to tap/click it — e.g. a slow ad pushing content down mid-tap, a notification popping over a button. This became common once Flash-era animation habits spread, applied because the capability existed rather than because it served the user.
- Do: test load behavior across devices/connection speeds; reserve placeholder space in advance for slow-loading elements; keep micro-animations (fade, expand/collapse) unobtrusive and brief.
- Exception: brief, unobtrusive micro-animations that don't interfere with the task are fine.
- Ask: "Could a slow-loading element shift layout right as the user is about to tap something?"
⟨uxp1-049⟩

### Interactive elements need persistent, hover-independent visual signifiers
Give buttons real-world cues (shadow, depth, texture) rather than stripping all signifiers for flat/minimalist design; give links a persistent signifier (underline) rather than relying on hover-only highlighting, which doesn't exist on touch at all. Never style a non-interactive element to look like a button or link.
- Avoid: stripping all depth/signifier cues from real buttons for flat design; styling non-interactive elements as buttons/links; relying solely on hover-highlight for link discoverability.
- Trade-off: visual minimalism vs discoverability of interactive elements.
- Ask: "Can a first-time user tell this is clickable or a link without hovering or clicking it?"
⟨uxp1-021, uxp1-033⟩

### Size touch/click targets to the finger, exceed the documented minimum, and be generous with the hit area
Treat published minimums (~44x44pt / 48dp / 44px CSS, ~1cm square) as a floor, not a target — fingertips (~16-20mm) are far wider and less precise than a mouse cursor, and Fitts's Law means undersized targets feel harder to use even when a tap doesn't fail.
- Do: generous internal padding and external margin; consider a tappable hit zone larger than the visually-rendered control (an "iceberg tip"); bind a label to its input so tapping the label focuses it; make the full visible button surface clickable, not just its text; give real feedback (color change, slight depression, sound, pointer cursor on hover for desktop); on mobile budget ~5 finger-widths across/10 down per screen (avoid 6+ controls in one row), prefer built-in device controls, space adjacent targets ~2mm apart.
- Avoid: shipping a target at or below the bare minimum; restricting the clickable area to only the text inside a button; skipping hover/cursor feedback on desktop web.
- Ask: "Does every tappable target meet or exceed the platform minimum? Is the entire visible button surface clickable?"
⟨di4-037, laws1-008, laws1-011, uxp1-022, uxp1-023, uxp1-034⟩

### Space, group, and differentiate targets via Fitts's Law; place completion actions near their trigger
Movement time to a target shrinks as size grows and distance shrinks (Fitts's Law) — keep related/sequential targets close together, and don't place a small target far from a preceding click point and expect reliable accuracy.
- Do: adequate spacing between unrelated adjacent targets to avoid accidental taps; when adjacent controls have opposite/high-consequence outcomes (approve/reject, delete/cancel), give them distinct visual treatment in addition to spacing — never rely on spacing alone; position a task-completing action (e.g. submit) adjacent to the last input it acts on.
- Avoid: placing accept/reject or destructive/safe actions immediately adjacent with identical styling. (Consolidated destructive-action block: interaction-feedback.md.)
- Ask: "Is this target big enough and close enough to where the user's pointer already is?"
⟨laws1-009, laws1-012, psy1-039, uxp1-022⟩

### Quick reference
- One-handed thumb reach: position frequent touch targets by how users actually hold/reach the device (center tends to be the most accurate reachable zone on mobile, not a desktop scan pattern), and on large screens provide a way to bring hard-to-reach top-of-screen controls down into the lower half. ⟨laws1-010, laws1-014⟩
- Screen edges/corners as zero-effort Fitts's-Law targets: place very frequent global controls (app launchers, menu bars) at a screen edge/corner, where the boundary stops the pointer and makes the target effectively infinite in that direction. ⟨laws1-013⟩
- One-tap clear button on mobile text fields: give text fields a one-tap "x" clear control instead of forcing character-by-character deletion; use the platform's default clear-button affordance where one exists, and usability-test a custom beside-the-field clear button before shipping since users may mistake it for Go/Search. ⟨di4-038⟩

## Mobile Constraints & Accessibility

### Ensure full keyboard operability with a logical, tested tab order
Every function must be operable via keyboard alone, mouse as optional convenience, following the platform's standard shortcut/tab-order/default-button conventions. Tab order must follow a logical reading order matching how content should be understood.
- Do: define shortcuts/accelerators/mnemonics per platform style guide; arrow keys + modifiers for list selection incl. multi-select; Tab/Shift-Tab for focus traversal; standard controls operable via arrow keys, Enter, spacebar; a clear default button so Enter triggers the primary action; for high-speed data entry, consider auto-advancing focus without requiring Tab; set tabindex/DOM order for a logical sequence; test by actually tabbing through, and with real assistive technology.
- Avoid: any function reachable only by mouse; assuming visual layout automatically produces correct tab order.
- Exception: spatial/graphic editors are much harder, though not impossible, to make fully keyboard-operable.
- Ask: "Can every function be reached and completed using only the keyboard? Does tabbing follow a logical order?"
⟨di1-020, uxp1-088⟩

### Never disable pinch-zoom or text scaling
Never set a viewport meta tag or equivalent that disables user scaling (user-scalable=no, maximum-scale=1.0) — no layout renders pixel-perfect on every device, so locking display is self-defeating and removes a critical accessibility affordance for low-vision users.
- Do: always allow pinch-zoom and text scaling; support OS accessibility features for text size/contrast on mobile and desktop; test across device sizes with real assistive technologies.
- Avoid: disabling user-scalable/pinch-zoom via viewport meta or JS.
- Exception: games/interactive experiences where zoom would break gameplay are a narrow, deliberate exception, not a general license.
- Ask: "Is pinch-zoom or text scaling disabled anywhere in this build?"
⟨uxp1-087⟩

### Quick reference
- Six mobile constraints to design against: tiny screen space (trim ruthlessly); widely varying widths (design flexible, not one fixed target); touch accuracy (~1cm targets, spaced); hard text entry (minimize typing, favor numeric/autocomplete); harsh physical environments (strong contrast, larger text/targets); divided attention (tasks quick, interruptible, resumable, self-explanatory). ⟨di4-027⟩
- Strip mobile to the essential task: identify the few things a mobile user needs right now rather than assuming desktop parity, get core content within ~100px, link out to the full/desktop site, and minimize typing (toward zero/few characters), page loads, scrolling (prefer one long page over pagination unless pagination avoids extra loads), and taps — a full "parallel" mobile experience should still go narrower/deeper rather than flat. ⟨di4-028, di4-030⟩
- Substitute low-effort device input for manual entry: check whether location, camera, voice, gesture, haptic feedback, background execution, or biometric auth can replace or simplify a manual-entry/verification step. ⟨di4-029, laws1-033⟩
- Minimize input-mode switching: keep data-entry-heavy work on one input mode (keyboard-only or mouse-only) where possible — switching breaks flow and shifts visual attention, especially for touch typists. ⟨psy1-040⟩
- Screen-reader content patterns: write link text that stands alone out of context (screen readers list links by text alone — avoid "click here"/repeated "read more"), and add a visually-hidden "skip to content" link atop every page template so screen-reader users can bypass the nav menu. ⟨uxp1-084, uxp1-085⟩
- Mobile support is mandatory: treat mobile-friendliness as baseline, not optional ("doesn't work on mobile" is a critical bug and SEO liability) — use a responsive framework instead of a separate mobile version, evaluate web vs native case by case (native needed for hardware access/heavy computation), and consider starting mobile-first, which tends to simplify the design. ⟨uxp1-096⟩
- Search as a text field plus button: implement as a standard text field with a search/magnifying-glass button rather than an icon-only reveal that adds a tap, and auto-focus with the keyboard up on mobile search screens. ⟨uxp1-035⟩
