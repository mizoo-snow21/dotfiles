# Naming & Shared Language

How to name a component so its scope and purpose stay legible, and how a team's shared
vocabulary keeps the system coherent. Route here when naming or renaming a component, or when a
component resists naming (a boundary smell). Split from system-consistency.md (V2); provenance
tags unchanged.

## Naming as a Boundary Contract

### Naming determines existence and reuse boundary `SYS-019`
An interface object without a meaningful, shared name is not a genuinely reusable part of the
system even if it exists in code. Naming it after a surface trait, a specific page, or a specific
content type locks it to that expression and discourages reuse elsewhere; vague category names
(e.g. "General") likewise defeat findability even when the underlying markup is simple.
Ask: would this name still make sense if the pattern were reused somewhere we haven't thought of
yet?
(DS ch5; IC ch10; AD ch5)

### A good name encodes its own usage guidance `SYS-020`
The best names hint at where/how a pattern should be used through the name/metaphor itself, so
the pattern doesn't have to separately assert its rules — e.g. "Minions" (many per page) vs.
"Boss" (exactly one). A name describing only form or shape (e.g. "Showcase") invites misuse and
duplication; naming for function ("Fact Grid") makes intended use unambiguous. Naming also
communicates ownership — a name should track who or what actually drives a component's behavior,
not just its visual form.
Ask: can someone infer this pattern's purpose from its name alone?
(DS ch5,10; IC ch9)

### Naming difficulty is a diagnostic, not a wordsmithing problem `SYS-021`
When no appropriate name comes to mind for a new pattern, that signals something wrong with the
pattern's definition, not a labeling gap: either its purpose is unclear or it duplicates a
purpose that already exists. The same diagnostic applies to content-section titles — an
un-nameable section signals the grouping itself doesn't match the content's natural structure (a
recurring "Other/Misc" category is a warning sign), and the fix is to regroup, not force a title
onto a bad grouping.
When: an "Other" catch-all is sometimes genuinely necessary and not itself a sign of a problem.
Ask: why can't we name this — is the purpose actually unclear, or does it duplicate an existing
module?
(DS ch5; DI ch4)

### Memorable names come from user vocabulary, cross-domain metaphor, and personality `SYS-022`
Naming a component after the vocabulary users themselves already use for it forces the team to
think from the user's perspective throughout the component's life. Metaphors borrowed from other
domains give the team something familiar to associate a module with; names with genuine
personality build a mutually-reinforcing family (a large CTA "Boss" pairs naturally with small
secondary "Minions"). A name lacking any evocative metaphor or personality is hard to remember,
and hard-to-remember names correlate with a pattern falling out of use and a near-duplicate being
created in its place — regardless of how technically precise the original name was.
Trade-off: user-vocabulary naming adds a small extra naming burden for developers, in exchange
for keeping the team user-perspective-aware.
(DS ch5)

### Naming is bounded, cross-role, and user-validated `SYS-023`
Naming as a cross-role team (not just the engineer who wrote the code) surfaces a more accurate
understanding of a module's true purpose, since different roles read it through different
lenses; it is a UX decision best made at the design stage, not left to whichever engineer
implements the component. The discussion should stay bounded, though — too many opinions produce
a vague name — so gather input broadly but leave the final call to the specific pair (e.g.
designer-developer) who built the module. Validate the chosen name against users' actual mental
model where feasible (e.g. card-sorting), which can reveal a name/appearance that doesn't match
user behavior at all.
Do: involve more than one role in naming, time-box the discussion, designate a final
decision-owner, and validate against real users where feasible.
Trade-off: broader input improves purpose-accuracy but risks vagueness if not bounded by a clear
decision-owner.
(DS ch5,8)

### A name should track a pattern's actual specificity `SYS-024`
A name should reflect where a pattern sits on the specific-to-generic spectrum and signal
whether it's safe to reuse elsewhere or intentionally scoped to one context. When unsure, start
specific; if a pattern is later reused more broadly than intended, rename it to reflect the new
scope — a stale name misleads the team about whether reuse is safe.
Do: rename a pattern when its actual reuse scope no longer matches its original name.
(DS ch8)

### A name is real only once it displaces ad hoc description `SYS-025`
A pattern isn't a genuinely functional part of the shared design language until the team
actually uses the approved name in place of whatever ad hoc description was used before naming.
Consistent conversational use of the approved name — not the act of choosing it — is the real
completion criterion, and is what keeps naming in design files and code aligned with how the
team actually talks about the component.
Ask: has the team's actual conversational habit switched to the approved name, or are people
still describing it ad hoc?
(DS ch5)
## Shared Language

### Shared language requires agreement on purpose and context, not just names `SYS-026`
A team sharing a vocabulary isn't enough if members interpret the same term differently — true
shared language requires agreement on a pattern's name AND its purpose, the context it's used
in, and when it should be used, or a nominally "unified" language actually diverges in practice.
Patterns and design principles alone are not sufficient for team consistency: a product built by
many contributors stays unified only if contributors share the same principles, aligned brand
vision, common design/frontend approach, and knowledge of which patterns are effective and why —
not merely a shared component library.
Ask: does everyone agree not just on the pattern's name, but on why it exists, what problem it
solves, and when to use it?
(DS ch1,4,5; AD ch1)

### An explicit design language reframes debates around necessity, not pixels `SYS-028`
Once a design language is made explicit and shared, a small validated improvement discovered in
one place can propagate to every pattern that shares that language, instead of being adjusted
one instance at a time. It also shifts team conversations from an element's pixel-level
appearance to whether a pattern is needed at all, reasoning in terms of context, purpose, and
usage.
Trade-off: investment in making the language explicit vs. the ongoing efficiency gained from
system-wide leverage.
(DS ch1)

### Visibility drives everyday adoption of the pattern language `SYS-073`
Naming shared patterns as a team is necessary but not sufficient — the language must be actively
spread across the whole team so it gets used in every relevant context. Displaying the product's
most characteristic patterns labeled, in a space the team encounters casually and often (not
only a documentation site nobody opens proactively), lowers the barrier to participation and
helps even initially uninterested members gradually engage.
Do: make the current pattern language visible somewhere the team encounters casually and often,
not only in documentation nobody opens proactively.
(DS ch5)
