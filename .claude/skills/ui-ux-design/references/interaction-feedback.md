# Interaction, Feedback & Microinteractions

Load when: designing or reviewing a trigger, control, feedback moment, loading state, error message, undo path, mode, loop, or any single-microinteraction detail.

Contents: Triggers & Discoverability · Interaction Rules, Defaults & Completion · Feedback, Restraint & Animation · Loading, Progress, Waits & Cancellation · Error Prevention & Recovery · Modes, Loops, Undo & Repetition · Testing, Composition & Polish

## Triggers & Discoverability

### Trigger identity must stay truthful and consistent
Same-looking control = same behavior everywhere, every time — never a shortcut meaning one thing usually and something destructive elsewhere, or a non-interactive element styled clickable. Design distinct waiting/hover/activated/active/toggle states; keep status indicators adjacent to their control; surface the control's single most valuable live-data point on it.
⟨mi1-013, mi2-047, mi1-036, di1-014, mi1-015, di3-017, mi1-024, mi1-014⟩

### Match control type and prominence to states and frequency
Pick type by state count: single action → button/gesture; on/off → toggle (repeat-press only if result reads unambiguously); few states → dial/buttons; continuous range → slider/dial/increment; multi-input → prefilled fields. Frequent actions favor at-a-glance state unless speed matters and error risk is low; infrequent favor the simplest, most explicit control. Scale visibility to frequency (moving object > object+signifier+label > labeled object > icon > label > invisible); reserve motion/sound for top priority only.
⟨mi1-016, mi1-052, mi1-017, mi1-018, mi1-019, mi1-020⟩

### Hidden triggers need a learnable discovery path
No-label actions (double-click, shortcuts, drag-drop, gestures, sensors, voice) must be learnable via some visible affordance, near-universal, or restricted to a narrow, memorable rule set. Pair a high-priority invisible trigger with a visible fallback unless technically impossible. Show a conditional trigger only when its precondition holds, not permanently disabled. Hide deliberately for hierarchy, never as default minimalism (no-screen devices, e.g. Google Glass, may rely on invisible triggers alone).
⟨mi1-022, di3-016, mi1-012, mi1-023, mi1-021⟩
⚖ Tension: hiding controls vs discoverability → act-d01

### System triggers need visibility, configuration, and manual override
Even an automatic trigger the user can't invoke manually needs an opt-out — ideally inline when it fires, at minimum granular per-event settings, never one blanket toggle — plus a manual force-action alongside it. Decide explicitly: firing frequency, what context tunes it, whether firing is visibly indicated, retry/abort on failure.
- Avoid: unconfigurable trigger conditions; push notifications as a retention tactic.
⟨mi1-007, mi1-027, mi1-028, mi1-029, uxp1-083⟩

### Match the action-exposure mechanism to visibility, space, and input device
Choose among buttons, menu bars, popup/context menus, toolbars, links, action panels, hover tools by how visible/space-efficient the set needs to be. Cluster related actions into small, aligned button groups (split past 3-4); reveal per-item hover actions only on mouse-primary UIs; use always-visible action panels near the target object when actions don't map to a menu bar.
- Avoid: dropdown-as-action-trigger; hover-only exposure on touch; mixed-scope button groups.
⟨di3-015, di3-018, di3-019, di3-020⟩
⚖ Tension: show options vs hide behind menu → forms-d01

### Shortcuts must never be the only path
Offer accelerators for frequent actions, but never make an important action reachable only via a shortcut or hard-to-find control. Make the shortcut itself easy to discover — a buried one gets ignored in favor of familiar, slower habitual paths.
⟨mi1-056, psy2-017⟩

### Quick reference
- In feature-parity markets or on small/constrained-screen/no-screen devices, invest disproportionately in microinteraction polish over new features, reducing the product to one tight essential scenario. ⟨mi1-004, mi1-005⟩
- For immersive full-screen mobile content, hide controls by default and reveal a small semi-transparent overlay only on tap, auto-hiding after brief inactivity or a tap elsewhere. ⟨di4-033⟩

## Interaction Rules, Defaults & Completion

### Design all four parts of every microinteraction
Explicitly define what starts it (trigger), what happens (rules), how the user perceives the result (feedback), and its repeat/expire/change behavior (loop/mode). Never leave any part implicit — an undesigned feedback or loop/mode part causes confusion even when the core rule works.
⟨mi1-006⟩

### Scope one task per microinteraction; audit the small stuff
A microinteraction accomplishes exactly one bounded task. Budget real design/dev time early, not as filler; audit small/mundane interactions (delete, a dead search button) as rigorously as major features — overall quality never exceeds the worst small element.
⟨mi1-001, mi1-002, mi1-003⟩

### Give completion buttons a specific label; preview costly actions
Place a large, clearly-labeled (real button, not a link) completion control at the flow's end-point, with a specific verb ("Send", "Purchase") not generic "Done," near the last input. Rewrite context-dependent labels to state exactly what they'll do; disable when no valid target exists. Before a costly, hard-to-reverse, or unfamiliar action, show a preview letting the user commit or correct from the same screen.
⟨di3-021, di3-022, di3-023⟩

### State purpose as end-state; write rules you can explain simply
State purpose as the final state reached ("get the user into the system"), not an intermediate step. If you can't explain the rule set simply, redesign — don't ship and hope feedback teaches users. Check rules against 9 questions (trigger response, control over automation, step order, data sources, algorithm/parameters, feedback per step, mode, loop, end/transition); list in prose, then flowchart to expose hidden complexity.
⟨mi1-032, mi1-033, mi1-031, mi1-034, mi1-035⟩

### Prefer single-screen state changes over multi-screen wizards
Default to progressively revealing/changing state within one screen; reserve wizards for infrequent, one-off interactions with clearly distinct steps. Design every directly-manipulated object's waiting, active, and updated appearance explicitly. Use range constraints to prevent invalid states outright.
- Trade-off: wizards suit rare/first-time flows; single-screen suits frequent ones.
⟨mi1-037, mi1-038, mi1-039⟩
⚖ Tension: wizard vs settings-editor → struct-d01

### Personalize by default using known context (Tesler's Law)
Use available signals (platform, time, ambient noise, time-since-use, battery, location, especially past behavior) to personalize by default — except where a signal could embarrass, expose, or endanger the user (medical contexts), where generic is safer. Treat task complexity as irreducible: default to system-absorbed, not user-facing; decide who owns each decision point; auto-fill what the system knows.
⟨mi1-040, mi1-041, laws1-058, mi1-042, mi1-043, laws1-060, laws1-059⟩

### Minimize and deliberately bias choice architecture
Minimize offered choices — each needs at least one more rule. Replace explicit choice with a smart default wherever possible; auto-perform or pre-highlight the predictable next step. Give the most-taken option visual prominence, but never exploit it to mislead. Disclose a consequential default's concrete effect in the UI. Never offer choices that fork the whole rule set without a path back (small bounded choices, e.g. a 3-position setting, are fine); sequence multi-step choices broad-to-detailed.
⟨mi1-044, mi1-045, mi1-048, mi1-049, mi1-046, mi1-050, mi1-047⟩
⚖ Tension: fewer choices vs reversibility-control → act-d04

### Design against edge cases structurally; never share a control across mismatched-severity functions
Cutting choices removes rare edge cases that would derail the common case — use structurally-constrained inputs (dropdowns, pickers) instead of free text wherever the range is well-defined. Never combine two functions of very different consequence on one control that could be confused under time pressure (e.g. mute doubling as volume-down).
⟨mi1-051, mi1-053⟩

### Accept the widest reasonable input variety; order lists by real likelihood
For free-text fields representing structured values (phone, email), accept every plausible format and normalize behind the scenes rather than rejecting non-matching ones. Order selection lists by expected frequency, not always alphabetically, when alphabetical would bury the likely choice.
⟨mi1-054, mi1-055⟩

### Microcopy: earn every word, stay accurate, stay persistent
Prefer conveying meaning through visual design; add text only to remove real ambiguity. When needed: short, plain, validated with real users; label directional controls; match wording between a control and its copy; one name per concept everywhere; relative time casually, absolute when time-critical; no double negatives; label above/on/inside the control; pair a persistent label with placeholder-as-example, never alone; append "…" when activation needs another step.
⟨mi1-060, mi1-061, mi1-062, mi1-063, mi1-064, mi1-065, mi1-066, mi1-067, mi1-068, uxp1-005, mi1-025, mi1-026⟩
⚖ Tension: simple vs precise vocabulary → label-d02

### Only break a well-established interaction when the replacement is obviously better
Users carry real expectations from years of habit. Violate them only when the new behavior is clearly, at-a-glance, more valuable — never merely different (cf. Apple's "Save As" redesign backlash).
⟨mi1-030⟩

### Quick reference
- For computed/ranked/algorithmic rules, specify step sequence, branches, repetition granularity, and tunable variables; disclose variables when it would let users meaningfully improve their behavior (Nike FuelBand's hidden formula blocked this); weigh human value, not just computational efficiency, in ranking/recommendation logic. ⟨mi1-069, mi1-070, mi1-071⟩ ⚖ Tension: metric vs judgment → act-d06

## Feedback, Restraint & Animation

### Feedback confirms what happened and what resulted, at minimum necessary signal
Always confirm two things — what action was taken, and what resulted — without exposing the internal mechanism (unlike a slot machine, which hides its own). Give the minimum feedback that communicates current state; decide the message first, then use the fewest channels its importance justifies (low-stakes background triggers can skip it). Mandatory right after a manual trigger, on any significant system-triggered change, when a rule is about to be/has been broken, on a command that can't execute (retry silently first), and as a progress estimate for slow processes.
⟨mi2-001, mi2-002, mi2-008, mi2-003⟩

### Decide feedback content/timing before channel; keep non-text feedback learnable and safe
Settle necessity and timing first; only then choose form (visual/audio/haptic), constrained by actual hardware. When text isn't reliable, use non-text signals users can learn through repeated use, and never attach a punishing consequence to a plausible misreading. Feedback should feel like it IS the action (a click sound that plausibly is the mechanism closing), not a generic acknowledgment.
⟨mi2-004, mi2-005, mi2-006, mi2-007⟩

### Prefer visual feedback via existing/minimal elements, in the user's current attention area
Before adding a new UI element, check whether an existing one (scrollbar, cursor, progress bar, tooltip, hover state) can be repurposed, or whether a minimal persistent signal (a title-bar dot for unsaved changes) suffices. Never show the same info twice; minimize visual effects as frequency increases; reserve blinking for must-notice cases; place feedback near where the user is looking, using motion (fade-in) if it must appear elsewhere (meaningless actions like clicking empty space need none).
⟨mi2-009, mi2-013, mi2-014, uxp1-079⟩

### Default to no animation; when used, it must let users predict the interaction
Add animation only when it meaningfully increases engagement while conveying real information. Its motion must let users predict the interaction (consistent direction: enters left, exits right). Good animation is fast, smooth, natural, simple, purposeful — justify each against the 8 legitimate reasons (context, explanation, relationships, focus, faster-feeling wait, virtual space, engagement). Set duration from an intuitive guess, then halve it (twice if it still works).
⟨mi2-015, mi2-016, mi2-017, mi2-018, mi2-019, mi2-020⟩

### Error messages: accurate, specific, actionable, blame-free
Accuracy above all — a clear-sounding but wrong message ("Installation complete" mid-install) is worse than an ambiguous one. State what the user did, what went wrong, and an explicit fix, ideally inline; never a bare "Error" label. One line, active voice, verb naming the next action; avoid blame phrasing ("Password is incorrect," not "Your password is incorrect").
- Exception: spoken/voice interfaces can use first-person address more comfortably than written text.
⟨mi2-021, psy2-052⟩

### Vary feedback deliberately, but stay consistent and reward-oriented
Feedback needn't be identical every time — define explicit rules for context, duration, intensity, and repetition variance. Once set, apply consistently: reinforce desired behavior positively and predictably; never punish; never design intermittent/unpredictable feedback purely to boost engagement, slot-machine style.
⟨mi2-027, mi2-028⟩

### Quick reference
- The moments users are most frustrated (errors, long waits) are the best place for light, surface-level personality to defuse tension — keep it sparing, never blaming/mocking, and never expose the data-collection mechanism when personalizing feedback, only its benefit. ⟨mi2-010, mi2-011, mi2-012⟩
- Reserve sound for the "foghorn test" (important even unseen), always allow muting, distinguish emphasis sounds (confirm a user action, pair with visual) from alert sounds (system event); earcons under 1s, played once, familiar-associable, never reused for an unrelated event; speech is slow, high-bandwidth — limit prompts to 2-3 short choices, required action last; haptics confirm an action or simple alert only (3-4 levels max). ⟨mi2-022, mi2-023, psy1-060, mi2-024, mi2-025, mi2-026⟩
- Rare-but-critical events (near-empty battery, security threat, system failure) need an unmistakable, high-salience alert surfaced earlier than strictly necessary — users' calibrated expectations make rare events the most likely to be missed. ⟨psy1-055⟩ ⚖ Tension: detection sensitivity → act-d05

## Loading, Progress, Waits & Cancellation

### Use the Doherty threshold's bands to choose feedback technique
Target sub-0.4s responses for interactive feedback, not just final results — productivity rises non-linearly below this threshold. Bands: under ~0.1s unnoticed; 0.1-0.3s noticeable, feels like reduced control; beyond ~1s attention drifts and cognitive load rises.
⟨laws1-064, laws1-065⟩

### Use skeleton screens and blur-up image loading
Show a structural placeholder the moment loading starts instead of a blank screen, swapping in real content as it arrives — feels faster and reserves layout space. For images, load a tiny blurred version first and cross-fade to full resolution, avoiding both pixelation and layout shift.
⟨laws1-066, laws1-067⟩

### Show progress for any ~2+ second wait; one continuous bar when duration is knowable
For any UI-interrupting or background operation over ~2s: show what's happening, fraction complete, time remaining, how to cancel — keep the rest of the UI operable where possible. A progress indicator increases patience regardless of accuracy; consistent durations reduce frustration. When step count is knowable, use one continuous left-to-right bar, never multiple bars restarting per sub-phase (a rough non-percentage animation is fine when true progress can't be computed). On mobile, show progress where content will appear, rendering what's already available.
⟨laws1-068, di3-024, psy1-050, uxp1-073, di4-039⟩

### Spinner vs. bar; never loop-and-refill; add % or ETA only when reliable
Use a spinner, not a bar, when duration is unknowable or the wait is very short — it must reflect real state, stopping/updating on failure. Never let a bar fill and refill from zero — test over real network conditions, not localhost. Add a percentage only for waits long enough to read; "time remaining" replaces it only when the estimate is genuinely reliable, since an inaccurate one damages trust more than none. Past ~10s, give ETA and current status.
⟨uxp1-074, uxp1-075, laws1-069, uxp1-076⟩

### Use optimistic UI to make near-certain actions feel instant
For actions that almost always succeed, show success feedback before server confirmation, surfacing an error afterward only on genuine failure. Improves perceived speed without changing real processing time.
⟨laws1-070⟩
⚖ Tension: speed-optimism vs deliberate friction → act-d02

### Give unavoidable waits a worthwhile task; let users cancel instantly
Give waiting users something genuinely valuable to do, not obvious busywork — absent a real reason, people default to idling. Let users cancel any slow process instantly, beside its progress indicator: try making the process feel instantaneous first; label cancel clearly; act on click (delay past 1-2s breeds doubt it worked); confirm cancellation; separate control per action when several run in parallel.
⟨psy2-040, di3-025⟩

### Quick reference
- Moderate stress/arousal improves performance up to a point (Yerkes-Dodson), tipping sooner for difficult tasks — add mild arousal cues for boring/simple tasks, strip distractions from difficult/high-stakes ones; under stress, users perseverate (repeat the same failed action, even skilled ones), so error recovery must explicitly interrupt that loop; test under realistic stress conditions, not just apparent simplicity. ⟨psy2-054, psy2-055, psy2-056, psy2-057⟩

## Error Prevention & Recovery

### Prevent errors structurally first, then auto-resolve, then message
Design controls so an erroneous state is literally impossible where feasible (Apple's reversible Lightning connector), not just caught after the fact. Correct input triggers zero extra messaging; reserve error messages for what the system can't handle, trying auto-recovery first (e.g. auto-widen a zero-result search) before a plain error. Don't aim for zero errors — scale prevention to that failure's actual cost; reserve maximum investment for high-consequence domains.
⟨mi1-057, mi1-058, psy2-051, mi1-059, psy2-050⟩

### Confirmation dialogs don't reliably stop habituated destructive actions
Don't rely on a confirmation dialog to stop a habituated destructive action — dismissing it becomes just as habituated and unconsciously bypassed as the original action. Prefer removing the risky default path entirely, or relying on strong undo.
⟨di1-015⟩

### Quick reference
- Classify each usability-test error by outcome (positive: useful info even off-path; negative: blocked/undid/unrecoverable — prioritize these; neutral: no effect) and by type (commission: extra step; omission: skipped step; wrong-action: right procedure, wrong choice; motor-control: physical slip) — each type implies a different fix. ⟨psy2-058, psy2-059⟩
- Structure navigation to support systematic-search error recovery, the most reliable of the three strategies (systematic, trial-and-error, perseverative). Don't assume older users will fail — completion rates matched younger users in studies, though older users took more steps and relied more on trial-and-error; weight product-category experience over age. ⟨psy2-062, psy2-063, psy2-064⟩

## Modes, Loops, Undo & Repetition

### Avoid modes by default — zero is ideal
A mode is a branch point where the same input yields different results depending on hidden state; avoid adding modes wherever possible — most microinteractions should have zero, none more than one. The one legitimate reason: isolating an infrequent operation (e.g. settings) that would otherwise clutter the primary task; a mode should be a small detour, out and back.
⟨mi2-029, mi2-030⟩

### When a mode is unavoidable: dedicated screen, preserved state, spring-loaded/one-off
Give a genuinely necessary mode its own screen (an explicit exception to "no screen per rule") with an entry/exit transition marking the departure. Preserve untouched state on return, reflecting changes made inside. A spring-loaded mode (quasimode) stays active only while a physical trigger is held, ending the instant it releases — use sparingly, gesture explicitly labeled. A one-off mode activates for one bounded operation and auto-releases — always pair with a timeout.
⟨mi2-031, mi2-032, mi2-033, mi2-034⟩
⚖ Tension: auto-terminate vs interruption → act-d07

### Use long loops so the microinteraction improves with repeated use ("Long Wow")
A microinteraction that doesn't get better with use has something wrong with its design. Use session-, day-, or account-spanning loops to deliver new value over time — remembering prior settings/state is a concrete realization. Progressively reveal shortcuts and strip labels as familiarity grows — but reset to the fully-labeled state for a lapsed user, rather than assuming continued expertise.
⟨mi2-038, mi2-039⟩
⚖ Tension: progressive disclosure vs recognition → cog-d02

### Reversibility is a safety net: cheap exploration, multi-level undo, grace-period undo
Let users try unfamiliar actions and back out at no cost — even a minor annoyance kills willingness to experiment. Beyond simple navigation/forms (no full undo model needed there), provide reverse-order multi-level undo for file/layout/creation/reorder/cut-copy-paste changes, with a stable model of one undoable unit; keep a stack of 10-12+ items; name operations from the user's mental model, not the implementation; never make transient state (selection, scroll) undoable. For destructive or hard-to-reverse actions, give a short recall window via toast/banner before finalizing.
⟨di1-007, di3-026, uxp1-054⟩

### Streamline and batch repeated action sequences
When a task repeats the same operation many times, let the user do the whole set with as little input as possible — ideally one action per repetition, or one for all. Provide a "do it once" and "do it to everything" option together (Replace / Replace All), plus multi-select with a single bulk action; make the last action and full history easy to undo. Observe users directly — unconscious repetition often goes unreported.
⟨di1-019, psy1-054⟩

### Quick reference
- Match loop type to its real termination condition — for-loop (fixed attempts), while-loop (continues while a condition holds), collection-control loop (once over a known set), infinite loop (only error/manual intervention stops it, for genuinely ongoing states) — and deliberately tune period/duration and open- (fires regardless) vs. closed-loop (adapts to feedback) behavior. ⟨mi2-035, mi2-036⟩
- Keep a visible, chronological, appropriately-granular command history (one bulk action = one entry), persisted across sessions, letting users recall, repeat, or convert past actions into a named, parameterizable macro that can call other macros and run against multiple objects — avoid the word "programming" with non-programmers, restrict macro power where scripting access is a security risk. ⟨di3-027, di3-028⟩

## Testing, Composition & Polish

### Verify purpose, key data, microcopy, and time/flow in testing; map reactions to their cause
Confirm four things: overall purpose (a status message's job is to "convey," not merely "display"); which data actually matters; whether microcopy is clear; and time/flow. Map reactions to cause: excessive clicks → too much effort; "why am I doing this" → wrong labels; "not sure what happened" → unclear feedback; "where am I" → transitions/modes problem; not noticing a control → hierarchy problem; "I didn't know I could do that" → hidden trigger.
⟨mi2-053, mi2-054⟩

### Run a structured, multi-round test protocol with real, diverse target users, early
Per session: ask pre-exposure expectations; let users attempt it unassisted while collecting quantitative data; walk through again with them narrating decisions, checking they can explain the rules; ask what they'd want to remember tomorrow; close with the single most important fix. Run at least two rounds with a revision between. Recruit real, diverse target users, never convenient proxies, starting as early as paper prototypes exist; even under 10 participants helps, and one 5-user test surfaces ~85% of usability problems.
⟨mi2-058, uxp1-100, psy2-053⟩

### Classify an embedded microinteraction's role; default to fast/easy when it gates access
Before designing a microinteraction embedded in a larger feature, determine its relationship to it — activate (login), control (pause), sub-function (formatting tool), or terminate (off switch) — and its persistence relative to the feature's lifecycle. For most, "should this be memorable" is no: prioritize speed and ease, especially when it stands between the user and the rest of the product.
- Exception: a microinteraction intentionally chosen as the product's signature "memorable moment."
⟨mi2-042, mi2-043⟩
⚖ Tension: convention vs signature moment → act-d03

### Design empty and first-run states as a teaching moment; keep onboarding tips skippable
For user-generated content, design the empty state deliberately (illustration, emphasized call-to-action) rather than a bare placeholder; hide dependent chrome (tabs, filters) until there's content for it to act on. Use it to teach the specific first action, since a new user sees it exactly once. Onboarding tips must be skippable in one action, stop after completion, and never re-force on returning users (even after an update resets onboarding state) — a UI needing extensive tips is too complex.
⟨rui1-092, uxp1-055, uxp1-056⟩

### Quick reference
- A microinteraction's core concept is already justified — test its flow/structure (trigger→rule→feedback→loop) at near-full fidelity, since structural connections don't survive faking cheaply; testability varies by platform (desktop rarely worth it alone; web cheap; mobile increasingly necessary; physical devices essential but slow). ⟨mi2-048, mi2-049, mi2-050⟩
- Microinteraction changes have small effect sizes — a standard 5-8 person qualitative test can't reliably detect them; budget ~20+ testers, prefer quantitative/analytics data for subtle differences; watch for test-protocol artifacts (e.g. interrupting mid-task) causing errors that wouldn't occur in real use. ⟨mi2-051, mi2-052⟩
- Track completion rate, geometric-mean task time (not median — slow users skew it 5-10x), step and click/tap counts, system errors, and human errors split into slips (careless execution) vs. mistakes (misunderstood the rule); use 1-7 rating scales for satisfaction/difficulty/trust/usefulness, treating results as lower-reliability with small tester counts. ⟨mi2-055, mi2-056⟩
- Documentation fidelity ranks: working prototype > video (timing/flow) > storyboards (state context, not timing) > static screenshots (never rely on these alone) — combine methods; static-only should still cover the trigger, key rules, and the ending as a "what and why" story. ⟨mi2-040, mi2-041⟩
- Composing microinteractions into a feature: choose which gets visual/audio emphasis (not all equal), keep feedback tone consistent, and map every piece's handoffs so the seams stay invisible/inaudible as the feature grows. ⟨mi2-044, mi2-045⟩
- To polish a lackluster microinteraction, checklist: memorable moment or not; user/context data to leverage; most important data foregrounded; custom control worth it; error preventable; overlooked UI/hardware elements; invisible shortcut for experts; natural text/humor; animation/transition worth adding; other feedback channels; what improves by the 2nd or 100th use, or via a long loop. ⟨mi2-046⟩
