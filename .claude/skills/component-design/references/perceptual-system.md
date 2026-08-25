# Perceptual Patterns & Design Principles (context)

Design principles, perceptual/cognitive (style) patterns, brand voice/motion mood — the layer
where a component system meets visual identity. NOTE: this territory overlaps ui-ux-design's
scope (visual styling is upstream); load this file only when a system-wide design-language
decision or a brand-consistency audit is explicitly the task, and defer per-screen visual
decisions to ui-ux-design. Split from system-consistency.md (V2); provenance tags unchanged.

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
