# HIG — Technologies (Live Photos … Wallet)
live-photos, mac-catalyst, machine-learning, maps, nfc, photo-editing, researchkit, shareplay, shazamkit, sign-in-with-apple, siri, tap-to-pay-on-iphone, voiceover, wallet

## Live Photos
Source: https://developer.apple.com/design/human-interface-guidelines/live-photos
Live Photos lets people capture favorite memories in a sound- and motion-rich interactive experience that adds vitality to traditional still photos.
- **Apply adjustments to all frames.** If your app lets people apply effects/adjustments to a Live Photo, apply them to the entire photo; if unsupported, offer to convert it to a still photo.
- **Keep Live Photo content intact.** Don't disassemble a Live Photo and present its frames or audio separately; use a consistent visual treatment and interaction model across apps.
- **Implement a great photo sharing experience.** Let people preview the entire contents of a Live Photo before sharing; always offer the option to share it as a traditional photo.
- **Clearly indicate when a Live Photo is downloading and when it's playable.** Show a progress indicator during download and indicate when it completes.
- **Display Live Photos as traditional photos in environments that don't support Live Photos.** Don't attempt to replicate the experience — show a still representation instead.
- **Make Live Photos easily distinguishable from still photos.** Best identified through a hint of movement; since there are no built-in Live Photo motion effects outside the Photos app's full-screen browser, design custom motion effects. Where movement isn't possible, show a system-provided badge (with or without text); never include a playback button that could be read as a video playback control.
- **Keep badge placement consistent** — same location on every photo, typically a corner.

**Platforms:** visionOS — people can view a Live Photo but can't capture one. Not supported in watchOS. No additional considerations for iOS, iPadOS, macOS, or tvOS.

## Mac Catalyst
Source: https://developer.apple.com/design/human-interface-guidelines/mac-catalyst
Mac Catalyst lets you create a Mac version of your iPad app so people can enjoy the experience in a new environment.
- Good candidates already support drag and drop, keyboard navigation/shortcuts, multitasking (Split View, Slide Over, Picture in Picture), and multiple windows/scenes on iPad — these translate directly to the Mac.
- Apps relying on capabilities unavailable on Mac (gyroscope, accelerometer, rear camera, HealthKit, ARKit) or whose primary function is marking, handwriting, or navigation may not suit Mac Catalyst.
- Mac Catalyst automatically provides fundamental macOS features: pointer interactions, keyboard-based focus/navigation, window management, toolbars, rich text and contextual menus, file management, menu bar menus, and Settings app integration. System-provided UI (split view, file browser, activity view, form sheet, contextual actions, color picker) automatically takes on a Mac-like appearance.
- **Choose an idiom.** Xcode defaults to "Scale Interface to Match iPad" (iPad idiom): keeps layout consistent with minimal changes, but scales views/text down to 77% (e.g., 17pt iPadOS text renders at 13pt). The Mac idiom renders text/artwork at 100% for more detail and possibly better performance/lower power, but requires a layout audit and rework.
- **When adopting the Mac idiom, thoroughly audit and plan changes to your layout** — consider a separate asset catalog for Mac-specific assets.
- **Adjust font sizes as needed** — use text styles and avoid fixed font sizes, since Mac idiom text renders at 100% and can look oversized.
- **Make sure views and images look good in the Mac version** — Mac idiom renders iPadOS views at 100%, exposing more detail; avoid fixed view/layout sizes.
- **Limit appearance customizations to standard macOS customizations** similar to those available in iPadOS — not all iPadOS control customizations exist on macOS.
- **Navigation:** if your iPad app uses a tab bar, use a split view with a sidebar (streamlines navigation, keeps iPad/Mac layouts consistent) or a segmented control (works well for flat hierarchies) instead; in general prefer a split view over a segmented control.
- **Retain access to important tab-bar items** by listing them in the macOS View menu regardless of which replacement you use.
- **Offer multiple ways to move between pages** — Next/Previous buttons in addition to swipe/trackpad gestures, for pointer- and keyboard-only Mac users.
- Most iPadOS gestures convert automatically to mouse/trackpad interactions:

| iPadOS gesture | → Mouse | → Trackpad |
|---|---|---|
| Tap | Left or right click | Click |
| Touch and hold | Click and hold | Click and hold |
| Pan | Left click and drag | Click and drag |
| Pinch | — | Pinch |
| Rotate | — | Rotate |

> Note: the two touches in pinch/rotate gestures are sent to the view under the pointer, not the view under each touch.
- **Create a macOS version of your app icon** using the lifelike rendering style macOS users expect while keeping cross-platform harmony.
- **Layout:** take advantage of the wider Mac screen — divide a single column into multiple columns, use regular-width/height size classes with side-by-side reflow, and present an inspector UI next to content instead of a popover.
- **Consider moving controls from the iPad main UI into the Mac app's toolbar**, listing associated commands in the menu bar.
- **Adopt a top-down flow** — put the most important actions/content near the top of the window; move iPad toolbar controls into the macOS window toolbar.
- **Relocate buttons from the side and bottom screen edges** — the iPad ergonomic rationale for edge placement doesn't apply on Mac.
- **Menus:** Mac users expect all commands in the persistent menu bar (unlike iPadOS, which has none). Pop-up/pull-down buttons and context menus in your iPad app automatically take on macOS appearance; look for additional places to support context menus (called "contextual" menu on Mac), since Mac users expect nearly every object to offer one.

**Platforms:** No additional considerations for iPadOS or macOS. Not supported in iOS, tvOS, visionOS, or watchOS.

## Machine learning
Source: https://developer.apple.com/design/human-interface-guidelines/machine-learning
Machine learning enables apps and games to learn from data and usage patterns, letting you improve existing experiences and create engaging new ones.
- Design models and UI together — model quality matters as much as UI quality; be prepared to change your use of data/metrics as the app experience evolves.
- First identify the role machine learning plays in your app, across five dimensions, to guide how you receive and display data:
  - **Critical or complementary:** if the app still works without the ML feature, it's complementary (e.g., QuickType); otherwise critical (e.g., Face ID). The more central a feature, the more people expect accurate/reliable results; secondary features get more forgiveness.
  - **Private or public:** the more sensitive the data, the more serious the consequences of inaccurate results (e.g., health app vs. music app) — regardless of sensitivity, always protect user privacy.
  - **Proactive or reactive:** proactive features provide unsolicited results (e.g., Siri Suggestions) and get less tolerance for low quality, so may need more data; reactive features respond to explicit requests/actions (e.g., QuickType).
  - **Visible or invisible:** visible features let people form reliability opinions via visible choices; invisible features (e.g., News topic suggestions) are harder to communicate reliability for or gather feedback on.
  - **Dynamic or static:** dynamic features improve live via interaction and often need calibration/feedback; static features improve only via app updates.
### Explicit feedback
Explicit feedback is information people provide in response to a specific app request (distinct from implicit signals like favoriting or social feedback, which serve the person's own goals).
- **Request explicit feedback only when necessary** — prefer implicit feedback first.
- **Always make providing explicit feedback voluntary**, never mandatory-feeling.
- **Use simple, direct language** for each option and its consequence — avoid vague terms like "dislike"; describe outcomes, e.g. "Suggest less pop music," "Mute politics for a week."
- **Add icons to an option description only if it helps** — never use an icon alone.
- **Consider offering multiple, progressively more specific options** to help people clarify their response.
- **Act immediately on explicit feedback and persist the change** everywhere in the app.
- **Consider using explicit feedback to fine-tune when/where you show results**, not just what.
### Implicit feedback
Implicit feedback arises from how people interact with your app's features, without extra effort from them.
- **Always secure people's information** gathered implicitly.
- **Help people control their information** — disclose how it's gathered/shared and let them restrict its flow; people may distrust apps they suspect of cross-app data sharing.
- **Don't let implicit feedback decrease exploration opportunities** — avoid over-reinforcing existing behavior at the cost of discovery.
- **Use multiple feedback signals when possible** to avoid misinterpreting a single ambiguous action's intent.
- **Consider withholding private or sensitive suggestions** — accounts/devices are often shared.
- **Prioritize recent feedback** over historical (e.g., Face ID prioritizes recent facial input); fall back to historical data if recent isn't available.
- **Update predictions on a cadence matching the person's mental model** — immediate for typing suggestions; not too frequent for song recommendations.
- **Be prepared for implicit feedback to shift when you change your UI**, even without a real behavior change.
- **Beware confirmation bias** — implicit feedback only reflects what people can currently see/do; don't rely on it solely.
### Calibration
Calibration is a process where people provide information a feature needs to function (e.g., scanning a face for Face ID).
- **Only use calibration when the feature truly can't function without it**; otherwise prefer implicit or explicit feedback.
- **Always secure people's information** collected during calibration.
- **Be clear about why you need the information** — emphasize what the feature does, not how it works.
- **Collect only the most essential information.**
- **Avoid asking people to calibrate more than once**, and do it early (exception: calibrating with a changing object rather than a person, e.g. a new baseball field).
- **Make calibration quick and easy** — prioritize a few important pieces and infer the rest; avoid requiring lookups or difficult actions.
- **Make sure people know how to calibrate successfully** — give an explicit goal and show progress.
- **Immediately provide assistance if progress stalls** — give actionable next steps, never imply fault.
- **Confirm success** — give a clear completion and a path into using the feature.
- **Let people cancel calibration at any time** without judgment or follow-up messaging.
- **Give people a way to update or remove calibration information**, ideally also outside the calibration flow.
### Mistakes
Every ML feature will make mistakes; anticipate them, help people handle them, and learn from them when it improves the app.
- Patterns for addressing mistakes: **limitations** (set expectations), **corrections** (let people fix wrong results), **attribution** (insight into where suggestions come from), **confidence** (gauge result quality), **feedback** (explicit/implicit reporting of mistakes).
- **Understand the significance of a mistake's consequences** and match corrective tools/empathy to its severity.
- **Make it easy to correct frequent or predictable mistakes**, or risk losing trust.
- **Continuously update the feature for evolving preferences/trends** to avoid mistakes, ideally without requiring user work.
- **Address mistakes without complicating the UI when possible** — weigh a pattern's UI impact against the risk of compounding the mistake (e.g., a wrong attribution magnifies the original error).
- **Be especially careful to avoid mistakes in proactive features** — people have less patience for unsolicited wrong suggestions and feel less in control.
- **Consider the effect of fixing one area's mistakes on overall accuracy elsewhere** (e.g., improving dog recognition may hurt cat recognition); be prepared for mistakes to evolve as models evolve.
### Corrections
People use corrections to fix mistakes an app makes.
- **Give people familiar, easy ways to make corrections** — show the steps/controls the app used so people can reuse them to refine or undo results.
- **Provide immediate value when people make a correction** — instantly display corrected content and persist the update.
- **Let people correct their corrections** — respond immediately and persist again.
- **Balance a feature's benefit against the effort required to correct it** — people abandon features that are easier to do manually.
- **Never rely on corrections to make up for low-quality results.**
- **Learn from corrections when it makes sense**, but confirm a correction will actually improve quality before using it to update models.
- **Prefer guided corrections** (suggest specific alternatives, less user effort) **over freeform corrections** (no suggested alternatives, more input) when possible; a combination can work too.
### Multiple options
- Contexts for offering multiple options: suggested (proactive, e.g. For You recommendations), requested (reactive, e.g. QuickType), and corrections (e.g. Photos Auto-Crop).
- **Prefer diverse options** over pure accuracy — balances relevance with helping people discover new things (e.g., Maps offering a scenic vs. no-toll vs. highway route).
- **In general, avoid providing too many options** — more options increase cognitive load; list options on one screen when possible.
- **List the most likely option first** — use confidence values and/or context (time, location) to rank; consider selecting the first option by default.
- **Make options easy to distinguish and choose** — brief descriptions highlighting differences; group into categories for rapid scanning when there are too many to show at once.
- **Learn from selections when it makes sense** to refine future ranking, without adversely affecting the experience; continuing to offer results people don't choose erodes trust.
### Confidence
Confidence indicates the measure of certainty for a result; not all models produce it by default.
- **Verify that confidence values correspond to result quality** before deciding whether to convey them to people at all.
- **Know what your confidence values mean before deciding how to present them** — low-quality results may be forgiven for critical/complementary features with attribution/context, but prominent presentation of low-quality results erodes trust.
- **Translate confidence values into concepts people already understand** rather than raw numbers (e.g., prefer "Because you listen to pop music" over "97% match").
- **Where attribution isn't helpful, rank/order results to imply confidence**, or express it via semantic categories (e.g., "high chance"/"low chance") rather than raw numbers.
- **In domains where people expect statistical info** (weather, sports, polling), display confidence values that aid interpretation.
- **Whenever possible, convey confidence via actionable suggestions** tied to people's goals (e.g., "This is a good time to buy") rather than percentages.
- **Consider changing presentation based on confidence thresholds** — e.g., show results directly at high confidence, ask for confirmation at lower confidence.
- **When confidence values are known to correlate with quality, avoid showing results when confidence is low** — especially for proactive/suggestion features, set a threshold below which you withhold results.
### Attribution
An attribution expresses the underlying basis for a result without explaining exactly how a model works.
- **Consider using attributions to help distinguish among multiple results**, encourage behavior change, minimize the impact of mistakes, build a mental model, or promote trust — decide your goal before adopting them.
- **Avoid being too specific or too general** — overly specific feels surveilled, overly general feels impersonal.
- **Keep attributions factual/objective** — never imply understanding or judgment of emotions/preferences/beliefs (e.g., "Because you've read nonfiction," not "Because you love nonfiction").
- **Avoid technical or statistical jargon**, except when the result itself is inherently statistical/technical (weather, sports, polling, science).
### Limitations
Every feature has limitations — things it can't do well, and things it can't do at all; a mismatch between expectations and reality can feel like a defect.
- **Help people establish realistic expectations** — describe rare-but-serious limitations upfront (marketing or in-feature context); attribution can help set expectations for minor limitations.
- **Demonstrate how to get the best results** — e.g. placeholder text suggesting valid input, real-time feedback while interacting (e.g. Memoji lighting/distance tips), or suggesting alternatives instead of showing no results.
- **Explain how limitations cause unsatisfactory results**, so the feature doesn't seem broken/intermittent (e.g., Memoji explains it doesn't work well in the dark).
- **Consider telling people when a limitation is resolved**, so they can update their mental model and return to previously avoided interactions.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Maps
Source: https://developer.apple.com/design/human-interface-guidelines/maps
A map displays outdoor or indoor geographical data in your app or on your website, supporting zooming, panning, rotation, annotations, overlays, and routing.
- **In general, make your map interactive** — people expect to zoom, pan, and interact; avoid noninteractive elements obscuring the map.
- **Pick a map emphasis style to suit your app:** *default* (fully saturated colors) suits standard map apps without much custom content and keeps visual alignment with the Maps app; *muted* (desaturated) suits apps with information-rich content that needs to stand out.
- **Help people find places** — offer search combined with category filters.
- **Clearly identify selected elements** — use distinct styling (outline, color variation).
- **Cluster overlapping points of interest** to improve legibility — clusters expand to reveal individual points as people zoom in.
- **Help people see the Apple logo and legal link** — okay if temporarily covered, but not always; use ~7pt padding on the sides and ~10pt above/below; keep the logo/link fixed to the map, not moving with your interface; if a custom element can move relative to the map, anchor the logo/link 10pt above its lowest resting position.
> Note: the Apple logo and legal link aren't shown on maps smaller than 200x100 pixels.
- **Use annotations that match your app's visual style** — default marker is red-tinted with a white pin; tint is changeable, and the icon can be a string (keep to 2–3 Unicode characters for readability) or an image/logo.
- **Consider making custom information related to standard map features independently selectable** — the system treats Apple-provided features (points of interest, territories, physical features) independently from your own annotations, letting you configure custom appearance/info for them when selected.
- **Use overlays to define map areas with a specific relationship to content:** *above roads* (default) sits above roads but below buildings/trees, showing what's underneath; *above labels* sits above roads and labels, hiding everything beneath — for content fully abstracted from map features.
- **Ensure enough contrast between custom controls and the map** — use a thin stroke, light drop shadow, or blend modes.
- **Place cards** display rich place info (hours, phone, address) and can appear directly in-map on selection, or for Apple-provided selectable map features (points of interest, territories, physical features).
> Important: if you don't display a place card directly within a map view, you must include a map in the place card.
- Place card styles: *automatic* (system picks based on map view size), *callout* (popover-style; *full* = large/detailed, *compact* = space-saving; default is *automatic* callout), *caption* (an "Open in Apple Maps" link), *sheet* (place card in a sheet). Full callout renders as a popover on iPadOS/macOS and as a sheet on iOS.
- **Consider your map presentation when choosing a place card style** — full callout gives the richest info but must fit context (e.g., use compact callout for small maps with many annotations).
- **Make sure place cards look great on different devices/window sizes** — set a minimum width for full callout style to prevent text overflow on small devices.
- **Avoid duplicating information** already shown elsewhere in your app/website when choosing a style.
- **Keep the location visible when displaying a place card** — set an offset distance pointing to the selected location.
- **When displaying place cards outside a map** (search results, store locators), use location cues (place name/address plus a details button, or a map pin icon) to indicate interactivity.
- **Indoor maps — adjust detail by zoom level:** show large areas (rooms, buildings) at all zoom levels, progressively revealing detailed features/labels when zoomed in.
- **Use distinctive styling** (color + icons) to differentiate features/areas/stores/services.
- **Offer a floor picker** for multi-level venues — keep floor numbers (not names) concise.
- **Include surrounding areas** (streets, playgrounds, nearby locations) for orientation context; dim/distinctly color noninteractive surrounding areas to show they're supplemental.
- **Consider supporting navigation to/from nearby transit points** (bus stops, train stations, parking); offer a quick switch to Apple Maps for further navigation.
- **Limit scrolling outside your venue** to avoid people getting lost; keep at least part of the indoor map visible onscreen; adjust scroll limits based on zoom level.
- **Design indoor maps as a natural extension of your app's visual style** — don't replicate Apple Maps' appearance.

**Platforms:** watchOS — maps are static, noninteractive snapshots placed in the interface at design time with the appropriate region shown at runtime; tapping opens the Maps app; up to 5 annotations supported. Fit the entire map element to the screen without scrolling; show the smallest region encompassing all points of interest, since content doesn't scroll. No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS.

## NFC
Source: https://developer.apple.com/design/human-interface-guidelines/nfc
Near-field communication (NFC) allows devices within a few centimeters of each other to exchange information wirelessly, letting iOS apps read data from electronic tags attached to real-world objects.
- **Support single- or multi-object scanning** while the app is active, and display a scanning sheet whenever people are about to scan.
- **Don't encourage contact with physical objects** — an iOS device only needs to be near the tag, not touch it; use "scan"/"hold near" instead of "tap"/"touch."
- **Use approachable terminology** — avoid technical terms like NFC, Core NFC, near-field communication, tag; use friendly conversational language instead:

| Use | Don't use |
|---|---|
| Scan the [object name]. | Scan the NFC tag. |
| Hold your iPhone near the [object name] to learn more about it. | To use NFC scanning, tap your phone to the [object]. |

- **Provide succinct instructional text for the scanning sheet** — a complete sentence, sentence case, ending punctuation; identify the object to scan and revise the text for subsequent scans; keep it short to avoid truncation.

| First scan | Subsequent scans |
|---|---|
| Hold your iPhone near the [object name] to learn more about it. | Now hold your iPhone near another [object name]. |

- **Support both background and in-app tag reading** — background reading lets people scan without opening the app first (the system shows a notification to tap and send data to the app), but you must still provide an in-app scanning path for devices that don't support background reading.
> Note: background reading isn't available when an NFC scanning sheet is visible, Wallet/Apple Pay are in use, cameras are in use, the device is in Airplane Mode, or the device is locked after a restart.

**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## Photo editing
Source: https://developer.apple.com/design/human-interface-guidelines/photo-editing
Photo-editing extensions let people modify photos and videos within the Photos app by applying filters or making other changes.
- Edits are always saved as new files in Photos, preserving originals; tapping the extension icon in edit mode shows an action menu, and dismissing the extension's modal view (with its own top toolbar) confirms/saves or cancels the edit.
- **Confirm cancellation of edits.** If someone taps Cancel, ask them to confirm before discarding changes; skip the confirmation if no edits have been made yet.
- **Don't provide a custom top toolbar** — your extension loads in a modal view that already has one; a second toolbar is confusing and wastes space.
- **Let people preview edits** before closing the extension and returning to Photos.
- **Use your app icon for the photo editing extension icon** to reassure people the extension comes from your app.

**Platforms:** No additional considerations for iOS, iPadOS, or macOS. Not supported in tvOS, visionOS, or watchOS.

## ResearchKit
Source: https://developer.apple.com/design/human-interface-guidelines/researchkit
The ResearchKit framework provides predesigned screens and transitions for building a research app that lets people everywhere participate in medical research studies.
- **Always display the onboarding screens in the correct order** — introduction, eligibility, consent, then data-access permission — since they're typically not revisited once complete.
- **1. Introduction:** provide an introduction that informs and gives a call to action, clearly describing the subject/purpose of the study; let existing participants log in and continue an in-progress study.
- **2. Determine eligibility as soon as possible** — don't route ineligible people to the consent section; present only necessary eligibility requirements in simple, straightforward language, and make entering info easy.
- **3. Get informed consent** — make sure participants understand the study before consenting; comply with applicable App Store Guidelines consent requirements; typically covers how the study works, participant responsibilities, and consent itself.
- **Break a long consent form into digestible sections** (one aspect each — data gathering, data use, benefits, risks, time commitment, withdrawal, etc.), using simple language with an optional Learn More button for detail; participants must be able to view the entire form before agreeing.
- **If it makes sense, provide a quiz** testing participants' understanding (in lieu of questions normally asked when obtaining consent in person).
- **Get the participant's consent and, if appropriate, contact information** — present a confirmation dialog, then signature/contact-detail screens; most apps email participants a PDF of the consent form for their records.
- **4. Request permission to access data** — get permission for location, Health, or other data, and for notifications, clearly explaining why it's needed; don't request access to noncritical data.
- **Surveys:** tell participants how many questions and roughly how long it'll take; use one screen per question; show progress; keep surveys short (several short surveys beat one long one); use the standard font for questions and a slightly smaller font for explanatory text; tell participants when the survey is complete.
- **Active tasks:** describe how to perform the task in clear, simple language; explain any requirements (timing/circumstances); make sure participants can tell when the task is complete.
- **Use a profile screen** to let participants manage personal data that may change (e.g., weight, sleep habits), remind them of upcoming activities, and provide access to leaving the study, the consent document, and the privacy policy.
- **Use a dashboard to show progress and motivate continued participation** — e.g., daily progress, weekly assessments, activity results, and comparisons with aggregated results from other participants. Ideally, both the profile and dashboard are accessible at all times.

**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## SharePlay
Source: https://developer.apple.com/design/human-interface-guidelines/shareplay
SharePlay helps multiple people share activities — like viewing a movie, listening to music, playing a game, or sketching on a whiteboard — while in a FaceTime call or Messages conversation, synchronizing app playback across devices.
- When someone shares content in FaceTime, the system asks each participant to launch the app (or download it from the App Store if not installed); offering platform versions as a Universal Purchase lets one purchase cover all supported platforms.
- **Let people know that you support SharePlay** — e.g., use the `shareplay` SF Symbol to identify shareable content/experiences.
- **If part of your app requires a subscription, help nonsubscriber participants join quickly** — e.g., temporary/provisional access, a one-time pass from an existing subscriber, or Family Sharing support; if people can subscribe mid-session, present a streamlined sign-up flow so others don't wait.
- **Support Picture in Picture (PiP) when possible** — on iPhone/iPad, people can open a shared video in a PiP window; on Mac, a shared video opens in a background window people can foreground.
- **Use the term "SharePlay" correctly** — as a noun ("Join SharePlay") or a verb for a direct action (e.g., "SharePlay Movie"); avoid using it as an adjective (no "virtual"/"spatial SharePlay") and never alter the term (no "SharePlayed," "SharePlays," "SharePlaying").
- Define **activities** (app-defined shareable experience types) as needed, each with its own description.
- **Briefly describe each activity** so invitees understand what they're about to share; keep descriptions short enough to avoid truncation.
- **Make it easy to start sharing an activity** — if no session exists, present UI to start a group activity; the system then asks people whether to share or continue solo.
- **Help people prepare to join a session before displaying the activity** — surface login, content-download, or payment steps first, and make them as simple/effortless as possible.
- **Defer app tasks that might delay a shared activity** — e.g., ask for a participant's profile at a convenient pause point rather than up front.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS.
### visionOS
- Most visionOS apps are expected to support SharePlay; wearers choose the Spatial option in FaceTime to share.
- FaceTime can show other participants as spatial Personas in each wearer's space; people interact via natural speech/gesture, sense attention, and see who's using a shared tool.
- **Shared context** describes characteristics that help people feel physically present together while viewing the same content.
> Note: the system obscures some visual details of wearers during shared activities to preserve privacy; a person can adjust their spatial Persona; spatial Personas can be placed shoulder to shoulder and support shared gestures like handshake/high five, but remain physically apart.
- **Choose the spatial Persona template that suits your shared activity:** *side-by-side* (participants along a curved line, all facing content — best for watching media together; less nonverbal interaction), *surround* (participants arranged all the way around 3D content, facing each other — promotes verbal/nonverbal interaction), *conversational* (participants grouped around a center point with content along the circle, not centered — good when people being together matters more than shared viewing, e.g., background music).
- **Be prepared to launch directly into your shared activity** when someone shares it on a FaceTime call — avoid unrelated windows; present any required sign-in in an autodismissible window.
- **Help people enter a shared activity together, but don't force them** — when one participant changes immersion level, check whether synchronizing would disrupt others' current tasks and offer a choice if so.
- **Smoothly update a shared activity when new participants join** (accommodate up to 5), keeping content and positions synchronized.
- **Make sure everyone views the same app state** (e.g., minimal vs. theater viewing mode) to preserve the sense of togetherness, except when someone temporarily exits.
- **Use Spatial Audio** to strengthen the shared activity's realism.
- **Let people discover natural, social solutions to conflicts** (e.g., verbal turn-taking for a shared tool) rather than adding UI; for simultaneous-edit conflicts, consider a simple rule like "last change wins."
- **Help people keep private and shared content separate** and easy to distinguish; allow dragging content from a private window into a shared one if possible.
- **Let people personalize their own experience** (volume, subtitles, comfort/accessibility settings) without changing it for others.
- **Consider giving each participant a unique view of shared content** when a specific viewing angle matters (e.g., Spatial Capture depth) — allow a temporary transition to a Full Space that hides others while keeping the overall experience synchronized.
- **Make it easy to exit and rejoin a shared activity** — provide a control to quickly rejoin, and consider keeping shared content visible while a person's spatial Persona is hidden.

## ShazamKit
Source: https://developer.apple.com/design/human-interface-guidelines/shazamkit
ShazamKit supports audio recognition by matching an audio sample against the ShazamKit catalog or a custom audio catalog.
- Use cases: graphics matching currently playing music's genre, closed captions/sign language synced to audio for accessibility, syncing in-app experiences with virtual content (e.g., online learning, retail).
- Request microphone access with a clear explanation of why, per Privacy guidance.
- **Stop recording as soon as possible** — only record as long as needed to get the sample, since people don't expect the mic to stay on.
- **Let people opt in before storing recognized songs to their iCloud library** — get approval first, even though the Music Recognition control and Shazam app already show your app as the source.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Sign in with Apple
Source: https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple
Sign in with Apple provides a fast, private way to sign into apps and websites, letting people use their existing Apple Account without extra forms, passwords, or verification.
- Can be offered in every version of your app/website, across platforms, including non-Apple platforms.
- Supports Face ID, Touch ID, or Optic ID authentication plus built-in two-factor authentication; Apple doesn't use it to profile people or their app activity.
- **Ask people to sign in only in exchange for value** — briefly describe sign-in benefits (personalization, extra features, sync).
- **Delay sign-in as long as possible** — let people explore/familiarize themselves before committing.
- **If an account is required, ask people to set it up before offering sign-in options** — explain why, then offer Sign in with Apple and any other methods after setup.
- **Consider letting people link an existing account to Sign in with Apple** (before or after sign-in) — e.g., suggest linking if a shared email matches an existing account, or surface a linking suggestion in account settings.
- **In a commerce app, wait until after purchase to ask for account creation** — e.g., offer it on the order confirmation page after guest checkout/Apple Pay; skip re-asking for name/email already provided via Apple Pay.
- **As soon as sign-in completes, welcome people to their new account** immediately — don't delay with unnecessary info requests.
- **Indicate when people are currently signed in** (e.g., "Using Sign in with Apple" in settings/account UI).
### Collecting data
- **Minimize requests for additional data** (e.g., birth date, region); build on trust by explaining why you need it and displaying what you received.
- **Clarify whether requested additional data is required** (legally/contractually — e.g., terms of service, region, birth date, real-identity laws) **or merely optional/recommended**, explaining the benefit of optional data.
- **Don't ask people to supply a password** — a core benefit is not needing one, unless they've stopped using Sign in with Apple with your app.
- **Avoid asking for a personal email address when people used a private relay address** — respect the choice; instead let them view their relay address in-app, direct them to Settings > Apple Account > Password & Security > Apps using Apple Account, or use other identifiers like order number/phone number.
- **Give people a chance to engage with your app before asking for optional data**; never block account access or features if they decline.
- **Be transparent about collected data** — e.g., welcome people using the name/email they shared, and display all data you collect.
### Displaying buttons
- **Prominently display a Sign in with Apple button** no smaller than other sign-in buttons, and avoid requiring scrolling to see it.
- System-provided buttons guarantee: Apple-approved appearance, ideal content proportions at any style, automatic title translation to the device's language, corner radius configuration to match your UI (iOS, macOS, web), and a system-provided VoiceOver label.
- Button title variants are available for iOS, macOS, tvOS, and the web; watchOS provides one fixed title: "Sign in."
- Up to three button appearances depending on platform: **White** (all platforms + web; use on dark backgrounds with sufficient contrast). **White with outline** (iOS, macOS, web; use on white/light backgrounds that lack contrast with plain white; avoid on dark/saturated backgrounds). **Black** (all platforms + web; use on white/light backgrounds with sufficient contrast; never on black/dark backgrounds). watchOS's "black" button actually uses a system-defined dark gray fill (not pure black) to contrast with Apple Watch's pure black background.
- **Adjust the corner radius to match other buttons** in your app (square, rounded, or capsule) in iOS, macOS, and web.
- **Maintain minimum button size and margin:**

| Minimum width | Minimum height | Minimum margin |
|---|---|---|
| 140pt (140px @1x, 280px @2x) | 30pt (30px @1x, 60px @2x) | 1/10 of the button's height |

### Creating a custom Sign in with Apple button
- **Always make the button instantly identifiable** as Sign in with Apple; App Review evaluates all custom buttons.
- **Use only Apple Design Resources' downloadable logo artwork** (PNG/SVG/PDF, black and white, logo-only or logo+text) — never create a custom Apple logo.
- Logo-file rules: use the file only to position the logo in a button (never as the button itself); match logo file height to button height; don't crop the logo file; don't add vertical padding.
- **Don't change:** titles (only "Sign in with Apple," "Sign up with Apple," or "Continue with Apple"); general shape (logo+text buttons are always rectangular; logo-only can be circular or rectangular); logo/title colors (both must be black or white, no custom colors).
- **Can change:** title font (weight/size); title case (all-caps allowed); background appearance (must stay black or white overall; a subtle texture/gradient is okay); button corner radius; button bezel/shadow (e.g., stroke or drop shadow).
- **Logo+text custom buttons:** use PNG only at 44pt button height (the default/recommended iOS height); SVG/PDF work at any height; logos come in small/medium/large sizes.
- **Prefer the system font for the title**; if using another font, keep the same button-height-to-title-size proportions as the system — title font size = 43% of button height (button height = 233% of title font size, rounded to the nearest integer).
- **Preserve the default capitalization style** (first word and "Apple" capitalized, rest lowercase) unless your interface is all-uppercase.
- **Keep the title and logo vertically aligned** to the middle of the button — the logo's built-in padding keeps them aligned once the title is centered.
- **Inset the logo if needed** to horizontally align with other authentication logos.
- **Maintain a minimum margin of at least 8% of the button's width** between the title and the button's right edge.
- Maintain the same minimum size/margin table as above (140pt / 30pt / 1/10 height).
- **Logo-only custom buttons:** use SVG/PDF for any size, PNG only at 44x44pt; don't add horizontal padding (artwork already includes correct 1:1-aspect padding); use a mask (not cropping) to change from the default square shape (e.g., circular/rounded rectangle); maintain a minimum margin of at least 1/10 of the button's height.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Siri
Source: https://developer.apple.com/design/human-interface-guidelines/siri
Siri is a personal assistant that helps people get information and perform quick actions throughout the system and the apps they use, powered by Apple Intelligence on supported devices.
- To work with Siri, an app must expose its actions (intents) and content (entities) via the App Intents framework.
- Apps can associate features/content with **App schema domains** (preset templates for common areas like email, music, photos) to gain built-in logic for natural conversation and deeper contextual understanding.
- Annotate onscreen views/content with app entities so Siri understands what's currently displayed and can resolve references during conversation.
- Donate entities to the on-device Spotlight index to make app content searchable via Spotlight/Siri.
- Donate actions as intents so Siri can anticipate and surface likely future actions (e.g., recent activity, items of interest) at appropriate times.
- **Identify your app's most popular actions and the contexts** (device, hands-free, etc.) where they're relevant, to prioritize what to expose and inform your Siri design.
- **Use familiar terms for content/actions** that people are most likely to recognize (e.g., "track," "song," or "podcast," whichever fits).
- **Offer relevant content** to Spotlight — favor personally relevant items (recent searches, favorites, wishlist) over the entire catalog, except categories like email/messaging where full catalog access can be appropriate.
- **Don't advertise** — never include ads, marketing, or in-app purchase pitches in Siri-delivered content.
- **Only provide a custom response if built-in responses don't meet your app's needs** — Siri already handles a wide variety of natural language requests without extra configuration.
- Use **App Shortcuts** to expose custom actions when your app's functionality falls outside existing App schema domains.
- Define additional optional intent/entity properties to contextually enhance responses (e.g., a playback-control Snippet while audio plays).
> Note: because responses can appear in many contexts (some non-visual), optional custom properties may not always appear.
- **Write response dialogue that's clear and descriptive** — customize follow-up question wording for clarity (e.g., "Which soup?" beats "Which one?").
- **Keep responses as succinct as possible** — remove unnecessary words/details/humor, since people may hear the same response repeatedly.
- **Provide responses deliverable both audibly and visually**, letting Siri choose per context (e.g., onscreen weather on iPhone vs. spoken on AirPods); ensure the voice response stands alone without depending on visual elements.
- **Design inclusive interactions** — avoid unnecessary specific pronouns (e.g., "Who should I send it to?" instead of "What's his or her name?").
- **Ask an open-ended follow-up question** when the full list of options is too long to read aloud in a timely way.
- **Keep responses device-independent whenever possible**, since a request can be initiated on one device and take effect on another; be accurate if you must reference a specific device.
- **Omit your app name from responses** — the system already provides attribution.
- **Use appropriate language and respect parental controls** — avoid offensive language, since Siri may speak responses aloud where others can hear.
- **Help people understand errors/failures** with situation-specific messages rather than generic defaults (e.g., name the specific out-of-stock item).
### Editorial guidelines
- **Refer to Siri by name**, not pronouns (she/him/her) — just use "Siri."
- **Never impersonate Siri**, reproduce its functionality, or provide a response that appears to come from Apple; never use reserved phrases like "Call 911" or "Hey Siri."
- **In a localized context, translate only the word "Hey" in "Hey Siri"** — "Siri" itself is a trademark and is never translated. Approved translations include: ar_AE/ar_SA "يا Siri", da_DK "Hej Siri", de (AT/CH/DE) "Hey Siri", en (all locales) "Hey Siri", es_CL/ES/MX/US "Oye Siri", fi_FI "Hei Siri", fr (BE/CA/CH/FR) "Dis Siri", it (CH/IT) "Ehi Siri", ja_JP "Hey Siri", ko_KR "Siri야", ms_MY "Hai Siri", nb_NO/no_NO "Hei Siri", nl_BE "Hé, Siri", nl_NL "Hé Siri", pt_BR "E aí Siri", ru_RU "привет Siri", sv_SE "Hej Siri", th_TH "หวัดดี Siri", tr_TR "Hey Siri", zh_CN "嘿Siri", zh_HK "喂 Siri", zh_TW "嘿 Siri".

## Tap to Pay on iPhone
Source: https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone
Tap to Pay on iPhone lets merchants accept contactless payments using an app on their iPhone, without connecting external hardware.
- Works alongside existing payment-acceptance hardware/accessories.
- Requires a supported payment service provider (PSP), the Tap to Pay on iPhone entitlement, and ProximityReader APIs (via the PSP SDK or directly).
> Note: if your PSP's SDK supplies UI for tap results etc., follow the PSP's documentation instead.
### Enabling Tap to Pay on iPhone
- **Help merchants accept terms and conditions before they begin interacting with customers** — use the ProximityReader API to check status and present the acceptance flow only when necessary, ideally via in-app messaging/onboarding before checkout begins.
- **Present terms and conditions only to an administrative user** — show an explanatory message if a nonadministrator tries to activate the feature; enterprise apps can let an admin accept terms via a web interface or a different app/device.
- **If necessary, help merchants make sure their device is up to date** — if your PSP requires specific iOS versions, present terms and conditions only after the merchant updates.
### Educating merchants
- **Provide a tutorial** describing supported payment types and how to accept each — via a Learn More option, automatically after accepting terms, automatically for new users, or in help/settings.
- Build tutorials from Apple-approved Tap to Pay on iPhone marketing assets, or use the ProximityReaderDiscovery API for a pre-built, Apple-maintained, localized merchant-education experience.
- A self-built tutorial should show: launching checkout for each payment type, positioning a contactless card/wallet, and handling PIN entry (including accessibility mode); end by letting merchants accept terms if they haven't yet.
### Checking out
- Offer payment options besides Tap to Pay on iPhone as necessary; respond quickly if checkout starts before the feature is enabled; let merchants check out even if device configuration is in progress; present pre-payment actions (e.g., tipping) before checkout completes.
- **Provide Tap to Pay on iPhone as a checkout option whether enabled or not** — tapping the button presents terms and conditions if needed, then auto-shows the Tap to Pay screen once configured.
- **Avoid making merchants wait** — prepare the feature as soon as the app starts and after every foreground transition, since configuration is needed per-device and on each app-frontmost transition.
- **Keep the Tap to Pay checkout option available even mid-configuration** — let merchants select it, then show a progress indicator (indeterminate by default; determinate if the API reports configuration progress).
- **If you support multiple payment-acceptance methods, make the Tap to Pay button easy to find** without scrolling; if it's your only method, open it automatically at checkout.
- **Make it easy to switch between Tap to Pay on iPhone and supported hardware accessories** — allow setting up both at once and switching during checkout without visiting app settings.
- **Button label:** use "Tap to Pay on iPhone," or "Tap to Pay" if space is constrained — except when it's the app's only payment method, in which case existing Charge/Checkout buttons can activate it directly. Use only for payment actions.
> Important: use the "Tap to Pay on iPhone" label only for payment actions — use different language for nonpayment actions.
- If using icons in multi-method buttons, use `wave.3.right.circle` or `wave.3.right.circle.fill` SF Symbols; always avoid the Apple logo in Tap to Pay on iPhone buttons.
- **Design the Tap to Pay button to match your app's other buttons** in color/shape, while keeping the required label text.
- **Determine the final payable amount** (including tipping etc.) before starting the Tap to Pay experience; aim to display the final amount on the Tap to Pay screen; show pre-payment options (like payment-type selection) before opening the Tap to Pay screen.
### Displaying results
Customers pay by tapping a contactless card or digital wallet near the screen; success (with PIN entry if required) shows a checkmark and gives the app encrypted payment data for the PSP; failure shows an error screen.
- **Start processing a transaction as soon as possible** — request the tap result before the checkmark animation finishes, via `returnReadResultImmediately`.
- **Display a progress indicator for authorization only after the checkmark animation finishes** (`PaymentCardReader.Event.readyForTap`), since authorization can take several seconds.
- **Clearly display transaction results** (declined or successful) — reasons can include insufficient funds, fraud suspicion, or wrong PIN; offer a digital receipt (QR code or text) when possible.
- **Help merchants complete checkout when Tap to Pay can't finish a payment** (unreadable/unsupported card, amount/PIN-entry restrictions) — offer an alternate payment method, a different acceptance method (hardware/payment link), or relaunch Tap to Pay for another card.
- Regional considerations to coordinate with your PSP: Strong Customer Authentication (SCA) may require displaying a PIN entry screen instead of the transaction result; Offline PIN markets may need PIN fallback flows collecting partial data to continue via another method like a payment link.
- **If the system returns a merchant-actionable error, display a clear description and recommended resolution** (e.g., recommend an iOS update if unsupported).
- **Make it easy for merchants to get help with unresolved issues** — direct them to in-app/website help content and support contact.
### Additional interactions
- **Use a generic label** (e.g., "Look Up," "Store Card," "Verify," "Refund") — never "Tap to Pay on iPhone"/"Tap to Pay" — for reading a card with no transaction amount (lookups, storing card info, refunds, identity verification).
- **If supporting an independent loyalty-card transaction** (loyalty/discount/points cards read via NFC alongside or independently of a payment card), give it a separate, clearly labeled button that avoids payment-related terms, to prevent merchants choosing the wrong button.

**Platforms:** No additional considerations for iOS. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS.

## VoiceOver
Source: https://developer.apple.com/design/human-interface-guidelines/voiceover
VoiceOver is a screen reader that lets people experience your app's interface without needing to see the screen, helping people who are blind or have low vision.
- Supported in apps/games built for Apple platforms, including those built in Unity via Apple's Unity plug-ins.
### Descriptions
- **Provide alternative labels for all key interface elements** — system controls have generic defaults, but add descriptive labels conveying your app's functionality, and to custom elements; keep labels up to date as content/interface change.
- **Describe meaningful images** — since VoiceOver already covers surrounding context (e.g., captions), describe only what the image itself conveys.
- **Make charts and other infographics fully accessible** — provide a concise description of what each conveys, and make any interactive drill-down available to VoiceOver users too.
- **Exclude purely decorative images from VoiceOver** — unnecessary description wastes people's time and adds cognitive load.
### Navigation
- **Use titles and headings to convey information hierarchy** — offer unique, succinct page titles (the first thing VoiceOver announces) and accurate section headings.
- **Specify how elements are grouped, ordered, or linked** when the relationship is conveyed only visually (proximity, alignment) — describe these relationships explicitly to VoiceOver so, e.g., an image is announced together with its caption rather than separately.
- VoiceOver reads elements in the same order people read content in their active language/locale (e.g., top-to-bottom, left-to-right in US English).
- **Inform VoiceOver when visible content or layout changes occur**, so it (and other assistive technologies) can help people update their understanding of the content.
- **Support the VoiceOver rotor when possible** — identify headings, links, and other content types to it so people can navigate by type; the rotor can also bring up the braille keyboard.

**Platforms:** visionOS — custom gestures aren't always accessible: when VoiceOver is on, apps/games with custom gestures don't receive hand input by default, so people can explore via voice without unintended app response. A person can opt into Direct Gesture mode to disable standard VoiceOver gestures and let apps process hand input directly. No additional considerations for iOS, iPadOS, macOS, tvOS, or watchOS.

## Wallet
Source: https://developer.apple.com/design/human-interface-guidelines/wallet
Wallet helps people securely store credit/debit cards, driver's license or state ID, transit cards, event tickets, keys, and more on iPhone and Apple Watch.
### Passes
Passes are digital representations of information — event tickets, boarding passes, membership cards, coupons — that people add to Wallet.
- **Offer to add new passes to Wallet** with one tap when an action creates one (e.g., buying a ticket, registering for rewards); for frequent/predictable actions (e.g., flight check-in), add passes in the background after one-time authorization so people don't need to tap each time — Wallet notifies people whenever a pass is added. Alternatively, show a custom preview view with an Add to Apple Wallet button.
- **Help people add a pass created outside your app** (website/other device) by suggesting it the next time they open your app; don't re-ask if they decline.
- **Add related passes as a group** (e.g., multi-connection flight boarding passes, or a bundled set of event tickets from a website) so people don't add each one individually.
- **Display an Add to Apple Wallet button** wherever pass info appears, to let people add a pass they previously declined or removed. An Add to Apple Wallet badge is also available for emails/webpages.
- **Let people jump from your app to their pass in Wallet** via a link labeled something like "View in Wallet."
- **Tell the system when passes expire** — set expiration date, relevant date, and voided properties correctly so Wallet can hide expired passes (with a button to revisit them).
- **Always get permission before deleting passes from Wallet** — e.g., an in-app setting for manual vs. automatic removal, or a confirmation alert.
- **Help the system suggest a pass when relevant** — supply relevance info so the system can link to it on the Lock Screen at the right time/place (e.g., gym card near the gym); certain pass types (e.g., event tickets) can also start a Live Activity.
- **Keep passes up to date** — reflect real-time changes (e.g., flight delays, gate changes) since digital passes, unlike physical ones, can update.
- **Use change messages only for updates to time-critical information** (e.g., gate change, not a changed phone number) — never for marketing; available per-field.
### Pass anatomy
- Define pass content via **pass fields** (what/how info appears) and **semantic tags** (describe content to the system, enabling relevance surfacing and featured actions like venue directions); semantic tags are required for poster event and semantic boarding passes (which need pass fields too, for backward compatibility on older iOS).
- Supplemental info can go on linked sheets from the pass front; the back holds rarely needed settings/info like legal text.
- Pass field areas: logo/logo text (brand, visible when collapsed), header (critical info, visible when collapsed), primary field (most important info), secondary/auxiliary fields (useful but less critical), footer fields (supplemental, e.g., pass category), back fields (supplemental details in pass detail view). Layout varies by pass style.
### Designing passes
- Use Pass Designer to design/preview passes, starting from templates or a blank pass, across styles (boarding, coupon, event ticket, store card, generic, poster generic).
- **Design a pass that looks great and works on all devices** — don't put essential info in elements unavailable on some devices (e.g., Apple Watch shows less); avoid padding images, since watchOS crops white space from some images.
- **Keep the pass front uncluttered** — put essential info (event date, balance) in the header for visibility when collapsed; use the rest of the front for frequently needed info; put rarely needed details on the additional info sheet.
- **Make your pass instantly identifiable** using brand colors and visual elements (images, icons, full-art backgrounds).
- **Ensure sufficient contrast between background and text colors**, against both solid backgrounds and background images.
- **Use language that works on any device** — avoid device-specific phrasing (e.g., "Slide to view" doesn't apply on Apple Watch).
### Pass styles
- **Boarding passes** — travel tickets (airline, train, bus, boat, generic transit), typically one trip per pass; use semantic tags for airline boarding passes, pass fields for other transit types.
- **Coupons** — coupons, special offers, discounts.
- **Event tickets** — entry to events (sports, concerts, movies, plays), typically one event per pass (or one pass for multiple events, e.g., season ticket); supports a full-art background. Non-poster event tickets use standard pass fields with an optional background image/thumbnail.
- **Store cards** — loyalty, discount, points, or gift cards; usually displays account balance.
- **Poster generic passes** — full background image, distinct field layout, flexible/uncategorized use.
- **Generic passes** — anything else (e.g., gym membership, coat-check ticket).
### Pass images
- Create pass images as PNG at @2x and @3x.
- **Reserve pass images for visual content only** — embedded text isn't accessible and may not display everywhere; use text fields/semantic tags for text, and Pass Designer/APIs (not embedded images) for barcodes.
- **Keep image file sizes small** for fast downloads via email/webpage.
- **Provide a pass icon** (app icon or a separate design) for the Lock Screen, Mail, and Wallet.

| Image | Supported styles | Filename | Min width | Max width | Height |
|---|---|---|---|---|---|
| Logo | Non-semantic airline boarding, non-airline boarding styles, coupons, non-poster event tickets, generic passes, store cards | logo.png | 50 pt | 160 pt | 50 pt |
| Primary logo | Airline boarding passes, poster event tickets, poster generic passes | primaryLogo.png | 30 pt | 126 pt | 30 pt |
| Secondary logo | Poster event ticket | secondaryLogo.png | 12 pt | 135 pt | 12 pt |
| Icon | All | icon.png | 38 pt | 38 pt | 38 pt |
| Strip image | Coupon, store card | strip.png | 375 pt | 375 pt | 144 pt |
| Thumbnail | Event ticket, generic pass | thumbnail.png | 60 pt | 90 pt | 90 pt |
| Background (non-poster) | Event tickets | background.png | 343 pt | 343 pt | 503 pt |
| Background (poster) | Poster event tickets, poster generic passes | artwork.png | 358 pt | 358 pt | 448 pt |
| Footer | Airline boarding passes | footer.png | 268 pt | 268 pt | 15 pt |

- **Avoid inner drop shadows on logo artwork** — reduces legibility.
- **Position content within the safe area on poster styles** — a material strip covers the bottom edge of poster artwork; account for any barcode in the background design; preview layout in Pass Designer.
### Order tracking
Wallet's order dashboard shows active/completed orders with item and fulfillment (shipping/pickup) details, updating as status changes; in iOS 17+, people can start tracking from your app/website with more ways to add an order.
- **Make it easy to add an order** — auto-add via `PKPaymentOrderDetails` (app) / `ApplePayPaymentOrderDetails` (web) on Apple Pay completion; use `AddOrderToWalletButton` (iOS 17+) to show the system Track with Apple Wallet button on order confirmation/status/tracking pages or in emails; re-adding an already-added order opens Wallet to show it.
- **Make order info available immediately after placement** — supply what you have and use a status like "Check back later for full order details" if some data isn't ready yet.
- **Provide fulfillment info as soon as available and keep status current** — the system auto-updates and can notify customers; statuses include Order Placed, Processing, Ready for Pickup, Picked Up, Out for Delivery, Delivered, Issue, or Canceled.
- **Supply a high-resolution logo image with a nontransparent background**, 300x300px PNG/JPEG.
- **Supply distinct, high-resolution product images with nontransparent, uncluttered backgrounds** (avoid "lifestyle" context), 300x300px PNG/JPEG, one per product.
- **Keep text brief** — the system truncates overly long text.
- **Use clear, localized language**, and make sure displayed prices match the customer's confirmed final price.
- **Provide a universal link** to your order-management area so people can open it even without your app installed.
- **Clearly describe each item** (price, name, image via `LineItem`) — an order lists all ordered items, a fulfillment lists only items it includes; can attach a PDF receipt to a transaction.
- **Supply a prioritized list of your apps** for the system to link to in the order details view — it links to the highest-priority installed app, or the first listed app if none are installed.
- **Avoid sending duplicate notifications** — e.g., suppress Wallet order notifications when the customer has one of your associated apps installed.
- **Make it easy to contact the merchant** — provide at minimum a website/landing-page link, ideally also Messages for Business, phone, email, and/or a support page link; presented as a menu via the Contact button.
- **Help people track a multi-fulfillment order** with enough info to know location/timing, plus: a direct carrier tracking link (in addition to a tracking number), a scannable pickup barcode within Wallet, and clear pickup/receipt instructions.
- **Keep the fulfillment screen centered on order tracking** — prioritize tracking info over other recommended content.
- **Choose shipping-fulfillment values matching known detail** — use the `carrier` property if known (default "Track Shipment" if not); use specific status values (`onTheWay`, `outForDelivery`, `delivered`) if interim steps are known, or `shipped` if not; always provide a tracking link when available.
- **Keep customers informed with approachable, accurate, relevant fulfillment status descriptions** that reflect brand voice.
- **Be direct and thorough describing an Issue or Canceled status** — explain why and what to do.
### Identity verification
On iOS 16+, people can store an ID card in Wallet and let an app/App Clip access it to verify identity in place (e.g., confirming identity for a credit card application in a banking app).
> Developer note: Apple doesn't create or see the ID documents people add to Wallet; when people share identifying info, you receive only encrypted, on-device-unreadable data.
- Use the Apple-provided **Verify with Wallet** button for a consistent, trusted verification request — reveals a sheet describing the request, letting people agree or cancel.
- **Present a Wallet verification option only when the device supports it**; provide a fallback verification method for unsupported devices.
- **Ask for identity information only at the precise moment you need it** — not when simply creating an account.
- **Clearly and succinctly explain (in a purpose string) why you need the data** — sentence case, direct/specific, active voice, ending period. Example: "Federal law requires this information to verify your identity and also to help [App Name] prevent fraud."
- **Ask only for the data you actually need** — e.g., request an age threshold check rather than exact age/birth date.
- **Clearly indicate whether/how long you'll keep the data** — specify a duration via PassKit APIs (a period, indefinitely, or only until verification completes) and the system auto-displays explanatory content.
- **Choose the system-provided verification button matching your use case:** age verification (transaction completes after age check, e.g., leasing a car); identity verification (transaction completes after identity check, e.g., car rental); a form that's part of a larger process needing extra info (e.g., SSN/phone for opening a financial account); or a generic "Continue"-style button when the other labels don't fit (e.g., signing up for a government service). All labels have a multiline variant used automatically under constrained horizontal space.
- The verification button always uses white text on black; a light-outline style variant is available for contrast against dark app backgrounds; corner radius is adjustable to match other buttons.

**Platforms:** watchOS — Wallet shows passes in a scrolling carousel of cards; people can add a pass to Apple Watch even without a watch-specific app; tapping a pass reveals a details screen in a scroll view (and sometimes per-transaction detail); each pass style has fixed basic layout areas, with overflow shown in the scrolling details screen.
> Important: watchOS crops the strip image to fit the card interface's aspect ratio and may crop white space from other images.

No additional considerations for iOS, iPadOS, macOS, or visionOS. Not supported in tvOS.
