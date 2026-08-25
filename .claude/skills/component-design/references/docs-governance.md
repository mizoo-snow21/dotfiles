# Documentation & Governance

How a pattern library is organized, documented, and governed so it stays a living single source
of truth. Route here when writing/reviewing pattern documentation or choosing/auditing a
governance model. Split from system-consistency.md (V2); provenance tags unchanged.

## Pattern-Library Organization and Documentation as Contract

### A design system is patterns plus practices, nested as a system-of-subsystems `SYS-001`
A design system is not just a component collection: it is a set of interconnected patterns
(repeatable interface elements) together with the practices for creating and using them,
organized under coherent rules to serve the product's purpose. It is itself a nested system —
composed of smaller subsystems (a layout rule, a logo-scaling rule) and nested inside larger ones
(the product, the team, the company). In an effective system, design intent, code
implementation, and pattern-library documentation for a given pattern stay mutually consistent.
Do: check that design intent, code, and documentation for a given pattern stay mutually
consistent, not treated as separate concerns.
Ask: are we treating "the components we built" as equivalent to "a design system," or is there a
coherent, documented set of practices governing them too?
(DS ch1)

### A pattern library documents the system; it is not the system `SYS-003`
A pattern library (the collection/documentation of patterns and usage guidelines) is not
equivalent to the design system behind it. Even a comprehensive, actively-maintained library does
not guarantee UX consistency or good design — it cannot fix patterns that are inherently poorly
designed, misapplied, or inconsistently interpreted, and a library built without the upstream
strategic work (principles, standardized patterns, governance) lacks real reusability behind its
documentation. Conversely, a product can be UX-consistent without a comprehensive library if its
underlying design language is coherent.
When: are we solving a consistency problem by improving the pattern library, when the real gap is
in the underlying principles/practices?
Ask: would we still call this "a consistent design system" if the library were deleted but the
principles/practices remained — or does the claim collapse?
(DS ch1,6,10)

### A style guide is narrower than a pattern library `SYS-004`
A style guide traditionally documents only stylistic/cognitive patterns (color, typography, icon
style), while a pattern library covers a broader scope: functional patterns plus cognitive
patterns plus the design principles that govern them, not just brand style.
(DS ch1)

### A shared component's real contract spans every discipline that touches it `SYS-005`
A seemingly simple shared component (e.g. a carousel) is organizationally complex because its
correct definition needs input from every discipline that touches it: business/editorial decides
content, copy keeps text within space constraints, visual/art direction keeps imagery legible at
every size, UX confirms interaction is intuitive, front-end handles responsiveness/accessibility/
performance, back-end wires it to data. A component's full specification is a cross-disciplinary
contract, not merely a visual or technical artifact.
Do: involve every discipline whose constraints affect the component in specifying and documenting
it.
(AD ch5)

### Documentation lives inside the pattern, not a separate discarded spec `SYS-006`
Documentation — including accessibility, performance, and other cross-discipline considerations —
should be attached directly to the living pattern itself, not kept in large separate
wireframe/spec documents that get discarded once a project ships. The design system should be
treated as the source that produces both the live product and its documentation, not a byproduct
documented after the fact.
Do: attach documentation and cross-discipline considerations directly to the living pattern, and
make changes to shared patterns in the design system first, letting them flow into whichever
applications/templates consume them.
(AD ch3,5)

### The pattern library should be the actual production source `SYS-007`
The most effective pattern libraries make the library itself the real code production consumes,
rather than a separate reference hand re-implemented elsewhere — both documentation and the live
application consume the same underlying pattern source, so a change made once is automatically
reflected everywhere. The same discipline applies to accessible/visual state: drive both from one
single source of truth rather than two parallel representations.
When: highly decentralized organizations building on wildly different technology stacks may not
realistically achieve full synchronization — even a partial shared library with some go-to
patterns is still valuable.
Do: source production front-end code directly from the pattern library rather than hand
re-implementing it elsewhere.
(AD ch3,5; IC ch8)

### Track a pattern's lineage in both directions `SYS-008`
A well-maintained pattern library tracks a pattern's full lineage both ways: what smaller
patterns it is composed of, and everywhere else it is itself used. This tells a team exactly
which other patterns and templates need retesting before a change ships, and over time surfaces
redundant or underused patterns to weed out. A library entry that omits usage context leaves the
team unable to judge how widely a change will ripple.
Do: record where and how each documented pattern is actually used, not just what it looks like,
and track both composition and usage locations.
Ask: if I change this pattern, which composed-of and composed-into patterns need retesting?
(AD ch1,3)

### Interface inventory before formalizing a shared pattern set `SYS-009`
Before designing/building a shared component system (or periodically thereafter), conduct a
comprehensive interface inventory: capture one instance of each unique UI pattern currently in
production, across categories, involving representatives from every discipline. This produces
concrete visual evidence of which patterns exist and which are redundant, and opens the naming
conversation without forcing the group to reach final naming consensus in the same short session.
Do: screenshot one instance of each unique pattern (not every occurrence), time-box the session,
and repeat it periodically rather than treating it as one-time.
Ask: are we disproportionately auditing high-visibility areas (homepage) and neglecting less
glamorous but equally real ones (support, error pages, legal)?
(AD ch4; DS ch3)

### The system's real center is a shared method, not tooling `SYS-041`
The core of an effective design system is not the tools it uses but a shared understanding among
the team of what design and UX approach fits their team and product; once that shared
understanding exists, tooling, documentation, and process follow from it.
(DS ch6)

### Bootstrapping a design system: five systematization steps `SYS-043`
Formally starting a design system breaks into five concrete steps: define guiding design
principles; define and standardize reusable patterns; build a pattern library; maintain a single
master design file of current patterns; refactor code/frontend toward a modular approach.
Do: define design principles before standardizing patterns, keep a single master file of
current, correct patterns, and refactor implementation code toward modularity to support the
patterns.
(DS ch7)

### Choose an organization scheme by validating it against real users `SYS-047`
Common organization schemes — alphabetical (flat, minimizes categorization disputes but degrades
once the list grows large), hierarchical/Atomic-Design-style (models composition/part-whole
relationships), and purpose/structure-based (groups by functional role) — each suit different
needs. The right choice depends on how the people who actually use the library conceptualize and
search for components: designers tend to think structurally, developers functionally, content
strategists blend both, so a scheme must reconcile multiple mental models rather than optimize
for one role. It is normal to revise the organization scheme over time as the library grows.
Do: validate an organization scheme against how real users search/think (card-sorting, usability
testing), explicitly decide and record ambiguous placement questions as a team, and define
explicit nesting rules for a hierarchical scheme.
Trade-off: alphabetical (zero categorization debate vs. poor browsability at scale); hierarchical
(explicit composition relationships vs. ill-fitting category boundaries); purpose-based (answers
"why would I use this" directly vs. typically only reached after iterating through other schemes).
(DS ch10)

### An unfindable pattern behaves like a nonexistent one `SYS-048`
When team members don't know a pattern exists, or can't find it in the library, they are likely
to create a duplicate or bypass the library entirely — even a diligently-built, actively
maintained library can fail to stop duplication this way as module count grows and searching
stops being faster than creating something new. A superficial or unmeaningful naming convention
degrades this further; the same mechanism (no shared vocabulary defined up front) causes
near-duplicates to accumulate even before a library exists at all. When a library search
genuinely comes up empty, proactively redirecting the user to the closest existing alternative
and explaining why prevents the duplicate from ever being built.
Do: provide explicit "closest alternative" guidance when an exact pattern match doesn't exist, at
the moment of the failed search.
Ask: can team members actually find the right existing pattern quickly, or is creating a new one
faster than searching? If we clean up today's duplicates, what stops the same accumulation from
reappearing once the library grows further?
(DS ch3,5,6,10)

### A borrowed hierarchy taxonomy is a tool, not a mandate `SYS-049`
The specific vocabulary of a hierarchy taxonomy (e.g. "atoms, molecules, organisms") isn't
sacred — what matters is that the chosen vocabulary conveys a hierarchy the team can internalize,
and teams have successfully substituted entirely different vocabulary while preserving the same
underlying structure. Applying a canonical hierarchy's category boundaries often surfaces
distinctions (e.g. "template" vs. "page") that are hard to use consistently and cause repeated
unproductive debate; collapse a distinction into fewer tiers when it doesn't resolve real
ambiguity quickly. More than roughly three tiers tends to create confusion, but a genuinely
load-bearing distinction (e.g. coarse-grained vs. fine-grained patterns) is worth keeping even
while simplifying everything else.
Do: adapt hierarchy naming to whatever vocabulary the organization will actually adopt, collapse
levels that don't carry real distinguishing value, and keep a coarse/fine-grained distinction
even when simplifying other levels.
(AD ch2; DS ch10)

### Documentation grain, addition rigor, and drift tolerance should track governance strictness `SYS-050`
How strictly a pattern library documents patterns (fine-grained atomic components vs. larger
prescriptive flows/templates) is itself a governance decision: documenting bigger units signals
"use this as-is," documenting smaller units signals "compose freely," and it should match the
system's stated governance stance. The same logic extends to how rigorous the process for adding
new patterns should be, and to how much drift between the library and the actual state of
design/code a team should tolerate — tight sync matters more in strict, centrally-governed
systems, and higher drift tolerance is acceptable in more permissive/distributed ones.
Do: define at minimum a standard submission format and a recurring review cadence for adding new
patterns, regardless of how strict the overall system is.
Ask: does the documentation grain size, addition rigor, and sync-drift tolerance all match how
strictly this system is governed overall?
(DS ch10)

### Document a minimum core: name, purpose, example, variations `SYS-051`
When documenting a pattern under limited time/resources, prioritize four baseline fields first:
name, purpose (what it is / why you'd use it), example (visual + code), and variations (what
forms it can take) — the essential questions someone browsing needs answered to decide whether
and how to reuse a pattern. The purpose statement specifically should be expressible in one or
two sentences; difficulty compressing it to that length is itself a signal the purpose may not be
clear yet.
Do: prioritize name, purpose, example, and variations before other documentation fields, and
keep purpose statements short and concrete.
Ask: can this pattern's purpose be stated in one or two sentences?
(DS ch10)

### Pair purpose with content-team-validated usage constraints `SYS-052`
Beyond stating a pattern's purpose, effective documentation adds concrete recommended
constraints for using it well (e.g. "max 3 lines per fact," "max 12 facts"), and defining these
numeric/structural constraints requires collaboration with the content team, not design/
engineering alone.
Do: define concrete usage constraints jointly with the content team.
(DS ch10)

### Document variations so a reader knows which one to use, not just that options exist `SYS-053`
Displaying all variations of a pattern together makes it easy to see at a glance which exist, but
that display must be paired with an explicit explanation of what differentiates each one, or a
viewer can see options exist without knowing which to choose. For demonstrating a pattern, live
interactive code is usually best since it shows real behavior/interaction/animation, but static
images or GIFs are better for effects that can't be reproduced live or need to show one specific
state. A generic example (placeholder content indistinguishable from what any other pattern might
show) fails to communicate what makes a pattern's purpose distinct.
When: does this example need to show live interactive behavior, or a specific/hard-to-reproduce
static state?
Do: explain what differentiates each variation, not just display them side by side, and make
example content clearly demonstrate the pattern's intended, distinguishing use.
(DS ch10; DI ch8)

### As a library matures, extend documentation with versioning, credit, and cross-links `SYS-054`
Beyond the baseline name/purpose/example/variations, useful additional documentation fields
include component versioning (what changed vs. prior versions, especially API/UI changes and
deprecated/replacement elements), a list of contributors, and links to related patterns.
(DS ch10)

### Document a value's usage role — treat semantic values as a system-wide contract `SYS-055`
Listing a category's constituent values (a color palette, a type scale) is not enough: also
specify how and where each value is meant to be used, ideally paired with concrete do/don't
examples (e.g. blue is used for informational/link elements but never buttons, to avoid confusion
with the primary interactive color). Standardizing a shared value set alone does not guarantee
consistent usage. When a value signals something functional (e.g. this color means
"interactive"), that becomes an implicit contract users rely on across the whole interface —
reusing the same meaningful value for an unrelated, non-functional purpose elsewhere breaks that
contract and creates false expectations.
Do: document usage role and do/don't examples for each value, and either make a
functionally-colored element genuinely interactive or use a different, non-meaningful value for
decorative-only elements.
Ask: does any other element already use this exact value to signal a different (or no) function?
Will reusing it here create a false expectation?
(DS ch9,10)

### Cross-reference appearance and component systems bidirectionally `SYS-056`
Appearance (color, typography, etc.) and components/patterns are documented as separate systems
for manageability but are tightly coupled in practice; documentation should let a reader navigate
from a component to the appearance values it uses, and from an appearance value to the components
that use it, entering from either a global appearance page or an individual component's own doc
page. Splitting a component's appearance/style documentation onto a separate page without a
strong cross-reference weakens the documentation by hiding this connection.
Do: let readers reach appearance values from a component page and vice versa, and support both a
system-wide appearance overview and a per-component view.
(DS ch10)

### Define interaction-state behavior once, system-wide `SYS-057`
→ Canonical: `VST-009` in variants-states.md (same rule, same DS ch10 source, plus the guard
about when a different kind of control legitimately gets a different treatment). (DS ch10)

### A mature library can take over single-source-of-truth from a master file `SYS-064`
As a pattern library matures, some teams find it takes over the "single source of truth" role
previously held by a master design UI kit, reducing pressure to keep that master file perfectly
current — a master file can then be limited to core, rarely-changing elements, while the pattern
library becomes designers' primary reference for current/detailed patterns.
(DS ch10)

### A shared collaborative document can serve as an MVP pattern library `SYS-065`
A shared collaborative document (e.g. a shared folder of docs) can serve as an MVP-level pattern
library: everyone on the team can access, comment, and edit it using familiar tools, encouraging
participation, at the cost of the structure and interactivity dedicated pattern-library tooling
would provide.
Trade-off: low-friction accessibility vs. structured/interactive presentation.
(DS ch10)

### Define a pattern's semantic role before its visual specifics `SYS-067`
When establishing a new pattern, first define it abstractly: what content/purpose it serves,
where in the experience it appears, who owns/curates its content, and how it behaves in
different states or contexts. Before finalizing visual design or markup, sketch the pattern's
content structure — list essential content elements, determine hierarchy/grouping, and decide
which elements are required vs. optional. Doing this collaboratively (design, engineering,
content strategists together) lets designers and engineers work in parallel afterward without
producing surprising, divergent results, because both sides share a model of how the pattern is
built.
Do: articulate a pattern's purpose, context, content owner, and state-dependent behavior before
detailing layout/visuals, and sketch content structure with designers, engineers, and content
strategists together.
Ask: what content does this pattern structurally require vs. merely accept optionally? Have we
agreed on the content hierarchy before starting visual or code work?
(AD ch2,4; DS ch3)

### Treat expected content as a testable hypothesis, not the starting point `SYS-068`
Designing a pattern content-first (building the module around one particular piece of content,
then hoping it generalizes) risks a fragile, over-fitted module. Instead, start from the
pattern's purpose/target action, define the kind of content it should hold as an explicit
hypothesis, then design and test against it. When real content doesn't fit, the cause is one of
three distinct things, each pointing to a different fix: the purpose was never precisely defined
(revisit the target action); the design doesn't actually serve the intended purpose (try a
different design); or mismatched content is being forced into an unsuitable pattern (revise the
content, or use a different pattern).
Trade-off: design speed (content-first) vs. pattern robustness (purpose-first,
content-as-hypothesis).
Ask: was this pattern's target behavior/purpose ever made explicit, or did we start from a
specific piece of content? When content doesn't fit, is the cause an undefined purpose, a design
that doesn't serve the purpose, or genuinely mismatched content?
(DS ch3)

### Run the systematization audit after core UX settles, at consistent granularity `SYS-069`
A purpose-directed inventory and pattern-definition process works best after foundational UX
work (research, content strategy, information architecture) is already settled; if the interface
has known fundamental usability flaws or a major redesign is imminent, run that work first. While
grouping existing elements into pattern candidates, keep every group at a consistent level of
granularity — an object-level module (a "book list") should not be grouped with an action-level
control (a "reserve" button). The same purpose-group-define-approve process repeats separately
for each cognitive-pattern category, with an integration pass afterward to reconcile overlaps.
Start from core, foundational patterns and expand to peripheral ones, and repeat the exercise
periodically as the system evolves.
When: the interface has known fundamental usability problems, or a major redesign is imminent —
clarify the new design direction before auditing existing patterns.
Do: begin with core patterns before peripheral ones, run one pattern category's inventory at a
time, and list concrete roles a property plays rather than one vague descriptive sentence.
(DS ch8,9)

### Reduce an organically-grown value set to what's functionally necessary `SYS-070`
When narrowing an organically-grown style-value set (e.g. a color palette that accumulated 62
distinct greys), starting from each value's actual purpose reveals how many distinct values are
truly needed. Where multiple variations of a value are genuinely needed, specify one base value
plus defined increments from it (e.g. 20% lighter/darker than base) rather than an arbitrary list
of unrelated values — a consistent base is easier to remember and reason about, and this
generalizes to other categories (a base font size, a base spacing unit). Separately, mapping a
pattern's underlying content to style names while standardizing size variation lets a single
pattern adapt to more content types, increasing how much it can be reused.
When: a product that legitimately needs light/dark theme support, or multiple
data-visualization series colors, may need more tonal variation than a single-theme product.
Do: define a base value plus systematic increments for any property that legitimately needs
multiple variations, and treat accessibility contrast-checking as one of the steps of defining a
palette, not a separate later audit.
Trade-off: more value options make the system more complex and harder to keep consistent; too
few can be limiting for multi-theme support or data visualization.
Ask: is each value variation traceable to an actual, distinct purpose, or is it accidental drift?
(DS ch8,9)
## Governance Axes and Pattern Promotion

### Three independent axes describe a system's operating profile `SYS-037`
A design system's approach can be plotted along three largely independent, continuous axes: rule
strictness (strict ↔ loose), organizational distribution (centralized ↔ distributed), and
component modularity — each a spectrum, not a binary, with no fixed position universally correct.
A system's position isn't fixed either: it can shift as organizational priorities change (a team
that starts centralized/integrated can deliberately move toward distributed/modular, or tighten
its rules as it begins to prioritize consistency more).
Ask: where does this system currently sit on rule strictness and organizational distribution —
and is that position deliberate? Is our current strictness/organization posture still the right
one, or has it drifted without a deliberate decision behind the drift?
(DS ch6)

### Centralized governance: one accountable owner, trading bottleneck risk for consistency `SYS-038`
In a centralized model, rules and patterns are defined and managed primarily by one designated
group, who hold review/veto authority over shared patterns. This gives the system clear
accountability and focused creative direction, but risks that group becoming a bottleneck that
slows the wider product lifecycle — especially for small organizations that cannot spare
dedicated full-time members purely for system upkeep.
Do: designate a specific group as pattern owner with review/veto rights over shared patterns.
Trade-off: clear accountability and consistent creative direction, at the cost of concentrating
authority (and bottleneck risk) in one group.
(DS ch6)

### Distributed governance: shared ownership, prone to silent stalling without a named owner `SYS-039`
In a distributed model, everyone who uses the system participates in maintaining and evolving
it, and individual teams have autonomy — no single small group is a dependency, so the system can
be more resilient and agile. But initial enthusiasm from all members does not guarantee
sustained, roughly-equal contribution: without anyone formally responsible for upkeep, work
concentrates unevenly in a few individuals and can stall entirely without anyone noticing.
When: fits small companies that cannot dedicate a full-time team to the design system alone,
with many willing contributors already in place.
Trade-off: higher agility/flexibility and no single point of failure, versus more difficulty
keeping creative direction coherent without drift.
Ask: is contribution to the shared pattern library actually staying balanced across the team
over time, or concentrating in a few people?
(DS ch6)

### Neither governance model is universally better; fit to the team's culture `SYS-040`
No governance approach (centralized/distributed, strict/loose) is free of shortcomings, and none
is objectively superior — which one works depends on the team's existing culture, particularly
how strongly individual sub-teams already hold their own design opinions, and how the team
already communicates and makes decisions (Conway's Law: organizations tend to produce designs
mirroring their own communication structures). Governance strictness and modularization scope
both tend to scale with team/organization size, though a small team can run an unusually strict
system and a large company can deliberately keep a loose one. The deciding factor is not which
approach looks "best" in the abstract or worked for another team, but which approach's specific
weaknesses this particular team is best equipped to handle.
Ask: do sub-teams already have strong, persistent opinions about design decisions in their area?
Are we adopting this governance model because it fits our team, or because it worked well for
another team?
(DS ch6)

### Strict and loose governance are a genuine tradeoff, not a maturity ladder `SYS-042`
A strict model (e.g. Airbnb's DLS) centralizes ownership in a dedicated cross-platform team,
defines modules with high precision, treats design-code sync as a first-priority tooled
discipline, auto-generates documentation from the same source files used for design/code, and
routes new-pattern proposals through an approval process that actively checks for near-duplicates
first, deliberately keeping new-pattern creation frequency low. A loose model (e.g. TED)
deliberately deprioritizes visual consistency for brand-feel and per-page effectiveness —
deviating from established patterns is accepted if it serves a strong enough purpose, working
from simple sketches and a small, deliberately-incomplete pattern collection, on the explicit
principle that a design decision should never be justified purely by "that's how we've always
done it." Neither side is objectively better: the strict model trades flexibility for
predictability and reuse; the loose model trades predictability for per-context optimization, but
only holds together if the team's coherence genuinely comes from deep shared culture, not
enforced process — a loose system that works for one team does not automatically transfer to
another team lacking that same depth of shared purpose.
Do: route new-component proposals through a step that actively checks for existing near-
duplicates before approving something genuinely new, and generate documentation from the same
source files used for design/code where possible.
Trade-off: strict = high predictability/reuse, lower per-context optimization unless deliberately
preserved; loose = high per-context optimization and experimentation freedom, lower central
consistency, and only safe with genuinely deep shared team culture.
Ask: is our system's coherence coming from enforced rules, from genuinely shared team
understanding, or neither?
(DS ch6)

### A misfitting shared pattern is a governance decision, not a silent local override `SYS-044`
When an existing shared pattern doesn't quite work for a specific application, a design system
needs an explicit decision path: should the pattern be modified for everyone, should the team be
redirected to a different existing pattern that already fits, or does the situation genuinely
warrant a new pattern? This should be a deliberate governance decision, not resolved ad hoc by
whichever application hits the friction first.
Ask: does the pattern get modified for everyone, should we recommend a different existing
pattern instead, or does a genuinely new pattern need to be created?
(AD ch5)

### A healthy system needs bidirectional feedback between patterns and applications `SYS-045`
A healthy design system relies on continuous two-way feedback: shared patterns inform how
individual applications get built, and needs discovered while building specific applications
should in turn inform and evolve the shared system. Treating the system as a one-way, top-down
source that applications must simply consume, with no feedback channel back into it, risks the
system drifting out of sync with real application needs.
Do: maintain frequent communication between whoever maintains shared patterns and whoever
consumes them, and feed friction/needs discovered in specific applications back into the shared
pattern set rather than just applying local patches.
(AD ch5)

### Two viable pattern-promotion policies, each with a specific failure condition `SYS-059`
→ Canonical: `BND-012` in boundaries.md (immediate-add with strict dedup review vs. add-on-reuse
with pre-promotion discoverability — same two policies and failure conditions). (DS ch4)

### Generality of purpose, not visual similarity, is the promotion test `SYS-060`
→ Canonical: `BND-011` in boundaries.md (second-independent-need discipline; the underlying test
is generality of intended purpose, not visual similarity). (AD ch2; DS ch4)

### Assign explicit ownership: curator and producer are the two base models `SYS-061`
A pattern library needs an explicit maintenance/update cadence and clear ownership, beyond just
an addition process, chosen deliberately to match the team's structure — no single ownership
model is universally effective. In a curator model, the whole organization can propose patterns;
the design-system team defines requirements/review criteria and sends submissions back to their
original author for revision rather than editing directly — suited to looser, distributed
structures. In a producer model, the design-system team itself creates most patterns, working
closely with product teams and holding final say — suited to stricter, centralized structures.
Whichever model is used, the design-system team should be a proactive partner to contributing
teams, not a reactive gatekeeper. Restricting edit access to only certain roles (e.g. only
engineers, not designers) weakens the excluded group's sense of ownership over time and
concentrates the maintenance burden unfairly.
Do: assign explicit ownership for library curation and update cadence, engage contributing teams
proactively and early, and give contributing roles direct edit access to pattern documentation.
Trade-off: curator model = broad distributed contribution vs. less centralized quality control;
producer model = centralized quality control vs. less breadth of contribution.
(DS ch10)

### Cross-departmental libraries outlast single-team ones, synced by naming not mirroring `SYS-062`
Pattern libraries built and maintained with contribution across multiple disciplines/departments
tend to be more resilient and longer-lived than libraries serving only one department's needs. A
library built without deep, continuous designer involvement risks becoming technically rigid: new
work either gets force-fit into ill-suited existing patterns, or gets built ad hoc outside the
system. Keeping code, design files, and the pattern library in sync does not require literally
mirroring every pattern across all three — what matters is applying the same approach to naming,
folder/file structure, and shared conceptual understanding of purpose consistently across them.
Do: involve multiple departments in building and maintaining the pattern library, and apply the
same naming and structural approach across code, design files, and the library rather than
aiming for literal pattern-for-pattern mirroring.
(DS ch10)

### Perfect synchronization is unrealistic — accept bounded drift `SYS-063`
Keeping a pattern library and product code perfectly synchronized is very difficult, and treating
perfect sync as mandatory is itself counterproductive: a design language keeps evolving, so at
any moment multiple versions of it coexist, and demanding perfect synchronization would make the
system too rigid to function or consume disproportionate team effort chasing full parity.
Do: accept some bounded drift between the pattern library and current design/code as normal.
Trade-off: synchronization rigor vs. system flexibility to evolve.
(DS ch10)
