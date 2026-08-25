# Component Boundaries & Identity

This file guides decisions about where one component ends and another begins: whether two elements are truly the same component despite looking different (or different components despite looking alike), when a local solution deserves promotion to a shared pattern, and how tightly a system should enforce genericity versus preserve deliberate variation. Route here when defining a new component's boundary, auditing a UI for near-duplicate patterns, deciding whether to unify or split similar-looking elements, or judging how modular, strict, or specific a component system should be.

## Contents
- The Identity Test
- Drawing Boundaries
- Shared vs Local & Promotion
- Diagnosing Near-Duplicates
- Scope Axes: Modular/Integrated, Strict/Loose, Specificity
- Over-Abstraction Guards

## The Identity Test

### Same-component test: identity is the behavioral contract, not the visual form `BND-002`
Two things that look alike are not necessarily the same component, and one thing that looks different in different places may still be the same component: identity is the behavior a component embodies and the interaction contract it fulfills, not its visual shape, medium, or surface traits. Strip away styling and ask what structure and behavior remain — that is the true identity, and it should transfer even to a non-visual expression such as a screen-reader announcement. When: two elements look visually similar and it's unclear whether they're the same component; one element must appear in different visual forms across contexts; naming a new component before its visual design is settled.
Do: strip the presentation/CSS and ask what plain structure and behavior remain; define semantic role, behavioral contract, and who owns/drives the component before committing to visual form; check whether the behavior would still make sense in a different sensory expression.
Ask: If I strip the CSS, what plain structure and behavior remain? Is this actually the same underlying data/interaction, or just a visual resemblance? (AD ch2; DS ch1; DI ch1; IC ch1,3)

### Functional vs cognitive patterns: a stylistic variant is a skin, not a new component `BND-041`
Interface patterns split into functional patterns (concrete, executable parts tied to action/behavior — an interface "object") and cognitive/perceptual patterns (style/expression layered onto that object, not a separate object in its own right). A purely stylistic variation — color, font, spacing — should not be treated as requiring a new functional component; route it to styling the shared object instead. Which functional patterns a product needs is shaped by its domain and the specific actions it must support, not assumed universal across products. (DS ch1)

### Full ARIA menu semantics belong only to genuinely application-like option selection `BND-003`
A "true" ARIA menu (role=menu/menuitem with full desktop-application keyboard semantics) should only be used where a control genuinely imitates desktop-application option selection. When it doesn't, a hybrid outcome — e.g. a navigation reveal-list using only aria-expanded — is the correct final design, not an incomplete implementation; the right amount of semantic machinery follows from the control's actual identity, not a drive to fully implement the most elaborate applicable pattern.
Do: reserve full ARIA menu semantics for controls that genuinely emulate desktop-application menu conventions; accept a simpler hybrid when the real identity is navigation.
Ask: Does this control genuinely need to imitate desktop-application menu conventions, or does a simpler pattern already fit? (IC ch1)

### Tooltip vs toggletip are distinct components; interactive content escalates further `BND-004`
"Tooltip" commonly names two behaviorally distinct patterns: true tooltips (transient, hover/focus-revealed) and toggletips (persistently toggled by explicit click/tap, with a trigger that exists only to reveal information). A toggletip's trigger is not a conventional two-state toggle button despite looking like one, because its real state model is "shown / re-shown," not on/off. If disclosed content needs its own interactive controls (close/confirm/links), the requirement has outgrown tooltip/toggletip and calls for a menu or dialog instead.
Do: choose true tooltip vs toggletip by whether the interaction should be transient or explicit and persistent; give a toggletip trigger no purpose besides revealing information; reach for a menu or dialog when interactive content is genuinely needed.
Ask: Does this control actually have two meaningful states to toggle, or does clicking it just mean "show/re-show this information"? (IC ch1)

### Assert precisely which show/hide paradigm is in play `BND-005`
Tabs, accordions, table-of-contents links, and SPA view-switching all superficially "show/hide content" but carry different user expectations and must not be blurred: SPA view-switching is closer to navigation and must not be presented as tabs; in-page Module Tabs (content swap within one page) differ from tabs used for page-to-page navigation even when visually identical. Conversely, visual styling alone does not create a new component — a single-column list is still a Grid of Equals parameterized by column count, and suppressing a list's bullet marker doesn't remove its list semantics or non-visual value (item-count announcement, navigation shortcuts). When: content will grow past roughly four sections, prefer an accordion over tabs.
Ask: Does clicking this tab load a new page/document, or does it swap visible content within the current page? Does this single-column list use the same per-item template as a multi-column grid would? (DI ch1; IC ch1,2)

### A modal dialog is defined by mode-change, not shape `BND-006`
A modal dialog's defining property is that it changes the interface's mode and disables the rest of the interface — not its floating position, box shape, or close button. A floating panel that doesn't disable the rest of the UI (e.g. a draggable tool palette) is not a dialog even if it looks like one; there is never a need for a non-modal "dialog" — it should become a true modal (if it needs urgent input) or a notification (if purely informational). A genuine dialog should solicit a real decision, not just display a message, and its content should be short enough to act on without its own scroll region; long/complex content belongs on its own page, and low-importance supplementary input should stay inline rather than escalate to a Modal Panel.
Do: mark up and behave as a true modal only when the mode genuinely needs to change and the rest of the UI should disable; route purely informational content to a notification instead; keep low-importance supplementary input inline near the triggering action; use a native method like confirm() where it suffices, and if building a custom dialog, benchmark its focus, dismissal, and isolation behavior against confirm()'s accessibility contract. Trade-off: inline supplementary input guarantees the user can keep working but risks the input being abandoned/forgotten; a Modal Panel guarantees the input is captured immediately at the cost of blocking all other navigation.
Ask: Does this element change the interface's mode and disable the rest of the interface while shown? Does this message truly need to block the interface, or is it just informing the user of something already done? (DI ch1; IC ch3)

### Button vs link is a behavior distinction the team must define and apply consistently `BND-043`
The traditional distinction — a link navigates elsewhere, a button triggers an action on the current interface — is genuinely ambiguous in practice, and different teams and design systems legitimately draw the line differently (even major systems disagree). There is no universally correct definition, but whichever one a team chooses must be agreed on, documented, and applied consistently across the whole interface, because consistent expression of purpose — including to screen-reader users — matters more than which specific line is drawn. An alternative framing sidesteps the ambiguity: split Links from CTAs instead of buttons from links, then decide per CTA whether it's a button (keeps the user on the page) or a link (navigates away) as a scoped variation, not the top-level category split. When: a link visually styled as a standalone call-to-action is fine as long as the convention is used consistently interface-wide.
Do: agree on and document the team's own button/link definition explicitly; keep the chosen definition applied consistently across the whole interface.
Ask: Does this control keep the user on the current content, or take them elsewhere? Does the whole interface apply this rule consistently, or mix conventions unpredictably? (DS ch3)

### Control choice should track the true semantic action, not the visual on/off shape `BND-010`
Using a checkbox/radio purely as a generic interface on/off switch is technically accessible but semantically mismatched, because users associate those controls with designating a value for submission, not switching live interface state. The same visual on/off shape is correct for checking off a todo item, because that action genuinely is "designate this item as selected/done" — the underlying control choice should follow what the interaction actually means, not merely its visual resemblance to another pattern; an instance of the broader same-component test (BND-002).
Do: use checkbox/radio where the action genuinely means "select/designate this," not merely "flip a live switch."
Ask: Would the user reasonably believe they are choosing a value to submit, versus flipping a live switch? (IC ch1)

## Drawing Boundaries

### Boundary criteria escalate by size tier: indivisibility, then emergent purpose, then standalone section `BND-001`
A component's smallest tier is bounded by functional indivisibility (an element that stops working if decomposed further); the next tier up earns its own boundary when combining base elements creates a new, tangible purpose none of them had alone (not mere visual adjacency); the tier above that is bounded by forming a recognizable, standalone section of the interface, whether built from repeating one part or combining several different parts. This is not vocabulary to memorize but a reusable boundary-judgment technique — each tier answers "why does this deserve to be one unit" with a different, escalating criterion.
Do: ask whether decomposing further destroys the piece's function; ask whether combining elements creates a purpose none had in isolation; ask whether the result forms a recognizable, self-contained section regardless of whether its parts repeat or differ.
Ask: If I split this further, does any piece still function on its own? Does this grouping do something its parts can't do individually? Would a user recognize this as one distinct section of the interface? (AD ch1)

### Scope test for a behavioral unit: single-task and low-effort belongs in one component `BND-036`
A single-task, low-commitment, quickly-completed behavior belongs inside one atomic component; once a behavior grows to require multiple functions and sustained user attention, it has outgrown that unit and should be composed from multiple components instead. Sometimes a unit's entire purpose IS exactly one task, in which case the atomic behavior and the whole component's boundary correctly coincide and further decomposition would produce pieces with no independent meaning. The governing discipline is restraint: keep a unit's rule set minimal and focused, resisting the instinct to fold adjacent needs into an existing unit — a genuinely new capability should become its own unit.
Do: keep a single behavioral unit's rule set minimal and focused on one job; give a genuinely new capability its own unit rather than absorbing it into an existing one. Trade-off: restraint (small, separate units) keeps each unit predictable but can require users to learn/find a second unit rather than getting everything from one place, versus consolidation folding related needs into one unit.
Ask: Does this behavior do one task quickly with little required attention, or does it bundle multiple functions and require sustained focus? Is this new requirement actually part of this unit's one job, or does it belong in a separate unit? (MI ch1)

### Name a component after who actually drives it `BND-008`
A component's name should track who/what actually initiates its behavior — e.g. "content slider" (the user's deliberate action) rather than "carousel" (which implies autoplay) — because naming communicates a mental model of where control actually sits. Separately, statefulness (a page changing in place while the user operates it, not just via navigation) — not link/button count — is what makes a product feel app-like, and it is precisely that statefulness which creates the need for a notification/state-change-communication component in the first place.
Do: name a component to reflect who/what actually drives its motion or change; treat the presence of in-place state change, not control count, as the signal that a notification component is needed.
Ask: Does this component's name reflect who actually initiates its behavior? Does this page change state in place while the user operates it, beyond simple navigation? (IC ch2)

### A card's identity includes its collection membership, and its interactive surface has a real budget `BND-007`
A card's semantic contract includes membership in a collection (wrap it in a real list item inside a real list), not just its own contents, because that structure is what lets assistive technology convey how many cards exist and navigate between them. A card should not accumulate enough functionality to become a miniature web page: every additional interactive element inside it must be justified by real, non-redundant benefit against its keyboard-navigation cost.
Do: wrap each card in a real list item inside a real list; keep a card's interactive surface deliberately small; justify each additional tab stop by a real, non-redundant benefit not already reachable another way. Trade-off: wrapping the whole card in one link maximizes click target size but degrades the accessible name and can hide secondary interactive elements from some screen readers; targeted interactive elements keep the name concise but add tab stops.
Ask: Has this card accumulated so much independent functionality that it behaves like its own page? Is this destination already reachable another way that doesn't cost an extra tab stop? (IC ch3)

### Model the real state, not a convenient bistable toggle `BND-009`
A bulk "expand all / collapse all" feature for independently-toggleable sections should be two separate, always-available controls rather than one toggle button, because the count of open sections can land in a mixed/indeterminate state that a single boolean toggle cannot represent unambiguously.
Do: provide separate "expand all" and "collapse all" controls instead of one bistable toggle.
Ask: Can "all sections" state ever be a mixed/indeterminate combination? If so, don't model it as one boolean toggle. (IC ch2)

### Empty state is a required design surface, not an afterthought `BND-042`
Empty states are a required part of a component's design, not decoration. New/first-time users are among the most vulnerable to confusion from an interface with no example content or affordance cues, so a component whose primary content can be empty must give the empty state explicit, actionable instructional copy.
Do: give the empty state explicit, actionable instructional copy.
Ask: What should a first-time user with zero content see and be told to do? (IC ch1)

### Decouple a component's structure and style layer from its content/data `BND-031`
A pattern's markup structure and its content influence each other, but a resilient component keeps them decoupled: content can change without touching the pattern's markup, and the markup/style can change once without separately updating every instance's content. This applies equally to the visual-framework/style layer (color, fonts, spacing, grid), which should be defined once and referenced everywhere, analogous to a shared stylesheet, so framework-wide adjustments don't require touching every page.
Do: separate a component's structural definition from the data/content it displays; centralize style/framework definitions in one place, separate from content. (AD ch1; DI ch1)

### A component's contract should include explicit content-structure constraints `BND-032`
A template or component should fix the content structure it must accept — required image dimensions, character-length ranges for headings and text, required vs. optional fields — before any real content is selected. This lets otherwise-abstract components be validated against realistic constraints and gives the system explicit guardrails for what kinds of content each pattern must accommodate.
Do: define explicit content-structure constraints (image sizes, character-length ranges) as part of a component's contract. (AD ch1)

### Design components to adapt to their container context, not a fixed placement `BND-033`
A component should be built fluidly enough to be dropped into different containers/contexts and still work; the more context-independent a component is, the more resilient and versatile it becomes. A component's own styles and behavior should adapt to whatever container it's placed in, rather than assuming one fixed placement or viewport.
Do: design components to adapt their styling/behavior to their containing context rather than a fixed viewport or placement. (AD ch1)

### Don't let backend data structure dictate component boundaries `BND-034`
A form (or any component) should not simply mirror a database record's or object's field structure one-to-one, laid out in declaration order — that's convenient to implement but frequently not the most usable representation. Fields, grouping, and interaction model should instead reflect the user's actual data-entry intent and familiar conventions. A form spanning many topics should be split into titled sections that group related fields; tabs are usually a poor mechanism for grouping a single form's own fields.
Do: design controls and grouping around what the user is prepared to supply, using familiar conventions rather than a generic property sheet; use titled sections to group related controls within one form, not tabs. (DI ch3)

### No universal control or list pattern — the choice weighs several contextual factors `BND-035`
There is no single correct way to display a list or choose a control for a given input; the right pattern depends on content type, surrounding layout, and platform constraints. For choosing among equivalent controls for the same logical input, weigh: available screen space, general computer literacy of the user population, the user's domain expertise (do they already know the valid value range?), conventions/expectations carried from other applications, and what the target platform actually provides. Trade-off: compact/space-efficient patterns (carousel, one-window drilldown) trade away easy comparison/searchability that spacious patterns (two-panel selector, list inlay) provide.
Ask: How much on-screen space can this control occupy relative to competing content? Does the user already know the valid values/range from domain expertise? Does a convention from other apps/platforms already set an expectation for how this should look? (DI ch2,3)

### Seams between composed components should be invisible to the user `BND-037`
Before starting a new component, map how every component needed for a feature connects and hands off to the others (a "microinteraction map"). The handoff seams between components should ideally be invisible to the user — the whole feature should feel like one coordinated thing, not disconnected fragments — and this mapping step should also surface whether an existing component already covers the handoff, avoiding a redundant or conflicting new one.
Do: map how components hand off to each other before building a new feature; check for reuse or conflict against existing components before adding a new one.
Ask: Would the user ever perceive the handoff between these two components as a seam? Does an existing component already serve this handoff, making a new one redundant or conflicting? (MI ch2, ch6)

## Shared vs Local & Promotion

### Don't promote a one-off to a shared pattern until a second, independent need appears `BND-011`
A newly built UI solution should default to staying local/one-off, not become a new shared pattern immediately — a single use case doesn't prove reusability. A different team, working on a different application, independently wanting the same thing is a much stronger signal of genuine reuse value than assuming reusability up front. The underlying test is generality of intended purpose, not visual similarity to existing patterns: elements built for a narrow, time-boxed purpose stay one-off even if they resemble system patterns, but should be redefined more generically and promoted if broader need emerges later.
Do: default new solutions to one-off/local until a second, unrelated team independently requests the same thing; treat narrow, time-boxed, campaign-specific elements as one-off even if visually similar to existing system patterns; redefine and promote a one-off element into the library once broader need genuinely emerges. Trade-off: waiting for a second independent need avoids premature/unjustified abstraction and bloat, but delays sharing's benefits if that second need does eventually arrive.
Ask: Was this element defined for a general/broad purpose, or a narrow/time-boxed one? Has this one-off element since proven useful to other teams or purposes? (AD ch2; DS ch4)

### Pattern-promotion trigger is itself a genuine tradeoff `BND-012`
There are two legitimate criteria for when a new element becomes an official shared pattern: (1) auto-add every new element immediately, paired with strict duplicate-check/review discipline to prevent redundant patterns; or (2) add an element only after it has actually been reused a few times, keeping the library lean — but this only works if all created elements, even ones not yet promoted, stay fully discoverable, otherwise it silently reintroduces duplicate creation.
Trade-off: immediate-add favors completeness but demands strong dedup discipline to avoid clutter; add-on-reuse favors leanness but is contingent on pre-promotion discoverability.
Ask: Should new elements be added immediately with strict dedup review, or only after demonstrated reuse? (DS ch4)

### Economics of promoting to a shared pattern `BND-013`
Building a component as a flexible, named, reusable module costs more upfront than a one-off (documented example: roughly double the build time), but every later reuse then takes near-zero time. Once centralized, updating a pattern once propagates to every place that uses it, whereas the same visual style duplicated ad hoc must be manually repeated at every occurrence — slower and more error-prone. Reused modules also tend to improve faster than one-offs, because each new context surfaces a different edge case.
Do: centralize a pattern once it is duplicated across the codebase so future changes propagate automatically; weigh the extra upfront generalization cost against the likelihood this component will be needed again elsewhere.
Ask: Will this component likely be needed again elsewhere, enough to justify the extra upfront generalization cost? If this style changes later, how many places would need to be updated by hand? (DS ch3)

### Route a shared pattern's misfit through explicit governance `BND-016`
When an existing shared pattern doesn't quite work for a specific application, the design system needs a deliberate decision path — modify the pattern for everyone, redirect the team to a different existing pattern that already fits, or create a genuinely new pattern — rather than letting the team default to a silent local override. Pattern evolution overall breaks down into three distinct operations, each with its own criteria: modification (for feature/bug/style/a11y updates), addition (a genuine gap no existing pattern addresses), and removal/deprecation (unused, obsolete, or a bad idea).
Do: route a pattern misfit through an explicit modify/redirect/create-new decision rather than a silent local override; identify which of modify, add, or remove actually applies before acting. (AD ch2)

### Name and structure patterns by generic shape or action served, not by current context `BND-014`
How a pattern is named shapes how reusable it becomes: naming it after the specific page/context it currently lives in or the specific content type it currently holds artificially restricts where a team feels comfortable reusing it, even when the underlying structure is identical. Naming it after its generic structural shape, or the action/purpose it serves, signals that broader scope and is what should guide the initial name — with the name revised later if the pattern's actual reuse scope changes. When: starting with a more limited/specific name is acceptable if unsure, provided it is revised once reuse scope becomes clear.
Do: name display patterns for their generic shape (e.g. "card") rather than their current page or content context; frame a pattern's purpose by the user action it serves (a verb), not its current visual form (a noun); rename a pattern when its actual reuse scope no longer matches its original name.
Ask: Does this name tie the object to one context or content type that will limit its future use? Does the current name still reflect where this pattern sits on the specificity axis? (AD ch2; DS ch1,3)

### Group functional patterns by user-journey stage, not by which page currently hosts them `BND-044`
To keep functional patterns coherent as a product evolves, organize and classify core modules by the stage of the user journey they serve (e.g. Discover / Learn / Achieve) rather than by which specific page currently hosts them — reframing the design unit from "design this page" to "design this journey stage" keeps each pattern's purpose anchored to user behavior across the whole product.
Do: classify modules by target user-journey stage before evaluating them individually. (DS ch1)

### A pattern's known target purpose calibrates redesign and curbs duplication `BND-045`
A functional pattern's surface details (styling, interaction mechanics, layout) can change repeatedly over a product's life, but its underlying target purpose tends to stay fixed, because that purpose is tied to the product's core idea rather than any one execution. Once that target purpose is explicit and shared across the team, redesign changes can be judged against a known, shared goal rather than aesthetic taste, and anyone with a new need can check it against existing patterns' already-understood purposes before building something new — reducing duplicate/near-duplicate pattern creation.
Do: treat a pattern's purpose as the redesign anchor, and check new needs against existing patterns' known purposes before building something new. (DS ch1)

## Diagnosing Near-Duplicates

### Interface inventory: catalog live UI instances to surface near-duplicates as concrete evidence `BND-017`
Before designing/building a shared component system, screenshot and categorize every unique UI pattern currently in production (one instance of each unique pattern, not every occurrence). This produces concrete visual evidence of redundant near-duplicates versus genuinely distinct patterns, more persuasive than describing inconsistency in words. It is not a one-time exercise — repeating it periodically keeps the team's system understanding current at low cost per pass. When: teams disproportionately audit high-visibility areas (e.g. the homepage) and neglect less glamorous but equally real areas (support, error pages, legal) unless deliberately corrected.
Do: screenshot one instance of each unique pattern, not every occurrence; involve representatives from every discipline so the resulting vocabulary is cross-functional; time-box the inventory session to avoid an open-ended rabbit hole; repeat the inventory periodically rather than treating it as one-time. (AD ch2; DS ch1)

### Purpose-directed inventory: group elements by intended behavior, run only after core UX is settled `BND-018`
A purpose-directed inventory groups UI elements by the user action/behavior they are designed to support, rather than by visual appearance — a complementary axis to a visual interface inventory, since visually different elements can share a group and visually similar elements can end up in different groups. Its process: identify the main user actions/needs per journey stage, find and group existing elements by the purpose they currently serve, then decide per group whether to consolidate into one pattern or keep separate. This process works best only after foundational UX work (research, content strategy, IA, design direction) is already settled — running it against a soon-to-change interface locks in the wrong structure.
Do: group existing elements by the user action/purpose they serve, not by visual appearance; run the purpose-directed inventory only after basic UX direction is settled. (DS ch3)

### Keep grouping candidates at a consistent granularity level `BND-021`
When grouping existing elements by purpose to find pattern candidates, every group must stay at the same level of granularity — a concrete-object-level module (e.g. a "book list") should not be grouped together with an action-level element (e.g. a "reserve" button), because conflating different granularities produces incoherent pattern candidates.
Do: keep every candidate group either all-objects or all-actions, never mixed.
Ask: Are all items in this candidate group at the same level, rather than mixed? (DS ch3)

### Diagram or scale-compare near-duplicate patterns side by side before unifying `BND-019`
When several patterns look similar but were built independently, decompose and diagram each one's content structure side by side to evaluate whether they can be safely unified into one pattern covering all their use cases. Extending this to a whole functional category, compare all patterns within it on a shared prominence/visual-intensity scale to check whether they're competing for attention or redundantly occupying the same level, before adding a new module. When: visually-similar-but-independently-built patterns left undiagrammed drift apart over time, because changing one doesn't propagate to the others.
Do: diagram each near-duplicate candidate's content structure (identifier / header / content / actions / etc.) side by side; compare same-category patterns on a shared prominence/visual-intensity scale before adding a new one. (DS ch1)

### Content-structure comparison: a second technique for deciding whether elements should share one pattern `BND-020`
Beyond visual/prominence comparison, map each candidate's content structure: identify the core content required to serve its purpose (required vs optional), work out the hierarchical grouping, and sketch it visibly. Elements that can be safely unified generally share the same underlying content structure; elements that look visually similar but have structurally different content models (e.g. a discovery-page teaser image vs. a dense-list thumbnail) are a stronger signal to keep separate than visual similarity alone suggests. Sketching this structure explicitly, separate from visual design, also builds shared understanding across design and engineering before implementation.
Do: map each candidate's required vs optional content and its hierarchy before deciding to unify; sketch content structure separately from visual design, with design and engineering together.
Ask: If I change this module, would I want the same change applied to the other candidate module? If not, they may need separate structures. (DS ch1,3)

### Difficulty naming or titling a grouping is a diagnostic signal `BND-015`
When no appropriate name comes to mind for a new component, or a content section resists a clear, memorable title, treat that as a signal something is wrong with the definition itself — either the purpose is unclear or it duplicates an existing pattern's purpose — rather than as a mere labeling problem. A recurring "Other/Misc" catch-all is a particular warning sign of unsound categorization. Separately, a name lacking an evocative, memorable quality correlates with the pattern falling out of use and a near-duplicate being built in its place, even among team members who claim to prefer precise technical names. When: an "Other" category is sometimes genuinely necessary.
Do: treat naming/titling difficulty as a prompt to re-examine the component's actual purpose or the grouping itself; regroup content into more memorable units rather than force an awkward title; prefer a memorable, evocative name over a merely precise/technical one.
Ask: Why can't we name this? Is its purpose actually unclear, or does it duplicate an existing module's purpose? If I say this component's name out loud to a teammate, can they picture what it looks like? (DS ch2; DI ch1)

### A variation is a modified version of a shared core pattern, not a separate pattern `BND-022`
When elements share the same content structure but need different appearance or behavior due to context or intent, define the difference as a variation of one core pattern rather than as a separate pattern — and decide explicitly which properties belong to the shared core versus the variation, since that decision determines whether a future change to one place also changes the other. The same logic applies when a component needs a variant driven purely by extra state or permissions (e.g. an admin view adding edit/delete actions): model it as an override/extension of the base pattern's data, inheriting the base's structure and default content, rather than duplicating the whole pattern and manually keeping it in sync.
Do: identify explicitly which properties are shared-core vs variation-only before implementing; model state-driven variants as an override/extension of the base pattern's data rather than a duplicated pattern. Trade-off: overriding/extending the base pattern keeps variants in sync automatically but can make the base pattern's conditional logic harder to read than a fully separate, explicit pattern would be.
Ask: Which specific properties are part of the shared core, and which are unique to this variation? Does this variant differ from the base only by extra data/state, or is it a fundamentally different kind of component? (AD ch1; DS ch3)

## Scope Axes: Modular/Integrated, Strict/Loose, Specificity

### True modularity requires interchangeable parts; integrated design is optimized for one purpose `BND-025`
True modularity means more than "built from multiple parts" — it requires that the parts be genuinely interchangeable and assemblable in varied, changing ways to serve diverse or evolving goals. A system whose parts cannot be reconfigured is not modular even if it consists of multiple pieces. Integrated design is the mirror image: still multi-part, but the parts are not interchangeable because their connections were never designed to support alternate configurations — each part fits its one specific role, optimized for a single purpose rather than recombination.
Ask: Can these parts actually be recombined in different configurations to meet different needs, or do they only ever assemble one way? Were these parts' connections designed to support any alternate configuration, or only this one? (DS ch2)

### Modular vs integrated design: concrete benefits and drawbacks on both sides `BND-026`
Modular design offers agility (parallel team work), cost-efficiency (reuse over rebuild), easier maintenance (isolated fixes), adaptability, and generativity (new combinations produce outcomes not explicitly designed for) — but costs more to build well upfront with unclear early ROI, risks generic/predictable results unless novelty is deliberately reintroduced, can sacrifice a specific page's ideal impact for reuse's sake, and requires deliberate attention to the seams and relationships between modules, not just each module's own quality. Integrated design mirrors this: more specialized, higher internal consistency, more effective as a whole for its one purpose — but zero extensibility and no adaptability as needs grow.
Do: pay explicit attention to the relationships between modules (relative prominence, role in the user journey, hierarchy), not just each module in isolation. Trade-off: modular trades slower/uncertain-ROI upfront build and genericness risk for reuse, agility, and adaptability; integrated trades zero extensibility for higher specialization and internal consistency.
Ask: Have we accounted for build-time cost, genericness risk, page-level impact tradeoffs, and cross-module coherence — not just individual module quality? (DS ch2)

### Judge modularity by UX impact, not just efficiency `BND-027`
Modularity's value should be judged by how much it actually improves the user/product experience, not just efficiency or cost savings — in some cases modularity itself becomes a defining, identity-creating feature of the product. Structural modularity (how a thing is actually built) and perceived modularity (how modular it looks/feels) are separate questions that can diverge in either direction: a structure can be genuinely modular and have that modularity be the core design feature; or fully integrated in construction while deliberately styled to look modular because the aesthetic suits the product even without real reconfigurability.
Ask: Could modularity itself become part of this product's distinctive identity, not just a backend efficiency mechanism? Does this product need genuine reconfigurability, or just the visual/perceptual impression of modularity? (DS ch2)

### Decision checklist: when a modular vs. integrated approach suits a product `BND-028`
A modular approach tends to suit products that need to expand/shrink or otherwise be extended over time, serve multiple distinct user needs, contain heavy repeated structure, or require multiple teams to work independently in parallel. An integrated approach suits products designed for one specific purpose that won't change, that need art direction exceeding any reasonable modular system's boundaries, that have little genuinely shareable content, or that are used once with low reuse likelihood.
Ask: Does this product need to expand/contract, serve diverse user needs, repeat structure heavily, or support parallel independent team work? Is this a one-off, single-purpose piece of work with little need for future extension or reuse? (DS ch2)

### A system can deliberately exclude work from its modular boundary, and its modularity level is not fixed `BND-029`
A product can deliberately keep certain work (e.g. campaign/marketing) outside its core modular system's boundary to preserve necessary creative range, while still reusing a small set of brand-identity elements (palette, type, shapes) even when stepping outside. How much a system should be modularized is not fixed — it evolves in either direction over time: systems often modularize further as repeated patterns accumulate with growth, but the reverse also happens, adding more bespoke/integrated-style parts specifically where forced reuse was hurting high-impact pages.
Do: reuse a small set of brand-identity elements even when stepping outside the main modular system for creative work; reassess modularity level periodically rather than assuming it should stay fixed permanently.
Ask: Does this campaign need the creative range that stepping outside the core modular system provides? Has this area of the product outgrown its current position on the modular-integrated spectrum, in either direction? (DS ch2)

### Strict vs loose governance: predictable reuse vs context-optimized effectiveness `BND-030`
A strict, centralized system trades creative flexibility for site-wide predictability and reuse; a loose system trades some enforced consistency for room to optimize each page/context individually — and a loose system only holds together if its coherence comes from genuinely shared team culture and design understanding, not from enforced rules or process, which is why it doesn't automatically transfer to a team without that alignment. No governance approach (centralized/distributed, strict/loose, modular/integrated) is free of shortcomings; the deciding factor is which approach's specific weaknesses this particular team is equipped to handle, not which looks best in the abstract or worked for another team.
Trade-off: strict/centralized maximizes predictability and reuse at the cost of per-context flexibility; loose/culturally-aligned maximizes per-context optimization but only holds together with strong, genuinely shared team culture — without that, it degrades.
Ask: Is our system's coherence coming from enforced rules, from genuinely shared team understanding, or neither? What are this approach's known weaknesses, and can this specific team handle them? (DS ch2,3)

### Specificity is an axis with real costs on both ends — no universal correct level `BND-024`
A pattern can be defined narrowly/specific or broadly/generic, and there is no single correct level: specific/separate patterns are easier to keep locally correct and preserve intentional distinction, but harder to reuse and costlier to maintain as their count grows; generic/unified patterns reuse well and reduce duplication, but overusing them risks a bland, undifferentiated, inflexible result. The same axis works in reverse — once real usage data reveals distinct categories inside a generic component, splitting it into task-specific variants (with category-appropriate defaults) can make each case dramatically simpler, trading some component proliferation for relevance.
Do: default to maximum genericity or maximum specificity only after checking whether it erases an intended distinction or multiplies maintenance; specialize a generic component into category-specific variants once usage data supports it, with category-appropriate defaults. Trade-off: specific patterns preserve distinctiveness and local correctness but cost more to maintain and reuse less; generic patterns increase consistency and reduce duplication but any change propagates everywhere and overuse risks blandness.
Ask: Do you want users to perceive these two things as distinct from each other? Has usage data revealed distinct categories this generic component actually serves? (DS ch3; MI ch2)

## Over-Abstraction Guards

### A minimal, purpose-built component can be both smaller and more correct than a general-purpose library `BND-038`
A component satisfying baseline requirements with a small amount of purpose-built code can be a deliberately acceptable, final scope rather than an incomplete stepping stone toward a general-purpose library. Building minimal and purpose-fit avoids paying the complexity/weight cost of unused general-purpose features — and can beat an off-the-shelf general-purpose plugin on both size and correctness, since generic plugins carry code paths and defaults for use cases beyond the immediate need and can embed accessibility mistakes that go unnoticed at scale. Documented example: a purpose-built content slider under 2KB minified versus a generic carousel plugin at roughly 42KB that, in some cases, incorrectly hides focusable content from screen readers.
Trade-off: minimal custom is smaller and exactly scoped to the case but misses whatever unused library features would have added; general-purpose libraries add features and weight and may carry latent defects.
Ask: Does the use case genuinely need more than this minimal, working implementation provides? (IC ch2)

### Over-prioritizing consistency produces a generic, inflexible system `BND-039`
Optimizing purely for pattern consistency produces a generic, inflexible design system. Evolving a system's cognitive/perceptual patterns requires designers to actively use slack at the edges of the system's current boundaries to explore new ideas, rather than rigidly enforcing existing patterns everywhere all the time. When: a design system has matured and consistency enforcement is starting to feel rigid.
Do: reserve deliberate space at the system's boundary for exploration, rather than enforcing existing patterns as an absolute constraint everywhere. (DS ch2)

### Collapse taxonomy levels that don't earn their keep `BND-040`
A borrowed hierarchy/taxonomy (e.g. Atomic Design's atom/molecule/organism/template/page levels) is a tool, not a mandate: when the distinction between two adjacent levels repeatedly fails to resolve real ambiguity for a team, collapse those levels into fewer tiers rather than force-fitting the canonical taxonomy.
Do: collapse hierarchy levels that don't carry real distinguishing value for the team.
Ask: Does this level distinction actually resolve a recurring question for this team, or just cause repeated debate? (DS ch4)

### Quarantine legitimate special-case elements instead of bending general pattern rules to fit them `BND-023`
Some elements are legitimately special cases carrying unique state or outsized brand/symbolic weight. Mark such elements explicitly as special cases, separate from the general pattern rule set, rather than distorting the general rules to accommodate them — special cases should be rare, and keeping them isolated preserves the integrity of the general patterns.
Do: name special-case elements by their specific function rather than forcing a generic name onto them. (DS ch3)

### A redundant "×" close button alongside explicit action buttons signals dialog design debt `BND-046`
If a dialog already has explicit OK/Cancel (or equivalent) action buttons, it does not also need a separate "×" dismiss button. The presence of both is a legacy affordance carried over out of habit rather than need — two different controls that both close the dialog without a clear distinct purpose add redundant functionality and an extra tab stop for no benefit.
Ask: Does this dialog have both explicit action buttons and a generic "×" close button with no distinct purpose of its own? (IC ch3)
