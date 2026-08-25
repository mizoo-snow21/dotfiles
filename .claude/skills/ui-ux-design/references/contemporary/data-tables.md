<!-- Contemporary product-derived reference (V2). Provenance layer: product-derived —
every rule cites fetched public design-system docs / product materials; confidence is
marked per rule. These rules complement the book-derived foundation: books carry the
WHY (cognition, perception), these carry current practice under real product constraints.
When they conflict with a book rule, treat it as a decision point, not an override. -->
# Data Tables & Dense Lists — Cross-Product Decision Rules

Research method: fetched/searched published design-system documentation (GitHub Primer, Shopify
Polaris, IBM Carbon, Adobe Spectrum, Vercel Geist) plus product-engineering blog posts (Linear) and
one credible independent pattern analysis (Pencil & Paper) and one first-party product announcement
(Airtable community). Every rule below cites at least one source that was actually fetched or
returned verbatim quotes via search. Where a claim could not be verified against primary material,
it is marked confidence: low and the gap is stated rather than papered over.

---

## Decision rules

### ct-tbl-01 — How many density levels to offer, and are they a designer choice or a user toggle?
**Question:** Should row density be a fixed decision baked into the table, or an adjustable control?
**Guidance:** Treat density as a small named scale (3 for a general design system, up to 5 for an
enterprise/analyst tool), and pick who controls it based on audience: a general SaaS product picks
the density *per context* at design time (index/list screens dense, focused-task components
spacious); a tool whose users live in it for hours, or whose records vary wildly in content size,
exposes density as a *user preference* instead.
**Evidence:**
- Primer offers three cell-padding options — Condensed, Normal (default), Spacious — described as a
  per-table design choice, not end-user-facing. (primer.style/design/components/data-table/)
- IBM Carbon offers five row sizes (extra large, large, medium, small, extra small), explicitly
  tied to content needs: "Extra large row heights are only recommended if your data is expected to
  have 2 lines of content in a single row." (carbondesignsystem.com/components/data-table/usage/,
  verified via github.com/carbon-design-system/carbon-website usage.mdx)
- Airtable ships density as an end-user toggle: four row-height settings, letting users choose
  "the default short height to maximize the number of records you can see on your screen, or pick
  tall to see larger images and more text per each record." (community.airtable.com,
  "Row height: control density of records in grid view")
- Shopify Polaris frames density as an interface-wide principle, not a per-table switch: "Dense UIs
  help users focus... Information-rich interfaces like index pages or data tables require
  high-density layouts," but density "should not be applied to components that involve focused
  tasks, such as interacting with a dropdown menu or picker." (polaris-react.shopify.com, Layout →
  Density, via search extraction)
**Tension:** A fixed density is simpler to design and test and guarantees visual consistency; a
user-facing toggle costs UI real estate and an extra state to persist, but wins when the same table
serves both a scanning power-user and someone who needs to see thumbnails/long text (Airtable's
exact stated reason).
**Confidence:** high (four independent systems, explicit rationale in three of them).

### ct-tbl-02 — Numeric alignment and tabular figures
**Question:** How should numeric columns be aligned and typeset?
**Guidance:** Right-align quantitative numbers (currency, counts, percentages, measures) and apply
tabular/monospaced figures so digits stack in a fixed-width column; left-align qualitative
"numeric-looking" data (dates, phone numbers, postal codes, IDs) because comparing their magnitude
is not the point.
**Evidence:**
- Primer: "Right-align numeric values and use the `tabular-num` font variant when possible" to
  improve scannability. (primer.style/product/components/data-table/guidelines/)
- Vercel Geist: "Apply `tabular-nums` (or Geist Mono) to numeric columns so digits align across rows
  for comparison." Framed as deliberate "engineering-grade" aesthetic used consistently across
  tables, deploy logs, and metrics. (vercel.com/geist/table)
- Pencil & Paper: right-align quantitative numbers "to enable comparison and contrast," and use
  monospace/tabular figures because in a proportional typeface "$1,111.11" can visually read smaller
  than "$999.99" — decimal-point alignment lets users do mental math down a column. Explicitly
  carves out the exception: "qualitative numbers (dates, postal codes, phone numbers) may
  left-align despite numeric format." (pencilandpaper.io, "UX Pattern Analysis: Enterprise Data
  Tables")
**Tension:** None found — this is the one rule where every fetched source agrees with explicit
rationale.
**Confidence:** high.

### ct-tbl-03 — Default text alignment
**Question:** What's the default alignment for ordinary text columns?
**Guidance:** Left-align text by default (natural reading direction); never center text columns in
a data table — center alignment removes the left edge that makes a column scannable top-to-bottom.
**Evidence:**
- Adobe Spectrum: "Textual data is always left-aligned within a table and center alignment should
  never be used." (spectrum.adobe.com/page/table/, via search extraction of live page content)
- Primer: left alignment is the default; right-align is reserved for numeric/comparable data.
  (primer.style/design/components/data-table/)
**Tension:** None — no system recommends centered text columns.
**Confidence:** high.

### ct-tbl-04 — Border/divider strategy: full grid vs horizontal-only vs none
**Question:** When do column/cell borders help scanning vs. add noise?
**Guidance:** Use full grid lines (or column dividers) when a table has many columns of
heterogeneous, unrelated data that benefit from explicit separation; use horizontal-only dividers
(or none, relying on whitespace) for tables with few columns or where rows read as coherent units.
Keep any column divider very light (near-invisible) — it should organize, not decorate. Systems
moving toward calmer UI treat borders/dividers as a *last resort* for hierarchy, preferring contrast
and whitespace first.
**Evidence:**
- Carbon: column dividers are optional; when used, "1px max and a light grey colour" to avoid
  clutter. (via search synthesis of carbondesignsystem.com content)
- Adobe Spectrum: "Column dividers are for organizing table content and aid the user in parsing
  related data, though these are optional and should be used carefully to group related content."
  Also offers a "quiet" table variant — "transparent background and no side borders" — for when the
  table is "meant to be supplementary, subtle, or lightweight" rather than the main focus.
  (opensource.adobe.com/spectrum-web-components/components/table/, spectrum.adobe.com/page/table/)
- Linear (product blog, on the wider UI, not tables specifically, but stated as a general
  principle it applied surface-wide): "Borders and separators help clarify the relationship between
  elements... By rounding out their edges and softening the contrast, the polished interface gives
  users structure without cluttering their view." The redesign explicitly "reduces visual noise with
  fewer separators" and replaced heavier chrome with softened-contrast hairline borders.
  (linear.app/now/behind-the-latest-design-refresh, linear.app/now/how-we-redesigned-the-linear-ui)
- Pencil & Paper frames this as four competing row-division strategies (see ct-tbl-05) and says
  "free form" (no separators at all) is "best for lower-density, less-complex data."
**Tension:** Heavier grid lines cost visual weight and can feel "spreadsheet-y"/dated, but they win
when columns are unrelated and a reader's eye needs a hard stop (financial reconciliation tables,
wide operational dashboards). Borderless/whitespace-driven tables read as calmer and more modern but
require generous, consistent spacing to keep rows scannable — they degrade badly at high density
without that discipline.
**Confidence:** high (design-system agreement on light/optional dividers; medium on the "borders as
last resort" framing, since that's explicit only in Linear's general-UI post, not table-specific).

### ct-tbl-05 — Zebra striping: when it helps vs. when it fights your state colors
**Question:** Should alternating row background color be used to aid horizontal scanning?
**Guidance:** Zebra striping helps pure left-to-right scanning on wide tables with faint or no other
dividers. It becomes a liability the moment rows also carry semantic state (selected, hover, focus,
disabled, error) — the striping adds a background-color axis that now has to be visually
disambiguated from every other state color, and systems that ship it explicitly warn about this
collision. Prefer a plain white/near-white background with subtle horizontal row dividers when the
table has any interactive row states.
**Evidence:**
- IBM Carbon ships zebra striping as an explicit opt-in modifier ("style the table rows with
  alternating colors to make scanning horizontal information easier for the user") but pairs this
  with separate guidance elsewhere in the system to prefer no zebra striping plus row dividers in
  contexts with richer row state. (carbondesignsystem.com/components/data-table/usage/, GitHub
  carbon-website usage.mdx)
- Pencil & Paper states the tradeoff directly: with zebra stripes it "becomes tricky... to
  effectively differentiate between disabled, hover, focused and active states," because striping
  adds extra semantic color levels that "cause visual confusion." Its four listed row-division
  approaches (zebra stripes, line divisions, "card" rows against a tinted page background, and no
  dividers at all) each carry different best-fit contexts. (pencilandpaper.io)
- Vercel Geist offers a bare `striped` prop with no stated guidance on when to use it — a case where
  the component exists but the design system does not (yet) publish rationale.
  (vercel.com/geist/table)
**Tension:** Zebra striping genuinely improves row-tracking accuracy on very wide tables with many
plain-text columns and minimal other affordances (this is why it persists in spreadsheet-like UIs).
It loses when rows are interactive, selectable, or carry status colors — which describes most
modern product tables — because it competes with those colors for attention.
**Confidence:** medium-high (explicit tradeoff from one credible analysis + one design system's
opt-in/caveat pattern; not all systems take a position).

### ct-tbl-06 — Row actions: persistent vs. hover-revealed vs. overflow menu
**Question:** How should per-row actions be exposed?
**Guidance:** Use a numeric threshold, not a vibe: with one or two row actions that are frequent and
low-risk, show them as persistent inline icon buttons. At three or more actions, collapse them into
an overflow ("kebab") menu instead — this is a hard rule in at least one design system, not a
guideline. Reveal-on-hover is a valid way to reduce visual weight for occasional actions on
desktop, but it is not accessible on its own: it must have a keyboard-focus-visible equivalent and
should not be relied on as the *only* discovery path, because it fails for touch and for anyone
scanning via keyboard/AT. Destructive or rare actions belong inside the overflow menu regardless of
count.
**Evidence:**
- IBM Carbon (hard rule): "When the overflow menu contains fewer than three options, keep the
  actions inline as icon buttons instead. This approach reduces a click and makes available actions
  visible at a glance." And on the batch/selection interaction: "When batch mode is active, single
  action icons and overflow menus on the row should be disabled." (carbondesignsystem.com, verified
  via github.com/carbon-design-system/carbon-website usage.mdx)
- Shopify Polaris IndexTable: "reveal row actions on hover" as an explicit pattern alongside
  checkboxes for bulk selection. (shopify.dev/docs/api/app-home/patterns/compositions/index-table)
- Pencil & Paper: "When a checkbox is shown upon hover, it hints to rows being actionable" — same
  hover-reveal logic applied to selection affordances, with an explicit call-out that hover-only
  patterns create a "discoverability challenge on touch." (pencilandpaper.io)
- Carbon's own component backlog documents the tension inside the system itself: a filed issue
  "Overflow menu for data table rows should be visible on hover" shows the design intent (reduce
  clutter) colliding with implementation reality (discoverability), which is exactly the risk being
  guarded against. (github.com/carbon-design-system/carbon, issue #5804 — used as evidence of a
  live disagreement, not as design-system guidance itself)
**Tension:** Persistent actions cost horizontal space and add visual clutter proportional to action
count; hover-reveal buys back that space and reads as "clean" but is discoverability-hostile on
touch devices and easy to miss on desktop too. Overflow menus are the safest default for anything
destructive or rare because they require deliberate intent to open, at the cost of an extra click for
the single most common action.
**Confidence:** high for the 3-action threshold and batch-mode interaction (Carbon is explicit and
specific); medium for hover-reveal as a general pattern (widely used but its accessibility caveat is
inferred from a Pencil & Paper aside and a live Carbon GitHub issue, not a formal accessibility
guideline in any fetched source).

### ct-tbl-07 — Selection UI: checkbox placement and hover-reveal
**Question:** How should row selection be surfaced?
**Guidance:** Put selection checkboxes in the leftmost column, support a tri-state header checkbox
(unchecked / indeterminate / all-selected), and reveal the checkbox on hover (with it staying
visible once any row is selected) rather than showing empty checkboxes on every row all the time —
this keeps a non-selectable-feeling table visually calm until the user signals intent to select.
**Evidence:**
- Adobe Spectrum: "if a table has selectable rows, it should have checkboxes to the left of the
  table." (spectrum.adobe.com/page/table/)
- Shopify Polaris IndexTable: three-state checkbox behavior (unchecked/indeterminate/checked),
  supports shift-click range selection. (shopify.dev index-table pattern doc)
- Pencil & Paper: "When a checkbox is shown upon hover, it hints to rows being actionable" — framed
  as deferring the interactive affordance until it's contextually relevant. (pencilandpaper.io)
**Tension:** Always-visible checkboxes are more discoverable and more touch-friendly (no hover
state to miss) at the cost of a busier default view; hover-reveal is calmer by default but requires
a fallback for touch (typically: checkboxes become permanently visible once the table enters "select
mode," e.g. via a long-press or an explicit "Select" toggle).
**Confidence:** medium-high (placement and tri-state are consistently documented; hover-reveal
timing is stated by only one source with explicit rationale).

### ct-tbl-08 — Bulk action bar: appear contextually, replace the toolbar
**Question:** Where do bulk actions live, and when are they visible?
**Guidance:** Don't show bulk-action buttons permanently disabled/greyed-out. Instead, replace the
table's normal toolbar (search, filters, per-page settings) with a dedicated action bar the moment
one or more rows are selected, showing a selection count and a cancel/deselect-all affordance. This
is "very smart use of space" — the UI only asks for the screen real estate when it's relevant to what
the user is doing right now.
**Evidence:**
- IBM Carbon: "Once an item from the table is selected, the batch action bar appears at the top of
  the table, presenting a set of possible actions to apply to all select items... To exit the batch
  action mode, the user can select the cancel button on the far right of the bar or deselect all
  items." (carbondesignsystem.com, verified via GitHub carbon-website usage.mdx)
- Shopify Polaris IndexTable: "Display bulk action bar only when items are selected, replacing
  filter controls... Show selection count: 'X of Y selected.' Include action buttons (edit, archive,
  delete) with critical tone for destructive operations... Use Modal API to confirm destructive
  actions before execution." (shopify.dev index-table pattern doc)
- Pencil & Paper: "Once one or more rows are selected, only then is it relevant to display said
  actions" — explicitly framed as reducing cognitive load via conditional disclosure.
  (pencilandpaper.io)
**Tension:** None found — every source that discusses bulk actions agrees on contextual
replacement over permanent-but-disabled buttons. The only cost is a layout shift when selection
starts/ends, which systems mitigate with an animated transition (Carbon explicitly designs an
"animation clip" for the batch bar appearing/disappearing, per its own issue tracker).
**Confidence:** high (independent agreement, matching rationale, across two full design systems and
one pattern analysis).

### ct-tbl-09 — Sorting affordances: header-as-button, with a mandatory default
**Question:** How should sortable columns be indicated and how should sort state be seeded?
**Guidance:** Make the column header itself the sort control (not a separate icon button next to
static text) — it should behave as a real button, with the label staying visually stable and an
arrow/chevron indicating direction without disturbing the header's alignment. If any column in the
table is sortable, one column must have a default sort applied on load; don't ship a sortable table
in an arbitrary/unsorted state.
**Evidence:**
- Primer: column headers are "buttons that sort rows by the column data in ascending or descending
  order. Sort functionality may be disabled on a column-by-column basis." Sortable table rule: "If a
  table is sortable, one column must be sorted by default." Clicking toggles asc/desc on the active
  column; clicking a new column sorts it ascending first. (primer.style/design/components/data-table/)
- Vercel Geist: "Sortable column headers are buttons. The visible label stays Title Case; the
  sort-direction arrow is decorative and the button announces the next sort state to assistive
  tech." (vercel.com/geist/table)
- IBM Carbon: three explicit states — unsorted, sorted-up, sorted-down — with the arrow icon shown
  "on hover and when a column is sorted" (i.e., not permanently visible on unsorted columns, to
  reduce visual noise). (carbondesignsystem.com, via GitHub carbon-website usage.mdx)
- Pencil & Paper: "The sort chevron shouldn't interfere with the alignment of the heading," and
  recommends the default sort reflect business priority — "most recent entries at the top... or
  entries most needing action" rather than an arbitrary column. (pencilandpaper.io)
**Tension:** None on the header-as-button pattern. On default-sort, the cost is a design decision
every table author must make deliberately (which column, which direction) — the alternative
(leaving it unsorted) is cheaper to ship but leaves users staring at server/insert order, which
Primer's rule exists specifically to prevent.
**Confidence:** high (three design systems converge on header-as-button; the mandatory-default-sort
rule is explicit in Primer and echoed as a best practice in Pencil & Paper).

### ct-tbl-10 — Column headers: Title Case noun phrases, unlabeled action column
**Question:** How should column headers be worded, and does every column need a visible header?
**Guidance:** Column headers should be short noun phrases in Title Case, never full sentences
("Requests (7d)," not "How many requests in the last 7 days"). The column holding row actions is the
one exception to "every column has a header" — give it no visible label (but keep an accessible
label for screen readers) since the icons/menu are self-explanatory and a header would just say
"Actions" redundantly.
**Evidence:**
- Vercel Geist: "Column headers (`<Table.Head>`) are Title Case nouns or noun phrases: `Last Used`,
  `Requests (7d)`, `Created`, `Status`. Never sentences." (vercel.com/geist/table)
- Primer: "The column that contains row actions does not have a visible column header," while
  actions are described as "Actions that affect the item represented in the row."
  (primer.style/product/components/data-table/guidelines/)
**Tension:** None found; this is a low-controversy micro-convention, but it's easy to get wrong
(labeling the actions column "Actions" is extremely common in the wild despite this guidance).
**Confidence:** medium (only two sources, but both are explicit and specific — no counter-example
found in any fetched material).

### ct-tbl-11 — Rendering missing/unknown values
**Question:** What should an empty cell show when a value is unknown or not applicable?
**Guidance:** Use a plain em dash ("—") for missing/inapplicable values. Don't substitute "N/A,"
"null," or a blank string — a dash reads as "intentionally empty" at a glance, is scannable in a
numeric column (it doesn't get mistaken for a value), and avoids the visual noise of repeated text.
**Evidence:**
- Vercel Geist: "Render `—` in cells where a value is unknown or not applicable. Don't substitute
  `N/A`, `null`, or an empty string." (vercel.com/geist/table)
**Tension:** No counter-evidence found; this is a small, specific convention that only one fetched
source states explicitly, but it aligns with the broader "keep cells terse" principle Primer states
independently ("Cells should represent data in the shortest possible format").
**Confidence:** low-medium (single explicit source; flagged because it wasn't cross-verified against
a second design system, though it is consistent with Primer's general terseness rule).

### ct-tbl-12 — Empty states: replace the table, don't render an empty shell
**Question:** What happens when a table has zero rows (no data yet, or a filter matched nothing)?
**Guidance:** Don't render a table with headers and an empty body — render a dedicated empty-state
component in the table's place, with explanatory text (and ideally a way out, e.g. "clear filter").
This applies to both "no data exists yet" and "current filter/search matched nothing" — the two
cases should probably use different copy, but both replace the grid rather than leaving a
headers-only husk.
**Evidence:**
- Primer: shows a Blankslate component and "optionally provide explanatory text for missing data
  rather than symbols." (primer.style/product/components/data-table/guidelines/)
- Vercel Geist: "When the underlying list is empty (filter cleared, never created), render `Empty
  State` outside the table rather than an empty `<Table.Body>`." (vercel.com/geist/table)
**Tension:** None found — both sources that address this agree.
**Confidence:** medium-high (two independent design systems, matching guidance, though neither
distinguishes copy for "no data" vs. "no matches" — that distinction is a reasonable inference, not
sourced).

### ct-tbl-13 — Pagination vs. virtual/infinite scroll
**Question:** At what point does a table need pagination or virtualization instead of rendering
every row?
**Guidance:** For tables a user navigates deliberately (they want to know "page 3 of 12," or need a
stable position to return to), paginate — it gives a sense of place a scrolling view doesn't. Start
around 20 rows per page as a default and adjust for row complexity/visual density. Once a table's
row count climbs into the low thousands, or the page otherwise starts feeling heavy on scroll,
switch to virtualization (rendering only the rows in/near the viewport) rather than paginating
purely for performance reasons — the two techniques solve different problems (navigability vs.
render cost) and can be combined (paginate visually, virtualize under the hood, or virtualize with a
manual "show more" instead of true infinite scroll).
**Evidence:**
- Primer: "Use pagination to accommodate tables with a large dataset... By paginating, the user can
  focus on segments of a large dataset without being overwhelmed. Pagination also helps with
  performance by reducing the amount of data to be downloaded and the amount of content that needs
  to be rendered. 20 rows is a good place to start for page size." (primer.style/product/components/
  data-table/guidelines/)
- Vercel Geist: ships both a `virtualize` prop and a `ShowMore` component for "progressive loading of
  large datasets" — i.e., treats virtualization and manual incremental loading as the pattern for
  large tables, rather than numbered pagination. (vercel.com/geist/table)
- General web-development consensus (via search synthesis of Material React Table docs and related
  community sources, not an official Material Design page): virtualization becomes worth the
  complexity once client-side rendering of the full row set "starts to feel heavy on scroll,"
  commonly cited around the low thousands of rows, because a virtualized 50,000-row table "costs
  about the same as a 50-row one." This is **not** verified against an official Material Design
  guidelines page — treat the specific row-count thresholds as illustrative, not canonical.
**Tension:** Pagination is simpler to implement, gives users a mental model of "where am I," and
plays well with server-side filtering/sorting; it breaks down for workflows like "scan everything
looking for one thing," where a page boundary is pure friction. Virtual/infinite scroll removes that
friction and scales to huge datasets, but loses the "page X of Y" orientation and complicates
deep-linking to a specific row/position unless deliberately engineered back in.
**Confidence:** medium for the pagination rationale and 20-row starting point (Primer, explicit);
low for the specific virtualization row-count thresholds (no official design-system source fetched —
only community/library documentation).

### ct-tbl-14 — Responsive collapse strategy for wide tables
**Question:** How should a many-column table behave on a narrow viewport?
**Guidance:** Pick from four complementary strategies rather than one silver bullet, and prioritize
which columns survive by product importance, not by the order columns happen to be declared: (1)
freeze/pin the identifying leftmost column(s) so context survives horizontal scroll; (2) let users
explicitly show/hide and reorder columns via a column picker, defaulting to the most important
subset; (3) allow column resize (mainly useful when default widths already don't fit the content —
skip it if the table's spacing is already generous); (4) as a last resort, drop to horizontal scroll
or collapse secondary columns into a "detail" affordance on the row itself.
**Evidence:**
- Primer: responsive strategies include "using column width options, removing less important
  columns, or enabling horizontal scrolling." Column width supports `grow`, `growCollapse`, `auto`,
  or fixed pixel values with `minWidth`/`maxWidth`. (primer.style/design/components/data-table/,
  primer.style/product/components/data-table/guidelines/)
- Pencil & Paper lists the same strategy family with rationale for each: sticky/freeze columns keep
  "the leftmost column... visible during horizontal scroll"; reorder-and-hide gives users "control
  [over] visible columns via dropdown menus"; resize is recommended "when resizable columns are not
  needed because the table has proper spacing by default" (i.e., resize is a fallback, not a first
  choice); and whichever option is used, "prioritize as a product team which columns are the most
  important for the user to see upon page load," persisting the user's chosen view across the
  session. (pencilandpaper.io)
- Shopify's app-home Index Table composition ties this to a `listSlot="primary"`/`"secondary"`
  header attribute specifically for "responsive column collapsing." (shopify.dev/docs/api/app-home/
  patterns/compositions/index-table)
**Tension:** Horizontal scroll is the cheapest to implement but the worst for scanning (you lose the
left-anchor column unless it's pinned). A column picker gives users control and preserves scanning
quality but adds a settings surface and a "why did my columns disappear" support burden if the
default isn't well chosen. None of the fetched sources recommend silently truncating/wrapping cell
content as a primary responsive strategy.
**Confidence:** medium-high (two systems plus one detailed pattern analysis converge on the same
strategy set with matching rationale).

### ct-tbl-15 — Keep header row height consistent with body row height
**Question:** Can the header row use a different height/size than the body rows?
**Guidance:** No — use the same row size token for the header and body. Mixed row heights break the
visual rhythm that makes a dense table scannable (the eye calibrates to one row height and a
different header height reads as misaligned, not as a deliberate hierarchy cue).
**Evidence:**
- IBM Carbon: "Do use the same row height for the table and header rows. Don't mix row heights for
  the table and header rows." (carbondesignsystem.com/components/data-table/usage/, via search
  extraction)
**Tension:** None found — this is a narrow, low-controversy rule; no fetched source recommends
mismatched header/body heights.
**Confidence:** medium (single explicit source, but stated as an unambiguous do/don't rule rather
than a soft suggestion).

### ct-tbl-16 — Scale surrounding chrome (toolbar) to match row density
**Question:** Should the table's toolbar (search/filter/settings bar above the table) be a fixed
size regardless of row density?
**Guidance:** No — pair a taller/more generous toolbar with spacious row sizes and a more compact
toolbar with compact row sizes, so the whole component (not just the rows) communicates one density
level. A tall toolbar sitting on top of an extra-small-row table (or vice versa) undercuts the
density signal the row height was trying to send.
**Evidence:**
- IBM Carbon: "The tall toolbar should only be paired with the large and extra large row heights
  and the small toolbar should only be used with the small and extra small row heights."
  (carbondesignsystem.com/components/data-table/usage/, verified via GitHub carbon-website
  usage.mdx)
**Tension:** None found in fetched sources; this is a coherence rule rather than a contested one,
but it's the kind of detail that's easy to violate when toolbar and table are built/styled by
different teams or components.
**Confidence:** medium (single source, but explicit and specific).

### ct-tbl-17 — Vertical alignment inside multi-line cells
**Question:** Should cell content be vertically centered or top-aligned within the row?
**Guidance:** Center-align content vertically when row heights vary only slightly (roughly up to 2–3
lines) — centering distributes the extra whitespace evenly and looks intentional. Once cells
regularly run 3–4+ lines (long descriptions, wrapped multi-line text), switch to top-alignment so
the first line of every cell lands on the same baseline and the table stays scannable at a glance,
rather than having content "float" at different heights depending on how much each cell wrapped.
**Evidence:**
- Pencil & Paper: "Centering the text vertically within row height spreads out the white space" for
  rows with minimal height variance; "Multi-line cells should stick to the top of the cell to ensure
  everything is visible at first glance" once rows exceed roughly 3–4 lines. It also cites Google
  Sheets negatively as an example of jerky scroll behavior caused by uneven multi-line row handling.
  (pencilandpaper.io)
**Tension:** No counter-evidence found in fetched sources, but this rule is sourced from a single
pattern-analysis article rather than an official design system, so treat the exact line-count
thresholds as approximate.
**Confidence:** low-medium (single source; specific enough to be actionable, but not
cross-verified against a primary design-system doc).

### ct-tbl-18 — Filtering: narrow the row set, don't just highlight
**Question:** What should an inline filter/search box do to the table?
**Guidance:** A table-level filter query should remove non-matching rows entirely (not just
highlight matches in place), so the user's screen fills with only what's relevant to the current
task — the value is reducing what has to be scanned, not just marking it.
**Evidence:**
- Primer: a dedicated filter input lets users "write a query and only show rows that match that
  query," which helps users "focus only on the rows relevant to their task."
  (primer.style/product/components/data-table/guidelines/)
- Pencil & Paper adds a secondary, complementary tactic for search-within-results: "Consider
  highlighting the matches within the rows" — i.e., highlighting is additive to filtering, not a
  replacement for it. (pencilandpaper.io)
**Tension:** None found — the two sources are complementary rather than conflicting (filter to
narrow, then optionally highlight the match inside the narrowed set).
**Confidence:** medium (two aligned sources, one primary design system and one pattern analysis).

---

## Cross-product observations (where systems genuinely diverge)

- **Who controls density.** Primer and Carbon treat density as a *designer* decision baked into a
  given table instance (pick Condensed/Normal/Spacious, or one of five Carbon row sizes, when you
  build the screen). Airtable ships density as an *end-user* preference with no design-time default
  implied beyond "short." Polaris takes a third position: density isn't a table-level knob at all,
  it's a system-wide principle applied per *component type* (index pages and tables get dense
  treatment; pickers and dropdowns don't, regardless of user preference). None of these is "more
  correct" — they map to different product shapes: Airtable's users build wildly different table
  content (images vs. plain text) so a fixed density can't serve everyone; GitHub/Carbon's tables are
  more uniform per surface, so a designer can pick once.

- **How strongly to warn against zebra striping.** No fetched source says "never use zebra
  striping," but they disagree on how much friction to put in front of it. Carbon ships it as a
  low-ceremony opt-in modifier with no visible warning in the component API itself. Pencil & Paper
  treats it as actively risky once rows have interactive/semantic states and effectively argues for
  line dividers as the safer default. Geist exposes a `striped` prop with no published guidance
  either way — a gap, not a position. This looks less like genuine disagreement and more like
  *documentation maturity* varying by system: the ones with more explicit interaction-state
  vocabulary (selected/hover/focus/disabled) are also the ones more likely to flag the collision.

- **Borders as structure vs. borders as noise.** Carbon and Spectrum's "standard" table variant both
  treat visible borders/dividers as a legitimate default structuring tool (light, optional, but
  present). Linear's product-wide redesign narrative explicitly moves in the opposite direction —
  fewer separators, softened contrast, borders used sparingly for elevation instead of shadows — as
  part of a broader "don't compete for attention you haven't earned" philosophy. Spectrum's own
  "quiet" table variant shows the same tension living *inside* one system: use borders when the
  table is the main focus, drop them when it's supplementary. The real variable isn't the product
  category, it's how much the table is competing with other UI for the same screen.

- **Row actions: threshold rule vs. vibe.** Carbon is the only fetched source with a hard, numeric
  threshold (fewer than 3 → inline; 3+ → overflow menu). Every other source describes hover-reveal
  and overflow menus as good patterns without a specific cutoff. This matters in practice — "a few"
  actions is exactly the ambiguous case implementers get wrong, and Carbon's own issue tracker shows
  its own community relitigating the hover-vs-persistent tradeoff even with the threshold rule in
  place, which suggests the threshold resolves *how many* but not *hover vs. always-visible*, and
  that second axis is still genuinely unsettled across the industry.

- **Pagination vs. virtualization is under-documented by design systems themselves.** Of the six
  primary systems investigated, only Primer and Geist say anything concrete about large-dataset
  strategy, and even Primer's guidance (paginate, ~20 rows) is a UX/product argument (avoid
  overwhelming the user) rather than a performance argument. The strongest performance-driven
  virtualization guidance found in this research came from secondary/community sources, not an
  official design-system page — this is a real gap in what's publicly documented, not just a gap in
  this research.

---

## Sources

Primary (design-system documentation, fetched or quoted from live content):
- GitHub Primer — [Guidelines: DataTable](https://primer.style/product/components/data-table/guidelines/)
- GitHub Primer — [Data table (Primer Design)](https://primer.style/design/components/data-table/)
- Shopify Polaris — [Index table pattern (app-home)](https://shopify.dev/docs/api/app-home/patterns/compositions/index-table)
- Shopify Polaris — [Layout → Density](https://polaris-react.shopify.com/design/layout/density) (content via search extraction; direct fetch redirected)
- IBM Carbon — [Data table usage](https://carbondesignsystem.com/components/data-table/usage/) (verified against source at [carbon-website usage.mdx](https://github.com/carbon-design-system/carbon-website/blob/main/src/pages/components/data-table/usage.mdx))
- Adobe Spectrum — [Table](https://spectrum.adobe.com/page/table/) (content via search extraction; direct fetch returned empty/JS-rendered shell)
- Adobe Spectrum Web Components — [Table component docs](https://opensource.adobe.com/spectrum-web-components/components/table/)
- Vercel Geist — [Table](https://vercel.com/geist/table)
- Linear — [How we redesigned the Linear UI (part II)](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Linear — [Behind the latest design refresh](https://linear.app/now/behind-the-latest-design-refresh)
- Airtable Community (official product announcement) — [Row height: control density of records in grid view](https://community.airtable.com/announcements-6/row-height-control-density-of-records-in-grid-view-1618)

Credible independent pattern analysis (used per the brief's allowance for "credible pattern
write-ups," cited explicitly wherever used above):
- Pencil & Paper — [UX Pattern Analysis: Enterprise Data Tables](https://www.pencilandpaper.io/articles/ux-pattern-analysis-enterprise-data-tables)

Secondary / community sources (used only for ct-tbl-13's virtualization thresholds, explicitly
flagged there as low confidence and not attributable to an official design system):
- Material React Table docs and related community discussion, surfaced via search synthesis (no
  single canonical URL fetched directly — see confidence note on ct-tbl-13).

Sources attempted but not usable (JS-rendered pages returned empty/truncated content to WebFetch, or
had no substantive rationale beyond a one-line intro):
- Atlassian Design System — [Table](https://atlassian.design/components/table) (deprecated in favor
  of Dynamic Table; page had no extractable rationale content) and
  [Dynamic table](https://atlassian.design/components/dynamic-table) (intro line only: "A dynamic
  table displays rows of data with built-in pagination, sorting, and re-ordering functionality" —
  not enough to source a decision rule).
- Stripe — no public design-system documentation with table-specific rationale was found; Stripe's
  Sail design system is not publicly documented in a way that could be verified by fetch.
- Notion — no public design-rationale material on table row height/density was found.
