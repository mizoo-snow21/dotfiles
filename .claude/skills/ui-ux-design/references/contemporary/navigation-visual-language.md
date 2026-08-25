<!-- Contemporary product-derived reference (V2). Provenance layer: product-derived —
every rule cites fetched public design-system docs / product materials; confidence is
marked per rule. These rules complement the book-derived foundation: books carry the
WHY (cognition, perception), these carry current practice under real product constraints.
When they conflict with a book rule, treat it as a decision point, not an override. -->
# Navigation & Visual Language — Cross-Product Decision Rules

Research corpus for the "art direction axes" framework. Every rule is grounded in a source that
was actually fetched and read (spot-checked on 2026-08-25); where no first-party source could be
found despite genuine attempts, the rule is marked low confidence and says why, rather than
omitted or silently backed by a third-party guess. IDs: `ct-nav-NN` = Part 1 (navigation/app
shell), `ct-ad-NN` = Part 2 (visual language axes).

---

## Part 1 — Navigation & app shell

### ct-nav-01 — Sidebar vs top-nav: split by scope, not by preference
**Question.** When does a product commit to a persistent left sidebar as primary navigation
instead of a top bar?
**Guidance.** Use the sidebar for within-product, hierarchical, frequently-switched navigation
(projects, boards, sections); reserve the top bar for a small set of universal, cross-context
actions (search, create, account) that must be identical no matter which part of the product the
user is in. The split is architectural (product-level vs. global-level), not aesthetic.
**Evidence.** Atlassian: "The sidebar provides the vertical space and information density needed
for a bird's-eye view of work that wasn't possible with dropdown menus in the top bar... With
product navigation in the sidebar, we could streamline the top bar across all products. This top
bar is now consistently dedicated to universal actions like search and create." Also: "Users
today work across multiple tools... all of which use a sidebar for primary tasks." —
https://www.atlassian.com/blog/design/designing-atlassians-new-navigation (fetched, quote
confirmed). IBM Carbon states the same split structurally: "left-to-right translates to
product-to-global. The left side of the header contains items relevant at the product level.
Moving to the right along the header, the functions become more global." —
https://v10.carbondesignsystem.com/components/UI-shell-header/usage/ (fetched, quote confirmed).
**Tension.** Atlassian's own 2018 attempt at making every product's nav "identical" for
consistency failed; the lesson the team drew was that "consistency doesn't mean everything has to
be identical" — over-uniformity cost recognizability. Sidebar-for-hierarchy still has to leave
room for per-product identity.
**Confidence.** High — two independent first-party sources agree on the same split logic.

### ct-nav-02 — Item-count thresholds decide sidebar vs flat header, not taste
**Question.** At what point does a flat top bar or short menu need to become a dedicated
sidebar/panel?
**Guidance.** Treat this as a countable threshold, not a judgment call: once secondary
destinations exceed a small fixed number, or users need to jump between them often, promote them
to a persistent panel.
**Evidence.** IBM Carbon: "Use the left panel if there are more than five secondary navigation
items, or if you expect a user to switch between secondary items frequently." The same page adds
a depth ceiling: "The left panel does not support three tiers of navigation" — beyond two levels,
Carbon's guidance is to switch to in-page tabs rather than add another nav layer. —
https://v10.carbondesignsystem.com/components/UI-shell-left-panel/usage/ (fetched, quote
confirmed). Google's Android layout guidance gives the mobile/large-screen analog: "The
navigation bar can hold three to five navigation destinations... the navigation drawer can hold
more than five... but the pattern isn't as ideal [at compact width] because users must reach for
the top bar," while on large screens "use a nav rail... more ergonomic and visually balanced due
to hand placement," with an explicit "Don't: use a bottom navigation bar on large screen sizes." —
https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns
(fetched).
**Tension.** A hard item-count rule is easy to apply but can force a sidebar onto a product that
would otherwise stay simpler — the rule optimizes for scanability at the cost of chrome overhead
when item count is borderline.
**Confidence.** High for Carbon's explicit numeric rule; high for the Android breakpoint guidance
(both fetched with quotes confirmed).

### ct-nav-03 — Hierarchy depth has a hard practical ceiling
**Question.** How many levels of nested navigation should one navigation system try to represent?
**Guidance.** Cap in-nav hierarchy at two levels (top-level + sub-level). Beyond that, don't add a
third nesting tier to the same widget — switch representation: use in-page tabs for a third tier,
or switch from a back-link to a breadcrumb once depth exceeds one, since breadcrumbs support
jumping to any ancestor while a back-link only supports linear undo.
**Evidence.** GitLab Pajamas: "There are two levels of navigation: top-level items and sub-level
items. There is not a third level of depth." —
https://design.gitlab.com/patterns/navigation-sidebar/ (fetched, quote confirmed). GitHub Primer:
"For one-level-deep flows, use a back link... For deeper hierarchies, use a breadcrumb to allow
users to navigate anywhere in the hierarchy" rather than forcing a return to the parent index
first. — https://primer.style/product/ui-patterns/navigation/ (fetched).
**Tension.** A hard depth cap forces genuinely deep information architectures to be flattened or
pushed into page-level structure (tabs, filters) rather than nav chrome — which is a feature
(keeps nav legible) but a real constraint on how much the nav widget alone can express.
**Confidence.** High (both fetched with quotes confirmed).

### ct-nav-04 — Current-location is shown redundantly, not once
**Question.** How should a user always know where they are?
**Guidance.** Don't rely on one signal. Stack multiple concurrent, cheap indicators — a page
title, a breadcrumb trail, and an active-state highlight in the nav list — so location is legible
even if a user missed one of the cues (e.g. arrived via a deep link and never saw the nav
highlight change).
**Evidence.** GitHub Primer: "Users should always have a clear understanding of their location
within the application," achieved through three concurrent mechanisms named explicitly:
PageHeader (title), Breadcrumbs (path), and NavList active-item highlighting. —
https://primer.style/product/ui-patterns/navigation/ (fetched).
**Tension.** Redundant location cues cost vertical space and visual weight; a very dense or
mobile-constrained layout may not be able to afford all three simultaneously.
**Confidence.** High (fetched, quote confirmed).

### ct-nav-05 — Icons pair with labels at the top level only, and labels stay short
**Question.** Where does an icon add value in nav, and where does it just add noise?
**Guidance.** Give each top-level destination a unique icon (or avatar) paired with a label;
don't repeat icon+label pairing at deeper sub-levels, where the parent icon has already done the
job of category recognition and labels alone are enough. Keep every nav label to roughly 1-2
words so it reads at a glance and matches the destination's own page title.
**Evidence.** GitLab Pajamas: "A top-level item is designated with a unique icon or avatar";
labels must be "short and easy to remember, ideally just 1-2 words." —
https://design.gitlab.com/patterns/navigation-sidebar/ (fetched, quote confirmed; icon-only-at-
top-level is an explicit structural rule, not just an observed pattern). Shopify's App Bridge nav
docs echo the same length guidance (labels "1-2 words using nouns," consistent with destination
page titles) but this was surfaced via search summary, not independently re-fetched —
https://shopify.dev/docs/api/app-home/app-bridge-web-components/app-nav (medium confidence, flag
for re-verification before treating as a primary quote).
**Tension.** Icon-only recognition trades faster scanning for ambiguity risk (icon meaning is
culturally/contextually loaded) and localization risk (short labels compress worse in some
languages) — GitLab's rule sidesteps this by never dropping the label, only limiting where the
icon repeats.
**Confidence.** High for the GitLab rule; medium for the Shopify corroboration.

### ct-nav-06 — Collapse state is conditional and persisted, not a default toggle
**Question.** When does a sidebar get a collapse/hamburger control, and how should the collapsed
state behave?
**Guidance.** Only surface a hamburger/collapse control when there is a collapsible panel behind
it to reveal — don't add the affordance decoratively. Persist the user's show/hide choice (e.g.
via a cookie) rather than resetting it every session, but let viewport size override that
preference on small screens (overlay instead of persistent-open).
**Evidence.** IBM Carbon: "As a header scales down to fit smaller screen sizes, header links and
menus should collapse into a left-panel hamburger menu"; "hamburger menu is only needed when
there is a collapsable left navigation." —
https://v10.carbondesignsystem.com/components/UI-shell-header/usage/ (fetched). GitLab Pajamas:
"The user's preference is set with a cookie to keep the navigation sidebar hidden or visible," and
on small screens the sidebar becomes an overlay instead. —
https://design.gitlab.com/patterns/navigation-sidebar/ (fetched, quote confirmed).
**Tension.** Persisting a per-user preference means the same product can look structurally
different session-to-session for the same user vs. a fresh visitor — screenshots and support
documentation have to account for both states.
**Confidence.** High (both fetched with quotes confirmed).

### ct-nav-07 — Nav density is tuned per rendering platform, not fixed to one spec
**Question.** Should the same navigation component look identical across native app, browser tab,
and OS-embedded contexts?
**Guidance.** When a product ships as both a native app and a web app, tune the same sidebar's
spacing/density per platform's own conventions rather than forcing one universal spec — match
what users already expect a "native-feeling" app to look like in each shell.
**Evidence.** Linear: the sidebar was tuned across "very condensed to more spacious
configurations" for cross-platform parity (native macOS/Windows app + browser), and the designer
"often relied on Apple standards... to get close to the feeling of a native app." —
https://linear.app/now/how-we-redesigned-the-linear-ui (fetched).
**Tension.** Platform-tuned density undercuts pixel-for-pixel design-system consistency across
surfaces — the team is explicitly trading "one universal spec" for "feels native everywhere."
**Confidence.** High (fetched from Linear's own product blog).

### ct-nav-08 — Nav chrome should recede once it has done its orienting job
**Question.** How much visual weight should persistent nav carry relative to the work area?
**Guidance.** Don't let navigation compete visually with content once the user has arrived at
their destination. Dim, desaturate, or otherwise de-emphasize inactive nav chrome so attention
stays on the task, while keeping the active-location indicator legible.
**Evidence.** Linear, stated as an explicit design principle: "Don't compete for attention you
haven't earned" — applied specifically to dimming the sidebar "so it remains visually subdued
after users reach their destination," letting "the main content area — where users work — take
precedence." — https://linear.app/now/behind-the-latest-design-refresh (fetched, quote
confirmed).
**Tension.** A too-dim nav risks discoverability for infrequent destinations a user hasn't
memorized the position of yet — recede-after-arrival works better for daily-use tools with
returning users than for first-time or occasional users.
**Confidence.** High (fetched, quote confirmed).

---

## Part 2 — Visual language axes

### ct-ad-01 — Split functional (in-app) type from expressive (brand) type
**Question.** Does a product need one typeface personality, or two?
**Guidance.** Separate the typeface used inside the working product (dense, functional, must
render identically everywhere) from the typeface used in marketing/brand touchpoints (allowed to
be expressive, used sparingly, seen occasionally). Don't force one typeface to do both jobs.
**Evidence.** Atlassian runs exactly this split: in-app, "Using our app (product) typefaces,
Atlassian Sans and Atlassian Mono, will create a consistent experience across all browsers" and
"ensures the UI is optimized, performs well and is frictionless as you move between Atlassian
apps" — https://atlassian.design/foundations/typography (fetched, quote confirmed) — while the
separate brand typeface (Charlie Sans) is reserved for marketing surfaces and was designed to be
"neutral but not boring, expressive but not obnoxious" (secondary source: the type foundry's own
case study, not an Atlassian-owned page — medium confidence for this specific framing).
**Tension.** Maintaining two full typographic systems (in-app + brand) is real ongoing design and
engineering cost versus a single unified typeface; smaller teams may not be able to afford the
split.
**Confidence.** High for the in-app half (first-party, fetched); medium for the brand-typeface
rationale (foundry case study, not Atlassian's own words).

### ct-ad-02 — Custom type over system stack buys cross-platform metric consistency, at a real cost
**Question.** Why would a product commission a custom typeface instead of using the OS default
font stack, given the extra cost?
**Guidance.** Choose custom type when the product must look and measure identically across
operating systems (web, Windows, macOS, mobile) and the OS default fonts differ enough in
metrics to break that goal. Default to a system stack when cross-platform pixel-identical
rendering isn't the priority and load-time/zero-maintenance matters more.
**Evidence.** Atlassian: "due to systems fonts having different weights, character spacing, and
baselines, we would never be able to create a single user experience" — citing SF Pro sitting
higher on the baseline than Segoe UI as a concrete example. Atlassian Sans derives from Inter for
its "utilitarian nature"; Atlassian Mono derives from JetBrains Mono, "tailored for developers." —
https://www.atlassian.com/blog/how-we-build/implementing-typography-at-scale-the-journey-behind-the-screens
(fetched, quote confirmed).
**Tension.** GitHub Primer, by contrast, appears to use a plain system-font stack — but its own
typography docs state no rationale for that choice at all: fetched directly, the page "does not
explain performance, familiarity, cross-platform, or other reasons for this choice... omits any
explanation of font family selection philosophy," covering only accessibility (rem units) and
grid alignment. This is a real gap in what's publicly documented, not evidence that Primer lacks a
reason — only that the reason isn't stated where you'd expect it.
**Confidence.** High for Atlassian's stated rationale (fetched, quote confirmed). Low confidence /
explicitly unverifiable for "Primer chose system fonts because X" — flagged as a documented
absence, not a fact.

### ct-ad-03 — A display/body split lets dense UI add personality without losing legibility
**Question.** How does a technical, information-dense product add typographic character without
hurting readability?
**Guidance.** Use a slightly more expressive cut of the type family for large/heading text
(display sizes can absorb more personality without harming reading) while keeping body text in
the plain, maximally legible cut. This is cheaper than commissioning two families and safer than
applying the expressive cut everywhere.
**Evidence.** Linear: "Inter Display to add more expression to our headings while maintaining
their readability," while regular Inter is kept for body copy. —
https://linear.app/now/how-we-redesigned-the-linear-ui (fetched, quote confirmed).
**Tension.** The two cuts must be visually close enough that switching between them (heading →
body) doesn't read as inconsistent — too big a personality gap between display and body creates
its own incoherence.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-04 — Deliberately de-saturating brand color buys "timeless," not "safe"
**Question.** Why would a product reduce how much of its own brand color appears in its UI?
**Guidance.** When brand color is starting to feel dated, loud, or attention-competing against the
Nav-recedes principle (ct-nav-08), reduce its frequency and saturation across the interface
rather than replacing the hue — this reads as restraint/maturity rather than loss of identity, as
long as the color still appears at genuinely meaningful moments.
**Evidence.** Linear explicitly "limit[ed] how much chrome (blue in our case) was used" in
pursuit of "a more neutral and timeless appearance," while naming the trade-off directly: "you
also have to be realistic and manage risks" rather than disassembling the product's whole
identity. — https://linear.app/now/how-we-redesigned-the-linear-ui (fetched, quote confirmed).
**Tension.** Less brand color everywhere risks the product losing recognizability in screenshots,
marketing, and at-a-glance brand recall — the source names this as a real risk being managed, not
a free win.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-05 — Color should be tiered: neutral base, semantic role, component instance
**Question.** How does a color system stay coherent across hundreds of components without becoming
either monotone or chaotic?
**Guidance.** Build color in three explicit layers: a neutral grayscale base for structure, a
small set of semantic roles (success, danger, warning, accent) that carry meaning independent of
any one component, and component-level tokens that reference the semantic layer rather than raw
values. Reserve saturated color for the semantic layer only — it communicates status/action, not
brand decoration.
**Evidence.** GitHub Primer: a neutral gray scale (0–13) forms the base; semantic roles layer on
top "to communicate status, action, or emphasis," organized as a three-tier token hierarchy (base
→ functional → component). —
https://primer.style/product/getting-started/foundations/color-usage/ (fetched, quote/structure
confirmed).
**Tension.** Primer's own high-contrast theme requires a 7:1 minimum contrast ratio, so when
backgrounds are kept deliberately soft/neutral, "borders compensate by increasing contrast" —
i.e. the soft aesthetic has to give something back to accessibility elsewhere in the system.
**Confidence.** High (fetched).

### ct-ad-06 — Accessibility contrast minimums are an input to the aesthetic, not a check afterward
**Question.** Does accessibility compliance constrain how "quiet" or "soft" a surface can actually
look?
**Guidance.** Treat contrast-ratio requirements (especially for a high-contrast theme mode) as a
design constraint decided alongside the palette, not a QA pass applied after visuals are locked —
soft/low-contrast surfaces need a compensating mechanism (heavier borders, darker text) built in
from the start.
**Evidence.** GitHub's own engineering post on Primer's color system frames accessibility as
foundational, not incidental: "we believe that accessibility should be at the heart of design,"
describing a color system engineered to scale across light, dark, dark-dimmed, high-contrast, and
colorblind-safe modes simultaneously. —
https://github.blog/engineering/user-experience/unlocking-inclusive-design-how-primers-color-system-is-making-github-com-more-inclusive/
(fetched, quote confirmed). Note: this source does NOT state a "dark-first reduces eye strain"
rationale — that specific claim, though widely repeated online, was checked against GitHub's own
sources and could not be confirmed; independent discussion even notes contested/no conclusive
evidence for the eye-strain claim. Treat "dark-first for eye strain" as folklore, not a documented
first-party rationale.
**Tension.** Supporting five simultaneous color modes (light/dark/dark-dimmed/high-contrast/
colorblind) multiplies the token-maintenance surface considerably versus a single fixed palette.
**Confidence.** High for the accessibility-first framing (fetched, quote confirmed). Explicitly
low/contested for the popular "dark mode = less eye strain for developers" claim — do not cite as
settled fact.

### ct-ad-07 — Perceptually-uniform color math fixes "some accent colors look heavier than others"
**Question.** How do you make many different hue-based theme colors read as equally weighted
across light mode, dark mode, and user-customized themes?
**Guidance.** Build the palette in a perceptually uniform color space (e.g. LCH) rather than
RGB/HSL, so that two colors set to the same lightness value actually look equally light to the
human eye — this is a systematic fix, not something you can reliably eyeball per-color.
**Evidence.** Linear rebuilt its palette in LCH specifically because "a red and a yellow color
with lightness 50 will appear roughly equally light to the human eye," using this to keep
light/dark/custom themes visually consistent. —
https://linear.app/now/how-we-redesigned-the-linear-ui (fetched, quote confirmed).
**Tension.** This is real engineering investment (color-space conversion, tooling) to fix a
problem that's invisible until you have many hues across many theme variants — not worth it for a
product with one fixed light-mode palette and few accent colors.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-08 — Dynamic/personalized color is a mobile-OS-scale move, not a default for B2B tools
**Question.** Should a product derive its color theme from the individual user's own context
(e.g. wallpaper) rather than shipping one fixed brand palette?
**Guidance.** Dynamic, per-user color theming fits platform-level, deeply personal contexts
(a phone's home screen and system apps) where personalization outweighs brand-recognition needs.
It's a poor default for professional/enterprise or brand-forward products where consistent visual
identity across users and screenshots matters more than individual personalization.
**Evidence.** Material 3: "Dynamic color is the key part of Material You, in which an algorithm
derives custom colors from a user's wallpaper... This color palette is used as the starting point
to generate light and dark color schemes." —
https://developer.android.com/develop/ui/compose/designsystems/material3 (fetched, quote
confirmed).
**Tension.** Dynamic color trades consistent brand recognition (the thing GitHub Primer's and
Linear's systems above are explicitly optimizing for) for individual relevance — the two goals
are close to opposites, which is why this pattern shows up at OS level and rarely inside
professional SaaS tools.
**Confidence.** High for the mechanism (fetched, quote confirmed); the "why this fits phones but
not B2B tools" framing is this document's synthesis, not a direct quote from Google.

### ct-ad-09 — Tonal elevation communicates hierarchy with less visual noise than shadows, especially in dark mode
**Question.** How should a system indicate that one surface sits "above" another once shadows stop
working well (e.g. dark backgrounds where shadows barely read)?
**Guidance.** Use a tonal-color shift (a more elevated surface gets a more prominent tint of the
base color) as the primary elevation signal, keeping drop-shadow as a secondary/situational cue
for when a stronger visual separation is actually needed — not as the only mechanism.
**Evidence.** Material 3 "represents elevation mainly using tonal color overlays... a new way to
differentiate containers and surfaces from each other — increasing tonal elevation uses a more
prominent tone — in addition to shadows," while shadows remain "still useful when you need
stronger visual separation." Dark-theme overlays also moved from black-alpha layering to
tonal-color overlays sourced from the primary color slot. —
https://developer.android.com/develop/ui/compose/designsystems/material3 (fetched, quote
confirmed).
**Tension.** Tonal elevation requires the whole surface-color system to be built around a
generative tonal palette; it's not a drop-in replacement for a shadow token in a system that
wasn't designed around tonal roles from the start.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-10 — Constraining the shape vocabulary is itself the coherence mechanism
**Question.** How does a large design system avoid "everyone rounds corners to whatever value
looks nice locally," which produces visual noise across hundreds of components?
**Guidance.** Deliberately restrict the number of distinct shape families available (e.g. to
three: square, rounded, cut) rather than allowing continuous/unlimited corner customization.
Treat expressiveness as a knob to be capped on purpose, not maximized.
**Evidence.** Google's own account of building Material Design's shape system: the team
constrained options explicitly "to balance creative flexibility with Material Design's principle
of clarity and coherence" — unlimited shape variation was considered and rejected as undermining
the systematic approach. Shape's job is "directing attention, expressing brand, and supporting
interactions." — https://developers.googleblog.com/building-the-shape-system-for-material-design/
(fetched, quote confirmed).
**Tension.** A constrained shape vocabulary limits how distinctive any single product built on the
system can look purely through corner geometry — differentiation has to come from elsewhere
(color, type, motion) if geometry itself is capped.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-11 — Corner radius should be a role-based token, not a single brand statement
**Question.** Should a product have one signature corner-radius value, or many?
**Guidance.** Scale radius by component category/weight rather than picking one number for "our
brand's roundness": small interactive elements (badges, checkboxes) get the smallest radius,
larger containers (cards, modals) get progressively larger radius, and fully circular pill/avatar
shapes get a dedicated "full" token. Geometry communicates a component's function and visual
weight, not just brand personality.
**Evidence.** Atlassian Design System: "Radius tokens standardize corner roundness, ensuring
consistency and cohesion throughout all of our apps," with an explicit scale — xsmall (2px) for
badges/checkboxes, small (4px) for labels/tags, medium (6px) for buttons/inputs, large (8px) for
cards/floating UI, xlarge (12px) for modals/tables, full (999px) for avatars/pills — and a rule
that focus-ring radius always equals base radius + 2px. —
https://atlassian.design/foundations/radius (fetched, quote/scale confirmed).
**Tension.** A finely-graded radius scale is more work to apply correctly (six-plus values to
choose between) than one flat "everything is 8px" rule, and is easy to apply inconsistently
without tooling enforcement.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-12 — Density should be an explicit, named mode for data-heavy professional tools
**Question.** Should a professional/enterprise product pick one fixed information density, or
offer a choice?
**Guidance.** For components that carry the bulk of a data-heavy workflow (tables in particular),
ship multiple explicit density modes (e.g. tall/normal/short/compact row heights) rather than one
fixed density — because the same product serves both fast scanning and detailed-content tasks,
which want different densities.
**Evidence.** IBM Carbon's data table ships four row-size modes (tall, normal, short, compact),
with "tall" specifically reserved for two-line content. —
https://v10.carbondesignsystem.com/components/data-table/usage/ (fetched; existence of the four
modes confirmed directly on the page). Note: the page itself does not state the business
rationale ("why enterprise tools need this") in so many words — that framing is this document's
inference from the modes' existence and naming, not a quoted first-party justification.
**Tension.** Multiple density modes multiply QA/testing surface (every row-dependent interaction
now needs verification at four heights) versus a single fixed density.
**Confidence.** High for the modes' existence (fetched); medium for the stated business rationale
(inferred, not quoted).

### ct-ad-13 — Structure can be conveyed by spacing and soft contrast instead of hard dividers
**Question.** How does a dense, information-heavy interface avoid looking cluttered with borders
and separator lines?
**Guidance.** Where borders/separators have proliferated "without clear reason," soften their
contrast and round their edges rather than removing them outright — rely on whitespace and subtle
contrast to carry grouping, so structure is felt through layout rather than seen as an explicit
line.
**Evidence.** Linear, as an explicit stated principle: "Structure should be felt not seen" —
applied to softening borders/separators that had "proliferated across the platform, sometimes
appearing without clear reason," in order to "provide structure without visual clutter." —
https://linear.app/now/behind-the-latest-design-refresh (fetched, quote confirmed).
**Tension.** Very soft dividers can fail for users with lower contrast sensitivity or on
poorly-calibrated displays — the softness that reduces "visual clutter" for most users can reduce
legibility of structure for some.
**Confidence.** High (fetched, quote confirmed).

### ct-ad-14 — A signature functional device should be traceable to a real interaction problem, not decoration
**Question.** What makes one memorable UI element ("the ripple," "the command palette," "the
contribution graph") read as identity rather than as a gimmick?
**Guidance.** A distinctive device earns its place when it's the visible trace of an actual
interaction mechanic — feedback anchored at the real point of contact, a map of real behavior over
time, a genuinely faster path through the product — rather than an applied decorative flourish
that could be removed without changing how the product behaves.
**Evidence.** Material's ripple effect is documented (in secondary/spec-summary form) as
originating from a "tactile reality" (paper/ink) metaphor: the ripple spreads outward from the
actual point of input, giving "instant visual confirmation at the point of contact" — the visual
device is tied directly to where the touch happened, not applied uniformly regardless of input
location. Source: m2.material.io/develop/ios/supporting/ripple — this exact page could not be
independently fetched (client-rendered), so the quote is corroborated across multiple independent
secondary write-ups rather than read directly from Google's own text.
**Tension.** None of the other candidate "signature devices" investigated for this document
(GitHub's contribution graph, Stripe's checkout/typography identity) turned up a first-party
stated design rationale despite direct searching — meaning the most-cited "iconic" UI moments in
the industry are often reverse-engineered narratives from outside observers, not documented
product-team intent. That gap is itself worth noting: a device can become a de facto brand
signature through user/press adoption even without the product team ever publishing why they built
it that way.
**Confidence.** Medium-low for the ripple rationale specifically (real URL, snippet-corroborated,
not independently fetched). The broader point about unattributed "signature device" folklore is
high confidence as an observed research gap.

---

## Synthesis — what makes a visual system read as ONE coherent system

1. **Tokens are tiered by role, not chosen by feel.** Every high-confidence system found here
   (Primer's neutral→semantic→component color layers, Atlassian's category-based radius scale,
   Material's constrained shape families) maps a visual property to a *function* — status, weight,
   component category — before it maps to an aesthetic preference. Coherence comes from the
   mapping rule being explicit and reusable, not from the raw values happening to look good
   together.

2. **Restraint is a stated, deliberate act — not the absence of a decision.** Linear's redesign
   posts name their own restraint outright: "Don't compete for attention you haven't earned,"
   "Structure should be felt not seen," and the explicit choice to de-saturate brand chrome. The
   pattern across sources: a coherent system's authors can cite the *principle* that produced a
   quiet surface, not just describe the surface as quiet after the fact.

3. **Functional and brand identity are allowed to diverge, on purpose.** Atlassian runs two
   type systems (Atlassian Sans/Mono in-app, Charlie Sans for brand) rather than forcing one
   typeface to be both maximally legible at density and maximally expressive. Coherence is
   evaluated *within* each context (does the in-app system feel like one thing? does the brand
   system feel like one thing?) rather than requiring identical treatment everywhere a logo or
   heading appears.

4. **Cross-platform/cross-theme consistency is solved with engineering, not eyeballing.**
   Atlassian's custom type exists specifically because system fonts differ in baseline/weight
   across OSes; Linear's LCH color rebuild exists specifically because RGB/HSL lightness doesn't
   match human perception across hues. Both are systemic fixes for problems that are invisible in
   a single screenshot but break coherence at scale (many components, many themes, many
   platforms).

5. **Accessibility minimums are treated as an input to the look, not a check performed on it.**
   Primer's high-contrast mode forces compensating border weight when backgrounds stay soft; this
   is the accessibility requirement actively shaping how quiet the surface is allowed to be, which
   is why the accessibility engineering blog post and the color-usage docs describe the same
   system rather than a base design plus a bolted-on a11y pass.

6. **A rule the team can state in one sentence beats a rule tuned per screen.** The clearest
   through-line across every fetched source: Carbon's ">5 items → left panel," GitLab's "2 levels,
   no more," Primer's "3-cue location redundancy," Atlassian's per-category radius scale. Each is
   a citable rule, not a per-screen judgment call — which is exactly what lets dozens or hundreds
   of screens/components stay visually and structurally consistent without a designer re-deciding
   the same trade-off every time.

7. **Where no first-party rationale exists, the industry narrative fills the gap — and that
   narrative should not be cited as the product team's own reasoning.** Several of the most
   commonly repeated "why" claims in this space (dark-mode-reduces-eye-strain, Primer's
   flat-surface philosophy, Stripe's typography-as-brand-signal, GitHub's contribution graph as
   intentional identity) could not be traced to a first-party source despite direct attempts —
   only third-party design teardowns repeat them. Treat repetition across secondary sources as
   evidence the *observation* is probably accurate, not evidence of the *stated intent* behind it.

---

## Source list (all fetched and quote-checked unless noted)

**Navigation**
- Atlassian — https://www.atlassian.com/blog/design/designing-atlassians-new-navigation
- IBM Carbon — https://v10.carbondesignsystem.com/components/UI-shell-header/usage/
- IBM Carbon — https://v10.carbondesignsystem.com/components/UI-shell-left-panel/usage/
- Google/Android — https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns
- GitLab Pajamas — https://design.gitlab.com/patterns/navigation-sidebar/
- GitHub Primer — https://primer.style/product/ui-patterns/navigation/
- Linear — https://linear.app/now/how-we-redesigned-the-linear-ui
- Linear — https://linear.app/now/behind-the-latest-design-refresh
- Shopify (medium confidence, not independently re-fetched) — https://shopify.dev/docs/api/app-home/app-bridge-web-components/app-nav

**Visual language**
- Atlassian — https://atlassian.design/foundations/typography
- Atlassian — https://www.atlassian.com/blog/how-we-build/implementing-typography-at-scale-the-journey-behind-the-screens
- Atlassian — https://atlassian.design/foundations/radius
- GitHub Primer — https://primer.style/foundations/typography/ (fetched — confirms ABSENCE of
  stated rationale, cited as a documented gap, not a source of a positive claim)
- GitHub Primer — https://primer.style/product/getting-started/foundations/color-usage/
- GitHub — https://github.blog/engineering/user-experience/unlocking-inclusive-design-how-primers-color-system-is-making-github-com-more-inclusive/
- Google/Android (Material 3) — https://developer.android.com/develop/ui/compose/designsystems/material3
- Google Developers Blog (Material shape system) — https://developers.googleblog.com/building-the-shape-system-for-material-design/
- IBM Carbon — https://v10.carbondesignsystem.com/components/data-table/usage/
- Material ripple (medium-low confidence, not independently fetched, corroborated by secondary
  write-ups only) — https://m2.material.io/develop/ios/supporting/ripple

**Explicitly excluded / could not verify with a first-party source** (per-agent research
attempts documented, not used as evidence anywhere above): Stripe typography rationale (Söhne),
Notion typography/design rationale, GitHub contribution-graph design intent, IBM Plex full
rationale text, "dark-mode reduces eye strain" as a stated design-team rationale, Vercel dashboard
nav rationale, Figma UI3 nav rationale, Carbon's sharp-corner "brand philosophy" framing.
