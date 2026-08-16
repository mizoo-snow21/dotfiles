# Labeling, Language & Search

Load when: wording labels/microcopy at the IA level, choosing or auditing terminology and controlled vocabulary, or designing search — whether to add it, and the box, results, filters, query handling, and no-results recovery.

Contents: Label Fundamentals · Consistency & Sourcing Vocabulary · Controlled Vocabulary & Thesaurus Systems · Terminology Form & Classification Structure · Faceted Navigation & Filtering · Deciding On and Designing Search · Search Results, Ranking & Recovery

## Label Fundamentals

### Labels are the clearest signal of your organization scheme
Labels carry the full communicative burden with no chance to clarify in the moment — treat their design and testing with the same rigor as visuals and branding.
- Do: Isolate a page's labels with everything else hidden; check whether the prominent ones read as self-evidently clear.
- Ask: "With everything else hidden, do the prominent labels here read as self-evidently clear?"
⟨ia2-021⟩

### Use visual hierarchy to reduce the semantic burden on header labels
Consistent numbering, font size/weight, color, indentation and spacing let users infer parent/child relationships without maximally-explicit label text. Relax strict treatment for content users already read visually (e.g. a schedule table under a headline).
- Avoid: Expecting a plain, unstyled label to carry the full weight of communicating hierarchy alone.
⟨ia2-025⟩

### Label sequential process steps with consistent verb phrases plus numbering
In multi-step flows (checkout, signup, onboarding), number each step and phrase every step label as an action, so users always know where they started, where they are, and what to do next.
- Avoid: Mixing noun-phrase and verb-phrase step labels within the same flow.
- Ask: "At each step, can the user tell what action they're expected to take right now?"
⟨ia2-026⟩

### Quick reference
- Contextual/in-body link labels are author-written and depend on surrounding prose — test them by asking users to predict a link's destination from context, and coach authors on giving sufficient context rather than mandating exact wording (exception: doesn't apply to centrally-controlled nav labels). ⟨ia2-024⟩

## Consistency & Sourcing Vocabulary

### Eliminate label collisions — no ambiguous overlap, no reused label with two meanings
Audit sibling labels whose boundaries users can't tell apart without clicking (e.g. "Coffee" vs "Coffeehouse" vs "Shop"), and never reuse one label for two different meanings/destinations on the same site.
- Do: Merge/rename/differentiate overlapping siblings; rename one of two same-worded conflicting labels or add disambiguating subtext.
- Trade-off: Disambiguating subtext clarifies meaning but costs screen space.
- Ask: "If I hid the destination pages, could a first-time user correctly guess what's behind each sibling label?"
⟨ia2-022, ia2-028⟩

### Write labels in users' actual vocabulary, not internal jargon — verify accuracy
Source labels from user research, search logs, or customer-facing docs, not internal department/process names; validate via card sorting or first-click testing that each label matches what's actually filed beneath it.
- Do: Add a scope note/description next to any label that could be misread.
- Trade-off: Distinctive/branded labels feel unique vs. plain descriptive labels are more predictable to navigate by.
- Ask: "Would someone outside our organization instantly understand this label, and does it say exactly what they'll find?"
⚖ Tension: correct term vs user's term → tradeoffs-decision-points.md (label-d01)
⟨ia2-023, ia3-035, ia3-044⟩

### Apply the strictest consistency to navigation and product terminology
One term per concept, used with identical wording, styling and placement everywhere it recurs (nav, buttons, help text, emails) — a single inconsistent instance breaks users' sense of familiarity because these labels repeat constantly.
- Do: Draw from established conventional terms (Home, Search, Site Map, Contact, Help/FAQ) where applicable; audit for the same concept named differently elsewhere and unify it.
- Ask: "Is this concept called something different elsewhere in the product?"
⟨ia2-027, uxp1-008, ia3-035⟩

### Design labels as one coherent system: style, grammar, granularity, spelling
Control punctuation/capitalization, grammatical form (verb/noun/question), granularity, comprehensiveness, and singular/plural convention across a whole label set — which specific convention matters less than applying it uniformly.
- Do: Keep granularity comparable across siblings (don't mix "Chinese restaurant" with "restaurant" with "Burger King"); check for conspicuous gaps.
- Ask: "Does this whole label set share one consistent style, grammatical form, granularity, and vocabulary level?"
⟨ia2-032, ia3-021⟩

### Quick reference
- When labels feel unavoidably vague, narrow the scope of the system/sub-site they belong to — a tightly-scoped module supports sharper labels than a broad all-purpose one (exception: genuinely sitewide global nav must stay broad). ⟨ia2-031⟩
- Before redesigning, compile every existing label plus its destination header/title-tag into one audit table, and benchmark comparable/competitor sites for de facto standard terms before inventing new ones (doesn't scale to huge sites — scope the table to a smaller segment). ⟨ia2-033, ia2-034⟩
- Derive labels by reading a content sample and leaning on titles/abstracts (with manual review of any automated extraction), and treat authors' own suggested labels as candidates, not authoritative, since authors lack whole-system indexing perspective. ⟨ia2-036, ia2-037⟩
- For specialized domains, recruit user reps/SMEs who field real questions as a label source, and build a separate plain-language vocabulary in parallel when both expert and lay audiences must be served (e.g. "leg" vs "femur"). ⟨ia2-038⟩
- Combine open card sorting (discover groupings from scratch), closed card sorting (validate a drafted set, asking participants to describe each label first), free listing (3-5 users ranking their own words for an item), and search-log mining (least intrusive) to learn real vocabulary — treat all results as informative, not definitive, since sorting happens outside real product context. ⟨ia2-039, ia2-040, ia2-041⟩
- After gathering any raw candidate-label list, sort alphabetically, dedupe, standardize punctuation/capitalization, check for gaps, and explicitly plan for future content so it doesn't get dumped into a vague "Miscellaneous" catch-all. ⟨ia2-042⟩
- Budget for ongoing label maintenance for as long as the product exists — content and users both keep changing, so schedule recurring search-log analysis and user testing to catch drift. ⟨ia2-043⟩

## Controlled Vocabulary & Thesaurus Systems

### Design controlled-vocabulary UX for infrequent general users, not trained specialists
Don't assume users have professional training in your classification system — today's web audience visits infrequently and can't be told to "learn library science" first. Assume no prior familiarity with preferred terms or classification logic on each visit.
- Exception: A genuinely closed, expert, repeat-use tool (e.g. an internal library-science system) may still hold the older trained-user assumptions.
- Ask: "Are we assuming a level of vocabulary training our actual users don't have?"
⟨ia3-017⟩

### Quick reference
- Tag content with hidden index terms (keywords/metadata) even when not visibly displayed, so search surfaces content lacking the exact query word and users can browse across organizational silos. ⟨ia2-029⟩
- When adopting an existing controlled vocabulary/thesaurus, choose one scoped as narrowly as your actual audience (a domain thesaurus "thinks" like your users) rather than a broad general-purpose one; fall back to other sources if none exists for the domain. ⟨ia2-035⟩
- Match vocabulary-control complexity to the actual problem: a synonym ring for search-recall-only, an authority file for one displayed canonical term, a taxonomy for browsable hierarchy, a full thesaurus only when you need all three together. ⟨ia3-001⟩
- Build a synonym-ring to expand search behind the scenes (near-synonyms, acronyms, misspellings, discontinued/competitor names), but protect precision by ranking exact matches first and offering expansion as opt-in when the literal query returns few/no results. ⚖ Tension: recall vs precision → tradeoffs-decision-points.md (search-d01) ⟨ia3-002, ia3-003, ia3-018⟩
- Build an authority file (one preferred term per concept) whenever the vocabulary must drive browsable structures (index, nav, taxonomy), not just a search box — a synonym ring alone doesn't tell you which single label to display. ⟨ia3-004⟩
- Surface a mapped preferred term visibly in results (not just invisibly matched) so the system both fixes and teaches the correct term; in A-Z browsable indexes add an explicit "X see Y" pointer wherever a variant starts with a different letter, but keep mappings selective — evidence-backed only, since an overlong index hurts everyone. ⟨ia3-005, ia3-006, ia3-007⟩
- Design taxonomies to serve two audiences at once: a visible browsable front-end hierarchy for users and a backend tagging tool for authors/indexers — validate both roles. ⟨ia3-008⟩
- Surface taxonomy categories and subject headings as live clickable pivots alongside search results and on record pages, not inert text — a rich backend thesaurus goes underused if the front end never exposes it as navigable. ⟨ia3-009, ia3-012⟩
- Design the online vocabulary layer to converge many variant user terms down onto one preferred term (the reverse of a print thesaurus) and let correction/mapping happen invisibly — a well-blended thesaurus is one users don't consciously notice. ⟨ia3-010, ia3-011⟩
- Choose thesaurus type by how much control you actually have: classic (controls indexing + search), indexing-only (still pays off via shared indexer guidelines and a browsable preferred-term index), or retrieval-only (right fallback when document-level indexing is impractical — huge volume, syndicated/third-party content, fast-changing news). ⟨ia3-013, ia3-014, ia3-015⟩
- In a retrieval thesaurus, let users explicitly control which relation types expand their query (preferred terms, variants, broader/narrower/related terms) rather than always applying one fixed expansion. ⟨ia3-016⟩
- Base related-item/cross-sell recommendations on defined associative (related-term) relationships in the vocabulary rather than ad hoc rules alone. ⟨ia3-019⟩

## Terminology Form & Classification Structure

### Default preferred terms/facet labels to nouns and spelled-out forms — deviate deliberately
Users recognize and remember nouns more easily than verbs or adjectives, so default to nouns — but use verbs for task-oriented actions and adjectives for attribute-style facets (price, size, color). Default to spelling things out, except when an abbreviation is the dominant real-world usage (TV, IRS, 401K) — then make the abbreviation preferred and map the full form as a variant.
⟨ia3-020, ia3-022⟩

### Disambiguate homographs with parenthetical qualifiers and scope notes
When a term has multiple unrelated meanings, disambiguate each sense with a parenthetical qualifier ("Cell (biology)" vs "Cell (jail)") and attach a scope note pinning down the one intended meaning for indexers — distinct from a dictionary definition. Consider surfacing the scope note to users at search/results time.
- Avoid: Leaving a bare ambiguous term unqualified — users select the wrong sense and get irrelevant results.
⟨ia3-024, ia3-025⟩

### Support users' natural drive to categorize — validate via card sorting, keep categories small
People spontaneously categorize the world; how well information is categorized matters for recall far more than who did the categorizing. Invest as much in category naming as in the grouping. Keep categories to roughly 3-4 items — dumping unclassified information on users overwhelms them.
- Exception: For products aimed at children under ~7, design categorization for the accompanying adults.
- Ask: "Has this IA actually been validated against how target users naturally group these items?"
⟨psy1-049⟩

### Quick reference
- Reserve icon-only labels for small option sets (roughly under 7) or severely space-constrained contexts (mobile), and always test comprehension first — a fitness-tracker study found most users could correctly guess only one or two of seven icons; avoid icon-only for large vocabularies or low-repeat-use audiences. ⟨ia2-030⟩
- Scale compound-term granularity to content volume and site scope: large/broad-scope sites need finer-grained split terms to avoid huge undifferentiated result sets, narrow specialized sites can keep broader compound terms. ⚖ Tension: simple vs precise vocabulary → tradeoffs-decision-points.md (label-d02) ⟨ia3-026⟩
- Allow polyhierarchy/cross-listing under multiple parent categories as content volume grows, rather than forcing a strict single-parent hierarchy; cross-list items that card-sort data shows split between piles, and cluster items with unusually high co-placement rates even across different formal categories (exception: physical objects like a book on a shelf can occupy only one place). ⟨ia3-027, ia3-038⟩
- Switch from a single hierarchy to faceted classification ("how can this be described") when content has multiple independent describable attributes, instead of forcing one placement decision per item. ⟨ia3-028⟩

## Faceted Navigation & Filtering

### Quick reference
- Match each facet's UI control to its data structure: expandable/drill-down for hierarchical facets (e.g. product type → varietals), flat lists/range controls for uniform-valued facets (e.g. price) — don't force one control style onto both. ⟨ia3-029⟩
- Let facet values drive result sorting, not just filtering — including facets pulled from external sources (e.g. critic ratings). ⟨ia3-030⟩
- Deliberately decide which facets/sort options appear on each page, balancing user needs against business needs (e.g. margin) and page context — don't expose every facet everywhere by default. ⟨ia3-031⟩
- Build the underlying facet/metadata structure to be durable and complete, then treat the front-end navigation interface on top of it as the layer you keep testing and revising. ⟨ia3-032⟩

## Deciding On and Designing Search

### Design search for evolving, iterative information needs, not one-shot query→answer
Most real needs are ambiguous and change mid-search as users learn what's available and refine their vocabulary (Bates' "berry-picking" model) — except genuine known-item lookups, which do fit a single-answer model.
- Do: Support reformulating a search after seeing results; preserve context across reformulations; surface related/adjacent content at each step.
- Avoid: Measuring search success purely by time/clicks-to-answer as if one right answer always exists; resetting all context on query edit.
- Ask: "Does this query type actually have one right answer, or are we forcing an evolving need into a one-shot model?"
⟨ia1-008, ia1-011⟩

### Support four distinct information-need types differently
Known-item seeking (spearfishing — exact target), exploratory seeking (lobster trap — a few good results), exhaustive research (drift net — everything, however much effort), and refinding ("the one that got away") each need different support — one generic UI can't serve all four.
- Do: Exact/direct lookup for known-item; open browsing for exploratory; broad synonym coverage + patient paging for exhaustive; save/bookmark/history for refinding.
- Ask: "Which of the four need types is primary here, and does the design actually support it?"
⟨ia1-009⟩

### Integrate search, browse, and ask as one bidirectional discovery system
Users mix modes within a session — design the IA so they move fluidly between them: search results surface relevant browse categories, browse pages offer a scoped search box, self-service escalates to human help.
- Ask: "Can a user who searches move naturally into browsing the found category, and vice versa?"
⟨ia1-010, ia2-091, ia3-036⟩

### Adopt query-enhancement tools based on real user error patterns, not by default
Enable spell-checking, phonetic matching, stemming, NLP, or synonym expansion based on evidence from your own search logs of what errors/variations users actually produce — not every tool solves every problem, and not every engine supports every builder.
⟨ia2-071⟩

### Default to a single, simple search box
Most users expect to type plain descriptive words, not boolean/field syntax — handle stemming, synonyms, and relevance inference behind the scenes. Only add multiple fields when the domain genuinely requires distinct inputs (e.g. travel "From"/"To"), each clearly labeled.
- Exception: Designing specifically for expert audiences (librarians, lawyers, researchers) who will use advanced syntax.
⟨ia2-084, ia2-085⟩

### Implement autocomplete/autosuggest as the primary query-assistance tool
Showing likely matches as the user types — sourced from the search index, controlled vocabulary, or a curated match list — has largely displaced the dedicated advanced-search interface for most users; it works with partial info and signals what the system "knows."
⟨ia2-086⟩

### Quick reference
- Combine search-log analytics (scale, real queries) with contextual inquiry (qualitative, observed behavior) to learn information needs — relying on one method alone misses what the other catches. ⟨ia1-014⟩
- Before adding search, evaluate whether content has outgrown comfortable browsing, is fragmented across silos, would benefit from query-log diagnostics, is expected by web convention, or updates too fast to hand-index — fix underlying navigation problems too, don't use search as a band-aid for it; a site index can be a cheaper alternative. ⟨ia2-063, ia2-064⟩
- Involve IA expertise directly in search-engine selection and configuration, not just IT/platform preference. ⟨ia2-065⟩
- Define narrower search zones (by content type, audience, role, topic, geography, time, author, department) instead of one undifferentiated index pool, for higher precision — but most users ignore zone selectors and only engage after a first disappointing query, so set a sensible default zone with an easy path to broaden. ⟨ia2-066⟩
- Reserve dedicated advanced-search interfaces for the narrow expert audience who needs real structural control (librarians, lawyers, researchers) — but design the default experience so most users never need to visit that page. ⚖ Tension: show options vs hide behind menu → tradeoffs-decision-points.md (forms-d01) ⟨ia2-087⟩

## Search Results, Ranking & Recovery

### Choose result content richness by how confident the user is about what they want
Minimal, symbolic content (title/author only) for users who already know their target and need to scan fast; richer descriptive content (summaries, keywords, snippets) for users still exploring. Add a distinguishing field (edition, format, location) when minimal fields can't tell similar results apart.
⟨ia2-072⟩

### Always show total result count and pagination; balance results-per-page against detail
Match results-per-page to how much info each result shows (fewer if detailed, more if terse); always display the total count and provide clear pagination — but most users only ever look at the first screen regardless of signposting, so front-loading the best results still matters most.
- Trade-off: More results per page (breadth) vs. more detail per result (depth).
⟨ia2-073⟩

### Choose sort vs. rank by the user's task type
Offer sorting (date, alphabetical, specific field) for decision/comparison tasks (e.g. comparing prices); offer ranking (relevance, popularity, rating) for open-ended learning tasks where users trust the top items are most relevant. Pick the field/algorithm by task relevance, not ease of implementation.
⟨ia2-074⟩

### Group/cluster search results into categories instead of one flat list
Once result sets are large enough that best matches risk being buried, group into labeled categories with item counts (topic/audience/product line) — this helps users scan faster and skip irrelevant groups. Hand-curated topical clustering outperforms clustering by raw file-type/date metadata, though it costs more.
- Exception: Result sets small enough that plain sort/rank already surfaces the best matches.
- Ask: "Would grouping these results into categories help users scan them faster?"
⟨ia2-081, uxp1-077⟩

### Make the current search state visible and editable on the results page
Always show the original query terms, visibly and editably, on the results page, and restate what actually happened: search zone/scope, implicit operators, active filters, current sort/rank order — so users can adjust intelligently instead of guessing or retyping from scratch.
- Avoid: Requiring a trip back to a separate search page just to see or edit the query; leaving users to guess what scope/filters were silently applied.
⟨ia2-088, ia2-089⟩

### Adopt a "no dead ends" policy for zero-result and failed searches
Never leave a user at a dead end on a failed search — always offer at least one of: a way to retry/modify the search, tips for improving the query, a browsing alternative, or a way to contact a person.
⟨ia2-090⟩

### Always order results by relevance — diagnose the specific cause when they aren't
Users expect Google-level relevance from every search feature. If results aren't relevant, diagnose: a weak ranking algorithm (invest in proven techniques or a reputable off-the-shelf solution), a bad default filter (e.g. "nearest to me" hiding better/cheaper shippable options — choose defaults for usefulness, let users change them), or business-driven promotion (never do this). Always provide sort/filter controls.
- Trade-off: Short-term business promotion vs. long-term user trust.
- Ask: "Is this result ranked here because it's relevant, or because the business wants it seen?"
⟨uxp1-078⟩

### Quick reference
- Offer "more like this" (pearl growing) — related items, shared-tag browsing, citation links — from a good seed result, instead of forcing a full query reformulation. ⟨ia1-012⟩
- Distinguish destination pages (what users actually want) from navigation pages (homepages, category/index pages) and exclude/deprioritize navigation pages from results — mixing them in dilutes relevant results with an extra unneeded click (exception: test the classification first if it's genuinely unclear for a given page). ⟨ia2-067⟩
- Deliberately decide which structural elements get indexed (exclude boilerplate/disclaimers, include useful fields like author/category) and expose field-level search wherever structured metadata exists, rather than relying only on full-text matching. ⟨ia2-068, ia2-070⟩
- Default news/press/time-sensitive listings to reverse-chronological (newest-first); use straight chronological only for presenting genuinely historical data. ⟨ia2-076⟩
- Treat ranking rules, stopword lists, and manual "best bets"/editor's-choice boosting as first-class IA decisions, not automatic defaults — automatic signals alone can rank a long low-value document above a short more-relevant one on heterogeneous content; use search-log analysis to identify high-value queries worth manual curation (exception: fairly homogeneous content, where automatic ranking works more reliably). ⟨ia1-025, ia2-077⟩
- Popularity-based ranking (PageRank-style) works well for large, richly interlinked, multi-site content pools but poorly within small sites or isolated content silos lacking enough internal/cross-linking for a meaningful signal. ⟨ia2-078⟩
- Rank by user/expert ratings only where a large, motivated base of honest raters exists or can realistically be built — most sites lack the critical mass this approach needs. ⟨ia2-079⟩
- Pay-for-placement ranking suits multi-vendor/marketplace content models — use it deliberately and never disguise paid placement as an organic quality signal. ⟨ia2-080⟩
- Where the next action is unambiguous and low-risk (e.g. installing a free app), let users act directly from the results list, skipping the intermediate destination page. ⟨ia2-082⟩
- In search-heavy repeat-use environments (catalogs/directories), let users save a subset of results and save searches themselves to re-run manually or on a schedule — especially valuable for dynamically-updated content. ⟨ia2-083⟩
- Read search logs for two danger patterns: popular queries returning zero results (distinguish wrong-term-typed — add a synonym/fix nav labels — from genuinely-missing content) and popular queries returning hundreds of results (investigate intent, add a best-bet or better filters). ⟨ia3-039⟩
