# Trade-offs & Decision Points

Load when: two valid principles pull the design in opposite directions and you must pick a side deliberately. Each entry: the competing principles, which context favors which side, the risks of each, and the questions that decide it. Never resolve these by instinct or by silently picking one side — walk the questions.

Contents: Choice, disclosure & visibility (cog-d01/02, forms-d01, nav-d01, act-d01, vh-d01) · Convention vs. differentiation (learn-d01, act-d03, iaorg-d01) · Flow & structure (learn-d02, struct-d01, nav-d02) · Visual: density, depth, type (vh-d02, typo-d01/02/03) · Organization & terminology (iaorg-d02, label-d01/02, search-d01) · Speed, friction, control & responsibility (act-d02/04/05/06/07, behav-d01)

## Choice, disclosure & visibility

### cog-d01 — Minimize the choice set vs. keep large option sets visible via grouping
- **A:** A. When users must evaluate and choose among alternatives, reduce the number of simultaneous options — smaller sets decide faster and convert better (Hick's Law; choice-overload/jam-study evidence shows a 24-item assortment converts far worse than a 6-item one).
- **B:** B. When options are for recognition or navigation rather than comparison, don't force an arbitrary low cap — a persistently visible, well-grouped list stays scannable even with many items, and showing options beats forcing users to recall them from memory.
- **Favor A when:** Product/plan/tier selection and other choice sets requiring active comparison; Points where decision speed or completion rate is the measured concern; Settings or catalogs large enough to overwhelm working memory (holds ~3-4 items for comparison)
- **Favor B when:** Persistently visible navigation menus and toolbars scanned rather than memorized; Dropdowns/autocomplete and other recognition-based value selection; Any list where clear categorization/grouping already keeps it scannable
- **Risk of A:** Over-aggressively cutting or hiding options can remove capability or cues users actually need; Forcing users toward recall instead of recognition when the options could simply stay visible
- **Risk of B:** Presenting many ungrouped, un-chunked options in a task that's actually evaluative (not just navigational) overwhelms working memory and slows decisions
- **Decide by asking:** "Is this a compare-and-decide moment or a scan-and-find moment?" / "If comparison is required, is the set chunked into ~3-4 groups of ~3-4, or just cut with a raw cap?" / "If many items stay visible, are they clearly categorized enough to be recognized rather than recalled?"
⟨laws1-022, laws1-024, psy2-068, laws1-017, laws1-020, psy1-030, psy1-034, psy1-027, laws1-016⟩

### cog-d02 — Progressive disclosure (hide secondary options) vs. recognition-over-recall (keep options visible)
- **A:** A. Default to essential/primary content only; place secondary, advanced, or infrequent options behind an explicit reveal (dropdown, accordion, expandable menu) to reduce upfront clutter and cognitive load.
- **B:** B. Favor recognition over recall — surface the valid option set directly (visible lists, dropdowns) rather than hiding it and requiring the user to remember it exists, what it was, or where to find it, since forgetting is the default outcome.
- **Favor A when:** Feature-dense tools and settings screens with power-user options rarely needed by most users; Long informational content serving both skimmers and deep-divers
- **Favor B when:** Forms/inputs where the user must supply a specific value from a known set; Any point where hiding an option would force the user to recall its existence, name, or location rather than recognize it
- **Risk of A:** Over-simplifying by hiding something users actually need can strip out load-bearing information/cues (e.g. icon-only controls with no labels); A hidden option is easy to forget entirely, since forgetting is the default outcome, not an exception
- **Risk of B:** Showing everything at once reintroduces the clutter and choice overload that progressive disclosure was meant to solve
- **Decide by asking:** "Is this option secondary/infrequent enough to hide, or does hiding it just relocate a recall burden the user can't satisfy?" / "If we hide this, did we remove clutter, or did we remove information/cues the user actually needed?"
⟨laws1-062, uxp1-072, psy1-036, psy1-030, psy1-034, laws1-028⟩

### forms-d01 — Show the full option set directly (recognition) vs. hide it behind a menu, dropdown, or advanced section (progressive disclosure)
- **A:** A. Recognition over recall: show the whole option set on screen (dropdown/list, or the small number of most-used actions placed directly on the page) rather than requiring the user to recall or hunt for it, since knowledge visible on screen is more reliable than knowledge recalled from memory and screen-reader/motor-impaired users are generally better served by controls that are simply present.
- **B:** B. Progressive disclosure: hide long-tail, advanced, or rarely-used options behind a dropdown, popup menu, or an 'advanced settings' toggle to save space and avoid overwhelming the user, especially once the visible option count would exceed roughly 6-7 items (short-term memory capacity) or would clutter a compact/mobile layout.
- **Favor A when:** the option set is small and bounded (a handful of choices); the control is used frequently, or is one of the few most-used actions in a group; screen-reader or motor-impaired users need to reach the option without extra menu navigation; the user might not accurately recall the options unaided (a bounded set they didn't author)
- **Favor B when:** the option count would exceed roughly 6-7 items and start exceeding short-term memory capacity; most users are advanced/power users only rarely, so most never need to see the option; screen space is genuinely scarce (mobile, dense toolbars, compact page layout); a richer picker (grid, calendar, custom layout) is only needed occasionally and shouldn't consume permanent page space
- **Risk of A:** consumes more screen space, which is scarce on mobile and dense layouts; a long flat list of directly-shown options can itself overwhelm short-term memory (~7±2) if the set is large; doesn't scale to genuinely large option sets
- **Risk of B:** reduces discoverability and accessibility relative to controls placed directly on the page, since screen-reader users and users with limited pointer precision are generally better served by on-page controls; adds an extra click/tap and scrolling cost even for a small option set; users may never realize a hidden feature exists at all
- **Decide by asking:** "Is the option set small and bounded enough to show directly without overwhelming short-term memory (~7±2)?" / "Would hiding this control behind a menu meaningfully hurt discoverability or accessibility, given how frequently it's used?" / "Is screen space genuinely scarce enough (mobile, dense toolbar, compact layout) to justify the extra interaction cost of hiding it?" / "Among the options being considered for hiding, are any of them among the few most-used actions that deserve to stay directly visible?"
⟨di4-003, di4-011, di4-019, di4-020, di4-025, uxp1-031, uxp1-032⟩

### nav-d01 — Hide secondary navigation for focus vs. keep primary navigation visible for discoverability
- **A:** A. Hide or tuck away navigation that is secondary, rarely used, or would distract from the task at hand — shrink/bury the long tail of features, suppress full global nav during immersive tasks, and keep dropdown/mega-menu sub-items collapsed until deliberately opened (di2-001, di2-004, di2-013, uxp1-067)
- **B:** B. Keep primary/frequently-needed navigation directly visible rather than hidden behind an icon or extra click — hiding it measurably hurts findability, task difficulty, and completion time, and richer always-visible structure (mega menus, fat footers, second-level category examples) helps users understand what's available (uxp1-067, uxp1-068, ia2-049, ia3-043)
- **Favor A when:** The user is in a focused, immersive task where any navigation option is a distraction (di2-004); The control or item is genuinely rare / power-user-only (Possible tier) rather than something used nearly every session (uxp1-067); The hidden items are still reachable behind a clearly-labeled, always-visible trigger, e.g. a Fat Menu's top-level category label, not an ambiguous icon (di2-013); The main page already handles the ~80% common case; only the rare 20% is being tucked away (di2-001)
- **Favor B when:** The item is Essential — used nearly every session — where hiding it can sink the product (uxp1-067); The context is primary site/app navigation on mobile, where hamburger menus are measured to roughly halve findability (uxp1-068); Users need to understand a category's scope or a site's breadth before committing to a path (ia3-043, ia2-049)
- **Risk of A:** Hiding an Essential interaction causes severe user frustration and can sink a product (uxp1-067); A fully hidden primary nav (hamburger) measurably halves findability and increases task difficulty and completion time (uxp1-068)
- **Risk of B:** Showing full navigation during an immersive task gives the user a ready excuse to abandon it (di2-004); Exposing everything at once clutters the main UI and undermines approachability for most users (uxp1-067); A rich, always-open mega menu adds implementation and accessibility complexity versus a simpler alternative (di2-013)
- **Decide by asking:** "Is this control/nav item Essential (used nearly every session) or Possible (rare/power-user)?" / "Is the user in an immersive, focused task where any nav is a distraction, or in an exploratory browsing mode where discoverability matters?" / "If hidden, is there still a clearly-labeled, always-visible trigger, rather than an ambiguous icon with no label?"
⟨di2-001, di2-004, di2-013, ia2-049, ia3-043, uxp1-067, uxp1-068⟩

### act-d01 — Hiding controls for simplicity vs. keeping them discoverable
- **A:** A: Hide/collapse controls and rely on invisible triggers to keep the UI clean and create visual hierarchy -- context and technology, not a blanket minimalism goal, should decide what's safe to hide.
- **B:** B: Every hidden or invisible trigger needs a learnable discovery path or a visible fallback, since users can't act on what they can't discover, and hidden interactions are undiscoverable to new users by definition.
- **Favor A when:** the trigger is genuinely rare/low-priority and would clutter a high-frequency primary flow if always visible; screen space is scarce and the audience skews toward repeat/expert users who will learn the gesture; showing a conditional control before its precondition is met would be a non-functional distraction
- **Favor B when:** the trigger is high-priority or safety-relevant and cannot afford to go undiscovered; the audience is largely first-time or infrequent users with no way to learn an invisible convention from others; no visible fallback is technically possible only on devices genuinely lacking any screen or control surface
- **Risk of A:** users never learn an action exists because no visible label points to it, especially first-time users; an interface that feels 'empty' or under-featured because too much was hidden by default rather than for a real contextual reason
- **Risk of B:** always-visible controls clutter the UI and reduce the findability of the genuinely important, frequent ones; over-showing dilutes the intended visual hierarchy the same way over-hiding does
- **Decide by asking:** "How would a user with zero prior experience with this app discover this action exists?" / "Is this control being hidden because context/technology genuinely calls for it, or just to look minimal?" / "What tier of usage frequency does this control fall into, and does its visibility match that tier?"
⟨mi1-021, mi1-022, mi1-023, mi1-017, mi1-020, di3-016⟩

### vh-d01 — Progressive step reveal (Responsive Disclosure) vs. show-all-but-disabled (Responsive Enabling)
- **A:** A. Progressively reveal only the current step's controls, letting the interface grow as the user completes each step (Responsive Disclosure).
- **B:** B. Show most of the UI up front but disable what isn't usable yet, enabling pieces as steps are completed (Responsive Enabling).
- **Favor A when:** the task branches and later steps depend heavily on an earlier choice; a dense wall of interlinked controls shown all at once would be overwhelming for a rarely-performed, complex task; users benefit from watching the interface grow to build a mental model
- **Favor B when:** overall interface stability matters more than a dynamically growing/re-laying-out screen; the always-visible-but-disabled layout doesn't look ugly or stressful and there's enough space for it; possibly novice users benefit from seeing the full eventual set of controls up front
- **Risk of A:** reveals a step's controls only to yank them away again once branching makes them irrelevant, if the branch logic isn't decided up front
- **Risk of B:** over-disabling things 'to be helpful' when they don't actually need to be disabled; mystery-meat disabled controls with no visible reason or nearby way to enable them
- **Decide by asking:** "Does interface stability matter more here than letting the user watch the interface grow?" / "Would the always-visible-but-disabled version look ugly or stressful, or is there too little space for it?" / "Does the task branch such that later steps' relevance depends on an earlier choice?"
⟨di2-039, di2-040⟩

## Convention vs. differentiation

### learn-d01 — Convention/familiarity vs. deliberate departure from convention
- **A:** A. Match established conventions and idioms so users can transfer prior experience and skip relearning basic structure (Jakob's Law) — reuse conventional placement/behavior for standard components rather than inventing novel patterns without a strong reason.
- **B:** B. Deliberately depart from convention, or try a genuinely different structural pattern, when the current approach underperforms or a specific UX improvement / meaningful differentiation goal exists — but validate the departure with real users before shipping broadly.
- **Favor A when:** common, well-understood interactions (navigation, search placement, forms, page structure) where users bring experience from other products; no evidence that the current/standard approach is underperforming
- **Favor B when:** the chosen structural pattern is not working as well as hoped, and a known alternative pattern solves the same underlying problem differently; a specific UX improvement or meaningful differentiation goal exists, and it can be validated with users
- **Risk of A:** staying with a chosen pattern that is underperforming instead of considering a known alternative that addresses the same problem differently
- **Risk of B:** a deviation that seems clearer to the design team can still be unlearnable for users who bring different expectations, if it is not tested before shipping
- **Decide by asking:** "Is there an established convention for this pattern, and if so, why are we deviating from it?" / "If we removed this deviation from convention, would users lose anything, or just look more generic?" / "Have we tested whether users understand this non-standard pattern, or are we assuming they will?" / "Is there a known alternative pattern that solves this same structural problem differently?"
⟨laws1-001, laws1-003, laws1-004, di1-003⟩

### act-d03 — Preserving established convention vs. investing in a differentiated signature moment
- **A:** A: Only break a well-established, widely-understood interaction when the replacement is obviously, visibly better -- difference should be a byproduct of genuine improvement, never a goal pursued for its own sake.
- **B:** B: Pursuing a 'signature moment' -- a microinteraction so well-crafted it becomes a standout, differentiating feature -- is a legitimate strategy, achieved through disciplined restraint on a narrow, focused interaction rather than expanding its scope.
- **Favor A when:** the interaction is high-frequency, deeply habituated, and users' mental model of it has years of reinforcement behind it (e.g. Save/Save As); the change would touch a core, load-bearing workflow rather than a peripheral, low-stakes moment
- **Favor B when:** the interaction is a good candidate for a memorable, narrowly-scoped moment specifically chosen as the product's differentiator (not embedded deep in a gating flow like login); the market has converged on feature parity, so overall 'feel' from small interactions is what actually drives loyalty and purchase decisions
- **Risk of A:** over-indexing on convention forecloses genuinely valuable innovation and differentiation opportunities
- **Risk of B:** a redesigned interaction that is merely different, not obviously better, provokes sustained user backlash, as with Apple's 'Save As' redesign replacing one simple rule set with several confusing ones across OS versions; expanding a microinteraction's scope in pursuit of impressiveness works against the restraint a genuine signature moment requires
- **Decide by asking:** "Is the new/differentiated behavior obviously, visibly better to the user, or just different?" / "Is this interaction a deliberately chosen focal point for differentiation, or an incidental part of a core, habituated workflow?" / "Can we achieve distinctiveness through disciplined restraint on a narrow scope, rather than by breaking an established convention?"
⟨mi1-030, mi1-008, mi1-009, mi1-010, mi1-011⟩

### iaorg-d01 — Cross-channel IA: keep semantic structure consistent vs. match each channel's dominant need
- **A:** A. Keep the underlying semantic structure (category meanings, labels, logic) consistent across every channel a user might use, adapting only the concrete layout and capabilities per channel — coherence requires both fit to context and the same underlying logic held across media.
- **B:** B. Don't force the primary/flagship channel's organizing scheme onto a different channel with fundamentally different dominant user needs — pick the structure that matches that channel's actual dominant use case, even when it means using a different top-level organizing principle.
- **Favor A when:** Designing a product or service available across desktop, mobile, phone support, or other channels serving essentially the same predominant task (e.g. a bank, retailer, or service with app + web + phone/voice touchpoints); Users move between channels expecting to recognize the same categories and terms
- **Favor B when:** An organization operates multiple channels or products where the actual predominant user task differs fundamentally between channels (e.g. a physical theme park organized by themed 'Lands' vs. its website, whose primary users mostly haven't visited yet and want to book a vacation, so the site uses a travel/hospitality structure instead); The flagship channel's organizing metaphor doesn't match what most users of a secondary channel are actually trying to do
- **Risk of A:** Forcing identical structure onto a channel whose users have a fundamentally different dominant need creates friction, since the shared structure doesn't map to what that channel's users actually came to do
- **Risk of B:** Letting each channel invent its own independent categorization or vocabulary for the same content breaks cross-channel familiarity and forces users to relearn the structure each time they switch channels
- **Decide by asking:** "Do our channels serve essentially the same predominant user task, or fundamentally different ones?" / "If we let this channel's structure diverge from the others, are we doing it because its actual dominant user need is different — or just because it's convenient?" / "Where structures diverge, can we still keep brand and naming consistent so users have some anchor across channels?"
⟨ia1-002, ia1-021⟩

## Flow & structure

### learn-d02 — Guided/constrained simplicity vs. open/dense efficiency
- **A:** A. Constrain and guide the interface (wizard-like) to minimize learning investment for infrequent, one-off, or low-motivation users.
- **B:** B. Keep the interface open, dense, and efficiency-oriented for users who use it daily and are motivated to invest in learning it.
- **Favor A when:** most users will remain permanent novices or infrequent users with minimal per-use learning time
- **Favor B when:** most users will grow into intermediate/advanced users through frequent, motivated use
- **Risk of A:** too little openness leaves users feeling boxed in and frustrated
- **Risk of B:** too much openness leaves under-prepared users lost about what to do next
- **Decide by asking:** "Will most users become intermediate-to-advanced, or stay permanent beginners with minimal per-use time?" / "Does this product need to serve both a first-time/casual user and a frequent, intermediate-to-advanced user at once, requiring a layered approach rather than picking one extreme?"
⟨di1-005, di1-006⟩

### struct-d01 — Guided sequential flow (Wizard) vs. random-access editor (Settings Editor) for structuring a multi-step or multi-field task
- **A:** A. Guide the user step by step through a fixed, predetermined sequence (Wizard) when the task is long/complex/unfamiliar and the designer can be assumed to know the best path.
- **B:** B. Give the user random access to view and change settings/properties in whatever order they want (Settings Editor) when users need to find and edit individual items rather than follow a fixed sequence.
- **Favor A when:** The task is long or complex and typically unfamiliar to the user (e.g. software installation).; The designer can reasonably be assumed to know the best path better than the user does.; The task has branching or many linear steps where earlier decisions affect later options.
- **Favor B when:** The context is app-wide/system-wide settings, an account/profile editor, a free-form authoring tool's document/object properties, or a product configurator.; Users need to confirm current settings at a glance, not just change them.; The task is creative or exploratory (writing, art, programming), or the user is actively trying to learn the underlying tool.
- **Risk of A:** Constrains power users, creative users, and users trying to learn the tool, who find the fixed sequence frustrating.; Never reveals what the user's choices actually did to the underlying state, so users don't understand the result.; Used reflexively for every multi-field task, it becomes pointless overhead when a single short form would work as well.; Some cultures find wizards paternalistic or condescending.
- **Risk of B:** Without a fixed sequence, a task with genuine step dependencies (where earlier decisions constrain later options) gives the user no guidance through that dependency chain.; Burying a commonly needed setting behind an overly deep hierarchy (three-plus levels) can require dozens of clicks to reach it.
- **Decide by asking:** "Does this task have a fixed dependency order where earlier choices constrain later options, or does the user need random access to view/change individual items independently?" / "Is the user unfamiliar with the domain and better served by being guided, or a power/creative user who wants visibility into and control over the underlying state?" / "Could this multi-field task be reduced to a single short form instead of either a wizard or a settings-style page?"
⟨di1-030, di1-031⟩

### nav-d02 — Add cross-links for flatter access vs. preserve a perceivable hierarchy
- **A:** A. Provide multiple, cross-cutting access paths to the same content — search, browse, index, sitemap, cross-links, and rich dropdown/footer menus — so content is reachable quickly from wherever the user enters, effectively turning a multi-level site into a fully-connected one (ia3-033, ia2-053, di2-013, di2-014)
- **B:** B. Keep the underlying hierarchy structurally perceivable — don't let unlimited horizontal/vertical shortcuts, or too many stacked navigation layers, obscure how areas relate to each other or crowd out the actual content (ia2-046, ia2-047, ia2-048)
- **Favor A when:** Users arrive via search, social links, or deep links with no context from the top-level hierarchy and need direct routes in (ia2-053, ia3-033); Users already know the name of what they want and don't need or want to learn the hierarchy; The site is large with many categories, where casual browsers benefit from seeing more of what's available at once (di2-013)
- **Favor B when:** The site's value depends on users building an accurate mental model of how sections relate (ia2-046); Global, local, and contextual navigation are already competing for the same limited screen space (ia2-047); A purely tree-structured, up/down-only navigation would be too limiting, but the opposite extreme — unrestricted jump-anywhere hypertext — is explicitly called out as equally bad (ia2-046)
- **Risk of A:** Unlimited cross-links let users bypass the hierarchy entirely from anywhere, producing the disorientation of 'an Escher building with no exit' (ia2-046); Combined/stacked navigation layers crowd out the actual page content (ia2-047); A dynamic mega menu adds real implementation and accessibility overhead versus a static alternative (di2-013)
- **Risk of B:** A purely hierarchical, strictly up/down navigation is too limiting for large or complex sites (ia2-046); Without supplementary/cross-cutting paths, a meaningful share of users and tasks are not well served by the primary hierarchy alone (ia2-053)
- **Decide by asking:** "Does adding this shortcut or cross-link still leave the underlying hierarchy perceivable, or does it let users bypass structure entirely from anywhere?" / "Have global, local, and contextual navigation been reviewed together as one system, or only each in isolation?" / "Would a cheaper, static option (e.g. a footer sitemap) achieve enough of the benefit without a dynamic mega menu's added complexity?"
⟨ia2-046, ia2-047, ia2-048, ia3-033, ia2-053, di2-013, di2-014⟩

### nav-d03 — More, simpler steps (lower per-step cognitive load) vs. fewer page jumps (lower re-orientation cost)
- **A:** A. Break a complex decision into several simple, logical steps — cognitive load costs more than motor load, and users tolerate clicks that each deliver logical progress.
- **B:** B. Keep the ~80% most common task on one page with no context switch — every page/window jump forces re-orientation and compounds load time; shrink or progressively disclose in place before moving content to another page.
- **Favor A when:** each collapsed-together step would demand noticeably more thinking; the decision has real branching; users are unfamiliar with the domain.
- **Favor B when:** the task is frequent/habitual for its user; the "steps" are really one decision split cosmetically; in-place disclosure (tabs, accordion, inline expansion) can absorb the complexity without a jump.
- **Risk of A:** each extra jump re-orients and slows a task the user runs daily; wizard overhead on what one short form could do.
- **Risk of B:** one dense page raises per-step cognitive load exactly where A warns; primary flow buried in options.
- **Decide by asking:** "Is the split lowering thinking per step, or just adding jumps?" / "Can in-place disclosure deliver A's simplicity without B's jump cost?" / "How often does THIS user run this task?"
⟨psy1-037, psy1-038, di2-001⟩

## Visual: density, depth, type

### vh-d02 — Generous whitespace as default vs. deliberate information density
- **A:** A. Start with generous, even excessive whitespace and only remove it until the layout looks right — space almost always reads as cleaner and more polished.
- **B:** B. Some contexts genuinely benefit from a more compact/dense layout that prioritizes showing a lot of information at once.
- **Favor A when:** general content pages, marketing pages, most application screens where breathing room and perceived quality matter
- **Favor B when:** information-dense views like dashboards or data-heavy tables where users need a lot of information visible at once for at-a-glance comparison; continuous-monitoring dashboards (live business/ops data) where users must scan and act on a lot of information at a glance with minimal scrolling
- **Risk of A:** forcing unnecessary scrolling or paging in contexts where users actually need to compare a lot of data at a glance
- **Risk of B:** compactness happening by default/neglect rather than by deliberate intent — density is a much less obvious mistake to notice than under-spacing, since removing space when needed is an obvious signal but realizing more space was needed is not; without aggressive curation, high density degrades into marginal data competing for attention so users can't identify what matters
- **Decide by asking:** "Is this layout dense because the content genuinely needs to be, or because I never gave it enough space?"
⟨rui1-026, rui1-027, di1-028, di4-050⟩

### typo-d03 — Depth and separation technique: deliberate decorative richness vs. flat minimalism
- **A:** A: Use deliberate decorative depth/separation techniques -- simulate a consistent overhead light source for raised/inset elements, use hairlines and borders (matched to a prominent font) as a refined visual motif -- to create a polished, dimensional look.
- **B:** B: Minimize these techniques in favor of flatter, quieter treatments -- convey depth via relative lightness/darkness or blur-free offset shadows instead of realistic light simulation, and prefer box-shadow/background-color contrast/spacing over borders for separating elements.
- **Favor A when:** designs aiming for a tactile, dimensional, or classic/refined feel; skeuomorphic or richly-styled visual directions; elements needing strong emphasis on their raised/inset physical state; a font-forward design where a matching border reinforces the typography
- **Favor B when:** flat/minimalist visual directions; designs that already feel busy or cluttered, where borders would add noise; interfaces prioritizing clarity and quiet backgrounds over ornamentation
- **Risk of A:** overdone light-simulation or excessive/inconsistent borders read as busy, dated, or amateurish if not tuned carefully or applied consistently
- **Risk of B:** excessive flatness can lose meaningful visual separation and hierarchy cues if lightness contrast alone isn't deployed deliberately
- **Decide by asking:** "Does this design's overall direction call for tactile/dimensional richness, or quiet flatness?" / "Before adding a border here, have I tried box-shadow, background-color contrast, or extra spacing instead?" / "If depth is needed, will a fully realistic light-simulated shadow serve better here, or would a flat lightness-contrast treatment fit the rest of the design better?"
⟨rui1-065, rui1-066, rui1-067, di4-061, di4-062, rui1-093, rui1-074⟩

### typo-d01 — Line length: reading speed vs. reader preference/comfort
- **A:** A: Longer lines (~80-100 characters) deliver measurably faster reading because each line-wrap forces an eye-movement interruption, and long lines have fewer interruptions per amount of text.
- **B:** B: Shorter-to-medium lines (~45-75 characters / 10-12 words) are what readers say they prefer, choose when given the option, and are the default recommendation for paragraph/body text.
- **Favor A when:** urgent reference/news content; content where information-delivery speed is the priority; content the user must scan/process quickly
- **Favor B when:** feature stories or content meant to be lingered over and enjoyed; general body/paragraph text where reader comfort and engagement matter more than raw speed; any default paragraph styling absent a specific speed requirement
- **Risk of A:** users report lower satisfaction/comfort even though they read faster; may feel harder to engage with
- **Risk of B:** slower objective reading speed despite user preference -- a mismatch between what users say they want and what performs best
- **Decide by asking:** "Does this content need to be read quickly (reference/urgent), or is reader engagement/comfort the priority?" / "Am I defaulting to a line length because of stated preference research, or because raw speed is genuinely the goal here?"
⟨psy1-025, rui1-045, di4-048⟩

### typo-d02 — Serif vs. sans-serif for small on-screen body text
- **A:** A: Prefer sans-serif over serif for small on-screen text because screen pixel rendering has historically struggled to render fine serif details cleanly at small sizes (a few screen-optimized serif fonts like Georgia are exceptions).
- **B:** B: Research shows no meaningful difference in reading speed, accuracy, or preference between serif and sans-serif; choose typefaces for brand tone/personality instead of a legibility difference that isn't actually supported by evidence.
- **Favor A when:** legacy or low-resolution/low-DPI displays; an unverified or thin/delicate serif face used at very small point sizes
- **Favor B when:** modern high-DPI screens; a serif face specifically designed/hinted for screen use (e.g. Georgia); any typeface whose letterforms are already confirmed clearly identifiable at the target size
- **Risk of A:** needlessly restricts typeface choice and brand expression based on a rendering assumption that may be outdated for the actual target devices
- **Risk of B:** on genuinely low-resolution or small-pixel-density contexts, an unverified serif face can still degrade legibility in practice
- **Decide by asking:** "What is the actual rendering context (display resolution, point size) this text will appear in?" / "Has this specific typeface been verified legible at the target size and resolution, or is the sans-serif default just a safety assumption?"
⟨di4-048, psy1-021⟩

## Organization & terminology at scale

### iaorg-d02 — Broad-and-shallow hierarchy vs. deep, faceted/compound categorization at scale
- **A:** A. Favor broad-and-shallow hierarchies with page-level grouping over narrow-and-deep structures — minimize clicks to reach content, and defer to user-testing rather than a fixed magic number of options per level.
- **B:** B. For large-scale or highly varied content, use deep, specific faceted or compound categorization (multiple simultaneous classification dimensions) rather than flattening everything into a shallow hierarchy.
- **Favor A when:** General-purpose sites/apps where most users navigate top-down through a small number of categories; Content sets not large or varied enough to need multi-dimensional filtering
- **Favor B when:** Content sets large or varied enough that no single shallow hierarchy can represent every way users might want to slice it
- **Risk of A:** A shallow hierarchy may force users into an artificial single-path categorization when their real need is multi-dimensional (e.g. filtering by several facets at once) — a risk this cluster's own supporting record (ia2-011) does not directly address
- **Risk of B:** Deep or highly specific faceted structures can reintroduce the click-depth and complexity costs that broad-shallow hierarchies were chosen to avoid, if not paired with strong page-level grouping and information scent
- **Decide by asking:** "Is this content set large/varied enough that a single shallow hierarchy can't represent every way users want to find things, or does a broad-shallow structure with good page-level grouping already serve most users?" / "If faceted/compound categorization is needed, is it layered on top of a broad-shallow backbone, or does it replace the backbone entirely?"
- Related: label-d02
⟨ia2-011, ia3-026⟩

### label-d02 — Simple, minimal vocabulary/category structure vs. deep, precise, multi-dimensional categorization at scale
- **A:** A: Keep the vocabulary and category structure as simple and minimal as the problem requires — the simplest controlled-vocabulary structure that solves the actual problem, with categories kept small (roughly 3-4 items) so users aren't overwhelmed.
- **B:** B: As content volume and site scope grow, categorization must go deeper and more precise — finer-grained compound terms, polyhierarchy/cross-listing across multiple parent categories, and faceted classification across several independent dimensions — to keep result sets manageable and content properly differentiated.
- **Favor A when:** The specific search/browse problem is narrow (e.g., only search recall for known synonyms) so a lighter structure (synonym ring or authority file) fully solves it.; Content volume is small enough that broad, undifferentiated categories don't overwhelm users.; Overly granular categories risk dumping too many top-level choices on users at once.
- **Favor B when:** The site is broad-scope and high-volume, so under-decomposed compound terms would return huge undifferentiated result sets.; Content or products have multiple independent describable attributes that a single hierarchy can't capture.; Content volume is large enough that a strict single-parent hierarchy forces awkward placement decisions for items that legitimately belong in more than one category.
- **Risk of A:** A broad-scope, high-volume site with an under-decomposed vocabulary returns thousands of undifferentiated results per term.; Forcing single-parent categorization on inherently multi-attribute or high-volume content strands items that belong in more than one place.
- **Risk of B:** Building a full thesaurus or deeply faceted, polyhierarchical structure when a simpler tool (synonym ring, authority file) would have solved the actual UX problem adds unnecessary implementation and maintenance cost.; Too many fine-grained categories or facets can overwhelm users past the small-category comfort threshold.
- **Decide by asking:** "What specific search/browse problem are we solving, and what is the lightest structure that solves it?" / "Given our current and expected content volume, would a compound/broad term return a manageable, well-differentiated result set?" / "Does this content have more than one independent describable dimension, or could most items reasonably live under a single category?"
- Related: iaorg-d02
⟨ia3-001, psy1-049, ia3-026, ia3-027, ia3-038, ia3-028⟩

### label-d01 — Technically/industry-correct terminology vs. the majority user's own term ('user warrant')
- **A:** A: Choose the preferred term for linguistic/documentary validity — the technically or industry-correct term — especially when the goal includes educating users on correct terminology or when the preferred term also serves as the literal index/query vocabulary with no variant terms shown.
- **B:** B: Choose the preferred term for 'user warrant' — the term that serves the majority of actual users' real search/comprehension needs — favoring plain, jargon-free, audience-native vocabulary over technically correct labels.
- **Favor A when:** The goal explicitly includes teaching users the correct/industry term (e.g., a healthcare or technical domain where accuracy matters).; The preferred term doubles as the actual index/query vocabulary with no variant terms surfaced, so precision of the term itself matters more.
- **Favor B when:** The audience is general/lay and infrequent, not trained specialists.; Internal or industry jargon would be understood only by a small fraction of users and signals prioritizing the organization's own vocabulary over customers' needs.; The site serves both expert and lay/general audiences with genuinely divergent vocabularies for the same content.
- **Risk of A:** Labels understood only by trained professionals or insiders depress comprehension and conversion for general users.; Forcing one 'correct' vocabulary on both expert and lay audiences underserves whichever group doesn't use that vocabulary.
- **Risk of B:** Optimizing purely for majority current usage forgoes any opportunity to teach users more precise/correct terminology.; A term chosen solely for popularity may be linguistically inconsistent with the vocabulary's structure or with authoritative sources.
- **Decide by asking:** "Is our goal to maximize raw findability, to teach users correct/industry terminology, or both — and does that change which term should be preferred?" / "Does the preferred term double as the literal index/query vocabulary with no variant terms shown?" / "Does our audience include both specialists and lay users with genuinely different vocabularies — if so, should we build two parallel labeling systems instead of picking one term?"
⟨ia3-023, ia2-038, ia2-023⟩

### search-d01 — Tune search for recall or for precision
- **A:** Favor recall: return most/all relevant documents, accepting irrelevant ones, using strong stemming and broad matching
- **B:** Favor precision: return fewer but more reliably relevant documents, using weak/no stemming and narrower matching
- **Favor A when:** Exhaustive research, legal, or scientific tasks where missing a relevant document is costly; Learning-oriented or 'vanity search' tasks where the user wants comprehensive coverage even at the cost of noise
- **Favor B when:** Quick, specific-answer tasks where the user wants one reliable result; Users who will be frustrated by irrelevant noise in the result set
- **Risk of A:** Irrelevant documents get included alongside relevant ones (more noise) as recall/stemming strength increases
- **Risk of B:** Relevant documents get missed, including word-variant or tangential matches, as precision/narrower matching increases
- **Decide by asking:** "What is the dominant user information-seeking goal for this domain: completeness or a fast, reliable answer?" / "Should stemming be strong (favor recall) or weak/none (favor precision) for this content and audience?"
⟨ia2-069⟩

## Speed, friction, control & responsibility

### act-d02 — Instant/optimistic feedback vs. deliberate friction for trust and error prevention
- **A:** A: Respond as fast as possible -- target sub-0.4-second responses, and use optimistic UI to show success immediately for near-certain actions, since speed keeps attention and productivity at their peak.
- **B:** B: Not all delay is bad -- a confirmation step or a deliberately lengthened, explained process engages more careful thinking, reduces error and regret, and can increase confidence that a check was actually done thoroughly.
- **Favor A when:** the action has a very high success rate and low stakes if it occasionally fails (e.g. posting a comment); the task is one the user expects to feel instant, and speed itself signals quality
- **Favor B when:** the action is high-stakes or irreversible, where a moment of deliberate friction reduces costly error or regret; the process is one users expect to take real time (e.g. a security or privacy scan) -- finishing suspiciously fast can itself breed distrust that the work was actually done, or the change can be missed entirely if it happens too quickly to register
- **Risk of A:** a response faster than the apparent complexity of the task warrants can undermine confidence that the system actually did the work, and very fast automatic changes can go unnoticed entirely; if an optimistic UI's rare failure isn't surfaced afterward, users lose data or trust without realizing it
- **Risk of B:** unnecessary friction on a low-stakes, high-success action slows the product down for no real benefit and frustrates users expecting speed
- **Decide by asking:** "Does this action have a high enough success rate and low enough stakes to show optimistic feedback safely?" / "Is this a process users expect to take visible time, where finishing too fast would undermine their trust that it was done properly?" / "If we add friction here, can we explain to the user what it's actually checking?"
⟨laws1-070, laws1-071, laws1-072⟩

### act-d04 — Reducing choices and degrees of freedom vs. preserving user control through reversibility and safe exploration
- **A:** A: Minimize offered choices, replace them with smart defaults, and reduce the user's degrees of freedom wherever possible (poka-yoke) so that mistakes and unnecessary decisions are structurally prevented rather than merely handled.
- **B:** B: Users need genuine freedom to explore, try unfamiliar actions, and change their minds at low or no cost -- provide multi-level undo, safe exploration, command history, and grace-period recall for destructive actions, since taking away control removes the safety net that makes exploration and correction possible.
- **Favor A when:** the choice or degree of freedom in question doesn't change outcomes for most users, or exists mainly to accommodate rare edge cases; an entire category of error can be made structurally impossible without meaningfully limiting what users can accomplish
- **Favor B when:** the interaction is genuinely exploratory or creative, where trying, checking the result, and reversing is core to how users work; an action is destructive, hard-to-reverse, or one where mistakes are costly enough that a safety net matters more than a decision saved
- **Risk of A:** over-reducing choice or control can remove options and flexibility users genuinely relied on, or leave no path to correct a system-picked outcome the user disagrees with
- **Risk of B:** preserving too much optionality/reversibility infrastructure (deep undo stacks, many exposed choices) adds complexity, more rules, and more decisions for users to make in the first place
- **Decide by asking:** "Would removing this choice or degree of freedom change outcomes for real users, or only for a rare edge case?" / "Is this a domain where users need to explore and revise, or one where a single smart default genuinely serves everyone?" / "If we reduce control here, is there still a reliable way to reverse or correct the system's choice?"
⟨mi1-044, mi1-057, di1-007, di3-026, uxp1-054, di3-027⟩

### behav-d01 — Removing friction/stopping cues to maximize engagement vs. preserving user control and wellbeing
- **A:** A: Removing friction and stopping cues (one-tap repeat actions, autoplay-next, infinite scroll, variable-ratio reward schedules) reliably maximizes habitual repetition, dwell time, and engagement metrics.
- **B:** B: Every removed friction point and stopping cue is a removed user decision point — protective/deliberate friction (error prevention, security, moderation, favoring long-term outcomes over short-term gains) is a legitimate design tool, not a defect to eliminate.
- **Favor A when:** The habitual action being encouraged is genuinely in the user's interest, not just the business's (e.g. a helpful one-tap reorder of something the user actually wants repeated).; The business has a real, non-manipulative need to reduce steps or friction in a repeat action.
- **Favor B when:** The action carries risk of harm, compulsion, or long-term regret if left unchecked.; The design already relies on variable/unpredictable rewards — the most habit-forming reinforcement pattern of any schedule.; The friction serves error prevention, security, deliberate moderation, or protecting a long-term outcome over a short-term one.
- **Risk of A:** Compulsive, habitual behavior detached from actual user benefit.; Removing all stopping cues eliminates the moments a user would naturally decide to stop, maximizing passive consumption or ad exposure at the expense of user control.
- **Risk of B:** Added friction reduces conversion or habit formation if applied indiscriminately.; Friction without a genuine protective purpose is just a usability defect, not a virtue.
- **Decide by asking:** "Is encouraging habitual repetition of this action actually good for the user, or only good for the business?" / "Does this design remove the user's natural stopping point, and is that actually in their interest?" / "Is removing this friction actually good for the user, or just good for a conversion metric?" / "Is this reward pattern serving the user's goal, or primarily maximizing how often they check it?"
⟨laws1-076, laws1-078, laws1-082, laws1-075⟩

### act-d05 — Tuning detection sensitivity: catching more real events vs. fewer false alarms
- **A:** A: Bias a detection/alerting/validation system toward higher sensitivity so it catches more real events, accepting more false alarms, when missed detections are the more costly outcome.
- **B:** B: Bias the same system toward lower sensitivity so it produces fewer false alarms, accepting more missed detections, when false alarms themselves cause real harm (needless anxiety, wasted follow-up procedures, alert fatigue).
- **Favor A when:** a missed detection is catastrophic or irreversible (e.g. air-traffic control, security threats); the rare-but-critical event in question is exactly the kind users' built-in expectations make them likely to miss without an unmistakable, high-salience signal
- **Favor B when:** false alarms carry a real cost of their own -- needless anxiety, wasted follow-up action, or habituation that causes users to tune out and eventually miss the alerts that matter (e.g. diagnostic screening)
- **Risk of A:** over-sensitive detection trains users to distrust or ignore alerts through sheer frequency of false positives, defeating the alert's purpose over time
- **Risk of B:** under-sensitive detection lets real, costly events slip through specifically because they're rare and therefore already under-attended to by users
- **Decide by asking:** "For this specific system, is a missed detection or a false alarm the more costly outcome?" / "Does the current sensitivity setting actually reflect that judgment, or was it left at a default?"
⟨psy1-061, psy1-055⟩

### act-d06 — Trusting the measured statistic vs. overriding it with contextual/practical judgment
- **A:** A: Trust rigorously collected quantitative data (proper sample sizes, geometric-mean task times, slip-vs-mistake coding) as the most reliable signal of whether a microinteraction change actually helped, since intuition alone can't detect the small effect sizes typical of microinteraction changes.
- **B:** B: Data doesn't design the product for you -- a statistically notable result may not be practically meaningful, and a human still has to interpret a number in its real-world category context before acting on it.
- **Favor A when:** the sample size is adequate (the book recommends at least ~20 testers) and the metric is a well-understood one like completion rate or task time; the question at hand is whether a real, replicable difference exists at all between two versions
- **Favor B when:** the raw number, taken alone, contradicts known category norms (e.g. a 0.5% click-through rate looks alarmingly low in isolation but is actually a healthy rate for online ads); the decision requires judging whether a statistically real difference is large enough to matter for the product
- **Risk of A:** treating every measured number as actionable without contextualizing it risks 'fixing' or removing something that was actually performing normally for its category
- **Risk of B:** disregarding data too readily, or substituting personal intuition for measurement, forfeits the main advantage quantitative testing offers for detecting small microinteraction effects
- **Decide by asking:** "Is this result statistically meaningful given our sample size and metric choice?" / "Separately, does it actually matter practically for a feature of this kind and category?"
⟨mi2-057⟩

### act-d07 — Auto-terminating loops for security/resource conservation vs. avoiding interruption annoyance
- **A:** A: End an operation or session automatically after inactivity or elapsed time (e.g. auto-logout, resource-conserving timeouts) to protect security or conserve system resources.
- **B:** B: Automatic termination risks becoming an annoying, unwanted interruption -- weigh the real benefit against the cost of cutting off a user who may still need the state preserved.
- **Favor A when:** the session holds sensitive data (e.g. banking) where an unattended, still-open session is a real security exposure; the resource being conserved (battery, server connection) has a real, ongoing cost while idle
- **Favor B when:** users often pause mid-task for legitimate reasons (reading, interruption) and would lose meaningful unsaved progress if cut off; the security or resource benefit is marginal relative to how disruptive the interruption is
- **Risk of A:** users lose unsaved work or get frustrated by premature auto-termination, especially if the timeout doesn't match real usage patterns
- **Risk of B:** skipping auto-termination in a genuinely sensitive context leaves a real security or resource-cost exposure unaddressed
- **Decide by asking:** "Does the security or resource benefit of auto-terminating this state actually outweigh the interruption it causes for how this feature is really used?"
⟨mi2-037⟩
