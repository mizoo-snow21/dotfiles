# Pattern Catalog — Data Display

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

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
