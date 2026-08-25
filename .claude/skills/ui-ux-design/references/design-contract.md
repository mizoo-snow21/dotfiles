# design_contract — the handoff artifact to component-design

Produce this when (and only when) the task continues past screen design into component
architecture or implementation planning — a compound request ("design it AND componentize it"),
an explicit handoff, or a deliverable another agent/skill will consume. It is an internal
working artifact: emit it at the end of the design work, after the final critique passes; show
it to the user only if they ask for a spec. For a design that ends at a rendered screen, skip
this file entirely.
(skill-derived, V2. The fields are the decisions this skill's own workflow already made —
writing them down costs little and prevents the downstream skill from re-deciding or silently
overriding them.)

## Shape

```yaml
design_contract:
  user_goal:            # who the user is, what success means on this screen
  user_context:         # frequency, pressure, environment, expertise
  primary_tasks:        # ranked; the #1 task the layout is optimized for

  information_architecture:  # groups, hierarchy, and why (mechanism, not taste)

  primary_action:       # THE action; everything else is secondary by definition
  secondary_actions:    # with visibility decisions (persistent / on-demand / overflow)

  chosen_ui_patterns:   # named pattern per surface + the reason it beat the alternative

  interaction_requirements:  # triggers and what each control actually does (wired honesty list)
  feedback_requirements:     # what the user must always be able to tell, and how
  loading_states:       # designed, with trigger data
  empty_states:         # designed, with trigger data
  error_states:         # designed, with recovery path
  destructive_behaviors:     # guardrail per action, proportional to cost (undo > confirm where possible)

  visual_hierarchy:     # what wins the squint test and why
  information_density:  # density posture per region, on purpose
  responsive_requirements:   # breakpoints/behavior that must survive implementation
  accessibility_requirements: # floor: contrast, targets, color-independence, semantics, keyboard

  visual_direction:     # the chosen art direction: axes settings + token decisions
                        # (from references/art-direction.md), so implementation can't drift
                        # back to a generic default

  important_tradeoffs:  # each tension resolved, which side taken, why this context favors it

  component_candidates: # OPTIONAL hints only — component-design owns the actual boundaries;
                        # never present these as decided architecture
  decided_states:       # explicit list of states this design covers (lets downstream tell
                        # "not needed" from "not specified")
  visual_differentiation_intent: # pairs that look alike but ARE different / look different ON
                        # PURPOSE — protects deliberate design from convenience-driven merging
  open_gaps:            # what this design knowingly leaves undecided
```

## Handoff rule

When component architecture is next, hand this contract to component-design (its
references/handoff-contract.md consumes exactly these fields). Fields marked here as decided are
not up for architectural re-litigation; a downstream request to change one is a design-change
request, to be weighed here, not an "open question" to be absorbed silently.
