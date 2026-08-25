---
name: component-design
description: Book-grounded component-architecture judgment — converts an already-decided UI/UX design (ideally ui-ux-design's design_contract output) into component boundaries, shared-vs-local decisions, composition, variants, states, behavior contracts, and accessibility contracts. Use this once a screen's content and look are already decided and the task is specifically about splitting a UI into components, refactoring into components, deciding what to extract or reuse ("should these be one component?", "should we merge these two components?", "コンポーネント分割", "共通化すべき?"), designing or auditing a component library / design system structure, defining a component's states/variants/API at concept level, or reviewing an existing component architecture — even if the user just says "componentize this screen", "make this reusable", or asks for a component inventory. Do NOT use it for choosing what a screen should contain or how it should look, or for a request that is mostly a content/visual decision wearing "component" language (that is ui-ux-design's job — load it first if that hasn't happened); not for making a CSS value reusable as a token/variable; and not for writing framework code.
---

# Component Design

Convert a decided interface design into **component architecture**: where boundaries go, what
is shared, how parts compose, what each component's variants, states, behavior, and
accessibility contracts are, and how the whole stays consistent as a system.

The goal is not producing many components. It is producing **correct boundaries**: an
architecture a team can change later without regret. An eloquent rationale wrapped around a
wrong boundary is a failure; a plain rationale on a right boundary is success.

## Scope

- **Upstream (not yours):** user goals, IA, navigation strategy, UI pattern *selection*,
  visual hierarchy, interaction design intent, visual styling — ui-ux-design's territory.
  If the given design has a genuine defect or gap, flag it as an open question back to the
  designer; a preference for an architecturally cheaper design is NOT a defect (see
  references/handoff-contract.md's honesty rule) — do not redesign the UI.
- **Yours:** component boundary, shared vs local, composition, component contract (variants /
  states / behavior / accessibility), reusable architecture, system consistency.
- **Downstream (not yours):** framework code and APIs. Express behavior as contracts
  ("closing the dialog returns focus to its trigger"), never as implementation ("use Radix
  Dialog.Root"). ARIA and semantic HTML ARE in scope — they are the neutral,
  framework-independent accessibility contract language; React/Vue/Svelte/Tailwind/shadcn/
  Radix/React-Aria specifics are not, even when the user's stack is known.

## Source integrity (V2)

Every substantive judgment in `references/` is distilled from five purchased books (Atomic
Design; Design Systems; Inclusive Components; Designing Interfaces 2e; Microinteractions) —
provenance tags like `(IC ch12)` appear on each entry. V2 additions are explicitly tagged
`product-derived V2` (e.g. the WAI-ARIA APG overlay-stacking rules) or `skill-derived`
(workflow/contract mechanics) — never silently mixed into book provenance. When a question
falls outside the base (async/data lifecycle, token architecture, virtualization, i18n beyond
labeling — the build's gap list), say so and reason transparently instead of substituting
generic frontend lore as if it carried the same authority.

## The core question

Before unifying anything, ask:

> **Moved to a different context, is this still explainably the same concept?**

Identity lives in *purpose and behavioral contract*, not visual form. Two blocks that look
identical but differ in what they mean, how they behave, or what state they carry are
different components that may share visual primitives. Two controls that look nothing alike
but make the same kind of choice under the same contract may be one concept. "Looks similar"
is a hypothesis to test, never a conclusion. (references/boundaries.md owns this test.)

## Workflow

Size the pass to the task first: for a single new variant/state on an already-architected
system, steps 1–4 and 9 typically collapse to one sentence each — spend the effort on steps
5–8 instead. A from-scratch architecture walks all steps. Read a reference file when its
decisions are on the table.

0. **Intake gate** → `references/handoff-contract.md`. If a design_contract exists, start
   from it; otherwise reconstruct one from the given input, classifying every field as
   decided / explicitly open / unstated. Unstated items become open questions to raise —
   never assumptions to invent silently. Check `visual_differentiation_intent` before any
   merge proposal.
1. **Inventory semantic roles.** List the jobs the interface does (actions, choices, inputs,
   displays, containers, feedback), not the rectangles it shows.
2. **Draw candidate boundaries** → `references/boundaries.md`. Apply the core question to
   every "these look alike" pair. Diagnose near-duplicates before unifying.
3. **Shared vs local** → boundaries.md. Don't promote to shared before a second independent
   need exists; don't bend a general pattern to fit a special case — quarantine it. A shared
   *interaction shape* ("both open a list and pick one") is the same trap as shared looks:
   unify only when the FULL contract matches — if one consumer needs even one flag the others
   don't, keep separate components (or a shared behavior definition under distinct
   components) instead of one configurable panel. Run the change-cost review
   (handoff-contract.md) on every promotion candidate; refusing an abstraction is a valid,
   stated outcome.
4. **Composition** → `references/composition.md`. Primitive/composite split, what composes
   vs what configures, context-independence of anything reusable.
5. **Variants** → `references/variants-states.md`. A variant is a modified expression of the
   same concept with its scope stated explicitly; if the "variant" changes the concept, it's
   a different component.
6. **States** → variants-states.md — start from its worked state-table example: per state
   axis, write concrete shape (values, not adjectives), ONE owner (derived state reads from
   it, never duplicates it), and every transition with its trigger. All change paths listed.
7. **Behavior** → `references/behavior.md`. Triggers, rules, feedback, loops — as contracts:
   what must always happen, what must never happen, what gets disclosed.
8. **Accessibility contract** → `references/a11y-semantics.md` (structure, labeling, state
   communication, live regions) and `references/a11y-interaction.md` (keyboard, focus,
   overlay stacking/scroll-lock, multimodal, progressive enhancement). Part of each
   component's contract, written with it — not a checklist run afterwards.
9. **Pattern grounding** → `references/patterns.md` (index + meta-principle), then ONLY the
   family file in play: patterns-navigation / patterns-layout / patterns-lists /
   patterns-actions / patterns-data-display / patterns-forms / patterns-overlays-feedback /
   patterns-mobile. Selection frameworks first, then the catalog entry.
10. **Responsive behavior.** Decide per component whether narrow viewports get the same
    component adapting or a genuinely different structure with the same contract
    (patterns-mobile.md; boundaries.md identity test).
11. **Naming** → `references/naming-shared-language.md`. Name by purpose/action, not visual
    form. If a component resists naming, treat that as a boundary smell, not a wording chore.
12. **System consistency** → `references/consistency-mechanisms.md` (same interaction states
    defined once — with the guard: only where genuinely the same kind of state change;
    intentional variation stays intact). Documentation/governance decisions →
    `references/docs-governance.md`. System-wide design-language questions →
    `references/perceptual-system.md` (overlaps ui-ux-design's territory; load only when the
    design language itself is the task).
13. **Conceptual API complexity.** Count what a consumer must know. Every option, slot, and
    warning is cost — justify each against a real, existing need.
14. **Name the trade-offs.** Where the references hold a two-sided trade-off (strict/loose,
    modular/integrated, generic/specific, composition/configuration), say which side this
    product takes *and why* — never pretend the trade-off doesn't exist.
15. **Final critique** (below), then write the deliverable.

## Deliverable shape

The component_contract skeleton in `references/handoff-contract.md`: component inventory with
boundary reasoning; shared-vs-local decisions with named current consumers; composition
structure; per-component contract (variants, state table, behavior, accessibility); naming;
explicitly-taken trade-offs; open questions back to the UI designer (defects only). Reasoning
stays attached to decisions — a bare component list is not architecture.

## Final critique — architecture is the source of truth

Before delivering, attack your own output:

- Would each shared component survive the core question in every context it serves?
- What did you unify that you shouldn't have? What did you split that shares one contract?
  (Check both directions.) Did any merge flatten a difference the design_contract marked as
  intentional?
- Is any component accumulating jobs (a "mini web page")? Any abstraction with exactly one
  real consumer? Any configuration option without a current need?
- Do look-alike controls behave identically everywhere, and different-looking controls with
  one contract share one definition?
- Is every state reachable, communicated (visually AND to assistive tech), and owned by
  exactly one source of truth? Grep your own document for each state you named: does any
  section assign it a different owner or behavior than another section? (Self-contradiction
  between sections is the most common state defect.)
- Same sweep for behavior contracts: for each interaction you specified in two places (a
  component section and a flow/summary section), do both state the same trigger → outcome?
- For every shared component: name its ≥2 CURRENT consumers and confirm their contracts are
  identical — not merely their interaction shape. One divergent requirement means split, or
  share a behavior contract under separate components.
- Does every overlay/disclosure component say where focus goes on open and close — and for
  stacked overlays, which shared effects are ref-counted (AXK-046)?
- If the visual design changes next quarter, which of your boundaries break? If that answer
  is "many", the boundaries are drawn on looks, not meaning.
- Did the component count grow because the architecture needed it — or because splitting felt
  productive? More components is not a better score.
