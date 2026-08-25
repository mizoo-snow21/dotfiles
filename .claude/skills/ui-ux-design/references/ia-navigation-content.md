# Information Architecture, Navigation & Content Structure

Load when: deciding how to organize content, choosing a hierarchy or navigation scheme, designing wayfinding (breadcrumbs, menus, entry points), or modeling/linking content.

Contents: IA Foundations & Process · Organization Schemes · Hierarchy Structure & Depth · Content Modeling & Contextual Linking · Sitemaps & Wireframes · Navigation Systems · Wayfinding & Orientation

## IA Foundations & Process

### Settle IA before sketching the interface
Work out what objects users see, how they're categorized, and how users act on them before the first wireframe — visual commitment locks in structure prematurely, especially for new products needing flexibility.
⟨di1-023⟩

### Findability precedes usability
Solve whether content can be found at all before polishing its in-page usability — findability is a separate, prior problem.
⟨ia3-037⟩

### Ground every "it depends" IA decision in users, content, context
Decompose ambiguous IA questions into three factors — users, content, context — and gather direct evidence for each; no two information ecologies are alike, so another project's or competitor's answer doesn't transfer.
⟨ia1-004⟩

### Run a content-property checklist before choosing an organization scheme
Before proposing a scheme, characterize the content set's ownership, format, structure, metadata, volume, and dynamism — these six properties shape what's even feasible.
⟨ia1-005⟩

### Observe real information-seeking behavior instead of guessing
Determine actual users, tasks, and needs through real-world observation, not brainstorming/focus groups alone — needs vary hugely by urgency, patience, and domain vs. system familiarity.
⟨ia1-007⟩

### Pair every organization scheme with a content-ownership policy
Findability and organizational manageability are goals to balance together — an easy-to-browse structure with no clear content owner will decay.
⟨ia1-006⟩

### Design a concrete feature before deciding the app shell
Pick one real feature and design its functional elements before deciding nav/shell/layout — shell decisions (top nav vs. sidebar, width, logo placement) can't be made confidently with no real content to inform them.
⟨rui1-001⟩

### Ship the smallest useful version in short cycles, not full upfront speculation
Design a simple version of the next feature, build it, iterate on the real thing, then move on — don't resolve every edge case in the abstract, or bake unbuilt "nice-to-have" functionality into the current pass.
⟨rui1-005, rui1-006⟩

### Quick reference
- Ask what larger system an artifact belongs to before designing it, and periodically re-check the accumulated whole still coheres (bricklayer vs. cathedral-builder). ⟨ia1-003⟩
- Write design principles that are specific and opinionated, taking a side on a real trade-off; chain each to the law that justifies it and a checkable rule — vague platitudes settle nothing. ⟨laws1-073, laws1-074⟩

## Organization Schemes

### Match scheme to whether users know what they want
Use an exact/objective scheme (alphabetical, chronological, geographical) for known-item search; use an ambiguous/subjective scheme (topic, task, audience, hybrid) when users are browsing or don't yet know what they want; combine both where feasible.
- Do: invest more testing time in ambiguous schemes — higher design risk, usually higher value.
⚖ Tension: recall vs precision → tradeoffs-decision-points.md (search-d01)
⟨ia2-001⟩

### Leverage established category typology for recognizability
For a well-established category (bank, airline, hospital, university), align the base structure with what users already expect from that category; deviate only in small, deliberate ways for brand differentiation.
⚖ Tension: convention vs departure → tradeoffs-decision-points.md (learn-d01)
⟨ia1-016⟩

### Keep hybrid organization schemes shallow, not deep
Mixing schemes (topic/task/audience/alphabetical) is fine at a shallow layer like the homepage; don't let a deep hierarchy interleave schemes at every level — users lose the single logic that predicts the next item.
- Do: keep each scheme visually/spatially separated, not interleaved into one list.
⟨ia2-009⟩

### Layer hypertext links and free tagging on a designed hierarchy — never as its replacement
Build the hierarchy/database structure first as the primary system; use hypertext links and user tagging (folksonomies, hashtags) only as a supplementary layer. Purely tag-driven organization has failed at scale; heavy hypertext-only linking disorients users who lose their place.
⟨ia2-014, ia2-015⟩

### Segment heterogeneous content into similar clusters before choosing a structure
Don't force one uniform structure across content of wildly different granularity/format (articles vs. journals vs. databases; text vs. video vs. tools). Segment into similar clusters first, then pick hierarchy / database model / hypertext-tagging per cluster.
⟨ia2-016, ia2-018⟩

### Validate ambiguous labels and category boundaries with real users
Ordinary words carry multiple meanings and abstract topics resist clean categorization ("pitch" has a dozen meanings) — this ambiguity is structural, not a design failure. Test how real users interpret a label/boundary before finalizing it.
⚖ Tension: correct term vs user's term → tradeoffs-decision-points.md (label-d01)
⟨ia2-017⟩

### Organize around how users think, never the org chart
Don't mirror internal team/department structure or your own mental model in navigation — organize around how target users classify and label content, validated through research. Provide multiple paths since no single scheme satisfies everyone.
⟨ia2-019⟩

### Quick reference
- Use alphabetical order as a default for reference-style content (directories, glossaries), or layer it under another grouping — don't rely on it alone for content users can't name precisely. ⟨ia2-002⟩
- Organize chronologically when date is the primary context (press releases, archives, schedules), paired with topic/search for users who don't care about the date. ⟨ia2-003⟩
- Organize geographically when location is intrinsic (locators, local news); auto-detect location where possible; contested borders add complexity. ⟨ia2-004⟩
- Define a topic scheme's full intended coverage up front, including future topics, so growth doesn't force a redesign or a "Miscellaneous" dump. ⟨ia2-005⟩
- Reserve task-based organization for a few clear, high-priority tasks — embed it in nav rather than forcing a whole large site into task structure. ⟨ia2-006⟩
- Split IA by audience only when segments are clearly distinct; decide open (cross-browsable) vs. closed deliberately, and revisit the audience model periodically. ⟨ia2-007⟩
- Don't build a site's primary organization around a real-world metaphor unless it's universally familiar and can flex as functionality grows — elaborate spatial metaphors (town/library) have broken under real use and forced redesigns. ⟨ia2-008, ia3-042⟩
- Treat metaphor exploration in concept work as ideation, not a mandatory final structure — most explored metaphors should be discarded, not built. ⟨ia3-041⟩
- Apply a database/relational model (metadata-tagged records) to homogeneous structured subsites (catalogs, directories) for auto-indexes, field search, and related links; build a deep per-department vocabulary, not one shallow sitewide vocabulary. ⟨ia2-013⟩
- When a product accumulates new content/access types, reconcile each addition's classification scheme with the existing one before exposing them through shared search/browse. ⟨ia1-001⟩
- Don't copy a competitor's IA pattern just because they're prestigious — evaluate the specific pattern on its own merits; market success isn't evidence the IA is good. ⟨ia3-040⟩

## Hierarchy Structure & Depth

### Design deliberate structural and verbal cues for sense of place
Choose nav labels, headings, and content patterns that unambiguously signal what kind of "place" this is and what's possible there — users read digital environments the way they read physical ones.
⟨ia1-015⟩

### Treat top-level navigation as structural, not cosmetic
Reserve top-level nav slots only for genuinely top-tier concepts — they define conceptual boundaries and signal relative importance of everything beneath; cluttering them with unequal items dilutes the hierarchy signal.
⟨ia1-017⟩

### Keep semantic structure stable; decouple parts that change at different rates
Keep top-level nav, labels, and category meanings stable across visual redesigns unless there's a validated reason — semantic structure changes far slower than visual design. Don't broaden labels "to be safe"; decouple independently-evolving parts instead (e.g. subdomains).
⟨ia1-019, ia1-020⟩

### Keep categories mutually exclusive by default; cross-list only genuinely ambiguous items
Allow deliberate cross-listing (polyhierarchy) for content that truly belongs in more than one place, but stop before it becomes so common it erodes the hierarchy's value.
⚖ Tension: cross-links vs clean hierarchy → tradeoffs-decision-points.md (nav-d02)
⟨ia2-010⟩

### Favor broad-and-shallow over narrow-and-deep — but group options visually
Narrow-deep forces many clicks and raises abandonment; broad-shallow gives faster access but can overwhelm if options aren't grouped. The real constraint on link count is scannability, not a fixed "7±2" — user-test the specific design.
⚖ Tension: minimize choices vs grouped visibility → tradeoffs-decision-points.md (cog-d01)
⟨ia2-011⟩

### Absorb growth at the second hierarchy level, not the homepage
Favor broad-shallow top-level structure and add new categories at level two — the homepage is usually the most tested and costly-to-change surface, so reserve room there rather than planning to keep expanding it.
⟨ia2-012⟩

## Content Modeling & Contextual Linking

### Define content-chunk boundaries as the smallest independently-meaningful unit
A content chunk isn't automatically a sentence, paragraph, or page — it's the finest piece that should be handled independently. Chunking is a subjective call.
- Ask: "Does this need smaller user-accessible chunks? What's the smallest section worth indexing on its own? Should it be reusable across documents?"
⟨ia3-065, ia3-067⟩

### Preserve a content model's required parts and their order
Keep all required fields present and in the order users expect (e.g. a recipe's ingredients before its steps) — dummy filler text alone doesn't break recognizability, but reordering or dropping a required component does.
⟨ia3-068⟩

### Pull important contextual links out of body text into a dedicated visible area
Add contextual (editorially chosen) links after the core architecture is set, sparingly, in a dedicated visible section for links that matter to the business/user goal (cross-sell, up-sell); keep inline body-text links for low-importance reference only — users skim past hyperlinks.
- Avoid: burying commercially important links only inline, or overloading the page with contextual links.
⟨ia2-051⟩

### Quick reference
- Specify content-embedded IA elements (headings, embedded links/metadata, chunk order, sequence indicators) in the template spec, not left to individual authors' discretion. ⟨ia1-029⟩
- Give cross-cutting content (seasonal, thematic) one canonical home, linked from related sections, rather than scattering duplicate copies for local discoverability. ⟨ia3-046⟩
- Use a shared page template only for content with a genuinely repeated structure (a consistent feed, or text sharing one document type) — don't force free-form text into one generic template. ⟨ia3-048⟩
- Separate content from its container (chunk-level mapping + database-driven CMS) so one update to a reused chunk (e.g. contact info) propagates everywhere instead of being hardcoded per page. ⟨ia3-066⟩
- Design content models to surface contextual, need-based navigation (e.g. cross-selling a matching item) at the point of relevance, rather than relying on users to rediscover it via the top-down hierarchy. ⟨ia3-069⟩
- Build a formal, automated content-linking model only at volume (large, similar, unlinked content) — link small counts by hand. Match on a unique ID when available; else combine attributes when a single field (e.g. name) collides on duplicates. ⟨ia3-070, ia3-071⟩
- Maintain a governing IA style guide (so day-to-day content additions don't erode organization/navigation/labeling) and a pattern library of reusable solutions to cut re-solving cost. ⟨ia3-072, ia3-073⟩

## Sitemaps & Wireframes

### IA diagrams show content structure, not semantic meaning
Judge any sitemap/wireframe by whether it clearly shows the content units and how they connect — don't expect it to convey semantic meaning or label rationale. Pair with a content model or controlled vocabulary when semantic precision matters.
⟨ia3-049, ia3-050⟩

### Choose sitemap vs. wireframe by which question you're answering
Sitemap: where content lives and how it's navigated. Wireframe: how one page/template should look and be organized architecturally. Pick based on which question is actually on the table.
⟨ia3-054⟩

### In a wireframe's fixed space, deliberately choose which architecture earns space over content
A wireframe's space is limited — explicitly decide which architectural elements (nav, chrome) must be visible vs. deferred; over-represented architecture crowds out the content the page exists to show.
⚖ Tension: whitespace vs density → tradeoffs-decision-points.md (vh-d02)
⟨ia3-055⟩

### Use position and font weight to signal content priority in wireframes
Communicate relative content priority through visual weight — prominent placement and larger heading fonts for higher-priority groups — independent of final visual design.
⟨ia3-056⟩

### Match wireframe fidelity to project stage and audience
Favor rough, low-fidelity sketches early, increasing precision as the design matures; most working wireframes sit between the two extremes.
⟨ia3-061⟩

### Treat low-fidelity artifacts as fast, disposable exploration — defer detail, don't polish
Keep content approximate and defer typeface/shadow/icon/copy decisions; emphasize layout and placement. Use them to explore and decide quickly, then leave them behind — don't keep polishing after the decision is made.
- Avoid: finalizing fine styling before layout is settled, or treating early wireframe copy as final.
- Exception: when the content wording itself is the thing under review.
⟨ia3-062, rui1-002, rui1-004⟩

### Build hierarchy in grayscale before introducing color
When refining a layout in higher fidelity, work in grayscale first — let spacing, contrast, and size alone create hierarchy — then layer color on afterward, rather than letting color paper over a structurally weak hierarchy.
⟨rui1-003⟩

### Quick reference
- Use a high-level sitemap, built top-down from the main page, to settle the major organizing scheme — not for navigation/page-level detail (use a detailed sitemap for that); the same format can represent bottom-up content-model relationships. ⟨ia3-051⟩
- For transaction/task-centric systems, map the user's step-by-step path (a task-oriented sitemap/process map) to surface UX opportunities a content sitemap would miss. ⟨ia3-052⟩
- In a detailed sitemap, diagram content chunks as elements separate from their page container (grouped by relatedness), not fixed to one page layout before it's decided. ⟨ia3-053⟩
- Wireframe only the most important, complex, unusual, or template-setting pages — skip pages that just apply an established template. ⟨ia3-057⟩
- Produce parallel wireframes per screen size whenever a page's structure genuinely changes across mobile/tablet/desktop. ⟨ia3-058⟩
- State up front that a wireframe's fonts/colors/whitespace are placeholders, not final design; settle decisions designers don't want to make (e.g. label wording), leave open the ones they do (color, placement). ⟨ia3-059, ia3-060⟩
- Combine content + layout + navigation in a medium-fidelity wireframe and reuse it repeatedly as the main cross-role IA discussion artifact. ⟨ia3-063⟩
- Weigh high-fidelity wireframe benefits (stakeholder engagement, real width/font testing, paper-prototype testing) against cost/time and the risk of shifting focus to visual design before the IA is mature. ⟨ia3-064⟩

## Navigation Systems

### Choose a navigation model that matches the content's actual structure
Pick hub-and-spoke, fully-connected, multi-level, stepwise/pyramid, pan-and-zoom, or flat navigation to fit how content actually connects — decide before its visual form, and mix models locally rather than forcing one everywhere.
⟨di2-003⟩

### Follow placement conventions for global vs. utility navigation
Place global nav top and/or left by default (strong convention); go right only with a fully liquid layout. Reserve top-right for a compact logged-in utility cluster (account, help, logout, cart, notifications), reused for login when signed out; keep search nearby.
⟨di2-005, di2-015⟩

### Give first-time users a small set of clear, task-based entry points
Show a few prominent entry points with plain-language labels and a clear call to action instead of exposing full complexity at once — size the count to what the design can bear, and offer an opt-out for returning/expert users.
- Exception: not needed when most users are already intermediate/advanced, or the product's purpose is already obvious.
⚖ Tension: guided simplicity vs open efficiency → tradeoffs-decision-points.md (learn-d02)
⟨di2-007⟩

### Give sequential content both a parent hub and back/forward/up links (Pyramid)
For content viewed in order (slideshow, wizard, chapters), give every item page back/forward links plus an explicit up-link to a parent hub listing all items — back-only navigation forces repeated clicking to escape a deep sequence.
- Exception: looping the last item to the first can work when exact sequence position doesn't matter to the user.
⟨di2-009⟩

### Reserve modal panels for genuinely blocking situations
Block all navigation with a modal only when the user truly cannot proceed (required input, must-acknowledge message, required login). Limit exits to 1-3 options, include a close control, return users to where they were, and prefer a web overlay over an OS-level dialog.
- Avoid: using modals for low-priority, optional input — use inline or deferred input instead.
⟨di2-010⟩

### Design global, local, and contextual navigation as one coordinated system
Design the three layers together, not in isolation — they compete for the same screen space and can overwhelm users if combined thoughtlessly. Deliberately decide whether global nav includes search and structural/location hints.
⟨ia2-047, ia2-048⟩

### Choose text vs. icon nav labels based on available space
Prefer text on desktop web, where space is abundant and text is clear/accessible; prefer icons only in space-constrained contexts like mobile, and validate comprehension before shipping icon-only nav.
⟨ia2-052⟩

### Provide multiple, parallel access paths to the same content
Never rely on a single path — offer browse, search, and an index/sitemap together. A well-designed hierarchy alone reliably fails a meaningful share of users/tasks; treat supplementary navigation as real design work, not a nice-to-have.
⟨ia2-053, ia3-033⟩

### Show second-level category examples to strengthen top-level comprehension
Pair a top-level label with a few representative second-level items so users can correctly infer scope — bare labels alone measurably hurt comprehension (information scent).
⟨ia3-043⟩

### Make the primary access affordance visually dominant over secondary ones
When one element is the primary means to a page's core task (e.g. a search box), place it prominently and design secondary/alternative elements (e.g. a map) so they don't pull attention away.
⟨ia3-047⟩

### Classify every control as Essential, Easy, or Possible
Essential (near-every session): prominent, never hidden. Easy (frequent): discoverable one level down. Possible (rare/power-user): tucked away but findable. Classify early; iterate with real user testing.
- Avoid: hiding an Essential control, or cluttering the main UI with rare Possible-tier options.
⚖ Tension: hiding controls vs discoverability → tradeoffs-decision-points.md (act-d01)
⟨uxp1-067⟩

### Avoid the hamburger menu; keep primary navigation visible
Hiding primary nav behind a hamburger roughly halves findability and increases completion time. Prefer bottom nav (4-5 items), top tabs, or a short left-aligned list; never use one on desktop; if unavoidable, add a "Menu" text label.
- Exception: many low-priority "Possible"-tier mobile features may genuinely need one as a last resort.
⚖ Tension: hidden vs visible nav → tradeoffs-decision-points.md (nav-d01)
⟨uxp1-068⟩

### Quick reference
- Don't surface full global navigation during an immersive task (e.g. full-screen slideshow) — offer only back/forward plus an escape hatch. ⟨di2-004⟩
- Dedicate a Menu Page (full-page link list with enough context per link) when visitors already know what they want — keep promotional content off it; skip when the site needs to hook visitors first. ⟨di2-008⟩
- Encode an app's full interactive state (position, filters, zoom, mode) into a shareable, restorable URL, updated live, so reloading reproduces exactly what was viewed; decide which parameters are worth preserving. ⟨di2-011⟩
- Use a rich mega/fat dropdown menu (imagery + typographic hierarchy, not a plain link list) to expose deep structure (3+ levels) without extra clicks — verify screen-reader support, or fall back to a static sitemap footer. ⟨di2-013, ia2-049⟩
- Give every page a full-width footer sitemap (desktop) or bottom nav list (mobile, below the fold) as a static, cheaper, accessible complement to the header nav — verify with usability data that users actually reach it. ⟨di2-014, ia2-049, di4-034⟩
- For large multi-department portals, design a distinct "which subsite" step separate from within-subsite search/browse — they typically need different IA. ⟨ia1-013⟩
- Let local navigation diverge between sub-site areas only when the content genuinely needs it — not because decentralized teams designed independently without coordination. ⟨ia2-050⟩
- Use a site map (top 2-3 levels only) for large hierarchical sites; skip it for small 2-3-level sites — it also helps SEO crawling. ⟨ia2-054⟩
- Provide a flat alphabetical site index for known-item search; scope granularity from search-log/user research, and rotate multi-word terms only when a real user would plausibly search either order. ⟨ia2-055, ia2-056⟩
- Keep guided tours short, exitable anytime, with consistent controls, one question per step, zoomed-in screenshots, and a TOC beyond 2-3 pages — most users skip guides entirely, so treat them as optional, not core. ⟨ia2-057⟩
- Let configurators/wizards move linearly, skip ahead, or go back freely; keep global nav visible; show the consequence of each choice (e.g. a live product preview). ⟨ia2-058⟩
- Deploy algorithmic personalization only for narrow, well-bounded needs (e.g. tracking one stock) atop solid structure. Offer manual customization mainly where users return often and are motivated to invest setup time (e.g. intranets) — most visitors won't bother. ⟨ia2-059, ia2-060⟩
- Use visual/graphical navigation (image grids) only where users recognize the result on sight (physical products) — avoid metaphor-driven "virtual space" or animated sitemap visualizations, which have proven more novel than useful. ⟨ia2-061⟩
- Layer social navigation signals (voting, social-graph feeds) on top of a stable shared global structure — don't let social personalization narrow exposure so much that shared orientation is lost. ⟨ia2-062⟩
- Visually separate a subsite's local navigation from its host portal's global navigation — don't co-locate them in one shared nav frame, or users can't tell which links leave the topic area. ⟨ia3-045⟩
- Inside a mobile app, hand off directly to native apps/features (phone, maps, calendar, mail, browser, media) for data that belongs to them, prefilled with current context, instead of making users retype or switch manually. ⟨di4-040⟩

## Wayfinding & Orientation

### Treat every page/window jump as a real cost
Design the ~80% most common task to complete on one page, no context switch — each jump forces re-orientation and compounds load time. Shrink a control (fewer options, shorter labels, icons) before moving it to another page; use progressive disclosure (tabs, accordion) instead.
- Exception: burying the rare ~20% of tasks an extra jump away is fine if it keeps the primary flow simple — usability-test when unsure.
- ⚖ Tension: pulls against preferring more, simpler steps to cut cognitive load (cognition-mental-models.md) → nav-d03
⟨di2-001⟩

### Mark every decision point with a clear sign
At every point a user must decide where to go, provide a clear, unambiguous label, and put a strong call to action on the first page. Don't assume environmental/cultural cues (an X in a corner) will be universally recognized.
⟨di2-002⟩

### Always provide an Escape Hatch from restricted navigation
On any restricted-navigation screen (wizards, modals, pages reached with no context like via search), always provide an explicit, unmistakable link back to a known safe location — a guaranteed exit reduces the feeling of being trapped, like an undo.
- Exception: not needed if the page already has a Sequence Map or Breadcrumbs that let users navigate back.
⟨di2-012⟩

### Show Breadcrumbs to reveal hierarchical position
On any page 2+ levels deep, show the full parent chain as a clickable trail of real page titles — shows where you are, not how you clicked here. Valuable when landing deep via search with no context. Prefer over a custom back button, which can conflict with the browser's own.
- Avoid: treating breadcrumbs as showing what to do next (that's a Sequence Map's job), or dropping them purely as a trend.
- Exception: not always necessary on mobile — evaluate case by case.
⟨di2-017, uxp1-063⟩

### Animate transitions that could otherwise disorient the user
When a change risks disorienting the user (zoom, pan, rotate, panel toggle, page jump), animate briefly instead of snapping. Keep transitions fast (under a second, ~300ms for scrolling), animate only the affected region, and collapse rapid repeated actions into one.
- Avoid: animating the whole window when only part changed, or overusing motion until it slows users down.
⟨di2-019⟩

### Design IA both top-down (structure first) and bottom-up (content self-orients)
Check top-level structure against orientation questions (where am I / find X / browse / notable / what can I do / contact / account). Many users arrive via search or social links, bypassing top nav — structure each page (chunking, sequencing, metadata) to answer "where am I / what next" on its own.
⟨ia1-022, ia1-023⟩

### Run the navigation stress test: parachute into a deep page with no context
Ignore the homepage and drop onto random deep pages; check whether each page alone tells the user where they are, what the parent section is, and where nearby links lead. Surfaces bottom-up orientation gaps homepage-only testing misses.
⟨ia1-024, ia2-045⟩

### Always make current location and identity visible, however the user arrived
Every page must show which site/app the user is in and where they are in the hierarchy, regardless of entry point. Use progress indicators, breadcrumbs, or save-state indicators for journeys; give hierarchy levels a distinct visual identity (e.g. home vs. settings).
⟨ia2-044, ia3-034, uxp1-062⟩

### Always confirm when a journey or task has finished
For every journey, however small (even a settings change), signal start, in-progress, and — critically — completion explicitly ("changes saved," "message sent"). Never leave users guessing whether an action took effect.
- Avoid: requiring a separate Apply-then-Save step, or relying on window-close-to-save behavior the user doesn't know about.
⟨uxp1-061⟩

### Make optional journeys and steps skippable
Wherever a journey or step isn't strictly required (classic case: onboarding for users who aren't new), make it skippable. Never trap users in a required flow with no exit but completion.
⟨uxp1-064⟩

### Quick reference
- Show a compact Sequence Map (with "you are here") for linear flows near the back/forward controls — prefer breadcrumbs instead for large hierarchical (non-linear) navigation. ⟨di2-016⟩
- Overlay orientation cues directly on the scrollbar (static markers for stable info, dynamic tooltips for changing info, search-result markers when active) so cues sit where attention already is while scrolling. ⟨di2-018⟩
- Don't add a "back to top" button — mobile browsers already offer a tap-status-bar shortcut; repeat main navigation (and consider search) in the footer instead so the bottom of the page isn't a dead end. ⟨uxp1-069⟩
