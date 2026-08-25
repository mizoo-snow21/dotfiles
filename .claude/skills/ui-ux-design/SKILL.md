---
name: ui-ux-design
description: Book-grounded UI/UX design judgment for designing or reviewing any user interface — web apps, SaaS products, admin panels, dashboards, mobile UIs, settings screens, forms, onboarding flows, search/filter UIs, tables, information architecture, wireframes, and landing pages. Use this whenever the task involves deciding what a screen should contain, how it should be structured, which UI pattern to use, how it should look (layout, spacing, typography, color, depth, visual direction), how interactions and feedback should behave, or critiquing/redesigning an existing UI ("this feels cluttered", "review my UI", "does this design look right?") — even if the user just says "make a page/screen/dashboard/form" or "improve this UI". May render the decided screen as working HTML/CSS/React, but does not define component boundaries, shared-vs-local architecture, or variant/state/behavior contracts (component-design owns that — hand off once the screen's content and look are decided), and pure framework refactors with no design decision need neither. Also use it when explaining WHY a design decision is right or wrong.
---

# UI/UX Design

## Mission

Make UI design decisions and be able to defend them. The foundation is distilled from 7
purchased books (Laws of UX, 100 Things Every Designer Needs to Know About People,
Information Architecture 4e, 101 UX Principles, Microinteractions, Designing Interfaces 2e,
Refactoring UI) — provenance tags like `⟨laws1-012⟩` link each rule to its source
(references/source-map.md). V2 adds clearly-separated layers: `references/contemporary/`
(product-derived — cited public design-system practice) and art-direction/anti-generic
reasoning (grounded in measured eval evidence). Layers never masquerade as each other.

The measure of success is **the rendered UI itself** — its usability, hierarchy, and craft —
not the sophistication of the explanation. And measured V1 evidence adds a sharper corollary:
**a control that renders but does not work is worse than a plainer screen that works.**
Design ambition must never outrun wiring-and-verification budget.

## Scope & neighbors

Owns: UX reasoning, IA, navigation, pattern selection, interaction & feedback, error
prevention/recovery, cognitive load, visual hierarchy, density, layout, spacing, typography,
color, depth, art direction, visual craft, usability, UI-level accessibility.

Not owned — and who is: component boundaries/variants/state architecture → **component-design**
(hand it the design_contract; its architecture never overrides decisions made here). Chart
type/marks/color per chart → **dataviz** (this skill owns the screen structure around charts).
Apple-platform conventions → **apple-hig** leads, this skill contributes the UX reasoning.
Animation implementation/performance → animation skills (this skill decides what feedback
exists and what it must communicate). Driving a live browser to verify a running app →
webapp-testing. Framework refactors with no design decision → none of these.

## Workflow

Work through these stages internally — don't recite them; let them shape the artifact.

1. **Understand** — Who is the user? What are they trying to achieve, how often, under what
   pressure? What does failure cost? Note the context factors art direction will need
   (frequency, duration, trust stakes, category). If unstated, infer the probable answer and
   record the assumption.
2. **Structure** — Organize information before drawing: primary vs secondary, groupings,
   hierarchy of user needs (`references/ia-navigation-content.md`,
   `references/cognition-mental-models.md`).
3. **Select patterns** — from evidence, not habit (`references/patterns-structure-data.md`;
   forms → `references/forms-input.md`; current cross-product practice →
   the matching `references/contemporary/` file). **Renderability rule:** if the deliverable
   is judged from static output, every required state must be visible in the page or
   reachable through interaction that actually works — decide HOW each state will be shown
   now, not after the visual layer.
4. **Design interaction** — triggers, feedback, loading, errors, undo, destructive guardrails
   (`references/interaction-feedback.md`). **Close with the wiring commitment:** list every
   control that will render as interactive and what each one actually does. Anything you
   cannot commit to wiring gets simplified to a native element, visibly disabled, or cut —
   BEFORE the visual layer spends budget on it. ⟨mi1-012/013⟩
5. **Art direction, then the visual layer** — choose a visual point of view from context
   (`references/art-direction.md` — required for green-field work, honor existing brand
   otherwise), then execute: hierarchy first, spacing second, type/color/depth third
   (`references/visual-hierarchy-layout.md`, `references/typography-color-depth.md`).
   Labels/search wording → `references/labeling-search.md`.
6. **Resolve tensions deliberately** — the moment two valid principles collide, open
   `references/tradeoffs-decision-points.md` and walk the decision questions. Never resolve a
   tension silently.
7. **Verify wiring & states** — walk the step-4 commitment list against the artifact: every
   control does what it signals; every required state renders. If a browser/parser is
   available, actually run it. This pass happens BEFORE the critique, while budget remains.
   Two measured recurring defects to check explicitly: (a) a CSS rule like
   `.x{display:flex}` silently defeats the `hidden` attribute — add
   `[hidden]{display:none!important}` or verify every hidden state actually hides;
   (b) muted/tertiary text tokens shipping below 4.5:1 — compute the contrast, don't eyeball.
8. **Final critique** — run the critique below; fix what it catches. When subagents are
   available and the deliverable matters, have an independent critic judge the ARTIFACT
   before reading your rationale (a weak UI must not be rescued by a good explanation).
   Critique-driven changes are targeted fixes, not a redesign.
9. **Handoff** — if the task continues into component architecture or implementation
   planning, emit the design_contract (`references/design-contract.md`) and hand to
   component-design.

Reading budget (measured, not aspirational): build tasks load 2–4 references; loading more
breadth than that correlated with LESS working output in eval, not more. Critique/redesign
tasks: run the critique list first, then load only the 2–4 files the found problems belong
to. `contemporary/` files are per-domain — load at most the one matching the screen type.

## Reference routing

| Question you're answering | Load |
|---|---|
| How many options/fields, defaults, disclosure, memory limits | cognition-mental-models.md |
| Organizing/navigating content; hierarchy shape; menus, entry points | ia-navigation-content.md |
| What to call things; search box/results/filters wording | labeling-search.md |
| Which screen/list/table/dashboard pattern fits | patterns-structure-data.md |
| Form structure, controls, validation, touch input | forms-input.md |
| Feedback, loading, errors, undo, destructive actions (consolidated block) | interaction-feedback.md |
| Emphasis, grouping, layout, spacing, density | visual-hierarchy-layout.md |
| Type scale, color system, contrast, borders vs shadows | typography-color-depth.md |
| Motivation, progress, social proof, trust, dark-pattern boundaries | behavior-motivation-ethics.md |
| Choosing a visual direction; breaking the default recipe | art-direction.md |
| "Why is this a card/border/icon?" — genericness questions | anti-generic.md |
| Current product practice: tables/lists | contemporary/data-tables.md |
| Current product practice: settings, forms, billing | contemporary/settings-forms.md |
| Current product practice: search, filters, command, empty/loading/error | contemporary/search-command-states.md |
| Current product practice: navigation shells, visual-language axes | contemporary/navigation-visual-language.md |
| Two principles conflict | tradeoffs-decision-points.md |
| Handoff to component architecture | design-contract.md |
| Where did this rule come from | source-map.md |

## Reasoning quality bar

Never justify a decision with only: 見やすい / 使いやすい / modern / clean / simple /
professional / "best practice". Name the mechanism: cognitive load, decision cost, mental
model, information scent, recognition vs recall, hierarchy, proximity/grouping, contrast,
visual weight, feedback, mapping, discoverability, error prevention, task frequency. One
named mechanism per decision is enough — the right decision matters more than deep prose.
When principles conflict, say which side you took and why this context favors it. When you
deviate from a rule here, say so — deviation is allowed, silence about it is not.

## Final critique (run before delivering any UI)

- **Task fit**: Can the target user complete their most frequent task fastest? Anything
  serving the business against the user? Remove it.
- **Hierarchy**: Squint test — does the most important element win? Is everything emphasized
  (= nothing is)?
- **Structure**: Do groupings follow meaning? Is location and next step always evident?
- **Density**: Every dense area dense on purpose, every sparse area sparse on purpose?
- **States**: Empty, loading, error, long-content, destructive-confirmation designed AND
  rendered/reachable — verified in step 7, spot-check again here.
- **Wired honesty**: step 7 confirmed every control does what it signals ⟨mi1-012/013⟩ — if
  step 7 was skipped, stop and do it now; a decorative control fails the deliverable.
- **Errors**: prevented where possible, recoverable in place where not; irreversibility
  guarded proportionally to cost (undo beats confirmation ⟨di1-015⟩).
- **Words**: Would the target user use these labels? Jargon the user-warrant rules reject?
- **Accessibility floor**: contrast, touch targets, color-independent meaning, semantic
  headings, keyboard reachability.
- **Genericness**: run anti-generic.md's questions on every major container/border/icon/
  emphasis. Does the screen have the declared art direction, or the default recipe?
- **Honesty**: for any element a reviewer might question, you have a grounded answer — book
  rule, cited product practice, or a flagged judgment call. Never a fabricated source.
