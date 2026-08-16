# Visual Hierarchy, Layout & Spacing

Load when: building emphasis/de-emphasis and visual weight, applying Gestalt grouping (proximity/similarity/alignment), choosing layout patterns and grids, setting spacing systems and whitespace-vs-density, handling responsive behavior, or shaping visual flow and scanning.

Contents: Establishing Hierarchy & Emphasis · Gestalt Grouping, Alignment & Spacing · Perception, Attention & Visual Flow · Chunking Content (Tabs/Accordion/Collapsible/Movable Panels) · Page-Level Layout Patterns · Spacing, Sizing & Responsive Behavior · Action Hierarchy (Buttons)

## Establishing Hierarchy & Emphasis

### Establish and communicate a clear hierarchy of importance
Rank every element on a screen by importance; make the single most important thing most visually prominent and let everything else recede in proportion. Style each content type (titles, subtitles, lists) so its visual form matches its role.
- Avoid: giving every element roughly the same visual weight by default.
- Ask: "Looking at this screen, is it immediately obvious what matters most?"
⟨di2-020, rui1-013⟩

### Stack multiple emphasis cues for short or small important elements
For headlines, taglines, CTAs, or small-but-important controls, combine ≥2 emphasis techniques (size, color/contrast, weight, whitespace/background, position, density, repetition-rhythm) rather than one alone — cues reinforce each other.
- Do: place small critical items near top/left/top-right; pair strong contrast with generous whitespace; treat density/background/repetition as deliberate tools, not leftover styling.
⟨di2-021, di2-022⟩

### Use visual contrast deliberately and sparingly (Von Restorff effect)
Contrast (color, size, shape, position, motion) directs attention — but emphasis is relative: emphasizing too many elements at once makes them compete and cancel out.
- Avoid: adding contrast without an attention-directing purpose; emphasizing many elements simultaneously.
- Ask: "If everything on this screen is emphasized, what actually stands out?"
⟨laws1-050, laws1-051⟩

### Emphasize an element by de-emphasizing what competes with it
Hierarchy is relative — prominence depends on the weight of everything around an element, not just its own styling. If direct emphasis on a target stops working, reduce the weight of what's competing with it instead.
- Do: lower contrast/weight of competing elements; strip unnecessary background/styling that competes with the main content.
⟨rui1-017⟩

### Build text hierarchy with weight and color, not size alone
Make primary text bolder rather than bigger; make secondary text a softer color rather than smaller. Keep the system small — ≤2-3 text colors (dark primary, grey secondary, lighter grey tertiary), ~2 font weights (400-500 normal, 600-700 emphasis) — and avoid weights under 400 for UI-sized text.
- Avoid: font size as the only hierarchy lever; using a lighter weight to de-emphasize small text.
- Exception: light/thin weights can work for large headings.
⟨rui1-014, rui1-015⟩

### Drop, fold, or de-emphasize data labels based on redundancy
Check whether a value's own format (email, phone, currency) or context already identifies it, and drop the label if so. If it can't be dropped, fold its meaning into the value's phrasing ("12 left in stock"). If a label remains, de-emphasize it and let the value carry emphasis.
- Exception: on information-dense reference pages (spec sheets) where users scan for the label itself, reverse it — emphasize the label, only slightly de-emphasize the value.
- Ask: "Does this value's format or context already tell the user what it is, without a label?"
⟨rui1-018, rui1-019, rui1-020⟩

### Decouple visual hierarchy from HTML heading semantics
Pick h1-h6 for semantic/accessibility correctness, but size it purely by the visual hierarchy the design needs — including styling a heading small or visually hidden when the content beneath it should carry the real emphasis.
- Avoid: assuming an h1 must render large just because it's an h1.
- Exception: long-form/document content (articles, docs) where default heading-size progression is often appropriate.
- Ask: "Is this title acting like a heading, or like a label for the content beneath it?"
⟨rui1-021⟩

### Quick reference
- Visual prominence doesn't guarantee attention: users find things by learned meaning and tune out content resembling ads ("banner blindness") even when important — don't style important non-ad content in ad-like patterns, especially near ad zones. ⟨di2-023, laws1-052⟩
- To make one element pop from a set, vary a single visual feature (usually color or shape); if two must vary, pair color with orientation — multi-dimensional variation slows recognition instead of speeding it. ⟨psy1-007⟩
- On colored backgrounds, de-emphasize text by hand-picking a same-hue color and tuning saturation/lightness, not generic grey or reduced-opacity white — grey doesn't cut contrast on color the way it does on white, and washed-out white reads as disabled. ⟨rui1-016⟩
- Weight and contrast are interchangeable emphasis levers: lower contrast (not shape) to de-emphasize a heavy element like a solid icon; increase weight (not contrast) to reinforce a subtle element (e.g. a thin border) when darkening would look harsh. ⟨rui1-022, rui1-023⟩

## Gestalt Grouping, Alignment & Spacing

### Apply the four Gestalt grouping laws deliberately
Use proximity (place related items close), similarity (matching shape/size/color/orientation for same-kind items), continuity (align elements so edges form an implied line/curve), and closure (a cluster reads as one enclosed shape) deliberately. Combine more than one factor when a grouping needs to read strongly.
- Ask: "Which Gestalt factor(s) are doing the work here? Would combining another make it read more clearly?"
⟨di2-024⟩

### Use proximity and similarity to show grouping, peer sets, and special items
Place related items close, unrelated items with deliberate distance; give same-kind items consistent, distinctive styling so they read as peers. To mark one item special within a uniform set, shift exactly one visual trait (e.g. background color) rather than restyling it entirely.
- Avoid: restyling a "special" item so heavily it no longer reads as part of the family.
⟨di2-025⟩

### Use spacing to disambiguate grouping; keep inter-group spacing larger than intra-group spacing
Use spacing/proximity as the primary grouping tool before lines, boxes, or dividers. When a group relies on proximity alone (no border/background), make spacing around the whole group visibly larger than spacing between elements inside it.
- Avoid: near-equal gaps between related and unrelated elements (e.g. a caption misread as belonging to the wrong photo, data entered in the wrong field).
- Trade-off: visual noise from added dividers vs. relying on spacing alone.
- Ask: "Is the space around this group bigger than the space within it?"
⟨psy1-014, rui1-037⟩

### Use alignment, indentation, and containment to show order and nesting
Align a list of similar items pixel-precisely along a shared line/column to show it's an ordered, scannable set (continuity). Indent/shrink text under a parent element to mark it as a modifier. Use containment (box, background block, tabbed module, accordion, whitespace-bounded group) or indentation to signal parent-child relationships (closure).
- Avoid: letting alignment drift by even a few pixels in a list meant to read as ordered.
⟨di2-026⟩

### Quick reference
- Users perceive an interpreted, brain-constructed view, not raw pixels (e.g. illusory contours like the Kanizsa triangle) — shape grouping and emphasis deliberately through color and shape, and use shadow/depth to make elements read as closer together or farther apart. ⟨psy1-001⟩

## Perception, Attention & Visual Flow

### Design very few focal points connected by an implied line
Design each page with only a handful of genuine focal points, connected along an implied line so the eye moves from strongest to weakest. A strong focal point can — and often should — override the default top-to-bottom, left-to-right reading order.
- Do: place the primary CTA directly in the flow below the text you most want read (if reading is a precondition), or separate it with whitespace if not; keep form controls in one continuous flow ending in a clear done action.
- Avoid: scattering multiple competing focal points; breaking a sequential-reading flow with a distracting eye-catcher.
- Ask: "How many genuine focal points does this page have, and are they competing? Where does the eye go first — does that match what's really important?"
⟨di2-027⟩

### Deliberately cue changes users must notice (avoid change blindness)
When a screen updates and only part of it changes, don't assume users will notice — change and inattentional blindness mean people routinely miss large changes outside their current attention, and looking at something doesn't guarantee it registered.
- Do: add an explicit visual cue (highlight/flash/color change) or audio cue for changes users must notice, including validation errors after submission and any non-full-reload state change.
- Ask: "If this element changes without a full reload, is there a cue strong enough to guarantee the user notices?"
⟨psy1-012, laws1-053⟩

### Place important content ~30% inset from the top corner, not the literal edge
Position the most important information roughly 30% in from the top and left (or right, for RTL) edge — users learn to skip literal edges (logos, whitespace, nav chrome) and start scanning from a point inset from the corner, following their normal reading-direction scan path.
- Avoid: placing critical content at the literal screen edge and expecting it found quickly.
- Ask: "Is the most important content in the true starting zone, or stranded at a literal edge?"
⟨psy1-008⟩

### Give interactive elements affordances that match their real behavior
Give interactive elements a visual cue (shadow, raised appearance) signaling how they can be operated — critical on touchscreens, which have no hover state. The cue must match real behavior; a mismatched affordance confuses users even when a label technically clarifies it.
- Do: use shadow/depth for pressable cues; show a visible pressed/active state; make tap affordance visible without hover.
- Avoid: flat color blocks as the sole interactivity signal; relying on a label to fix a control whose shape signals the wrong action.
- Trade-off: flat/minimal visual style vs. clarity of what's interactive.
- Ask: "Can a user tell this is interactive without hovering? Does its shape suggest the action it actually performs?"
⟨psy1-010, psy1-011⟩

### Keep signifiers even in flat/minimalist design
Minimalism cuts clutter effectively, but not when it strips the signifiers that distinguish interactive from non-interactive elements, as flat ("brutalist") design tends to. Balance by keeping the page logically segmented, making buttons obviously clickable, pairing icons with text labels (an "x" icon labeled "Delete"), and applying signifiers like drop shadows consistently to all interactive elements, not just some.
- Avoid: stripping signifiers until users can't tell what's tappable; applying a signifier to only some interactive elements.
- Trade-off: visual minimalism vs. discoverability of what's interactive.
- Ask: "Are visual signifiers applied consistently to every interactive element, or only some?"
⟨uxp1-094⟩

### Quick reference
- In contexts where users are habituated to lower-stakes signals, make genuinely critical alerts many times more visually/aurally distinct than feels sufficient — people build expectations about what they'll normally see and can fail to notice a real deviation, especially under stress (illustrated by the USS Vincennes radar-misclassification incident). ⟨psy1-053⟩
- Research which specific "salient cues" your actual target users rely on to recognize/act on something, and emphasize those — don't assume users notice the same details an expert or designer would (ordinary people ID coins by color/size/hole; collectors by mint year and typeface). ⟨psy1-057⟩
- Build icons from simple, clean geometric shapes ("geons") rather than intricate/decorated forms, especially at small sizes — people identify objects by matching basic geometric primitives, so simpler shapes are recognized faster. ⟨psy1-004⟩
- Reserve screen edges (peripheral vision) for gist-level brand/orientation content — logos, nav chrome, evocative imagery — keep task-critical detail where users foveate, and avoid blinking/moving elements in peripheral view unless deliberately hijacking attention from the current task. ⟨psy1-002, psy1-003⟩

## Chunking Content: Tabs, Accordion, Collapsible & Movable Panels

### Quick reference
- Choose the chunking container by module behavior, not habit: Module Tabs when only one is visible at a time (similar size, <~10, static set); Accordion when several may be open at once (variable height, shared width, order matters); Collapsible Panels when modules are optional/supplementary to a dominant main area and value varies per user; Movable Panels when several should be open at once, relevance/size vary widely, and users rearrange/remove/re-add modules (dashboards, portals, tool palettes). ⟨di2-028⟩
- Module Tabs: small tabbed area, one module visible at a time — similar-length modules, <~10 (ideally ~5), static set; nail the IA and use short (1-2 word) titles first, keep the selected tab visually continuous with its panel, and if too many exist, truncate labels or move them to the side rather than scrolling tabs or stacking two rows. ⟨di2-033⟩
- Accordion: vertically stacked, independently open/closeable panels, fixed order — modules vary in height but share a width, belong to an interactive-element system (tool palette, 2-level menu), order matters; default to multiple open at once (forced single-open makes other modules jarringly vanish) and persist state, except when very limited vertical space forces single-open. ⟨di2-034⟩
- Collapsible Panels: individually open/closeable panels for secondary/supplementary content (not grouped modules) so closing one returns its space to main content — no module deserves default-open, value varies per user, modules are largely unrelated; flip a panel's default to open if most users leave it open, and use Tabs/Accordion instead if modules are actually grouped. ⟨di2-035⟩
- Movable Panels: independently open/closeable, draggable, user-repositionable boxes — desktop apps, portals, dashboards where module relevance/size/position vary a lot per user and users add/remove/rearrange modules; support drag-and-drop with ghosting, one-gesture toggle, full removal with later re-add from a browsable list, persisted state, and a reset-to-default escape hatch. ⟨di2-036⟩

## Page-Level Layout Patterns

### Visual Framework: keep layout and style consistent across pages
Give every page or window the same base layout, color palette, style elements, and layout grid, while leaving enough flexibility for each page's distinct content.
- Do: share color/fonts/voice across pages; keep "you are here" signposts consistent (titles, logo, breadcrumbs, nav highlighting, module tabs); keep navigation and spacing/alignment consistent; separate style definition from content (stylesheet/shared class) so the framework is revisable in one place.
- Exception: the home page/main window may be "special" but should still share some framework elements; closely related/affiliated sites can share most elements while keeping a few distinguishing points.
- Trade-off: strict framework consistency vs. differentiating a related sub-site enough to feel distinct.
⟨di2-029⟩

### Right/Left Alignment for form labels and controls
In two-column forms/tables, right-align labels in the left column and left-align controls/values in the right column, keeping each label close to its control — near proximity groups a label with its control far better than a wide gap, and the two aligned edges create parallel implied lines that pull the eye down the page.
- Do: right-align each label a few pixels from its control; left-align controls precisely along a shared line; align control right edges too for visually heavy controls (or group short-with-short, long-with-long).
- Exception: long labels needing careful reading — right-aligned text is harder to read since the eye must hunt for each line's start, so left-align or move labels above controls; UIs localized across languages with very different label lengths — put labels above controls, at the cost of vertical space; when another column sits left of the labels.
- Trade-off: readability (favors left-aligned labels) vs. tight label-to-control grouping (favors right-aligned labels).
⟨di2-037⟩

### Quick reference
- Center Stage: give the single most important content/task the largest sub-section — at least 2x the width of anything beside it and 2x the height of anything above/below it in the first screenful — everything else as smaller supporting panels; use a contrasting color and a large heading to anchor it, and never push it below the fold. ⟨di2-030⟩
- Grid of Equals: arrange same-style, same-importance items (articles, products) into a grid on one shared small template, equal visual weight; favor richer visual variety (color, whitespace, images) over plain text blocks, and never let a hover/default highlight move or resize an item — change color/style only. ⟨di2-031⟩
- Titled Sections: fix the information architecture first — split content into coherent, well-named units — then give each a visually distinct title (weight, color, size, font, tracking) with clear whitespace/background separation; a section that resists a short memorable name means the grouping is probably wrong, so don't let "Other/Misc" become a permanent fix. ⟨di2-032⟩
- Diagonal Balance: in an asymmetric page/dialog that fits one screen, put strong elements (title, tabs) top-left and other strong elements (action buttons) bottom-right so the weights balance and support left-to-right reading flow — less natural on platforms (e.g. classic Mac OS X) that already center titlebars/buttons. ⟨di2-038⟩
- Responsive Disclosure: for a complex, unfamiliar, or infrequent multi-step task kept on one page, show only the current step's controls and reveal each next step in place once the prior is complete, keeping earlier steps visible/editable — builds a correct mental model without wizard-style context switches, but don't reveal a step's controls only to yank them away once branching makes them irrelevant. ⟨di2-039⟩
- Responsive Enabling: for a multi-step task that must fit on one page where stability matters more than watching it grow, show most controls up front but disabled, enabling each as the prior step completes — place a disabled control near what unlocks it, explain why it's disabled, disable only what genuinely can't be used yet; a reverse variant ("responsive disabling") narrows options as input gets more specific. ⟨di2-040⟩

⚖ Tension: reveal steps vs disable steps → tradeoffs-decision-points.md (vh-d01)

## Spacing, Sizing & Responsive Behavior

### Design fluid layouts that adapt to viewport instead of fixed/separate versions
Design layouts to resize fluidly across screen sizes (fluid grids, flexible images, media queries) so content fills available space, rather than fixed-size or separate desktop/mobile designs — a layout built to survive arbitrary resizing tends to also survive localization or font-size changes.
- Do: let center-stage content (text, tree, table, diagram, editor) expand while margins stay compact; wrap text to ~10-12 words/line (~30-35 em-characters); expand form fields and scrollable lists/tables as the window widens; keep navigation/signposts anchored to top/left; let the least important content clip or hide first as the window shrinks below its natural size.
- Avoid: letting a paragraph stretch to a very wide line length; maintaining fully separate device-specific designs when fluid would serve equally well.
- Exception: the visual design genuinely requires an exact, fixed amount of screen real estate.
- Trade-off: very long lines (~100 characters) read somewhat faster in some studies, but users report preferring shorter lines around 55 characters — no single correct line length.
⚖ Tension: line length → tradeoffs-decision-points.md (typo-d01)
⟨di2-041, laws1-034⟩

### Start with too much white space, then remove it
Begin spacing with noticeably more room than seems necessary, then remove space until it looks right — space added reactively (just enough to avoid cramping) tends to produce only the minimum breathing room; what feels "a little too much" in isolation usually reads as "just enough" in the full UI.
- Avoid: defaulting to the minimum margin/padding needed to avoid looking bad.
⚖ Tension: whitespace vs density → tradeoffs-decision-points.md (vh-d02)
⟨rui1-026⟩

### Build a predefined, non-linear spacing/sizing scale
Build a spacing scale from a sensible base unit (16px suggested), predefined in advance rather than tuned pixel-by-pixel. No two adjacent values should differ by less than ~25%, tighter at the small end and looser at the large end, not a linear step — the same absolute pixel gap matters far more at the small end (12→16px is a 33% jump) than the large end (500→520px is 4%).
- Avoid: a purely linear step size (e.g. always +4px) across the whole scale; fine-tuning pixels without a predefined scale to select from.
⟨rui1-028, rui1-029⟩

### Size elements to actual content need, not to fill or cram space
Size every layout/section/element to what its content needs in both directions — don't stretch to fill available canvas/viewport just because the space exists or a sibling is full-width, and don't cram it either. Unnecessarily wide layouts are harder to interpret than content-sized ones.
- Do: if a narrower-optimal component looks unbalanced in a wider page, split into columns (pull supporting content into an adjacent column) rather than widening the primary content; for something meant to be narrow/small (mobile), design on a canvas matching its real target width rather than a large canvas.
- Avoid: stretching a layout to fill width just because the space exists or a sibling is full-width.
⟨rui1-030, rui1-031, rui1-032, rui1-033⟩

### Quick reference
- Build the base experience to work for every browser, device, connection speed, and assistive technology first, then progressively layer richer styling/interaction for capable environments, rather than designing for the best case and patching fallbacks afterward (progressive enhancement vs. graceful degradation). ⟨laws1-035⟩
- Don't apply percentage-based grid sizing dogmatically: give an element whose optimal size doesn't change with viewport (e.g. a sidebar, or something inside a component not meant to scale) a fixed width instead, letting siblings flex to fill remaining space; if an element has one clear optimal fixed width across most viewports, give it a max-width equal to that size and let it shrink only when required, instead of assigning different grid-column counts per breakpoint. ⟨rui1-034, rui1-035⟩
- Don't assume a size relationship that looks right in one context should be preserved by a fixed ratio (em units relative to another element's font-size, padding as a font-size multiple) — retune each property independently per context/variant; elements large in a large context need to shrink proportionally faster than already-small elements as space shrinks. ⟨rui1-036⟩

## Action Hierarchy: Buttons & Destructive Styling

### Rank actions into primary/secondary/tertiary tiers and style accordingly
Rank every actionable element on a page into primary (usually exactly one), secondary, and tertiary tiers, and style each to communicate rank: primary gets a solid, high-contrast background; secondary gets outline/lower-contrast; tertiary gets link-like styling. Styling by semantic type alone ignores that every page has its own pyramid of importance.
- Avoid: styling an action purely by its semantic category without considering its hierarchy rank on this page.
⟨rui1-024⟩

### Quick reference
- Don't automatically give a destructive/high-severity action big, red, bold styling by default — style it per its actual hierarchy rank on the current page (secondary/tertiary if not the primary action); reserve strong warning styling, and unequal visual weight vs. the safe option, for a confirmation step where the destructive action becomes primary — equal weight between destructive and safe choices in a confirmation dialog raises the odds of an unintended irreversible pick. ⟨laws1-054, rui1-025⟩
