# Anti-Generic Reasoning — detecting unjustified familiar defaults

Load during the visual layer and during the final critique. This file does NOT ban anything:
cards, rounded corners, gradients, badges, shadows, and borders are all correct in the right
context. Its job is to catch the *unjustified familiar default* — the construct that is present
because it is what generated UI looks like, not because this product's problem asked for it.

Provenance: the failure evidence is measured, not aesthetic opinion (skill-derived V2, from the
15-case blind benchmark and V1 CSS audit); the counter-moves are book-derived where tagged.

## The measured default recipe (what "generic" concretely is)

Audited across 60 independently-generated screens for 15 different products, near-every output
converged on ONE recipe regardless of product identity: a 9–11-step blue-grey neutral scale
(hue ≈210–225°), a single blue/indigo primary (#4f46e5-family), border-radius 4–12px scale,
soft low-opacity shadows, identical system font stack, white cards on a grey page. Blind judges
scored distinctiveness ~3.0/5 flat for every arm. The recipe is not wrong — it is competent —
but when every product gets it, no product's context is being read. Treat any output matching
the full recipe as a prompt to run the questions below, not as an automatic failure.

## Genericness review questions (ask of every major visual construct)

- Why does this need a container? What does the box group that proximity + a heading could not?
  ⟨rui grouping-via-spacing rules — visual-hierarchy-layout.md⟩
- Why does this need a border? Is it separating anything, or is it the third nested outline?
- Why is this a card? Would removal flatten the hierarchy or clarify it?
- Why is it rounded exactly this much everywhere? Geometry is an identity decision
  (art-direction.md), not a default.
- Why does this need an icon? What does it disambiguate ⟨laws1-029⟩ — or is it decoration
  occupying signal space?
- Why is this visually emphasized? What task evidence says the user needs it first?
- Why is this action always visible? Frequency data or habit?
- Why is spacing uniform? Uniform rhythm reads as "nothing is more related than anything else"
  — proximity should encode meaning ⟨grouping rules⟩.
- Would removing this element improve the squint test?
- Is this solving THIS product's problem, or reproducing a familiar SaaS convention? Convention
  is a legitimate answer when users' mental models expect it ⟨jakob's-law / learn-d01⟩ — "it's
  conventional AND this user expects it here" passes; "it's what dashboards look like" fails.

## Measured generic failure modes (tag names match the benchmark taxonomy)

Evidence base: these were the judges' most frequent complaints across all arms.
- **excessive-containers**: nested boxes that group nothing (a card inside a panel inside a
  section, each with border+radius+shadow). Fix: one grouping device per level — space first,
  then a heading, a border only when scanning across many columns of unrelated data needs it.
- **excessive-uniformity / visual-monotony**: every region same visual weight, same row rhythm,
  same card size — the screen has no reading order. Fix: hierarchy first (what wins the squint
  test), then let importance change size/weight/density — not just position.
- **generic-saas-composition**: hero-stat-row + card-grid + table, applied to every product.
  Fix: compose from the user's #1 task, not from the genre template (a triage tool leads with
  the queue; a monitoring tool leads with what changed).
- **unnecessary-decoration**: gradients/badges/avatar-stacks/icon rows with no informational
  job. Fix: every decorative element must either carry information or belong to the declared
  art direction's ONE signature device (art-direction.md) — never both absent.
- **weak-typography**: hierarchy carried only by font-size steps of the same neutral face.
  Fix: typography character is an art-direction axis; weight/case/spacing/family contrast can
  carry identity without new colors.
- **safe-but-characterless**: no individual flaw, no point of view. This is the recipe above.
  Fix: art-direction.md — commit to one direction and let it show in the tokens.

## The counterweight rule (why books alone didn't prevent this)

The corpus's restraint rules (restrained palettes ⟨rui1-053/054⟩, functional minimalism
⟨laws1-046/047/049⟩) are correct but one-sided: followed without a differentiation step they
reproduce the default recipe — measured, not hypothesized. Their counterweight is book-derived
too: **brand personality via coordinated levers** ⟨di4-041/044/049/060⟩ — font geometry, color
saturation/hue, border weight, corner geometry, density, motion — chosen together to express
ONE personality. V2 makes that counterweight operational: the art-direction pass
(art-direction.md) is a required stage of the visual layer, not an optional flourish. Restraint
shapes the system; direction gives it identity; neither substitutes for the other.
