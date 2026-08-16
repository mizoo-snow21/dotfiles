---
name: ui-ux-design
description: Book-grounded UI/UX design judgment for designing or reviewing any user interface — web apps, SaaS products, admin panels, dashboards, mobile UIs, settings screens, forms, onboarding flows, search/filter UIs, tables, and landing pages. Use this whenever the task involves deciding what a screen should contain, how it should be structured, which UI pattern to use, how it should look (layout, spacing, typography, color, depth), how interactions and feedback should behave, or critiquing/redesigning an existing UI — even if the user just says "make a page/screen/dashboard/form", "improve this UI", "does this design look right?", or asks for HTML/CSS/React that renders a user interface. Also use it when explaining WHY a design decision is right or wrong.
---

# UI/UX Design

## Mission

Make UI design decisions and be able to defend them. Every substantive rule in this skill is distilled from 7 purchased books (Laws of UX, 100 Things Every Designer Needs to Know About People, Information Architecture 4e, 101 UX Principles, Microinteractions, Designing Interfaces 2e, Refactoring UI) — provenance tags like `⟨laws1-012⟩` link each rule to its source (see references/source-map.md). Do not dilute these rules with generic design taste.

The measure of success is **the rendered UI itself** — its usability, hierarchy, and craft — not the sophistication of the explanation. Reasoning exists to produce a better screen, not to decorate a mediocre one.

## Scope

This skill owns: UX reasoning, information architecture, navigation, UI pattern selection, interaction & feedback, error prevention/recovery, cognitive load, visual hierarchy, information density, layout, spacing, typography, color, depth, visual craft, usability, UI-level accessibility.

It does NOT own: React component APIs, component architecture/abstraction, Tailwind/shadcn/Radix conventions, or framework-specific implementation. Design the screen here; implement it with whatever stack the task dictates.

## Workflow

Work through these stages internally — don't recite them to the user; let them shape the artifact.

1. **Understand** — Who is the user? What are they trying to achieve on this screen, how often, under what pressure? What's their mental model? What does failure cost them? If the prompt doesn't say, infer the most probable answer and state the assumption in your design notes.
2. **Structure** — Organize the information before drawing anything: what's primary vs secondary, what gets grouped, what's the hierarchy of user needs. Load `references/ia-navigation-content.md` for organization/navigation decisions and `references/cognition-mental-models.md` for how much users can hold, defaults, and disclosure.
3. **Select patterns** — Choose the screen's structural pattern and its component patterns from evidence, not habit (`references/patterns-structure-data.md`; forms → `references/forms-input.md`).
4. **Design interaction** — Triggers, feedback, loading, errors, undo, destructive-action guardrails (`references/interaction-feedback.md`; motivation/ethics → `references/behavior-motivation-ethics.md`).
5. **Design the visual layer** — Hierarchy first, then spacing, then type/color/depth (`references/visual-hierarchy-layout.md`, `references/typography-color-depth.md`). Wording of labels and search behavior → `references/labeling-search.md`.
6. **Resolve tensions deliberately** — the moment two valid principles collide (density vs whitespace, hide vs show, convention vs novelty…), open `references/tradeoffs-decision-points.md` and walk the decision questions. Never resolve a tension silently.
7. **Final critique** — before delivering, run the critique below and fix what it catches.

Typical loads per task: 2–4 reference files. A settings screen → cognition + forms + interaction (+ tradeoffs). A dashboard → patterns + visual-hierarchy + typography (+ tradeoffs). A search UI → labeling-search + patterns + cognition. A redesign/critique → start from the critique list, then load whichever files the found problems belong to.

## Reference routing

| Question you're answering | Load |
|---|---|
| How many options/fields to show, defaults, disclosure, memory limits, conventions | cognition-mental-models.md |
| How to organize/navigate content; hierarchy shape; menus, breadcrumbs, entry points | ia-navigation-content.md |
| What to call things; microcopy at IA level; search box/results/filters | labeling-search.md |
| Which screen/list/table/dashboard pattern fits | patterns-structure-data.md |
| Form structure, controls, validation, touch input | forms-input.md |
| Feedback, loading, errors, undo, modes, animation, action buttons | interaction-feedback.md |
| Emphasis, grouping, layout, spacing, density | visual-hierarchy-layout.md |
| Type scale, color system, contrast, borders vs shadows, polish | typography-color-depth.md |
| Motivation, progress, social proof, trust, dark-pattern boundaries | behavior-motivation-ethics.md |
| Two principles conflict | tradeoffs-decision-points.md |
| Where did this rule come from | source-map.md |

## Reasoning quality bar

Never justify a decision with only: 見やすい / 使いやすい / modern / clean / simple / professional / "best practice". Name the mechanism: cognitive load, decision cost, mental model, information scent, recognition vs recall, hierarchy, proximity/grouping, contrast, visual weight, feedback, mapping, discoverability, error prevention, task frequency, emphasis/de-emphasis, surface relationship. One named mechanism per decision is enough — depth of explanation is not the goal; the right decision is.

When principles conflict, say which side you took and why that context favors it (one sentence). When you deviate from a rule in this skill, say so and justify it — deviation is allowed, silence about it is not.

## Final critique (run before delivering any UI)

- **Task fit**: Can the target user complete their most frequent task fastest? Does anything on the screen serve the business against the user (dark pattern)? Remove it.
- **Hierarchy**: Squint test — does the most important element win? Is anything emphasized that shouldn't be (labels louder than data, borders louder than content)? Is everything emphasized (= nothing is)?
- **Structure**: Do groupings follow meaning (proximity = relatedness)? Is the user's location and next step always evident?
- **Density**: Is every dense area dense on purpose, every sparse area sparse on purpose?
- **States**: Empty, loading, error, long-content, and destructive-confirmation states designed — not just the happy path? In a static deliverable, are required states actually visible in the rendered page rather than only claimed in notes?
- **Wired honesty**: Does every visible control actually do what it signals? A trigger must perform what its appearance promises (⟨mi1-012, mi1-013⟩) — a filter, tab, or button that renders but does nothing misleads worse than its absence. Wire it, disable it visibly, or remove it.
- **Errors**: Are errors prevented where possible, and recoverable in place where not? Is destructive irreversibility guarded proportionally to its cost?
- **Words**: Would the target user use these labels themselves? Any jargon the books' user-warrant rules would reject?
- **Accessibility floor**: contrast, touch-target size, color-independent meaning, semantic headings.
- **Honesty check**: If a reviewer asked "why?" of any element, do you have a book-grounded answer? If not, either fix the element or flag the judgment call.
