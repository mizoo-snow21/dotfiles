# Variants & States

This reference serves the decisions of splitting a component into variants, designing and
exposing its state machine, deciding whether a behavior needs a dedicated mode, deciding what
should persist across sessions, and picking a control shape for a given value space. Route here
whenever a component-design task asks "is this a different kind of the same component, or a
different condition of it?", "what states does this object actually have?", or "which control
fits this input?".

Sections:
- Variant vs state distinction
- Modeling variants
- Modeling states
- Modes
- Persistence
- Control-variant candidate sets

## Variant vs state distinction

**Variant** is the kind of meaning, use, or expression a component takes. **State** is the
component's current, interaction-driven condition. Do not freeze any specific variant list as a
universal rule — the candidate control sets later in this file are observed options for a given
value-space shape, not an exhaustive taxonomy.

### Label vs. explicit state: don't let one transition move both axes `VST-001`
A component's visible label/content is a variant/display axis; an explicit interaction-state
attribute (e.g. aria-pressed/aria-checked) is a separate state axis. When a toggle's label itself
changes to reflect a transition (e.g. "Play"/"Pause"), don't also flip the state attribute for the
same interaction — the label already communicates the change, and flipping both risks them
disagreeing about what the current state means. When: a toggle's label text itself changes to
reflect its two states; except: the label is stable and only the state attribute communicates the
toggle.
Do: pick one axis — label or explicit state attribute — to carry the toggle's meaning for a given
transition.
Ask: does the label already fully communicate the change, so a parallel state flip is redundant or
contradictory?
(IC ch2)

### Match a control's implementation to its real state model, not its surface resemblance `VST-002`
A control's correct implementation follows its actual state model, not how closely it resembles
another pattern: a toggletip trigger that only ever shows/re-shows content (no meaningful "hidden
again" state) shouldn't get two-state toggle-button semantics just because clicking an icon to
reveal something looks like a toggle, and a one-shot action (e.g. "Reset") is not a state to select
between, so it must not be implemented with a binary state-selector control — use an
action-appropriate control instead (e.g. a long-press/spring-loaded trigger). More generally,
controls that look the same must behave the same: same-purpose controls in a set should share one
consistent state-visual language.
Do: ask whether the control genuinely has two meaningfully distinct, togglable states before giving
it toggle-button semantics; use action-appropriate controls for one-shot actions; give same-purpose
controls a shared state-visual language.
Ask: is this actually a state to choose between, or a one-shot action?
(IC ch5; MI ch6)

## Modeling variants

### Model a variant as an override of the shared base pattern, not a duplicated pattern `VST-003`
When an element shares content structure with an existing pattern but needs a different look,
behavior, or extra structure — whether from design intent or from state/permissions (e.g. an admin
flag revealing extra edit/delete actions on a list row) — model it as a variation that
extends/overrides the shared base pattern's data, inheriting the base's structure and default
content, rather than creating a fully separate, duplicated pattern. Decide explicitly which
properties belong to the shared core and which are variation-only before implementing, since that
determines whether a future change to one place also changes the other. Except: the variant differs
so substantially in meaning/role that it isn't reasonably "the base plus an override" — that's a
separate-pattern call, not this rule's territory.
Do: identify which properties are core vs. variation-only before implementing; model
state/permission-driven variants as an override of the base pattern's data.
Trade-off: inheriting from a base pattern keeps variants in sync automatically, but can make the
base pattern's conditional logic harder to read than a fully separate, explicit pattern.
(AD ch3; DS ch8)

### Design and validate every component against the realistic range of content/data states `VST-008`
A component/template must be validated against the plausible range of dynamic content it will
actually encounter — an empty cart vs. a ten-item cart, a first-time user's dashboard vs. a
returning user's, a short headline vs. a long one, a non-admin's view vs. an admin's with extra
controls — not just a single best-case populated example. Production content routinely diverges
from the ideal case designers default to showing, so a resilient component must be designed and
validated against its best case, worst case, and the realistic range between. Empty state
specifically is a required, first-class design surface, not decoration or an afterthought, and its
instructional copy should proactively tell a first-time user what to do next.
Do: articulate and check variations driven by content length, data volume, first-use vs. returning
state, and permission level; design and validate against best case, worst case, and realistic
in-between; give the empty state explicit, actionable instructional copy.
Ask: what is the emptiest/shortest version of this content that must still render acceptably, and
what is the longest/most-populated version?
(AD ch2, ch3; IC ch3)

### Split a generic component into task-specific variants once usage data reveals real categories `VST-019`
A single generic, free-form component can't apply category-specific smart defaults or hide
irrelevant fields. Once usage data accumulates to reveal common, distinct use-case categories, split
the generic component into category-specific variants, each asking only what's relevant to that
category and pre-filled with defaults drawn from historical data. When: usage data exists (or can be
gathered) showing what those categories actually are; except: usage patterns aren't yet known —
start generic until enough data exists to justify specialization.
Do: specialize into category-specific variants once usage data supports it; pre-fill
category-specific defaults from historical data.
Trade-off: simplicity/relevance per variant vs. more components to maintain.
(MI ch6)

### A very narrow viewport needs a genuinely different structural variant `VST-038`
For very narrow (effectively single-column) viewports, present the same underlying data using a
wholly different, real markup structure, rather than forcing a horizontally-scrolling squeeze of
the wide-viewport structure. Both variants should remain fully-formed and accessible, shown/hidden
by a media query, not one deformed to fit the other's space. Except: for extremely large data sets,
keeping both structures in the DOM simultaneously bloats the DOM tree — an accepted tradeoff against
the performance/complexity cost of dynamically reconstituting markup on resize.
Do: render two real markup structures from the same data and show/hide by media query.
Trade-off: DOM size (two structures always present) vs. runtime cost of dynamically switching
structures on resize.
(IC ch11)

### Give the primary action explicit visual prominence, with an explicitly scoped "primary" `VST-024`
A component set should have at most one visually prominent primary/completion action, with
secondary actions (reset, help, optional) styled with restrained visual weight so they don't
compete with it. But "primary" is ambiguous unless its scope is defined explicitly: it can mean the
single most important action across the entire product (so only one primary button per screen), the
most important action within a local screen/section, or emphasis by purpose rather than importance
(required vs. optional, allowing several equally-important flat buttons side by side).
Do: give the primary completion action strong visual prominence; style secondary actions with
restrained visual weight.
Trade-off: importance-scoped primary (one per screen) maximizes clarity but is restrictive;
purpose-scoped emphasis (required vs. optional) scales to more buttons but ties variant meaning to
a business/UX category instead of a single global rank.
Ask: is "primary" scoped to the whole product or to a local section?
(DS ch8; DI ch8)

### Action label form and length should match the container's space and frequency of use `VST-034`
An action's label may use text, an icon, or both; keep icon-only styling consistent throughout a
container once chosen. Roomier containers support longer, more descriptive labels than a menu item
or button can; longer labels help first-time/infrequent users learn or recall what an action does,
while shorter labels suit dense, expert-facing interfaces where excess text costs scanability.
Trade-off: longer labels aid learnability/recall for infrequent users but add visual noise and space
cost that experienced users may not need.
(DI ch6)

### Row headers are a supplementary, optional variant of table headers `VST-037`
Column headers are broadly necessary for a data table; row headers are optional and situational,
appropriate when a table has a natural "key" column that other cells in that row relate to — not
every table has one, so row headers are a variant to apply when the data calls for it, unlike
column headers.
Do: add row headers when a table has a clear per-row identifying value.
(IC ch11)

### Motion pattern variants: define timing, easing, and property together `VST-035`
A motion pattern needs three linked variables together, not timing alone: duration, easing, and
which properties are allowed to change — the same numeric duration produces different perceived
speed depending on the distance/scale involved. Set a base duration tied to a reference distance
and scale each instance's duration proportionally to its own travel distance/size delta, and tier
duration further by the scale of the transition (small-scope dropdowns/tooltips get shorter timing
than large-scope full-screen transitions). Judge the result by whether the motion feels
uniform/rhythmic, not by forcing identical numeric duration values everywhere.
Do: define timing, easing, and the animated property together; set a base duration tied to a
reference distance and scale other instances relative to it.
Trade-off: technical precision vs. perceived/felt consistency.
(DS ch9)

## Modeling states

### Worked example — a state table is the deliverable's floor, not an extra `VST-EX1`
V1 evals showed state modeling described in adjectives ("handles loading gracefully") scores at
baseline; typed shapes with owners score above it. For every stateful component, write the state
model in this shape before prose:

| state axis | concrete shape (values, not adjectives) | single owner | transitions (trigger → result) |
|---|---|---|---|
| content | `idle \| loading \| loaded(rows: Row[]) \| empty \| error(msg, retryable)` | ShipmentList | `mount → loading`; `fetch ok → loaded/empty (rows.length)`; `fetch fail → error` |
| selection | `Set<RowId>` (possibly empty; no "select-all" boolean — derive it) | ShipmentList | `row checkbox → toggle id`; `header checkbox → all visible ids / clear` |
| sort | `{col: ColId, dir: asc \| desc} \| null` | ShipmentList | `header click → same col: flip dir; new col: asc` |
| row expansion | `RowId \| null` (exclusive) — a second axis, never mixed into `content` | ShipmentList | `row click → toggle; opening one closes the previous` |

Rules the table enforces mechanically: one owner per axis (derived displays read from it, never
duplicate it — VST-005); every axis lists ALL its change paths (VST-006); waiting/active/updated
each designed (VST-013); no axis smuggled into another ("empty" is a content value, not a boolean
beside it). If two sections of your document would fill this table differently, that IS the
defect the final critique's state sweep exists to catch.
(worked example, V2 — instantiates VST-005/006/013 and the MI ch3 rules-define-transitions model;
tabled format is skill-derived, the rules it enforces are book-derived)

### Attach a component's state indicator to the control that changes it `VST-004`
A component's current state must be exposed on the element the user actually operates to change
it, not on the separate target/content being changed, and not in a distant or separately-located
indicator — a collapsible section's expanded/collapsed state belongs on the toggle control, not on
the content it shows/hides. A trigger control can (and often should) also surface its own most
decision-relevant internal data directly on itself, becoming a glanceable state display before
activation. Where state is shown via a separate visual indicator rather than the control's own
appearance changing, that indicator must sit immediately adjacent to the trigger it describes —
never in a distant panel.
Do: place the state attribute/indicator on the toggle control, not on the content being
shown/hidden; surface the most decision-relevant internal data directly on the trigger; place state
indicators immediately beside their trigger.
Ask: which element does the user actually operate to change this state — is the state exposed
there, not on the thing being changed?
(IC ch8; MI ch2)

### Derive presentation from one authoritative state source, don't duplicate state into a flag `VST-005`
Prefer deriving a component's visual/behavioral presentation from state that already exists in one
authoritative place — a native DOM structure or pseudo-class (:empty, :checked, :first-child) or a
single state attribute — rather than adding and removing a second, separately-toggled class or flag
that duplicates the same information. Where a component needs both an accessible state attribute
and a visually-driven state, drive both directly off the same attribute instead of maintaining a
parallel CSS class alongside it. Except: no native pseudo-class or existing DOM signal corresponds
to the needed state.
Do: leverage :empty, :checked, :first-child, etc. instead of manual class toggling; style off the
same state attribute that already carries the accessible state.
Ask: does a native pseudo-class or existing single attribute already express this state, without
adding a second, separately-toggled flag?
(IC ch3, ch8)

### A derived state must track every input path that can change its underlying value `VST-006`
Where a control's own state is derived from an underlying value that can change via more than one
interaction path (e.g. a boundary-reached flag affected by both clicking a button and by the user
scrolling the region directly), the derivation logic must observe state changes from all relevant
paths, not only the path the control itself initiates. If it only updates in response to one of
several ways the underlying value can change, it silently falls out of sync whenever it changes via
an unobserved path.
Do: observe every interaction path that can change the underlying value a derived control state
depends on.
Ask: what are all the distinct ways this underlying value can change, and is each one observed?
(IC ch9)

### Define interaction-state behavior once, system-wide, instead of reinventing it per component `VST-009`
Interaction states (hover, focus, selected, disabled, etc.) are usually documented per component
individually, which risks inconsistent treatment across component types — does hover on a
secondary link, icon button, ghost button, and tab all change the same way? Define
interaction-state rules once at the system level and reference them from each component, rather
than letting each component invent its own ad hoc treatment. This applies where the underlying
interaction genuinely is the same kind of state change — a different kind of control
legitimately gets a different treatment (see BND-039: over-prioritizing consistency produces a
generic, inflexible system).
Do: define interaction-state rules once at the system level and reference them from each component.
Ask: is this component's hover/focus/selected/disabled treatment consistent with other interactive
components, or ad hoc?
(DS ch10)

### An interactive object needs at least three deliberately-designed states `VST-013`
A user-operable object typically passes through at least three states that must each be
deliberately designed, not left as an incidental byproduct of a default look: a waiting/default
state, an active state while being operated, and an updated state once the interaction completes
(e.g. a drag-and-drop object needs a distinct draggable waiting look, a distinct dragging state
that may also affect drop targets, and typically reverts to default once dropped). A single
trigger's default/waiting state is not necessarily singular — it can vary depending on
prior/external context (e.g. logged-in vs. logged-out), and that variation changes what a single
press of the trigger will actually do; each such compound waiting state needs its behavior
explicitly defined.
Do: design waiting, active, and updated states deliberately for every operable object.
Ask: have I explicitly designed this object's waiting, active, and updated states, or only its
default look? Does this trigger have more than one possible starting state depending on context,
with each one's behavior explicitly defined?
(MI ch3)

### A control's default/hover/rollover/active states each carry distinct meaning `VST-014`
A manual-trigger control's states aren't purely cosmetic: default is idle/waiting, hover may
preview internal data without activating, rollover can swap appearance to preview the effect of
activating, and active is the moment of engagement (which can itself morph into a new element, e.g.
a progress bar). Implementing a two-state toggle as a plain button that flips state on each press —
instead of a dedicated toggle switch/button with visually distinct states — is risky, since users
often can't tell at a glance which state is active or rule out a hidden third state; use this
pattern only when the resulting state is unambiguous from other context (e.g. a light bulb, where
"lit"/"unlit" is self-evident regardless of the button's own look).
Do: use a dedicated toggle switch/toggle button with visually distinct states for ambiguous
two-state controls.
Ask: what should hover/rollover reveal before the user commits to activating? If a new user saw
only this button, could they tell which state is currently active?
(MI ch2)

### ANTI-PATTERN: a rule must not have an undisclosed side effect on unrelated state `VST-016`
When a component's rule silently produces a side effect on state the user did not intend to touch
— and no feedback discloses that side effect — the result can cause real, sometimes irreversible
harm (e.g. an already-sent document silently overwritten). A labeled action must not silently
modify state outside its apparent scope; if it does, disclose the side effect via explicit
feedback, or, preferably, redesign the rule so it has no hidden side effect at all. This is a
critical design defect, not a minor rough edge.
Do: disclose any side effect on unrelated state via explicit feedback; prefer redesigning the rule
so it has no hidden side effect at all.
Ask: does activating this rule change anything the user did not explicitly ask to change?
(MI ch3)

### Transform a single screen's state incrementally; reserve a new screen for rare, distinct steps `VST-017`
Turning every rule-step into its own full screen breaks flow continuity for most interactions,
because the user has to reload/reorient each time. For the common case, prefer incrementally
transforming the state of a single screen step by step, so only what's relevant to the current
decision changes. Except: the step is genuinely rare, distinct, and one-time — exactly the
exception an unavoidable mode is designed to be.
Do: transform a single screen's state incrementally for most multi-step interactions.
Trade-off: full-screen steps can isolate complex/rare decisions cleanly but interrupt the
continuity most interactions rely on.
(MI ch3)

### Make invalid states structurally impossible via control redesign rather than validating them away `VST-018`
Reducing the number of choices offered has the side benefit of eliminating edge cases that would
otherwise complicate the rules. Where an edge case would require special-casing the rules after the
fact, prefer redesigning the input control itself so the invalid state is structurally impossible
to enter (e.g. a dropdown-based date picker instead of free text for a birthdate, so an invalid
date literally cannot be entered) rather than adding rules to detect and reject it later.
Do: prefer eliminating an edge case structurally via control design over handling it with extra
rules.
Ask: can the input mechanism itself be redesigned so this edge case can't occur, rather than adding
a rule to catch it?
(MI ch3)

### Classify the origin of a state change: user, remote actor, or environmental/time-based `VST-007`
A component's state-changing behavior can begin either from a manual trigger (the user performs an
explicit action) or a system trigger (the component detects a condition — time, data arrival,
location — has been met). At finer grain, a state change a user needs to be kept abreast of can
originate from the user's own action, another user or remote actor changing the app in real time,
or an environmental/time-based event independent of any interaction; design state handling against
all applicable origins, not just the local-UI case.
Trade-off: system (automatic) triggers reduce user effort but reduce predictability/control if the
condition is not obvious to the user.
(MI ch1; IC ch10)

## Modes

### A mode is defined by its behavioral effect, not its appearance `VST-020`
A mode is a genuine functional state where the same trigger/input produces different results than
usual, or where the interface's normal functionality is temporarily disabled to prioritize the mode
itself — this, not floating position, box shape, or a close button, is what actually defines a
modal dialog. Modes should be minimized: most components are better off with none at all, though a
mode is sometimes genuinely necessary; where one is unavoidable, a component should have at most
one. A mode is especially dangerous when invisible — if the screen looks unchanged but the same
action now does something different, users act on a wrong prediction and can get an unexpected,
sometimes destructive result — so any active mode must be visually unmistakable.
Do: default to zero modes, cap at one if truly unavoidable; prefer direct manipulation over an
explicit mode-switch step where feasible; make an active mode visually unmistakable.
Ask: can this functionality be handled within the component's single primary rule instead of a
separate mode? Can the user tell, purely by looking, whether this mode is active?
(MI ch1, ch5; IC ch12)

### The legitimate reason to add a mode: isolating an infrequent operation or a different rule set `VST-021`
The main justification for a mode is that some infrequently-used operation exists which, left in
the primary flow, would clutter it — a "settings mode" that only configures rather than performs
the primary task is the common example. Separately, a choice that would switch to a fundamentally
different rule set (e.g. a "Forgot password?" link diverting into an entirely different flow)
should also be treated as a distinct mode rather than blended into the primary rule path as an
ordinary choice among related values (temperature: high/medium/low is fine to keep inline). Except:
the operation is used frequently enough that a mode switch would itself become a burden.
Do: reserve modes for genuinely infrequent, secondary operations; model a rule-set-switching choice
as an explicit mode with a clear return path.
Trade-off: clean primary flow vs. the confusion cost of adding a mode.
(MI ch3, ch5)

### An unavoidable mode gets its own screen, and returning preserves everything except mode-made changes `VST-022`
When a component genuinely needs a mode, give it its own dedicated screen/space wherever the device
supports it — an explicit exception to the general preference for in-place state transformation —
with a transition animation both entering and leaving, signaling a deliberate context switch rather
than a broken state. When the user leaves the mode and returns to the main interaction, only the
changes actually made while in the mode should be reflected; everything else must be exactly as it
was when the user left. Except: the mode is spring-loaded or one-off, which don't require a
dedicated screen.
Do: give an unavoidable mode its own screen; animate the transition into and out of it; preserve
all main-flow state exactly except for changes explicitly made in the mode.
(MI ch5)

### Spring-loaded (quasimode) and one-off modes avoid dedicated-screen overhead `VST-023`
A spring-loaded mode (quasimode) is active only for as long as a specific key is held or a physical
action is sustained (e.g. holding Shift for uppercase); because the user is physically holding the
trigger, they can't forget they're in a different mode, so it suits only short/simple operations,
not slow or complex ones. A one-off mode is active for exactly one subsequent operation and then
auto-clears (e.g. double-tap-to-select on iOS accepting exactly one following command); because
nothing physically holds it open, it must auto-expire via a timeout loop, which suits fast,
context-dependent switches, including gesture- or voice-triggered interactions, where it also
prevents accidental misfires.
Do: use spring-loaded mode for short operations gated by a held trigger; auto-clear a one-off mode
after exactly one operation, paired with a timeout loop.
Trade-off: no dedicated screen needed vs. limited to operations short enough to sustain the physical
trigger (spring-loaded), or to exactly one follow-up action (one-off).
(MI ch5)

## Persistence

### Persist state/arrangement/preference across sessions, with a reset-to-default escape hatch `VST-010`
A component's state, arrangement, or preference should persist across sessions (and across devices,
where feasible) for logged-in/returning-user contexts, rather than resetting to default every time
— e.g. an Accordion's per-panel open/closed state, Movable Panels' arrangement, a remembered volume
level, or a "keep me signed in" choice. This is what lets a component genuinely improve on repeated
use instead of just repeating identically. Because users may lose track while customizing, provide
a discoverable "reset to default" control as a safe recovery path. Except: the component is purely
a navigation menu, where persistence matters less, or the interaction is genuinely a one-off with no
meaningful repeat-use context.
Do: persist each panel's/module's open/closed state and position across sessions for logged-in
tool-palette-style components; provide a discoverable "reset to default" control; persist relevant
usage data/preferences to make repeat use progressively better.
Ask: if the user returns in a new session, are their positions/open-closed states/preferences
exactly as they left them? Is there a clear way to reset to default if a customization becomes a
mess?
(DI ch4; MI ch5)

### Progressive simplification by familiarity must pair with a reversion rule after a long absence `VST-012`
A long loop can track how experienced a user has become with a component and progressively reveal
advanced features or strip away beginner labels/explanations (e.g. a labeled icon-and-text button
simplifying to icon-only for experienced users). This must be paired with a reversion path: if the
user has been away for a long time, the component should revert to the more explicit,
beginner-friendly version rather than assuming continued familiarity.
Do: progressively simplify or reveal advanced options based on tracked familiarity; revert to the
beginner-friendly state after a long gap in use.
Trade-off: cleaner UI for experts vs. confusion for users returning after a long absence if
reversion is missing.
(MI ch5)

### Persisted preference state should resolve: explicit user choice, then OS/system, then default `VST-036`
A persisted preference model (e.g. a theme toggle) should resolve in priority order: an explicit
choice the user has already made in this app wins outright; if no stored choice exists, fall back
to the OS-level preference; otherwise use the default. Once an OS-derived default is used, persist
it as if it were an explicit choice.
Do: check stored preference first, then OS-level preference, then default.
Ask: has the user already made an explicit choice for this app, distinct from the OS setting?
(IC ch6)

### A long loop can drive visual state purely from elapsed time/recency, without new user action `VST-011`
A long loop can tie a component's visual presentation to elapsed time or recency since an event,
without requiring any new user action — e.g. a list item's visual weight fading as it ages, or a
recently-used term highlighted in a color that fades with time. This is state defined by elapsed
duration, not by direct interaction.
Do: tie visual state (opacity, color, emphasis) to elapsed time since a relevant event where useful.
(MI ch5)

## Control-variant candidate sets

These are candidate control shapes observed for each value-space shape, not an exhaustive or
universal taxonomy — match by cardinality first, then weigh the tradeoffs below against your own
space, literacy, and convention constraints.

### Match control type to the shape of the underlying state space `VST-025`
The right control type for a manual input follows the cardinality/shape of the state it
represents: a single momentary action fits a button; a two-state action fits a toggle
switch/button; several discrete states fit a dial-with-stops or separate buttons per state; a
continuous range fits a slider or dial; compound data entry falls back to form fields. Among
controls that could equally represent the same logical input, weigh: available screen space, the
user population's general computer literacy, the user's domain expertise (do they already know the
valid range?), conventions/expectations carried over from other applications or the platform, and
what the target platform's technology actually provides.
Do: match control type to the number/shape of possible states rather than defaulting to a generic
button/field for everything.
Ask: how many discrete states, or what range of continuous values, does this control need to
represent? Does a convention from other apps/platforms already set an expectation for this value?
(MI ch2; DI ch8)

### TRADEOFF: control choice trades operation simplicity against state legibility `VST-015`
For the same underlying set of possible values, different control types trade off simplicity of
operation against ease of recognizing the resulting state at a glance. Multiple single-function
controls (e.g. separate up/down/mute volume buttons) are simple to operate but each covers only one
function; a single multi-function control (e.g. a slider) makes the current state directly legible
but requires more nuanced operation. For infrequently-repeated interactions, favor whichever
control is simplest to operate/recognize correctly; for interactions requiring speed and low error
tolerance, favor dedicated single-purpose controls kept clearly separate, since a shared control
risks a costly mistake (e.g. never share a mute control with volume-down). A single binary choice
shows the same tension concretely: a checkbox is compact but leaves the unchecked state's meaning
implicit, while two radio buttons make both options explicit at a higher space cost.
Trade-off: multi-function controls are more state-legible but riskier for fast, error-sensitive
actions; single-function controls are safer but less at-a-glance informative.
Ask: does this interaction need fast, mistake-resistant operation, or is at-a-glance state
legibility more valuable?
(MI ch3; DI ch8)

### Control-variant catalog: binary (2-option) single choice `VST-026`
For a single choice between exactly two options, the candidate variants are: checkbox, a pair of
radio buttons, a 2-item dropdown, and a persistent-pressed toggle button — each trading label
visibility for space and clarity.
Trade-off: checkbox is compact but the unchecked state's meaning can be ambiguous; two radio
buttons keep both options always visible/labeled but cost more space; a 2-item dropdown labels both
options and scales if they may grow, but only one is visible at a time and needs more interaction
skill; a toggle button shares the checkbox's tradeoffs, space-efficient as an icon but less
conventional as text.
(DI ch8)

### Control-variant catalog: single-select from a small number of items `VST-027`
When choosing 1 of N items and N is small, candidates are: N radio buttons (all visible, high space
cost), an N-item dropdown (low space, only current value visible), an icon-based
mutually-exclusive toggle-button set, a single-select list, and a spinner/stepper control.
Trade-off: radio buttons show everything but cost space; a dropdown is compact but needs
interaction skill; icon toggles are compact and visible but icons can be hard to decode and need
tooltips; a single-select list shows many options at higher space cost than a dropdown or spinner;
a spinner is very compact but shows only one value at a time and isn't well known to novices.
(DI ch8)

### Control-variant catalog: single-select from a large number of items `VST-028`
When choosing 1 of N items and N is large, candidates are: a scrollable dropdown, a single-select
list/table, a single-select tree/cascading list organized by category, and a custom selection
dialog (e.g. file/color/font pickers) opened in a separate window.
Trade-off: a scrollable dropdown is compact but scrolling while browsing needs real skill; a
list/table shows many items but costs more space; a tree/cascading list improves findability but is
unfamiliar to novices and costs space and skill; a custom dialog presents a large set thoroughly but
is unfamiliar to some users and physically distant from the triggering control.
(DI ch8)

### Control-variant catalog: unordered multi-select from N items `VST-029`
For selecting an unordered subset of items from N options, candidates are: an array of N
checkboxes, an array of N toggle buttons, a multi-select list/table, a checkbox-annotated list, and
a multi-select tree/cascading list — each inheriting its single-select counterpart's
visibility-vs-compactness tradeoffs, plus a distinct failure mode: a plain multi-select list or tree
can look visually identical to its single-select sibling, so users may not realize multiple
selection is possible.
Trade-off: checkbox arrays are explicit and visible but cost space; toggle-button arrays are
compact but icons can be hard to decode; multi-select lists/tables show many options but risk that
multi-select goes unnoticed; checkbox lists make the selection affordance clear; multi-select trees
add category organization but risk confusion with the single-select variant.
(DI ch8)

### Control-variant catalog: text input `VST-030`
Text-entry controls range from a plain single-line field, to a combobox (field + bounded dropdown
of known values), to a field augmented with a "More"/dropdown-chooser button opening a specialized
picker, to a plain multiline textarea, to a rich/inline-tag textarea, to a full rich-text toolbar
with live preview — each step trading simplicity and keyboard-only operability for richer input
capability.
Trade-off: a combobox is fast and well known but doesn't scale past a small dropdown item set; a
"More" button opens a specialized picker but is less well-known and at-hand than a combobox; a
plain textarea is simplest for unformatted multi-line text; an inline-tag textarea lets power users
type markup directly but isn't genuinely WYSIWYG; a rich-text toolbar with live preview is quick to
grasp but requires the toolbar, so it isn't fully keyboard-operable.
(DI ch8)

### Control-variant catalog: single numeric value input `VST-031`
For entering a single number, variants include a forgiving-format text field (accepts many formats,
needs server-side validation), a structured-format field split into typed chunks (shape signals
expected format but adds visual complexity), a spinbox/stepper for small/discrete steps, a slider
for a visually obvious range, and a text field validated after entry (optionally paired with input
hints). Forgiving Format and Structured Format are also documented as their own dedicated patterns:
Forgiving Format is a single free-text field that delegates interpretation to the application,
suited when the input space is parseable and visual simplicity matters; Structured Format is
several small purpose-shaped fields whose layout mirrors the expected data structure, suited to a
well-known, standardized format, at the cost of harder copy-paste and reduced assistive-technology
usability.
Trade-off: forgiving-format is simple and flexible but risks format confusion and needs validation;
structured-format signals the required shape but costs space/complexity and can reject legitimate
out-of-shape values, and is harder for assistive tech; a spinbox needs no keyboard but isn't
universally familiar and has fiddly small buttons; a slider gives an at-a-glance metaphor but costs
space and has unclear keyboard accessibility; a post-entry-validated field with hints is familiar
and keyboard-accessible but needs validation plus a hint to communicate the allowed range.
(DI ch8)

### Control-variant catalog: bounded numeric sub-range (dual value) `VST-032`
For entering a sub-range within a larger range, variants are a double-ended slider, two separate
sliders (paired with a text field), two linked spinners, and two text fields validated after entry
— trading familiarity and space against direct visibility of the selected range.
Trade-off: a double slider is compact but poorly known and needs a paired text field for keyboard
access; two separate sliders are easier to grasp but cost much more space; two linked spinners keep
values in range with low space cost but have fiddly small buttons and don't show the range
visually; two text fields with post-entry validation are most familiar and compact but need
validation plus another way to communicate the range.
(DI ch8)

### Control-variant catalog: date/time input `VST-033`
For date or time input, variants are a forgiving-format text field, a structured-format field split
into date components, a calendar/clock picker control, and a calendar/clock picker combined with a
dropdown-style text field showing the current value. Except: the date is likely to be far from the
current date (e.g. birthdate, expiry date) — a calendar-metaphor picker is a poor fit here.
Trade-off: forgiving-format is simple and flexible but risks format ambiguity and needs validation;
structured-format shows the format from the shape but costs space/complexity and can reject
valid-but-out-of-shape input; a calendar/clock picker gives an at-a-glance metaphor and bounds input
but costs space and may not be keyboard-accessible; a picker combined with a dropdown text field
combines both benefits at the cost of more complex interaction.
(DI ch8)
