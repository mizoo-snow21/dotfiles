# Pattern Catalog — Actions & Commands

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

## Actions & Commands

### Choosing Where to Expose a Set of Actions `PTN-061`
Action-exposure patterns form a spectrum trading exhaustiveness, visibility, and space: Menu
Bar (everything, always available, accessible fallback) → Popup/Context Menu (situational
subset, on demand) → Toolbar/Button Groups (small persistent, visually-grouped, scoped set) →
Hover Tools (per-item, hidden until needed, mouse-only) → Action Panels (persistently visible,
richly laid out, most space-hungry but most flexible). Do: match the pattern to the action
set's size/scope/required visibility rather than designer familiarity; verify
keyboard/screen-reader access survives the chosen mechanism. Trade-off: exhaustive
always-visible exposure costs space or an extra step; situational lightweight exposure saves
space but sacrifices discoverability or touch compatibility. Ask: would an unfamiliar user
find this action through the chosen mechanism? Does it still work for keyboard-only and
touch-only users? (DI ch6)

### Action Component Design Goal `PTN-047`
For any interface "verb" component (button, menu item, command), the goal is fourfold: the
correct action for the task, a clear label, discoverability, and support for chaining with
related actions. Ask: is this the correct action, not just a plausible one? Is it discoverable?
Can it be chained with related actions? (DI ch6)

### Drag-and-Drop `PTN-048`
Drag-and-drop leans on physical-world intuition, not learned software convention, so a drop
target's behavior must resolve unambiguously to exactly one of two meanings: relocate the
item, or apply the target's own function to it — never something else. Ask: when dropped here,
does this relocate/reparent the item, or invoke this target's function using it as input?
(DI ch6)

### Menu Bar `PTN-049`
A persistent horizontal menu bar (File/Edit/View-style) is the conventional place to expose an
application's complete action set, organized by category, and a guaranteed-discoverable
accessible fallback for screen readers and keyboard access keys. Exception: a trend toward
hiding the menu bar by default in favor of toolbars/ribbons/panels, available on demand.
(DI ch6)

### Popup/Context Menu `PTN-050`
Invoked by right-click or equivalent on a target, list only the actions relevant to that
target — not the full application catalog — and keep the list short. (DI ch6)

### Don't Repurpose a Dropdown-Select for Actions `PTN-051`
A dropdown/select is conventionally understood as choosing a value, not invoking an action;
reusing it to "select an action to run" breaks that contract. (See Form: Dropdown Chooser for
the legitimate value-selection role.) (DI ch6)

### Toolbar `PTN-052`
A compact row of usually-icon action buttons; works best when each action has a clear,
self-explanatory icon — an action that genuinely needs words should use a labeled control
instead of being forced into ambiguous icon form. (DI ch6)

### Link as a Lightweight Action Trigger `PTN-053`
Distinctively-colored, underlined-on-hover text is a well-established convention for a
low-emphasis action, avoiding a button's visual weight. Trade-off: because users learn colored/
underlined text means "clickable," that styling must then be avoided for any non-clickable
text elsewhere. (DI ch6)

### Double-Click Resolves to One Learned Meaning `PTN-054`
Double-click conventionally means "open this item" or "perform its default action" — not an
opportunity to invent a third meaning; on an object it commonly opens a property
sheet/editor, on text it commonly enters inline edit mode. Ask: does this object type have an
established open/default-action meaning elsewhere that double-click should match? (DI ch6)

### Keyboard Access Is a Required Path `PTN-055`
Every action reachable via pointer must also be reachable via keyboard (standard shortcuts,
menu access keys), following platform convention rather than inventing new ones — for users
who can't use a mouse, the keyboard path can be their only way to invoke the action at all.
Ask: can this action be invoked without a mouse, via a standard shortcut or access key? (DI ch6)

### Typed Commands (CLI) `PTN-056`
A command-line style interface offers free-form access to a system's entire action set with
high per-composition power, but is structurally poor at discovery — most CLIs don't make
available commands easy to find on their own. When: fits an efficiency layer for expert users
willing to learn a vocabulary; avoid as the primary interaction for casual/first-time users.
Trade-off: composability and power vs. near-zero discoverability without prior learning.
(DI ch6)

### Custom Controls Must Visually Afford Their Behavior `PTN-057`
Specialized/expert-facing apps have more freedom for non-standard controls, but every custom
control must still visually communicate that it's actionable and how (raised/3D look, borders,
cursor change, tooltip) or users won't discover it's interactive. Ask: does this element
visually signal, on its own, that it can be clicked/dragged/adjusted? (DI ch6)

### Button Groups `PTN-058`
Cluster related, same-scope actions into a small group of visually-unified buttons (same
border/size/icon style/hover), split into groups of ~2-5 rather than one long row; never mix
actions with different scopes/targets into one group. Exception: a single "primary" action may
deliberately break from shared styling to stand out (see Prominent "Done" Button). (DI ch6)

### Hover Tools `PTN-059`
Reveal per-item action controls only on pointer hover, hiding instantly on pointer leave with
no animated transition; currently poorly suited to touch, which has no free
hover-before-commit state. When: avoid as the sole action-access path when the primary input is
touch/touchpad. Exception: a persistent lightweight cue (grayed-out controls highlighted on
hover) is a middle-ground alternative when actions must stay discoverable without hover.
(DI ch6)

### Action Panels `PTN-060`
A persistently-visible, richly-laid-out panel of grouped actions for the current
item/selection, instead of hiding them behind a menu, popup, or hover reveal; lay out each
action strictly one-per-line for correct screen-reader readability. When: fits when the action
set is too large for Hover Tools or a short menu; avoid when screen space is very limited.
Trade-off: uses more space than a menu bar or hover-reveal in exchange for permanent visibility
and full layout freedom. (DI ch6)

### Label Form and Length `PTN-062`
An action's label may be text, icon, or both, chosen for what best communicates it, kept
consistent within a container; roomier containers can support longer, more descriptive labels
helping infrequent users, while dense/expert interfaces suit terser labels. Trade-off: longer
labels aid learnability/recall but add visual noise and space cost experienced users may not
need. (DI ch6)

### Prominent "Done" Button `PTN-063`
A large, clearly-labeled, visually-standout button at a task flow's endpoint so the user is
confident their action registered; prefer a task-specific verb ("Send," "Purchase") over
generic "Done" when it communicates the outcome more precisely, placed directly after the
flow's last field. Ask: would a task-specific verb communicate the outcome more precisely than
a generic "Done"? (DI ch6)

### Smart Menu Items `PTN-064`
Dynamically rewrite an action trigger's label to state precisely what will happen ("Close
[document name]," "Undo Delete Message"), generalizing to any UI verb element, not just menu
items; disable the action entirely when there's no valid target. Exception: for multi-object
selections, a generic plural-safe label is an accepted simplification over attempting per-item
precision. (DI ch6)

### Preview Before Committing `PTN-065`
Before a heavyweight or hard-to-predict action, show a preview/summary of the result, from
which the user can proceed, revise a prior step, or cancel without leaving the preview screen.
(DI ch6)

### Progress Indicator Paired with Cancelability `PTN-066`
For any operation expected to block the UI for ~2+ seconds or that runs in the background, show
progress (what's happening, fraction done, remaining time, how to cancel), with cancel placed
directly beside the indicator and taking effect instantly; first consider whether the operation
can simply be made fast enough that cancelability becomes less urgent. Ask: is the time
estimate accurate enough for a determinate progress bar, or should it be indeterminate? When
multiple parallel operations run, does one cancel control cancel everything, or does each need
its own? (DI ch6)

### Multi-Level Undo `PTN-067`
Let users reverse a sequence of past actions one at a time in reverse chronological order (and
redo forward) across a whole session — undo/redo the underlying transaction, not just its
visual reflection; exclude transient/cosmetic state (selection, scroll position) from the
stack, and exclude actions with real-world side effects (purchases, sent messages). Trade-off:
skipping this remains viable for repeated-task workflows — the user just re-executes manual
steps, costing time rather than engineering. (DI ch6)

### Command History `PTN-068`
Keep a visible, chronological record of executed actions — what, to what, when — independent
of whether they're individually undoable, so users can review, relocate, or re-invoke them;
summarize a bulk action on many objects as one history entry, and treat the display as
secondary/optional UI. (DI ch6)

### Macros `PTN-069`
Let users bundle a recorded/defined action sequence into one named, replayable higher-level
action, triggerable by command/button/drag-and-drop; support macros calling other macros,
persist them, and let behavior vary parametrically per invocation. Trade-off: a full scripting
language is extremely powerful but is a genuine security risk and can intimidate
non-programmer users, even though composing a macro is functionally programming. (DI ch6)

### Offload Sub-Tasks the System Handles Better `PTN-122`
Fast calculation, doing multiple things simultaneously, perfectly reliable recall, complex
pattern detection, and searching a large dataset are inherently cheaper for software than for
users — delegate a sub-task of this kind to the system rather than asking the user to perform
it manually. Ask: is this sub-task calculation, parallel tracking, exact recall, pattern
detection, or search over a large set — something the system is inherently better at? (MI ch3)
