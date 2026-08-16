# System Consistency, Naming & Documentation

This file serves decisions about keeping a component system coherent as it grows: how to name a
pattern so its scope and purpose stay legible, how to keep functional and cognitive (style)
patterns from colliding, when a fix belongs at the pattern level instead of a one-off patch, and
how a pattern library should be organized, governed, and documented so it stays a living single
source of truth rather than a drifting reference. Route here when naming or renaming a component,
judging whether a stylistic exception threatens brand consistency, choosing or auditing a
pattern-library governance model, or writing/reviewing pattern documentation.

## Contents
- Naming as a Boundary Contract
- Shared Language
- Design Principles as Decision Criteria
- Perceptual and Cognitive Patterns
- Pattern-Library Organization and Documentation as Contract
- Governance Axes and Pattern Promotion
- Consistency Mechanisms

## Naming as a Boundary Contract

### Naming determines existence and reuse boundary `SYS-019`
An interface object without a meaningful, shared name is not a genuinely reusable part of the
system even if it exists in code. Naming it after a surface trait, a specific page, or a specific
content type locks it to that expression and discourages reuse elsewhere; vague category names
(e.g. "General") likewise defeat findability even when the underlying markup is simple.
Ask: would this name still make sense if the pattern were reused somewhere we haven't thought of
yet?
(DS ch5; IC ch10; AD ch5)

### A good name encodes its own usage guidance `SYS-020`
The best names hint at where/how a pattern should be used through the name/metaphor itself, so
the pattern doesn't have to separately assert its rules — e.g. "Minions" (many per page) vs.
"Boss" (exactly one). A name describing only form or shape (e.g. "Showcase") invites misuse and
duplication; naming for function ("Fact Grid") makes intended use unambiguous. Naming also
communicates ownership — a name should track who or what actually drives a component's behavior,
not just its visual form.
Ask: can someone infer this pattern's purpose from its name alone?
(DS ch5,10; IC ch9)

### Naming difficulty is a diagnostic, not a wordsmithing problem `SYS-021`
When no appropriate name comes to mind for a new pattern, that signals something wrong with the
pattern's definition, not a labeling gap: either its purpose is unclear or it duplicates a
purpose that already exists. The same diagnostic applies to content-section titles — an
un-nameable section signals the grouping itself doesn't match the content's natural structure (a
recurring "Other/Misc" category is a warning sign), and the fix is to regroup, not force a title
onto a bad grouping.
When: an "Other" catch-all is sometimes genuinely necessary and not itself a sign of a problem.
Ask: why can't we name this — is the purpose actually unclear, or does it duplicate an existing
module?
(DS ch5; DI ch4)

### Memorable names come from user vocabulary, cross-domain metaphor, and personality `SYS-022`
Naming a component after the vocabulary users themselves already use for it forces the team to
think from the user's perspective throughout the component's life. Metaphors borrowed from other
domains give the team something familiar to associate a module with; names with genuine
personality build a mutually-reinforcing family (a large CTA "Boss" pairs naturally with small
secondary "Minions"). A name lacking any evocative metaphor or personality is hard to remember,
and hard-to-remember names correlate with a pattern falling out of use and a near-duplicate being
created in its place — regardless of how technically precise the original name was.
Trade-off: user-vocabulary naming adds a small extra naming burden for developers, in exchange
for keeping the team user-perspective-aware.
(DS ch5)

### Naming is bounded, cross-role, and user-validated `SYS-023`
Naming as a cross-role team (not just the engineer who wrote the code) surfaces a more accurate
understanding of a module's true purpose, since different roles read it through different
lenses; it is a UX decision best made at the design stage, not left to whichever engineer
implements the component. The discussion should stay bounded, though — too many opinions produce
a vague name — so gather input broadly but leave the final call to the specific pair (e.g.
designer-developer) who built the module. Validate the chosen name against users' actual mental
model where feasible (e.g. card-sorting), which can reveal a name/appearance that doesn't match
user behavior at all.
Do: involve more than one role in naming, time-box the discussion, designate a final
decision-owner, and validate against real users where feasible.
Trade-off: broader input improves purpose-accuracy but risks vagueness if not bounded by a clear
decision-owner.
(DS ch5,8)

### A name should track a pattern's actual specificity `SYS-024`
A name should reflect where a pattern sits on the specific-to-generic spectrum and signal
whether it's safe to reuse elsewhere or intentionally scoped to one context. When unsure, start
specific; if a pattern is later reused more broadly than intended, rename it to reflect the new
scope — a stale name misleads the team about whether reuse is safe.
Do: rename a pattern when its actual reuse scope no longer matches its original name.
(DS ch8)

### A name is real only once it displaces ad hoc description `SYS-025`
A pattern isn't a genuinely functional part of the shared design language until the team
actually uses the approved name in place of whatever ad hoc description was used before naming.
Consistent conversational use of the approved name — not the act of choosing it — is the real
completion criterion, and is what keeps naming in design files and code aligned with how the
team actually talks about the component.
Ask: has the team's actual conversational habit switched to the approved name, or are people
still describing it ad hoc?
(DS ch5)

## Shared Language

### Shared language requires agreement on purpose and context, not just names `SYS-026`
A team sharing a vocabulary isn't enough if members interpret the same term differently — true
shared language requires agreement on a pattern's name AND its purpose, the context it's used
in, and when it should be used, or a nominally "unified" language actually diverges in practice.
Patterns and design principles alone are not sufficient for team consistency: a product built by
many contributors stays unified only if contributors share the same principles, aligned brand
vision, common design/frontend approach, and knowledge of which patterns are effective and why —
not merely a shared component library.
Ask: does everyone agree not just on the pattern's name, but on why it exists, what problem it
solves, and when to use it?
(DS ch1,4,5; AD ch1)

### An explicit design language reframes debates around necessity, not pixels `SYS-028`
Once a design language is made explicit and shared, a small validated improvement discovered in
one place can propagate to every pattern that shares that language, instead of being adjusted
one instance at a time. It also shifts team conversations from an element's pixel-level
appearance to whether a pattern is needed at all, reasoning in terms of context, purpose, and
usage.
Trade-off: investment in making the language explicit vs. the ongoing efficiency gained from
system-wide leverage.
(DS ch1)

### Visibility drives everyday adoption of the pattern language `SYS-073`
Naming shared patterns as a team is necessary but not sufficient — the language must be actively
spread across the whole team so it gets used in every relevant context. Displaying the product's
most characteristic patterns labeled, in a space the team encounters casually and often (not
only a documentation site nobody opens proactively), lowers the barrier to participation and
helps even initially uninterested members gradually engage.
Do: make the current pattern language visible somewhere the team encounters casually and often,
not only in documentation nobody opens proactively.
(DS ch5)

## Design Principles as Decision Criteria

### Principles are a decision criterion at every level, and co-evolve with patterns `SYS-011`
Design principles function as the basis for decisions at every level of a product — which
feature/pattern to build first, how a flow should work, how a visual detail should be resolved —
not only high-level branding calls. They aren't a one-time upstream deliverable either: as
functional patterns mature, they in turn shape and refine the principles, in continuous two-way
influence over a product's life. For principles to work this way, all team members need to
recognize and agree on them, or priorities diverge between individuals.
Ask: does this decision — from feature scope down to a button detail — trace back to one of our
stated design principles? Have mature patterns fed back into revising the principles, or are they
still treated as fixed once written?
(DS ch1,2)

### Four criteria make a principle actually usable `SYS-012`
An effective design principle is (1) truthful and essential — it defines what a generic quality
word (innovative, convenient, fun) concretely means for THIS product, not something any
competitor could equally claim; (2) practical and actionable — it discriminates one design
choice from another, ideally paired with a concrete interface example; (3) has a point of view —
it explicitly ranks competing values so the team can resolve conflicts; (4) memorable and few in
number — roughly 3-5 principles, since one nobody can recall in daily work stops being a real
decision tool.
Do: pair each principle with a real interface example, rank principles explicitly when they can
conflict, and keep the set to roughly 3-5 items.
Trade-off: ranking every principle equally feels fair to every value but forfeits the clarity
gained from an explicit priority order when principles conflict in practice.
Ask: if we removed this principle's specific product context, could any competitor claim the
same principle? If it conflicted with another on a real decision, which one wins, and have we
written that down?
(DS ch2)

### Principles can be outcome-facing or process-facing; per-team sets must reconcile `SYS-013`
Design principles vary in what they optimize for: some are outcome/brand-facing ("clear",
"vibrant"), others are process/behavior-facing, describing how the team should work ("be
efficient", "iterate"). Organizations also differ in scope — one shared principle set
system-wide, versus per-team principles — but per-team sets allowed to diverge without any
mechanism keeping them traceable to one underlying system risk fragmenting the product's
experience across surfaces.
Trade-off: per-team principle autonomy (context fit) vs. cross-system consistency (shared
identity).
(DS ch2)

### Deriving principles from scratch: vision, independent answers, the builders, re-validation `SYS-014`
When a team cannot articulate design principles from scratch, start from the product's broader
vision/values and ask how principles could support it. To surface candidates, ask team members
individually — across roles and tenure — what "great design" means for the product, pointing to
concrete interface examples, then look for themes that repeat; this both surfaces genuine shared
understanding and reveals where mental models diverge. Principles should be written primarily
for the people building the product, not as brand marketing copy, and must be periodically
re-tested against real decisions or sharp, specific principles drift into vagueness and lose the
team's trust.
Do: compare answers across different roles and tenure lengths, not just designers, and re-check
principles against real decisions periodically.
(DS ch2)

### Define goal and ethos before functional and cognitive patterns `SYS-015`
Before defining a product's functional and cognitive patterns, first establish its purpose/goal
in one clear sentence and its ethos — the values/spirit it should express. The goal determines
which functional patterns to design for; the ethos determines the cognitive pattern set (tone,
imagery, color, typography) used to express brand character. Two products in the same functional
domain can end up with entirely different pattern languages because their goals and ethos
differ.
Ask: what is this product's purpose in one sentence, and what ethos should its cognitive
patterns express?
(DS ch1)

### Sub-domain principles must stay specific, not generic boilerplate `SYS-016`
Just as overall design principles must avoid vague, generic statements, principles for a
specific pattern area (voice and tone, motion, color) must stay concrete and specific to that
area rather than reused boilerplate ("be friendly") that could apply to any product.
Systematizing any cognitive-pattern category should end with explicit principles governing its
use — general ones (e.g. "always use accessible contrast") alongside brand-specific ones (e.g.
which colors may dominate large areas vs. only sparingly) — giving the team something to reason
from and refer back to.
Do: write principles specific enough to guide an actual decision, for each pattern category
separately, and document not just what a color/pattern is but where it should and should not be
used, and why.
(DS ch9)

## Perceptual and Cognitive Patterns

### Functional vs. cognitive patterns is the core boundary axis `SYS-002`
Design patterns split into two kinds: functional patterns (behavior/module — buttons, headers,
form elements, menus; tied to what a user needs and does) and cognitive/perceptual patterns
(style/expression — color, typography, icon style, spacing, shape, animation, sound, tone; tied
to how a user feels and perceives). A functional pattern is fundamentally an interface object; a
cognitive pattern is style layered onto that object, not a separate object in its own right.
When: is this difference a change in behavior/interactive part (functional) or a change in
appearance/emotional tone only (cognitive)?
Do: do not treat a purely stylistic variant (color, font, spacing) as if it required a new
functional module/component.
(DS ch1,3,4)

### Qualitative motion principles are a legitimate fallback before exact values exist `SYS-017`
Before defining concrete animation (or other cognitive-pattern) values, first articulate the
purpose motion should serve (softening transitions, prompting a next action, revealing content)
and the mood it should convey; audit existing motion by capturing real examples and grouping by
purpose/mood. When a team isn't yet confident defining exact timing/easing values, it's
acceptable to start with broad qualitative principles instead (e.g. "only animate the single
most important moment") rather than omit motion guidance entirely. Anchoring principles to a
shared spatial metaphor (elements as physical objects) gives designers and engineers a common
mental model for predicting correct motion without an explicit rule for every case.
Do: state a pattern's role/purpose before choosing timing/easing values, capture existing
instances and group by purpose/mood first, and write qualitative principles as an interim step
rather than skipping guidance entirely.
(DS ch9)

### Voice/tone is authored with interaction design, documented as method `SYS-018`
Voice-and-tone guidelines produced by a team not involved in defining interactions and patterns
tend to produce inconsistent tone, or a tone mismatched to context. Effective voice/tone
documentation gives actionable how-to guidance for writing copy in context ("keep content
relevant to what the user is doing", "never leave the user hanging", "explain what happened and
how to fix it") rather than only listing adjectives like "friendly" or "simple".
Do: involve people who define interaction patterns in writing voice/tone guidelines, and write
procedural, situational guidance rather than just adjective lists.
(DS ch9)

### Cognitive patterns stitch an independently-built system into one felt whole `SYS-030`
Cognitive patterns (tone, typography, palette, shape, motion, and critically the ratios and
relationships between these elements, not the elements in isolation) are what connect a system's
independently-built parts into one perceived identity. Two products can share similar palettes
and shapes yet feel completely distinct because identity comes from proportion and relationship,
not raw constituent elements; unifying headings or colors module-wide is not by itself
sufficient. This connective role extends across platform/context boundaries — even under a rigid
native-platform spec, and down to a single, consistently-reused fine-grained interaction detail
kept identical across web, iOS, Android, and third-party clients.
Do: study the ratios and combinations that create the intended mood, not just the constituent
tokens, and keep one or two small, highly-recognizable interaction details byte-for-byte
consistent across every surface.
Ask: if a user has never seen this module before, will its cognitive patterns still tell them it
belongs to this product? Have we specified not just which colors/fonts/shapes are allowed, but
their proportions and how they relate?
(DS ch4; MI ch6)

### Consistency and brand distinctiveness are a tunable balance `SYS-031`
Too many stylistic exceptions weaken a brand, but over-indexing on consistency also suppresses
distinctiveness and can produce a generic, inflexible system — perfect internal consistency is
not automatically the same as "correctly matching the brand." A strict system needs deliberately
preserved room for creative experimentation, and team members must actually understand the
underlying rules (via clear, persuasive documentation) to meaningfully deviate from them for good
reason — otherwise rules just get ignored or silently rewritten.
When: are we optimizing for consistency at the expense of the details that actually created this
brand's distinctive feel?
Trade-off: more exceptions → richer brand expression but weaker system predictability; more
consistency → stronger predictability but risk of a generic, flattened brand feel.
(DS ch4,6)

### Reserve space for signature moments, trialed small before wider rollout `SYS-032`
A design system needs deliberately preserved space to nurture, protect, and evolve small,
highly-crafted "signature moment" interactions (a refined loading animation, a distinctive
sound), most powerful when they carry meaning connected to the brand rather than being arbitrary
decoration. The low-risk way to introduce a new cognitive pattern is to trial it first in one
small, inconspicuous element, staying conscious of why it deviates from current practice; if it
works, extend its defining traits to other relevant areas — a changed pattern otherwise reads as
foreign even if well-received in isolation — and scope rollout to the specific role it's meant to
play rather than blanket-applying it everywhere.
Ask: does this micro-interaction detail carry meaning connected to the brand, or is it arbitrary
decoration? Have we propagated this new pattern's defining traits anywhere else yet, or does it
still stand alone?
(DS ch4)

### Cognitive changes escape the scrutiny functional changes get `SYS-033`
Cognitive patterns are often perceived by stakeholders as "mere style or decoration," so
changing them draws far less internal pushback than an interaction-flow change would, making it
easy for a business requirement to introduce a brand-mismatched visual element with little
scrutiny. A related trap: an exception approved as harmless because of low current
volume/frequency can become a de facto permanent fixture, drifting from "a small highlight" into
something that clashes with the brand's intended tone as its volume grows — by which point it is
already embedded and hard to deprioritize removing.
When: re-evaluate frequency-justified exceptions periodically as their actual volume changes,
rather than approving them permanently based on today's low frequency.
Ask: are we treating this "just visual" request with the same brand scrutiny we'd apply to a
functional change? What happens to this exception's brand impact if its frequency grows 10x?
(DS ch4)

### Recognizing a symbolic visual attribute enables deliberate, not accidental, change `SYS-036`
The same value (a color, or a shape used in core navigation) applied at different proportions
produces an entirely different perceived brand feel, so intended proportional usage should be
documented alongside the value itself, not just the value in isolation. If a visual attribute is
identified as symbolic/brand-defining, recognizing it as such helps a team judge the right
balance between making improvements and preserving the product's existing character — if the
actual goal is to change the product's identity, that should be a deliberate redesign decision
made before a systematization pass, not an accidental byproduct of one.
Do: document intended proportional usage alongside each value, and make deliberate redesign
decisions before starting a systematization pass, not during it.
(DS ch9,10)

### Cross-category cognitive relationships must be documented and reconciled `SYS-058`
For a set of cognitive patterns (color, typography, spacing, voice/tone, motion) to function as
one system, their relationships to each other must be explicitly shown — how color relates to
color, typography to spacing, voice/tone to appearance — and each domain's individually-consistent
system must ultimately be evaluated together for the overall impression it gives, re-tied to the
product's purpose. One concrete mechanism: bundle typography-contrast level and spacing level
into named "density" categories tied to a functional purpose (e.g. Spacious/Regular/Compact),
since pre-defined discrete spacing values alone don't guarantee consistent felt visual density if
typography contrast varies independently.
Do: explicitly document how different pattern categories relate to and constrain each other, and
define named density (or similar bundled) categories tied to functional purpose rather than
relying on independent tokens alone.
Ask: does the combination of typography + layout + color + motion + tone read as one coherent
impression?
(DS ch9,10)

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
Interaction states (hover, focus, selected, disabled) are usually documented per component
individually, but that treatment risks inconsistency across component types — does hover on a
secondary link, icon button, ghost button, and tab all change the same way? An explicit, unified
state-behavior definition, applied consistently whenever a new interactive element is introduced,
avoids ad hoc per-component treatment.
Do: define interaction-state rules once at the system level and reference them from each
component.
Ask: is this component's hover/focus/selected/disabled treatment consistent with other
interactive components, or ad hoc?
(DS ch10)

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
Two common criteria for deciding when a new element becomes an official library pattern: (1) add
every new element immediately, paired with a strict duplicate-check/review process to prevent
redundant patterns — fits stricter systems, favors completeness; (2) add an element only after it
has actually been reused a few times, keeping the library lean — but this only works if all
created elements, even ones not yet promoted, stay fully visible/discoverable to the team, or it
reintroduces the same duplicate-creation failure the policy was meant to avoid.
Trade-off: library completeness/strict dedup discipline vs. leanness contingent on
pre-promotion discoverability holding up in practice.
(DS ch10)

### Generality of purpose, not visual similarity, is the promotion test `SYS-060`
The right criterion for adding a new component to the shared pattern library is the generality of
its intended purpose, not how visually similar it looks to existing patterns: elements defined
for a general/broad purpose are added because they're likely to be reused; elements built for a
narrow, time-boxed, or campaign-specific purpose are treated as one-off, non-system components
even if visually similar to existing patterns — with an explicit path to redefine and promote a
one-off element later if broader need genuinely emerges.
When: an exception exists for a one-off element that later proves useful beyond its original
narrow purpose.
Do: treat narrow-purpose, campaign-specific elements as one-off even if visually similar to
system patterns, and promote a one-off element into the library only if broader need emerges
later.
Ask: was this element defined for a general/broad purpose, or a narrow/time-boxed one?
(DS ch10)

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

## Consistency Mechanisms

### Fix a shared-pattern defect at the system level, not per-instance `SYS-010`
When a defect or improvement opportunity is found in one specific instance of a shared pattern,
the instinctive local fix is to patch just that occurrence. Because the underlying pattern is
shared, the better default is to fix it once at the pattern/system level so every place using it
benefits — a one-off patch leaves the same defect recurring everywhere else the pattern is
reused, and repeated one-off patches erode the system's consistency over time. Cleaning up one
instance also does not prevent recurrence unless the underlying mechanism that produced the
problem is itself addressed.
Do: when real content or a bug breaks a pattern on one page, fix the underlying
component/pattern definition, not just that page.
Trade-off: system-level fixes take more investigation/friction upfront but prevent gradual
erosion of consistency across the whole system.
Ask: is this problem isolated to this one application, or does it reflect a defect in the shared
pattern that would recur anywhere else it is used? If we clean this up today, what stops the same
problem from reappearing later?
(AD ch2,5; DS ch5 review)

### Document a variant's prominence, frequency, and purpose as explicit classification `SYS-029`
A functional pattern's visual prominence ("loudness") can be documented as an explicit, shared
classification rather than argued ad hoc: for each variant, record its type, prominence,
frequency of use, and purpose (e.g. Primary = high prominence + frequent + main action; Secondary
= lower prominence + occasional + supporting action). This converts subjective visual-hierarchy
disputes into a documented, referenceable system.
Do: record prominence/frequency/purpose per variant in shared documentation.
(DS ch1)

### A properly generalized module costs more upfront but makes reuse near-free `SYS-066`
Reusing an established modular component takes far less time than rebuilding the equivalent from
scratch; a simple custom component took roughly half the time of building the equivalent as a
flexible, named, reusable module, but every later reuse of the module took almost no time. The
same logic applies to updates: a centralized pattern's update propagates automatically everywhere
it is used, while the same visual style duplicated ad hoc throughout a codebase must be updated
by hand at every occurrence. Reuse across varied contexts also tends to improve the shared
component's design over time, since each new context surfaces a different use case or edge case
for it.
When: a component that is genuinely a one-off with no realistic reuse does not need the extra
generalization investment.
Do: centralize a pattern once it is duplicated across the codebase, so future changes propagate
automatically.
Trade-off: higher upfront build cost for a proper reusable module versus near-zero marginal cost
on every subsequent reuse.
Ask: will this component likely be needed again elsewhere, enough to justify the extra upfront
generalization cost? If this style changes later, how many places would need to be updated by
hand?
(DS ch7; AD ch4)

### Establish and centralize a Visual Framework `SYS-071`
Define and reuse a single consistent basic layout, color palette, font set, and tone/vocabulary
across every page/window of a product, flexible enough to accommodate each page's distinct
content, including keeping "you are here" signposts (title, logo, breadcrumb, current-location
nav) and navigation devices consistently placed across pages. Implementing this forces a
separation between the style/framework layer and page content, analogous to a stylesheet:
framework decisions are defined once, centrally, and referenced by content rather than repeated
ad hoc per page, so a framework-wide correction doesn't require editing every page individually.
This is not merely cosmetic — a badly organized site can be technically compliant and still
alienate cognitively-impaired or time-pressured users, making information architecture itself an
inclusion concern.
When: a homepage or main window is commonly allowed to be visually "special"/distinct from
interior pages, while still sharing some framework characteristics.
Do: share a defined color/font set and consistent tone/vocabulary across all pages, keep
signposts and navigation devices consistently placed, and centralize style/framework definitions
separate from content.
Ask: do the homepage and interior pages share enough visual DNA that a user recognizes them as
the same product? If the framework's color/font/spacing needs to change, does that require
editing every page's content, or only one shared definition?
(DI ch4; IC ch4,6)

### For dynamic content, the hard problem is the permanent record, not the live update `SYS-072`
The mechanical problem of announcing a transient, real-time event is comparatively easy to solve;
the harder and more important task is the clarity of each message's content and, above all, the
structure and presentation of the permanent history/interface state into which each transient
message offers only a fleeting glimpse. Structuring content well remains paramount even for
dynamic, real-time events, not just static documentation.
(IC ch10)

### An off-the-shelf framework trades speed for distinctiveness `SYS-075`
Adopting a shared front-end framework speeds development and gives consistent, cross-browser-
tested components, but interfaces built on the same framework tend to look alike, ship unused
CSS/JS as bloat since teams rarely use 100% of a framework, and can require so much custom
override that the framework's speed benefit is outweighed by the cost of fighting its structure.
A framework's own naming/structure conventions can also clash with an organization's existing
lexicon.
Trade-off: development speed and consistency vs. brand/visual distinctiveness; out-of-the-box
completeness vs. shipped bloat; initial customization ease vs. long-term cost of fighting
framework structure.
Ask: will most of the framework's components actually be used, or will much of it ship unused?
Does the framework's conventions clash with the team's existing codebase?
(AD ch1)

### Design for device/context flexibility, not one fixed visual `SYS-076`
Because the web is consumed across a large and growing diversity of devices, screen sizes, input
types, and capabilities, components and layouts should be designed and built to work well across
that range rather than assuming one canonical, fixed visual presentation (the print-era mentality
of a design as a static image). This implies treating performance and progressive enhancement as
core design constraints rather than afterthoughts, and anticipating that the device/context
landscape will keep expanding.
Do: create flexible layouts and components that look and function well irrespective of device
dimension or screen size, treat performance as an essential design principle, progressively
enhance from a core experience, and design for future-friendliness.
Ask: does this component assume one fixed visual presentation, or will it keep working as new
devices/contexts appear?
(AD ch4)

### Separate theme stylesheet vs. a single CSS invert-filter override `SYS-077`
A fully separate alternative-theme stylesheet is flexible but costs extra load weight and has to
be kept in sync manually as the site evolves. Augmenting the existing light theme with a terse
CSS filter:invert(100%) override is far cheaper and self-maintaining, at the cost of only ever
producing a strict color inversion rather than an arbitrarily distinct visual theme.
When: building a simple light/dark theme toggle where the two themes are just inverted
brightness, not divergent designs; avoid the invert-filter approach when the alternative theme
needs to differ from the base theme in more than color/brightness.
Trade-off: flexibility (separate stylesheet) vs. maintenance/performance efficiency
(invert-filter).
(IC ch6)
