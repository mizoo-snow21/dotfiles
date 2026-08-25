# Behavior Contracts

This file governs how a component acts once its shape and states are already decided: what starts it, what logic governs what happens, how the result gets communicated back, and how the whole thing persists or repeats over time. Route here when specifying, reviewing, or debugging a component's interactive contract — writing a trigger, a rule set, a feedback message, an error path, or a repeating/timed behavior. It assumes visual form, state inventory, and composition are already settled elsewhere; the questions here are strictly about what the component *does*.

## Sections

1. The behavior-contract model
2. Triggers
3. Rules
4. Defaults & choices
5. Feedback
6. Error prevention
7. Loops & timing

## 1. The behavior-contract model

### Four-part behavior contract: trigger, rule, feedback, loop/mode `BHV-001`
A component's interactive behavior fully decomposes into four parts that must each be specified: a trigger (what starts it), rule(s) (the logic governing what happens), feedback (how the result is communicated back), and loop/mode (how the behavior persists, repeats, or ends over time). A defined rule with no matching feedback leaves the rule effectively invisible to the user.
Do: for any component with non-trivial interactive behavior, write out its trigger, rule, feedback, and loop/mode explicitly before implementation.
Ask: what starts this behavior, what logic governs it, how does the user learn what happened, and how does it persist, repeat, or end over time?
(MI ch1)

### Rule-specification checklist `BHV-002`
A component's rule set should explicitly define: how it responds when the trigger fires; whether/how the user can manually intervene mid-process; ordering/timing constraints between actions; what data is used and where it comes from; what algorithm/parameters drive automatic behavior; what feedback is returned, when, and for which steps; and what mode the behavior is currently in.
Do: use the seven-item checklist to verify a rule spec is complete before implementation.
Ask: have I specified trigger response, manual override points, sequencing/timing, data sourcing, governing algorithm/parameters, feedback per step, and current mode?
(MI ch3)

### Verb-and-noun model for specifying a rule set `BHV-003`
Treat a microinteraction as a sentence: nouns are the UI objects/elements the rules act on (each needs its properties and states defined), and verbs are the actions the user performs on them (each verb itself has properties — speed, duration — that also need defining).
Do: list the nouns and the properties/states each needs, then list the verbs and the properties each verb itself needs.
Ask: what are the nouns and what states do they need; what are the verbs and what timing properties do they need?
(MI ch3)

### Decompose an algorithm-driven rule into order, branching, repetition, and variables `BHV-006`
When a component's rule set is complex enough to be an algorithm, decompose its design into four elements: processing order (which steps depend on which, under what conditions), branching (if-then conditionals), repetition (whether the whole algorithm or only part loops, and what triggers each repeat), and variables (tunable inputs that adjust behavior without rewriting logic).
When: specifying or reviewing an algorithm-driven behavior (recommendations, autocomplete, scoring, etc.).
Ask: what is the processing order, what branches exist, what repeats and under what trigger, and what variables can be tuned without rewriting the logic?
(MI ch3)

### Constraint checklist used to prevent invalid states proactively `BHV-007`
Enumerate a component's real constraints across five dimensions before designing its rules: available input/output modalities; input type and range limits; cost/burden imposed on user or system; what data can technically be obtained; and what data may legitimately be collected. Use known constraints to prevent invalid states proactively rather than only validating them after entry.
Do: enumerate modality, range, cost, and data-availability/legitimacy constraints up front, then design them out of the input surface.
Ask: what input/output modalities, value ranges, cost burdens, and data availability actually bound this component's behavior?
(MI ch3)

### Build a rule set as happy-path, then branches, then flowchart `BHV-004`
Write the plain happy-path sequence of steps first, then progressively layer in the branching special cases as they're discovered, then render the resulting rule set as a flowchart — visualizing the flow surfaces overly-complex steps and logic errors that prose hides.
Do: write the happy path, layer in special-case branches as discovered, then flowchart the result before implementation.
(MI ch3)

### Validate a component's real behavior by building it in the actual medium, not only static comps `BHV-064`
A static mockup cannot represent interaction, motion, responsive flexibility, performance, scrolling, or device/browser quirks — these only become visible once a component is built in the target medium. Getting it into the browser early confronts the team with real constraints far sooner than reviewing only static comps.
Trade-off: static comps are faster to produce and iterate on visually but cannot validate interaction/behavior/performance; coded prototypes cost more up front but validate the real constraints static comps can't show.
(AD ch4)

## 2. Triggers

### Trigger taxonomy: manual vs. system, and the manual trigger's triple duty `BHV-008`
A component's behavior starts one of two ways: a manual trigger (explicit user action) or a system trigger (the component detects a condition and starts on its own). A manual-trigger control typically does triple duty: it initiates the behavior, may let the user adjust it while in progress, and visually signifies that the interaction is available or in progress.
Trade-off: system triggers reduce user effort but reduce predictability/control if the condition isn't obvious to the user.
Ask: should this behavior require explicit user action, or can it react automatically to a condition — and does the control need to signal availability, accept mid-interaction adjustment, and initiate, or only some of these?
(MI ch1)

### System (automatic) trigger specification checklist `BHV-005`
A system trigger needs its own explicit rule set covering: how often it may fire; what context tunes its frequency (e.g. suppressing it at night); whether any visible indication marks the moment it fires; how a mid-action system error is handled (abort vs. retry, and at what interval); and its resource cost (battery, bandwidth, processor).
Trade-off: more frequent/aggressive automatic firing improves freshness at the cost of resource consumption.
Ask: how often can this fire, what context reduces unnecessary firings, is there a visible sign it fired, and what happens if it fails mid-action?
(MI ch2)

### A trigger must be recognizable from its surrounding context `BHV-009`
A manual trigger must be recognizable as a trigger purely from the surrounding context — it should look and sit where the user's existing understanding of the surrounding UI already tells them to look.
Do: place and style triggers so their surrounding context signals interactivity, not just the trigger element in isolation.
Ask: would a user unfamiliar with this specific screen still recognize this element as something to interact with, based on its surrounding context?
(MI ch2)

### Discoverability golden rule and the visual findability hierarchy `BHV-010`
A trigger's prominence should scale with its expected usage frequency: near-universal, frequent behaviors must be instantly visible; moderately-used behaviors should be easy to find; rarely-used behaviors should require deliberate searching. Findability runs, easiest to hardest: a moving object; an object with both signifier and label; a labeled object alone; an unlabeled icon; a label with no object; an invisible trigger with no visible information at all.
Trade-off: more findable forms (motion, signifier+label) cost more visual attention/space than sparse or invisible forms; very low prominence trades faster access for rare actions against reduced clutter for common ones.
Ask: how often, and by what proportion of users, will this action be taken — and where on the findability spectrum does the trigger need to sit given that priority?
(MI ch2)

### An invisible trigger must be learnable and reliably repeatable `BHV-012`
A trigger with no visible signifier is acceptable only if it is discoverable (found by chance or learned from another source) and, once learned, reliably reproducible — either it works consistently almost every time, or under a narrow, clearly learnable condition. It should not be assigned to high-priority interactions unless there is genuinely no room for a visible control.
When: considering a gesture-only, sensor-only, or otherwise unlabeled control; except: no room exists for any visible control at all.
Ask: once a user learns this invisible trigger, will it behave the same way reliably every time they try it again?
(MI ch2)

### Hiding controls builds hierarchy but must not become a default goal `BHV-013`
Deliberately hiding lower-priority controls reduces visual clutter and creates an implicit importance hierarchy among what remains visible, but invisibility must never be treated as a general design goal in itself — it should be a deliberate, contextual choice, not indiscriminate minimalism.
Trade-off: hiding controls reduces clutter and emphasizes what remains visible, at the cost of discoverability for what's hidden.
Ask: do I have a specific, contextual reason to hide this control, or am I hiding it simply to look minimal?
(MI ch2)

### Match attention-grabbing intensity (motion, sound, blinking) to actual priority `BHV-015`
Moving or sound-emitting triggers, and high-intensity effects like blinking, involuntarily capture attention. Reserve motion/sound triggers for high-priority interactions, and reserve continuous/repeating motion, sound, or blinking specifically for the highest-priority cases (errors, warnings, must-notice-now messages).
Do: reserve animated/sound attention-grabs for errors and warnings, and blinking/high-frequency effects for must-notice-now messages only.
Ask: is this interaction actually high-priority enough to justify involuntarily grabbing the user's attention?
(MI ch2,4)

### Add a label only when the control's own design cannot disambiguate `BHV-016`
Add a text/icon label to a trigger only when the trigger cannot otherwise visually convey the necessary information; try to express the content visually first (e.g. star icons for a rating rather than a number) before falling back to text.
When: a control's meaning might be ambiguous without a label; except: nearby controls look too similar to distinguish without one.
Trade-off: labels add clarity at the cost of visual/cognitive load.
Ask: could this be made clear visually before reaching for a text label?
(MI ch2)

### Native interactive elements provide a complete trigger/activation contract for free `BHV-046`
A native interactive element already comes with a complete built-in activation contract — mouse click, Space/Enter, and touch tap — without extra event wiring, and doesn't require manual event-suppression to avoid unintended side effects (e.g. form submission).
Do: default to native interactive elements to inherit their built-in activation contract rather than reimplementing it.
Ask: does this custom control correctly replicate every activation modality a native element would provide for free?
(IC ch2)

### Never generate a false signifier: visual affordance and actual behavior must match `BHV-066`
If an element visually presents itself as a certain kind of control, it must actually behave like that control. Applying interactive-looking styling to a non-interactive element, or failing to make a button-shaped control respond as a button, breaks the association users have already learned between an object's appearance and its behavior.
Do: keep an element's visual affordance and its actual interactive behavior consistent.
Ask: if a user attempted the action this element appears to support, would they get the response they expect?
(MI ch2)

### Toggle-via-plain-button is ambiguous unless the resulting state is self-evident elsewhere `BHV-065`
Implementing a two-state toggle as a plain button that changes state on each press is risky: users often can't tell at a glance which state is active, or rule out a hidden third state. Use this pattern only when the resulting state is unambiguous from context other than the button itself (e.g. a light bulb, where lit vs. unlit is self-evident regardless of the button's own appearance).
When: implementing a two-state control; except: the resulting state is self-evident from something other than the control itself.
Do: use a dedicated toggle switch/button with visually distinct states for otherwise-ambiguous two-state controls.
Ask: if a new user saw only this button, could they tell which of the two states is currently active?
(MI ch2)

### Context-dependent trigger/action behavior must be explicitly defined per variant and kept honestly synced `BHV-020`
When a trigger's default state or an action's effect varies by context (auth state, current selection, mode), each variant needs its behavior explicitly defined, not just the "normal" case. Where a label communicates the action's effect, it must update dynamically — and the control must be disabled when there is no valid target — so the label always states the true, current effect.
When: a trigger's default depends on external context, or a control's effect depends on the current selection; except: for multi-object selections, a generic plural-safe label is an accepted simplification.
Do: explicitly define every context-dependent variant, update the label whenever the target changes, and disable the action when there is no valid target.
Ask: does this trigger have more than one possible default depending on context, and is each one's behavior explicitly defined?
(MI ch3; DI ch6)

### Trigger consistency contract: the same trigger produces the same result, applied uniformly system-wide `BHV-021`
A given trigger must always start the same behavior every time it is used, so users can build a stable, correct mental model of it — and this must hold system-wide: an interaction convention applied to one field or one instance of a data type must be applied identically everywhere that trigger, gesture, or affordance appears (auto-advancing focus across sub-fields, tap-to-act on semantically-typed inline data, etc.).
Do: keep a trigger's outcome identical across every activation; if context must change the outcome, make the context change visible rather than silent; apply the same convention consistently across the whole application.
Ask: does this trigger produce the same result every single time, regardless of unrelated app state — and is the convention applied the same way everywhere it appears?
(MI ch2; DI ch8,10)

### Same-looking objects must behave the same everywhere; different behavior needs different appearance `BHV-022`
Two distinct objects should be visually distinguishable if they behave differently, and conversely, objects that look the same — including the same control across different screens — must behave identically wherever they appear. A shared control whose destination or effect varies unpredictably by context breaks the user's model of what that control means.
Do: keep a shared/reused control's behavior identical across every context it appears in.
Ask: does this shared control do the conceptually same thing in every context it appears in — and if two objects look identical, do they actually behave identically?
(MI ch3)

### Gesture semantic-resolution contract: conventional gestures resolve to exactly one predictable meaning `BHV-038`
Established gestures carry strong pre-existing expectations that a component must honor. Double-click resolves to exactly one of two conventional meanings ("open" or "default action"), never a third invented one. Drag-and-drop leans on physical-object intuitions and resolves to exactly one of two meanings per drop target — relocate the item, or apply the target's function to it — predictably and consistently with the cues given during the drag.
Do: map double-click to the single meaning users already expect for this object type; make a drop target's actual behavior predictable and consistent with the drag cues given.
Ask: does the drag/drop behavior match what a user would expect if this were a physical object being moved or placed?
(DI ch6)

### Automatic/system-triggered behavior still needs user-facing settings and a manual override `BHV-019`
Even when a behavior is started by a system trigger, the component should still let the user adjust or disable that automatic behavior, and provide a way to force the same action manually when relevant. The same accommodation applies to a recurring automatic UI (e.g. a startup dialog on every launch): a persistent "don't show again" control protects the audience for whom the recurrence adds no value.
Do: expose settings to adjust/disable an automatic trigger, provide a manual escape hatch, and provide "don't show again" on repeat-shown automatic dialogs.
Ask: if the automatic trigger's precondition silently fails, does the user have any way to force the same behavior manually?
(MI ch2; DI ch3)

### Whole-surface-as-trigger for unfamiliar users `BHV-011`
When target users cannot be trusted to recognize a small conventional control as interactive, make the entire surface the trigger while keeping a smaller visible element (like a button) only as a signifier, not the sole hit area.
When: target users are unfamiliar with the interaction convention; except: the audience already understands standard conventions, where a large invisible hit area could cause accidental activation.
Trade-off: a very large trigger surface increases accidental activation risk if the surrounding area also contains other meaningful content.
(MI ch2)

### Data-forward trigger: let the trigger double as a glanceable state display `BHV-014`
A trigger control can surface the most relevant internal data of the behavior it triggers, even before activation, so the control itself becomes an at-a-glance information source that helps the user decide whether to engage (a stock-ticker icon reflecting price movement, a download icon showing progress).
Ask: what is the single most valuable piece of internal data this control could surface at a glance, before activation?
(MI ch2)

## 3. Rules

### Define rules around the end-state goal, and let the interaction guide the user without feeling memorized `BHV-025`
State a component's purpose as the actual end-state the user is trying to reach ("the user is authenticated," not "the user enters a password"), and keep the rule set tightly focused on that end-state. A rule set necessarily constrains the user, but well-designed rules avoid making the user consciously feel like they're following a rigid, memorized procedure — feedback and in-context cues should guide them implicitly.
Do: state the component's goal as an end-state before writing its rules, and let feedback carry the user through rather than requiring memorization.
Ask: what is the actual end-state this behavior is trying to reach, and does each rule serve it or just describe a step?
(MI ch3)

### A component's rules form a coupled system, not independent toggles `BHV-023`
Changing one governing rule can force a redesign of other dependent rules and the feedback tied to them; rules within a component should be audited together as an interdependent set, not adjusted in isolation.
Trade-off: simplifying one rule for clarity can create hidden inconsistencies elsewhere in the same component.
Ask: what other rules or feedback elements implicitly depend on the rule I am about to change?
(MI ch1)

### Replacing an established rule is only safe when the new behavior is self-evidently better `BHV-024`
Replacing a long-established governing rule breaks the mental model users built over years of practice, and users cannot reconstruct a correct new model from feedback alone unless the change is explained or the benefit is immediately obvious.
When: redesigning the core rule of a long-established behavior; except: the interaction is genuinely new, so no established mental model exists to violate.
Trade-off: a technically superior new rule can still fail in practice if it conflicts with decades of trained user behavior.
Ask: can I write out this new rule in one or two plain sentences a non-expert could follow, and is its benefit immediately visible or only apparent after explanation?
(MI ch3)

### Disclosure contract: rule exceptions, hidden defaults, and side effects on unrelated state must be disclosed via feedback `BHV-018`
Any exception to the user's expected default behavior, any value defaulted silently on the user's behalf, and any effect a rule has on state beyond what the trigger implies must be surfaced through explicit feedback rather than left implicit — including silently closing sibling UI the user never touched. An undisclosed side effect on unrelated state is a critical defect, not a minor rough edge, and can cause irreversible harm.
Do: surface any exception to expected behavior via timely feedback; surface a defaulted decision's actual value directly in the label; disclose any side effect on unrelated state, or better, redesign the rule to have none.
Ask: does this control's rule behave exactly as its label implies in every case, and does activating it change anything the user did not explicitly ask to change?
(MI ch1,3; DI ch4)

### Tesler's Law: decide whether the system or the user absorbs a task's irreducible complexity `BHV-027`
Every task carries irreducible complexity that can only be relocated — to the system (which decides and handles details automatically) or to the user (who retains manual control at the cost of effort). Default to system-absorbed complexity while keeping an intervention/override path available, offloading specifically what systems are inherently better at: fast calculation, doing several things at once, perfect recall, pattern detection, and searching a large set. Where the next step can be predicted confidently, perform or pre-fill it rather than presenting it as an explicit choice.
When: deciding how much of a task's complexity a component should absorb automatically vs. leave to explicit control; except: cases that specifically call for full user control.
Trade-off: system-absorbed complexity reduces user effort but reduces user control and can surprise users when the automatic decision is wrong.
Ask: should the system decide this automatically, and if so is there still a way for the user to intervene when needed?
(MI ch3)

### Two acceptance models for a predicted/suggested value `BHV-028`
Suggestion-acceptance behavior splits into two models: explicit acceptance, where the suggestion is shown as a list the user must actively pick from (good when the user may not know what's needed), and automatic/inline acceptance, where the system pre-fills the top candidate and further typing simply overrides it. The two models can be combined in one control.
Do: choose explicit-list, automatic-inline, or a combination based on whether the user needs a prompt or can rely on a confident single guess.
Ask: does the user need to see the range of options, or can a single best guess be offered and cheaply overridden?
(DI ch8)

### Transform state incrementally on one screen rather than replacing whole screens per step `BHV-026`
For most multi-step microinteractions, prefer incrementally transforming a single screen's state step by step over turning every rule-step into its own full screen; a dedicated new screen is appropriate only for infrequent, clearly distinct, one-off steps.
When: designing the screen-level flow for a multi-step interaction; except: rare, clearly distinct, one-time steps.
Trade-off: full-screen steps can isolate complex/rare decisions cleanly but interrupt the continuity most interactions rely on.
Ask: is this step common and similar enough to the surrounding flow that it should be an in-place change rather than a new screen?
(MI ch3)

### Prefer a single scrollable page over multi-page pagination when navigation between pages is costly `BHV-045`
If moving to the next page/screen carries a real cost (e.g. a web page that must download), a single long scrolling page is usually preferable to splitting content across several separately-loaded pages; conversely, when navigation between screens is instantaneous, per-screen pagination can reduce the physical scrolling required.
Trade-off: one long scrollable page avoids repeated load-wait cost but requires more scrolling; discrete per-screen pages reduce scrolling but each transition may cost a download/wait unless content is already local.
Ask: does moving between pages here carry a real cost, or is navigation effectively instantaneous?
(DI ch10)

### Action-component design contract: correct action, clear label, discoverable, chainable `BHV-037`
For any interface "verb" component (button, menu item, command), the design goal is fourfold: make the correct action available for the task, give it a clear label, make it discoverable, and support chaining/sequencing it with related actions.
Ask: is this the correct action for the task, is its label clear without trial and error, is it discoverable, and can it be chained with related actions to support real task sequences?
(DI ch6)

### Search/filter behavioral contract for complex-data components `BHV-039`
A search/filter/query affordance attached to a complex-data display should be highly interactive (responds fast without disrupting fast typists), repeatable/iterative (lets the user refine and combine search with filtering), context-preserving (shows a result within its surrounding data, not isolated), and compound-condition-capable. After a search or selection, the component should recenter its viewport on the found/selected target rather than merely indicating a result exists off-screen.
Do: use simple one-click controls for straightforward filtering and a fuller query interface for elaborate needs; reposition the viewport on the found target automatically; reuse the navigation mechanism already used elsewhere for search results.
Ask: is the user narrowing by category, or composing more elaborate multi-condition queries — and is it visually obvious where the target is after a search?
(DI ch7)

## 4. Defaults & choices

### Minimize choices: every offered choice adds a rule, must be meaningful, and should be eliminated where possible `BHV-029`
Offering one more choice requires at least one more rule to handle it, so keeping user-facing choices as small as possible is the primary way to keep a rule set minimal — the ideal microinteraction offers no explicit choice at all, operating through a single smart-default path. Every kept choice must be meaningful; where an edge case would otherwise require special-casing the rules, prefer redesigning the input control itself so the case is structurally impossible, rather than adding a rule to detect and reject it later.
Trade-off: fewer choices simplify the rule set but reduce user control over edge preferences.
Ask: could this choice be eliminated in favor of a single smart default, and would offering it make the experience meaningfully more valuable?
(MI ch3)

### A component's defaults should track actual majority user behavior, revisited with usage data `BHV-033`
The most visually prominent option among a set of choices should be the one users actually pick most often, since presentation itself measurably biases which option gets chosen. The same logic applies to a default open/closed state: if usage data or testing shows users routinely override a default, switch it to match observed behavior rather than an a-priori guess.
Do: make the statistically-likely choice visually dominant, and switch a routinely-overridden default to match observed usage.
Ask: does the most visually prominent option match what most users actually want, and does usage data show most users overriding this default anyway?
(MI ch3; DI ch4)

### Sequence a multi-step decision from coarse to fine-grained `BHV-034`
When a user must make a series of related decisions in sequence, order them from simple/broad choices toward progressively more detailed ones, since users decide quickly and confidently when they can easily compare the options in front of them — easiest starting from coarse distinctions.
Ask: am I asking for the most detailed distinction first, or building up to it from coarser choices?
(MI ch3)

### Avoid form fields as a control type where possible; prefill when unavoidable `BHV-035`
Multi-field data entry imposes the highest input burden among control types and should be avoided where a simpler control (button, toggle, dial, slider) can represent the same state. When form fields are genuinely unavoidable, prefill them with the user's previously entered values or a sensible default rather than leaving them empty.
Do: prefill form fields with prior input or a reasonable default when they can't be avoided.
Ask: can this be represented with a simpler control before falling back to form fields?
(MI ch2)

### Use known context to pre-adjust defaults, weighed against privacy risk `BHV-036`
Rather than starting a microinteraction from a generic blank default, use whatever is already known about the user and context (platform, time of day, ambient conditions, and especially past behavior) to proactively adjust initial state, defaults, or copy. Weigh this against privacy: skip using or collecting data whose use could embarrass, endanger, or expose the user, preferring a plain, unpersonalized experience over a privacy-risking one.
Trade-off: personalization improves relevance but increases privacy risk and data-collection burden.
Ask: what do I already know that could make the default more useful right now, and could using this particular signal embarrass, endanger, or expose the user?
(MI ch3)

## 5. Feedback

### Every user-initiated action requires feedback; specific circumstances always require it explicitly `BHV-047`
Any user action on a component must produce feedback — a basic contract, not optional polish. Explicit feedback is required with no exceptions: immediately after a manual trigger or adjustment; when a system trigger materially changes state the user sees or can act on; whenever the user is about to violate, or has violated, a rule; and at the start and end of any process or mode transition. Background/insignificant system-triggered changes may skip feedback.
Do: always confirm manually-triggered actions, always give feedback at a rule violation, and always signal process start/end and mode transitions.
Ask: what does this action look like or sound like to a user who cannot see the visual change?
(MI ch4; IC ch3)

### Gate notification/interruption relevance by the user's current engaged context `BHV-048`
Even within an actively focused surface, not every event should surface as a notification — relevance is contextual to what the user is currently doing. Notify for events tied to the user's current context; for events elsewhere, only interrupt an unrelated task if the event directly addresses the user rather than for every incoming event.
Do: notify for events tied to the user's current context, and interrupt only for events that directly address the currently-engaged user.
Ask: is the user currently engaged with the specific context this event pertains to, and does it directly require this user's attention right now?
(IC ch10)

### Feedback minimalism trio: minimum necessary, causally tied, scaled to importance, never redundant `BHV-049`
Three rules taken together: give the minimum feedback needed to convey current state, not the maximum possible; feedback must be causally/inseparably linked to the actual action or state change it reports, never an arbitrary signal; and using more feedback channels at once increases attention drawn, so the number of simultaneous channels should scale with the message's actual importance. Never duplicate feedback for information already visibly conveyed.
Do: ask what the minimum feedback is before choosing its form; tie feedback directly to the specific change it reports; escalate to multiple channels only for high-importance messages.
Trade-off: more channels are more noticeable but more likely to feel like noise if overused.
Ask: what is the smallest feedback that still communicates the necessary state, and does this signal have a real connection to the action it represents?
(MI ch4)

### Decide the feedback message before its modality; modality is constrained by device capability `BHV-050`
Feedback conventionally communicates one of a small set of things: something happened, the user executed an action, a process started/finished/is ongoing, or the requested action cannot be done. Decide which applies first, then choose its form (visual/audio/haptic or a combination) based on what the hardware actually supports, since available channels vary by device.
Do: decide the message first, then map it to whichever channels are actually available.
Trade-off: richness of feedback vs. hardware constraints.
Ask: which standard feedback message applies here, and what channels does the target hardware actually expose?
(MI ch4)

### Feedback itself needs an explicit rule set along context, duration, intensity, and repetition `BHV-058`
A component's feedback is not necessarily fixed — it can be governed by its own rule set along four axes: context (should feedback change with surrounding conditions?), duration (how long it persists and what stops it), degree/intensity (how bright/fast/loud, and whether that changes over time), and repetition (whether it repeats, at what frequency, for how long).
Do: define feedback along context/duration/intensity/repetition as an explicit rule set, not a one-off.
Ask: should this feedback vary by context, what determines how long it lasts, and does it repeat and for how long?
(MI ch4)

### Feedback and its results must be causally and spatially anchored to the trigger that produced them `BHV-054`
A modal or result panel benefits from a visual anchor connecting it back to the specific control that opened it, rather than a generic centered overlay disconnected from its trigger. More generally, visual feedback should appear where the user's attention already is, since attention narrows while focused on a task and feedback outside that field goes unnoticed unless given motion to draw the eye.
When: a modal is triggered by a specific, visible control with a clear 1:1 relationship; except: the modal represents a global/app-wide state rather than a response to one specific control.
Do: anchor a modal toward its triggering control when the relationship is 1:1; place feedback near the point of user focus, adding motion when it must appear outside that area.
Ask: can this modal be visually anchored to the control that triggered it, and is this feedback placed where the user's attention already is?
(MI ch4; DI ch3)

### Visual feedback default is gated by action origin and whether a response is needed `BHV-053`
Visual feedback should be the default for most user-initiated actions, except actions with no real effect. For system-initiated changes, give visual feedback only as needed, depending on whether the change requires the user's response or is purely informational and optional to act on.
When: except the user action has no real effect (e.g. clicking a non-interactive area).
Do: default to visual feedback for user-initiated actions, and gate system-initiated visual feedback by whether a response is needed.
Ask: did the user initiate this or did the system, and if the system, does it require a response or is it purely informational?
(MI ch4)

### Indicate emphasis/hover/selected state via color or style, never via position or size change `BHV-041`
When an item within a set of visually equal peers needs emphasis, express it through color or other stylistic properties while keeping its position and size identical to its neighbors; content jumping or reflowing on hover is explicitly disruptive.
Do: use color or other non-structural styling to indicate emphasis/hover/selection.
Ask: does the emphasis treatment for this item change its position or size relative to its neighbors? (it must not)
(DI ch4)

### Selected state must read as unambiguous, not rely on color alone `BHV-042`
The currently-selected item in a small set (e.g. a tab) should be visually joined to what it controls (matching background, connected border) so the two read as one continuous unit, rather than relying on a color change alone — this must remain unambiguous even with as few as two options.
Do: visually connect the selected item to what it controls as one continuous shape/unit.
Ask: with only two options present, is it still immediately obvious which one is selected?
(DI ch4)

### Preview the pending drop position live during drag-and-drop repositioning `BHV-043`
When draggable panels are repositioned within a fixed layout grid of drop slots, show a "ghost" — a dashed-outline placeholder — that dynamically indicates where the dragged item will land as the user drags it over each candidate slot.
When: draggable panels use a fixed layout grid of drop slots rather than fully free positioning.
Do: render a dashed/outlined ghost preview at the candidate drop slot as the user drags over it.
Ask: during a drag, is it visually obvious where the item will land if dropped right now?
(DI ch4)

### Animation-as-feedback contract: fast, smooth, natural, purposeful, directionally coherent, and short `BHV-055`
Because the brain reacts strongly to motion, use animation sparingly and, when used, keep it fast (never delaying the underlying action), smooth, natural (follows physical laws like gravity/inertia), simple, and purposeful (communicates something real, never mere polish). Its direction must map predictably to the change it represents and stay coherent with the spatial model already established. For duration, take the initially-intended length, halve it, then halve again if it still reads clearly; an animation must never make the interaction feel less efficient than not animating at all.
Trade-off: shorter animation may sacrifice some legibility of the transition for responsiveness.
Ask: does this animation communicate structure, state, or a relationship the user needs, and is its exit/continuation motion coherent with the entry animation's spatial model?
(MI ch4)

### Sound feedback contract: emphasis vs. alert, the foghorn test, mutability, and non-confusable earcons `BHV-056`
Sound falls into two roles: "emphasis" sounds reinforce that a user-caused action happened (best paired with visual feedback), and "alert" sounds signal a system-initiated change or anomaly. Any sound must pass the foghorn test — even without visual confirmation, the information must be important enough that the user genuinely needs to know it — and a mute option must be provided regardless. Distinct events must use distinct, non-confusable earcons, generally well under a second, with an exception for a continuous low tone indicating an ongoing background process; the same earcon must never be reused across different event types.
Trade-off: sound conveys urgency effectively but is the most disruptive channel.
Ask: if the user could not see this action happen, would they genuinely need to know it happened via sound — and could this earcon be mistaken for a different event's?
(MI ch4)

### Voice feedback requiring a spoken response must constrain the response to a short, definite set `BHV-057`
When voice feedback requires the user to respond by speaking, valid response options must be short, explicit, and limited to two or three choices, not open-ended — the prompt should end with the exact word the user needs to say.
Do: end voice prompts with the specific action word the user should say.
Ask: are the valid spoken responses reduced to 2-3 explicit choices, and does the prompt end with the exact word to say?
(MI ch4)

### Haptic feedback contract: low bandwidth limits it to simple confirmation/alert signals `BHV-067`
Touch sensitivity is far lower-bandwidth than sight or hearing — roughly 1% of what hearing can convey — and most people can only distinguish about 3-4 vibration intensity levels. Haptic feedback's three legitimate uses are: confirming that a physical action was actually registered, alerting the user when sound is unavailable or undesirable, and simulating surface texture/friction (less common).
Do: use haptics for simple confirmation, or as a sound-unavailable alert.
(MI ch4)

### Microcopy contract: labels and feedback copy must be accurate, minimal, consistent, and neutral `BHV-017`
Every label and feedback message must: tell the user in advance what will actually happen, not vague or clever copy; use the user's own plain vocabulary rather than jargon; refer to the same concept with the same word every time within a component; be accurate at the moment shown; fit in one line where possible; use neutral, non-accusatory phrasing rather than blame; use relative time expressions except where precision matters; avoid double negatives; and frame consequences positively (reward the desired action) rather than punitively, consistently across every occurrence of the same event.
When: except the audience is domain experts (where domain jargon is clearer), or scheduling contexts requiring an exact time value.
Ask: does this label tell the user what will actually happen in their own vocabulary, and is the same word used for the same concept everywhere in this component?
(MI ch2,3,4)

### Feedback tone: brief personality is fine at friction points, but must stay surface-level and not feel like surveillance `BHV-052`
Feedback is a legitimate place to express brief product personality, especially at friction points like errors or long waits, where a humanized response defuses frustration. This must stay surface-level — over-personifying backfires the way the uncanny valley does, setting expectations the component can't meet. When personality is based on collected user data, the personalization must not make the underlying data collection feel exposed or surveillance-like.
When: except feedback needs to be strictly neutral/functional (e.g. safety-critical contexts).
Trade-off: more personality increases charm but risks unmet expectations or discomfort past a threshold; personalization value trades against perceived privacy intrusion.
Ask: does this feedback set an expectation of intelligence the component can't actually deliver, and does it make the underlying data collection feel exposed?
(MI ch4)

### Gatekeeper components should prioritize speed and ease over memorable delight `BHV-063`
For a component that blocks or gates access to the rest of a product's functionality (e.g. a login flow), the goal should be speed and ease, not delight or memorability — especially important precisely because the rest of the app is unusable until the gatekeeper is cleared.
When: except the component is not a blocking gatekeeper, where delight would not slow down critical usage.
Trade-off: memorability/delight vs. speed and frictionlessness, weighted by whether the component blocks other usage.
Ask: does this component block access to the rest of the product until completed, and if so, is speed being prioritized over delight?
(MI ch6)

### Reuse existing UI elements as feedback carriers instead of adding new ones `BHV-051`
Repurpose standard interface parts already on screen — scrollbars, cursors, progress bars, tooltips, hover states — as feedback carriers rather than adding new UI elements, conveying more information without growing the interface's surface area.
When: avoid where the repurposed meaning would be non-obvious or would conflict with the element's primary role.
Trade-off: discoverability of repurposed meaning vs. avoiding visual clutter.
Ask: can an existing on-screen element already carry this feedback instead of adding a new one?
(MI ch4)

## 6. Error prevention

### Error prevention over error messaging: poka-yoke first, silent retry second, pop-up last `BHV-030`
Error prevention is a core function of a component's rules, not an afterthought. Apply poka-yoke: design the rule, and the physical form of a control where applicable, so an erroneous input or action literally cannot occur, rather than only detecting it afterward. When a failure does occur, first retry silently if the condition may be transient, or attempt to resolve/route around the problem automatically (e.g. silently widening a zero-result search radius and reporting the adjustment). A pop-up error message is a last resort — a correctly-operated microinteraction ideally shows no message at all.
Trade-off: mistake-proofing reduces user control/flexibility in exchange for reduced error rate — generally favorable for microinteractions; retry delay trades against immediacy of error transparency.
Ask: can the rule be redesigned so this mistake is structurally impossible, and before showing an error, can it be resolved or worked around automatically?
(MI ch3,4)

### Error feedback must include the correction path, not just the problem `BHV-031`
When feedback reports an error, the message should state not only what went wrong but also how to fix it — ideally by providing the corrective UI alongside the message itself (e.g. showing the password re-entry field together with the "incorrect password" message).
Do: pair error messages with the specific corrective action or control, shown right alongside the error.
Ask: does this error message tell the user how to fix the problem, not just that one exists?
(MI ch4)

### Rules can prevent intentional misuse, not only accidental input errors `BHV-032`
A component's rules can proactively filter or redirect disallowed input to guard against intentional misuse, distinct from catching accidental data-entry mistakes — e.g. blocking profanity in a comment field, or preventing the exact same action from being repeated identically (blocking a duplicate post).
Ask: beyond accidental mistakes, could this input/action be intentionally misused, and should the rule guard against that too?
(MI ch3)

### Touch controls must tolerate imprecise input, with a tappable hit area larger than the visible target `BHV-044`
Because a moving device or a moving user makes precise touch nearly impossible, touch-oriented components should be forgiving of imprecise taps and make mistakes cheap and easy to correct. A control's effective touch-sensitive hit area does not have to match its rendered visual size — the interactive area can extend invisibly into surrounding margin/whitespace.
Do: make accidental taps cheap to undo or correct, and surround visible touch targets with generous tappable padding, targeting roughly a platform-specific minimum (e.g. ~44x44px) for the effective hit area.
Ask: is this touch target's effective hit area large enough, even if its visible footprint stays compact?
(DI ch10)

## 7. Loops & timing

### Loop/mode contract: persisting or repeating behavior needs an explicit termination model `BHV-059`
Loop/mode is the meta-rule governing how a behavior persists over time — whether it stays engaged until manually turned off, terminates on a condition, or suspends/resumes when interrupted. Four forms cover most cases: count-controlled (fixed repetitions then ends), condition-controlled (repeats while a condition holds), collection-controlled (iterates over a set then ends), and infinite (doesn't end until an error or forced stop).
When: except infinite loops are legitimate when the behavior is genuinely meant to persist until explicitly stopped (e.g. a light staying on).
Do: pick the loop form whose termination condition matches the actual requirement.
Ask: does this behavior end after one cycle, persist until stopped, end on a condition, or pause/resume on interruption — and what stops the repetition?
(MI ch1,5)

### Open loop vs. closed loop: choose based on whether the behavior needs to self-adjust from feedback `BHV-060`
An open loop runs to completion without reacting to feedback (e.g. "turn on the light every day at 10pm"). A closed loop has a feedback mechanism and self-adjusts based on it (e.g. adjusting volume in response to measured ambient noise). Choose closed loop when the repeating behavior should adapt to changing conditions, open loop when it should not.
Trade-off: closed loops adapt better but add complexity and unpredictability compared to open loops.
Ask: should this repeating behavior adjust itself based on ongoing feedback, or run identically each time?
(MI ch5)

### Loop timing parameters strongly affect perceived responsiveness `BHV-061`
A loop's repetition count/period materially shapes the user's experience: too short a period feels rushed or annoying, too long feels sluggish or unresponsive. Loop parameters need the same deliberate tuning as any other algorithm parameter.
Trade-off: faster loops feel responsive but can feel rushed/naggy; slower loops feel calm but can feel unresponsive.
Ask: does this loop's period feel rushed, sluggish, or right for the task at hand?
(MI ch5)

### Loop-based auto-termination is useful but risks annoying the user if mistuned `BHV-062`
Loops can cap how long a state persists or end a microinteraction altogether (e.g. auto-logging a user out after inactivity for security, or rate-limiting a rapidly repeated action). This pattern is legitimate but must be tuned carefully against real usage, since an overly aggressive or ill-matched threshold becomes an annoyance.
Trade-off: security/abuse prevention vs. user convenience and annoyance.
Ask: is the inactivity/rate threshold generous enough to avoid punishing normal use?
(MI ch5)

### Batch rapidly repeated user actions into one animation, not one animation per repetition `BHV-040`
When a user triggers the same incremental action many times in quick succession, the component should combine the repeated actions into a single animated transition rather than replaying a full transition for every repetition — otherwise animations stack up and force the user to wait through many redundant transitions to see the cumulative result.
Do: detect rapid repetition of the same action and animate only the net/cumulative result once.
Ask: if the user repeats this action 10 times quickly, will they watch 10 sequential animations, or does the component collapse them into one?
(DI ch3)
