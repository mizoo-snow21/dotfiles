# Pattern Catalog — Lists

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

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
