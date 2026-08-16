# Accessibility Contracts I — Semantics, Labeling & State Communication

This file covers the accessibility contracts a component must uphold once its markup, labels, and state signals are being decided: what semantic structure it exposes, how it names itself (including under machine translation), how it communicates state changes, and how it delivers live and transient feedback. Route here when choosing HTML/ARIA structure, writing or associating a label, exposing toggle/disabled/sort state, wiring a live region, or designing a notification or data table. The strongest agreement across every source book, given prominence throughout: state, category, and type must never be communicated through a single perceptual channel alone — color, a bare icon, or text with no fallback each fail some user population.

## Contents
1. Semantic Structure
2. Labeling (incl. Translation-Safety)
3. State Communication
4. Live Regions
5. Notifications
6. Tables & Structure-Heavy Components

## 1. Semantic Structure

### Custom containers need a role and a name to matter `AXS-008`
Any generic or custom wrapper acting as a section, panel, focusable scroll region, or tabpanel carries no accessible semantics by default. It needs both an explicit role (e.g. `region`, or the matching compound-widget role) and an accessible name via `aria-labelledby` pointing at real text, because `aria-label`/`aria-labelledby` is only reliably exposed on elements whose role supports naming. When: a component wraps heading-introduced or otherwise substantive content in a non-sectioning element, or makes a custom element keyboard-focusable via `tabindex="0"`.
Do: apply `role="region"` (or the matching widget role) to semantics-free wrappers; label a custom focusable region via `aria-labelledby` at a caption/heading; label a tabpanel via `aria-labelledby` referencing its own tab, since users can land inside it by paths other than activating the tab; for a table of contents, use `<nav><ul>` plus `aria-labelledby` naming the list. (IC ch1-3; DI ch2)

### List semantics as a free grouping/navigation mechanism `AXS-009`
Any set of comparable, repeated items or related sibling controls — whether or not a bulleted/numbered marker is visually wanted — should be wrapped in `<ul>`/`<ol>`, giving screen-reader users a grouping cue ("list of N items") and dedicated list-navigation shortcuts, independent of visual bullet styling. When: the items don't form a compound ARIA widget (menu, tablist), whose own grouping role should be used instead.
Do: use `<ul>`/`<ol>` even when list-style is visually suppressed; add a group `aria-label`/`aria-labelledby` on the list when individual item labels aren't self-descriptive as a set. (IC ch1,2)

### ARIA role assignment replaces, not adds to, native role `AXS-011`
Applying an ARIA role to an element fully overrides its native/implicit HTML role in the accessibility tree rather than supplementing it, so overriding a meaningful native role must only be done with a compelling, specific reason — doing so without one can silently strip information the user needs (e.g. that a link is a link).
Do: before overriding, check whether the override would hide information the user actually needs; don't add a role to an element with meaningful native semantics without a specific reason. (IC ch1,2; DS ch1)

### Heading level is structural, not importance-based `AXS-012`
A heading's level must reflect where its section sits in the document's actual nesting hierarchy, never a subjective sense of importance. Because nesting depth is only known at composition time, a reusable component containing its own heading cannot hard-code an absolute level — it must compute the level from ancestor context, and any component that relocates or reproduces an author-supplied heading must preserve that heading's original level. When: assigning a heading level to any section, especially inside a reusable or composed component, or relocating/cloning/wrapping an author-supplied heading.
Do: derive level purely from nesting depth, never perceived importance; derive a reusable component's internal heading level dynamically from context; when a relocated/reproduced heading can't literally stay an `h1`-`h6`, apply `aria-level` to preserve its original level — and never repurpose `aria-level` as a CSS styling hook. (IC ch1,2)

### Heading navigation follows source order, not visual grouping `AXS-014`
Content that precedes a heading in source order is structurally outside that heading's section for heading-based screen-reader navigation, even when visually grouped with the section and sharing the same DOM container — a user jumping between headings will skip it entirely. When: a component places meaningful (non-decorative) content before its own heading in source order for layout reasons; avoid/except: purely decorative images (`alt=""`) are unaffected, since they carry no content to miss.
Do: put the heading first in source order, then use CSS (e.g. flexbox `order`) to independently restore the desired visual position. (IC ch3)

### Visually-hidden technique, not display:none, for AT-only content `AXS-015`
Content that must stay available to screen readers while offscreen visually must use the visually-hidden CSS clip/position technique, not `display:none` or `visibility:hidden` — the latter two remove content from the accessibility tree as well as the visual layout.
Do: use the visually-hidden clip pattern for AT-only content; reserve `display:none` (e.g. driven by a DOM `:empty` selector) for content that should genuinely disappear for everyone, screen readers included. (IC ch1)

### `<form>` changes real browser and AT behavior, not just semantics `AXS-016`
Wrapping inputs in `<form>` is not cosmetic: Enter-to-submit inside a form field reliably fires only when that input lives inside a `<form>`, which matters even for single-field, XHR-only UIs. Separately, most screen readers auto-trigger "forms mode" on focusing most inputs regardless of a wrapping `<form>`, but some input types (e.g. `range`) have been observed non-functional in some browser/AT combinations without one. When: a component includes input types with known inconsistent forms-mode support, or any input+submit pairing where Enter-to-submit should work even though submission is handled entirely via JS.
Do: wrap such inputs in a `<form>` even when no real submission/navigation happens.
Ask: if the user presses Enter in this field, does it trigger the same action as clicking its associated button? (IC ch1)

### Persistent utility controls belong outside `<main>` `AXS-054`
Cross-page utility controls (e.g. a theme switcher) belong in a landmark other than `<main>` — such as `<header role="banner">` or `<footer role="contentinfo">` — because screen-reader users expect `<main>` to hold the content that changes between pages/views, and page-invariant chrome there misleads that expectation.
Do: place persistent, global utilities in header or footer landmarks. (IC ch2)

### True tabbed interface: the WAI-ARIA tabs contract `AXS-055`
A true tabbed interface's contract: the container carries `role="tablist"`; each tab carries `role="tab"` (with `role="presentation"` on any wrapping `<li>`); the active tab carries `aria-selected="true"`; each content region carries `role="tabpanel"`; non-active panels are hidden via the `hidden` attribute. `role="tablist"` does not delegate tab semantics to its children — each child still needs its own explicit `role="tab"`. When: implementing a genuine tabbed interface (not a table of contents, not an SPA view switcher) with only 1-3 sections, consider a lighter same-page-links pattern instead of full tab semantics.
Do: `role="tablist"` on the container, `role="tab"`+`role="presentation"` wrapper on each tab, `aria-selected="true"` on the active tab, `role="tabpanel"`+`aria-labelledby` on each panel, `hidden` on inactive panels. (IC ch2)

### Collapsible toggle: real button nested in heading `AXS-056`
A collapsible section's toggle must be a genuine `<button>` nested inside the section heading (e.g. `<h2><button>...</button></h2>`), not a click handler on the heading text nor `role="button"` on the heading itself — nesting preserves the heading's navigational role while giving the toggle real button semantics and free keyboard operability, whereas `role="button"` on the heading overrides its native semantics and forces hand-reimplementing focus/key bindings. Once the real button is in place, most further ARIA is unnecessary: `role="button"` is redundant, `aria-haspopup` doesn't apply, and `aria-controls` is both unneeded when content immediately follows in source order and a weak choice regardless (poor cross-AT support). This button is not obligated to look like a default button — it can be restyled as an enhanced version of its heading as long as its role/semantics remain intact underneath.
Do: nest a real `<button>` inside the heading; rely on source order rather than `aria-controls` where possible. (IC ch2)

### Headings double as a screen-reader navigation mechanism `AXS-013`
Headings function simultaneously as visible structural labels and as a distinct, non-linear navigation mechanism for screen-reader users, who can jump directly between headings of a given level or of any level. (IC ch1)

### Unstandardized components need an invented accessible contract `AXS-057`
Some components (e.g. tabs) have a prescribed structure mandated by spec (WAI-ARIA), deviated from only with justification; others — the card is the example given — have no equivalent standard, no `<card>` element and no "ARIA card" pattern. For unstandardized components, the accessible contract must be invented by combining known semantic primitives (headings, lists, links) and interaction patterns, balancing sound HTML structure against ergonomic interaction, rather than looked up.
Do: for unstandardized components, compose the accessible contract from established semantic primitives. (IC ch3)

## 2. Labeling (incl. Translation-Safety)

### Fieldset/legend group-labeling for native control sets `AXS-001`
When a choice is expressed as a set of related native form controls (e.g. two mutually exclusive radios standing in for one on/off setting), wrap them in `<fieldset>` with a `<legend>` naming the group, so assistive technology prepends the shared group label to each option's own announcement.
Do: wrap the control set in `<fieldset><legend>naming the setting</legend>...</fieldset>`; give each option its own short label in addition to the group legend. (IC ch1)

### Placeholder/inline-prompt text is not a label substitute `AXS-002`
A field's placeholder or inline prompt must never be its only labeling mechanism: it is transient example content, not a persistent accessible name — browsers/AT don't reliably expose it as one, and it disappears on focus/fill and is erasable by autofill, leaving users without identification exactly when they revisit a filled field. When: labeling any text input; avoid/except: a single input immediately paired with a clearly self-descriptive submit button (e.g. "Search") may validly omit a *visible* label, provided it still carries an accessible (e.g. visually-hidden) one.
Do: provide a visible label in almost all cases; where a visible label is genuinely redundant, use a visually-hidden `<label>` (not `aria-label`) as the accessible name; if placeholder text is still used, give it adequate contrast (WCAG 1.4.3) and a secondary style cue so it isn't mistaken for entered content.
Ask: if this field is revisited later, does it still carry an identifying label once filled or once the prompt has vanished? (IC ch1; DI ch3)

### Translation-safe labeling contract `AXS-003`
Any label, group label, or icon alt text expected to survive machine/on-page translation must be a real, visually-hidden text node associated via `aria-labelledby` — never an `aria-label` value or SVG-internal `<title>`/`<text>` — since translation tooling operates on visible text nodes and skips attribute values and SVG-internal text. When: the interface is expected to run through page-level machine translation; avoid/except: brevity in illustrative example code, where the tradeoff is explicitly being demonstrated rather than shipped.
Do: point `aria-labelledby` at a visually-hidden element with real text rather than setting `aria-label` directly; for inline SVG icons, use a visually-hidden `<span>` sibling, not an SVG `<title>`/`<text>` or `aria-label`. Trade-off: `aria-label` is terser but not machine-translatable; `aria-labelledby` plus a visually-hidden node is translatable but needs an extra element and id wiring — choose translatability whenever the page itself is translatable. (IC ch1-3)

### Decide the role before choosing the ARIA association `AXS-004`
Before implementing supplementary text attached to a control (tooltip, helper text), decide whether it is the control's PRIMARY accessible label (its only name) or a SUPPLEMENTARY description on an already-adequate label — the two need different ARIA relationships, and conflating them computes the wrong accessible name. Some AT also requires the referenced element to carry a label-worthy role (`role="tooltip"`) for the relationship to be honored reliably.
Do: for a primary label, use `aria-labelledby` from the control to the text plus `role="tooltip"` on that text; for an auxiliary description, use `aria-describedby` and provide the control's own accessible name via a separate mechanism (e.g. a visually-hidden span). (IC ch1)

### Multi-id aria-labelledby composes name independent of DOM order `AXS-005`
`aria-labelledby` accepts multiple space-separated ids and composes the accessible name from each referenced element's text in the order the ids are listed — not DOM or visual order — so a name can be assembled from several independently-positioned pieces of content (e.g. a dynamic count plus a static label) without constraining their visual layout.
Do: list multiple ids in `aria-labelledby` in the desired announced order, independent of how the referenced elements are visually/DOM-positioned. (IC ch1)

### Click-triggered disclosure content must not use aria-describedby `AXS-007`
For content revealed by an explicit click/tap (a toggletip), `aria-describedby` is the wrong association: its content is present in the accessibility tree at all times, so a screen-reader user already has access before ever activating the control, making the click appear to do nothing.
Do: use a separate, initially-empty live region populated only on click for toggletip content, instead of `aria-describedby`. (IC ch1)

### Repeated controls sharing generic text need distinct per-row names `AXS-010`
When multiple repeated controls in a list share generic visible text or icon content (e.g. several "on/off" toggles, a "delete" icon button per row), each needs a distinct accessible name incorporating its own row's identifying content — via `aria-labelledby` pointing at the row's text, or a per-row visually-hidden label — rather than every control announcing the same ambiguous name.
Do: point each repeated control's `aria-labelledby` at its own row's identifying text; for icon-only repeated buttons, compose a distinct name incorporating the row's identity (e.g. "delete {item name}"); mark decorative SVG inside such buttons `focusable="false"` so it's never a spurious extra tab stop. (IC ch1)

### aria-hidden on a referenced element doesn't break id-based naming `AXS-028`
An id-based relationship such as `aria-describedby`/`aria-labelledby` still pulls in the referenced element's text even when that element itself carries `aria-hidden="true"` — the reference mechanism operates independently of `aria-hidden`'s effect on browsing-tree traversal, so a purely decorative, visually-styled element's wording can still contribute to another element's announcement.
Do: reference an `aria-hidden` element's text via `aria-describedby`/`aria-labelledby` to still surface its content as part of another element's announcement. (IC ch3)

### Voice and tone is an accessibility contract, not brand copy `AXS-051`
Written UI voice/tone matters not only for sighted users but functions as a primary access channel for users who experience the product mainly through screen readers. Tone guidance should be keyed to each message's emotional/functional goal (a success message can be upbeat; a system-outage message should stay serious/factual) rather than one uniform tone across the whole product, and should be derived from an audited collection of real UI copy.
Do: treat voice/tone quality as part of the accessibility contract, especially for screen-reader-dependent users; collect real copy examples and key tone guidance to each message's goal.
Ask: what is this message's emotional/functional goal, and does the tone actually match it? (DS ch4)

### Label content and placement contract `AXS-052`
A label's wording must be brief, genuinely clear about the resulting action (not merely short — "Submit" is short but uninformative), phrased in the target user's own vocabulary rather than jargon, and used consistently for the same concept throughout a component (never "alert" in one place and "warning" in another). It should sit above or directly on/inside its control, and a text field's only label must never vanish silently (e.g. an in-field label that disappears once typing starts) without a persistent fallback. When: writing any label, or placing an in-field/placeholder label; avoid/except: for a domain-expert audience, domain jargon is the clearer choice.
Do: write labels in plain vocabulary and confirm they state the actual outcome; reuse the same term for the same concept everywhere; place labels above or on their control; provide a persistent label or example text alongside any in-field label that disappears on typing. (MI ch1)

### A title attribute duplicating visible text adds nothing `AXS-006`
A `title` attribute whose value merely repeats an element's own already-visible text supplies no new information to anyone and, for screen-reader users, can cause pure repetition with no benefit.
Do: remove `title` attributes that only restate visible text. (IC ch1)

### title is not a viable accessible information-delivery mechanism `AXS-053`
`title` is not a reliable tooltip/labeling mechanism for inclusive design: its content is inaccessible to touch users, keyboard-only users, and most assistive technology users, and — aside from limited, unreliable support on form inputs — doesn't work reliably in screen reader software at all; relying on it effectively hides its content from those groups. Avoid/except: `title` has limited, still-unreliable support as supplementary info specifically on form `<input>` elements in some screen readers.
Do: provide a clearly worded, permanently visible label instead of relying on `title`.
Ask: is this information reaching touch, keyboard-only, and screen-reader users, or only sighted mouse users who hover? (IC ch1)

## 3. State Communication

### Never communicate state, category, or type through style alone `AXS-024`
Any interface part whose state, category, or type is differentiated only by a single perceptual or format channel — color alone, a bare unlabeled icon alone, shape/position alone, or plain text alone with no fallback for non-text/no-display contexts — is inaccessible to some portion of users. Critical differentiation must be encoded redundantly across at least two independent channels (color plus text, an icon plus a text prefix, or a non-text signal plus a learnable, consistent pattern when text can't be guaranteed available). This is the strongest cross-book agreement in this file: it is independently stated for toggle-button state, disabled-button state, and notification/message-type differentiation, for error/required-field indication, and — in the reverse direction — for cases where text itself isn't always available or legible.
Do: pair color-coded state with a non-color cue (shape, position, icon, text); prefix or otherwise textually mark differentiated message/notification categories, not just color or icon; use real text (e.g. the word "required") rather than a bare symbol like an unlabeled asterisk; where a disabled state relies on greyed-out color alone, consider removing the affordance-carrying element instead, so structure — not color — communicates the state; where text can't be guaranteed available or legible, provide non-text alternatives (sound, light, state change) designed for consistent, learnable meaning. (IC ch1-3; DI ch3; MI ch2)

### Boolean toggle state needs an explicit ARIA state attribute `AXS-017`
A toggle control's on/off (or pressed/unpressed) state must be exposed via an ARIA boolean state attribute (`aria-pressed` or `aria-checked`) carrying the literal string `"true"` or `"false"` — unlike native HTML boolean attributes, omitting it or leaving it valueless communicates no state at all, and its mere presence changes how the control's role is announced (e.g. generic "button" to "toggle button"). Avoid/except: some frameworks (e.g. Vue) silently strip false-valued attributes, so the value may need explicit stringification to survive.
Do: always set `aria-pressed`/`aria-checked` to the literal string `"true"`/`"false"`, never a valueless attribute. (IC ch1)

### role=switch vs aria-pressed: precision-vs-support tradeoff `AXS-018`
For a control that is genuinely and exclusively an on/off switch, `role="switch"` plus `aria-checked` communicates that semantics more precisely than `aria-pressed` (announcing e.g. "switch, on" rather than the generic "pressed"), but this trades against assistive-technology support breadth, which has historically lagged for `role="switch"` — unsupported AT falls back to announcing it as a checked checkbox/button, degraded but still adequate.
Do: default to `role="switch"`+`aria-checked` for genuinely binary controls unless support breadth is the overriding priority, in which case use `aria-pressed`. Trade-off: `role="switch"` gives a more precise announcement but narrower AT support; `aria-pressed` is safer for support breadth but less semantically specific for a literal switch.
Ask: is broad assistive-technology support more important here than the more precise on/off announcement? (IC ch1)

### No redundant visible toggle-state text beside an ARIA state attribute `AXS-019`
When a toggle button carries both `aria-pressed` AND a visible on/off text label duplicating the same state, the redundant visible text must be hidden from assistive technology (`aria-hidden`) so screen-reader users don't hear the state announced twice, or hear it in a way that reads as contradictory.
Do: `aria-hide` any visible state text that duplicates what `aria-pressed`/`aria-checked` already announces. (IC ch2)

### Stable-label-vs-changing-state announcement contract `AXS-020`
A toggle must carry its state-change meaning on exactly one axis at a time: if its visible label text itself changes between states (e.g. "Play"/"Pause"), don't also flip an explicit ARIA pressed/checked attribute in parallel — the label change already communicates state, and combining both risks disagreement about what the current label even means. Conversely, if the label stays stable, state must be communicated via an explicit ARIA state attribute (or a live region) — a bare text-content swap alone is not proactively announced by most screen readers. When: deciding whether the label already fully communicates the state change, or state is carried by a separate ARIA attribute.
Do: pick one axis — label text OR explicit ARIA state — never both at once; for icon-only toggles, keep the accessible name stable, hide the decorative icon (`aria-hidden="true"`), and drive accessible state purely through `aria-pressed`, since voice-control users vocalize what they see and a changing label plus a changing icon can target the wrong action; never rely on a bare text-content swap alone — pair it with an explicit ARIA state attribute or a live region. (IC ch1)

### A disclosure control's label/icon depicts its effect, not its state `AXS-021`
The visible label or icon on a stateful toggle/disclosure control (e.g. a plus/minus expand-collapse icon) should always represent what activating it WILL DO next, not the name of the state it's currently in — e.g. a minus icon while expanded means "this will collapse," not "currently expanded."
Do: show plus for "this will expand" and minus for "this will collapse" — an effect-oriented icon choice tied to the same attribute that drives the accessible state. (IC ch2)

### Drive accessible and visual state from one source of truth `AXS-022`
Where a component has both an accessible state attribute (e.g. `aria-expanded`) and a visually-driven state, both must be derived from the SAME single attribute (e.g. styling off `[aria-expanded="true"]`) rather than toggling a second, parallel representation such as a mirrored CSS class — two independent representations of the same logical state can drift apart, and a single source of truth can't.
Do: style directly off the ARIA state attribute rather than maintaining a separate, parallel CSS class for the same state. (IC ch2)

### Sortable-column state: real button, aria-sort, and a text fallback `AXS-023`
A sortable table column's control must be a real `<button>` nested inside the header cell (`role="columnheader"`), not the header cell itself made clickable. Current sort state is exposed via `aria-sort="ascending"|"descending"|"none"` on the header cell, but because `aria-sort` support is inconsistent across screen readers, the button's own accessible label must also spell out the resulting action in words (e.g. "sort by [column] in ascending order") so state is never conveyed by `aria-sort` or an icon alone.
Do: nest a real `<button>` inside the column header cell; set `aria-sort` on the header cell alongside `role="columnheader"`; give the button a text label describing the resulting sort order, not just an icon. (IC ch3)

### Ambiguous state feedback must never lead to a harmful consequence `AXS-025`
If feedback about a component's state can plausibly be misread, the component's behavior contract must guarantee that a resulting user action never causes harm — the safety burden falls on designing out the dangerous state, not solely on making the signal less ambiguous, since misunderstanding of imperfect feedback is expected to happen. When: state feedback could plausibly be misread AND the resulting action could cause harm or safety risk.
Do: make the component's behavior safe even under a plausible misreading of its own feedback, rather than relying only on clarifying the signal. (MI ch2)

### Communicate why a control is disabled `AXS-026`
A disabled control must never leave its cause unexplained: wherever the interface can't make the reason obvious through spatial proximity alone, surface an explanation of why it's currently disabled and what would enable it — users perceive an unexplained disabled control as broken rather than intentionally inactive. When: a control is disabled and the reason isn't obvious from context.
Do: confirm there's a genuine functional reason the control can't work yet; surface an explanation of cause and remedy when it isn't obvious from layout; keep the trigger that would enable a disabled item visible in the main UI rather than buried in a submenu. (DI ch1)

### Internal state is invisible until feedback makes it concrete `AXS-027`
Because a digital component's internal state and rules aren't physically observable, feedback (visual, audio, or haptic) is the mechanism through which that abstract state is made concrete — a state-affecting change with no proportionate feedback is effectively hidden from the user, even when the underlying rule governing it is well designed.
Do: pair every state-affecting rule with feedback proportionate to its importance.
Ask: if this state change produced zero feedback, would the user have any way of knowing it happened? (MI ch1)

## 4. Live Regions

### Live-region delivery contract: dual role/attribute, no focus move `AXS-029`
To announce a state change to screen-reader users WITHOUT relocating their keyboard focus, apply `role="status"` together with `aria-live="polite"` on the same container (both simultaneously, since browser/AT support for each API varies) and replace the region's content on the event — the announcement fires automatically, decoupled from focus location. Avoid/except: moving focus to the changed content is itself the correct, deliberate UX (e.g. deliberately navigating the user to new content) — not applicable to a pure status announcement.
Do: combine `role="status"` and `aria-live="polite"` on the same live-region element. (IC ch1-3)

### Default live-region politeness to polite when paired with a focus move `AXS-030`
When a status announcement and a focus move happen together (e.g. after deleting the currently-focused element), default the live region to `aria-live="polite"`, which waits for the interface to settle (e.g. a focus-triggered heading announcement to finish) before announcing — an "assertive" region interrupts immediately and can override or truncate a concurrent focus announcement, confusing which message belongs to what. Avoid/except: the message is urgent/time-critical enough that interrupting is genuinely desired, in which case "assertive" is appropriate.
Do: use `aria-live="polite"` with `role="status"` by default when pairing a status message with a focus move. (IC ch1)

### Live-region mount-before-populate timing contract `AXS-032`
Adding a live region to the DOM at the same moment as the content meant to be announced is unreliable — assistive technology needs to have already registered the region as "live" before an in-region mutation can be reliably detected, so there must be elapsed time between mounting the region and inserting its announced content.
Do: mount the empty live region first, then insert the announced content after a short delay/tick — never in the same operation. (IC ch2,3)

### Mute live regions in inactive or hidden browser-tab contexts `AXS-033`
Where a live-region-bearing UI can exist in a hidden/inactive context (e.g. the same app open in a background tab), that instance's live region(s) must be switched off (`role="none"` and/or `aria-live="off"`) while hidden and restored when visible again, detected via the Page Visibility API (`document.hidden`/`visibilitychange`) — a sighted user simply doesn't look at a background tab, but a screen-reader user can't equivalently "not hear" a hidden tab's live region. Avoid/except: some screen reader/browser combinations already auto-silence hidden-tab live regions, but this can't be relied on for all users — the manual toggle remains the required baseline.
Do: toggle role/`aria-live` off for hidden document instances via the Page Visibility API, and restore it when visible. (IC ch2,3)

### Gate real-time announcements by the user's current engagement context `AXS-034`
Whether a real-time event should interrupt the user (be announced) rather than silently update the UI depends on what the user is currently doing: announce events tied to the user's active context (e.g. a new message in the thread they're replying to), but don't interrupt an unrelated task unless the event directly and specifically addresses the user (e.g. an @mention) — don't deprive users of information entirely, just don't interrupt them during a different task unless it truly needs attention right now.
Do: announce updates directly tied to the user's current context immediately; interrupt an unrelated ongoing task only for events that specifically address the user. (IC ch2,3)

### Scope live-region announcements to genuinely new content `AXS-035`
On a persistent, growing live region (e.g. a message stream), set `aria-relevant="additions"` so only newly-appended content triggers an announcement — edits or removals of existing entries must not re-announce — while keeping the underlying markup well-formed and semantically structured (e.g. a real list) so edited or removed content remains discoverable by navigation even though it isn't proactively announced.
Do: set `aria-relevant="additions"` on the live-region parent of a growing list; use semantic list markup so non-announced edits/removals remain discoverable via navigation. (IC ch2,3)

### Aural notification volume needs deliberate throttling `AXS-036`
A firehose of live-region announcements is worse for screen-reader users than the visually-equivalent clutter is for sighted users, because sighted users can visually filter or avert their eyes from clutter at will, while a screen-reader user can't equivalently "tune out" a continuous stream of audio — real-time/chat-style apps must restrict messages to suitable contexts and give users direct control over notification verbosity.
Do: restrict live-region messages to suitable contexts/situations rather than announcing every possible event; give users direct control over notification verbosity. (IC ch2)

### Don't over-announce: aria-atomic default, no routine-motion announcements `AXS-037`
Only set `aria-atomic="true"` when the intent is genuinely to re-announce a live region's ENTIRE content on every change — otherwise leave it at its default (announcing just the changed/added part) — and never wire routine, expected, user-caused UI motion (e.g. every carousel slide scrolling into view) into a live-region announcement as if it were a notification; a documented real-world example (a carousel plugin announcing every slide) is called "a huge irritant."
Do: leave `aria-atomic` unset/false unless the entire region genuinely needs full re-announcement on every change; only announce genuinely notification-worthy changes, not routine or incidental UI motion the user already caused. (IC ch2,3)

### Comparable, not identical, cross-modality experience is the bar `AXS-040`
The standard for an accessible alternative delivery channel (e.g. a live-region announcement standing in for a visual change) is that it serves the SAME PURPOSE as its visual counterpart for all users through parallel channels simultaneously — not that the experience feels identical, and not a separate accommodation carved out only for screen-reader users specifically. Framing the goal as "communicating to users" rather than "screen-reader users" keeps design centered on universal communication rather than a bolt-on accommodation.
Ask: does this alternative delivery mechanism serve the same purpose as the visual experience, even if the experience itself differs? (IC ch2)

### Translate non-verbal visual feedback into a textual status, not a sound `AXS-041`
When a visual interaction includes a non-verbal animated effect (e.g. an item animating into a cart icon), the correct live-region translation is a clear textual status announcement describing the outcome (e.g. "product added successfully"), not a literal sonic equivalent of the animation — a literal sonic translation communicates far less than plain language describing what actually happened.
Do: announce the outcome in plain language via a live region rather than attempting to sonify the animation. (IC ch2)

### Disambiguate a live-region announcement from a focus move `AXS-046`
Because live regions are a comparatively unfamiliar technology, some screen-reader users assume their keyboard focus has moved whenever they hear new content announced, since historically only focus changes triggered announcements. Use explicit clarifying terminology in the announced text ("notification," "update," or "alert") to make clear that context hasn't actually changed. When: composing the copy of a live-region announcement that could plausibly be mistaken for a focus/navigation event.
Do: include a clarifying word ("notification," "update," "alert") in ambiguous live-region messages. (IC ch2,3)

### Live-region content may be arbitrary markup, not just plain text `AXS-038`
Content inserted into a live region to trigger an announcement doesn't need to be a plain text node — it can be any markup, and the announcement fires immediately once that content is inserted, since announcement is driven by DOM mutation inside the region, not a text-only API. (IC ch2)

## 5. Notifications

### Notification routing: actionable gets a dialog and focus, FYI must not `AXS-031`
A notification-type component splits into two behaviorally distinct categories: (1) messages asking the user to take action belong inside a dialog (or inline disclosure) with action buttons, and focus must move into it on open, because the keyboard operator needs to reach those buttons; (2) purely informational "FYI" messages must NOT receive keyboard focus — deliver them via a live region instead, since focus communicates operability, and forcing focus onto content with nothing to operate strands the user there for no reason. Avoid/except: moving focus to a message was historically treated as "best practice" purely because it was the most reliable way to trigger announcement — that justification no longer applies once live regions are available, and shouldn't be used to justify focusing FYI content.
Do: route actionable messages through a dialog and move focus into it; route FYI messages through an ARIA live region and leave focus exactly where it was.
Ask: does this message require the user to choose/act, or is it purely informational? (IC ch2,3)

### Default a notification to being both seen and heard `AXS-039`
Most live-region content should be visible on screen AND announced aurally — visually-hidden (aural-only) delivery should be a narrow special case, not a default pattern. The one legitimate exception is when a change is already fully self-evident visually (e.g. an item visibly joining a list), where a simultaneous visible status message is redundant and can split sighted users' attention across two events for one logical change, so the live-region text should be visually hidden while still announcing to screen readers. When: is there a specific reason this content should be aural-only, or is the visual change already sufficient on its own?
Do: make live-region content visible on screen as well as announced, by default; visually hide it only when it would otherwise duplicate an already fully self-evident visible change. Trade-off: a visible status message adds explicit confirmation for sighted users but can compete for attention with the primary visible change it describes when both fire simultaneously for one event. (IC ch1,2)

### Notification preferences must be explicit, granular, user-controlled `AXS-042`
Per-notification-type controls must live in a real settings screen the user actively controls (one toggle per type, grouped as native form controls), rather than the product deciding on the user's behalf which types matter — turning off a type must remove it from both visual and aural output together, and every user gets the same granular control regardless of assumed group needs, since giving every user the same explicit choice avoids paternalistic assumptions on behalf of any group.
Do: expose one on/off toggle per notification type in a real, discoverable settings screen; ensure disabling a type removes it from both visual and aural delivery; don't assume which notification types a given user group wants and hide the choice from them. (IC ch2,3)

### Prefer automatic, timed disappearance over manual dismiss `AXS-043`
Rather than requiring the user to actively dismiss a transient, non-actionable notification, let it disappear by itself after an appropriate duration — a manual "×" dismiss button is usually not worth its cost: an extra interaction most users never need, and a real focus-management problem once the button itself is removed from the DOM after being pressed. Avoid/except: the message genuinely needs to persist until acknowledged — that belongs in a dialog (the actionable-message path), not an auto-expiring FYI notification.
Do: auto-expire FYI notifications after a suitable duration by default. Trade-off: manual dismissal gives the user direct control over timing, at the cost of an extra interaction and a focus-management edge case when the dismiss button removes itself from the DOM. (IC ch2,3)

### A transient notification must never be the sole source of its information `AXS-044`
It's acceptable for a user to miss a transient notification as it comes and goes, but only if the notification's content is also durably discoverable elsewhere in the persistent interface (e.g. a "user came online" notification is also reflected in a persistent active-users list; an "award earned" notification is also recorded in a permanent profile history) — the harder, more important design task is the structure of that permanent record, not the live-region delivery mechanism itself.
Do: ensure every notification's content is also durably represented elsewhere in the interface before shipping the transient notification itself; prioritize design effort on the permanent record's structure and language, not just the live-region mechanics.
Ask: if a user misses this notification entirely, can they still discover the same information elsewhere in the interface? (IC ch2,3)

### Be wary of desktop/OS-level push notifications `AXS-045`
Requesting or defaulting to desktop/browser push-notification permissions should be treated with strong caution, since they operate outside the page's own accessible/inclusive design controls and interrupt users at the OS level — a much more intrusive channel than in-page notifications.
Do: don't default to requesting desktop push notifications without a specific, compelling reason. (IC ch2)

## 6. Tables & Structure-Heavy Components

### Table markup is a real semantic/behavioral contract `AXS-047`
Table elements (`<table>`, `<th>`, `<td>`) tell browsers to expose specific structure and elicit specific AT behaviors (row/column navigation, header announcements) — using them for non-tabular content, or styling a `<td>` to merely look like a header, breaks that contract even though sighted non-AT users see nothing wrong. Header cells must be `<th>` with an explicit `scope="col"`/`scope="row"`, which is what lets a screen reader announce the relevant header(s) on navigating into a data cell. "Don't use tables for layout" is correctly understood as "don't use an HTML element for a purpose other than the one it declares." When: choosing whether table markup fits a given content, retrofitting an unavoidable legacy layout table, or making a wide data table responsive on narrow viewports.
Do: mark header cells `<th>` with explicit scope, never a styled `<td>`; reserve `<table>` for genuinely tabular data, use modern CSS layout for visual grids; apply `role="presentation"` to strip semantics from an unavoidable legacy layout table; don't use CSS display overrides to reflow a table's rows/columns for narrow viewports — this tends to strip the table's semantics from the accessibility tree even though the DOM still uses `<table>`/`<tr>`/`<td>`, and stops it reading visually as "the same table"; instead let the container scroll horizontally (`overflow-x`), and for very narrow viewports swap to a genuinely different semantic structure instead of squeezing the wide one. (IC ch3)

### `<caption>` is the correct table-label element; `<summary>` is deprecated `AXS-048`
Every non-purely-presentational table should have either a `<caption>` (optionally nesting a heading such as `<h2>`) or a preceding heading, unless it's already inside a `<figure>` with a `<figcaption>`; the deprecated `summary` attribute behaves like invisible alt text and is unnecessary once the table communicates its own content via caption or heading. A caption is both visually and screen-reader accessible and is read out directly when a user jumps to the table via its dedicated shortcut; nesting a heading inside it combines table-shortcut discovery, heading-shortcut discovery, and normal linear browsing as three independent ways to find the same table without duplicating the label. Avoid/except: never use the deprecated `summary` attribute — it is not a viable substitute for `<caption>`.
Do: use `<caption>`, optionally nesting a heading, for every genuine data table; rely on an enclosing `<figcaption>` if the table already sits inside a `<figure>`. (IC ch3)

### Generate table markup from a validated data shape `AXS-050`
A reusable table component should accept structured data (a headers array and a two-dimensional rows array) as its API and generate the correct accessible markup (`<th scope>`, `<td>`, `<caption>`) from it automatically, validating the input shape to surface authoring errors early — rather than relying on every author to hand-write correct, complete table markup, which is routinely malformed or missing required headers.
Do: derive header/cell markup automatically from a typed data shape; validate the shape of headers/rows props to catch authoring errors early. (IC ch3)

### Row headers are an optional, situational table-header variant `AXS-049`
Column headers (`scope="col"`) are broadly necessary for a data table; row headers (`scope="row"`) are an optional, situational addition — appropriate when a table has a natural per-row "key" value that other cells in that row relate to — rather than a universal requirement. When: there is a natural "key" value per row that other cells in that row relate to.
Do: add `scope="row"` headers when a table has a clear per-row identifying value. (IC ch3)
