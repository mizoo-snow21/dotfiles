# Cognition, Choice & Mental Models

Load when: deciding how much a user can hold in mind, how many options to show at once, when to hide vs. disclose complexity, what to default, whether to design for recognition or recall, how to match conventions and existing mental models, or how to make something learnable.

Contents: Cognitive Load Fundamentals · How Many Options to Show · Progressive Disclosure, Defaults & Settings · Recognition, Recall, Memory & Attention · Conventions & Mental Models · Onboarding & First Use · Adoption, Task Continuity & Ongoing Use

## Cognitive Load Fundamentals

### Treat interface comprehension as a cognitive cost competing with the task
Minimize how much of the user's limited mental budget the interface itself consumes (navigation, layout parsing, control operation) — it draws from the same pool as the underlying task.
- Do: evaluate how much effort in a flow goes to the interface vs. the task; reduce interface-side demand.
- Ask: "How much of the user's mental effort is being spent on the interface itself rather than the underlying task?"
⟨laws1-021⟩

### Chunk related content and controls into visually distinct groups
Group related content/controls into visually distinct chunks (proximity, whitespace, dividers, color, hierarchy) rather than an undifferentiated stream — proximity alone is often enough, no border/background needed.
- When: dense pages, listings, toolbars, long forms/text, related metadata clusters.
- Do: group by relationship via proximity/whitespace/dividers/hierarchy; cluster related toolbar actions, separate functional groups with dividers.
- Avoid: walls of ungrouped content; assuming grouping needs a visible border.
- Ask: "Can a user visually identify the groups and their relationships at a glance?"
⟨laws1-016, laws1-019, laws1-020⟩

### Use structural hierarchy and formatting to tame dense text
To make a wall of text digestible, add headings/subheadings, shorten line length, add whitespace between sections, and differentiate links/keywords — structural hierarchy reduces load more reliably than cutting content.
- When: long-form content, documentation, articles.
⟨laws1-018⟩

### Prefer reducing cognitive load even at the cost of extra visual or motor steps
Cognitive load (thinking/remembering) costs more than visual load (looking/searching), which costs more than motor load (clicking/moving) — a change adding clicks or scanning but removing a cognitive burden is usually worth it. Users tolerate clicking as long as each click delivers logical progress.
- Do: favor breaking a complex decision into several simple, logical steps over one dense step.
- Avoid: treating all three load types as equally costly; optimizing purely for fewer clicks if it raises load per step.
- Exception: engagement-first products (games) may deliberately increase load for challenge/immersion.
- Trade-off: cognitive vs. visual vs. motor load — reducing one often raises another.
- Ask: "If I collapsed these steps to cut clicks, would each remaining step require noticeably more thinking?"
⟨psy1-037, psy1-038⟩

### Ask for the minimum information necessary in forms
Every additional required field costs cognitive energy and raises decision fatigue and abandonment risk — request only what's strictly necessary, and don't re-ask for what the system already knows.
- Ask: "Does the system already know this, and if so, why are we asking again?"
⟨laws1-030⟩

### Don't equate visual reduction with lower cognitive load
Reducing visible complexity helps only up to the point users can still tell what actions exist and what to do next — over-simplifying (e.g. icon-only controls with no labels) can strip out needed information and raise load instead of lowering it.
- Trade-off: visual simplicity vs. discoverability and clarity.
- Ask: "Did we remove visual complexity, or did we remove information the user needed?"
⟨laws1-028⟩

## How Many Options to Show

### Cap recall-based choice sets at about 3-4 items — but not recognition lists
Limit choices a user must actively hold in mind/compare to ~3-4; beyond that, chunk into ~3-4 groups of ~3-4. This is a recall-capacity limit, not a cap on everything visible — recognizing a visible option costs far less than recalling one from memory.
- Avoid: 8-10+ ungrouped items; the old "7±2" rule of thumb; applying this cap to an always-visible menu.
- Exception: persistently visible, recognition-based lists (e.g. site nav) don't need the cap — clear grouping keeps them scannable well past 7.
- Ask: "Is this a recall task (must be remembered) or a recognition task (stays visible)? The limit only applies to the former."
⚖ Tension: minimize choice set vs. grouped visibility → tradeoffs-decision-points.md (cog-d01)
⟨psy1-027, laws1-017⟩

### Reduce simultaneous choices when decisions are slow (Hick's Law)
Decision time grows with the number and complexity of options presented; when users hesitate or abandon, first check how many choices are shown at once and reduce them.
⟨laws1-022⟩

### Don't assume more options is better — large assortments reduce completion and conversion
More choices don't automatically raise satisfaction or conversion. Cap options for a single decision at ~3-4; beyond that, use progressive disclosure — top 3-4 first, then a next tier. (Jam study: 24 varieties drew more browsers than 6, but converted far fewer — ~3% vs. 31% — since people compare only ~3-4 items in working memory.)
- Avoid: assuming more options is inherently more appealing; giving in when users say they want "more choices" — stated preference doesn't match conversion behavior.
- Trade-off: breadth of choice (browsing draw) vs. decision speed and conversion.
⟨laws1-024, psy2-068⟩

### Break complex tasks into smaller sequential steps
Decompose an inherently complex task into a sequence of smaller decisions instead of exposing all sub-decisions on one screen, lowering per-screen load. For onboarding into a feature-rich product, use a stepwise checklist of small, low-risk actions rather than showing full capability up front — users learn best by doing in a low-risk environment.
- When: onboarding, checkout, complex settings, multi-part forms.
⟨laws1-023, laws1-026⟩

### Defer refinement choices; curate large catalogs
Don't force filtering/refinement decisions before the primary task is done — reveal filters only after the main action (e.g. search runs). When a catalog is too large to browse efficiently, surface curated subsets ("Trending," "Popular") instead of the full unranked list.
- Avoid: front-loading every possible option before the user has started.
⟨laws1-025, laws1-027⟩

## Progressive Disclosure, Defaults & Settings

### Default to essential content; put secondary complexity behind progressive disclosure
Show only primary actions/content by default; place secondary, advanced, or infrequent options behind an explicit reveal (dropdown, accordion, expandable menu). For long informational pages, give each topic a 1-2 sentence summary with a link/expansion to full detail, so skimmers and deep-divers self-select.
- Do: study what different user segments actually need and when, before designing the disclosure structure.
- Avoid: a long wall of undifferentiated content with no way to jump to what's needed.
- Ask: "Could this page show a short summary first, with detail available on demand?"
⚖ Tension: progressive disclosure vs. recognition-over-recall → tradeoffs-decision-points.md (cog-d02)
⟨laws1-062, psy1-036⟩

### Choose defaults deliberately — they're the only "setting" most users ever experience
Most users never touch settings, so a default is the de facto configuration for the majority. Balance three factors: how many users would actually want it (from data), how hard it is to change, and how discoverable the alternative is. Derive defaults from testing/usage data, prioritizing the highest-traffic ~20% of journeys (Pareto). Only pre-fill when blindly accepting it won't cause a serious, hard-to-reverse problem.
- Avoid: defaulting to something just because it's new; assuming users will adjust settings themselves; silently changing a default (e.g. to last-used value) without making it obvious.
- Ask: "Would most users actually want this as the default, or is it just convenient to ship?" / "If a user accepts this default without looking, what's the worst that happens?"
⟨psy2-018, uxp1-091, uxp1-092⟩

### Quick reference
- Organize settings by task/jobs-to-be-done rather than internal structure; hide power-user/fiddly options behind further navigation, don't lump them with everyday settings; subdivide large categories and add search to long lists — sensible defaults mean most users never need the hidden options. ⟨uxp1-072⟩

## Recognition, Recall, Memory & Attention

### Favor recognition over recall
Let users recognize a correct value from a presented set (dropdowns, autocomplete, visible lists) rather than recalling and typing it from memory. Assume forgetting is the default outcome, not a design failure to fully prevent — surface needed info directly instead of expecting users to remember it.
- When: form design; inputs with a known/finite value set; a returning user must supply info given earlier, or navigate to something used before.
- Avoid: forcing free recall when recognition would work as well; assuming a user remembers something because they were told once.
- Ask: "Could this free-text field instead be a recognition-based control?"
⟨psy1-030, psy1-034⟩

### Pair icons with text labels for important or ambiguous actions
The same icon can mean different or contradictory things across products — there's no governing standard. Don't rely on an icon alone for consequential or non-universal actions; add a text label, especially in primary navigation.
- Exception: icons with genuinely universal, unambiguous meaning may stand alone.
⟨laws1-029⟩

### Never require remembering across screens — watch for note-taking as a warning sign
Don't ask users to recall data read on one screen while completing a task on another; don't let anything interrupt a working-memory-dependent task mid-way. In testing, users jotting notes or sticky-noting is a direct signal the interface is overloading working memory.
- Do: keep any referenced value visible on the same screen or carry it forward automatically; let memory-dependent tasks finish uninterrupted; treat visible note-taking as a redesign signal.
- Ask: "Does this flow ever require holding information in the head across a screen change?" / "Did any participant write something down rather than trust the interface to remember it?"
⟨psy1-026, psy1-028⟩

### Put the most important information at the start or end, never the middle
Avoid placing the single most important point mid-sequence — put it near the start or, especially, the end (recency effect); never let an unrelated interruption follow important content, since it washes out what was just retained (suffix effect).
- Ask: "Is the single most important piece of information sitting in the middle of this sequence rather than the start or end?"
⟨psy1-032⟩

### Give users a persistent way to see where they left off
Users substantially underestimate how much they mentally drift (estimate ~10%, actually ~30%, up to 70% in low-demand tasks) — provide a persistent "current location" indicator in long flows/documents and support easy jumping between topics (e.g. hyperlinks).
- Ask: "If a user drifted away mid-task, is there an obvious way to see where they are and get back on track?"
⟨psy1-041⟩

### Design for users who won't read documentation first
Most users start using a product immediately without reading manuals, even though upfront learning would save time (the Active User Paradox) — design in-context, in-the-moment guidance (e.g. tooltips) that supports learning-by-doing instead of relying on prior reading.
- Avoid: designing help systems assuming users will read documentation before acting.
⟨laws1-061⟩

### Quick reference
- Connect new information explicitly to a schema (existing knowledge structure) the audience likely holds — research what schemas they have — and favor concrete nouns/images ("table," "chair") over abstract ones ("justice") for anything that must be remembered; things seen recall better than things merely described. ⟨psy1-029, psy1-031⟩
- Sustained focused attention lasts only ~7-10 minutes even for an engaged audience — cap tutorial/explanatory videos there, and insert a break or new stimulus for anything longer. ⟨psy1-056⟩
- True simultaneous multitasking on two attention-demanding tasks doesn't happen — it's fast task-switching, which raises errors (even hands-free calling while driving stays distracting, since the conversation itself is the cognitive load); if concurrent demand is unavoidable, simplify the interface and build in easy error correction. ⟨psy1-058⟩
- For feature-dense or expert-oriented tools, an intent-based mode — user states the desired outcome in natural language instead of operating specific controls — closes the novice/power-user learning-curve gap by shifting the "how" burden to the system. ⟨laws1-063⟩

## Conventions & Mental Models

### Reuse established conventions and idioms; adapt details, don't copy verbatim
Default to widely established conventions for common interactions instead of inventing novel behavior without reason — but adapt each pattern's details to your actual users rather than reproducing an example implementation unmodified. Users spend most of their time on other products, so what feels familiar is whatever behaves like those products.
- Do: make each component idiomatic to something users already learned elsewhere, with clear relationships between parts; identify why a pattern helps before customizing it.
- Avoid: inventing novel patterns for well-understood tasks without strong reason; diverging to appear original; copying an example pattern unmodified without checking fit.
- Trade-off: familiarity/learnability vs. novelty/differentiation.
- Ask: "Is there an established convention for this, and if so, why are we deviating from it?"
⚖ Tension: convention vs. departure → tradeoffs-decision-points.md (learn-d01)
⟨laws1-001, uxp1-090, uxp1-093, di1-001, di1-002⟩

### Roll out major redesigns gradually, with opt-in and revert
When substantially changing an established product's structure or behavior, don't switch every user simultaneously — roll out gradually and let users opt in (and revert) during a transition period. Forcing an unfamiliar mental model overnight breaks expectations and causes confusion, frustration, even flight to competitors.
- Do: offer opt-in preview, allow reverting during a transition window, collect feedback before full rollout.
- Ask: "Can users choose when to switch to the new version, or is it forced?"
⟨laws1-002⟩

### Align the product's conceptual model with users' actual (researched) mental models
Match the interface's conceptual model to target users' actual mental models — discovered through research, not assumed — and validate through testing; don't assume one uniform mental model fits your whole user base. A mismatch makes a product hard to learn and likely rejected — often because the interface just reflects the underlying database/software structure instead of a deliberate design.
- Avoid: assuming one mental model for the whole user base; designing on untested assumptions about users; letting the interface expose internal system structure as its "design."
- Ask: "Have I actually researched what mental model this audience brings, rather than assuming it?"
⟨psy1-044, psy1-045⟩

### Keep familiar elements in stable positions; honor built-up mental models of layout
Keep controls and recurring elements (e.g. search) in a consistent location — users remember where things are more than what they're labeled, and returning users act on a built-up layout model the instant a screen loads. Top/bottom list/menu positions are especially noticed, so silent changes there are especially costly. When an error occurs, place the fix exactly where attention narrows — users stop scanning the rest of the screen.
- Do: add new controls into empty space rather than reflowing existing positions; keep functions in the same location across the app; preserve the user's own arrangement; test before repositioning.
- Avoid: auto-reorganizing a user-organized area unasked; silently changing the first/last item in a list; relocating familiar controls without strong reason.
- Ask: "Does this change move anything the user already learned to find in a specific place?" / "Is the fix right where the user's narrowed attention will be?"
⟨di1-017, psy1-009⟩

### Quick reference
- When launching on a new device class or unfamiliar technology, root the interface in already-understood components (tabs, sidebars, search fields, window-like containers) so users transfer existing mental models instead of learning a whole new paradigm from zero. ⟨laws1-005⟩
- Base the appearance/behavior of controls (toggles, radio buttons, buttons) on their physical-world counterparts so their affordance is legible without explanation — form elements originated from physical control panels. ⟨laws1-006⟩

## Onboarding & First Use

### Teach product usage through demonstration, not text alone
Users reliably don't read on-screen text, so text-only instructions are largely ineffective — teach by showing (real screenshots, short videos of the actual interface). Use a first-run welcome screen focused on the new user's first task, always skippable for returning/veteran users.
- Do: show the interface being used instead of describing it; reuse familiar patterns from products users likely know; short per-step videos for high-value procedures; reserve demo videos for professional/specialized tools (unnecessary for typical consumer products).
- Avoid: relying on text explanations users won't read; forcing veteran users through a demo video.
- Trade-off: production cost of screenshots/video vs. plain-text instructions.
- Ask: "Is this teaching moment shown through demonstration, or only explained in text the user probably won't read?"
⟨uxp1-070, psy1-048⟩

### Provide multi-level help along a continuum from light to heavy
The support level any user needs varies enormously (new vs. long-returning vs. habitual; even new users differ on wanting a tutorial vs. finding tooltips annoying) — combine lighter- and heavier-weight help mechanisms on one continuum so each user gets the depth they want, using only mechanisms users already know.
- Do: brief inline annotations; tooltips (1-2 lines, ~1-2s hover delay), essential for icon-only UI; mouseover panels for medium explanations; collapsible panels for longer text; skippable intro screens/tours/videos with easy later re-access; full Help window; human support (email/web/social/phone); community forums for high-frequency software.
- Avoid: more than a brief inline annotation directly on the page — longer on-page text goes unread even by advanced users.
- Ask: "Does this range of help reach both the impatient first-time user and the one who wants deep documentation?"
⚖ Tension: guided simplicity vs. open efficiency → tradeoffs-decision-points.md (learn-d02)
⟨di1-034⟩

### Deliver a quick, ungated first success (Instant Gratification)
Give users a quick success within seconds of first opening the interface — never gate it behind registration, lengthy instructions, slow loading, or ads. An early feeling of success builds confidence and trust and increases the odds of continued use even once things get harder.
- Do: predict the first action a new user wants and make it trivial; use clear CTAs ("Type here," "Drag an image here"); creative tools show a blank canvas plus an inviting prompt and palette; task tools show the typical starting point directly.
- Avoid: requiring registration, long tutorials, slow-loading screens, or ads before the first task.
- Ask: "What is the first thing a new user will want to do, and how many steps stand between them and doing it?"
⟨di1-008⟩

### Design the first glance to be correct (satisficing / scan-first behavior)
Design the visible surface so the first plausible-looking option a scanning user notices is usually the correct one — users scan in quick glances and click the first "good enough" option rather than reading everything or evaluating every alternative (color/shape decode faster than text).
- Do: put the most-likely-needed options prominently; use clear CTAs and short plain labels matching the user's first guess; use layout/hierarchy to communicate intent; keep navigation cheap to undo a wrong guess.
- Avoid: expecting users to carefully compare every option; visual complexity that pushes novices toward random guessing.
- Exception: depends on a wrong guess being cheap to reverse (safe exploration).
- Ask: "If a user only glances at this screen, will the correct next step be the most visually obvious one?"
⟨di1-009, psy2-015⟩

### Quick reference
- For a genuinely novel product where no realistic user mental model can already match its conceptual model, invest in training material (short video, guided intro) that actively reshapes the user's mental model before real use begins — rather than redesigning the product to fit an old model that doesn't fit. ⟨psy1-046⟩

## Adoption, Task Continuity & Ongoing Use

### A better procedure won't replace an established habit without a deliberate push
Don't assume users will switch to an objectively better new way of doing something just because it's better — satisficing means they'll keep the old, less-efficient procedure unless the switch is clearly worth the effort. Make the new procedure the path of least resistance (e.g. default to it) rather than merely offering it as an alternative.
- Avoid: assuming shipping a better feature is sufficient to change established behavior.
- Ask: "Is the new way actually easier to discover and adopt than the old habit, or just theoretically better?"
⟨di1-010⟩

### Support goal changes mid-task; allow reentrance instead of trapping users
People routinely change what they're doing partway through — avoid trapping users in a flow disconnected from the rest of the app (unless deliberate), and support reentrance so an interrupted task resumes without losing progress.
- Do: preserve partially entered data; prefer non-modal dialogs users can set aside; support multiple concurrent open projects.
- Avoid: locking users into a disconnected flow without deliberate reason.
- Exception: wizards and modal panels are legitimate deliberate constraints.
- Ask: "If the user leaves this flow right now, can they resume it later without losing progress?"
⚖ Tension: wizard vs. settings-editor → tradeoffs-decision-points.md (struct-d01)
⟨di1-011⟩

### Defer non-essential choices; keep required upfront fields minimal
Don't force users to answer non-essential questions before proceeding — let them skip optional decisions and return later, keeping truly-required upfront fields as few as possible. Forcing answers users aren't ready for causes frustration or abandonment, especially in onboarding/registration ahead of any actual value.
- Do: mark required fields clearly and minimize their count; separate a few essential choices from a longer secondary list, hidden by default; supply sensible visible/editable defaults; let users experience value before registration, or offer low-friction account creation from data already entered.
- Avoid: a long mandatory registration form before any value delivered; requiring answers users may not yet have enough information to give.
- Ask: "Which of these upfront fields are truly required to proceed, and which could be deferred or defaulted?"
⟨di1-012⟩

### Quick reference
- Support creative work as small, revisable steps (build, check, test, adjust, sometimes discard and redo) rather than a top-down single pass — keep the feedback loop between a change and seeing its result as short as possible, since long delays (e.g. slow compiles) break flow state. ⟨di1-013⟩
- For content used in short idle moments (commute, waiting in line), make entry near-instant — no setup, minimal load, persisted login — and resume exactly where the user left off; slow loading is even more fatal here given the user's tiny patience budget. ⟨di1-016⟩
- Keep folders, naming, ordering, and window/file state user-controlled rather than auto-managed — users deliberately leave things in a place or open state as a prospective-memory cue for something they intend to do later, and auto-tidying defeats that. ⟨di1-018⟩
- Don't assume users understand or want a filesystem mental model — many capable users have none and don't need one; explicitly show how and where work is stored/retrieved within the product's own model, or hide filesystem complexity entirely. ⟨uxp1-095⟩
- When a user or stakeholder requests a specific feature or form, ask "why" repeatedly until reaching the actual underlying goal, then design for that goal — including removing the requested UI entirely if reachable without it. ⟨di1-004⟩
