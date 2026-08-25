# Art Direction — choosing a visual point of view before polishing one

Load at the START of the visual layer (workflow step 5), before any token values are chosen.
Purpose: replace "accept the first plausible visual system" with a deliberate, context-fitted
direction. Measured motivation: without this pass, independently-generated screens for 15
different products converged on one identical recipe and scored ~3.0/5 distinctiveness
(anti-generic.md documents it). The fix is not decoration — it is choosing.

Book grounding: brand personality is expressed through coordinated levers — typeface geometry,
color hue/saturation, corner geometry, border weight, density, motion — working as one system
⟨di4-041, di4-044, di4-049, di4-060⟩; aesthetic-usability works through functional coherence,
not ornament ⟨laws1-046..049⟩. Product evidence: see contemporary/navigation-visual-language.md
— real products commit to genuinely different poles of these axes and stay coherent.

## When to run which depth

- Visual direction already given (brand guide, existing product, design system): honor it;
  skip exploration; still run the coherence check below.
- Green-field or unstated: run the full pass — typically ~3 candidate directions, internally.
  Do not show the user three designs; explore, choose, then present the chosen one with its
  reasoning. A line in DESIGN-NOTES ("direction chosen: X over Y because context Z") is enough.

## The axes (explore across several — a direction is a COMBINATION, not a color swap)

| Axis | Poles (not exhaustive) | What it must answer |
|---|---|---|
| Character | quiet / editorial / technical / precise / expressive / playful / utilitarian | What should using this feel like, given user + stakes? |
| Typography character | neutral system / technical-mono-influenced / editorial serif-accented / expressive display | Who is speaking? |
| Density posture | low / medium / high | Daily-use professional tool vs occasional consumer flow ⟨learn-d02⟩ |
| Geometry | sharp / restrained rounding / soft | Precision vs approachability |
| Surface strategy | flat+borders / tonal layers / elevation+shadows | How does structure read? (pick ONE primary device) |
| Color strategy | neutral-dominant + 1 deliberate accent / brand-saturated / dark-first / warm vs cool neutrals | Hue family is a DECISION — "SaaS indigo" only survives if chosen on purpose |
| Spacing rhythm | tight-regular / generous-even / contrast-heavy (dense clusters + emphatic gaps) | What does proximity encode here? |
| Motion character | none / restrained-functional / springy | Matches Character axis |
| Signature device | ONE memorable functional element (distinctive nav treatment, a chart style, a status language, an emphatic type moment) | The thing a user could describe from memory — functional, singular |

These are exploration axes, not presets. Never pick by novelty: three candidates should differ
on several axes each, and each candidate must be ARGUABLE from context.

## Choosing (context beats flash — §23 of the V2 spec, and the benchmark agrees)

Score candidates against: user type & expertise; task frequency & duration (a tool lived in for
hours earns density + quiet character; an occasional consumer flow earns warmth + guidance);
product category conventions ⟨jakob's-law / learn-d01 — deviation needs a reason users benefit
from⟩; trust requirements (fintech/health: precision, restraint, no playfulness near money or
irreversibility); information density needs; brand context given. The most appropriate
direction wins, NOT the most distinctive. Distinctiveness is the byproduct of committing to a
real direction; it is never the goal. Benchmark evidence both ways: a warm, rounded, personable
direction won the consumer-events case against three neutral competitors, and a dark
developer-tool direction won the RBAC case — but ONLY because each fit its context; the same
moves on an enterprise credentialing form would have lost.

## Coherence check (what makes it read as ONE system)

- Every axis decision points at the same Character word. A "precise/technical" direction with
  soft 16px corners and springy motion is three directions, not one.
- The direction survives the accessibility floor untouched: contrast, target sizes,
  color-independence are non-negotiable regardless of direction.
- The signature device is singular and functional. Two signature devices = decoration.
- Tokens carry the direction: hue family, radius scale, spacing scale, type scale all derive
  from the chosen direction — if swapping your tokens into the measured default recipe
  (anti-generic.md) changes nothing visible, no direction was actually chosen.
- Density/whitespace decisions still resolve per region through vh-d02 (deliberate density) —
  direction sets the posture, task evidence sets each region.
- State the direction in one sentence in DESIGN-NOTES. If it can't be said in a sentence, it
  won't survive implementation.
