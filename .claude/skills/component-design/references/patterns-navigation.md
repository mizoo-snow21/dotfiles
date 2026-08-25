# Pattern Catalog — Navigation

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

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
