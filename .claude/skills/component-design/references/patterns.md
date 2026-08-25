# Component Pattern Catalog

This file is the concrete UI pattern catalog for the component-design skill: a named
vocabulary of established component shapes to reach for once a component's *role* is already
decided, organized by functional family so the right neighborhood is fast to find. Route here
whenever a navigation, layout, list, action-exposure, data-display, form/control, overlay,
feedback, or mobile-touch component needs a concrete shape — not when the underlying role
itself is still undecided (that decision belongs to boundaries.md). Each family opens with its
selection framework, when one exists, before the catalog entries; every entry states when the
pattern applies, when to avoid it, and keeps its trade-offs two-sided rather than prescribing a
winner.

## Meta-Principle

### Familiar Patterns Reduce Learning Cost `PTN-125`
Design patterns work well because they are already established and familiar — they leverage
users' existing mental models for low-effort understanding. Introducing a wholly new pattern
imposes a real learning cost; product differentiation should come from how established
patterns are executed and connected to serve the product's purpose, not from inventing novel
patterns for their own sake. Do: check whether this problem already has a familiar,
well-understood pattern before inventing one. Exception: a genuinely new problem, where no
established pattern fits, can justify a new one despite the learning cost. Ask: does this
problem already have a familiar pattern that solves it? Is the proposed novelty serving the
product's purpose, or just differentiating for its own sake? (DS ch1)

## Family index (V2 — load only the family in play)

| Component family | File |
|---|---|
| Navigation (menus, tabs, breadcrumbs, sidebars) | patterns-navigation.md |
| Layout & panels (accordions, split panes, cards-as-layout) | patterns-layout.md |
| Lists (rows, virtualized, selection) | patterns-lists.md |
| Actions & commands (buttons, toolbars, bulk actions) | patterns-actions.md |
| Data display (tables, trees, information graphics) | patterns-data-display.md |
| Forms & controls (inputs, pickers, validation surfaces) | patterns-forms.md |
| Overlays & feedback (dialogs, toasts, progress) | patterns-overlays-feedback.md |
| Mobile & touch | patterns-mobile.md |
