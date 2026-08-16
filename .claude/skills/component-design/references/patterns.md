# Component Pattern Catalog

This file is the concrete UI pattern catalog for the component-design skill: a named
vocabulary of established component shapes to reach for once a component's *role* is already
decided, organized by functional family so the right neighborhood is fast to find. Route here
whenever a navigation, layout, list, action-exposure, data-display, form/control, overlay,
feedback, or mobile-touch component needs a concrete shape — not when the underlying role
itself is still undecided (that decision belongs to boundaries.md). Each family opens with its
selection framework, when one exists, before the catalog entries; every entry states when the
pattern applies, when to avoid it, and keeps its trade-offs two-sided rather than prescribing a
winner.

## Contents

- Meta-Principle
- Navigation
- Layout & Panels
- Lists
- Actions & Commands
- Data Display
- Forms & Controls
- Overlays
- Feedback
- Mobile & Touch

## Meta-Principle

### Familiar Patterns Reduce Learning Cost `PTN-125`
Design patterns work well because they are already established and familiar — they leverage
users' existing mental models for low-effort understanding. Introducing a wholly new pattern
imposes a real learning cost; product differentiation should come from how established
patterns are executed and connected to serve the product's purpose, not from inventing novel
patterns for their own sake. Do: check whether this problem already has a familiar,
well-understood pattern before inventing one. Exception: a genuinely new problem, where no
established pattern fits, can justify a new one despite the learning cost. Ask: does this
problem already have a familiar pattern that solves it? Is the proposed novelty serving the
product's purpose, or just differentiating for its own sake? (DS ch1)

## Navigation

### Signpost Contract `PTN-001`
Any recurring navigational component (titles, tabs, breadcrumbs, scrollbars, sequence
indicators) must show where the user currently is, not just where they can go. Do: highlight
or mark the current selection/position in tabs, menus, breadcrumbs, and sequence indicators.
Ask: if a user lands here mid-task, can they tell where they are without backtracking? (DI ch3)

### Navigation Has a Real Cost `PTN-002`
Every jump (page, dialog, window) costs real user time, attention, and re-orientation; a flow
needing multiple jumps for the common case is spending that cost needlessly. Trade-off:
consolidating on one page raises density/complexity, splitting into steps lowers per-step
complexity but adds jump cost. Ask: is a sub-page/extra dialog being introduced for a case
that's actually rare? (DI ch3)

### Separate the Navigation Model from Its Widget `PTN-003`
A navigation model (global nav, modal, related-content nav) is a behavioral contract, not a
fixed widget — tabs, a dropdown, or a sidebar tree can all implement "global navigation." Do:
decide what the navigation must do before choosing which component renders it. (DI ch3)

### Full Navigation Distracts Mid-Task `PTN-004`
Rich navigation helps open exploration but is a mistake inside a focused, immersive task (e.g.
a slideshow) — offer only back/next plus an escape hatch there. When: avoid restricting nav
when the user is meant to explore freely. Trade-off: navigational richness vs. focus/reduced
distraction. (DI ch3)

### Pan-and-Zoom Viewer `PTN-005`
For content that is one continuous space (maps, large images, dense documents, timelines)
rather than discrete pages, model it as a pannable/zoomable viewport, not a set of navigable
pages. Do: provide pan controls, zoom in/out, and a reset-to-origin control. (DI ch3)

### Flat Navigation / Canvas-and-Palette Shell `PTN-006`
For canvas-and-palette tool apps (e.g. an image editor), page-hierarchy navigation is largely
unnecessary — tools stay reachable via menus/toolbars/palettes, and interruptions route
through Modal Panel or Stepwise rather than page navigation. When: avoid when the product's
primary structure is content pages the user moves between. Trade-off: having all tools
available at once maximizes power but increases the difficulty of finding one specific tool.
(DI ch3)

### Clear Entry Points `PTN-007`
Show a small number of clearly-labeled, task-matched entry points at arrival instead of the
full nav/toolset; any repeat-shown onboarding variant needs a persistent "don't show again"
control. Trade-off: clarity for new users vs. unwanted friction for repeat/expert users. Ask:
do visitors already know what this app is and why they came? If yes, this pattern is
unnecessary. (DI ch3)

### Menu Page `PTN-008`
A page whose entire content is a list of links to content-rich destinations, each carrying
enough label/description for confident choice, with nothing else competing for attention.
When: the page's job is pure routing; avoid when the page instead needs to "hook" the user or
explain a value proposition. Trade-off: richer per-link description/thumbnail improves
confidence but costs space and links-per-screen. (DI ch3)

### Pyramid `PTN-009`
Connect a sequence of item pages with back/next links AND a parent index that links directly
to every item, so the set supports both linear browsing and random-access jumping; the last
item should link back to the parent/index rather than loop to the first, when order matters.
Exception: looping may be acceptable when order genuinely doesn't matter. (DI ch3)

### Bookmarks / Deep-Linked State `PTN-011`
Make a component's reachable states — not just top-level pages — addressable via
permalink/deep link, encoding content position plus meaningful supplementary state (filters,
zoom, display mode), but excluding personal settings a recipient wouldn't want silently
applied. Ask: if the user bookmarks or shares the current URL, does it reproduce what they're
looking at? (DI ch3)

### Escape Hatch `PTN-012`
Provide a clearly-labeled link back to a familiar location whenever a user might land with no
context to recover from (deep link, error, dead end); a clickable logo at top-left linking home
is the established convention, including on restricted pages like login. Ask: if a user lands
here with zero prior context, is there a labeled way back? (DI ch3)

### Fat Menus `PTN-013`
A hover/click-triggered dropdown exposing a large, well-organized slice of site structure from
any page. Hard contract: the open/hover mechanism must stay fully usable via keyboard and
screen reader — if it can't, fall back to Sitemap Footer instead. When: avoid when the link
count overflows the viewport, or accessibility can't be guaranteed. Trade-off: one-gesture
access to nearly the whole site vs. implementation/accessibility complexity. (DI ch3)

### Sitemap Footer `PTN-014`
A footer sitemap — main sections, key subpages, utility/legal links — as a lightweight,
mostly-static, more-accessible fallback to Fat Menus. Trade-off: Fat Menus give dynamic
one-gesture access with higher accessibility risk; Sitemap Footer is simpler and more
accessible but only found by bottom-scrolling users. (DI ch3)

### Sign-in Tools `PTN-015`
Group account-related utility nav (logout, profile, help, cart, notifications) into one
consistently top-right-positioned cluster users already expect there; collapse into a dropdown
when long, reuse the same space for the login form when logged out. Do: keep this area
visually unobtrusive; always include a visible logout control. Trade-off: a dropdown collapses
clutter but adds a step; a flat list is scannable but costs width. (DI ch3)

### Sequence Map `PTN-016`
On each page of a linear flow (reading, wizard, process), show a compact map of every step
with the current one marked and visited steps clickable. When: fits primarily linear,
one-directional content; avoid for large/hierarchical structures (favor Breadcrumbs) or very
many steps whose order isn't critical. (DI ch3)

### Breadcrumbs `PTN-017`
Show a linked trail from the top page through every intermediate parent to the current page,
built from the page's fixed hierarchy position — never from click history, since most entry
points (search, filters, deep links) don't drill straight down. Ask: is the trail computed
from hierarchy position, or from click history? (DI ch3)

### Annotated Scrollbar `PTN-018`
Give a scrollbar a second role as a content map / "you are here" indicator via static or
dynamic annotations on or beside the track, chosen from the content's own structure (headings,
row numbers, search hits). Trade-off: rich track markers turn the scrollbar into a powerful 1D
overview-plus-detail UI, but are less familiar to some users than a plain scrollbar. (DI ch3)

### Animated Transition `PTN-019`
Animate a state change (zoom, pan, reflow, collapse/expand) instead of switching
instantaneously, to preserve spatial continuity — animate only the affected region, start
immediately, keep it short; when the same action repeats rapidly, collapse the repeats into
one animated transition instead of replaying per repetition. Trade-off: well-tuned animation
aids orientation and feels polished; poorly-tuned (slow, laggy, over-applied) actively degrades
responsiveness. (DI ch3)

## Layout & Panels

### Choosing Among Module Tabs, Accordion, and Collapsible Panels `PTN-028`
These three patterns all hide/group content modules but differ on two axes: whether one module
shows at a time (Tabs) or several can be open (Accordion, Collapsible Panels), and whether
grouping implies the modules are related (Tabs, Accordion) or meant to stay independent
(Collapsible Panels). Do: use Tabs when exactly one related module should show; Accordion when
several related modules can be open and order matters; Collapsible Panels when modules are
independent, optional, supplementary. Trade-off: exclusivity (Tabs) simplifies most
aggressively but can't show multiple modules together; multi-open flexibility can grow the
page long. Ask: does the user need one module visible or possibly several? Are these modules
related, or independent supplements? (DI ch4)

### Visual Containment `PTN-020`
Enclosing related items inside a shared visual boundary (box, background block, tab module,
accordion, indentation) communicates a parent-child/ownership relationship, not mere
proximity. Ask: does this grouping need to communicate ownership, or only "these are related"
(which proximity alone expresses)? (DI ch4)

### Visual Framework `PTN-021`
Define and reuse one consistent layout, palette, font set, and tone across every page, with
style centralized separately from content so framework-wide changes don't require touching
every page. Exception: a homepage/main window is commonly allowed to be visually distinct
while still sharing some framework traits. (DI ch4)

### Center Stage `PTN-022`
Size the page's single most important content or task as the largest sub-section (commonly at
least ~2x surrounding elements) so it anchors the eye first. When: avoid when the page
genuinely presents multiple items of equal importance — use Grid of Equals instead. (DI ch4)

### Grid of Equals `PTN-023`
Arrange items of roughly equal importance into a grid where each follows the same template and
gets equal visual weight (a 1-column list is the degenerate case, not a separate pattern);
emphasize an item via color/style only, never by changing its position or size. Ask: does this
emphasis treatment change position or size relative to neighbors? (it must not) (DI ch4)

### Titled Sections `PTN-024`
Give each content section a short, distinct, memorable title, separated by whitespace or
contrast. If a section resists a clear title, that signals the grouping itself is wrong —
regroup rather than force a vague title; a recurring "Other/Misc" category is a particular
warning sign. Exception: an "Other" category is sometimes genuinely necessary. (DI ch4)

### Module Tabs `PTN-025`
House several content modules in a small tab area where only one is visible at a time; fits a
small (<~10, ideally ~5), fairly static set. The selected tab must read as visually continuous
with its panel, not just a color change; avoid making an overflowing tab row
scrollable/carousel-like — that forfeits the pattern's see-everything value. When: avoid when
users often want more than one module visible (favor Accordion) or the set grows unbounded.
(DI ch4)

### Accordion `PTN-026`
House several content modules as independently openable panels in fixed order; default to
allowing multiple open at once rather than auto-closing others, which disorients users about
where content went. Persist open/closed state across sessions for logged-in, tool-palette-style
accordions; avoid nesting an accordion inside another accordion's module. Trade-off:
single-open keeps the page shorter but risks disorienting disappearance; multi-open avoids that
but can grow the page long. (DI ch4)

### Collapsible Panels `PTN-027`
House optional, supplementary content — not meant to read as related to each other, unlike
Tabs/Accordion — in independently openable panels; provide a visible on-screen affordance to
reopen, not only a keyboard shortcut, and default a routinely-reopened panel to open once usage
data supports it. Exception: keyboard-shortcut-only reopen may be acceptable in an expert
application. (DI ch4)

### Movable Panels `PTN-029`
Let users drag content modules to reposition them in a dashboard/portal, showing a
ghost/dashed-outline preview of the landing slot during drag; persist position and open/closed
state across sessions, with a discoverable "reset to default." When: avoid when module
positions are deliberately meaningful to the designer's hierarchy — use static Titled Sections
instead. Trade-off: free-drag layout maximizes freedom but risks disorder; a drop-slot grid
constrains placement but stays orderly. (DI ch4)

### Right/Left Alignment for Label-Control Pairs `PTN-030`
In a two-column label-then-control layout, right-align labels close to their controls and
left-align the controls along a shared vertical line. Exception: long labels read better
left-aligned; labels varying widely in length across locales are often better placed above
their controls instead. Trade-off: right-aligned labels maximize proximity but produce a
ragged left edge; left-aligned labels read more easily but weaken label-control grouping.
(DI ch4)

### Diagonal Balance `PTN-031`
When a page/dialog fits one screen without scrolling, place strong elements (title, tabs)
upper-left and action controls (OK/Cancel, Submit) lower-right, so the asymmetric layout still
balances and matches the natural left-to-right reading flow. Exception: platforms/conventions
that habitually center titles and controls (e.g. classic Mac OS X) make this less applicable.
(DI ch4)

### Responsive Disclosure / Enabling / Disabling `PTN-032`
Three ways to guide a step-by-step flow on one page: Disclosure shows only the current step,
revealing the next once complete; Enabling starts with most UI visible-but-disabled, enabling
controls as steps complete; Disabling starts with a full option set and dynamically disables
options invalidated by input so far. Never disable a control without a genuine reason, and
surface an explanation when it isn't obvious from proximity. Trade-off: Disclosure avoids a
sparse wizard feel but can grow long; Enabling previews what's coming at the cost of a busier
start. (DI ch4)

### Liquid Layout `PTN-033`
Resize content to fill a resized window/dialog/page rather than leaving unused space or
forcing scrolling, while text/controls stay usable at every size; even so, cap wrapped
paragraph text at roughly 10-12 words per line regardless of container width. Trade-off:
adapts to more contexts but costs more design/engineering care than a fixed layout; a capped
line length improves reading speed but can leave visible unused width. (DI ch4)

## Lists

### List Selection Framework `PTN-034`
Before choosing a list layout, identify the dominant use case (overview at a glance,
one-at-a-time browsing, searching for a specific item, sorting/filtering, or
rearranging/adding/removing) and scope against non-visual data properties (length/boundedness,
ordering, grouping, item richness, interaction model) — there is no single correct list
pattern, and the same underlying question ("where to show item detail after selection") has at
least three valid answers (Two-Panel Selector, List Inlay, One-Window Drilldown). Do: let the
dominant use case drive the design; work the checklist before picking a visual pattern; don't
default to one pattern regardless of screen size. Trade-off: compact patterns (Carousel,
One-Window Drilldown) trade away the easy comparison spacious patterns (Two-Panel Selector,
List Inlay) provide. Ask: which use case is actually dominant, and does the chosen pattern's
affordances match it? (DI ch5)

### Two-Panel Selector `PTN-035`
A list panel sits beside a detail panel showing the selected item's full content; both stay
visible, and selecting a different item swaps only the detail side. When: needs enough space
for two panels at once; avoid on very small screens (use One-Window Drilldown) or when detail
is small enough to fit inline (List Inlay). Trade-off: costs significantly more space than the
alternatives in exchange for eliminating list/detail "hopping." (DI ch5)

### One-Window Drilldown `PTN-036`
Selecting a list item replaces the whole view with its detail, reusing the window for
whichever navigation level is current, with an explicit way back; add lightweight
previous/next links in the detail view to reduce repeated hopping. When: the only viable
option in extremely space-constrained contexts; avoid when users need to compare more than one
item's detail in quick succession. (DI ch5)

### List Inlay `PTN-037`
Selecting a list item expands its detail inline beneath/within that item, pushing later items
down; each item's open state is independent so several can expand at once. This is the same
expand-in-place behavior as Accordion applied to list items — reuse an existing accordion
primitive rather than building a separate component. When: avoid when space is too limited
even for one panel, or the list is a 2D grid rather than a single column. (DI ch5; DI ch4)

### Thumbnail Grid `PTN-038`
A 2D grid of near-uniformly-sized image thumbnails with minimal metadata beside (not over)
each; force-crop to uniform size only when size/aspect ratio doesn't itself carry meaningful
information. Exception: personal media collections where dimensional variance is meaningful
data. Trade-off: uniform cropping improves scannability but discards size/aspect information
that can matter. (DI ch5)

### Carousel `PTN-039`
A single scrollable/swipeable row of thumbnails, sometimes enlarging the focused item; compact
vertically but restricts users to sequential browsing rather than search/direct access. Best
for a moderate item count and flat, uncategorized lists. When: avoid when the list is large or
users need to search a specific item; avoid categorizing items inside a single Carousel.
Trade-off: compactness and visual appeal vs. discoverability/searchability. (DI ch5)

### Row Striping `PTN-040`
Alternate two similar, low-contrast row background colors in a wide multi-column table so
users can track a row left to right without losing their place; measured benefit appears
mainly for large, sparse tables — small/dense tables show only subjective preference. Ask: is
this table large and sparse, or small and dense? (DI ch5)

### Pagination `PTN-041`
Split a very long list into discrete pages with first/previous/next/last controls; put the
highest-value items on page 1, never render the current page as a clickable link, and truncate
long page-number sequences with an ellipsis while keeping neighbors and the last page
reachable. Trade-off: simple and web-conventional at the cost of an explicit page-boundary
interruption Infinite List avoids. (DI ch5)

### Jump to Item / Incremental Search `PTN-042`
In a sorted list/table/tree/dropdown, typing characters jumps to and selects the first item
whose leading text matches, auto-scrolling into view; an escalated incremental-search variant
re-filters and highlights every match live on each keystroke. Trade-off: incremental search
gives richer contextual feedback than a modal search dialog but needs a live scan/highlight
mechanism. (DI ch5)

### Alphabet Scroller `PTN-043`
Place alphabet letters along a scrollable list/table/tree's scrollbar as a direct index to jump
to a section — the same mechanism as Annotated Scrollbar specialized for alphabetic content,
most valuable on touch-only devices where Jump to Item's typing isn't available.
(DI ch5; DI ch3)

### Cascading Lists `PTN-044`
Represent a hierarchy as side-by-side single-select list columns, where selecting an item
populates the next column with its children; provide explicit affordances for deleting or
moving items between levels, since plain lists don't give this for free. Trade-off: uses
considerably more horizontal space than a tree view in exchange for showing more breadth and
clearer per-level orientation. (DI ch5)

### Tree Table `PTN-045`
Combine a tree/outline (hierarchy via indentation, leftmost column) with a table (attribute
columns) in one view; if columns become sortable, provide an explicit way to re-sort back to
hierarchy order. Trade-off: more visual/implementation complexity than either alone, in
exchange for not forcing a choice between hierarchy and attribute comparison. (DI ch5)

### New-Item Row `PTN-046`
Place a dedicated empty row at the start or end of a list/table letting users create an item in
place at its final position, rather than in a separate creation UI; treat it as valid
immediately and preserve partial edits if the user navigates away rather than silently
discarding them. (DI ch5)

### Card `PTN-120`
For a clickable card (Grid of Equals / Thumbnail Grid style), put the real link only around the
title text — never wrap the whole card — so it gets a unique accessible name; expand that one
link's hit area to cover the whole visual card rather than adding a second link. Style any
"read more" CTA as decorative, non-link, reacting to the title link's focus state via CSS —
otherwise an aggregated links list fills with identical, meaningless "read more" entries. Ask:
would making the CTA text the actual link name produce many identical, unhelpful entries in an
aggregated links list? (IC ch13)

## Actions & Commands

### Choosing Where to Expose a Set of Actions `PTN-061`
Action-exposure patterns form a spectrum trading exhaustiveness, visibility, and space: Menu
Bar (everything, always available, accessible fallback) → Popup/Context Menu (situational
subset, on demand) → Toolbar/Button Groups (small persistent, visually-grouped, scoped set) →
Hover Tools (per-item, hidden until needed, mouse-only) → Action Panels (persistently visible,
richly laid out, most space-hungry but most flexible). Do: match the pattern to the action
set's size/scope/required visibility rather than designer familiarity; verify
keyboard/screen-reader access survives the chosen mechanism. Trade-off: exhaustive
always-visible exposure costs space or an extra step; situational lightweight exposure saves
space but sacrifices discoverability or touch compatibility. Ask: would an unfamiliar user
find this action through the chosen mechanism? Does it still work for keyboard-only and
touch-only users? (DI ch6)

### Action Component Design Goal `PTN-047`
For any interface "verb" component (button, menu item, command), the goal is fourfold: the
correct action for the task, a clear label, discoverability, and support for chaining with
related actions. Ask: is this the correct action, not just a plausible one? Is it discoverable?
Can it be chained with related actions? (DI ch6)

### Drag-and-Drop `PTN-048`
Drag-and-drop leans on physical-world intuition, not learned software convention, so a drop
target's behavior must resolve unambiguously to exactly one of two meanings: relocate the
item, or apply the target's own function to it — never something else. Ask: when dropped here,
does this relocate/reparent the item, or invoke this target's function using it as input?
(DI ch6)

### Menu Bar `PTN-049`
A persistent horizontal menu bar (File/Edit/View-style) is the conventional place to expose an
application's complete action set, organized by category, and a guaranteed-discoverable
accessible fallback for screen readers and keyboard access keys. Exception: a trend toward
hiding the menu bar by default in favor of toolbars/ribbons/panels, available on demand.
(DI ch6)

### Popup/Context Menu `PTN-050`
Invoked by right-click or equivalent on a target, list only the actions relevant to that
target — not the full application catalog — and keep the list short. (DI ch6)

### Don't Repurpose a Dropdown-Select for Actions `PTN-051`
A dropdown/select is conventionally understood as choosing a value, not invoking an action;
reusing it to "select an action to run" breaks that contract. (See Form: Dropdown Chooser for
the legitimate value-selection role.) (DI ch6)

### Toolbar `PTN-052`
A compact row of usually-icon action buttons; works best when each action has a clear,
self-explanatory icon — an action that genuinely needs words should use a labeled control
instead of being forced into ambiguous icon form. (DI ch6)

### Link as a Lightweight Action Trigger `PTN-053`
Distinctively-colored, underlined-on-hover text is a well-established convention for a
low-emphasis action, avoiding a button's visual weight. Trade-off: because users learn colored/
underlined text means "clickable," that styling must then be avoided for any non-clickable
text elsewhere. (DI ch6)

### Double-Click Resolves to One Learned Meaning `PTN-054`
Double-click conventionally means "open this item" or "perform its default action" — not an
opportunity to invent a third meaning; on an object it commonly opens a property
sheet/editor, on text it commonly enters inline edit mode. Ask: does this object type have an
established open/default-action meaning elsewhere that double-click should match? (DI ch6)

### Keyboard Access Is a Required Path `PTN-055`
Every action reachable via pointer must also be reachable via keyboard (standard shortcuts,
menu access keys), following platform convention rather than inventing new ones — for users
who can't use a mouse, the keyboard path can be their only way to invoke the action at all.
Ask: can this action be invoked without a mouse, via a standard shortcut or access key? (DI ch6)

### Typed Commands (CLI) `PTN-056`
A command-line style interface offers free-form access to a system's entire action set with
high per-composition power, but is structurally poor at discovery — most CLIs don't make
available commands easy to find on their own. When: fits an efficiency layer for expert users
willing to learn a vocabulary; avoid as the primary interaction for casual/first-time users.
Trade-off: composability and power vs. near-zero discoverability without prior learning.
(DI ch6)

### Custom Controls Must Visually Afford Their Behavior `PTN-057`
Specialized/expert-facing apps have more freedom for non-standard controls, but every custom
control must still visually communicate that it's actionable and how (raised/3D look, borders,
cursor change, tooltip) or users won't discover it's interactive. Ask: does this element
visually signal, on its own, that it can be clicked/dragged/adjusted? (DI ch6)

### Button Groups `PTN-058`
Cluster related, same-scope actions into a small group of visually-unified buttons (same
border/size/icon style/hover), split into groups of ~2-5 rather than one long row; never mix
actions with different scopes/targets into one group. Exception: a single "primary" action may
deliberately break from shared styling to stand out (see Prominent "Done" Button). (DI ch6)

### Hover Tools `PTN-059`
Reveal per-item action controls only on pointer hover, hiding instantly on pointer leave with
no animated transition; currently poorly suited to touch, which has no free
hover-before-commit state. When: avoid as the sole action-access path when the primary input is
touch/touchpad. Exception: a persistent lightweight cue (grayed-out controls highlighted on
hover) is a middle-ground alternative when actions must stay discoverable without hover.
(DI ch6)

### Action Panels `PTN-060`
A persistently-visible, richly-laid-out panel of grouped actions for the current
item/selection, instead of hiding them behind a menu, popup, or hover reveal; lay out each
action strictly one-per-line for correct screen-reader readability. When: fits when the action
set is too large for Hover Tools or a short menu; avoid when screen space is very limited.
Trade-off: uses more space than a menu bar or hover-reveal in exchange for permanent visibility
and full layout freedom. (DI ch6)

### Label Form and Length `PTN-062`
An action's label may be text, icon, or both, chosen for what best communicates it, kept
consistent within a container; roomier containers can support longer, more descriptive labels
helping infrequent users, while dense/expert interfaces suit terser labels. Trade-off: longer
labels aid learnability/recall but add visual noise and space cost experienced users may not
need. (DI ch6)

### Prominent "Done" Button `PTN-063`
A large, clearly-labeled, visually-standout button at a task flow's endpoint so the user is
confident their action registered; prefer a task-specific verb ("Send," "Purchase") over
generic "Done" when it communicates the outcome more precisely, placed directly after the
flow's last field. Ask: would a task-specific verb communicate the outcome more precisely than
a generic "Done"? (DI ch6)

### Smart Menu Items `PTN-064`
Dynamically rewrite an action trigger's label to state precisely what will happen ("Close
[document name]," "Undo Delete Message"), generalizing to any UI verb element, not just menu
items; disable the action entirely when there's no valid target. Exception: for multi-object
selections, a generic plural-safe label is an accepted simplification over attempting per-item
precision. (DI ch6)

### Preview Before Committing `PTN-065`
Before a heavyweight or hard-to-predict action, show a preview/summary of the result, from
which the user can proceed, revise a prior step, or cancel without leaving the preview screen.
(DI ch6)

### Progress Indicator Paired with Cancelability `PTN-066`
For any operation expected to block the UI for ~2+ seconds or that runs in the background, show
progress (what's happening, fraction done, remaining time, how to cancel), with cancel placed
directly beside the indicator and taking effect instantly; first consider whether the operation
can simply be made fast enough that cancelability becomes less urgent. Ask: is the time
estimate accurate enough for a determinate progress bar, or should it be indeterminate? When
multiple parallel operations run, does one cancel control cancel everything, or does each need
its own? (DI ch6)

### Multi-Level Undo `PTN-067`
Let users reverse a sequence of past actions one at a time in reverse chronological order (and
redo forward) across a whole session — undo/redo the underlying transaction, not just its
visual reflection; exclude transient/cosmetic state (selection, scroll position) from the
stack, and exclude actions with real-world side effects (purchases, sent messages). Trade-off:
skipping this remains viable for repeated-task workflows — the user just re-executes manual
steps, costing time rather than engineering. (DI ch6)

### Command History `PTN-068`
Keep a visible, chronological record of executed actions — what, to what, when — independent
of whether they're individually undoable, so users can review, relocate, or re-invoke them;
summarize a bulk action on many objects as one history entry, and treat the display as
secondary/optional UI. (DI ch6)

### Macros `PTN-069`
Let users bundle a recorded/defined action sequence into one named, replayable higher-level
action, triggerable by command/button/drag-and-drop; support macros calling other macros,
persist them, and let behavior vary parametrically per invocation. Trade-off: a full scripting
language is extremely powerful but is a genuine security risk and can intimidate
non-programmer users, even though composing a macro is functionally programming. (DI ch6)

### Offload Sub-Tasks the System Handles Better `PTN-122`
Fast calculation, doing multiple things simultaneously, perfectly reliable recall, complex
pattern detection, and searching a large dataset are inherently cheaper for software than for
users — delegate a sub-task of this kind to the system rather than asking the user to perform
it manually. Ask: is this sub-task calculation, parallel tracking, exact recall, pattern
detection, or search over a large set — something the system is inherently better at? (MI ch3)

## Data Display

### Choose a Complex-Data Display by Organizational Model `PTN-070`
Before picking a component for a dataset, identify its actual organizational model — linear,
tabular, hierarchical, network/interconnected, geographic/spatial, text-based, or other — since
this determines which family of components legitimately fits; don't default to a familiar
table/list without checking whether the data's real shape needs a hierarchical, network, or
geographic component. Ask: how is this data actually organized, and does the chosen display
shape suggest false relationships or hide real ones? (DI ch7)

### Two Information-Seeking Needs `PTN-071`
For any complex-data display, determine whether the dominant need is "zeroing in" on a
specific, partially-known target (search/filter plus jump-and-recenter) or "getting the big
picture" (overview-first zoom plus cross-view comparison); after a search/selection recenters
the viewport, the target must land visibly in the display, not merely be flagged as existing
off-screen. Ask: does this component need Zero-In/search-and-jump, overview-plus-compare, or
both? (DI ch7)

### Item Disclosure vs. Drill-Down `PTN-072`
Revealing more detail about a point of interest works one of two structurally different ways:
Item Disclosure opens/closes detail in place without leaving the current view (same behavior as
List Inlay/Cascading Lists), while Drill-Down navigates to a dedicated view (same behavior as
One-Window Drilldown) — choose deliberately based on whether the current view/context needs
preserving. Ask: does revealing detail need to preserve context (favor Item Disclosure), or
does it warrant a dedicated view (favor Drill-Down)? (DI ch7)

### Overview Plus Detail `PTN-073`
A persistent small overview of a whole large dataset beside a zoomed detail view, with a
draggable viewport rectangle in the overview determining what the detail view shows,
synchronized both directions within ~0.1s latency (the threshold for a direct-manipulation
feel). (DI ch7)

### Datatips `PTN-074`
Hovering/tapping a point in a data graphic shows its underlying value(s) in a small floating
tooltip at the pointer, without permanently cluttering the display. When: avoid as the sole
mechanism when users need to compare many points simultaneously, or on touch-primary
interfaces lacking true hover — shares this limitation with Hover Tools. Exception: a
persistent, always-visible data panel is an alternative that never obscures content but
requires shifting attention from pointer to panel. (DI ch7)

### Data Spotlight `PTN-075`
Hovering an area of interest highlights the related "slice" of data throughout the graphic
while dimming the rest, instead of or alongside a numeric Datatip; keep the highlight/dim
transition fast and smooth. When: avoid (favor Datatips alone) when a hovered point is just a
single, simple value with no larger related slice. (DI ch7)

### Sort/Rearrange Changes What Insight a Display Reveals `PTN-076`
Letting users resort a complex-data component by a different criterion reveals patterns
invisible in the default order — expose per-column click-to-sort for tables, reorderable child
nodes for trees, and a chosen baseline variable for stacked charts. Ask: what ordering criteria
would actually matter to this component's users, beyond the default? (DI ch7)

### Search/Filter Behavioral Contract `PTN-077`
A well-designed search/filter/query affordance on a complex-data display should be interactive
(fast response), iterative (refine repeatedly, combine search with filtering),
context-preserving (show results within surrounding data), and compound-condition-capable
(combined criteria, not just single-attribute). Ask: is the user narrowing by
category/attribute, or composing more elaborate multi-condition queries? (DI ch7)

### Dynamic Queries `PTN-078`
Map standard controls (sliders, checkboxes, radio/dropdown, text fields) one-to-one to a
dataset's attributes so users can instantly and interactively filter a large multivariate
dataset, updating as each control is adjusted. When: the fallback for filtering when the user
can't select a point of interest directly within the data display itself — contrast with Data
Brushing. Trade-off: trades full query-language expressiveness for learnability and immediacy.
(DI ch7)

### Data Brushing `PTN-079`
Selecting ("brushing") a subset of data points in one view highlights that same subset
simultaneously across every other linked view of the same dataset, with a shared consistent
visual treatment and high-speed response in every view. (DI ch7)

### Local Zooming `PTN-080`
Shrink a dense dataset to fit one screen, then distort the display around the pointer so the
area near it enlarges for readability while the rest stays compressed, keeping context and
detail simultaneously; match the distortion mechanism to the graphic type. When: avoid when
users won't learn a demanding fisheye interaction, or the encoding depends on a preserved
aspect ratio (e.g. a map must scale both axes together). (DI ch7)

### Sortable Table `PTN-081`
Click a column header to re-sort the whole table by that column, toggling
ascending/descending; give headers a clickable affordance, indicate sort direction on the
last-sorted column, and use a stable sort so a secondary sort preserves prior ordering.
Exception: this convention is well-known enough that users may assume it exists even if a
given table doesn't implement it. (DI ch7; IC ch11)

### Radial Table `PTN-082`
Arrange items in a circle using arcs/curved lines through the interior to show pairwise
relationships; place aggregate/large-scale properties outside and fine-grained connections
inside, reducing excess lines and letting users filter/highlight via Data Spotlight or Dynamic
Queries. Trade-off: rewards patient/expert users at the cost of being unclear to casual or
first-time users. Ask: does a circular arrangement actually clarify this dataset's patterns, or
would another visualization work better? (DI ch7)

### Multi-Y Graph `PTN-083`
Overlay/stack multiple series sharing one X-axis, but give each its own separately-scaled,
clearly labeled Y-axis when the series have very different units/magnitudes — never overlay
curves with very different ranges on one shared Y-axis. Ask: do these datasets actually share a
comparable value range, or would overlaying them create a false apples-to-apples impression?
(DI ch7)

### Small Multiples `PTN-084`
Tile many small, strictly consistent-size/shape/scale mini-visualizations sharing common data
dimensions across one or two additional tiling dimensions, using binning/shingling (roughly 100
tiles as a rough ceiling) when a tiling dimension has too many distinct values. When: avoid
when individual images would be too small to read (e.g. mobile). Exception: for a genuinely
continuous/temporal dimension, an animated movie or step-through frames can substitute for
tiling. (DI ch7)

### Treemap `PTN-085`
Represent multidimensional/hierarchical data as nested rectangles — area encodes a numeric
attribute, nesting encodes hierarchy, color/labels encode further attributes — packing a dense
diagram into one space-efficient view; pair with Datatips and Dynamic Queries for
drill-down/filtering. When: avoid as a static, non-interactive artifact, and be cautious with
users unmotivated to learn an unfamiliar style. (DI ch7)

### Simplify or Fall Back for Unfamiliar Visualizations `PTN-086`
Unfamiliar, information-dense techniques (Radial Table, Treemap) reward patient power users but
poorly fit casual/first-time users; if real users repeatedly fail to understand a technique
without extra explanation, simplify it or fall back to something more familiar rather than
assuming visual appeal earns its value for free. Ask: are real users actually understanding
this visualization, or skipping past it without engaging? (DI ch7)

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

## Overlays

### Modal Panel `PTN-010`
Display a single focused panel and withhold other navigation until the user resolves the
immediate task; reserve for cases the app genuinely cannot proceed without (filename, login,
critical acknowledgment) — route low-importance input to an inline, non-blocking control
instead. On close, return the user to exactly the page/state they were on before, and on the
web prefer a lightweight custom overlay over an OS-level modal dialog. Exception:
sign-in/registration screens are sometimes presented as a whole stripped-down "modal" page
rather than a small overlay. Trade-off: a blocking modal guarantees input is captured
immediately; an inline non-blocking control risks the input being forgotten. Ask: does the app
genuinely need to block everything until this is resolved, or could the request be
deferred/hung inline instead? (DI ch3; IC ch12)

### Confirmation Dialog `PTN-112`
Gate an action behind a confirmation dialog only where its consequence is not easily reversible
or is high-stakes; where a mistake is cheap and quickly recoverable, skip confirmation and let
users learn by trial and error. Trade-off: confirmation adds friction to every legitimate use
in exchange for safety on the rare mistaken case. Ask: how costly is it, in time or
consequence, for a user to recover from performing this action by mistake? (IC ch3)

### True ARIA Menu Button Contract `PTN-115`
Pair a trigger button carrying a static `aria-haspopup="true"` (a fixed capability warning,
never toggled) with a dynamically toggled `aria-expanded="true"/"false"` reporting the menu's
actual open/closed state, plus a menu container with menu/menuitem roles; hide a decorative
disclosure-triangle glyph from assistive technology since `aria-haspopup` already communicates
a popup exists. (IC ch4; DI ch8; DI ch6)

### Toggletip `PTN-116`
A click-triggered info bubble whose content is announced only after activation, via an
initially-empty live region populated on click; the trigger is not a real toggle button —
clicking again does not hide it, and the live region is cleared and repopulated after a short
delay to force re-announcement, since a "toggled-on" state makes little sense once content has
already been read. (IC ch5)

## Feedback

### Live Region `PTN-117`
A container that announces added/changed content via screen reader without requiring
interaction or a focus move — pair `role="status"` with `aria-live="polite"` on the container
for widest compatibility; use it to deliver any state-change/FYI message that should be
announced but not focused. (IC ch10)

### Flash Messages `PTN-118`
Colored text strips above a page's primary action area, purely informational/non-actionable,
are adequately served by a single shared live region — they don't need the
dialog-with-focus-moved treatment reserved for actionable messages. (IC ch10)

### Prefer Automatic, Timed Disappearance `PTN-119`
Let a transient notification disappear by itself after a suitable elapsed duration rather than
requiring active dismissal, removing both the interaction burden and the focus-management
complexity a dismiss control introduces. (IC ch10)

## Mobile & Touch

### Vertical Stack `PTN-100`
Lay out a mobile page as a single column that reflows regardless of actual screen width; when
moving between pages carries a real cost (a downloaded web page), prefer one long scrollable
page over discrete per-page splits — for content already local (installed app), discrete
one-screen-at-a-time pages can be reasonable instead. When: avoid for immersive full-screen
experiences (video, games) that don't scroll like text. Trade-off: one long page avoids
repeated load-wait cost but requires more scrolling; discrete pages reduce scrolling but each
transition may cost a wait unless content is local. (DI ch10)

### Filmstrip `PTN-101`
Lay a small number of conceptually parallel top-level pages side by side, moved between with a
horizontal swipe, as an alternative to tabs/menu/nav page; unlike Carousel it typically omits
neighbor metadata — show a dot-style page indicator to signal multiple pages exist. When:
avoid when the number of pages is large, or discoverability matters with no plan to teach the
gesture. Trade-off: gives content the full screen with no nav chrome but doesn't scale to many
pages and isn't self-evident to new users. (DI ch10)

### Touch Tools `PTN-102`
Keep controls hidden by default over full-screen immersive content (video, photo, map),
surfacing them as an overlay only on tap and auto-hiding after inactivity or a tap elsewhere —
the touch-primary counterpart to Hover Tools, which relies on a mouse-hover state Touch Tools
cannot use. Do: show a one-time onboarding dialog to new users, since the tap-to-reveal gesture
isn't otherwise discoverable. (DI ch10; DI ch6)

### Bottom Navigation `PTN-103`
Place global/site navigation as a vertically stacked list of large, tappable items at the very
bottom of a scrollable mobile page, reserving the highest-value top screen real estate for
actual content — the mobile-scroll counterpart to the desktop Sitemap Footer. (DI ch10)

### Thumbnail-and-Text List `PTN-104`
Pair a small thumbnail with text in each list row, optionally adding vivid color/icon/badge
markers; small mobile screens tolerate more saturated color than desktop without feeling
aggressive, so this pattern can lean on stronger color than an equivalent desktop list. (DI ch10)

### Infinite List `PTN-105`
Load only an appropriately-sized initial chunk of a very long list, adding more on demand via
"Load More" or auto lazy-load as the user scrolls to the end, rather than paginating to a
separate page or downloading everything up front. (DI ch10)

### Touch Target Hit Area Beyond Visible Boundary `PTN-106`
A tappable control's effective touch-sensitive hit area doesn't have to match its rendered
visual size — extend it invisibly into surrounding margin/whitespace so it's easy to hit with a
finger while the visual footprint stays as small as the design calls for. Do: target roughly
1cm square (or a platform minimum, e.g. 44x44px) for the effective, not necessarily visible,
hit area. (DI ch10)

### Text Clear Button `PTN-107`
Place a small "×"/Clear control inside a text field (typically trailing edge) that empties its
entire contents in one tap; use the platform's own default clear-button convention when one
exists, and usability-test any custom one, since users may misread it as Go/Search. (DI ch10)

### Loading Indicators `PTN-108`
Show progress feedback exactly at the location the awaited content will render (or the spot the
user tapped), rather than as a generic global indicator elsewhere; render already-available
parts immediately, reserving the indicator only for parts still pending — the mobile analog of
the desktop Progress Indicator, scoped tightly to its object. (DI ch10; DI ch6)

### Hamburger Navigation Menu Button `PTN-113`
A button toggling a collapsed/off-canvas navigation list on small screens must be a real
`<button>` (not a link or generic clickable div) and communicate its expanded/collapsed state
via `aria-expanded`. (IC ch4)

### Native `<select>` as a Condensed Navigation Menu `PTN-114`
A native `<select>` used to condense navigation options for narrow viewports is a legitimate
menu whose semantics closely parallel a true button-triggered menu, and should be preferred
over a custom scripted dropdown when its semantics genuinely match the navigation-condensing
need — distinct from repurposing a select to invoke actions (see Action: Don't Repurpose a
Dropdown-Select for Actions), since here it's choosing a destination, a value-selection role it
already fits. (IC ch4)
