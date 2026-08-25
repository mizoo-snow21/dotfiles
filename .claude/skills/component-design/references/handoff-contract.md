# Handoff Contracts — design_contract in, component_contract out

Load at workflow step 0 (intake) whenever the input is a UI design — formal or informal — that
this skill must convert into architecture. Both contracts are internal working artifacts:
consume/produce them to structure the work, show them to the user only when asked.
(skill-derived, V2 — the contract fields answer ambiguities the V1 eval never exercised: every
V1 case supplied a spec-grade brief, while real handoffs supply a screenshot and a sentence.)

## Intake: the design_contract (produced by ui-ux-design, or reconstructed here)

If upstream provided a design_contract (see ui-ux-design/references/design-contract.md), start
from it. If not, reconstruct one from whatever was given — and mark every field you had to infer.
The distinction that matters is three-way, per field:

- **decided** — upstream chose this; architecture must honor it, not re-litigate it.
- **explicitly open** — upstream named it undecided; you may propose, flagged as a proposal.
- **unstated** — the input never mentions it. Treat as an open question to raise, NOT an
  assumption to invent silently. (This is the intake gate: unstated ≠ decided-by-you.)

Fields to check on intake (the five that remove the most ambiguity):
1. `decided_states` — which content/interaction states the design covers
   (empty/loading/error/permission variants). Lets you tell "not needed" from "not specified".
2. `pattern_selections` — which named UI pattern was already chosen per surface. Don't re-decide
   pattern choice under a different name.
3. `interaction_intent` — trigger/feedback semantics already fixed (save behavior, confirmations,
   exact copy where fixed) vs. left open.
4. `visual_differentiation_intent` — which look-alike or look-different pairs are INTENTIONAL.
   This field exists to stop architecture convenience from flattening deliberate design: if
   upstream says two blocks differ on purpose, "merge them, it's cheaper" is not an open
   question — it is a redesign request, and out of scope.
5. `open_upstream_gaps` — what upstream already knows is incomplete; confirm against this list
   instead of rediscovering it.

Honesty rule for open questions: an open question reports a defect or gap in the design. A
preference for a more architecturally convenient design is not a defect — if you catch yourself
phrasing "may we merge these" as a spec problem, stop; either honor the design or state plainly
that you are requesting a design change and why the change-cost math justifies asking.

## Output: the component_contract

The deliverable (SKILL.md "Deliverable shape") expressed as a structured skeleton. Fill what the
task needs; omit sections genuinely irrelevant. Reasoning stays attached to each decision.

```yaml
component_contract:
  components:            # inventory: name, semantic role, one-line boundary reasoning
  component_boundaries:  # the non-obvious split/merge calls + which test decided each
  shared_vs_local:       # per shared component: its ≥2 CURRENT consumers with identical contracts
  semantic_roles:        # role → component map (jobs, not rectangles)
  composition:           # what composes vs what configures; primitive/composite split
  variants:              # per component: variant axes with scope stated
  states:                # per component: the state TABLE (axis / shape / owner / transitions —
                         # see variants-states.md worked example); adjectives don't count
  behaviors:             # contracts: what must always / must never happen; disclosure
  accessibility_contracts: # semantics, keyboard, focus (incl. overlay stacking), state exposure
  responsive_behavior:   # same component adapting vs different structure, same contract
  token_requirements:    # which design tokens the components consume (names, not values)
  naming:                # names by purpose/action; naming difficulties flagged as boundary smells
  important_tradeoffs:   # each two-sided, with the side taken and why
  open_questions_upstream: # design defects/gaps only (see honesty rule above)
```

Change-cost review gate (run before promoting anything to `shared_vs_local`): number of current
consumers; semantic + behavioral + contract identity across them; likely future variation; blast
radius of a later change; API complexity added; local-override pressure expected. If projected
change-cost exceeds demonstrated reuse value, refusing the abstraction is a valid, stated
outcome (BND-011/012/013 own the underlying economics).
