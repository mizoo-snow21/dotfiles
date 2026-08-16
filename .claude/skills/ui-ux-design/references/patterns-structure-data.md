# Screen Patterns: Structure, Lists & Data

Load when: choosing a page/app structural pattern (dashboard, wizard, settings editor, canvas+palette, feed…), a list-to-detail or list-presentation pattern (master-detail, grid, carousel), a table design, or a composite data/information-graphic display (interactive charts, hierarchy views, filtering).

Contents: page/app structural patterns · list-to-detail patterns · list presentation & item actions · tables · hierarchy, long lists & pagination · information graphics & composite data patterns

## Page & App Structural Patterns

### Classify each page by its primary job first
Every important page does one (or more) of four jobs — show a single item, show a list/collection, provide a creation tool, or support a single task. Classify before picking a pattern; most real pages combine jobs.
- Do: Single-item → Alternative Views, Many Workspaces, Deep-linked State, Sharing Widget. List → Feature/Search/Browse, News Stream, Picture Manager. Creation tool → Canvas Plus Palette, Many Workspaces, Alternative Views. Single-task → forms, Wizard (long/branching), Settings Editor (open-ended properties).
- Ask: "Which of the four jobs does this page primarily do, and does its design match that job's typical patterns?"
⟨di1-024⟩

### Dashboard: consolidate monitoring data with aggressive curation
Consolidate high-density, continuously-refreshing external data onto one page, curated hard, using visual hierarchy so primary info fits with minimal scrolling.
- Do: remove/de-emphasize non-actionable data; group into titled sections (tabs only when side-by-side comparison isn't needed); drilldown for detail, datatips on graphic mouseover; pick chart type for comparison fitness, not decoration — simple line/bar beats gauges/dials/3D; use striped tables when text beats graphics; emphasize keywords/numbers since users skim; consider customizable layout.
- Avoid: scattering marginal/confusing data just because it's available.
- Ask: "Is every piece of data here something the user needs to act on or monitor?"
⚖ Tension: whitespace vs density → tradeoffs-decision-points.md (vh-d02)
⟨di1-028⟩

### Wizard: guide long or unfamiliar tasks step by step
For a long, complex, typically-unfamiliar task where the designer can be assumed to know the best path, guide users through a fixed sequence of chunks — but first check whether a short form would do.
- When: task has branching or many linear steps where earlier decisions affect later ones.
- Do: split into dependency-ordered chunks; add/skip steps dynamically by branch; calibrate chunk count (too few = pointless, too many = exhausting); let users move freely back/forward and edit earlier choices; pair with a step overview/map; give visible cancel/escape.
- Avoid: defaulting to a wizard for every multi-field task; using it for creative/exploratory tasks or users trying to learn the tool; letting users finish without understanding what their choices actually changed underneath.
- Exception: some cultures find wizards paternalistic.
- Trade-off: guided efficiency for unfamiliar tasks vs. constraint and hidden state for power/creative users.
- Ask: "Could this be one short form instead of a multi-step wizard?"
⟨di1-030⟩

### Settings Editor: random-access property editing
For app/system settings, profile editors, free-form property editing, or configurators, give users a findable page/window with random access to view and change properties — the opposite of a wizard's fixed sequence.
- Do: follow platform convention for settings location; place account/profile links near the username; group properties into pages with guessable titles (card-sort with real users); avoid hierarchies deeper than 2 levels; choose tabs / two-panel-selector / menu+drilldown presentation; decide immediate-apply vs. explicit save from convention or testing.
- Avoid: forcing sequential wizard-style navigation through settings that need random access; burying a common setting 3+ levels deep.
- Ask: "How many clicks does it take to reach the most commonly needed setting?"
⚖ Tension: wizard vs settings-editor → tradeoffs-decision-points.md (struct-d01)
⟨di1-031⟩

### Vertical Stack: default mobile page layout
Lay out mobile content in a single wrapping vertical column, avoiding side-by-side layouts, so pages degrade gracefully across device widths and font-size changes.
- When: nearly all mobile pages carrying text/forms, especially where per-page load cost is high — one long scrollable page then beats many small paginated ones.
- Do: put top-priority content within ~first 100px; place form labels above controls, not beside them; only place buttons side by side when their combined width can never exceed the viewport, accounting for localization and font growth.
- Exception: immersive full-screen content (video, games) that doesn't scroll; installed apps (no per-page reload cost) can reasonably split into discrete one-screen pages instead, since moving between them is instant.
⟨di4-031⟩

### Quick reference
- Feature/Search/Browse: for a large browsable+searchable collection's main page, combine a prominent search box, a strong featured item, and a category browse list so new visitors get a zero-effort hook plus two complementary find-paths; keep any other text field off the first screen so users don't mistype a query into it. ⟨di1-025⟩
- News Stream: list time-sensitive items newest-first in a continuous, ideally live-updating stream (manual refresh too), splitting high-volume streams into user-selectable substreams; show what/who/when/where per item, support light reactions plus full replies, and use infinite-list loading (not pagination) for deep streams. ⟨di1-026⟩
- Picture Manager: build image/video collections around a coordinated thumbnail grid + single-item detail (Two-Panel Selector if space allows, else One-Window Drilldown with prev/next) + browse/search, so once users recognize the pattern they can predict what they can do. ⟨di1-027⟩
- Canvas Plus Palette: for graphic-editing tools, pair a blank canvas with an icon-grid palette (left/top) users click or drag from; put secondary panels (properties, swatches) right/bottom; usability-test drag-vs-click-then-click creation, since expectations vary widely. ⟨di1-029⟩
- Alternative Views: when minor customization (font size, zoom) can't reconcile conflicting presentation needs (e.g. print vs. screen), offer switchable alternate presentations that preserve core content and app state (selection, position, unsaved edits, undo history) across the switch, remembering the user's last choice. ⟨di1-032⟩
- Many Workspaces: for apps built around browsing/editing multiple items, support side-by-side multitasking via tabs, tab groups, windows, or draggable split panes — simple content fits split panes, complex content needs a full tab/window; consider restoring prior open workspaces on relaunch. ⟨di1-033⟩
- Filmstrip: when several top-level pages are conceptually parallel (weather per city, scores per sport), let users swipe between them instead of a toolbar/tabs/menu page, with a dot indicator if you need to signal more pages exist; avoid too many pages (excessive swiping) or swipe-only navigation with no indicator. ⟨di4-032⟩
- E-commerce flow: follow the established Product → Cart → Checkout structure (categorized/filterable listings with direct-to-checkout for single items; quantity edit/remove/empty-cart; totals, shipping/payment, sign-in for returning customers, and guest checkout without forced account creation) rather than inventing a novel flow. ⟨uxp1-065⟩
- Messaging/chat UI: follow the established pattern — unread count; inbox grouped by contact, newest-first, with message previews; chronological thread view that clears unread status on open; a reply field that allows line breaks without submitting on Enter — rather than reinventing it. ⟨uxp1-097⟩

## List-to-Detail Patterns

### Choose a list-to-detail pattern by task and space
When a user selects an item from a list, choose how to reveal its detail — adjacent panel (Two-Panel Selector), inline expansion (List Inlay), or full replacement (One-Window Drilldown) — based on primary use case and available space, not default convention.
- Do: Two-Panel Selector when there's room for two panels and users browse quickly while keeping the list visible; List Inlay when users need to compare 2+ items and the list is single-column; One-Window Drilldown only when space is too tight for the others, or content is too large to share space (e.g. forum topic list → full post). Always give drilldown a way back.
- Avoid: defaulting to drilldown on desktop just because it's simple; forcing inlay when items aren't arranged in a single column.
- Exception: drilldown can be the right choice even off-mobile when content is simply very large.
- Trade-off: overview-with-detail visibility vs. screen space required; quick switching (two-panel) vs. comparability (inlay) vs. simplicity (drilldown).
- Ask: "Does the user need to compare items, browse quickly, or just view one at a time — and is there space for two panels?"
⟨di3-001, di3-003, di3-004, di3-005⟩

### Quick reference
- Two-Panel Selector: list panel beside (above/left of, mirrored for RTL) an instantly-updating detail panel; support keyboard/arrow-key selection and a visually distinct selected state; needs enough width for two simultaneous panels. ⟨di3-003⟩
- One-Window Drilldown: replace the list with item detail in the same window, always with a clear back affordance, plus prev/next links so users can move item-to-item without returning to the list each time. ⟨di3-004⟩
- List Inlay: expand an item's detail inline within a single-column list, pushing later items down in a scrollable area, with a labeled close control at both top and bottom of long panels and an animated open/close transition; can also host inline editing; opening too many items at once hurts overall list overview. ⟨di3-005⟩

## List Presentation & Item Actions

### Match list item density to task type
Scale how much each row shows to the task — name only for targeted lookup, richer previews/thumbnails for browsing — capping density before it overwhelms scanning.
- Do: show item name only for lookup tasks; add thumbnails/imagery and extra text for browse-oriented lists; cap density before it hurts scanability.
- Avoid: padding every row with maximal metadata regardless of task.
- Trade-off: information richness vs. scanability/density.
- Ask: "Is this list for finding one known item, or open-ended browsing?"
⟨di3-002⟩

### Quick reference
- Thumbnail Grid: for visually distinctive items (images/logos/screenshots) of similar size, use a uniform 2D thumbnail grid with subordinate metadata text; preserve original aspect ratio instead of force-cropping when size/shape itself is meaningful (e.g. personal photos). ⟨di3-006⟩
- Thumbnail-and-Text List: for selectable content rows (articles, videos, apps) especially on mobile, put a thumbnail beside the text (usually left) with an optional secondary line and status/rating markers — small screens tolerate more saturated color for these markers than desktop would. ⟨di4-035⟩
- Carousel: for visually distinctive, similarly-sized flat (non-categorized) items when vertical space is scarce and browsing is casual, show fewer than ~10 items in a scrollable/swipeable line with large jump-arrows and an animated transition; add a scrollbar for fast access to distant items, and redesign as a searchable list if users lean on it heavily; not for categorized lists or targeted search. ⟨di3-007⟩
- Off-screen peek: show a partial edge of hidden content (carousels, tab strips, scrollable panels) as a visual cue that more exists, but never as the sole means of reaching it. ⟨uxp1-071⟩
- New-Item Row: let users create an item by typing directly into an obviously-clickable empty/dummy row at the top or bottom of a list/table, committing a real (deletable) object as soon as creation starts so an abandoned edit isn't left in an undefined state, with pre-filled defaults. ⟨di3-014⟩
- Duplicate-and-edit: in CRUD/list-maintenance apps or repeated similar-item creation, offer a "duplicate and edit" action that copies an existing record into a new, auto-named, pre-filled, editable one instead of forcing users to retype it. ⟨uxp1-066⟩

## Tables

### Sortable Table: click-header column sorting
Let users click a column header to sort all rows by that column, toggling ascending/descending — now such a strong convention that users expect it by default.
- Do: choose columns for what users will want to sort/search by; give headers a clear clickable affordance plus hover feedback; show an up/down arrow for sort direction (also marks last-sorted column); use a stable sort so secondary sorts preserve tie-group order; persist sort order across restarts; consider drag-and-drop column reordering.
- Avoid: an unstable sort algorithm that scrambles previously-established order within tied groups.
- Ask: "Does the sort persist across sessions, and is it stable for tied values?"
⟨di3-041⟩

### Quick reference
- Row (zebra) striping: alternate two muted, similar-hue colors (one matching the page background) by single row — not 3-row blocks — only for large multi-column tables with wide column gaps where rows are hard to track; small tables show no measured benefit, and a thin horizontal rule is an acceptable substitute if it proves unhelpful. ⟨di3-008⟩
- Tree Table: combine an indented hierarchy outline in the first column with attribute columns elsewhere, one row per item; pair with sortable-table behavior but give users a dedicated way to restore tree order after a column sort breaks it; adds complexity, so avoid for novice-heavy audiences. ⟨di3-013⟩

## Hierarchy, Long Lists & Pagination

### Pagination for finite lists; infinite scroll only for feeds
Split a long, bounded list into pages with next/prev/first/last by default. Reserve infinite/continuous scroll for genuinely open-ended feed content (photo/social feeds) — never apply it to a finite list (messages, email, to-dos, catalogs, records), which disorients users and breaks the scrollbar's ability to show position or reach the footer.
- Do: make page 1 alone satisfy most users; let users set items-per-page for lists they'll linger on; disable prev/next at the ends; always link to page 1 and highlight (don't link) the current page; truncate long page-number lists past ~20 with ellipses, keeping first/adjacent/last visible; past ~3 pages, add search/sort/filter too.
- Avoid: infinite scroll on a finite list; making users hunt across pages for common items; omitting the first-page link when truncating.
- Exception: search results specifically should front-load quality on page 1, since users rarely go further.
- Trade-off: pagination matches convention but burdens deep browsing; infinite scroll is convenient but loses scrollbar position and footer access.
- Ask: "Does this content have a real beginning/end (pagination), or is it a genuine feed (infinite scroll)? Will most users find their target on page 1?"
⟨di3-009, uxp1-057, uxp1-059⟩

### Preserve position; never silently reflow a list on return
When a user leaves a list/feed for an item's detail and returns, restore their exact prior position (scroll offset or page) — not the top or page one — and never auto-refresh or reorder the feed while they're browsing it. Refresh only on explicit request, signaled by an unread-count indicator.
- Do: restore exact scroll position (infinite scroll) or exact page (paginated); preserve the user's position or next-unread item; show an unread-count cue when new content has arrived; let users manually trigger refresh.
- Avoid: resetting to the top or page one on return; auto-refreshing or reordering a feed mid-browse.
- Ask: "When a user navigates back to this list, do they land exactly where they left it? Could it change out from under them mid-session?"
⟨uxp1-058, uxp1-060⟩

### Quick reference
- Cascading Lists: for a deep hierarchy with many items per level, show each level in its own scrollable list column (leftmost = top level), populating the next column on selection, with a leaf item's detail in the rightmost position; needs wide horizontal space and is unfamiliar to hierarchy-novice users. ⟨di3-012⟩
- Fast-jump navigation: for a long alphabetically/numerically sorted list, table, tree, or dropdown, offer type-ahead (typed characters jump/select the closest match, without resetting to the top on no exact match) and/or an alphabet-scroller mounted on the scrollbar (adaptable to numeric/date ordering too). ⟨di3-010, di3-011⟩
- Infinite List loading: once infinite scroll is the right choice for a bottomless list, load only the first screen or two up front, then batch-load more via an explicit "load more" button (state the count) or silently near the end — pick batch size by whether the user is scanning or reading in order. ⟨di4-036⟩

## Information Graphics & Composite Data Patterns

### Choose an organizational model matching the data's structure
Pick the visual model (linear, tabular, hierarchical, network, geographic, textual) for an information graphic based on the structure the data itself suggests; show the same data in more than one model if it has multiple relevant facets.
- Do: identify which model(s) fit the data's inherent structure; represent the same dataset in more than one model when several facets are each individually interesting.
- Avoid: forcing data into a single model that hides an important structural facet (e.g. geographic data shown only as a plain table).
- Trade-off: single unified view (simplicity) vs. multiple views (completeness, extra cost).
- Ask: "Does this data have more than one structurally-relevant facet that deserves its own view?"
⟨di3-029⟩

### Use preattentive visual variables to encode data distinctions
To make data points stand out or encode extra dimensions without forcing users to read/think, vary preattentive properties (hue, brightness, saturation, size, orientation, shape, texture, position) instead of relying on plain text — these cues are processed before conscious attention, so they're found in constant time regardless of set size.
- Do: use redundant encoding (e.g. color + shape) to aid distinction; layer information by preattentive cues so users perceive distinct "grades" of data at a glance.
- Avoid: expecting users to notice a highlighted point marked only with plain, undifferentiated text.
- Trade-off: redundant encoding aids distinction but adds visual complexity.
- Ask: "Which preattentive variable encodes the distinction users need to see quickly?"
⟨di3-030⟩

### Provide focus-plus-context navigation for large data spaces
When a data graphic is too large to fully display, provide scroll/pan, zoom, expand/collapse, or drilldown so users can focus on a point of interest while retaining a sense of its place in the whole.
- Do: scroll/pan for over-viewport content (or click-to-load-next-screen when scrollbars are unreliable); zoom for dense maps/graphs; let hierarchical diagrams expand/collapse in place; connect any search feature to these mechanisms (e.g. searching a city should pan/zoom the map there).
- Avoid: forcing a new window for every detail view when in-place expand/collapse or drilldown would preserve context.
- Exception: drilldown takes the user away into separate detail, unlike expand/collapse which stays in place.
- Ask: "Does a search result actually pan/zoom to that point, or does it dump the user out of context?"
⟨di3-031⟩

### Design filter/query UIs to be interactive and composable
Make search/filter/query controls over a data graphic highly interactive, iterative, context-preserving, and able to combine conditions — users don't distinguish "filtering" from "querying," they just want to zero in on the relevant subset.
- Do: respond fast (skip per-keystroke updates if they disrupt typing); let users iteratively refine (search, then filter the results); show results within surrounding data context (e.g. scroll so the find is centered); support compound conditions, not just single toggles; consider highlighting a subset instead of hiding the rest when relative context matters.
- Avoid: returning results in total isolation from surrounding context; limiting to single toggles when compound queries are genuinely needed.
- Trade-off: instant per-keystroke feedback vs. disrupting the user's typing flow.
- Ask: "Can users combine multiple filter conditions, and are results shown with enough surrounding context to stay oriented?"
⟨di3-033⟩

### Choose the right technique to reveal exact data values
Pick among direct labels, legends, axes/rulers, datatips, spotlight, and brushing based on how precisely users need exact values versus how dense the graphic already is.
- Do: use direct labels for values needing accurate, immediate reading (watch for clutter at high density); keep legends on the same page as their graphic; use axes/rulers when direct labels would be too dense; use datatips for interactive graphics to avoid per-point clutter; keep any label text readable and well-aligned.
- Avoid: over-labeling a dense graphic to the point of clutter when axes or datatips would serve better.
- Exception: datatips and data spotlight require an interactive graphic — they don't work in static output.
- Trade-off: label clarity/accuracy vs. visual clutter at high data density.
- Ask: "Is this graphic static or interactive, and does that rule out datatips/spotlight?"
⟨di3-034⟩

### Quick reference
- Re-sortable graphics: offer sorting beyond alphabetical (numeric, date, physical position, category, popularity, user-defined, random) since reordering by value places comparable points adjacent and surfaces relationships a default order hides; let users choose the baseline series in a stacked bar chart. ⟨di3-032⟩
- Overview Plus Detail: for large maps/images, show a persistent small overview beside a zoomed detail view, with a draggable, distinctly-colored viewport box that keeps both views synced within ~0.1s. ⟨di3-035⟩
- Datatips: on hover, show a point's value in a compact floating tooltip that doesn't obscure the graphic, with optional drill-down links; use local zooming instead if the goal is an enlarged rendering rather than a value; a static side panel that updates on hover is a viable alternative to a floating tip. ⟨di3-036⟩
- Data Spotlight: on hover over a data "slice" (not a single point), highlight it and dim the rest for focus-plus-context in dense graphics; keep the base graphic interpretable without the interaction (some users print it); consider a longer initial hover delay or a click-trigger to avoid accidental activation, especially on touch. ⟨di3-037⟩
- Dynamic Queries: map standard controls (sliders, checkboxes, radio buttons) to data attributes for instant, real-time filtering without a query language — match control type to attribute type (range slider, single-choice dropdown with "select all," multi-select checkboxes); direct in-display selection works only when the data has a spatial representation. ⟨di3-038⟩
- Data Brushing: let a selection in one view (rubber-band, click, shift-click, lasso) highlight the same items in linked views simultaneously, with fast response and a consistent visual treatment (color hue is the most common choice) across every view. ⟨di3-039⟩
- Local Zooming: render the whole dataset small, then fisheye-enlarge the area under the pointer to preserve context while revealing detail (vertical-only for table rows, both axes together for maps); the surrounding-space distortion can disorient users, so prefer Overview Plus Detail or datatips when it's overkill. ⟨di3-040⟩
- Radial Table: arrange a table/list circularly to draw connecting lines between items more legibly than rows/columns, using the center for summary data and the exterior for fine detail; simplify or abandon it if users can't interpret it, and cut line clutter with bundling or spotlight/query filtering. ⟨di3-042⟩
- Multi-Y Graph: stack graphs sharing one X-axis but give each its own Y-axis scale (rather than one shared axis) when value ranges differ greatly, since overlaying differently-scaled series on a shared axis implies a false "apples to apples" comparison; omit the Y-axis when exact values don't matter. ⟨di3-043⟩
- Small Multiples: tile many small, visually consistent images across 1-2 extra dimensions (a sequence or a 2D matrix) instead of forcing extra dimensions into one image, binning/shingling a dimension with too many values; sparklines are the compact, label-stripped variant usable inline in text or table cells. ⟨di3-044⟩
- Treemap: represent hierarchical/multivariate data as nested, variously-sized rectangles (area = numeric value, color = another variable, nesting = hierarchy/category), with datatips for truncated labels and drilldown to a detail page; needs a meaningful grouping and screen/interactivity to stay readable — avoid for print or reluctant novices. ⟨di3-045⟩
