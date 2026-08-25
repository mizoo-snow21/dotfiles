# Pattern Catalog — Layout & Panels

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

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
