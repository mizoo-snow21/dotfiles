# HIG — Components: status & system experiences
activity-rings, gauges, progress-indicators, rating-indicators, app-shortcuts, complications, controls, live-activities, notifications, snippets, status-bars, top-shelf, watch-faces, widgets

## Activity Rings
Source: https://developer.apple.com/design/human-interface-guidelines/activity-rings
Activity rings show an individual's daily progress toward Move, Exercise, and Stand goals.
- **Display Activity rings when they're relevant** to the purpose of your app — apps related to health or fitness, especially ones contributing to HealthKit, are expected to include them (e.g., on a workout metrics screen or a post-workout summary screen).
- **Use Activity rings only to show Move, Exercise, and Stand information.** Never replicate, modify, or repurpose them for other data; never show this data in another ring-like element.
- **Use Activity rings to show progress for a single person only.** Never represent more than one person's data; make whose progress is shown obvious via label, photo, or avatar.
- **Always keep the visual appearance identical regardless of context:**
  - Never change ring colors (no filters, no opacity changes).
  - Always display rings on a black background.
  - Prefer enclosing rings/background in a circle by adjusting the corner radius of the enclosing view, not a circular mask.
  - Keep the black background visible around the outermost ring; add a thin black stroke if needed; avoid gradients, shadows, or other effects.
  - Always scale rings appropriately so they don't look disconnected.
  - Design the surrounding interface to blend with the rings — never the reverse.
- **Use matching colors for ring-specific labels/values** (Move, Exercise, Stand) when displaying labels or current/goal values tied to a ring.
- **Maintain Activity ring margins:** minimum outer margin no less than the distance between rings; nothing may crop, obstruct, or encroach on this margin or the rings.
- **Differentiate other ring-like elements** from Activity rings using padding, lines, labels, color, or scale to avoid visual confusion.
- **Don't send notifications that repeat what the Activity app already sends**, and don't show an Activity ring element in notifications; referencing progress in your own unique way is fine.
- **Don't use Activity rings for decoration** (e.g., in labels or background graphics) or **for branding** (e.g., app icon, marketing materials).
**Platforms:** iOS: available via `HKActivityRingView`; shows all three rings when an Apple Watch is paired, or the Move ring only (approximated from steps/workouts) when unpaired — history can mix both styles. watchOS: always shows all three rings. Not supported in macOS, tvOS, or visionOS.

## Gauges
Source: https://developer.apple.com/design/human-interface-guidelines/gauges
A gauge displays a specific numerical value within a range of values, using a circular or linear path with either an indicator (standard style) or a fill (capacity style).
- An **accessory variant** (circular/linear, standard/capacity) is visually similar to watchOS complications and works well in iOS Lock Screen widgets or anywhere you want to echo complications.
- **Write succinct labels** describing the current value and both endpoints of the range — VoiceOver reads visible labels even when not all styles display them onscreen.
- **Consider filling the path with a gradient** to help communicate the gauge's purpose (e.g., red-to-blue for hot-to-cold temperature).
**Platforms:** macOS also defines a level indicator (similar visual styles) configurable for capacity, rating, or (rarely) relevance. Capacity style can be discrete or continuous — prefer continuous for large ranges since discrete segments become too small to be useful. Consider changing fill color (default green) at significant levels (very low/high/mid), either for the whole indicator or via the tiered state showing a color sequence. Rating style: see Rating indicators. Relevance style (rarely used) shows relevancy via a shaded horizontal bar, e.g. in search-result lists. No additional considerations for iOS, iPadOS, visionOS, or watchOS. Not supported in tvOS.

## Progress Indicators
Source: https://developer.apple.com/design/human-interface-guidelines/progress-indicators
Progress indicators let people know an app isn't stalled while it loads content or performs lengthy operations; they are always transient, appearing only during the operation.
Use for: determinate indicators (well-defined duration, e.g. file conversion) — progress bars (fill leading→trailing) or circular progress indicators (fill clockwise). Prefer indeterminate ("activity indicator"/spinner, an animated spinning image) only for unquantifiable tasks (e.g. loading, syncing).
- **When possible, use a determinate progress indicator** — it helps people decide whether to wait, restart later, or abandon the task; indeterminate only shows that something is happening.
- **Be as accurate as possible reporting advancement**; even out the pace — jumping to 90% in 5 seconds then taking 5 minutes for the last 10% feels deceptive.
- **Keep progress indicators moving** so people know something is still happening; if a process stalls, give feedback explaining the problem and what to do.
- **When possible, switch a progress bar from indeterminate to determinate** once duration becomes knowable — people prefer determinate indicators.
- **Don't switch from the circular style to the bar style** — different shapes/sizes disrupt the interface.
- **If helpful, display a description providing additional context** — be accurate and succinct; avoid vague terms like "loading" or "authenticating."
- **Display a progress indicator in a consistent location** so people can reliably find operation status.
- **When feasible, let people halt processing** — include a Cancel button if interruption has no negative side effects; add a Pause button too if canceling would cause loss (e.g., a partially downloaded file).
- **Let people know when halting has a negative consequence** — provide an alert with options to confirm cancellation or resume.
**Platforms:**
- iOS, iPadOS: Refresh control — a specialized, normally-hidden activity indicator that becomes visible when a person drags down a reloadable view (e.g., table view). Perform automatic content updates regularly regardless — don't make people responsible for every refresh. Supply a short title only if it adds value (most cases don't need one); if included, don't explain how to refresh — show info about the content instead (e.g., last-update time).
- macOS: indeterminate indicators can be bar or circular. Prefer a spinner to communicate background-operation status or when space is constrained (asynchronous tasks, within a text field, next to a button). Avoid labeling a spinning progress indicator — a label is usually unnecessary since spinners appear when people initiate a process.
- watchOS: indicators display in white over the scene's background color by default; color is changeable via tint color.

## Rating Indicators
Source: https://developer.apple.com/design/human-interface-guidelines/rating-indicators
A rating indicator uses a series of horizontally arranged graphical symbols — by default, stars — to communicate a ranking level, rounding to whole symbols only (never partial), with symbols always the same distance apart regardless of component width.
- **Make it easy to change rankings** — let people adjust the rank of individual items inline within a ranked list, without navigating to a separate editing screen.
- **If replacing the star with a custom symbol, make sure its purpose is clear** — the star is highly recognizable as a ranking symbol; other symbols may not be associated with a rating scale.
**Platforms:** No additional considerations for macOS. Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## App Shortcuts
Source: https://developer.apple.com/design/human-interface-guidelines/app-shortcuts
An App Shortcut gives people access to your app's key functions or content throughout the system, initiated via Siri, Spotlight, the Shortcuts app, hardware features (Action button on iPhone/Apple Watch), or Squeeze Apple Pencil. App Shortcuts use App Intents; each app can include up to 10 App Shortcuts, each combining one or more actions.
Use for: exposing unique features or custom content not covered by app schemas. Prefer adopting app schemas instead when surfacing common types of functionality broadly through the system (lets Siri/Apple Intelligence surface features contextually without adopting individual App Shortcuts).
> Note: In addition to App Shortcuts, people can build their own custom shortcuts by combining App Intents actions in the Shortcuts app, enabling cross-app workflows.
- **Offer App Shortcuts for your app's most common and important tasks** — straightforward, completable-without-leaving-context tasks work best, though opening the app is fine for easier multistep completion.
- **Add flexibility with a set of options** — an App Shortcut can include a single optional parameter (e.g., "Start [morning, daily, sleep] meditation"); use predictable, familiar values since people won't have the list in front of them.
- **Ask for clarification when optional information is missing** — e.g., suggest the most-recently-used or time-of-day-appropriate default, with a short list of alternatives.
- **Keep voice interactions simple** — if a phrase sounds too complicated aloud, it's too hard to remember/say; ask for extra required info in a subsequent step instead of overloading one phrase.
- **Make App Shortcuts discoverable in your app** — consider showing occasional tips when people perform common actions.
- **Responding to App Shortcuts:** Snippets suit custom views for static info or dialog options (e.g., showing weather, confirming an order); Live Activities suit continuous, changing information over time (timers, countdowns).
- **Provide enough detail for audio-only devices** (AirPods, HomePod) — include all critical information in the full dialogue text since people may not see onscreen content.
- Editorial: **Provide brief, memorable activation phrases and natural variants** — app name is required but phrasing can be creative. **Use title case and plural "Shortcuts"** when referring to App Shortcuts or the Shortcuts app. **Use lowercase** when referring to individual (non-App) shortcuts.
**Platforms:** iOS, iPadOS: App Shortcuts can appear in Spotlight's Top Hit area or the Shortcuts area below, each with an SF Symbol or a preview image. Order shortcuts by importance for initial display — the system reprioritizes by usage frequency afterward. macOS: App Shortcuts aren't supported, but App Intents actions are, and people can build custom shortcuts from them in the Shortcuts app. No additional considerations for visionOS or watchOS. Not supported in tvOS.

## Complications
Source: https://developer.apple.com/design/human-interface-guidelines/complications
A complication displays timely, relevant information on the watch face, viewable each time a wrist is raised. Starting in watchOS 9, complications (also called accessories) are organized into families (e.g. circular, inline) with recommended layouts; a watch face specifies the family each slot supports. Legacy templates define nongraphic styles that don't take on a wearer's selected color.
> Developer note: prefer WidgetKit for watchOS 9+; use the ClockKit `CLKComplicationDataSource` protocol only to support earlier versions.
- **Identify essential, dynamic content** people want at a glance — static complications that don't display meaningful data are less likely to stay prominent.
- **Support all complication families when possible** to maximize the watch faces your complication is available on; if no useful data fits a family, provide an app-representative image (e.g. app icon) that still launches your app.
- **Consider creating multiple complications per family** to take advantage of shareable watch faces centered on your app (e.g., three circular complications, one per race segment, each deep-linking to that area).
- **Define a different deep link for each complication** — opening the same app area from every complication makes them seem less useful.
- **Keep privacy in mind** — with Always-On Retina display, watch-face info may be visible to others; prevent sensitive information exposure (see Always On).
- **Carefully consider when to update data** — data is provided as a timeline of entries with display times; timeline updates are limited per day and the system stores a limited number of entries per app, so choose times that maximize usefulness.
- Visual design: **Choose a ring or gauge style based on the data**: closed style for a percentage of a whole (e.g. battery); open style when min/max are arbitrary/non-percentage (e.g. speed); segmented style for app-defined ranges with rapid changes (e.g. Noise complication).
- **Make images look good in tinted mode** — in tinted mode the system applies a solid color to text/gauges/images and desaturates full-color images unless tinted versions are supplied (legacy templates: tinted mode applies only to graphic complications). Avoid using color as the sole way to communicate important information; supply an alternative tinted-mode image if desaturation looks bad.
- **Recognize people might prefer tinted mode** over full color — the system desaturates and applies a single wearer-selected color to images, gauges, and text.
- **Generally use line widths of two points or greater** — thinner lines are hard to see at a glance, especially in motion.
- **Provide a set of static placeholder images** for each complication supported — used when there's no data yet (e.g., on first install) or in the selection carousel; note placeholder image sizes vary per layout/template and may not match the actual-content image size.
- **Circular family:** supports text, gauges, and full-color images in circular areas on Infograph and Infograph Modular faces, plus extra-large layouts for the X-Large face; regular-size circular images can add bezel-curving text (fills up to ~180° before truncating).

| Image | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Image | 42x42 pt (84x84 px @2x) | 44.5x44.5 pt (89x89 px @2x) | 47x47 pt (94x94 px @2x) | 50x50 pt (100x100 px @2x) |
| Closed gauge | 27x27 pt (54x54 px @2x) | 28.5x28.5 pt (57x57 px @2x) | 31x31 pt (62x62 px @2x) | 32x32 pt (64x64 px @2x) |
| Open gauge | 11x11 pt (22x22 px @2x) | 11.5x11.5 pt (23x23 px @2x) | 12x12 pt (24x24 px @2x) | 13x13 pt (26x26 px @2x) |
| Stack (not text) | 28x14 pt (56x28 px @2x) | 29.5x15 pt (59x30 px @2x) | 31x16 pt (62x32 px @2x) | 33.5x16.5 pt (67x33 px @2x) |

> Note: the system applies a circular mask to each image.

Regular-size circular default text (SwiftUI): Style Rounded, Weight Medium, Text size 12 pt (40mm), 12.5 pt (41mm), 13 pt (44mm), 14.5 pt (45mm/49mm).

Extra-large circular (for X-Large watch face; e.g. Contacts complication with a contact photo; some text fields support multicolor text):

| Image | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Image | 120x120 pt (240x240 px @2x) | 127x127 pt (254x254 px @2x) | 132x132 pt (264x264 px @2x) | 143x143 pt (286x286 px @2x) |
| Open gauge | 31x31 pt (62x62 px @2x) | 33x33 pt (66x66 px @2x) | 33x33 pt (66x66 px @2x) | 37x37 pt (74x74 px @2x) |
| Closed gauge | 77x77 pt (154x154 px @2x) | 81.5x81.5 pt (163x163 px @2x) | 87x87 pt (174x174 px @2x) | 91.5x91.5 pt (183x183 px @2x) |
| Stack | 80x40 pt (160x80 px @2x) | 85x42 pt (170x84 px @2x) | 87x44 pt (174x88 px @2x) | 95x48 pt (190x96 px @2x) |

> Note: circular mask applied to circular, open-gauge, and closed-gauge images.

Circular no-content placeholders:

| Layout | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Circular | – | 42x42 pt (84x84 px @2x) | 44.5x44.5 pt (89x89 px @2x) | 47x47 pt (94x94 px @2x) | 50x50 pt (100x100 px @2x) |
| Bezel | – | 42x42 pt (84x84 px @2x) | 44.5x44.5 pt (89x89 px @2x) | 47x47 pt (94x94 px @2x) | 50x50 pt (100x100 px @2x) |
| Extra Large | – | 120x120 pt (240x240 px @2x) | 127x127 pt (254x254 px @2x) | 132x132 pt (264x264 px @2x) | 143x143 pt (286x286 px @2x) |

Extra-large circular default text: Style Rounded, Weight Medium, Text size 34.5 pt (40mm), 36.5 pt (41mm), 36.5 pt (44mm), 41 pt (45mm/49mm).

- **Corner family:** full-color images, text, and gauges in the watch-face corners (e.g. Infograph); some templates support multicolor text.

| Image | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Circular | 32x32 pt (64x64 px @2x) | 34x34 pt (68x68 px @2x) | 36x36 pt (72x72 px @2x) | 38x38 pt (76x76 px @2x) |
| Gauge | 20x20 pt (40x40 px @2x) | 21x21 pt (42x42 px @2x) | 22x22 pt (44x44 px @2x) | 24x24 pt (48x48 px @2x) |
| Text | 20x20 pt (40x40 px @2x) | 21x21 pt (42x42 px @2x) | 22x22 pt (44x44 px @2x) | 24x24 pt (48x48 px @2x) |

> Note: circular mask applied to each image.

Corner placeholders: 38mm –, 40mm/42mm 20x20 pt (40x40 px @2x), 41mm 21x21 pt (42x42 px @2x), 44mm 22x22 pt (44x44 px @2x), 45mm/49mm 24x24 pt (48x48 px @2x).
Corner default text: Style Rounded, Weight Semibold, Text size 10 pt (40mm), 10.5 pt (41mm), 11 pt (44mm), 12 pt (45mm/49mm).

- **Inline family:** utilitarian small (corner rectangular area, e.g. Chronograph/Simple faces; content = image, interface icon, or circular graph) and utilitarian large (mostly text-based, optional leading interface icon; spans the bottom of a face, e.g. Utility/Motion).

Utilitarian small:

| Content | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Flat | 9-21x9 pt (18-42x18 px @2x) | 10-22x10 pt (20-44x20 px @2x) | 10.5-23.5x21 pt (21-47x21 @2x) | N/A | 12-26x12 pt (24-52x24 px @2x) |
| Ring | 14x14 pt (28x28 px @2x) | 14x14 pt (28x28 px @2x) | 15x15 pt (30x30 px @2x) | 16x16 pt (32x32 px @2x) | 16.5x16.5 pt (33x33 px @2x) |
| Square | 20x20 pt (40x40 px @2x) | 22x22 pt (44x44 px @2x) | 23.5x23.5 pt (47x47 px @2x) | 25x25 pt (50x50 px @2x) | 26x26 pt (52x52 px @2x) |

Utilitarian large:

| Content | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Flat | 9-21x9 pt (18-42x18 px @2x) | 10-22x10 pt (20-44x20 px @2x) | 10.5-23.5x10.5 pt (21-47x21 px @2x) | N/A | 12-26x12 pt (24-52x24 px @2x) |

- **Rectangular family:** full-color images, text, a gauge, and an optional title in a large rectangular region — good for information-rich charts/graphs over time (e.g. Heart Rate complication's 24-hour graph, high-contrast white/red primary content with lower-contrast gray gridlines/labels). Since watchOS 10, rectangular layouts may be shown in the Smart Stack — optimize via background color/content, intent-based relevancy, or a custom Smart-Stack-tailored layout.

| Content | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Large image with title * | 150x47 pt (300x94 px @2x) | 159x50 pt (318x100 px @2x) | 171x54 pt (342x108 px @2x) | 178.5x56 pt (357x112 px @2x) |
| Large image without title * | 162x69 pt (324x138 px @2x) | 171.5x73 pt (343x146 px @2x) | 184x78 pt (368x156 px @2x) | 193x82 pt (386x164 px @2x) |
| Standard body | 12x12 pt (24x24 px @2x) | 12.5x12.5 pt (25x25 px @2x) | 13.5x13.5 pt (27x27 px @2x) | 14.5x14.5 pt (29x29 px @2x) |
| Text gauge | 12x12 pt (24x24 px @2x) | 12.5x12.5 pt (25x25 px @2x) | 13.5x13.5 pt (27x27 px @2x) | 14.5x14.5 pt (29x29 px @2x) |

> Note: both large-image layouts automatically include a four-point corner radius.

Rectangular default text: Style Rounded, Weight Medium, Text size 16.5 pt (40mm), 17.5 pt (41mm), 18 pt (44mm), 19.5 pt (45mm/49mm).

- **Legacy templates:**
  - *Circular small* (small image or few text characters, e.g. Color watch face corner):

| Image | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Ring | 20x20 pt (40x40 px @2x) | 22x22 pt (44x44 px @2x) | 23.5x23.5 pt (47x47 px @2x) | 24x24 pt (48x48 px @2x) | 26x26 pt (52x52 px @2x) |
| Simple | 16x16 pt (32x32 px @2x) | 18x18 pt (36x36 px @2x) | 19x19 pt (38x38 px @2x) | 20x20 pt (40x40 px @2x) | 21.5x21.5 pt (43x43 px @2x) |
| Stack | 16x7 pt (32x14 px @2x) | 17x8 pt (34x16 px @2x) | 18x8.5 pt (36x17 px @2x) | 19x9 pt (38x18 px @2x) | 19x9.5 pt (38x19 px @2x) |
| Placeholder | 16x16 pt (32x32 px @2x) | 18x18 pt (36x36 px @2x) | 19x19 pt (38x38 px @2x) | 20x20 pt (40x40 px @2x) | 21.5x21.5 pt (43x43 px @2x) |

> Note: in each stack measurement, width represents the maximum size.

  - *Modular small* (two stacked rows: icon+content, circular graph, or one larger item; e.g. bottom row on the Modular face):

| Image | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Ring | 18x18 pt (36x36 px @2x) | 19x19 pt (38x38 px @2x) | 20x20 pt (40x40 px @2x) | 21x21 pt (42x42 px @2x) | 22.5x22.5 pt (45x45 px @2x) |
| Simple | 26x26 pt (52x52 px @2x) | 29x29 pt (58x58 px @2x) | 30.5x30.5 pt (61x61 px @2x) | 32x32 pt (64x64 px @2x) | 34.5x34.5 pt (69x69 px @2x) |
| Stack | 26x14 pt (52x28 px @2x) | 29x15 pt (58x30 px @2x) | 30.5x16 pt (61x32 px @2x) | 32x17 pt (64x34 px @2x) | 34.5x18 pt (69x36 px @2x) |
| Placeholder | 26x26 pt (52x52 px @2x) | 29x29 pt (58x58 px @2x) | 30.5x30.5 pt (61x61 px @2x) | 32x32 pt (64x64 px @2x) | 34.5x34.5 pt (69x69 px @2x) |

  - *Modular large* (up to three rows of content, e.g. center of Modular face):

| Content | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Columns | 11-32x11 pt (22-64x22 px @2x) | 12-37x12 pt (24-74x24 px @2x) | 12.5-39x12.5 pt (25-78x25 px @2x) | 14-42x14 pt (28-84x28 px @2x) | 14.5-44x14.5 pt (29-88x29 px @2x) |
| Standard body | 11-32x11 pt (22-64x22 px @2x) | 12-37x12 pt (24-74x24 px @2x) | 12.5-39x12.5 pt (25-78x25 px @2x) | 14-42x14 pt (28-84x28 px @2x) | 14.5-44x14.5 pt (29-88x29 px @2x) |
| Table | 11-32x11 pt (22-64x22 px @2x) | 12-37x12 pt (24-74x24 px @2x) | 12.5-39x12.5 pt (25-78x25 px @2x) | 14-42x14 pt (28-84x28 px @2x) | 14.5-44x14.5 pt (29-88x29 px @2x) |

  - *Extra large* (larger text/images, e.g. X-Large watch faces):

| Image | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Ring | 63x63 pt (126x126 px @2x) | 66.5x66.5 pt (133x133 px @2x) | 70.5x70.5 pt (141x141 px @2x) | 73x73 pt (146x146 px @2x) | 79x79 pt (158x158 px @2x) |
| Simple | 91x91 pt (182x182 px @2x) | 101.5x101.5 pt (203x203 px @2x) | 107.5x107.5 pt (215x215 px @2x) | 112x112 pt (224x224 px @2x) | 121x121 pt (242x242 px @2x) |
| Stack | 78x42 pt (156x84 px @2x) | 87x45 pt (174x90 px @2x) | 92x47.5 pt (184x95 px @2x) | 96x51 pt (192x102 px @2x) | 103.5x53.5 pt (207x107 px @2x) |
| Placeholder | 91x91 pt (182x182 px @2x) | 101.5x101.5 pt (203x203 px @2x) | 107.5x107.5 pt (215x215 px @2x) | 112x112 pt (224x224 px @2x) | 121x121 pt (242x242 px @2x) |

> Note: in each stack measurement, width represents the maximum size.

**Platforms:** Not supported in iOS, iPadOS, macOS, tvOS, or visionOS (watchOS-only component).

## Controls
Source: https://developer.apple.com/design/human-interface-guidelines/controls
A control provides quick access to a feature of your app from Control Center, the Lock Screen, or the Action button — a button (performs an action, links to an app area, or launches a Camera experience on a locked device) or a toggle (switches between two states). People add controls by pressing and holding in an empty Control Center area, customizing the Lock Screen, or configuring the Action button in Settings.
Anatomy: a symbol image, a title, and optionally a value. Display differs by placement — Control Center shows symbol always, and title/value at larger sizes; Lock Screen shows symbol only; the Action button (iPhone) shows the symbol in the Dynamic Island plus value (if present) when pressed and held.
- **Offer controls for actions with the most benefit without launching your app** (e.g., starting a Live Activity directly from a control).
- **Update controls on interaction, on action completion, or remotely via push notification** to accurately reflect state/in-progress status.
- **Choose a descriptive symbol that suggests the control's behavior** — since title/value may not display, the symbol must carry enough meaning; toggles need symbols for both on/off states (e.g. `door.garage.open` / `door.garage.closed`).
- **Use symbol animations to highlight state changes** — animate the on/off transition for toggles; animate indefinitely during a button action's duration and stop when complete.
- **Select a tint color that works with your app's brand** — applied to a toggle's on-state symbol, and to the value/symbol shown in the Dynamic Island when triggered via the Action button.
- **Help people provide additional configuration info the system needs** (e.g. selecting which light to control) — prompt on first add; people can reconfigure anytime.
- **Provide hint text for the Action button** using verbs, describing what press-and-hold does.
- **If title or value can vary, include a placeholder** shown in the controls gallery or before Action-button assignment.
- **Hide sensitive information when the device is locked** — have the system redact title/value (and optionally the symbol state, showing the off-state symbol) to protect personal/security-related info.
- **Require authentication for security-affecting actions** (e.g. locking/unlocking a door, starting a car).
- **Camera experiences on a locked device** (iOS 18+): a control can launch directly into your app's camera capture UI while locked; any task beyond capture requires unlocking. Use the same camera UI in-app and in the camera experience for a seamless transition. Provide instructions for adding the control.
**Platforms:** No additional considerations for iOS, iPadOS, or macOS. Not supported in watchOS, tvOS, or visionOS.

## Live Activities
Source: https://developer.apple.com/design/human-interface-guidelines/live-activities
A Live Activity lets people track the progress of an activity, event, or task at a glance, delivering frequent content/status updates over a few hours with interactive elements, beyond what push notifications offer. Starts on iPhone or iPad and appears automatically across devices:

| Platform or system experience | Location |
|---|---|
| iPhone and iPad | Lock Screen, Home Screen, in the Dynamic Island and StandBy on iPhone |
| Mac | The menu bar |
| Apple Watch | Smart Stack |
| CarPlay | CarPlay Dashboard |

Anatomy — must support four presentations: **Compact** (Dynamic Island, one active Live Activity — two elements, leading/trailing of the TrueDepth camera), **Minimal** (Dynamic Island, multiple active — two shown, one attached/one detached, circular or oval depending on content size), **Expanded** (shown on touch-and-hold from compact/minimal), **Lock Screen** (banner at bottom of Lock Screen; use an expanded-like layout; briefly appears as a banner overlay on devices without Dynamic Island).
**StandBy:** appears in minimal presentation; tapping transitions to Lock Screen presentation scaled 2x to fill the screen; a custom Lock Screen background color auto-extends full-screen.
- **Offer Live Activities for tasks/events with a defined beginning and end**, best for short-to-medium duration activities not exceeding eight hours.
- **Focus on important information people need at a glance** — don't try to display everything; let tapping open the app for detail.
- **Don't use a Live Activity to display ads or promotions.**
- **Avoid displaying sensitive information** — show an innocuous summary and let tapping reveal sensitive info in-app, or redact views and let people configure display of sensitive data.
- **Create a Live Activity matching your app's visual aesthetic and personality** in both dark and light appearances.
- **If including a logo mark, display it without a container** — don't use the entire app icon.
- **Don't add elements to your app that draw attention to the Dynamic Island.**
- **Ensure text is easy to read** — use large, medium-weight-or-heavier text; use small text sparingly, keep key info legible at a glance.
- Creating layouts: **Adapt to different screen sizes and presentations**, using Specifications values as guidance. **Adjust element size/placement for efficient space use** — only use space needed. **Use familiar layouts** from Apple Design Resources templates (default margins, recommended text sizes) to stay legible and fit surroundings (e.g. Apple Watch Smart Stack). **Use consistent margins and concentric placement** — match rounded-shape corner radii to the Live Activity's outer corner radius (subtract margin, apply via `ContainerRelativeShape`) to avoid visual tension near corners. **When separating a content block, use an inset container shape or a thick line** — don't draw content to the Dynamic Island's edge. **Dynamically change height** on Lock Screen/expanded presentation as available info shrinks/grows.
- Colors: **Carefully consider custom background color/opacity** — compact/minimal/expanded can't be customized, but Lock Screen presentation can; ensure sufficient contrast, especially for Always-On reduced-luminance displays. **Use color to express app character/identity** — Dynamic Island uses a black opaque background; bold colors help recognizability and brand. **Tint the key line color to match your content** — a key line appears around the Dynamic Island on dark backgrounds.
- Animations: system/custom animations max 2 seconds duration; none performed on Always-On reduced-luminance displays. **Use animations to reinforce information and draw attention to updates.** **Animate layout changes**, preserving existing elements by animating to new positions rather than remove/re-add. **Try to avoid overlapping elements** during transitions — animate out then re-animate in at a new position if needed.
- Interactivity: **Make sure tapping opens the app at the right location.** **Focus on simple, direct actions** — only essential functionality directly related to the activity, ideally a single interactive element to avoid mis-taps (e.g., music playback, workouts, live audio recording). **Consider letting people respond to event/progress updates** with a button or toggle.
- Lifecycle: **Start Live Activities at appropriate times and make them easy to turn off** in-app (or people will disable Live Activities in Settings altogether). **Offer an App Shortcut that starts your Live Activity** (e.g. via the Action button). **Update only when new content is available** — maintain the same display otherwise. **Alert people only for essential updates** — alerts light up the screen and play a sound by default; avoid over-alerting and don't duplicate with push notifications for the same update. **Let people track multiple events with a single Live Activity** using a dynamic, rotating layout rather than separate activities. **Always end a Live Activity immediately when the task/event ends**, and consider a custom dismissal time (commonly 15–30 minutes) proportional to the activity's duration — removed immediately from Dynamic Island/CarPlay; persists up to four hours on Lock Screen, Mac menu bar, and watchOS Smart Stack.
- Presentation guidance: **Start with the iPhone design, then refine for other contexts** (StandBy, CarPlay, watchOS).
  - Compact: **Focus on the most important information.** **Ensure unified information/design** across the leading/trailing elements (consistent color/typography) despite the TrueDepth camera split. **Keep content as narrow as possible, snug against the TrueDepth camera** — don't obscure the status bar, no padding against the camera, keep leading/trailing balanced in size. **Link to relevant app content** — both elements should link to the same screen on tap.
  - Minimal: **Ensure your Live Activity is recognizable** — prefer updated information over a static logo where possible.
  - Expanded: **Maintain relative placement of elements** for a coherent expand from compact/minimal. **Wrap content tightly around the TrueDepth camera.**
  - Lock Screen: **Don't replicate notification layouts** — create a layout unique to the Live Activity's information. **Choose colors that work well on a personalized Lock Screen** — use custom background/tint and opacity sparingly. **Ensure good contrast in Dark Mode and Always-On** — default uses light background in light appearance, dark in dark appearance; verify custom colors on Always-On reduced-luminance devices. **Verify the generated dismiss-button color** matches your design (adjust via `activitySystemActionForegroundColor(_:)`). **Use standard margins (14 pt)** to align with notifications; avoid crowding edges.
  - StandBy: **Update your layout for StandBy** — assets should look great at larger scale; consider a custom layout using the extra space. **Consider using the default background color** — blends with the device bezel, softer look, and lets the system scale the activity slightly larger (no camera-margin accounting needed). **Use standard margins, avoid extending graphics to the screen edge** (else content feels cut off/broken). **Verify your design in Night Mode** — the system applies a red tint; check for sufficient contrast.
- **CarPlay:** system combines compact's leading/trailing elements into a single layout on CarPlay Dashboard; the same design applies to Apple Watch, so design for both — interactive elements are deactivated in CarPlay. **Consider a custom layout** (declare `ActivityFamily.small`) if larger text/more info would help. **Carefully consider buttons/toggles** — since interactivity is deactivated in CarPlay, prefer timely content over controls if people may observe while driving.
**Platforms:** No additional considerations for iOS or iPadOS. Not supported in tvOS or visionOS.
- macOS: active Live Activities appear automatically in the Menu bar (compact, minimal, expanded presentations); clicking launches iPhone Mirroring to display the app.
- watchOS: appears at the top of the Smart Stack, by default combining the compact presentation's leading/trailing elements; tapping opens the watchOS app if present, otherwise a full-screen view with a button to open the app on the paired iPhone. **Consider creating a custom watchOS layout** — can show more info and add interactivity (button/toggle). **Carefully consider buttons/toggles** — the custom watchOS layout also applies to CarPlay (where interactivity is deactivated), so omit them if people may observe while driving. **Focus on essential information and significant updates** — progress (e.g. delivery ETA), interactive elements (stopwatch/timer controls), significant updates (e.g. score changes).

### Specifications
CarPlay Live Activity sizes (pt): 240x78, 240x100, 170x78. Test with CarPlay simulator's Smart Display Zoom configurations: Widescreen 1920x720, Portrait 900x1200, Standard 800x480.

iOS dimensions (pt):

| Screen dimensions (portrait) | Compact leading | Compact trailing | Minimal (width range) | Expanded (height range) | Lock Screen (height range) |
|---|---|---|---|---|---|
| 430x932 | 62.33x36.67 | 62.33x36.67 | 36.67–45x36.67 | 408x84–160 | 408x84–160 |
| 393x852 | 52.33x36.67 | 52.33x36.67 | 36.67–45x36.67 | 371x84–160 | 371x84–160 |

Dynamic Island corner radius: 44 pt, matching the TrueDepth camera shape.

| Presentation type | Device | Dynamic Island width (pt) |
|---|---|---|
| Compact or minimal | iPhone 17 Pro Max / iPhone Air / iPhone 16 Pro Max / iPhone 16 Plus / iPhone 15 Pro Max / iPhone 15 Plus | 250 |
| Compact or minimal | iPhone 17 Pro / iPhone 17 / iPhone 16 Pro / iPhone 16 / iPhone 15 Pro / iPhone 15 / iPhone 14 Pro Max / iPhone 14 Pro | 230 |
| Expanded | iPhone 17 Pro Max / iPhone Air / iPhone 16 Pro Max / iPhone 16 Plus / iPhone 15 Pro Max / iPhone 15 Plus / iPhone 14 Pro Max | 408 |
| Expanded | iPhone 17 Pro / iPhone 17 / iPhone 16 Pro / iPhone 16 / iPhone 15 Pro / iPhone 15 / iPhone 14 Pro | 371 |

iPadOS dimensions (pt) — Lock Screen height given as a range:

| Screen dimensions (portrait) | Lock Screen (height range) |
|---|---|
| 1366x1024 | 500x84–160 |
| 1194x834 | 425x84–160 |
| 1012x834 | 425x84–160 |
| 1080x810 | 425x84–160 |
| 1024x768 | 425x84–160 |

macOS: use the provided iOS dimensions.

watchOS: Live Activities in the Smart Stack use the same dimensions as watchOS widgets.

| Apple Watch size | Size in Smart Stack (pt) |
|---|---|
| 40mm | 152x69.5 |
| 41mm | 165x72.5 |
| 44mm | 173x76.5 |
| 45mm | 184x80.5 |
| 49mm | 191x81.5 |

## Notifications
Source: https://developer.apple.com/design/human-interface-guidelines/notifications
A notification gives people timely, high-value information they can understand at a glance. Consent is required before sending any (`Asking permission to use notifications`); people configure styles and delivery timing per urgency level in Settings.
Anatomy: banner/view on Lock Screen, Home Screen, Home View, or desktop; a badge on the app icon; an item in Notification Center. Direct-communication notifications (calls, messages) use a distinct interface featuring prominent contact avatars and group names instead of the app icon.
- **Provide concise, informative notifications** — people want quick, valuable updates.
- **Avoid sending multiple notifications for the same thing**, even without a response — fills Notification Center and risks people disabling all your notifications.
- **Avoid telling people to perform specific tasks within your app** — offer Notification actions instead if a simple task is possible; instructions are hard to remember after dismissal.
- **Use an alert, not a notification, to display an error message** — avoid confusing the two components.
- **Handle notifications gracefully when your app is foregrounded** — notifications don't appear, but the info still arrives; present it discoverably but non-disruptively (e.g. badge increment, subtle insertion into the current view) rather than as a distracting notification.
- **Avoid including sensitive, personal, or confidential information** — you can't predict who might see it.
- Content: **Create a short title only if it provides context** — prefer brief, at-a-glance titles (especially on Apple Watch); if only a generic title is possible for a noncommunication notification, let the system show the app name instead. Use title-style capitalization, no ending punctuation. **Write succinct, easy-to-read content** — complete sentences, sentence case, proper punctuation; don't truncate manually (the system does it automatically). **Provide generically descriptive placeholder text** for when previews are hidden (e.g. "Friend request," "New comment," "Reminder," "Shipment") via `hiddenPreviewsBodyPlaceholder`, using sentence-style capitalization. **Avoid including your app name or icon** — the system displays these automatically (large app icon at leading edge; sender's avatar badged with a small icon for communication notifications). **Consider providing a sound** — custom sounds should be short, distinctive, professionally produced; don't rely on sound to communicate important information since people may not hear it, and a vibration can't be added programmatically.
- Notification actions (up to four buttons for in-place task completion): **Provide beneficial, contextually sensible actions** — short, title-case labels describing the result, no app name/extraneous info, brief enough to avoid truncation, localized. **Avoid an action that merely opens your app** — redundant with tapping the notification itself. **Prefer nondestructive actions** — if a destructive action is necessary, ensure enough context to avoid unintended consequences (the system styles destructive actions distinctly). **Provide a simple, recognizable interface icon for each action**, shown on the trailing side of the action title.
- Badging (a small filled oval with a number on the app icon showing unread-notification count): **Use a badge only to show unread notification count** — never unrelated numeric data (weather, dates/times, stock prices, scores). **Don't rely on badging as the sole method of communicating essential information** — people can disable badges. **Keep badges up to date** — update as soon as notifications are addressed (reducing count to zero removes all related items from Notification Center). **Avoid creating a custom element that mimics a badge's appearance/behavior.**
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS.
- watchOS: notifications occur in two stages — **short look** (appears while wrist is raised, disappears when lowered) and **long look** (more detail, scrollable via swipe/Digital Crown, dismissed by tap or lowering the wrist); people can also view them in Notification Center, and double-tap to respond on supported devices. If a companion iPhone app supports notifications, watchOS can auto-provide default short/long-look interfaces.
  - Short look: **Avoid using it as the only way to communicate important information** — it appears only briefly. **Keep privacy in mind** — provide only basic, non-sensitive title information.
  - Long look: available as **static** (message plus additional static text/images) or **dynamic** (full content access, more configuration options); system-defined structure includes a sash at top and a Dismiss button at the bottom, below custom buttons — you can't change the overall structure. **Consider a rich custom long-look interface** using SwiftUI Animations, SpriteKit, or SceneKit. **At minimum provide a static interface; prefer providing dynamic too** — system falls back to static when dynamic is unavailable (no network, iPhone companion unreachable); package static-interface resources with the app in advance. **Choose a background appearance for the sash** — customizable color or blurred appearance (blurred works well over a photo in the content area). **Choose a background color for the content area** — default is transparent; use white at 18% opacity to match other system notifications, or a custom/brand color. **Provide up to four custom actions below the content area** — Dismiss always appears last, below custom buttons; iPhone-companion-registered actionable notification types configure the buttons if applicable.
  - Double tap: responds using the **first nondestructive action** in the list. **Keep this in mind when ordering custom actions** — place the most frequently used action first (e.g., a parking app's "extend by 5/15/60 minutes" options, most common first).

## Snippets
Source: https://developer.apple.com/design/human-interface-guidelines/snippets
When someone performs a task via Siri or an App Shortcut, a snippet — a compact view appearing in response to actions taken via Siri, Spotlight, or the Shortcuts app — shows the result or asks for confirmation. Presented via an App Intent designed for the specific task.
Use for: two types — **confirmation** (lets people confirm or cancel an action, may include options affecting the result) and **result** (provides information, possibly the outcome of a confirmation, needing no further action). Every snippet-displaying app intent shows a result; the confirmation step is optional.
Anatomy: **Dialogue** (the app intent dialogue Siri speaks; shown by default above the custom view), **Custom view** (visually communicates the snippet's information; can include buttons for modifying content, more info, or another action), **System-provided button(s)** (confirmation snippet: secondary Cancel + primary customizable-label button; result snippet: single Done button that dismisses the view).
- **Ensure legibility** — sufficient contrast between custom content and system background in both light/dark appearances; keep consistent content margins.
- **Keep content concise** — custom views must be no taller than a 400-point maximum height; account for Dynamic Type scaling; for a result snippet needing more detail, deep-link to in-app content rather than cramming it into the custom view.
- **Choose a descriptive label for a confirmation snippet's primary button** — e.g. "Order" is clearer than "OK"/"Proceed" for an order-coffee snippet; system default is "Continue" if unspecified.
- **Communicate a snippet's purpose visually** — don't rely on the dialogue text (essential for non-visual interactions) to convey purpose; prefer omitting it from the visual representation and using the custom view instead.
**Platforms:** No additional considerations for iOS, iPadOS, or macOS. Not supported in tvOS, visionOS, or watchOS.

## Status Bars
Source: https://developer.apple.com/design/human-interface-guidelines/status-bars
A status bar appears along the upper edge of the screen and displays information about the device's current state, like the time, cellular carrier, and battery level.
- **Obscure content under the status bar** — its background is transparent by default, so content can show through and confuse people into thinking they can interact with it; keep the status bar readable and don't imply the content behind is interactive. Prefer a scroll edge effect to place a blurred view behind the status bar (`ScrollEdgeEffectStyle`, `UIScrollEdgeEffect`).
- **Consider temporarily hiding the status bar when displaying full-screen media** for a more immersive experience (e.g., Photos hides it when browsing full-screen photos).
- **Avoid permanently hiding the status bar** — people need it to check the time or connection status; let people redisplay it with a simple, discoverable gesture (e.g., a single tap in Photos).
**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## Top Shelf
Source: https://developer.apple.com/design/human-interface-guidelines/top-shelf
The Apple TV Home Screen provides an area called Top Shelf, which showcases your content in a rich, engaging way while also giving people access to favorite apps in the Dock; supporting full-screen Top Shelf lets people swipe through multiple full-screen content views, play trailers/previews, and get more info. System-defined layout templates (downloadable from Apple Design Resources) help position content.
- **Help people jump right into your content** — the Carousel actions and Carousel details templates each include a primary Play button and a More Info button by default.
- **Feature new content** — showcase new releases/episodes, upcoming movies/shows; avoid promoting already purchased/rented/watched content.
- **Personalize people's favorite content** — targeted recommendations, resuming playback, or jumping back into active gameplay.
- **Avoid showing advertisements or prices** — people already chose your app; prefer focusing on new/exciting content, and show prices only when people show interest.
- **Showcase compelling dynamic content** to draw people in; static images are acceptable as a fallback but dynamic is preferred; use Layered images for a captivating experience.
- **If not providing recommended full-screen content, supply at least one static image as a fallback** — displayed when the app is in the Dock/focus and full-screen content is unavailable; tvOS flips and blurs it to fit a 1920 px width at 16:9. Size: 2320x720 pt (2320x720 px @1x, 4640x1440 px @2x).
- **Avoid implying interactivity in a static image** — it isn't focusable.
- Dynamic layouts can appear as: a carousel of full-screen video/images with two buttons and optional details; a row of focusable content; a set of scrolling banners.
  - **Carousel actions:** full-screen video/images with a few unobtrusive controls; works well for content people already know (e.g. user-generated photos, franchise/show content). **Provide a title** — succinct title (show/movie/album title) and optionally a brief subtitle (e.g. date range, episode's show name).
  - **Carousel details:** extends carousel actions with content info (plot summary, cast list, metadata). **Provide a title identifying the currently playing content** near the top of the screen; optionally a phrase/app attribution above it (e.g. "Featured on *My App*").
  - **Sectioned content row:** a single labeled row of focusable, sectioned content (recent, new, favorites); a label appears on focus; small remote Touch-surface movements animate the focused image; can show multiple labels. **Provide enough content to constitute a complete row** — at minimum, span the full screen width; include at least one label for consistency/context.
    - Poster (2:3): Actual 404x608 pt (404x608 px @1x, 808x1216 px @2x); Focused/Safe zone 380x570 pt (380x570 px @1x, 760x1140 px @2x); Unfocused 333x570 pt (333x570 px @1x, 666x1140 px @2x).
    - Square (1:1): Actual 608x608 pt (608x608 px @1x, 1216x1216 px @2x); Focused/Safe zone 570x570 pt (570x570 px @1x, 1140x1140 px @2x); Unfocused 500x500 pt (500x500 px @1x, 1000x1000 px @2x).
    - 16:9: Actual 908x512 pt (908x512 px @1x, 1816x1024 px @2x); Focused/Safe zone 852x479 pt (852x479 px @1x, 1704x958 px @2x); Unfocused 782x440 pt (782x440 px @1x, 1564x880 px @2x).
    - **Be aware of additional scaling when combining image sizes** — images auto-scale up to match the tallest image's height (e.g. a 16:9 image scales to 500 px high alongside a poster/square image).
  - **Scrolling inset banner:** a series of large images nearly spanning the screen width; Apple TV auto-scrolls on a preset timer until brought into focus, circling back after the final image; small circular Touch-surface gesture triggers the system focus effect (animation, lighting, 3D effect for layered images); swiping pans to next/previous. **Provide three to eight images** — minimum three for effectiveness, more than eight makes navigation hard. **If you need text, add it to the image** — this layout doesn't show labels under content; place text on a dedicated layer above others in layered images, and add it to the image's accessibility label for VoiceOver.
    - Size: Actual 1940x692 pt (1940x692 px @1x, 3880x1384 px @2x); Focused/Safe zone 1740x620 pt (1740x620 px @1x, 3480x1240 px @2x); Unfocused 1740x560 pt (1740x560 px @1x, 3480x1120 px @2x).
**Platforms:** Not supported in iOS, iPadOS, macOS, visionOS, or watchOS (tvOS-only component).

## Watch Faces
Source: https://developer.apple.com/design/human-interface-guidelines/watch-faces
A watch face is the view people choose as their primary view in watchOS, customized with favorite complications; different faces can be configured for different activities/contexts. Since watchOS 7, people can share configured watch faces (via the Watch app, website, Messages, Mail, or social media) — recipients get the custom experience (including complications) without configuring it themselves, and are prompted to install the app if not already installed.
- **Help people discover your app by sharing watch faces that feature your complications** — ideally supporting multiple complications for a curated showcase; some faces let you also specify a system accent color, images, or styles.
- **Display a preview of each watch face you share** — get one via the iOS Watch app (email the face to yourself); the preview includes an illustrated device bezel suitable for websites/apps, or you can composite a high-fidelity hardware bezel from Apple Design Resources instead.
- **Aim to offer shareable watch faces for all Apple Watch devices** — some faces (California, Chronograph Pro, Gradient, Infograph, Infograph Modular, Meridian, Modular Compact, Solar Dial) require Series 4+; Explorer requires Series 3 (cellular)+. If using one of these, consider also offering a similar configuration on a face compatible with Series 3 and earlier, and clearly label each shareable face with its supported devices.
- **Respond gracefully if people choose an incompatible watch face** — the system errors on Series 3 or earlier for incompatible faces; consider immediately offering an alternative compatible configuration instead of showing an error, and use previews to set expectations about receiving an alternative face.
**Platforms:** Not supported in iOS, iPadOS, macOS, tvOS, or visionOS (watchOS-only component).

## Widgets
Source: https://developer.apple.com/design/human-interface-guidelines/widgets
A widget provides quick access to essential information and focused interactions from your app or game in additional contexts, appearing across platforms: Home Screen/Lock Screen (iPhone, iPad), desktop/Notification Center (Mac), horizontal/vertical surfaces (Apple Vision Pro), and a fixed Smart Stack position (Apple Watch).
Design considerations: the widget size to support; the context (devices/system experiences) it may appear in; the rendering modes/color treatment it receives based on size and context. WidgetKit provides default appearances per size/context, but a custom design tailored to context is worth considering.

### System family widgets — supported contexts
| Widget size | iPhone | iPad | Mac | Apple Vision Pro |
|---|---|---|---|---|
| System small | Home Screen, Today View, StandBy, and CarPlay | Home Screen, Today View, and Lock Screen | Desktop and Notification Center | Horizontal and vertical surfaces |
| System medium | Home Screen and Today View | Home Screen and Today View | Desktop and Notification Center | Horizontal and vertical surfaces |
| System large | Home Screen and Today View | Home Screen and Today View | Desktop and Notification Center | Horizontal and vertical surfaces |
| System extra large | Not supported | Home Screen and Today View | Desktop and Notification Center | Horizontal and vertical surfaces |
| System extra large portrait | Not supported | Not supported | Not supported | Horizontal and vertical surfaces |

### Accessory widgets — supported devices
| Widget size | iPhone | iPad | Apple Watch |
|---|---|---|---|
| Accessory circular | Lock Screen | Lock Screen | Watch complications and in the Smart Stack |
| Accessory corner | Not supported | Not supported | Watch complications |
| Accessory inline | Lock Screen | Lock Screen | Watch complications |
| Accessory rectangular | Lock Screen | Lock Screen | Watch complications and in the Smart Stack |

### Appearances and rendering modes
A widget can appear full-color, monochrome-with-tint, or clear/translucent, depending on location/device/customization.
- Home Screen (iPhone/iPad): people choose light, dark, clear, and tinted appearances. Light/dark = full-color design. Clear = desaturated, translucent, with highlights and Liquid Glass material. Tinted = desaturated content plus the person's selected tint color.
- Apple Vision Pro: appears as a 3D object surrounded by a frame, full-color with a glass- or paper-like coating that responds to lighting; people can choose a tinted appearance from system-provided palettes.
- Lock Screen (iPad): monochromatic, no tint color.
- Lock Screen (iPhone in StandBy): scaled up, background removed; below an ambient-light threshold, renders monochromatic with a red tint.
- Rectangular accessory on Lock Screen (iPhone/iPad): monochromatic, no tint. On Apple Watch: full-color or tinted as a complication, and can appear in the Smart Stack.
- Rendering modes: **fullColor** — used for system family widgets on all platforms; doesn't change view colors. **accented** — used for system family widgets on all platforms and accessory widgets on Apple Watch; removes the background, replaces with a tinted-color effect (tinted appearance) or Liquid Glass background (clear appearance); divides views into an accent group and a primary group, each tinted a solid color. **vibrant** — used on iPhone/iPad Lock Screen and iPhone StandBy in low light; desaturates text/images/gauges and creates a vibrant coloring effect suited to the Lock Screen background or macOS desktop (customizable tint on Lock Screen; red tint for StandBy low-light).

| Platform | Full-color | Accented | Vibrant |
|---|---|---|---|
| iPhone | Home Screen, Today view, StandBy and CarPlay (background removed) | Home Screen and Today view | Lock Screen, StandBy in low-light conditions |
| iPad | Home Screen and Today view | Home Screen and Today view | Lock Screen |
| Apple Watch | Smart Stack, complications | Smart Stack, complications | Not supported |
| Mac | Desktop and Notification Center | Not supported | Desktop |
| Apple Vision Pro | Horizontal and vertical surfaces | Horizontal and vertical surfaces | Not supported |

- **Choose simple ideas that relate to your app's main purpose** — timely content and relevant functionality (e.g. Weather widgets prioritize current high/low/conditions).
- **Aim to create a widget that gives quick access to wanted content** — meaningful content, useful actions, and deep links; replicating the app icon offers little value.
- **Prefer dynamic information that changes throughout the day** — unchanging content risks removal, even though widgets don't update minute-to-minute.
- **Look for opportunities to surprise and delight** (e.g. a unique visual treatment for a calendar widget on birthdays/holidays).
- **Offer widgets in multiple sizes only when it adds value** — small widgets typically show one piece of information, larger sizes support more layers; avoid just stretching a smaller widget's content to fill a larger area; prioritize creating one well-suited size over all sizes.
- **Balance information density** — sparse layouts feel unnecessary; overly dense ones aren't glanceable; use a larger size or graphics over text if too dense.
- **Display only information directly related to the widget's main purpose** — larger sizes can show more/more-detailed data without losing focus (e.g. all Calendar widget sizes stay centered on upcoming events).
- **Use brand elements thoughtfully** — colors, typefaces, stylized glyphs for recognizability without overpowering information; a small logo (top-right) is enough if the widget shows content from multiple sources.
- **Choose between automatic content and letting people customize it** — e.g., Stocks lets people pick tracked stocks; Podcasts auto-displays recent content.
- **Avoid mirroring your widget's appearance within your app** — confuses expectations about behavior.
- **Let people know when authentication adds value** (e.g. "Sign in to view reservations" when signed out).
- Updating content: widgets refresh periodically, not continuously/real-time; system may adjust update limits. **Keep your widget up to date** — match update frequency to how often data changes and when people need to see it (e.g. hourly tide-condition updates); if people check more often than you can update, show a last-updated timestamp. **Use system functionality to refresh dates/times** — preserves update opportunities; balance update frequency against showing stale content behind placeholders. **Use animated transitions to bring attention to data updates** — standard/custom animations up to two seconds.
- Interactivity: tapping/clicking launches the app by default; buttons/toggles offer functionality without launching (e.g. Reminders' completion toggle). **Offer simple, relevant functionality, reserve complexity for the app.** **Ensure interaction opens the app at the right location** — deep link directly to related details/actions. **Offer interactivity while remaining glanceable and uncluttered** — multiple targets (links, buttons, toggles) are fine but avoid app-like layouts; ensure confident tap/click targeting; inline accessory widgets support only one tap target.
- Margins and padding: **In general, use standard margins for legibility** — 16 points for most widgets; tighter margins of 11 points can work for content groupings (graphics, buttons, background shapes); note smaller margins apply on Mac desktop and Lock Screen/StandBy. **Coordinate content corner radius with the widget's corner radius** via `ContainerRelativeShape`.
- Text: **Prefer the system font, text styles, and SF Symbols** for cross-platform fit and easy great-looking text; use a custom font sparingly (e.g. for large text only, pairing with SF Pro for smaller text). **Avoid very small font sizes** — generally 11 points or larger. **Avoid rasterizing text** — use text elements/styles so it scales and VoiceOver can read it.
  > Note: in iOS, iPadOS, and visionOS, widgets support Dynamic Type from Large to AX5 when using `Font` for system fonts or `custom(_:size:)` for custom fonts.
- Color: **Use color to enhance appearance without competing with content** — specify asset-catalog colors for the widget's editing-mode UI too. **Convey meaning without relying on specific colors** — widgets can appear monochromatic, and watchOS may invert colors per chosen face; use text/iconography alongside color. **Use full-color images judiciously** — tinted/clear appearances desaturate full-color images by default; opting into full-color rendering draws special attention and can look out of place (e.g. in a clear appearance); reserve for media content (e.g. album art) at dimensions smaller than the widget size.
- Rendering modes detail: **Full-color** — support light and dark appearances, preferring light backgrounds in light mode / dark in dark mode, using semantic system colors or asset-catalog color variants. **Accented** — group components into an accent group and a primary group; iPhone/iPad/Mac tint both white; Apple Watch tints primary white and accented in the watch face's color. **Vibrant** — offer enough contrast for legibility: pixel opacity controls blurred-background material strength (fully transparent lets background material show through); pixel brightness controls vibrancy strength on the Lock Screen (brighter = more contrast). **Create optimized assets** — render images/numbers/text at full opacity; use white/light gray for prominent content, darker grayscale for secondary, to establish hierarchy; use opaque grayscale values (not white opacities) for best vibrant effect.
- Previews and placeholders: **Design a realistic gallery preview** — real data is fine, or realistic simulated data if real data is slow to generate/load. **Design placeholder content that helps recognize your widget** — combine static components with semi-opaque shapes standing in for dynamic content (rectangles for text lines, circles/squares for glyphs/images). **Write a succinct widget description** starting with an action verb (e.g. "See the current weather conditions and forecast for a location"); avoid self-referential phrases like "This widget shows…"; use approachable, sentence-style language. **Group your widget's sizes together with a single description** — avoid implying each size is a different widget. **Consider coloring the Add button** shown below your widget group in the gallery, for brand reinforcement.

**Platforms:** No additional considerations for macOS. Not supported in tvOS.
- iOS, iPadOS: Lock Screen widgets are functionally similar to watch complications and should follow Complications guidance too — a complications design often works well for Lock Screen widgets and vice versa, so consider designing them in tandem. Three shapes: inline text above the clock, circular and rectangular below the clock. **Support the Always-On display on iPhone** — use gray levels with enough contrast at reduced luminance. **Offer Live Activities to show real-time updates** — widgets don't support real-time info; for time-limited, frequently updated progress tracking, offer a Live Activity instead (shares underlying frameworks/design similarities with widgets — good to develop in tandem).
  - StandBy and CarPlay: system shows two small system-family widgets side by side, scaled up to fill the Lock Screen in StandBy; CarPlay uses the same small system-family widget with background removed, scaled to fit the Widgets screen grid — glanceable info and large text are especially important for CarPlay's car display. **Limit rich images/color to convey meaning in StandBy** — scale up and rearrange text for greater-distance glancing instead; don't use background colors (blend with the black background). In low light, StandBy widgets render monochromatic with a red tint.
- visionOS: widgets are 3D objects placed on horizontal/vertical surfaces, persisting across power cycles, at consistent real-world scale; size, mounting style, and treatment style affect perception. Appear full-color by default; accented rendering mode when tinted from system-provided palettes; no systemwide light/dark appearance (though individual widgets, like Music's poster widget, may offer their own light/dark theme option). **Adapt design/content for the spatial experience** — think of widgets as part of a room's surroundings (e.g. Music's poster-like appearance vs. a small desk-fit productivity widget). **Test across the full range of system color palettes and lighting conditions** for consistent tone/contrast/legibility; verify untinted elements stay legible in every tint palette if excluding elements from tinting.
  - Thresholds and sizes: two key thresholds — **simplified** (viewed at a distance) and **default** (viewed nearby). **Design a responsive layout for each threshold** — simplified: fewer details, larger type, no interactive elements; default: more details, smaller type; maintain shared elements across both for continuity. **Offer widget family sizes that fit a person's surroundings** — map to real-world dimensions and permanent spatial placement (e.g. small for a desk, extra large for wall art/photography). **Display content legibly across a range of distances** — people can scale a widget 75–125%; use print-design principles (hierarchy, typography, scale) and high-resolution assets.
  - Mounting styles: **elevated** (default; works on horizontal surfaces — tilts back, casts a soft shadow — and vertical surfaces — sits flush like a picture frame) and **recessed** (vertical surfaces only — content set back for a cutout/depth illusion). **Choose the mounting style fitting your content** — elevated for content that should stand out/feel present (reminders, media, glanceable data); recessed for immersive/ambient content (weather, editorial), vertical-surface only. A widget can opt out of a style; if only recessed is supported, horizontal placement isn't available.
    > Developer note: use `supportedMountingStyles(_:)` on `WidgetConfiguration` to declare elevated, recessed, or both; create separate widget configurations if different widgets in your app need different supported-style combinations.
    **Test elevated designs with each system-provided frame width** — layout can't change based on the chosen width, so ensure visual balance for each.
  - Treatment styles: **paper** (grounded, print-like; darkens/lightens with ambient lighting; e.g. Music poster widget displaying albums/playlists like framed artwork) and **glass** (lighter, layered look separating foreground/background for clarity/contrast; foreground stays bright/legible regardless of ambient light; e.g. a News widget with print-like background imagery and crisp foreground headlines). **Choose paper for a print-like, ambient-responsive look. Choose glass for information-rich widgets** needing consistent foreground legibility.
- watchOS: **Provide a colorful background that conveys meaning** — default is black; consider a custom color with added meaning (e.g. Stocks: red for falling, green for rising values). **Encourage the system to display/elevate your widget's Smart Stack position** via relevancy information (location-based or tied to ongoing system actions like a workout) using `RelevanceKit`.

### Specifications
iOS dimensions (pt):

| Screen size (portrait, pt) | Small | Medium | Large | Circular | Rectangular | Inline |
|---|---|---|---|---|---|---|
| 430×932 | 170x170 | 364x170 | 364x382 | 76x76 | 172x76 | 257x26 |
| 428x926 | 170x170 | 364x170 | 364x382 | 76x76 | 172x76 | 257x26 |
| 414x896 | 169x169 | 360x169 | 360x379 | 76x76 | 160x72 | 248x26 |
| 414x736 | 159x159 | 348x157 | 348x357 | 76x76 | 170x76 | 248x26 |
| 393x852 | 158x158 | 338x158 | 338x354 | 72x72 | 160x72 | 234x26 |
| 390x844 | 158x158 | 338x158 | 338x354 | 72x72 | 160x72 | 234x26 |
| 375x812 | 155x155 | 329x155 | 329x345 | 72x72 | 157x72 | 225x26 |
| 375x667 | 148x148 | 321x148 | 321x324 | 68x68 | 153x68 | 225x26 |
| 360x780 | 155x155 | 329x155 | 329x345 | 72x72 | 157x72 | 225x26 |
| 320x568 | 141x141 | 292x141 | 292x311 | N/A | N/A | N/A |

iPadOS dimensions (pt) — Canvas and Device values per screen size:

| Screen size (portrait, pt) | Target | Small | Medium | Large | Extra large |
|---|---|---|---|---|---|
| 768x1024 | Canvas | 141x141 | 305.5x141 | 305.5x305.5 | 634.5x305.5 |
| 768x1024 | Device | 120x120 | 260x120 | 260x260 | 540x260 |
| 744x1133 | Canvas | 141x141 | 305.5x141 | 305.5x305.5 | 634.5x305.5 |
| 744x1133 | Device | 120x120 | 260x120 | 260x260 | 540x260 |
| 810x1080 | Canvas | 146x146 | 320.5x146 | 320.5x320.5 | 669x320.5 |
| 810x1080 | Device | 124x124 | 272x124 | 272x272 | 568x272 |
| 820x1180 | Canvas | 155x155 | 342x155 | 342x342 | 715.5x342 |
| 820x1180 | Device | 136x136 | 300x136 | 300x300 | 628x300 |
| 834x1112 | Canvas | 150x150 | 327.5x150 | 327.5x327.5 | 682x327.5 |
| 834x1112 | Device | 132x132 | 288x132 | 288x288 | 600x288 |
| 834x1194 | Canvas | 155x155 | 342x155 | 342x342 | 715.5x342 |
| 834x1194 | Device | 136x136 | 300x136 | 300x300 | 628x300 |
| 954x1373 * | Canvas | 162x162 | 350x162 | 350x350 | 726x350 |
| 954x1373 * | Device | 162x162 | 350x162 | 350x350 | 726x350 |
| 970x1389 * | Canvas | 162x162 | 350x162 | 350x350 | 726x350 |
| 970x1389 * | Device | 162x162 | 350x162 | 350x350 | 726x350 |
| 1024x1366 | Canvas | 170x170 | 378.5x170 | 378.5x378.5 | 795x378.5 |
| 1024x1366 | Device | 160x160 | 356x160 | 356x356 | 748x356 |
| 1192x1590 * | Canvas | 188x188 | 412x188 | 412x412 | 860x412 |
| 1192x1590 * | Device | 188x188 | 412x188 | 412x412 | 860x412 |

visionOS dimensions:

| Widget | Size in pt | Size in mm (scaled to 100%) |
|---|---|---|
| Small | 158x158 | 268x268 |
| Medium | 338x158 | 574x268 |
| Large | 338x354 | 574x600 |
| Extra large | 450x338 | 763x574 |
| Extra large portrait | 338x450 | 574x763 |

watchOS dimensions:

| Apple Watch size | Size of a widget in the Smart Stack (pt) |
|---|---|
| 40mm | 152x69.5 |
| 41mm | 165x72.5 |
| 44mm | 173x76.5 |
| 45mm | 184x80.5 |
| 49mm | 191x81.5 |
