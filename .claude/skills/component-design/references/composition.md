# Composition & Conceptual API

This file serves decisions about how parts assemble into wholes: where to draw a component's
boundary, whether to split or merge a pattern, how a composite exposes its contract to
consumers, and how independently-built components combine into a coherent feature. Route here
when scoping a new component, deciding between a generic and a specific variant, designing a
composite's public surface (events, grouping, hit areas), or wiring several components into one
flow.

## Contents
- Part-Whole Hierarchy
- Primitive vs. Composite: Scope Discipline
- Context-Independence & Reuse by Reference
- Composite Contracts: Public API, Grouping, Interactive Surface
- Composition vs. Configuration, and Generic vs. Specific
- Validating & Documenting Composites
- Chaining & Seams: Composing Features from Components

## Part-Whole Hierarchy

### Hierarchical part-whole composition is a concurrent, vocabulary-agnostic, medium-agnostic mental model `CMP-003`
A multi-level component hierarchy (e.g. atoms→molecules→organisms→templates→pages) is a way of
reasoning about how small parts compose into larger parts, held concurrently at multiple levels
of granularity — not a mandatory linear bottom-up build order. Level names aren't sacred; any
vocabulary the organization will actually internalize works, as long as the underlying
hierarchical relationship survives, and the same reasoning applies to any UI medium, not just
web.
Do: treat each level as a lens for reasoning about the same interface at a different grain, not
a sequential build phase; adapt naming to what the org will adopt; apply hierarchy/boundary
reasoning independent of implementation platform; define explicit nesting rules per level.
Ask: does the underlying hierarchy still survive if we rename the levels?
(AD ch2; DS ch10)

### Cap hierarchy depth: keep only tiers that carry real distinguishing value `CMP-004`
More than about three tiers of hierarchical pattern categorization tends to create confusion.
Still, retain a distinction between coarse-grained and fine-grained patterns even when
simplifying levels, because that distinction carries real meaning for the pattern library's
structure and the underlying code.
When: each tier should resolve a real, recurring question; avoid tiers that are decorative
categorization.
Do: keep a coarse-grained vs. fine-grained distinction even when simplifying levels; avoid
maintaining 3+ tiers unless each carries real distinguishing value.
(DS ch10)

### A composite is sub-parts with distinct purposes serving one shared goal `CMP-008`
A functional pattern can be a single atomic module or a composite of several sub-modules
combined into one coherent pattern. In a well-formed composite, each sub-module carries its own
distinct purpose, while all sub-modules jointly serve one shared overall goal — e.g. a
recipe-card's name, image, ingredient-list, and action-button modules each do a distinct job but
jointly serve getting the user to cook the recipe.
Ask: does each proposed sub-part have its own distinct purpose, and do all sub-parts still serve
one coherent overall goal?
(DS ch3)

### Visual containment (enclosure) signals a parent-child/composition relationship `CMP-018`
Enclosing related items inside a shared visual boundary — a box, background-color block,
tab-style module, accordion, bordered/padded group, indentation, or hierarchical menu —
communicates that those items are a child group belonging to that container, not merely that
they are visually near each other (the Gestalt "closure" factor). Containment implies
parent-child ownership, a stronger signal than mere proximity grouping.
When: use a bounded container when the relationship is genuinely parent-child; when only "these
are related" is meant, proximity alone suffices.
(DI ch4)

### Check whether two differently-named patterns already share one underlying composition primitive before building separately `CMP-019`
Two components that appear to be different named patterns (e.g. "List Inlay" and "Accordion")
can in fact be the same underlying behavioral primitive — single-column container, item/panel
expands in place, independent open/close per panel — applied under different names. Before
building a separate implementation for a new name, check whether an existing primitive already
satisfies the same behavioral contract; if so, design guidance for one largely transfers to the
other.
(DI ch5)

## Primitive vs. Composite: Scope Discipline

### Keep a component single-purpose; push complexity up through composition `CMP-001`
Scope each small reusable component to one responsibility ("do one thing well"); when a UI need
is more complex than that, build the complexity by composing multiple simple components together
at a higher level rather than loading it into one component. Narrowly-scoped components are
easier to test and reuse in unanticipated contexts, and keep the same simple piece recurring
rather than proliferating slightly-different heavyweight variants that erode consistency.
Do: scope small components to a single responsibility; compose simple components together to
build more complex behavior rather than growing one component's scope.
Ask: is this component trying to do more than one job — could the extra responsibility be split
out and composed alongside it instead?
(AD ch2)

### Fewer, smarter objects vs. one behavioral unit doing one thing — an unresolved tension `CMP-002`
Two composition instincts pull opposite ways and neither wins outright: (a) prefer fewer,
smarter objects that absorb a wider range of related operations themselves (e.g. a credit-card
field that auto-detects card type instead of needing a separate type selector), vs (b)
restraint — scope each behavioral unit as small as possible, resisting folding more
functions/rules into it, spinning off a new unit when a genuinely new capability is needed. An
object may absorb more of a related range if doing so still serves its one conceptual job, but
should not absorb unrelated responsibilities; the resolution is local, case-by-case.
Trade-off: fewer, smarter objects reduce the number of distinct nouns a user must learn, but risk
scope creep into unrelated responsibilities — vs. strict one-job restraint keeps a unit's rules
coherent and predictable, but can mean users must learn/find a second unit rather than getting
everything from one place.
Ask: does the new capability fall within this object's single conceptual job, or is it an
unrelated responsibility that should spin off a new unit? Would merging require accumulating
unrelated rules just to cover the range?
(MI ch1,3)

## Context-Independence & Reuse by Reference

### Context-independence: a reusable component must derive placement-dependent properties from its composition context, not hard-code them `CMP-009`
A component meant for reuse in varying places cannot hard-code properties whose correct value
depends on where it ends up composed. This shows up in at least two forms: (1) internal heading
level is a function of document nesting depth, which only the composing context knows — it must
be computed/passed dynamically, and preserved via aria-level (never as a CSS styling hook) if the
component relocates or reproduces an author-supplied heading; (2) layout/behavior must adapt to
whatever container it's dropped into (full-bleed, article width, sidebar) rather than assuming
one fixed placement or viewport.
When: applies whenever a component is placed at varying nesting depths, container sizes, or
contexts; a component whose placement is fixed and known (e.g. a page-level unique widget) doesn't
need this.
Do: derive heading level dynamically from ancestor context rather than hard-coding it; preserve
the original heading level via aria-level when relocating/reproducing a heading, never repurposed
as a styling hook; design components to adapt styling/behavior to their containing context.
Ask: will this component ever need to render at a different nesting depth, width, or context than
the one I'm designing it in right now?
(IC ch3,8; AD ch3)

### Compose by reference, not duplication, to keep changes DRY `CMP-005`
Build a UI by including/referencing a shared pattern inside larger patterns rather than
duplicating its markup or style per instance. Because consumers reference the shared source, a
single edit to that source propagates everywhere it's used, instead of requiring the same change
to be manually repeated at every duplicated copy — Etsy's button-style update produced an
unusually large diff specifically because the button style existed in many duplicated places
rather than as one centralized pattern.
Do: include/reference shared patterns rather than duplicating their markup per instance;
centralize a pattern once it is duplicated across the codebase, so future changes propagate
automatically.
Ask: if this pattern needs to change later, will the change apply everywhere it's used, or will
each duplicated copy need to be found and updated by hand?
(AD ch3; DS ch7)

### Reuse-investment trade-off: a properly reusable module/library costs more upfront, but reuse then becomes near-free `CMP-026`
Investing extra time upfront to build a component as a flexible, named, reusable module (or to
organize a library of reusable parts before assembling products from it) costs more than a
one-off build the first time — FutureLearn found a simple custom component took about 3 hours to
build once, versus roughly double that as a reusable pattern-library module — but every
subsequent reuse then takes almost no time, versus rebuilding an equivalent from scratch each
time.
When: worth the upfront cost only when the component/library is realistically expected to be
reused; a genuine one-off with no realistic reuse is exempt.
Trade-off: higher upfront build/organization cost for a proper reusable module or library vs.
near-zero marginal cost on every subsequent reuse — and that upfront cost is invisible in any
single deliverable.
Ask: will this component likely be needed again elsewhere, enough to justify the extra upfront
generalization cost?
(DS ch7; AD ch4)

### Reuse repeated markup via symbol/use rather than duplicating it per instance `CMP-011`
When the same graphic (e.g. an icon) repeats once per row/instance across a composite (like a
list), define it once as an SVG `<symbol>` and reference it per-instance with
`<use xlink:href="#id">`, rather than duplicating the full markup in every row. A bloated DOM
slows interaction for everyone, and assistive technology users are disproportionately affected
because AT software must process and traverse more nodes per operation.
(IC ch3)

## Composite Contracts: Public API, Grouping, Interactive Surface

### Layer optional enhancements additively on a working composed base; never make the enhancement a prerequisite or a replacement `CMP-010`
When adding a JS-driven or feature-detected enhancement (a collapse toggle, extra prev/next
buttons) on top of an already-functional base interaction: the base markup should work fully and
remain usable before any enhancement is applied; new controls should build on and stay
synchronized with state changes the existing interaction already produces, rather than
duplicating or replacing that interaction; and the enhancement should render only if its own
dependency is actually supported, so its absence never breaks basic operability.
Do: author base markup as always-visible/fully operable with no enhancement-only state; add the
enhancement's UI only as a JS-driven/feature-detected step; make new controls read from and
respond to state the existing interaction already causes; gate an enhancement's rendering on its
own dependency's feature detection.
Ask: what does this component look like and do with JavaScript disabled or a dependency
unsupported — does basic operability still work?
(IC ch4,9)

### Expose a composite's public API as semantically-named custom events, not internal wiring `CMP-012`
A composed component's outward-facing API for significant state changes (e.g. a menu button's
item selection) can be a custom, semantically-named event carrying relevant data in its payload,
giving consumers a stable, clean way to react without needing to know the component's internal
implementation.
Do: expose semantically-named custom events as the component's public API for significant
internal state changes.
(IC ch4)

### Encode a reusable component's usage constraints as dev-facing runtime warnings, not documentation alone `CMP-013`
When a component has structural requirements that are easy to violate silently (e.g. a
toggletip's trigger must be a real `<button>`), encode those requirements as explicit runtime
checks: emit a developer-facing warning (e.g. console.error, detecting the disallowed element
and aborting further script execution for that instance), and echo the same check visually in
CSS via an attribute selector, so a developer inspecting markup in devtools notices the misuse
even without watching the console.
When: a hard-abort check is appropriate when the misuse would produce a broken or deceptive
accessible experience (e.g. a non-button disclosure trigger); when a reasonable degraded fallback
exists instead, degrade gracefully with that fallback while still emitting the warning, rather
than hard-failing or silently proceeding with no signal.
Do: detect disallowed underlying elements/structure at runtime and emit a console warning/error;
pair the JS runtime warning with a CSS-visible error indicator for the same misuse condition.
(IC ch5,8)

### Group related sibling controls with list markup unless a compound ARIA widget genuinely fits `CMP-014`
When composing multiple related, independent controls together (e.g. "expand all"/"collapse all"
buttons), wrap them in standard list markup (`<ul>`/`<li>`) so assistive technology reports them
as a related set with a count. Reach for a compound ARIA widget's own grouping mechanism
(role="menu"/menuitem, role="tablist"/tab) only when the interaction genuinely matches that
widget's paradigm — not by default.
Do: wrap related independent controls in a list; add a group label via aria-label/aria-labelledby
if individual labels aren't self-descriptive enough as a set; use a compound widget's grouping
role only when the controls genuinely form that widget.
(IC ch8)

### Whole-card clickability vs. one coherent accessible interactive contract `CMP-016`
Wrapping an entire card's contents in one `<a>` makes the whole card clickable but degrades the
link's accessible name into a verbose concatenation of all the card's content, and any further
interactive element nested inside that "block link" risks going unannounced by some screen
readers. Resolve by putting the single real `<a>` only around the card's title/heading, then
separately expanding that one link's hit area to cover the whole visual card for pointer/touch
users — via a CSS pseudo-content trick (no JS, extends the context menu across the card, but can
block text selection) or a JS "redundant click" proxy (preserves text selection, requires JS,
doesn't extend the context menu). Either technique leaves the underlying accessible/keyboard
contract anchored to the one real title link; only pointer/touch behavior is enhanced.
Do: keep the title text as the single real `<a>`, not the whole card; expand its hit area with
the CSS trick when text selectability isn't important, or the JS click-proxy when it must be
preserved; keep exactly one real focusable link inside the card regardless of technique.
Trade-off: whole-card clickability (one wrapping link) vs. a concise, useful accessible link name
and safely-announced nested interactive elements. Also: no-JS + full-card context menu (CSS
trick) vs. preserved text selection (JS proxy).
Ask: will this card ever need more than one interactive element, or grow richer text content?
Does its text need to stay selectable by pointer users?
(IC ch13)

### Justify every additional interactive element inside a composite by its keyboard-navigation cost `CMP-017`
Before adding a secondary interactive element inside an already-interactive composite (e.g. a
separate author link inside a card), weigh whether it is actually necessary or beneficial —
especially if the same destination is already reachable another way (e.g. via the permalink the
card already links to). Each additional focusable element inside a composite has a real,
non-zero cost to every keyboard user who tabs through it.
Ask: is this destination already reachable another way that doesn't cost an extra tab stop?
(IC ch13)

## Composition vs. Configuration, and Generic vs. Specific

### Composition vs. configuration: prefer a simple built-in heuristic over a full rule-authoring system, unless users genuinely need arbitrary custom rules `CMP-027`
When a component could be made more flexible by letting users author their own custom
rules/configuration, weigh that against a simple, fixed, built-in heuristic that covers the
common case at a fraction of the complexity cost. In the alarm-app example, the author
deliberately excluded custom repeat-rule authoring for alarms — even though it would add
flexibility — because it would make the whole app's rule logic dramatically more complex, instead
using a simple heuristic (checking weekday vs. weekend) that covers the common case.
When: building a full custom-rule-authoring system into a component purely "for flexibility,"
without target users who specifically need arbitrary custom rules, is an excessive-configuration
anti-pattern; cases where target users specifically need arbitrary custom rules may still justify
the added complexity.
Trade-off: flexibility/power of full user-authored configuration vs. simplicity and lower
complexity of a fixed built-in heuristic.
Ask: would a simple built-in heuristic cover the common case well enough to avoid full
user-authored configuration? Do target users specifically need arbitrary custom rules, or would a
fixed heuristic serve nearly everyone?
(MI ch6)

### Generic vs. task-specific pattern trade-off `CMP-025`
A pattern/component can be defined narrowly and specific to one case, or broadly and generic
across many. Specific, split-out patterns serve their particular case precisely (better defaults,
hidden irrelevant fields) but increase the number of things to keep consistent and reuse less;
generic, unified patterns reuse well but risk flattening the design into something bland or
forcing users through irrelevant questions. There is no single correct level of specificity — it
depends on what the design is trying to achieve. Where usage data reveals distinct recurring
categories within a generic component, that is a concrete trigger for splitting into
category-specific variants with tailored defaults (TaskRabbit replaced its single generic
free-text task-request form with category-specific forms only once usage data revealed common
categories), rather than deciding specificity upfront from guesswork.
Do: specialize a generic component into category-specific variants once usage data supports it,
pre-filling category-specific defaults; default to generic when usage patterns aren't yet known,
rather than guessing at specialization upfront.
Trade-off: specific/separate patterns give precise per-case fit and simplicity, but higher
maintenance surface and lower reuse — vs. generic/unified patterns give high reuse and
consistency, but risk blandness or irrelevant fields for any given case.
Ask: do you want users to perceive these two things as distinct from each other? Would content or
design intent needed for one case conflict with another if merged into one generic pattern?
(DS ch8; MI ch6)

### Modularity's value should be judged by UX/identity impact, not just efficiency — and structural modularity can diverge from perceived modularity `CMP-028`
Modularity's value should be judged not just by efficiency/cost savings but by how much it
actually improves the user/product experience — in some cases modularity itself becomes a
defining, identity-creating feature of a product. Structural modularity (genuine reconfigurability
in construction) and perceived modularity (looking modular) are separate questions that can
diverge either way: Puma City's genuine disassemble/relocate/rearrange capability is its core
design feature, while Basket Apartments' rotated-looking rooms create a modular visual impression
purely through balcony placement, without actual modular construction. Modularity is not an
unconditional good — how much of it is warranted depends entirely on what the product needs.
Ask: does this product need genuine reconfigurability, or just the visual/perceptual impression of
modularity? Could modularity itself become part of this product's distinctive identity, not just a
backend efficiency mechanism?
(DS ch6)

### A product's felt identity comes from relationships between composed elements, not the elements themselves `CMP-029`
Two products with similar palettes, few shapes, and a handful of icons can still feel completely
distinct, because their identity comes from the specific ratios/proportions and relationships
between elements — how colors relate to each other, how images relate to typography, how
typography relates to spacing — not from the individual elements in isolation (Vox vs. the
Guardian share the same general journalism-site anatomy yet feel opposite; overusing or
misplacing TED's signature red destroys "TED-ness" even though red is technically still on-brand).
Unifying headings or colors module-wide is not by itself sufficient to establish a distinct feel.
Do: study the ratios and combinations that create the intended mood, not just the constituent
tokens.
(DS ch4)

## Validating & Documenting Composites

### Validate a component both in isolation and inside its real compositional context `CMP-006`
Check a reusable component both on its own (the abstract, zoomed-in view — useful for focused
stakeholder discussion of a single pattern's aesthetics, hierarchy, and functionality) and
assembled into its real templates/pages with real neighboring components and real content (the
concrete, zoomed-out view). Neither view alone is sufficient before considering a component
finished — a component that looks correct in isolation can still fail in the context of a real
page (content overflow, spacing conflicts), and isolating a component also narrows the surface a
developer must inspect when something breaks.
Do: present/discuss a single pattern outside its surrounding page to keep design conversations
focused; also render the pattern within its actual template/page context to validate it
holistically before shipping.
Ask: have I validated this component both on its own and assembled into a real page with real
neighbors and real content?
(AD ch1,2,4)

### Define a composite's content-structure contract before visual or implementation work `CMP-007`
Before finalizing a pattern's visual design or markup, define its content-structure contract:
which content elements it requires vs. accepts optionally, the hierarchy/grouping among those
elements, and structural constraints (image dimensions, character-length ranges) content must
satisfy — independent of which final content will populate it. Content is dynamic and varies per
instance, so a design system has to work for a range of possible content, not one hypothetical
example; doing this collaboratively up front (designers, engineers, content strategists together)
prevents divergent results because neither side had a shared model of the pattern's content
structure.
Do: define explicit content-structure constraints as part of a component's contract; sketch
content structure/hierarchy before visual design, together with engineering and content strategy.
Ask: does the template/pattern articulate its content structure independent of which final
content will populate it?
(AD ch2; DS ch3)

### Document a pattern's composition lineage for usage guidance and change-impact assessment `CMP-030`
A pattern library entry should document not just an isolated demo of a pattern but its context:
usage guidance (when/where to use it, ideally with real screenshots/video from an actual
application) and lineage — which smaller patterns compose this pattern, and which larger
patterns/templates include it. Lineage acts as a dependency trail: if a pattern changes, it shows
exactly which other patterns and templates need review or retesting as a result.
Do: show real usage examples of the pattern in an actual application, not just an isolated demo;
record which smaller patterns compose a given pattern and which larger patterns/templates include
it.
(AD ch5)

## Chaining & Seams: Composing Features from Components

### Determine a sub-component's role and lifecycle relative to its parent feature before designing it `CMP-020`
A standalone microinteraction (one that fully constitutes an app/device on its own) is rare; most
are the periphery, interior, or core of a larger feature. Before designing a non-standalone
component, determine its relationship to the parent feature — does it launch it, control it,
serve as an internal sub-feature used within it, or terminate it — since each role implies a
distinct trigger, and separately assess how long the sub-component's UI should persist relative to
the parent feature's own lifecycle.
Do: identify the sub-component's role relative to its parent feature before designing its
trigger; match its visibility/persistence to that role.
(MI ch6)

### Chain components by using one's completion as the next one's trigger `CMP-021`
A larger feature can be composed from smaller components by daisy-chaining them: one component's
completion serves as the trigger for the next, whose completion in turn triggers a third, and so
on, rather than building one monolithic component that does everything. This lets each component
stay focused and simple while still combining into a coherent larger feature.
Do: use a component's completion event as another component's trigger to compose larger
features.
(MI ch6)

### In a composed feature, deliberately choose which sub-components stand out and keep tone consistent `CMP-022`
When multiple components combine into one feature, not all of them should be treated equally:
deliberately decide which need emphasis (stronger feedback, a bespoke control) and which should
stay unobtrusive, while keeping tone (color scheme, sound design, motion style) unified across the
whole set. A feature made of many components reads as either a coordinated whole or "a pile of
disconnected tiny moments" depending on whether emphasis and tone are managed deliberately.
Do: deliberately choose which sub-components get emphasis; keep tone consistent across all
sub-components of a composed feature; account for the prominence a custom control creates
relative to its siblings before using one.
Trade-off: custom controls gain distinctiveness at the cost of consistency with sibling
components.
(MI ch6)

### Seams between composed components should be invisible; check for reuse before adding a new one `CMP-023`
Before starting a new component's design within a larger composed feature, map how the needed
components connect/hand off to each other, and check whether an existing component already covers
that handoff rather than building a redundant or conflicting one. The handoff "seams" between
composed components should ideally be invisible to the user — the whole feature should feel like
one coordinated thing, not a collection of disconnected fragments.
Do: map how components hand off to each other before building a new feature; check for
reuse/conflict against existing components before adding a new one.
Ask: would the user ever perceive the handoff between these two components as a seam? Does an
existing component already serve this handoff, making a new one redundant or conflicting?
(MI ch6)

### Model multi-step flows as routed screens with a progress indicator, not stacked dialogs `CMP-015`
For a multi-step user flow (e.g. checkout), route the user between real screens according to
their decisions and resulting state changes, backed by a persistent, accessible progress
indicator — rather than composing the flow out of successive stacked modal dialogs. A modal
implies the user stays on the same page and returns to it once dismissed, but in practice many
"modals" take the user elsewhere anyway, making them functionally equivalent to an intermediary
page with worse layout constraints and stacking problems.
When: use a modal only where a step genuinely keeps the user in the same context; otherwise route
to a real screen.
Do: use a landmark region + visually-hidden heading + ordered list of steps to expose progress
non-visually; mark the current step both visually and with hidden text (or aria-current if AT
support allows).
Trade-off: aria-current="step" is the more semantically "correct" ARIA-native approach but had
weaker assistive-technology support than a visually-hidden text fallback at time of writing.
(IC ch12)

### Reuse existing UI elements as feedback/state carriers instead of adding new ones `CMP-024`
Repurpose standard interface parts already on screen — scrollbars, cursors, progress bars,
tooltips, hover states — to carry additional feedback/state, instead of adding a new dedicated UI
element for it. Repurposing existing, already-understood UI elements communicates state without
growing the interface's surface area or adding new things for the user to learn.
When: avoid where the repurposed meaning would be non-obvious or conflict with the element's
primary role.
Trade-off: discoverability of a repurposed meaning vs. avoiding visual clutter from a new
dedicated element.
(MI ch4)
