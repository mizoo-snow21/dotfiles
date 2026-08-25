# Consistency Mechanisms

Mechanisms that keep look-alike behavior genuinely consistent and intentional variation intact
as the system grows. Route here when auditing consistency or judging whether a stylistic
exception threatens coherence. Split from system-consistency.md (V2); provenance tags unchanged.

## Consistency Mechanisms

### Fix a shared-pattern defect at the system level, not per-instance `SYS-010`
When a defect or improvement opportunity is found in one specific instance of a shared pattern,
the instinctive local fix is to patch just that occurrence. Because the underlying pattern is
shared, the better default is to fix it once at the pattern/system level so every place using it
benefits — a one-off patch leaves the same defect recurring everywhere else the pattern is
reused, and repeated one-off patches erode the system's consistency over time. Cleaning up one
instance also does not prevent recurrence unless the underlying mechanism that produced the
problem is itself addressed.
Do: when real content or a bug breaks a pattern on one page, fix the underlying
component/pattern definition, not just that page.
Trade-off: system-level fixes take more investigation/friction upfront but prevent gradual
erosion of consistency across the whole system.
Ask: is this problem isolated to this one application, or does it reflect a defect in the shared
pattern that would recur anywhere else it is used? If we clean this up today, what stops the same
problem from reappearing later?
(AD ch2,5; DS ch5 review)

### Document a variant's prominence, frequency, and purpose as explicit classification `SYS-029`
A functional pattern's visual prominence ("loudness") can be documented as an explicit, shared
classification rather than argued ad hoc: for each variant, record its type, prominence,
frequency of use, and purpose (e.g. Primary = high prominence + frequent + main action; Secondary
= lower prominence + occasional + supporting action). This converts subjective visual-hierarchy
disputes into a documented, referenceable system.
Do: record prominence/frequency/purpose per variant in shared documentation.
(DS ch1)

### A properly generalized module costs more upfront but makes reuse near-free `SYS-066`
→ Canonical: `BND-013` in boundaries.md (economics of promoting to a shared pattern). (DS ch3)

### Establish and centralize a Visual Framework `SYS-071`
Define and reuse a single consistent basic layout, color palette, font set, and tone/vocabulary
across every page/window of a product, flexible enough to accommodate each page's distinct
content, including keeping "you are here" signposts (title, logo, breadcrumb, current-location
nav) and navigation devices consistently placed across pages. Implementing this forces a
separation between the style/framework layer and page content, analogous to a stylesheet:
framework decisions are defined once, centrally, and referenced by content rather than repeated
ad hoc per page, so a framework-wide correction doesn't require editing every page individually.
This is not merely cosmetic — a badly organized site can be technically compliant and still
alienate cognitively-impaired or time-pressured users, making information architecture itself an
inclusion concern.
When: a homepage or main window is commonly allowed to be visually "special"/distinct from
interior pages, while still sharing some framework characteristics.
Do: share a defined color/font set and consistent tone/vocabulary across all pages, keep
signposts and navigation devices consistently placed, and centralize style/framework definitions
separate from content.
Ask: do the homepage and interior pages share enough visual DNA that a user recognizes them as
the same product? If the framework's color/font/spacing needs to change, does that require
editing every page's content, or only one shared definition?
(DI ch4; IC ch4,6)

### For dynamic content, the hard problem is the permanent record, not the live update `SYS-072`
The mechanical problem of announcing a transient, real-time event is comparatively easy to solve;
the harder and more important task is the clarity of each message's content and, above all, the
structure and presentation of the permanent history/interface state into which each transient
message offers only a fleeting glimpse. Structuring content well remains paramount even for
dynamic, real-time events, not just static documentation.
(IC ch10)

### An off-the-shelf framework trades speed for distinctiveness `SYS-075`
Adopting a shared front-end framework speeds development and gives consistent, cross-browser-
tested components, but interfaces built on the same framework tend to look alike, ship unused
CSS/JS as bloat since teams rarely use 100% of a framework, and can require so much custom
override that the framework's speed benefit is outweighed by the cost of fighting its structure.
A framework's own naming/structure conventions can also clash with an organization's existing
lexicon.
Trade-off: development speed and consistency vs. brand/visual distinctiveness; out-of-the-box
completeness vs. shipped bloat; initial customization ease vs. long-term cost of fighting
framework structure.
Ask: will most of the framework's components actually be used, or will much of it ship unused?
Does the framework's conventions clash with the team's existing codebase?
(AD ch1)

### Design for device/context flexibility, not one fixed visual `SYS-076`
Because the web is consumed across a large and growing diversity of devices, screen sizes, input
types, and capabilities, components and layouts should be designed and built to work well across
that range rather than assuming one canonical, fixed visual presentation (the print-era mentality
of a design as a static image). This implies treating performance and progressive enhancement as
core design constraints rather than afterthoughts, and anticipating that the device/context
landscape will keep expanding.
Do: create flexible layouts and components that look and function well irrespective of device
dimension or screen size, treat performance as an essential design principle, progressively
enhance from a core experience, and design for future-friendliness.
Ask: does this component assume one fixed visual presentation, or will it keep working as new
devices/contexts appear?
(AD ch4)

### Separate theme stylesheet vs. a single CSS invert-filter override `SYS-077`
A fully separate alternative-theme stylesheet is flexible but costs extra load weight and has to
be kept in sync manually as the site evolves. Augmenting the existing light theme with a terse
CSS filter:invert(100%) override is far cheaper and self-maintaining, at the cost of only ever
producing a strict color inversion rather than an arbitrarily distinct visual theme.
When: building a simple light/dark theme toggle where the two themes are just inverted
brightness, not divergent designs; avoid the invert-filter approach when the alternative theme
needs to differ from the base theme in more than color/brightness.
Trade-off: flexibility (separate stylesheet) vs. maintenance/performance efficiency
(invert-filter).
(IC ch6)
