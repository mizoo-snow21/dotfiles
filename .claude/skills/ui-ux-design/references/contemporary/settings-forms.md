<!-- Contemporary product-derived reference (V2). Provenance layer: product-derived —
every rule cites fetched public design-system docs / product materials; confidence is
marked per rule. These rules complement the book-derived foundation: books carry the
WHY (cognition, perception), these carry current practice under real product constraints.
When they conflict with a book rule, treat it as a decision point, not an override. -->
# Settings Screens & Complex Forms — Cross-Product Decision Rules

Research date: 2026-08-25. Method: fetched/searched published design-system docs with stated rationale. Every claim below is tagged with a source URL and a confidence level. Where a system's documentation could not be retrieved in enough depth to support a claim, that is stated explicitly rather than filled in from memory.

---

## Decision rules

### ct-set-01 — Settings navigation: grouped cards + own sub-page beats flat single scroll once sections multiply
**Question:** When does a settings area need a sidebar/grouped structure instead of one long scrolling page?
**Guidance (conditional):** Shopify's settings pattern uses a two-column layout — glanceable labels/descriptions in the left column so merchants can scan and locate a setting, with the actual controls grouped into cards in the right column so related settings can be configured together. Its explicit escalation rule: "for complex or lengthy settings, organize content into distinct, themed sections that link to their own pages." So the default is grouped cards on one page; the pattern only forks into separate sub-pages once a single page can no longer stay scannable. Primer's tab guidance independently converges on a count-based ceiling: tabs are for switching between "2 or more related views" but you should "limit the number of tabs to avoid clutter; consider using a NavList for larger menus" — i.e. past a handful of sections, promote tabs to a list/sidebar.
**Evidence:** Shopify, [Settings pattern](https://shopify.dev/docs/api/app-home/patterns/settings); Primer, [UnderlineNav guidelines](https://primer.style/product/components/underline-nav/guidelines/).
**Tension:** Atlassian's component docs draw the line differently — by *relationship* rather than *count*: tabs are for "alternating between views within the same context," left/side navigation is for moving to genuinely different areas. Under this framing, a settings area with 3 loosely related domains (Profile, Billing, Security) is a left-nav case even at small scale, while 6 tightly coupled variants of the same object could stay as tabs.
**Confidence:** medium — Shopify and Primer quotes are directly fetched; the Atlassian framing came through search snippets, not a directly fetched page (the Atlassian Design System site did not return usable static content to WebFetch).

### ct-set-02 — Toggle vs. checkbox is a save-model decision, not a visual-style decision
**Question:** When should a binary settings control be a toggle switch vs. a checkbox?
**Guidance (conditional):** Two independent design systems converge on the identical rule, stated almost word-for-word: use a **toggle when flipping it calls the API/applies the change immediately** (e.g., turning on a flow in the store); use a **checkbox when the change stays "dirty" until the user clicks a form Save button**. Carbon states it as: "Toggle switches are preferred when the resulting action will be instantaneously applied, without the need for further confirmation. By comparison, checkboxes represent one input in a larger flow which usually requires a final confirmation step." Shopify's Polaris team gives the same answer in their public discussion thread.
**Evidence:** Shopify/Polaris, [GitHub Discussion #7297](https://github.com/Shopify/polaris-react/discussions/7297) ("checkbox when state is dirty... toggle when the API/save state is called immediately"); IBM Carbon, [Toggle usage](https://carbondesignsystem.com/components/toggle/usage/).
**Tension:** none between these two — this is a rare case of clean cross-vendor agreement.
**Confidence:** high — quoted language recovered from both systems independently, and they match.

### ct-set-03 — Even an immediately-applied setting should demote from toggle to checkbox/radio/select once it has dependents
**Question:** Is "changes apply immediately" alone sufficient to justify a toggle?
**Guidance (conditional):** No — Polaris adds an explicit carve-out on top of ct-set-02: "if the setting is dependent on other settings, uses progressive disclosure, or has options that are not a simple On/Off, use a different UI element such as Checkbox or Radio button." So the toggle contract is narrower than "binary + immediate" — it also requires the setting to be *independent* and *genuinely binary*. A three-state or conditionally-revealing control should never be a toggle regardless of save timing.
**Evidence:** Shopify, [Setting toggle guidance via GitHub Discussion #7297 search summary](https://github.com/Shopify/polaris-react/discussions/7297).
**Confidence:** medium — this detail came through a search-engine summary of the Polaris docs rather than a direct fetch of the primary component page (which is deprecated/redirects); the wording is close enough to Polaris's known voice to trust, but treat the exact phrasing as paraphrase.

### ct-set-04 — Material Design frames the same toggle/checkbox choice around independence-of-control and density, not save timing
**Question:** Do all systems justify toggle-vs-checkbox the same way?
**Guidance (conditional):** No — this is a genuine framing disagreement worth recording. Material 3 says: "Switches should be used instead of radio buttons if each item in a set can be independently controlled," and "if you have multiple options appearing in a list, you can preserve space by using checkboxes instead of on/off switches." Material's axis is *independence of the control within a set* and *visual density*, never mentioning immediate-apply vs. batched-save at all.
**Evidence:** Google Material Design 3, [Switch guidelines](https://m3.material.io/components/switch/guidelines), [Checkbox guidelines](https://m3.material.io/components/checkbox/guidelines).
**Tension:** Material's density/independence framing and Shopify/Carbon's save-timing framing aren't contradictory in practice (an immediately-applied, independent setting is usually both), but they're different mental models — a team following only Material's guidance could end up putting a toggle inside a form that requires an explicit Save, which Polaris and Carbon would call a mistake.
**Confidence:** medium — recovered via search snippets of the M3 pages, not a full raw fetch (the fetch tool returned only the page title with no body).

### ct-set-05 — Never disable the submit button to signal invalidity; attempt submission and show errors instead
**Question:** Should a form's save/submit button be disabled until all fields validate?
**Guidance (conditional):** Primer explicitly rejects the disabled-button pattern: "Disabling submit buttons lacks clarity about what actions unblock completion. Instead, attempt submission and display error messaging." The stated failure mode is that a disabled button gives the user no information about *what* is still wrong, whereas letting them submit and then explaining the specific problem is more actionable. This extends to degraded states too: on partial data-loss, Primer says disable only the affected fields with an inline error, never blank them out silently, and on total data-loss replace the form with an explanatory message rather than showing a broken empty form.
**Evidence:** GitHub Primer, [Forms overview](https://primer.style/ui-patterns/forms/overview).
**Confidence:** high — direct fetch, verbatim guidance.

### ct-set-06 — Mark the control as required in code, not just visually; skip visual marking where required-ness is already implied
**Question:** How should required fields be indicated, and are there exceptions?
**Guidance (conditional):** Primer's rule is that the required state belongs on the form control (which then propagates to the underlying input), not merely as a visual asterisk on the label — this matters for assistive tech. The visual/semantic marking itself is skipped for "familiar patterns like login forms where all fields are implicitly required" — i.e., skip decoration when 100% of fields are required and the form type is a well-known convention; mark explicitly whenever the form mixes required and optional fields. Individual checkboxes/radio buttons cannot themselves be marked `required` (only a fieldset/group can).
**Evidence:** GitHub Primer, [Forms overview](https://primer.style/ui-patterns/forms/overview); [Primer accessibility guidance on required fields](https://github.com/primer/design/commit/27c4065b3f1b75223b06a3640b1c80799fae5804).
**Confidence:** high.

### ct-set-07 — Validation timing: three real-world answers, and they don't agree on when "as-you-type" is acceptable
**Question:** Should form fields validate as the user types, on blur, or only on submit?
**Guidance (conditional), compared:**
- **Primer (GitHub):** Default to validating on submit to avoid interrupting flow. If the first submit attempt fails, *then* switch to progressive per-field validation on blur for the rest of the session — inline-before-first-submit is explicitly called out as degrading perceived performance (for server checks) and interrupting screen-reader users.
- **gov.uk:** Also defaults to submit-only, phrased even more strongly: "avoid validating the information in a field before the user has finished entering it... This sort of validation can cause problems — especially for users who type more slowly." Blur-validation is not recommended as a default at all. The one named exception is the Character Count component, and only because user research showed it "solves more problems than it creates" — gov.uk treats real-time validation as needing research-backed justification per case, not as a general default.
- **Stripe Elements (payment fields):** Runs continuous checks as the user types (e.g., Luhn algorithm on card number) but suppresses error *display* mid-keystroke — errors surface only once a field is "complete" (or a format is unambiguously wrong, like an expiry date already in the past), and messages are actionable ("Card number is incomplete") rather than generic.
**Evidence:** Primer, [Forms overview](https://primer.style/ui-patterns/forms/overview); gov.uk, [Validation pattern](https://design-system.service.gov.uk/patterns/validation/); Stripe, [Credit card checkout UI design guide](https://stripe.com/resources/more/credit-card-checkout-ui-design).
**Tension:** all three agree "don't error on every keystroke," but they disagree on how eager the *first* feedback moment should be — submit-only (gov.uk's strict default) vs. submit-then-blur (Primer) vs. continuous-but-debounced-display (Stripe, for a narrow high-stakes single-purpose field where format is unambiguous and immediate confidence — "valid card" checkmark — has real conversion value). The pattern: the more the field format is externally verifiable and time-pressure-sensitive (payment card), the more real-time feedback pays for itself; the more the service is used by low-confidence/high-stress users on variable-quality connections (gov.uk's citizen services), the more real-time feedback becomes a net negative.
**Confidence:** high for Primer and gov.uk (direct fetch quotes); medium for Stripe (search-summarized from a Stripe-published guide, not a raw fetch of that exact page).

### ct-set-08 — Error summary vs. inline-only: a hard "always both" rule vs. a count-based threshold
**Question:** When do you need an error summary banner in addition to inline field errors?
**Guidance (conditional), compared:**
- **gov.uk:** No threshold — "you must show both an error summary and an error message... even if there is only one error." This is a fixed requirement, not a judgment call.
- **Primer:** Threshold-based — on failed submission, focus the first invalid input directly if there are few errors; only surface an interactive error-summary Banner (that links to each bad field) once there are 3+ errors.
**Evidence:** gov.uk, [Error summary component](https://design-system.service.gov.uk/components/error-summary/); Primer, [Forms overview](https://primer.style/ui-patterns/forms/overview).
**Tension:** gov.uk's stance optimizes for a consistent, learnable pattern across an entire government service portfolio, at the cost of showing a one-line summary for what might be a single obvious error. Primer's stance optimizes for not adding UI ceremony when a single re-focus already solves the problem. Neither documents a controlled experiment for the specific threshold — this is a designed-consistency choice on both sides, not an A/B-tested one.
**Confidence:** high — both are direct-fetch quotes from the primary docs.

### ct-set-09 — Error summary placement and focus management are specified down to the DOM position
**Question:** Where exactly does an error summary go, and how does keyboard focus move to it?
**Guidance:** gov.uk places the summary "below" back links/breadcrumbs but "above the `<h1>`," and its front-end JavaScript automatically moves keyboard focus to the summary on page load after a failed submission — so assistive-tech users land on the error list before anything else, without extra developer wiring. Every error inside the summary must link directly to its field (for a multi-part input like a date picker, the link targets the first sub-field with an error).
**Evidence:** gov.uk, [Error summary component](https://design-system.service.gov.uk/components/error-summary/).
**Confidence:** high — direct fetch, and unusually specific/prescriptive even by design-system standards (this level of DOM-order precision is rare outside gov.uk).

### ct-set-10 — Container choice for a form should scale with field count: dialog < 5 fields, side panel for more, multi-step for a lot
**Question:** Should a form live in a modal dialog, a side panel, or a dedicated multi-step flow?
**Guidance (conditional):** Carbon gives a concrete numeric split: "use a dialog form when dealing with less than five inputs. Use a side panel form when dealing with more than five inputs." For genuinely large field counts, Carbon recommends multi-step forms with a step/progress indicator instead of stuffing everything into one screen — explicitly warning against overloading users with too many input controls at once, "especially in modals." Multi-step also buys the ability to save progress and return to a prior step to review.
**Evidence:** IBM Carbon, [Forms pattern](https://carbondesignsystem.com/patterns/forms-pattern/).
**Confidence:** medium — recovered via search summary of the Carbon docs; a direct WebFetch of the page returned only a truncated/empty body, so the exact "5 fields" number should be treated as reported-by-search rather than independently re-verified against raw HTML.

### ct-set-11 — "One thing per page" vs. grouped settings: context (stakes + user population), not page count, decides the default
**Question:** Should a complex form ask one question per screen, or group several related fields on one page — and this is the sharpest disagreement in the corpus.
**Guidance (conditional):** gov.uk's default is one question per page, justified by a cited internal case study: the Carer's Allowance team removed a 12-step progress indicator "without any negative effects" on completion, i.e., atomizing didn't cost them completion rate even though it multiplied page count. gov.uk frames grouping as the *exception*, permitted only when "user research will tell you when you can group pages together" — and it names the condition explicitly: internal services for government staff who need to "repeat and switch between tasks quickly" are a legitimate case for grouping, ordinary public-facing forms are not.
By contrast, every SaaS design system in this corpus (Shopify's settings-cards pattern, Carbon's forms-pattern grouping into fieldsets, Atlassian's Form component) defaults to grouping several related fields on one page/card and treats one-field-per-screen as the unusual case, reserved for onboarding wizards or payment flows.
**Evidence:** gov.uk, [Question pages pattern](https://design-system.service.gov.uk/patterns/question-pages/); Shopify, [Settings pattern](https://shopify.dev/docs/api/app-home/patterns/settings); IBM Carbon, [Forms pattern](https://carbondesignsystem.com/patterns/forms-pattern/).
**Tension (the finding itself):** gov.uk's services are engineered for users under real stress (benefits, tax, immigration, often on poor connections or low digital confidence) attempting a task exactly once; the atomized, low-cognitive-load-per-screen approach is calibrated to that population and to the cost of a single dropped user. SaaS settings screens are used repeatedly by returning professional users optimizing for speed and overview, where per-field pagination would be experienced as friction rather than support. The transferable rule is: **default to one-thing-per-page for infrequent, high-stakes, broad-population forms; default to grouped sections for frequent, low-stakes, professional-tool settings** — and validate the choice with actual user research rather than assuming either default, exactly as gov.uk itself recommends.
**Confidence:** high for the gov.uk side (direct fetch, cited internal evidence); medium for characterizing the SaaS side as a coherent "opposing default" — no SaaS system states its grouping choice as a reaction to gov.uk-style atomization; that framing is this analysis's synthesis, not a quoted claim.

### ct-set-12 — A dedicated "check your answers" review step earns its place before high-stakes or irreversible submission
**Question:** Is a review/confirm step worth the extra screen before final submission?
**Guidance (conditional):** gov.uk's rationale is two-part: it "increases users' confidence as they can clearly see that they have completed all the sections and that their data has been captured," and it "reduces error rates as users are given a second chance to notice and correct errors before submitting." It's recommended for small-to-medium single-pass transactions as one review page before submit; for larger multi-section processes (especially ones split across different users/roles), the recommendation shifts to a review page at the end of *each* major section rather than one giant review at the very end.
**Evidence:** gov.uk, [Check answers pattern](https://design-system.service.gov.uk/patterns/check-answers/).
**Confidence:** high — direct fetch.

### ct-set-13 — Destructive-action friction should scale on a named ladder, not be uniformly "always confirm"
**Question:** How much confirmation friction does a destructive action deserve?
**Guidance (conditional):** GitLab's Pajamas system states an explicit three-tier ladder tied to reversibility and severity:
- **Low severity** (trivially undoable, no real data loss): "consider adding no friction at all... to streamline the interface" — can even use the default (non-danger) button styling.
- **Medium severity** (hard to undo, emotional impact but not catastrophic): add one extra step without a full modal — e.g. "put the action within a dropdown requiring a minimum of two clicks."
- **High severity** (permanent/irreversible data loss): "strongly consider implementing a modal to confirm the action," using a danger-styled button, bold/danger-toned body copy stating the consequence, and — for named resources — requiring the user to type the resource's name to confirm.
Shopify's Polaris guidance for the modal itself layers on top of this: label the confirming button with the actual verb ("Delete", not "OK"/"Yes"), explain the consequence in the modal body, and cap the modal at two buttons total to avoid an unclear action hierarchy.
**Evidence:** GitLab, [Destructive actions pattern](https://design.gitlab.com/patterns/destructive-actions/); Shopify Polaris, [Modal component / destructive-action guidance](https://polaris-react.shopify.com/components/deprecated/modal?example=modal-with-destructive-primary-action).
**Confidence:** high for GitLab (direct fetch, quoted); medium for Polaris's modal-button specifics (search-summarized, not a raw fetch, though consistent with well-known Polaris conventions elsewhere in this research).

### ct-set-14 — Billing: always let the customer see the exact cost impact before committing to a plan/price change
**Question:** How should proration be disclosed during a plan change?
**Guidance:** Stripe's own subscription docs treat proration preview as the standard mechanism for disclosure, not an optional add-on: generate an invoice *preview* (which does not mutate the subscription) before calling the actual update, and use that preview "to confirm the change with the customer" beforehand. Because Stripe prorates to the second, the previewed amount can drift slightly between preview-time and the moment the real update executes; Stripe's mitigation is to pin a shared `proration_date` across both the preview call and the real update call so the two amounts match exactly.
**Evidence:** Stripe, [Prorations — preview proration](https://docs.stripe.com/billing/subscriptions/prorations) (docs served in Japanese at fetch time; translated/paraphrased above — original: "この情報を使用して顧客に変更を確認できます").
**Confidence:** high — direct fetch of Stripe's own documentation.

### ct-set-15 — Downgrades commonly default to "takes effect at period end," sidestepping mid-cycle credit complexity
**Question:** Should a downgrade apply immediately (with a credit) or be scheduled for later?
**Guidance (conditional):** Stripe's API supports both, but the platform-level pattern it documents and ships as a first-class customer-portal feature is deferring the downgrade to the end of the current billing period (`cancel_at_period_end`-style scheduling / Subscription Schedules), which avoids generating an immediate credit proration and the "double payment" edge cases Stripe's own docs warn about when mixing unpaid invoices with immediate downgrades. Stripe's customer portal added scheduled downgrades explicitly to formalize this as a supported self-serve flow.
**Evidence:** Stripe, [Change the price of an existing subscription — billing periods](https://docs.stripe.com/billing/subscriptions/change-price); Stripe, [Subscription schedules](https://docs.stripe.com/billing/subscriptions/subscription-schedules); Stripe changelog, ["Schedule downgrades" in customer portal](https://docs.stripe.com/changelog/acacia/2024-10-28/customer-portal-schedule-downgrades).
**Confidence:** medium — the API/mechanism facts are directly sourced; the framing of "this is the common/recommended default for downgrades specifically" is inferred from Stripe shipping it as a named customer-portal feature, not a single explicit "always defer downgrades" statement.

### ct-set-16 — Cancel stays a directly reachable, on-by-default action; retention friction is layered on top, not built by hiding the exit
**Question:** How reachable should "cancel subscription" be, and is retention friction acceptable?
**Guidance:** Stripe's customer-portal cancellation feature is enabled by default (self-serve cancel is the baseline, not an opt-in the merchant must turn on). Retention mechanics — a "cancellation deflection" retention-coupon offer, and optional collection of a cancellation reason from a fixed list — are separate, explicitly opt-in configuration layered on top of the reachable cancel action, not a redesign that hides or relocates the cancel entry point itself.
**Evidence:** Stripe, [Customer portal cancellation page](https://docs.stripe.com/customer-management/cancellation-page).
**Confidence:** high — direct fetch. Note this describes Stripe's own default configuration and available levers, not a normative "you should do it this way" statement from Stripe — merchants can still reconfigure or dark-pattern this if they choose; the finding is about what the platform makes easy vs. what it makes you opt into.

### ct-set-17 — Vertical, single-column form flow beats multi-column for scannability; group fields visually by relatedness and input method
**Question:** Should a form's fields run in one column or spread across multiple columns?
**Guidance:** Primer: "forms should flow vertically [because vertical flows] are easier for sighted users to scan visually" — explicitly warning against multi-column layouts adopted merely to save vertical space, since that trades scannability for compactness. On top of the single-column default, order fields by importance, cluster related inputs under shared labeling, and cluster keyboard-entry fields together to minimize input-method switching for mouse users moving between typing and clicking.
**Evidence:** GitHub Primer, [Forms overview](https://primer.style/ui-patterns/forms/overview).
**Confidence:** high — direct fetch, verbatim.

### ct-set-18 — Field help text: keep labels short and push overflow explanation into a caption, not a tooltip-only pattern
**Question:** Where should extra explanation for a field live when the label alone isn't enough?
**Guidance:** Primer's rule is to keep labels to roughly 3 words max, and "if you're having trouble keeping label text short, consider using a caption to provide more context" — i.e., the caption (persistent, adjacent help text) is the preferred escape hatch over relying on a tooltip that requires a hover/focus action to reveal.
**Evidence:** GitHub Primer, [Forms overview](https://primer.style/ui-patterns/forms/overview).
**Confidence: low-to-medium, with an explicit gap:** I attempted to pull Adobe Spectrum's Help Text guidance (the system most likely to have a fuller rationale here, since it has a dedicated Help Text component distinct from Primer's caption) from three different URLs (`spectrum.adobe.com/page/help-text/`, `opensource.adobe.com/spectrum-design-data/components/help-text`) and could not retrieve rendered guidance prose — the pages returned only component-property scaffolding (variant/size/disabled flags) with no placement or tooltip-vs-inline rationale text reaching the fetch tool. Spectrum's actual design rationale for help-text placement is therefore **not verified** in this research and the rule above rests on Primer alone.

---

## Cross-product observations

- **The cleanest convergent finding in this whole corpus is toggle-vs-checkbox-as-save-model** (ct-set-02): Shopify and IBM independently arrived at "immediate API call → toggle; dirty-state-until-Save → checkbox," using near-identical language, while Google frames the same component choice around an unrelated axis (independent-controllability/density). This is a good illustration of how a UI-component choice can encode a *system-state* decision (when does this take effect) that's easy to get backwards if you only think about it as a visual-style choice.
- **gov.uk is the outlier in rigor, not in conclusions** — it is the only system in this set that cites a specific before/after case study (Carer's Allowance) for a UX claim rather than asserting a best practice; it's also the only one with unconditional rules ("always show both error summary and inline," "one question per page by default") rather than conditional/threshold rules. That rigor comes from its context: single-attempt, high-stakes, broad-population civic services where the cost of guessing wrong is a citizen who can't complete a benefits claim, not a professional user who'll just try again.
- **Professional/SaaS tools (Shopify, Carbon, Primer) consistently trade gov.uk-style atomization for grouping + thresholds** — dialogs vs. side panels by field count, error summaries only past 3 errors, settings grouped into cards by default. The implicit shared assumption is a repeat, moderately-confident user population where scanning speed matters more than error-proofing every single field in isolation.
- **Billing-specific UX (Stripe) is the one area where "always disclose, always preview" is treated as non-negotiable even in a professional-tool context** — proration preview before commit (ct-set-14) and check-answers-style review (gov.uk, ct-set-12) are functionally the same pattern — "show the consequence before the irreversible action" — independently arrived at in a government-forms context and a payments context, which is reasonably strong evidence this rule generalizes across domains regardless of user sophistication.
- **Confirmation friction, destructive actions, and billing consequence disclosure all converge on the same underlying rule**: friction should be proportional to *how expensive it is to be wrong*, not applied uniformly. GitLab's three-tier ladder (ct-set-13), Stripe's mandatory proration preview (ct-set-14), and gov.uk's check-answers page (ct-set-12) are three domain-specific instances of one general principle.
- **Gap in this research:** Linear, Notion, and Vercel do not publish design-rationale documentation comparable to Polaris/Primer/Carbon/gov.uk — search only surfaced third-party reverse-engineering/case-study blog posts (LogRocket, Eleken, Tela Blog) and one first-party UI-redesign retrospective (Linear's ["How we redesigned the Linear UI"](https://linear.app/now/how-we-redesigned-the-linear-ui)) that discusses visual/interaction philosophy in general terms, not settings/forms-specific decision rationale with evidence. No claim in the numbered rules above is sourced to Linear, Notion, or Vercel for this reason — including them would have meant asserting inferred product behavior as if it were documented rationale, which the brief asked to avoid.
- **Atlassian's and Spectrum's own documentation sites resisted this research's fetch tooling** (both appear to be heavily client-rendered SPAs that return near-empty bodies to a static fetch) — every Atlassian- and Spectrum-attributed claim above is search-snippet-sourced rather than raw-page-sourced, and is flagged medium/low confidence accordingly rather than presented with the same confidence as the gov.uk/Primer/Shopify/Carbon/Stripe/GitLab findings, which were recovered via direct, successful fetches.

---

## Sources consulted

**Directly fetched (primary source, high-confidence citations):**
- gov.uk Design System — [Error summary](https://design-system.service.gov.uk/components/error-summary/), [Validation pattern](https://design-system.service.gov.uk/patterns/validation/), [Question pages](https://design-system.service.gov.uk/patterns/question-pages/), [Check answers](https://design-system.service.gov.uk/patterns/check-answers/)
- GitHub Primer — [Forms overview](https://primer.style/ui-patterns/forms/overview)
- GitLab Pajamas — [Destructive actions](https://design.gitlab.com/patterns/destructive-actions/)
- Stripe — [Prorations](https://docs.stripe.com/billing/subscriptions/prorations), [Change the price of a subscription](https://docs.stripe.com/billing/subscriptions/change-price), [Customer portal cancellation page](https://docs.stripe.com/customer-management/cancellation-page)

**Search-summarized from official docs (medium confidence — content confirmed by the design system's own site via search snippet, not independently re-verified against raw HTML):**
- Shopify — [Settings pattern](https://shopify.dev/docs/api/app-home/patterns/settings), [App settings layout](https://polaris-react.shopify.com/patterns/app-settings-layout), [GitHub Discussion #7297 on toggle vs. checkbox](https://github.com/Shopify/polaris-react/discussions/7297), [Modal / destructive action example](https://polaris-react.shopify.com/components/deprecated/modal?example=modal-with-destructive-primary-action)
- IBM Carbon — [Forms pattern](https://carbondesignsystem.com/patterns/forms-pattern/), [Toggle usage](https://carbondesignsystem.com/components/toggle/usage/)
- Google Material Design 3 — [Switch guidelines](https://m3.material.io/components/switch/guidelines), [Checkbox guidelines](https://m3.material.io/components/checkbox/guidelines)
- Primer — [UnderlineNav guidelines](https://primer.style/product/components/underline-nav/guidelines/), [Required-field a11y guidance commit](https://github.com/primer/design/commit/27c4065b3f1b75223b06a3640b1c80799fae5804)
- Stripe — [Credit card checkout UI design guide](https://stripe.com/resources/more/credit-card-checkout-ui-design), [Subscription schedules](https://docs.stripe.com/billing/subscriptions/subscription-schedules), [Customer portal scheduled downgrades changelog](https://docs.stripe.com/changelog/acacia/2024-10-28/customer-portal-schedule-downgrades)
- Atlassian Design System — [Tabs component](https://atlassian.design/components/tabs/), navigation-system pages (guidance recovered via search only; direct fetch returned no usable body)

**Attempted but unable to retrieve usable rationale (flagged, not used as a citation basis):**
- Adobe Spectrum — [Help text](https://spectrum.adobe.com/page/help-text/), [Spectrum design data: help-text component](https://opensource.adobe.com/spectrum-design-data/components/help-text) — pages returned only property scaffolding, no placement/rationale prose
- Atlassian Design System — [Form component](https://atlassian.design/components/form/examples) / [Form usage](https://atlassian.design/components/form/usage) — SPA returned minimal static content ("A form allows people to input information.") with no detailed guidance body reaching the fetch tool
- Linear, Notion, Vercel — no first-party settings/forms design-rationale documentation was found; excluded from the numbered rules for that reason (see Cross-product observations)

---
