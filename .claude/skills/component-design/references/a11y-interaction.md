# Accessibility Contracts II — Keyboard, Focus & Multimodality

This file serves decisions about how a component behaves once its visual design is settled: what
keys and gestures operate it, where keyboard focus goes and returns to, what a disabled state
actually costs, how it holds up across mouse/keyboard/touch, and what it must still do before any
JavaScript enhancement runs. Route here when defining a component's keyboard or focus contract,
choosing how hover-only behavior should degrade for keyboard/touch users, deciding whether an
enhancement is worth its cost against a working baseline, or auditing a component against
forced-colors mode and auto-moving-content requirements.

## Contents
- Keyboard Contracts
- Focus Management
- Disabled-State Costs
- Touch & Multimodal
- Progressive Enhancement & Baselines
- Inclusive-Design Meta-Principles

## Keyboard Contracts

### Keyboard/AT access is a required path, not a power-user convenience `AXK-005`
Every action reachable via mouse or hover — menu items, hover-triggered flyouts, hidden/collapsible
panels — must also be reachable via keyboard and usable by assistive technology, following
platform-standard shortcut/access-key conventions rather than inventing new ones. Any important
action keeps a visible, discoverable path even when a shortcut exists, and a panel that can be
hidden needs a visible on-screen control to reopen it, not only a shortcut a user may not know.
Where a hover-triggered mechanism genuinely can't be made keyboard/AT accessible, fall back to a
more static equivalent instead of shipping an inaccessible interactive one.
Do: follow standard shortcut/access-key conventions; keep a visible fallback path for any
important action; give hidden/closed panels an on-screen reopen control; verify hover flyouts
work via keyboard/screen reader before shipping, substituting a static pattern if they can't.
Ask: if this user had no mouse and didn't know any shortcut, could they still find and use this
feature?
(DI ch3, ch4, ch6; MI ch3)

### True ARIA menu button: keyboard/focus contract `AXK-001`
A true application-style menu button opens on Enter/Space/Down-arrow, moves focus among items
with Up/Down-arrow (wrapping), closes on Up-arrow-from-button or Escape (returning focus to the
button), and reserves Tab for leaving the whole menu in one step rather than stepping through
every item. Menu items carry tabindex="-1" so they're script-focusable but excluded from Tab
order; opening the menu focuses its first non-disabled item, never the first item regardless of
state. A persistent single-choice variant uses role="menuitemradio" + aria-checked and must focus
the currently-checked item on reopen, not default to the first.
Do: bind Enter/Space/Down-arrow to open and Up-arrow-on-button to close; move focus with arrow
keys only, wrapping at the ends; on open, focus the first non-disabled item (or the checked item
for persistent-choice menus); on Escape/selection, close and return focus to the trigger; use
role="menuitemradio"+aria-checked for persistent single-choice items.
Ask: can a keyboard user exit the whole menu with one Tab press instead of stepping through every
item? Does reopening a persistent-choice menu focus the currently selected item?
(IC ch4)

### Menu markup/semantics contract, and why navigation submenus must not borrow it `AXK-004`
A true ARIA menu button's trigger keeps aria-haspopup="true" fixed at all times (a static
capability warning, not a toggled state) while aria-expanded toggles true/false to report actual
open/closed state; a decorative disclosure-triangle glyph should be aria-hidden, since
aria-haspopup already communicates non-visually that activating it opens a popup. This full
menu-role machinery (aria-haspopup, role="menu"/"menuitem") must NOT be applied to a hover/focus-
revealed navigation submenu whose top-level item is also a real destination link — true ARIA
menus assume application-style, click-only activation with no independent link function, and
imposing that on a navigation trigger breaks direct navigation to the top-level page.
Do: keep aria-haspopup static and toggle only aria-expanded for real menu buttons; hide decorative
glyphs with aria-hidden; never apply role="menu"/"menuitem"/aria-haspopup to a navigation dropdown
whose trigger must stay a followable link.
Ask: if I applied full ARIA menu semantics here, would users lose the ability to navigate
directly to the top-level page?
(IC ch4)

### Tabs keyboard contract: WAI-ARIA baseline vs. tested deviation `AXK-002`
The WAI-ARIA tabs pattern specifies Left/Right-arrow to move focus and selection between tabs
(looping, via roving tabindex), reserving Tab to leave the tablist. Real user testing —
third-party and the author's own session with a blind, tech-savvy user — found many users,
including screen-reader power users, simply don't know the arrow-key-only convention, since Tab
reaches nearly every other interactive control on the web. Trade-off: strict ARIA-tabs
conformance (arrow-keys-only, Tab exits the tablist) vs. tested discoverability (tabs also
reachable by ordinary Tab; activation moves focus into the panel) — the tested deviation is
treated as justified specifically because it was validated against documented user confusion, not
chosen by default.
Do: implement arrow-key selection with wraparound and roving tabindex as the baseline,
additionally let tabs be reached by ordinary Tab navigation, and move focus into the tabpanel on
activation rather than only revealing it.
Ask: if a user only knows how to press Tab, can they still reach every tab and its content?
(IC ch7)

### Deviating from standardized ARIA patterns requires evidence, not preference `AXK-003`
It's legitimate to deviate from a standardized ARIA authoring-practice pattern when testing
provides compelling evidence the prescribed pattern fails real users — never on a hunch.
Conventions vary in strength: a narrow, component-specific convention (tabs' arrow-key-only
navigation) can be outweighed by a much stronger, near-universal one ("you can Tab to any
interactive control") once real usage data shows the narrower one is failing people. When:
compelling testing evidence exists; avoid/except: deviating purely on personal preference without
such evidence is not justified.
Do: treat documented usability-testing failures of a spec-prescribed pattern as sufficient
grounds to deviate; don't deviate without that evidence.
Ask: what testing evidence, specifically, motivates deviating from the standard pattern here?
(IC ch7)

### Unresolved trade-off: reaching tabpanel content is not solved cleanly by any single technique `AXK-036`
Letting a user move from an inactive tab position into its panel's content has no clean universal
solution. Giving every tabpanel tabindex="0" lets users tab/arrow into it, but VoiceOver on macOS
mishandles focusable elements nested inside other focusable elements (the next Tab stop lands
after, not inside, the panel), and a focusable-but-otherwise-inert panel arguably violates WCAG
2.4.3 Focus Order. Trade-off: tabindex="0" on panels reaches broadly but breaks in VoiceOver and
risks Focus Order violations; aria-controls (as a "jump to panel" shortcut) works but is honored
only by JAWS among assistive technologies — neither is a cross-AT solution.
(IC ch7)

### Tabs at narrow viewports: don't hybridize into an accordion, but visual tab styling can drop `AXK-037`
Reconfiguring a tabbed interface into an accordion specifically for small viewports is
discouraged: tabs and accordions have distinct accessible structures and keyboard contracts, so a
responsive hybrid means maintaining two structurally different accessible widgets bridged at a
breakpoint. Where the number of tabs is large or unknown, using an accordion at all widths is the
safer, simpler default. Separately, once a tabbed interface reflows to a single column at narrow
viewports, it no longer needs to look like tabs visually so long as the selected item stays
clearly marked — the underlying tablist/tab/tabpanel roles and aria-selected are decoupled from
visual styling.
Do: use an accordion at all widths when tab count is large/unknown instead of a tabs/accordion
hybrid; keep the selected-item indicator clear even after visual tabs are dropped at narrow
widths.
Trade-off: engineering complexity of a true tabs/accordion hybrid vs. the simplicity of
committing to one pattern.
(IC ch7)

### Scrollable-region keyboard-focus contract `AXK-006`
A custom scrollable region (slider, wide table wrapper) isn't focusable by default, and keyboard
users have no hover/mouse cursor to trigger scrolling, so it must be deliberately made
keyboard-focusable — but only conditionally, when its content actually overflows at the current
viewport (detected at runtime), never unconditionally. Once focusable it needs an explicit
accessible role and name (role="region" with aria-labelledby, since aria-label isn't reliably
exposed on an otherwise-inert div with no supporting role) and a visible focus style, and the
design must also visually signal that more content exists off-screen rather than relying on
functional scrollability alone.
Do: detect overflow at runtime and toggle tabindex="0" accordingly; pair a focusable region with
role="region" plus aria-labelledby/aria-label; apply a visible focus style; add a visible or
accessible hint that more content is scrollable.
Ask: on a viewport where this region doesn't overflow, does it still needlessly appear in the tab
order? Does a screen reader user landing here understand why it's focusable and scrollable?
(IC ch9, ch11)

### Toggle/disclosure trigger placement, state-timing, and connection-mechanism contract `AXK-007`
A toggle button must live inside the region/element it controls, not outside it, so a screen
reader user who jumps directly to that region via a navigation shortcut still lands somewhere
they can find and operate the trigger. For a purely decorative, visual show/hide reveal over
content that stays keyboard-reachable in normal tab order regardless, change the announced
aria-expanded state only on click, not on focus, since users don't expect state-change chatter
from mere tabbing. Do not rely on aria-controls to connect a toggle to its content — cross-AT
support is too inconsistent; instead ensure the revealed content's first focusable item is the
very next element in DOM/focus order after the toggle, or move focus to it programmatically, with
aria-controls only as a harmless extra.
Do: place the toggle as a child of the region/list it controls; update aria-expanded on click
only for decorative reveal toggles; place revealed content immediately after the toggle in
DOM/focus order, or move focus to it programmatically, rather than relying on aria-controls alone.
Ask: if a screen reader user jumped straight into this region via a landmark shortcut, would they
find an empty region with no way to reveal its content?
(IC ch4)

### Match the native HTML element to the control's actual semantic meaning `AXK-020`
Prefer a native HTML element whose built-in semantics genuinely match a control's meaning over a
custom-scripted equivalent: a binary on/off setting maps to a native checkbox with a label
(keyboard- and screen-reader-operable by default, announcing its own state change with no
JavaScript); a general two-state toggle unrelated to form submission maps to
button[type="button"] with an explicit aria-pressed value; radio inputs sharing a name attribute
automatically form a keyboard-navigable group where arrow keys move selection — real interaction
behavior, not just a label; a condensed-navigation menu maps well to a native <select>. When
repurposing <select> for navigation, don't auto-navigate on selection change via JavaScript —
that's an unexpected change of context triggered merely by input (WCAG 3.2.2); pair it with an
explicit confirm/go action instead. Use real <a href="#route"> elements for SPA view-switch
controls even when default navigation is intercepted and replaced with JS-driven view switching,
so browsers/AT can announce the control via native same-page-link behavior.
Do: use native checkbox+label for on/off settings, button[type="button"]+aria-pressed for general
toggles, native radio-group name-sharing instead of scripted arrow-key navigation, and native
<select> for condensed navigation only paired with an explicit confirm action.
Ask: is there a native element whose built-in semantics already match what this control needs to
do?
(IC ch2, ch4, ch7)

## Focus Management

### Return-to-origin focus contract, including a vanished-trigger/removed-target fallback `AXK-011`
Closing or dismissing a transient overlay (menu, modal dialog) must return keyboard focus to the
element that triggered it, restoring the user to exactly the place/context they were at before it
opened — a general contract for any such component, not specific to one widget. Where the
currently-focused element is itself removed from the DOM (a delete action removes its own
trigger, or a dialog's confirming action removes the row that opened it), browser behavior is
undefined — some browsers retain a ghost focus, some jump elsewhere, some fall back to the
document root, forcing users to re-navigate from the top. The contract must therefore explicitly
choose a still-present, contextually useful fallback target (the first remaining sibling row, or
a stable heading/landmark when the list becomes empty) and set focus to it deliberately, commonly
via tabindex="-1" plus a scripted .focus() call for elements not otherwise focusable — including
same-page anchor targets, since native fragment-navigation focus is unreliable across browsers —
rather than leaving post-action focus to undefined default behavior.
Do: return focus to the triggering control when a popup/menu closes; restore the exact prior
context when a modal is dismissed; explicitly .focus() a deliberately chosen fallback whenever the
default target has been removed from the DOM; use tabindex="-1"+.focus() for programmatic-only or
fragment-link targets without applying visible focus styling to them, since they aren't truly
interactive; default to the first remaining sibling after a row deletion, falling back to a
stable heading/landmark when the collection becomes empty.
Ask: if the element a popup or dialog would normally return focus to has since been removed,
where does focus go instead? Has this been tested in a browser where fragment/removal focus
behavior differs?
(IC ch3, ch4, ch12; DI ch3)

### Dialog initial-focus contract: first actionable control, not the wrapper `AXK-012`
When opening a custom modal dialog, move initial focus to the first interactive element inside it
(e.g. its primary button) rather than to the dialog's non-interactive wrapping container.
Focusing an actionable element inside a properly-labeled dialog simultaneously triggers
assistive-technology announcement of the dialog's accessible name/content (via its
aria-labelledby association) and places the keyboard user directly on a usable control — one
action, two outcomes.
Do: move initial focus to the first actionable control inside the labeled dialog container on
open.
Ask: when this dialog opens, does focus land on something the user can actually act on?
(IC ch12)

### SPA route-change focus and document-title orientation contract `AXK-013`
Replacing page content on a client-side route/view change does not by itself move
sighted-keyboard or screen-reader focus to the new content, so the app must deliberately focus
either the new view's principal heading or an outer tabindex="-1" wrapper, labelled via
aria-labelledby referencing the view's own visible heading (preferred over aria-label to avoid
label/text drift and preserve translatability) and paired with role="region". Independently,
document <title> must also update on every route change (e.g. "[App name]: [View name]"), because
on initial load, before any view-specific element has been focused, the announced page title is a
screen reader's primary orientation cue.
Do: focus the new view's heading or an outer tabindex="-1" wrapper on every route change; label
the focused container via aria-labelledby referencing its own heading, with role="region"; update
document.title on every route change.
Ask: after a client-side navigation, does a screen reader user get any signal at all that the
page changed?
(IC ch7)

### Never hand out a focus stop without something genuine to do there `AXK-014`
Focus should never go to something the user can't perceive or meaningfully act on. Content that
isn't currently visually perceivable (a slide scrolled out of view) must not be Tab-reachable; a
purely informational (FYI/status) message must never receive keyboard focus, since focus implies
operability and stranding a user on a non-operable element misleads them; a decorative icon
nested inside an already-interactive control must be prevented from becoming an independent tab
stop. For content that's merely offscreen but still logically present, use tabindex="-1" rather
than aria-hidden, so screen-reader users can still discover it via virtual-cursor browsing and get
an accurate count of the full collection — reserve aria-hidden for content that should truly be
excluded from all AT traversal. Correctly hiding (not merely shrinking) collapsed content removes
it from the focus order entirely, so keyboard users don't step through it to reach content further
down the page.
Do: restrict focus order to currently visible, genuinely operable items; never move focus to a
purely informational message; prevent nested decorative icons from becoming independent tab
stops; use tabindex="-1" (not aria-hidden) for interactive content that's merely offscreen; fully
hide collapsed content so it's removed from the tab order.
When: a brief violation of the invisible-content rule isn't catastrophic, since browsers natively
scroll a newly-focused element into view as a fallback.
Ask: if a sighted keyboard user tabs to this element, can they see it and do something with it?
(IC ch8, ch9, ch10)

### Focus-visible contract: visible, stable, and forced-colors-safe `AXK-008`
Every focusable interactive element needs a visible focus style so keyboard users can track which
element has control, and that style should avoid changing layout (position/size), since a
jiggling interface is disorienting. Because Windows High Contrast Mode strips box-shadow, a focus
(or hover-mirroring) style built on box-shadow must also include a paired transparent outline
that becomes visible once forced-colors mode is active, so the indicator survives there too.
Do: prefer non-geometry-shifting focus indicators; pair any box-shadow-based focus/hover style
with a transparent outline that becomes visible under forced-colors mode.
Ask: does this focus indicator remain visible under Windows High Contrast Mode / forced-colors
themes?
(IC ch2, ch13)

### Hover affordance needs a genuinely equivalent focus affordance, via :focus-within `AXK-009`
Where a whole-component hover style (a card's box-shadow) signals interactivity, keyboard users
need an equally prominent equivalent, not just a small, local :focus style on the interior link —
use :focus-within on the container so the same whole-component style fires when the interior
control is keyboard-focused. Because :focus-within has inconsistent legacy support, apply a plain
:focus fallback unconditionally first, and never combine :hover and :focus-within in one
comma-separated selector list — an unsupported selector invalidates the entire rule, silently
breaking the well-supported :hover behavior too in browsers lacking :focus-within.
Do: mirror whole-component hover styling with :focus-within on the container; keep a baseline
plain :focus rule as a fallback; write :hover and :focus-within as separate rule blocks, never
combined in one selector list.
Ask: in a browser without :focus-within support, does this component still show some focus
indicator?
(IC ch13)

### CSS visual reordering must not diverge from keyboard focus order `AXK-010`
Manipulating element order visually with CSS (Flexbox/Grid order) independently of DOM order
risks making the keyboard focus order contradict the visual layout, causing a sighted keyboard
user's tab traversal to jump around the screen non-sequentially. This risk only applies to
elements that are or could become focusable; it doesn't materialize for purely decorative,
non-interactive reordered elements. When: the reordered element is focusable or could become so;
avoid/except: safe when the reordered element isn't focusable at all (e.g. a decorative image).
Ask: does tabbing through this reordered layout still move visually in a sensible reading order?
(IC ch13)

### Hover-triggered content needs a focus-triggered equivalent `AXK-019`
Any content revealed on mouse hover (most notably tooltip text) must also be revealed on keyboard
focus — a hover-only reveal leaves keyboard and screen-reader users missing information exactly
as a sighted mouse user would if text only ever appeared on hover. This can be implemented in
pure CSS by driving the same display toggle from both the :hover and :focus pseudo-classes on the
triggering element, typically inside a position:relative wrapper so the position:absolute tooltip
can be placed reliably nearby.
Do: reveal any hover-triggered content on focus as well; drive a CSS-only tooltip's visibility
from both :hover and :focus on the trigger.
Ask: can a keyboard-only user, with no mouse, still see this hover-revealed content?
(IC ch5)

## Disabled-State Costs

### Disabling has costs: a "disabling has costs" contract family `AXK-015`
The native disabled attribute removes a control from the tab order entirely: disabling a submit
button to block invalid input makes it invisible to keyboard/AT users tabbing through the form
(prefer aria-invalid plus an accessible error message instead, letting users focus and attempt to
press it, then reporting what's wrong); disabling a control the user currently has focused creates
real friction, since they may tab away and back expecting Tab to still reach it. For temporary,
state-dependent disabling (e.g. a boundary-reached prev/next button), there's no universal answer
for keeping a control in the tab order (redundant but stable) vs. dynamically removing it (avoids
redundancy but can disorient) — test the specific component in context. Where a genuinely
disabled-but-still-discoverable state is wanted, use aria-disabled="true" with explicit tabindex
management rather than the native disabled attribute, since tabindex can't restore focusability
once disabled removes it; whichever mechanism is used, never leave a disabled control's cause
unexplained.
Do: prefer aria-invalid plus an accessible error message over disabling a submit control to block
invalid input; use aria-disabled plus manual tabindex management (not native disabled) when a
discoverable/announced disabled state is wanted; surface an explanation wherever the reason isn't
obvious from layout alone; test in context, with real content, whether a state-dependent control
should stay in or cycle out of the tab order.
Trade-off: native disabled gives an unambiguous visual signal to sighted mouse users at the cost
of keyboard/AT discoverability; keeping an inert control in the tab order is redundant but stable,
while removing and re-adding it as state changes avoids redundancy but can disorient — the source
explicitly declines to universally resolve this.
Ask: if a keyboard user currently has this control focused, what happens to their position when
it becomes disabled? Can a user tell why a disabled control is disabled, or does it just look
broken?
(IC ch3, ch9; DI ch4)

## Touch & Multimodal

### Touch target size and hit-area contract `AXK-016`
Important tappable targets need a minimum size of roughly 1cm/44px square with adequate spacing
from neighbors, because a fingertip is far less precise than a mouse pointer, especially under
real-world conditions like a moving device or user. The tappable hit area doesn't need to match
the visible/rendered size — it can extend invisibly into surrounding margin/padding so the
control stays easy to hit while its visual footprint stays as compact as the design calls for
("iceberg tips"). Pad or enlarge the hit area further whenever a small target sits close to or
overlaps another interactive target, which especially benefits users with low pointer precision.
Whichever technique expands the pointer/touch hit area, it's a purely presentational, pointer-only
layer: the underlying keyboard-focusable DOM structure must stay unaffected — Tab order and screen
reader interaction do not change.
Do: size important tappable targets at minimum ~1cm/44px square with adequate spacing; extend the
tappable hit area via padding/margin rather than growing the visible control; pad small or
closely-spaced targets further to reduce mis-taps; keep exactly one real focusable element
regardless of which hit-area technique is used.
Ask: on a moving bus, with an imprecise finger tap, is this control still reliably hittable
without hitting its neighbor? Does expanding this click target change what a keyboard or
screen-reader user actually reaches?
(DI ch10; IC ch13)

### Hover-revealed interaction is ambiguous and undetectable on touch `AXK-017`
A navigation trigger that both reveals a submenu on hover/focus and is itself a followable link is
genuinely ambiguous on touch: the first tap simultaneously requests "open the submenu" and
"follow the link," and there's no reliable way to detect "touch devices" to special-case this,
since screen size doesn't correlate with touch capability. Detect touch as a per-interaction event
(an actual touchstart), not a device-level capability, since many devices support touch alongside
mouse/keyboard simultaneously. The preferred resolution is a device-agnostic redesign — most
notably, giving each top-level destination its own in-page table of contents covering the same
sub-items — rather than intercepting the link with JavaScript to fake full ARIA menu semantics,
which breaks direct navigation to the top-level page. When: applying full ARIA menu semantics can
be acceptable when the control is genuinely an application-style action menu with no independent
navigational destination to preserve.
Do: detect actual touch usage via a touchstart-style event rather than gating on assumed device
capability; prefer giving each top-level destination its own table of contents over intercepting
link clicks with JS to fake menu semantics.
Ask: on a touch-only device, is the first tap on this control unambiguous?
(IC ch4, ch9; DI ch6)

### Hover/focus tooltips fail on touch; a click-triggered toggletip is the robust cross-modal fix `AXK-018`
A tooltip revealed on hover/focus doesn't work for touch users because focus and the active/press
state fire essentially simultaneously on touch — the tooltip becomes visible only for the instant
the control is actually being pressed, too late to inform the decision to press it. How serious
this is depends on how costly or recoverable an uninformed press would be; mitigations include
suppressing the actual action on a first press so it only reveals the tooltip ("tutorial mode"),
or inline text for new users streamlined to icon-only for established users. The more robust fix
is to replace the pattern entirely with a click/tap-triggered toggletip: an initially-empty
role="status" live region is populated with the bubble's content only on activation (revealing it
visually and announcing it to screen readers), and a repeat click clears then repopulates the
region after a short delay to force re-announcement, rather than modeling the trigger as a literal
on/off toggle button.
Do: consider a first-press "tutorial mode" or inline-then-icon-only labeling as mitigations;
prefer a click/tap-triggered toggletip built on an initially-empty role="status" live region over
a hover/focus tooltip where touch matters; clear then repopulate the live region on repeat
activation rather than modeling a real toggle state.
Ask: on a touch device, does this control's help text actually inform the decision to press it,
or only appear after the press already happened?
(IC ch5)

### Native scrollable/interactive regions are multimodal for free `AXK-021`
Browsers are multimodal by default (mouse, keyboard, and touch where supported) for genuinely
native interactive/scrollable content: building horizontally-traversable content atop a native
scrollable region gets mouse-drag/scrollbar interaction, trackpad-gesture scrolling, touch-swipe,
keyboard access, and screen-reader "browse mode" traversal all simultaneously with very little
implementation effort — the resulting motion is also smoother and more performant than a custom
JS-timer-driven animation. The same logic applies to a region's scrollbar itself: styling and
revealing the browser's own native scrollbar is more efficient and reliable than reimplementing
one, and degrades gracefully in non-supporting browsers rather than breaking.
Do: base horizontal/traversal content on a natively-scrollable region where possible, rather than
reimplementing mouse/touch/trackpad support with custom JS; style the native scrollbar rather than
building a custom one.
Ask: does this component need extra screen-reader- or touch-specific handling, or does building it
on native scroll already cover those modalities?
(IC ch9)

### Multimodal interaction paths are additive, never exclusive `AXK-027`
After adding a new interaction path to a component (e.g. prev/next buttons on top of an already
scroll-operable region), don't remove any interaction method that was already working just
because it now seems redundant to a new one — different users prefer different methods, so err on
the side of preserving every previously-supported path. Conversely, adding a conventional,
seemingly-redundant control is still often worthwhile even when the component is already operable
another way: it increases recognizability of the interaction pattern and lets users "snap"
precisely to a target rather than relying on the imprecision of free-form scrolling.
Do: keep every previously-supported interaction path available after adding a new one; consider
adding conventional controls even when direct interaction already works, for recognizability and
precision.
Ask: does adding this new interaction path remove or weaken any interaction path that already
worked?
(IC ch9)

### Explicit instructions as an inclusive-design fallback, exposed to every user `AXK-028`
"If in doubt, spell it out": when a component's usability depends on a non-obvious interaction
(e.g. that a region can be scrolled), provide plain-language instructional text rather than
relying purely on implicit affordance cues, which can be missed or ambiguous — though a purely
implicit cue (content partially cut off at the edge) plus a focus style can be judged sufficient
on its own when discovery isn't critical, trading certainty for terser code. Whichever approach is
used, expose the instructional content to ALL users of the region (e.g. via aria-describedby)
rather than gating it based on assumptions about which input modality a given user happens to be
using.
Do: provide explicit instructional text when a component's interaction model isn't fully
self-evident from implicit cues alone; associate it with the region (aria-describedby) so all
users receive it regardless of assumed input modality.
Trade-off: an implicit visual cue is terser but a less certain signal than explicit text; separate
hover-specific/focus-specific/combined messages give mode precision but add complexity, while a
single generic instruction ("scroll for more") exposed to everyone is often adequate, trading mode
precision for simplicity.
Ask: is this instruction available to every user of the component, or only to the ones assumed to
need it?
(IC ch9)

## Progressive Enhancement & Baselines

### The no-JS baseline must remain a complete, usable experience `AXK-022`
Before any JavaScript enhancement, a component should degrade to a plain, fully-usable baseline
made of ordinary document structure: a collapsible nav region is a bare, always-visible <nav>
with no toggle; a collapsible section is simply a heading followed by its content; a tabbed
interface is an in-page table of contents made of same-page links to page sections, mapping
directly onto the enhancement's structure (table of contents becomes tablist, each link becomes a
tab, each linked section becomes a tabpanel); a toggletip's baseline shows its content
inline/visible by default and enhances INTO the toggle behavior, rather than hiding content
behind an unreliable title attribute as the floor. The enhancement step — not the base markup —
is what introduces any hidden/collapsed/toggled state.
Do: author base markup as always-visible, ordinary document structure with no toggle/hidden
state; add the toggle control and hide/enhance content only as a JS-driven enhancement step;
build a tabbed interface as an enhancement layered over a table-of-contents baseline; show a
toggletip's content inline by default and enhance into the toggle behavior.
Ask: with JavaScript disabled, can a user still reach and use all of this component's content?
(IC ch4, ch5, ch7, ch8)

### Progressive enhancement has a floor: never sacrifice usability to stay JS-free `AXK-023`
Minimizing added technology layers (avoiding JavaScript) is a genuine engineering value — each
layer on top of HTML/CSS is a real increase in systemic complexity and fragility — but this
principle is always subordinate to the component actually working for users. Some components (a
full-featured application menu button, for instance) can't be built satisfactorily without
JavaScript; a CSS-only approximation like the checkbox hack can spoof visibility and even an
aria-expanded announcement, but genuine keyboard-interaction behavior (arrow-key navigation,
Escape, managed focus) fundamentally requires script-driven event handling that CSS can't
provide, so it remains an explicitly incomplete substitute, acceptable only when the revealed
content itself doesn't need that missing behavior. Trade-off: fewer technology layers reduces
complexity/fragility risk, at the cost of how behaviorally complete the component can be; a
JS-free approximation is coherent only where the underlying content doesn't need the missing
behavior.
Do: prefer not introducing JavaScript unless it's actually needed; never degrade a component's
real keyboard/focus behavior purely to achieve a JavaScript-free implementation.
Ask: is this JS-free implementation still fully keyboard-operable, or has real behavior been
quietly cut to avoid JavaScript?
(IC ch4)

### Feature-detect before rendering; enhancements stay optional sugar `AXK-024`
When a component's core function depends on an optionally-supported browser/CSS feature, and that
feature is undetected, the component should not render at all rather than render in a silently
broken state — a rendered-but-non-functional control misleads users into thinking a feature
exists when it doesn't. The same logic applies to additive enhancement controls (extra prev/next
buttons depending on IntersectionObserver): only render them if their own dependency is actually
supported, keeping the component fully mouse-, keyboard-, and touch-operable without them —
optional sugar layered on top of, never a prerequisite for, basic operability.
Do: feature-detect a component's core dependency and withhold the whole control if unsupported,
rather than rendering a broken one; gate an enhancement's rendering on its dependency's feature
detection while keeping the component fully operable without it.
Ask: in a browser lacking this feature, does the user see nothing, or a control that looks present
but silently fails?
(IC ch6, ch9)

### A JS-dependent resource-swap enhancement must not regress the no-JS baseline `AXK-025`
When a component swaps in a resource via JavaScript (e.g. a lazy-loading data-src placeholder
pattern), users without JavaScript running would otherwise see nothing at all, since the swap
logic never executes — provide a <noscript> fallback containing the real resource (e.g. the image
with its true src already set) so it still reaches users without script support.
Do: provide a <noscript> fallback with the true resource already referenced whenever a
JS-dependent resource-swap enhancement is used.
Ask: without JavaScript running, does this content still appear at all?
(IC ch9)

### Justify enhancement cost: skipping or rolling back an enhancement is a valid default `AXK-026`
Leaving underlying content unenhanced — never building the tabs/carousel/accordion widget at all,
or simply not running an enhancement script at a given viewport and staying at the
pre-enhancement baseline — is a deliberate, standing design option, not a fallback of last
resort: "no enhancement can be better than 'enhancement'." Building any enhancement should
require a good, well-researched reason (and must not come with a significant performance cost for
everyone) rather than being justified merely by the fact that it's technically possible.
Trade-off: unenhanced content is simpler and lower-risk but less visually polished/interactive; an
enhanced widget can be more compelling but must be justified, not assumed.
Do: default to leaving flow content unenhanced unless there's a well-researched reason to augment
it; consider gating an enhancement behind a viewport/condition check and skipping it entirely
outside that condition; ship optional display features only when their performance cost is
minimal.
Ask: what is the well-researched reason this enhancement needs to exist, beyond "it's possible"?
(IC ch6, ch7, ch9)

### Preserve deep-linking to collapsed content via hash tracking `AXK-038`
Even after JS enhancement collapses sections behind a toggle, the component should still honor
conventional hash-fragment deep-linking: on load, if the URL hash matches a section heading's id,
that section must be programmatically opened and focus moved to its toggle button; thereafter,
each time the user opens a section, the URL hash should be updated (via history.pushState,
without a page reload) to reflect the now-open section, so users can copy/share a URL that
reopens the same content without needing developer tools.
Do: on load, open and focus the section matching the URL hash; update the URL hash (without
reload) each time the user opens a section.
(IC ch8)

### Evidence-based lazy-loading scope for multi-slide components `AXK-029`
Measured real-world usage data — not assumption — found that of carousels containing
linked/clickable slide content, only about 1% of users ever click any slide feature, and 89% of
those clicks land on the first slide; auto-rotating carousels show a similarly steep engagement
drop-off beyond the first slide. This licenses treating the first slide as primary content to load
eagerly, lazily loading subsequent slides' resources only as/if the user actually reaches them.
Do: load the first slide eagerly; lazily load subsequent slides as the user scrolls/advances to
them.
Trade-off: eager upfront loading is simpler but wasteful for rarely-viewed slides; lazy loading
saves bandwidth at the cost of added implementation complexity.
(IC ch9)

## Inclusive-Design Meta-Principles

### Five baseline properties of any inclusive component `AXK-030`
Any inclusive component should, in the broadest terms, be: clear and easy to use; interoperable
with different inputs and outputs; responsive and device-agnostic; performant; and under the
user's control. This is offered as a general evaluative checklist applicable to any interactive
component, not specific to any one widget.
Ask: which of the five baseline properties (clarity, interoperability, responsiveness,
performance, user control) is weakest for this component as currently designed?
(IC ch9)

### Inclusive design is broad decent reach, not an identical experience — and a method, not a recipe `AXK-031`
Inclusive design is not about giving everyone the same experience — it's about giving as many
people as possible a decent experience; a simpler implementation reaching more people through
multiple accessible interaction paths is preferable to a flashier one that doesn't, and
ultimately the content, not the interaction mechanism, is what should be compelling.
Correspondingly, worked component examples should be read as a demonstration of how to reason
inclusively about a component's actual purpose, content, and barriers — not as fixed, canonical
recipes to copy verbatim onto a different component.
Do: favor a simpler implementation with broader, multi-path accessibility over a flashier one
with narrower reach; re-derive the specific solution for a new component from its actual purpose
and content, rather than copying a prior worked example verbatim.
Ask: would a simpler version of this component reach meaningfully more people than the current,
more elaborate one?
(IC ch9, ch13)

### Windows High Contrast Mode / forced-colors component contract `AXK-032`
Components must remain usable under OS-level forced-colors/high-contrast themes, which actively
strip or override background colors and images: don't encode meaningful (non-decorative) content
as a CSS background-image, since it can be inverted or stripped entirely — use <img alt="...">
instead; give inline SVG icons fill/stroke: currentColor so their color tracks the surrounding
text color when the theme recolors it; for elements relying on background-color for their visible
shape (e.g. buttons), add a transparent border as a shape fallback that only becomes visible once
forced-colors mode supplies a border color.
Do: use <img alt> for meaningful images instead of background-image; use fill/stroke: currentColor
on inline SVG icons; add a transparent border to background-color-shaped elements as a
forced-colors fallback.
Ask: under Windows High Contrast Mode, does this component's meaning and shape both survive?
(IC ch6, ch8)

### Auto-moving content must be stoppable, but a pause button alone is not sufficient `AXK-033`
Any component that can move, animate, or cycle content automatically must let users pause, stop,
or hide that motion (WCAG 2.2.2). But retrofitting a pause button onto autoplaying motion is
judged insufficient on its own: it "takes control away, then hands it back later," and for users
with vestibular disorders who experience nausea from unwanted motion, the harm has typically
already occurred by the time they locate and press the control. The stronger design decision is a
component that never moves without the user's own initiating action in the first place.
Trade-off: autoplay-plus-pause (opt-out) is easier to build but riskier for affected users;
no-autoplay (opt-in-only) is safer but forgoes autoplay's presentational appeal — the source
explicitly favors the safer option while naming both.
Do: provide a pause/stop control for any automatic content cycling; design components that never
move without explicit user-initiated action, rather than relying on autoplay plus a pause control.
Ask: for a user with a vestibular disorder, has any harm already occurred before they could reach
this component's pause control?
(IC ch9)

### Icon-only controls and tooltip/toggletip disclosure are often unnecessary complexity `AXK-034`
Icons alone aren't a fully reliable communication channel — even a common icon can be misread (a
cross reading as "close" as much as "delete"), and there's no universally correct icon choice, so
pair icons with visible text where comprehension matters and validate with real users. In the
same spirit, most of the time a tooltip or toggletip isn't needed at all if clear textual labeling
and familiar iconography are provided from the start — it's often just a complex way of providing
information that could simply be part of the document's ordinary prose. Decide WHAT information
genuinely needs to be conveyed before deciding HOW to disclose it. When: space is genuinely at a
premium (e.g. a dense toolbar with many controls) is a legitimate last resort for a tooltip, not a
general substitute for labeling.
Do: pair icons with visible text where comprehension matters and layout allows; validate
icon-only controls with real user testing; default to clear visible labels and prose content over
building a tooltip or toggletip.
Ask: if we removed the tooltip/toggletip and just wrote a clear label or a sentence of prose
instead, would anything actually be lost?
(IC ch3, ch5)

### Content-length and media-fit tolerance is itself an inclusion concern `AXK-035`
A component must remain visually coherent across the real range of content lengths and image
aspect ratios that will actually occur, not just the placeholder content used while designing it
— an interface that breaks on unexpected content length effectively restricts what contributors
can say, which is a form of exclusion, not just visual polish. Forcing images to a consistent
aspect ratio (object-fit: cover) is a genuine trade-off between visual grid consistency and full
image fidelity, since a centered crop cuts off two or more edges by default; mitigate by curating
or positioning source images (object-position) so the focal subject survives the crop.
Do: design layouts that degrade gracefully across a real range of content lengths, not just
placeholder content; curate or position source images (object-position) so a center-based crop
doesn't cut off the subject.
Trade-off: consistent grid appearance (forced aspect ratio + crop) vs. uncropped image fidelity —
a real trade-off requiring curation, not something to resolve by picking a winner.
(IC ch13)

### Competing techniques for a custom modal's isolation contract, and why inert is favored `AXK-039`
A custom (non-native) modal dialog must satisfy two isolation requirements: everything outside it
must be invisible to assistive technology and unreachable by mouse and keyboard. Two manual
techniques each have real costs: applying aria-hidden to a wrapper around all outside content plus
a click-blocking overlay plus tabindex="-1" on every outside focusable element is fragile, because
elements already legitimately tabindex="-1" must be excluded so they aren't wrongly reactivated on
close; keeping the overlay but trapping Tab/Shift+Tab focus by intercepting keydown is also
flawed, because it blocks reaching browser chrome (e.g. the address bar) by Tab, unlike native
confirm(). Trade-off: manual overlay+tabindex means fragile element bookkeeping; a manual focus
trap blocks legitimate Tab access to browser chrome; the inert attribute encapsulates both
AT-invisibility and interaction-blocking in one native mechanism but (at time of writing) has a
broader native support gap, mitigated by polyfill.
Do: prefer the inert attribute (with polyfill) applied to all direct siblings outside the dialog.
(IC ch12)

### Stacked/nested overlays: ref-count shared side effects, never toggle them `AXK-046`
When dialogs nest (a Discard-Confirm opened above an editor dialog), any side effect they share —
background scroll-lock, inert on the page, a dimming overlay — must be reference-counted, not
toggled: closing the inner dialog must decrement, and the effect is released only when the count
reaches zero. A boolean toggle silently releases the background scroll (or reactivates the page)
while the outer dialog is still open — a defect invisible in single-dialog testing and common in
practice. Also restate the focus contract per layer: closing the inner dialog returns focus to
the control inside the outer dialog that opened it, not to the page.
Ask: if two overlays are ever open at once, which shared effects are counted vs. toggled? Where
does focus land when only the inner one closes?
(product-derived V2 — WAI-ARIA APG dialog pattern; absent from the V1 book corpus, added after a
baseline-arm catch in the V1 eval)

### role="alertdialog" for interruptions that demand a response; role="dialog" otherwise `AXK-047`
A confirmation that interrupts a task to demand an immediate response (discard changes? delete?)
is an alertdialog: assistive technologies treat it more urgently, and it must have an accessible
name and describedby pointing at the message. A dialog that hosts content or a form the user
works in at their own pace stays role="dialog". Using dialog for both flattens the urgency
distinction the roles exist to carry.
Ask: does this overlay interrupt with a question that must be answered before anything else — or
host work? (product-derived V2 — WAI-ARIA APG alertdialog pattern; absent from the V1 book corpus)

### Bound a custom dialog's content to the viewport `AXK-040`
A custom dialog's content container should be given a max-height with overflow-y: auto (and a
readable max-width, e.g. ~50 characters) so the dialog can never grow larger than the viewport and
become obscured or unreachable, even though dialog text is normally expected to be concise.
Do: cap dialog content height with overflow-y: auto; cap message line length for readability.
(IC ch12)
