---
name: component-design
description: Book-grounded component-architecture judgment — converts an already-decided UI/UX design into component boundaries, shared-vs-local decisions, composition, variants, states, behavior contracts, and accessibility contracts. Use this whenever a task involves splitting a UI into components, deciding what to extract or reuse ("should these be one component?", "コンポーネント分割", "共通化すべき?"), designing a component library or design system structure, defining a component's states/variants/API at concept level, or reviewing an existing component architecture — even if the user just says "componentize this screen", "make this reusable", or asks for a component inventory. Do NOT use it for choosing what the screen contains or how it looks (that is ui-ux-design's job), nor for writing framework code.
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
  visual hierarchy, interaction design intent, visual styling. If the given UI spec has a
  problem, flag it as an open question back to the UI designer — do not redesign the UI.
- **Yours:** component boundary, shared vs local, composition, component contract (variants /
  states / behavior / accessibility), reusable architecture, system consistency.
- **Downstream (not yours):** framework code and APIs. Express behavior as contracts
  ("closing the dialog returns focus to its trigger"), never as implementation ("use Radix
  Dialog.Root"). React/Vue/Svelte/Tailwind/shadcn/Radix/React-Aria specifics are out of scope
  even if the user's stack is known — the architecture must stand without them.

## Source integrity (V1)

Every substantive judgment in `references/` is distilled from five purchased books (Atomic
Design; Design Systems; Inclusive Components; Designing Interfaces 2e; Microinteractions) —
provenance tags like `(IC ch12)` appear on each entry. When a question falls outside that
base (async/data lifecycle, token architecture, virtualization, i18n beyond labeling — the
build's gap list), say the source base doesn't cover it and reason transparently, instead of
silently substituting generic frontend lore as if it carried the same authority.

## The core question

Before unifying anything, ask:

> **Moved to a different context, is this still explainably the same concept?**

Identity lives in *purpose and behavioral contract*, not visual form. Two blocks that look
identical but differ in what they mean, how they behave, or what state they carry are
different components that may share visual primitives. Two controls that look nothing alike
but make the same kind of choice under the same contract may be one concept. "Looks similar"
is a hypothesis to test, never a conclusion. (references/boundaries.md owns this test.)

## Workflow

Work through these in order, skipping steps genuinely irrelevant to the task. Read a
reference file when its decisions are on the table — routing below.

1. **Inventory semantic roles.** List the jobs the interface does (actions, choices, inputs,
   displays, containers, feedback), not the rectangles it shows.
2. **Draw candidate boundaries** → `references/boundaries.md`. Apply the core question to
   every "these look alike" pair. Diagnose near-duplicates before unifying.
3. **Shared vs local** → boundaries.md. Don't promote to shared before a second independent
   need exists; don't bend a general pattern to fit a special case — quarantine it. A shared
   *interaction shape* ("both open a list and pick one") is the same trap as shared looks:
   unify only when the FULL contract matches — if one consumer needs even one flag the others
   don't, keep separate components (or a shared behavior definition under distinct
   components) instead of one configurable panel.
4. **Composition** → `references/composition.md`. Primitive/composite split, what composes
   vs what configures, context-independence of anything reusable.
5. **Variants** → `references/variants-states.md`. A variant is a modified expression of the
   same concept with its scope stated explicitly; if the "variant" changes the concept, it's
   a different component.
6. **States** → variants-states.md. Model each component's state space: interaction states,
   content states (empty/loading/error), modes (minimize; signify), persistence. Give every
   piece of state exactly ONE owner (single source of truth — derived state reads from it,
   never duplicates it), write the state's concrete shape (values, not adjectives), and state
   where each transition is triggered from.
7. **Behavior** → `references/behavior.md`. Triggers, rules, feedback, loops — as contracts:
   what must always happen, what must never happen, what gets disclosed.
8. **Accessibility contract** → `references/a11y-semantics.md` (structure, labeling, state
   communication, live regions) and `references/a11y-interaction.md` (keyboard, focus,
   multimodal, progressive enhancement). These are part of each component's contract, written
   with it — not a checklist run afterwards.
9. **Pattern grounding** → `references/patterns.md` when a component family (table, list,
   form control, overlay, navigation, feedback) is in play — selection frameworks first,
   then the catalog entry.
10. **Responsive behavior.** Decide per component whether narrow viewports get the same
    component adapting or a genuinely different structure with the same contract
    (patterns.md mobile section; boundaries.md identity test).
11. **Naming** → `references/system-consistency.md`. Name by purpose/action, not visual
    form. If a component resists naming, treat that as a boundary smell, not a wording chore.
12. **System consistency** → system-consistency.md. Same interaction states defined once;
    perceptual patterns coherent; documentation as part of the component.
13. **Conceptual API complexity.** Count what a consumer must know. Every option, slot, and
    warning is cost — justify each against a real, existing need.
14. **Name the trade-offs.** Where the references hold a two-sided trade-off (strict/loose,
    modular/integrated, generic/specific, composition/configuration), say which side this
    product takes *and why* — never pretend the trade-off doesn't exist.
15. **Final critique** (below), then write the deliverable.

## Deliverable shape

A component architecture document containing: component inventory with boundary reasoning;
shared-vs-local decisions; composition structure; per-component contract (variants, states,
behavior, accessibility); naming; explicitly-taken trade-offs; open questions back to the UI
designer. Reasoning stays attached to decisions — a bare component list is not architecture.

## Final critique — architecture is the source of truth

Before delivering, attack your own output:

- Would each shared component survive the core question in every context it serves?
- What did you unify that you shouldn't have? What did you split that shares one contract?
  (Check both directions.)
- Is any component accumulating jobs (a "mini web page")? Any abstraction with exactly one
  real consumer? Any configuration option without a current need?
- Do look-alike controls behave identically everywhere, and different-looking controls with
  one contract share one definition?
- Is every state reachable, communicated (visually AND to assistive tech), and owned by
  exactly one source of truth? Grep your own document for each state you named: does any
  section assign it a different owner or behavior than another section? (Self-contradiction
  between sections is the most common state defect.)
- For every shared component: name its ≥2 CURRENT consumers and confirm their contracts are
  identical — not merely their interaction shape. One divergent requirement means split, or
  share a behavior contract under separate components.
- Does every overlay/disclosure component say where focus goes on open and close?
- If the visual design changes next quarter, which of your boundaries break? If that answer
  is "many", the boundaries are drawn on looks, not meaning.
- Did the component count grow because the architecture needed it — or because splitting felt
  productive? More components is not a better score.
