# HIG — Foundations: experience (accessibility, layout, privacy, writing)
accessibility, immersive-experiences, inclusion, layout, privacy, right-to-left, spatial-layout, writing

## Accessibility
Source: https://developer.apple.com/design/human-interface-guidelines/accessibility
Accessible interfaces empower everyone to have a great experience with an app or game regardless of capabilities or how they use their devices — they are intuitive, perceivable (not reliant on any single sense), and adaptable (support system accessibility features and personalization).
- Audit accessibility with Accessibility Inspector; you can also declare feature support on the App Store via Accessibility Nutrition Labels (App Store Connect).

**Vision**
- **Support larger text sizes.** Ideally let people enlarge text by at least 200 percent (140 percent in watchOS apps), via custom UI or by adopting Dynamic Type.
- **Use recommended defaults for custom type sizes** — follow each platform's default/minimum sizes:

| Platform | Default size | Minimum size |
| --- | --- | --- |
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

- **Font weight affects legibility** — thin custom-font weights should aim larger than the recommended sizes.
- **Strive to meet color contrast minimum standards.** Accessibility Inspector uses WCAG Level AA values as guidance:

| Text size | Text weight | Minimum contrast ratio |
| --- | --- | --- |
| Up to 17 pts | All | 4.5:1 |
| 18 pts | All | 3:1 |
| All | Bold | 3:1 |

> Note: The table above is Apple's, verbatim; its rows conflict for bold text up to 17 pts. Under WCAG AA (which this table is derived from), bold text qualifies for 3:1 only at 14 pt and larger — hold smaller bold text to 4.5:1. When rows conflict, apply the stricter ratio.

- If default contrast is insufficient, provide a higher-contrast color scheme when Increase Contrast is on; check minimum contrast in both light and dark appearances if Dark Mode is supported.
- **Prefer system-defined colors** — they have accessible variants that adapt automatically to Increase Contrast and light/dark appearance.
- **Convey information with more than color alone** — add distinct shapes/icons for color-blind users (e.g., red-green, blue-orange pairings are hard to distinguish); consider letting people customize color schemes (chart colors, game characters).
- **Describe your app's interface and content for VoiceOver** — a screen reader letting people experience the app without seeing the screen.

**Hearing**
- **Support text-based ways to enjoy audio and video** — don't communicate dialogue or crucial info through audio alone; offer, per context:
  - **Captions** — textual equivalent of audible info, synced live (game cutscenes, video clips).
  - **Subtitles** — onscreen dialogue in the reader's preferred language (TV shows, movies).
  - **Audio descriptions** — spoken narration of visually-presented info, in natural pauses.
  - **Transcripts** — full textual description of audible + visual content (podcasts, audiobooks).
- **Use haptics in addition to audio cues** (success chime, error sound, game feedback); iOS/iPadOS also offer Music Haptics and Audio graphs.
- **Augment audio cues with visual cues** — important for games/spatial apps where content may be off-screen; pair directional audio guidance with visual indicators pointing to the interaction target.

**Mobility**
- **Offer sufficiently sized controls** — meet the recommended minimum control size per platform:

| Platform | Default control size | Minimum control size |
| --- | --- | --- |
| iOS, iPadOS | 44x44 pt | 28x28 pt |
| macOS | 28x28 pt | 20x20 pt |
| tvOS | 66x66 pt | 56x56 pt |
| visionOS | 60x60 pt | 28x28 pt |
| watchOS | 44x44 pt | 28x28 pt |

- **Consider spacing between controls as important as size** — about 12 pt padding around bezeled elements; about 24 pt padding around edges of elements without a bezel.
- **Support simple gestures for common interactions** — use the simplest gesture possible for frequent actions; avoid custom multifinger/multihand gestures.
- **Offer alternatives to gestures** — core functionality must be reachable through more than one physical interaction (e.g., pair a swipe-to-dismiss with a button).
- **Let people use Voice Control to give guidance and enter information verbally** — label interface elements appropriately for smooth Voice Control use.
- **Integrate with Siri and Shortcuts** so people can perform tasks via voice alone (Siri, the Action button, Home Screen/Control Center shortcuts).
- **Support mobility-related assistive technologies** — VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control, Switch Control; test and label elements appropriately.

**Speech**
- Apple's accessibility features help people with speech disabilities — and people who prefer text-based interactions — communicate effectively using their devices.
- **Let people use the keyboard alone to navigate and interact** — as a text-based alternative to voice input, support Full Keyboard Access; avoid overriding system-defined keyboard shortcuts.
- **Support Switch Control** — an assistive technology letting people control devices through separate hardware, game controllers, or sounds (click/pop) instead of speaking; support select, tap, type, draw actions.

**Cognitive**
- **Keep actions simple and intuitive** — prefer system gestures/behaviors people already know over custom gestures to learn.
- **Minimize use of time-boxed interface elements** — auto-dismissing-on-timer views/controls are problematic for people needing more processing time or using assistive tech; prefer dismissal via explicit action.
- **Consider offering difficulty accommodations in games** — e.g., reduce level-completion criteria, adjust reaction time, enable control assistance.
- **Let people control audio and video playback** — avoid autoplay without stop/start controls; consider a global opt-out setting for autoplay.
- **Allow people to opt out of flashing lights in video playback** — respond appropriately to the Dim Flashing Lights setting.
- **Be cautious with fast-moving and blinking animations** — excess use can distract, cause dizziness, or trigger epileptic episodes. When Reduce Motion is on, reduce automatic/repetitive animations (zooming, scaling, peripheral motion). Other practices:
  - Tightening animation springs to reduce bounce effects
  - Tracking animations directly with people's gestures
  - Avoiding animating depth changes in z-axis layers
  - Replacing x-, y-, z-axis transitions with fades
  - Avoiding animating into/out of blurs
- **Optimize your app's UI for Assistive Access** (iOS/iPadOS streamlined mode for cognitive disabilities):
  - Identify core functionality; consider removing noncritical workflows/UI elements.
  - Break up multistep workflows to one interaction per screen.
  - Always ask for confirmation twice for hard-to-recover actions (e.g., deleting a file).

**Platforms:**
- No additional considerations for iOS, iPadOS, macOS, tvOS, or watchOS.
- **visionOS: Prioritize comfort** — the immersive nature raises risk of motion sickness and visual/ergonomic discomfort:
  - Keep interface elements within field of view; prefer horizontal over vertical layouts (neck strain); avoid demanding attention in different locations in quick succession.
  - Reduce speed/intensity of animated objects, particularly in peripheral vision.
  - Be gentle with camera/video motion; avoid making the world seem to move without the person's control.
  - Avoid anchoring content to the wearer's head (feels confining; blocks Pointer Control use).
  - Minimize large/repetitive gestures (tiresome, surroundings-dependent).

## Immersive experiences
Source: https://developer.apple.com/design/human-interface-guidelines/immersive-experiences
In visionOS, apps and games can extend beyond windows and volumes to immerse people in content, running in the Shared Space (alongside other experiences) or a Full Space (alone), and can transition fluidly between the two.
- **Passthrough** provides real-time video of physical surroundings; the Digital Crown lets people recenter content (press-and-hold) or briefly hide all content to show passthrough (double-click).
- The system auto-adjusts content opacity for comfort: in `mixed` immersion, content dims when someone nears a physical object; in `progressive`/`full` styles, the system defines a boundary ~1.5 meters from the initial head position — nearing it fades the experience and increases passthrough; crossing it replaces immersive visuals in space with the app's icon, restored on return/recenter.

**Immersion styles**
- **Use dimmed passthrough to bring attention to your content** — subtly dim/tint passthrough (default black tint) or apply a custom tint color; avoid bright/dramatic tints that distract or diminish immersion.
- **Create unbounded 3D experiences** with `mixed` immersion in a Full Space — blends content with passthrough, no fixed boundary; system auto-makes nearby content semi-opaque near physical objects; can request info about nearby objects/room layout (ARKit).
- **Use `progressive` immersion** to blend a custom environment with surroundings — define a specific immersion range, support portrait or landscape; Digital Crown adjusts immersion within the default 120–360 degree range or a custom range; ~1.5-meter boundary auto-defined.
- **Use `full` immersion** for a fully immersive 360-degree custom environment that completely replaces passthrough; ~1.5-meter boundary auto-defined.

**Best practices**
- **Offer multiple ways to use your app or game** — support the accessibility features people use to personalize interaction.
- **Prefer launching in the Shared Space or using `mixed` immersion** — gives people more control to increase immersion when ready.
- **Reserve immersion for meaningful moments and content** — not every task needs immersion or full immersion; design for immersing in specific tasks/content rather than defaulting to fully immersive.
- **Help people engage with key moments regardless of immersion level** — use dimming, tinting, Motion, Scale cues; start subtle, strengthen only with good reason.
- **Prefer subtle tint colors for passthrough** (visionOS 2+) — helps hands and surroundings coordinate with content; avoid bright/dramatic tints.

**Promoting comfort**
- **Be mindful of people's visual comfort** — prefer placing 3D content within the field of view; display motion comfortably to avoid distraction/confusion/discomfort.
- **Choose an immersion style that supports likely movements** — people may shift weight, turn around, sit/stand; excessive movement can interrupt experiences. Avoid `progressive`/`full` (or transition back to `mixed`) if people might need to move beyond the 1.5-meter boundary.
- **Avoid encouraging movement during progressive/full immersion** — some people can't or won't move; e.g., let people bring a virtual object closer instead of requiring them to approach it.
- **If using `mixed` immersion, avoid obscuring passthrough too much** — switch to `full`/`progressive` if virtual objects would substantially obscure passthrough.
- **Adopt ARKit to blend custom content with surroundings** — request permission for sensitive data (hand positions, etc.); see Privacy.

**Transitioning between immersive styles**
- **Design smooth, predictable transitions when changing immersion** — avoid sudden, jarring, disorienting transitions.
- **Let people choose when to enter or exit a more immersive experience** — provide a clear action (e.g., Keynote's Exit button); avoid requiring system controls to reduce immersion.
- **Indicate the purpose of an exit control** — clarify whether it returns to a less-immersive context or quits altogether; if exiting quits the app, offer a way to pause/save progress first.

**Displaying virtual hands**
- **Prefer virtual hands that match familiar characteristics** — match the viewer's hand positions/gestures for natural interaction.
- **Use caution with larger-than-real virtual hands** — oversized hands obscure content, feel clumsy, and can seem too close to the face.
- **If hand-tracking data is interrupted, fade out virtual hands and reveal the viewer's own hands** — don't let virtual hands freeze; fade back in when tracking returns.

**Creating an environment**
- **Minimize distracting content** — avoid excess movement/high-contrast detail; use highest-quality textures/shapes for important areas, lower quality/dimming elsewhere.
- **Help people distinguish interactive objects** — proximity signals interactivity (near objects invite touch; far objects don't).
- **Keep animation subtle** — small gentle movements (drifting clouds) enrich without distracting; avoid heavy movement near the edges of the field of view.
- **Create an expansive environment** regardless of setting — small/restrictive environments feel claustrophobic.
- **Use Spatial Audio to create atmosphere** — avoid too much repetition/looping; lower or stop the soundscape if other audio (e.g., a movie) plays.
- **In general, avoid a flat 360-degree image** — lacks sense of scale; prefer object meshes with lighting and shaders for subtle animation (clouds, leaves, reflections).
- **Help people feel grounded** — always provide a ground plane mesh; especially important if a flat 360-degree image must be used.
- **Minimize asset redundancy** — overusing the same assets/models reduces realism.

**Platforms:** Not supported in iOS, iPadOS, macOS, tvOS, or watchOS.

## Inclusion
Source: https://developer.apple.com/design/human-interface-guidelines/inclusion
Inclusive apps and games put people first by prioritizing respectful communication and presenting content and functionality in ways everyone can access and understand.
- Designing inclusively is iterative; be prepared to examine assumptions and evolve understanding.

**Inclusive by design**
- Investigate people's goals and perspectives, using empathy to understand how different people might respond to content and experiences (a word/image can be incomprehensible or carry unintended meaning from other perspectives).
- Human characteristics/experiences to consider across perspectives: age; gender and gender identity; race and ethnicity; sexuality; physical attributes; cognitive attributes; permanent, temporary, and situational disabilities; language and culture; religion; education; political or philosophical opinions; social and economic context.
- Avoid framing the work as merely avoiding offense — an inoffensive app isn't necessarily inclusive; focus on inclusion to achieve both.

**Welcoming language**
- **Consider the tone of your copy from different perspectives** — an academic tone, for example, can seem to welcome only high levels of education; be clear, direct, and respectful.
- **Pay attention to how you refer to people** — address people directly as *you*/*your*; avoid indirect *the user*/*the player* (feels distant); reserve *we*/*our* for the software/company, since overuse can read as insulting/condescending.
- **Avoid using specialized or technical terms without defining them** — define terms first or use plain language, which is also easier to translate.
- **Replace colloquial expressions with plain language** — colloquialisms are culture-specific and hard to translate; some carry exclusionary origins (e.g., *peanut gallery*, *grandfathered in*).
- **Consider carefully before including humor** — highly subjective and hard to translate; risks confusing, irritating, or insulting people.

**Being approachable**
- Present a clear, straightforward interface (see per-platform Designing for guidance).
- Build in ways to learn how to use the app/game — e.g., an onboarding flow with a step-by-step path that others can skip.

**Gender identity**
- Avoid unnecessary references to specific genders (e.g., replace "his or her" with a gender-neutral plural noun) — this also aids localization into gendered-pronoun languages.
- Avoid referencing a specific gender in avatars, emoji, glyphs, or game characters where possible; prefer giving people customization tools. SF Symbols offers many nongendered glyphs.
- Most apps don't need to know gender; if required (health/legal reasons), offer inclusive options like *nonbinary*, *self-identify*, and *decline to state*, and consider letting people specify pronouns.

**People and settings**
- Portray a range of human characteristics and activities (racial backgrounds, body types, ages, physical capabilities) when depicting people.
- Avoid stereotypical representations of occupations/behaviors (e.g., only male doctors, female nurses).
- Review depicted settings/objects — showing high affluence can be unwelcoming/out-of-touch in some contexts; prefer familiar, relatable places, homes, activities, and items where it makes sense.

**Avoiding stereotypes**
- Everyone holds unconscious biases; a goal of inclusive design is recognizing where they influence design decisions (e.g., a narrow definition of "family," or security questions assuming shared cultural context).
- Prefer universal human experiences over context-specific ones when writing prompts/questions (e.g., "What's your favorite activity?" over "What was your favorite subject in college?").

**Accessibility**
- Support Apple's accessibility features (VoiceOver, Display Accommodations, closed captioning, Switch Control, Speak Screen); avoid assuming a disability precludes interest in the experience.
- Each disability is a spectrum (e.g., visual disabilities range from low vision to complete blindness); everyone can experience temporary (short-term hearing loss) or situational (noisy train) disabilities.
- **Avoid images and language that exclude people with disabilities** — include people with disabilities in general representation; avoid using disability to express a negative quality.
- **Take a people-first approach when writing about people with disabilities** — describe accomplishments/goals before mentioning a disability; find out how a specific person/community self-identifies.
- **Prioritize simplicity and perceivability** — familiar, consistent interactions; ensure content is perceivable via sight, hearing, or touch.

**Languages**
- Prepare software to handle other languages/regions (*internationalization*) and provide translated text/resources for specific locales (*localization*).
- Inclusive practices (plain language, avoiding unnecessary gender references, representing variety, avoiding stereotypes) also ease localization; SF Symbols streamlines localization with LTR/RTL-ready glyphs.
- Colors carry culture-specific meaning (e.g., white signifies death/grief in some places, purity/peace in others) — ensure color-based communication means the same thing in each localized version.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Layout
Source: https://developer.apple.com/design/human-interface-guidelines/layout
A consistent layout that adapts to various contexts makes an experience more approachable and helps an app feel at home across devices.

**Best practices**
- **Group related items to help people find information** — use negative space, background shapes, colors, materials, or separator lines to relate/separate content; keep content and controls clearly distinct.
- **Make essential information easy to find by giving it sufficient space** — surface the most important info immediately; move secondary info to another part of the window or an additional view.
- **Extend content to fill the screen or window** — backgrounds/full-screen artwork should reach the display edges; scrollable layouts should continue to the bottom and sides. Controls/navigation (sidebars, tab bars) sit atop content, not on the same plane. Use a background extension view for the appearance of content behind the control layer (e.g., beneath a sidebar/inspector) when content doesn't span the full window — `backgroundExtensionEffect()` / `UIBackgroundExtensionView`.

**Visual hierarchy**
- **Differentiate controls from content** — use the Liquid Glass material for a distinct, consistent control appearance across iOS, iPadOS, and macOS; use a scroll edge effect (not a background) to transition between content and controls.
- **Place items to convey their relative importance** — people view in reading order (top-to-bottom, leading-to-trailing); place important items near the top/leading side; account for Right-to-left reading order variation.
- **Align components with one another** — aids scanning, communicates organization/hierarchy; combine with indentation to show information hierarchy.
- **Take advantage of progressive disclosure** — indicate hidden additional content (Disclosure controls, partially visible items hinting at scroll/reveal).
- **Make controls easier to use by providing enough space and grouping them logically** — insufficient spacing/crowding makes controls hard to tell apart or understand.

**Adaptability**
- iOS, iPadOS, tvOS, and visionOS define *traits* characterizing device-environment variations; SwiftUI/Auto Layout help interfaces adapt dynamically.
- Common variations to handle: device screen sizes/resolutions/color spaces; device orientation; system features (Dynamic Island, camera controls); external display support, Display Zoom, resizable iPad windows; Dynamic Type text-size changes; locale-based internationalization (LTR/RTL direction, date/time/number formatting, font variation, text length).
- **Design a layout that adapts gracefully to context changes while remaining recognizably consistent** — respect system-defined safe areas, margins, and guides; use layout modifiers to fine-tune placement.
- **Be prepared for text-size changes** — support Dynamic Type (iOS, iPadOS, tvOS, visionOS, watchOS); for Unity games, use Apple's accessibility plug-in.
- **Preview your app on multiple devices** — orientations, localizations, text sizes; start with largest/smallest layouts; test wide-gamut color on real devices; use Device Hub simulator for clipping/layout issues.
- **When necessary, scale artwork in response to display changes** — don't change aspect ratio when cropped/letterboxed/pillarboxed; scale to keep important content visible. In visionOS, the system automatically scales a window moving along the z-axis.

**Guides and safe areas**
- A *layout guide* is a rectangular region for positioning/aligning/spacing content; the system provides predefined guides for standard margins and readable text width (`UILayoutGuide`, `NSLayoutGuide`); custom guides are also possible.
- A *safe area* is the area not covered by a toolbar, tab bar, or other views (`SafeAreaRegions`); essential for avoiding features like Dynamic Island or camera housing.
- **Respect key display and system features in each platform** — non-accommodation feels out of place and harder to use; safe areas help reposition content dynamically as bar sizes change.

**Platforms:**
- **iOS:** Aim to support both portrait and landscape orientations (no need to prompt rotation — let people try both); if landscape-only, support rotation either direction equally. Prefer a full-bleed game interface accommodating corner radius, sensor housing, Dynamic Island (optionally offer letterbox/pillarbox as an alternative). Avoid full-width buttons — respect system margins and inset from screen edges; if a full-width button is needed, harmonize with hardware curvature and align with adjacent safe areas. Hide the status bar only when it adds value (e.g., games, media viewing) — otherwise keep it visible.
- **iPadOS:** People can freely resize windows to a minimum width/height (like macOS) — design for the full range of sizes. Defer switching to a compact view for as long as possible (design full-screen first); for complex layouts (Split views), prefer hiding tertiary columns (inspectors) as the view narrows. Test at common system-provided sizes (halves/thirds/quadrants) across devices; minimize unexpected UI changes at min/max window size. Consider a convertible tab bar (`sidebarAdaptable`) for adaptive sidebar/tab-bar navigation as the view resizes.
- **macOS:** Avoid placing controls or critical information at the bottom of a window (windows are often moved so the bottom is offscreen). Avoid displaying content within the camera housing at the top edge (`NSPrefersDisplaySafeAreaCompatibilityMode`).
- **tvOS:** Be prepared for a wide range of TV sizes — layouts don't auto-adapt like iPhone/iPad; the same interface shows on every display, so design carefully for varied screen sizes. Adhere to the screen's safe area: inset primary content 60 points from top/bottom, 80 points from the sides; allow only partially displayed offscreen content or deliberately-offscreen elements outside this zone. Include appropriate padding between focusable elements — an element enlarges on focus (UIKit focus APIs), so avoid overlapping important information.
  - **Grids:** use appropriate spacing between unfocused rows/columns to prevent overlap on focus (`UICollectionViewFlowLayout` auto-determines column count). Include additional vertical spacing for titled rows (avoid crowding between rows/titles). Use consistent spacing so content reads as a grid. Make partially hidden content look symmetrical (same width on each side of the screen).
- **visionOS:** See Spatial layout for depth/scale/field-of-view guidance.
  > Note: When depth is added to content in a standard window, content extending too far along the z-axis beyond the window's bounds gets clipped by the system.
  - Consider centering the most important content and controls, especially in large windows.
  - Keep a window's content within its bounds — system window controls (Share menu above, resize/move/close controls below) appear just outside the XY bounds; encroaching content makes these controls hard to use.
  - Use an ornament for additional controls that don't belong within the window (e.g., toolbar, tab bar), without interfering with system-provided controls.
  - Make interactive components easy to look at — include enough space around them (e.g., place buttons so their centers are at least 60 points apart) to avoid the hover effect obscuring content.
- **watchOS:** Design content to extend edge-to-edge (the bezel provides natural padding) — minimize padding between elements to avoid wasting space. Avoid placing more than two or three controls side by side — no more than three glyph buttons or two text buttons per row (text buttons generally work best spanning the full width, but two short-label buttons side by side can work if the screen doesn't scroll). Support autorotation in views people might show to others (e.g., displaying a QR code) — `isAutorotating`.

### Specifications

**iOS, iPadOS device screen dimensions** (portrait, pt / px@scale)

| Model | Dimensions (portrait) |
| --- | --- |
| iPad Pro 13-inch | 1032x1376 pt (2064x2752 px @2x) |
| iPad Pro 12.9-inch | 1024x1366 pt (2048x2732 px @2x) |
| iPad Pro 11-inch 5th/6th gen | 834x1210 pt (1668x2420 px @2x) |
| iPad Pro 11-inch 1st–4th gen | 834x1194 pt (1668x2388 px @2x) |
| iPad Pro 10.5-inch | 834x1112 pt (1668x2224 px @2x) |
| iPad Pro 9.7-inch | 768x1024 pt (1536x2048 px @2x) |
| iPad Air 13-inch | 1024x1366 pt (2048x2732 px @2x) |
| iPad Air 11-inch | 820x1180 pt (1640x2360 px @2x) |
| iPad Air 10.9-inch | 820x1180 pt (1640x2360 px @2x) |
| iPad Air 10.5-inch | 834x1112 pt (1668x2224 px @2x) |
| iPad Air 9.7-inch | 768x1024 pt (1536x2048 px @2x) |
| iPad 11-inch | 820x1180 pt (1640x2360 px @2x) |
| iPad 10.2-inch | 810x1080 pt (1620x2160 px @2x) |
| iPad 9.7-inch | 768x1024 pt (1536x2048 px @2x) |
| iPad mini 8.3-inch | 744x1133 pt (1488x2266 px @2x) |
| iPad mini 7.9-inch | 768x1024 pt (1536x2048 px @2x) |
| iPhone 17 Pro Max | 440x956 pt (1320x2868 px @3x) |
| iPhone 17 Pro | 402x874 pt (1206x2622 px @3x) |
| iPhone Air | 420x912 pt (1260x2736 px @3x) |
| iPhone 17 | 402x874 pt (1206x2622 px @3x) |
| iPhone 16 Pro Max | 440x956 pt (1320x2868 px @3x) |
| iPhone 16 Pro | 402x874 pt (1206x2622 px @3x) |
| iPhone 16 Plus | 430x932 pt (1290x2796 px @3x) |
| iPhone 16 | 393x852 pt (1179x2556 px @3x) |
| iPhone 16e | 390x844 pt (1170x2532 px @3x) |
| iPhone 15 Pro Max | 430x932 pt (1290x2796 px @3x) |
| iPhone 15 Pro | 393x852 pt (1179x2556 px @3x) |
| iPhone 15 Plus | 430x932 pt (1290x2796 px @3x) |
| iPhone 15 | 393x852 pt (1179x2556 px @3x) |
| iPhone 14 Pro Max | 430x932 pt (1290x2796 px @3x) |
| iPhone 14 Pro | 393x852 pt (1179x2556 px @3x) |
| iPhone 14 Plus | 428x926 pt (1284x2778 px @3x) |
| iPhone 14 | 390x844 pt (1170x2532 px @3x) |
| iPhone 13 Pro Max | 428x926 pt (1284x2778 px @3x) |
| iPhone 13 Pro | 390x844 pt (1170x2532 px @3x) |
| iPhone 13 | 390x844 pt (1170x2532 px @3x) |
| iPhone 13 mini | 360x780 pt (1080x2340 px @3x) |
| iPhone 12 Pro Max | 428x926 pt (1284x2778 px @3x) |
| iPhone 12 Pro | 390x844 pt (1170x2532 px @3x) |
| iPhone 12 | 390x844 pt (1170x2532 px @3x) |
| iPhone 12 mini | 360x780 pt (1080x2340 px @3x) |
| iPhone 11 Pro Max | 414x896 pt (1242x2688 px @3x) |
| iPhone 11 Pro | 375x812 pt (1125x2436 px @3x) |
| iPhone 11 | 414x896 pt (828x1792 px @2x) |
| iPhone XS Max | 414x896 pt (1242x2688 px @3x) |
| iPhone XS | 375x812 pt (1125x2436 px @3x) |
| iPhone XR | 414x896 pt (828x1792 px @2x) |
| iPhone X | 375x812 pt (1125x2436 px @3x) |
| iPhone 8 Plus | 414x736 pt (1080x1920 px @3x) |
| iPhone 8 | 375x667 pt (750x1334 px @2x) |
| iPhone 7 Plus | 414x736 pt (1080x1920 px @3x) |
| iPhone 7 | 375x667 pt (750x1334 px @2x) |
| iPhone 6s Plus | 414x736 pt (1080x1920 px @3x) |
| iPhone 6s | 375x667 pt (750x1334 px @2x) |
| iPhone 6 Plus | 414x736 pt (1080x1920 px @3x) |
| iPhone 6 | 375x667 pt (750x1334 px @2x) |
| iPhone SE 4.7-inch | 375x667 pt (750x1334 px @2x) |
| iPhone SE 4-inch | 320x568 pt (640x1136 px @2x) |
| iPod touch 5th gen+ | 320x568 pt (640x1136 px @2x) |

> Note: All scale factors above are UIKit scale factors, which may differ from native scale factors (`scale` and `nativeScale`).

**iOS, iPadOS device size classes** — a size class is *regular* (larger screen or landscape) or *compact* (smaller screen or portrait); `UserInterfaceSizeClass`.

| Model | Portrait orientation | Landscape orientation |
| --- | --- | --- |
| iPad Pro 12.9-inch | Regular width, regular height | Regular width, regular height |
| iPad Pro 11-inch | Regular width, regular height | Regular width, regular height |
| iPad Pro 10.5-inch | Regular width, regular height | Regular width, regular height |
| iPad Air 13-inch | Regular width, regular height | Regular width, regular height |
| iPad Air 11-inch | Regular width, regular height | Regular width, regular height |
| iPad 11-inch | Regular width, regular height | Regular width, regular height |
| iPad 9.7-inch | Regular width, regular height | Regular width, regular height |
| iPad mini 7.9-inch | Regular width, regular height | Regular width, regular height |
| iPhone 17 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 17 Pro | Compact width, regular height | Compact width, compact height |
| iPhone Air | Compact width, regular height | Regular width, compact height |
| iPhone 17 | Compact width, regular height | Compact width, compact height |
| iPhone 16 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 16 Pro | Compact width, regular height | Compact width, compact height |
| iPhone 16 Plus | Compact width, regular height | Regular width, compact height |
| iPhone 16 | Compact width, regular height | Compact width, compact height |
| iPhone 16e | Compact width, regular height | Compact width, compact height |
| iPhone 15 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 15 Pro | Compact width, regular height | Compact width, compact height |
| iPhone 15 Plus | Compact width, regular height | Regular width, compact height |
| iPhone 15 | Compact width, regular height | Compact width, compact height |
| iPhone 14 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 14 Pro | Compact width, regular height | Compact width, compact height |
| iPhone 14 Plus | Compact width, regular height | Regular width, compact height |
| iPhone 14 | Compact width, regular height | Compact width, compact height |
| iPhone 13 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 13 Pro | Compact width, regular height | Compact width, compact height |
| iPhone 13 | Compact width, regular height | Compact width, compact height |
| iPhone 13 mini | Compact width, regular height | Compact width, compact height |
| iPhone 12 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 12 Pro | Compact width, regular height | Compact width, compact height |
| iPhone 12 | Compact width, regular height | Compact width, compact height |
| iPhone 12 mini | Compact width, regular height | Compact width, compact height |
| iPhone 11 Pro Max | Compact width, regular height | Regular width, compact height |
| iPhone 11 Pro | Compact width, regular height | Compact width, compact height |
| iPhone 11 | Compact width, regular height | Regular width, compact height |
| iPhone XS Max | Compact width, regular height | Regular width, compact height |
| iPhone XS | Compact width, regular height | Compact width, compact height |
| iPhone XR | Compact width, regular height | Regular width, compact height |
| iPhone X | Compact width, regular height | Compact width, compact height |
| iPhone 8 Plus | Compact width, regular height | Regular width, compact height |
| iPhone 8 | Compact width, regular height | Compact width, compact height |
| iPhone 7 Plus | Compact width, regular height | Regular width, compact height |
| iPhone 7 | Compact width, regular height | Compact width, compact height |
| iPhone 6s Plus | Compact width, regular height | Regular width, compact height |
| iPhone 6s | Compact width, regular height | Compact width, compact height |
| iPhone SE | Compact width, regular height | Compact width, compact height |
| iPod touch 5th gen+ | Compact width, regular height | Compact width, compact height |

**watchOS device screen dimensions**

| Series | Size | Width (px) | Height (px) |
| --- | --- | --- | --- |
| Apple Watch Ultra (3rd gen) | 49mm | 422 | 514 |
| 10, 11 | 42mm | 374 | 446 |
| 10, 11 | 46mm | 416 | 496 |
| Apple Watch Ultra (1st/2nd gen) | 49mm | 410 | 502 |
| 7, 8, 9 | 41mm | 352 | 430 |
| 7, 8, 9 | 45mm | 396 | 484 |
| 4, 5, 6, SE (all gens) | 40mm | 324 | 394 |
| 4, 5, 6, SE (all gens) | 44mm | 368 | 448 |
| 1, 2, 3 | 38mm | 272 | 340 |
| 1, 2, 3 | 42mm | 312 | 390 |

## Privacy
Source: https://developer.apple.com/design/human-interface-guidelines/privacy
Privacy is paramount: apps must be transparent about the privacy-related data and resources they require, and must protect the data people allow them to access.
- App submissions must declare privacy practices and privacy-relevant data collected, shown on the App Store product page (manageable in App Store Connect); people use this to decide before downloading.

**Best practices**
- **Request access only to data that you actually need** — over-asking, or asking before interest is shown, erodes trust; make permission requests as specific as possible.
- **Be transparent about how your app collects and uses people's data** — respect choices like Hide My Email and Mail Privacy Protection; understand app tracking obligations.
- **Process data on the device where possible** — e.g., Apple Neural Engine + custom CreateML models on iOS avoid risky/lengthy remote round trips.
- **Adopt system-defined privacy protections and follow security best practices** — e.g., CloudKit for encryption/key management of strings, numbers, dates (iOS 15+).

**Requesting permission**
- Data/resources requiring permission: personal data (location, health, financial, contact, other PII); user-generated content (emails, messages, calendar, contacts, gameplay info, Apple Music activity, HomeKit data, audio/video/photo content); protected resources (Bluetooth peripherals, home automation, Wi-Fi, local networks); device capabilities (camera, microphone); in visionOS Full Space, ARKit data (hand tracking, plane estimation, image anchoring, world tracking); the device's advertising identifier (app tracking).
- The system shows a standard alert with your supplied purpose-string copy; people can also review/change choices later in Settings > Privacy.
- **Request permission only when your app clearly needs access** — ideally wait until people use the feature requiring it (e.g., a Location button after they show interest).
- **Avoid requesting permission at launch unless required for the app to function** — launch-time requests are acceptable when obviously necessary (e.g., a navigation app needing location, or a visionOS game needing surroundings access before gameplay).
- **Write copy that clearly describes how your app uses the ability, data, or resource** — a brief, complete, straightforward, specific sentence; sentence case, active voice, ending period.

| Example purpose string | Notes |
| --- | --- |
| "The app records during the night to detect snoring sounds." | Active sentence, clearly describes how/why. |
| "Microphone access is needed for a better experience." | Passive, vague, undefined justification. |
| "Turn on microphone access." | Imperative, no justification. |

**Pre-alert screens, windows, or views** (custom screens shown before a system permission alert)
- **Include only one button and make it clear that it opens the system alert** — don't include a button that doesn't open the alert (feels manipulative); don't title the custom button "Allow" (risks people mistakenly tapping through without meaning to accept) — use "Continue" or "Next" instead.
- **Don't include additional actions in your custom screen or window** — e.g., no option to close/cancel without seeing the system alert.

**Tracking requests**
- If tracking as soon as the app launches, the system-provided alert must display before any tracking data is collected.
- **Never precede the system-provided alert with a custom screen that could confuse or mislead people** — prohibited designs (cause App Review rejection) include offering incentives, displaying a screen/window that looks like a request, showing an image of the alert, or annotating the screen behind the alert. See App Review Guidelines: 5.1.1 (iv).

**Location button** (iOS, iPadOS, watchOS — Core Location)
- Lets people grant temporary, one-time location authorization at the moment a task needs it; appearance can vary to match app UI but always communicates location sharing recognizably.
- First tap shows a standard alert explaining the button's limited-access behavior; after confirming understanding, tapping the button grants one-time permission (expires when the person stops using the app) without needing to reconfirm.
> Note: With no authorization status, tapping the button acts like choosing *Allow Once*. If *While Using the App* was previously chosen, tapping the button doesn't change status (`LocationButton` SwiftUI / `CLLocationButton`).
- **Consider using the location button for a lightweight way to share location for specific features** (attach location to a message/post, find a store, identify something nearby) — especially if people often grant only *Allow Once*.
- **Consider customizing the location button to harmonize with your UI** — you may choose: the system-provided title (e.g., "Current Location," "Share My Current Location"); filled or outlined glyph; background/title/glyph color; corner radius. Other visual attributes can't be customized, to preserve recognizability/trust; the system warns about low-contrast combinations or excess translucency; you must ensure text fits without truncation at all accessibility text sizes and in all translations.
> Important: If the system identifies consistent problems with a customized location button, it won't grant location access on tap (though the button can still perform other app-specific actions) — people may lose trust if it doesn't work as expected.

**Protecting data**
- **Avoid relying solely on passwords for authentication** — prefer passkeys; if passwords remain, add two-factor authentication; use Face ID, Optic ID, or Touch ID for apps kept logged in (`Local Authentication`).
- **Store sensitive information in a keychain** — provides a secure, predictable experience (`Keychain services`).
- **Never store passwords or other secure content in plain-text files** — even with restricted file permissions, an encrypted keychain is far safer.
- **Avoid inventing custom authentication schemes** — prefer passkeys, Sign in with Apple, or Password AutoFill.

**Platforms:**
- No additional considerations for iOS, iPadOS, tvOS, or watchOS.
- **macOS:** Sign your app with a valid Developer ID for distribution outside the store. Protect people's data with app sandboxing — required for all Mac App Store submissions (`Configuring the macOS App Sandbox`). Avoid making assumptions about who is signed in — fast user switching can mean multiple people are active on the same system.
- **visionOS:** ARKit algorithms (persistence, world mapping, segmentation, matting, environment lighting) run automatically in the Shared Space but don't send data to apps there; a Full Space is required to access ARKit APIs. Features like Plane Estimation, Scene Reconstruction, Image Anchoring, and Hand Tracking require explicit permission. User input is private by design — the system shows hover effects for interactive SwiftUI/RealityKit components without exposing gaze location before a tap. Camera access differs from other platforms: the back camera provides blank input (compatibility convenience only); the front camera provides input only after permission is granted. If bringing an iOS/iPadOS app with camera-dependent features to visionOS, remove the feature or replace it with content import.

## Right to left
Source: https://developer.apple.com/design/human-interface-guidelines/right-to-left
Support right-to-left (RTL) languages like Arabic and Hebrew by reversing the interface as needed to match the reading direction of the related scripts.
- System-provided UI frameworks support RTL by default — system components flip automatically; using system-provided elements and standard layouts may require no changes.

**Text alignment**
- **Adjust text alignment to match the interface direction**, if not automatic (e.g., left-aligned text in LTR becomes right-aligned in RTL to match the mirrored content position).
- **Align a paragraph (three or more lines) based on its language, not the current context** — mismatched alignment is hard to read; continue matching one- and two-line text blocks to the current context's reading direction, but align full paragraphs to their own language.
- **Use a consistent alignment for all text items in a list** — reverse alignment for all list items, including items in a different script, for comfortable reading/scanning.

**Numbers and characters**
- Hebrew text uses Western Arabic numerals; Arabic text may use Western or Eastern Arabic numerals (usage varies by country/region/area) — identify the appropriate representation per locale for number-centric content; apps that don't address numbers can rely on system-provided representations.
- **Don't reverse the order of numerals in a specific number** — digits in a number (e.g., "541," a phone number, a credit card number) always appear in the same order regardless of language/context.
- **Reverse the order of numerals that show progress or a counting direction; never flip the numerals themselves** — for controls like progress bars, sliders, rating controls, and any numeral sequence communicating specific order.

**Controls**
- **Flip controls that show progress from one value to another** (sliders, progress indicators) — people view forward progress as matching their reading direction; also reverse accompanying glyphs/images depicting beginning/ending values.
- **Flip controls that help people navigate or access items in a fixed order** — e.g., in RTL, a back button must point right to match screen-flow reading order; next/previous buttons for ordered lists flip similarly.
- **Preserve the direction of a control that refers to an actual direction or points to an onscreen area** — e.g., a "to the right" control always points right regardless of context.
- **Visually balance adjacent Latin and RTL scripts when necessary** — Arabic/Hebrew (no uppercase) can look small next to uppercased Latin text; increasing RTL font size by about 2 points often balances this.

**Images**
- **Avoid flipping images like photographs, illustrations, and general artwork** — flipping can change meaning or violate copyright; create a new image version if content is strongly tied to reading direction.
- **Reverse the positions of images when their order is meaningful** — e.g., chronological, alphabetical, or favorite ordering should reverse in RTL to preserve meaning.

**Interface icons**
- SF Symbols provides RTL variants and localized symbols for Arabic, Hebrew, and other languages; custom symbols can specify their own directionality (`Creating custom symbol images for your app`).
- **Flip interface icons that represent text or reading direction** — e.g., left-aligned text-representing bars become right-aligned in RTL.
- **Consider creating a localized version of an interface icon that displays text** — for icons with letters/words tied to script concepts (font-size choice, signature); if unrelated to reading/writing, consider a text-free alternative instead.
- **Flip an interface icon that shows forward or backward motion** — direction matching reading direction reads as "forward"; e.g., a speaker icon's sound waves should flip to emanate from the correct side in RTL.
- **Don't flip logos or universal signs and marks** — flipped logos confuse people and can have legal repercussions; universal symbols (e.g., checkmark) must keep a consistent appearance.
- **In general, avoid flipping interface icons that depict real-world objects** — unless the object indicates directionality (e.g., clocks look the same everywhere; icons showing a right-handed tool don't need flipping since most people are right-handed).
- **Before merely flipping a complex custom interface icon, consider its individual components and overall visual balance** — some components (badge, slash, magnifying glass) must adhere to a visual design language regardless of localization (e.g., SF Symbols keeps the same backslash for prohibition/negation in both LTR and RTL). In other cases, flip a component or its position to preserve meaning (e.g., a badge depicting actual in-app UI should flip if the UI flips) or to preserve visual balance. If a component implies handedness (a tool), consider preserving its orientation while flipping the base image if needed.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Spatial layout
Source: https://developer.apple.com/design/human-interface-guidelines/spatial-layout
Spatial layout techniques help take advantage of the infinite canvas of Apple Vision Pro and present content in engaging, comfortable ways.

**Field of view** — the space a person can see without moving their head; dimensions vary by Light Seal configuration and peripheral acuity.
> Important: The system doesn't provide information about a person's field of view.
- **Center important content within the field of view** — visionOS launches apps directly in front of people by default; in immersive experiences, keep attention on important content and avoid distracting motion or bright, high-contrast objects in the periphery.
- **Avoid anchoring content to the wearer's head** — statically-anchored content can feel stuck, confined, and uncomfortable, especially if it obscures passthrough and decreases apparent surrounding stability; instead anchor content in people's space so they can look around naturally.

**Depth**
- The system automatically uses color temperature, reflections, and shadow to communicate depth of virtual content; visual effects change as objects/viewer positions change, making the experience feel lifelike.
- Incorporating small amounts of depth even in standard windows helps content look natural (SwiftUI adds depth effects to 2D window views automatically). For additional depth, use RealityKit to create a 3D object, or a *volume* (a window-like component without a visible frame) for displaying 3D content.
- **Provide visual cues that accurately communicate the depth of your content** — missing or conflicting cues cause visual discomfort.
- **Use depth to communicate hierarchy** — objects stand out and become more noticeable; people notice depth changes (e.g., a window recedes along the z-axis when a sheet appears over it).
- **In general, avoid adding depth to text** — text that hovers above its background is hard to read, slows people down, and can cause vision discomfort.
- **Make sure depth adds value** — use depth to clarify and delight, not everywhere; depth suits large, important elements (tab bar/toolbar standing out from a window) more than small objects (e.g., a button's symbol standing out can reduce legibility/usability). Frequent or rapid depth changes are tiring because eyes must refocus each time.

**Scale**
- *Dynamic scale*: visionOS automatically increases a window's scale as it moves away from the wearer and decreases it as it moves closer, so it appears to maintain the same size at all distances — keeps content comfortably legible/interactive regardless of proximity.
- *Fixed scale*: an object maintains the same scale regardless of proximity, appearing smaller farther away (like a physical object).
- To support dynamic scaling, visionOS defines a point as an angle (unlike other platforms, which define a point as pixels varying with display Resolution).
- **Consider using fixed scale when you want a virtual object to look exactly like a physical object** — e.g., to preserve life-size scale of a product; because interactive content needs to scale for usability as it moves, prefer fixed scale sparingly, reserved for noninteractive objects.

**Best practices**
- **Avoid displaying too many windows** — obscures surroundings, feels overwhelming/constricted, and makes relocating the app cumbersome (moving many windows).
- **Prioritize standard, indirect gestures** — *indirect* gestures don't require moving the hand into the field of view; *direct* gestures (touching the virtual object) can be tiring, especially above the line of sight. Indirect gestures work at any distance; reserve direct gestures for nearby objects inviting close inspection/manipulation for short periods.
- **Rely on the Digital Crown to help people recenter windows in their field of view** — pressing it recenters content; the app needs no special support for this.
- **Include enough space around interactive components to make them easy for people to look at** — the hover effect confirms the looked-at element; place multiple regular-size components with centers at least 60 points apart, leaving 16 points or more of space between them; don't let controls overlap other interactive elements/views (makes selecting a single element difficult).
- **Let people use your app with minimal or no physical movement** — unless movement is essential, support remaining stationary.
- **Use the floor to help you place a large immersive experience** — align a flat horizontal plane with the floor for content extending up from it, to blend seamlessly and feel intuitive.

**Platforms:** Not supported in iOS, iPadOS, macOS, tvOS, or watchOS.

## Writing
Source: https://developer.apple.com/design/human-interface-guidelines/writing
The words chosen within an app are an essential part of its user experience, whether building onboarding, writing an alert, or describing an image for accessibility.

**Getting started**
- **Determine your app's voice** — think about who you're addressing and the vocabulary that suits them (e.g., banking app conveys trust/stability; a game conveys excitement/fun); keep a list of common terms for consistency.
- **Match your tone to the context** — vary tone by situation (e.g., straightforward/direct for a serious alert vs. light/congratulatory for a milestone), considering both the physical and in-app context.
- **Be clear** — choose easily understood words that convey the right thing; check whether each word needs to be there; read writing out loud to check clarity.
- **Write for everyone** — use simple, plain language; write with accessibility and localization in mind; avoid jargon and gendered terminology.

**Best practices**
- **Consider each screen's purpose** — order elements with the most important information first; format text for easy reading; break up multiple ideas across multiple screens and think through the information flow.
- **Be action oriented** — use active voice and clear (usually verb-based) labels for buttons/links; prioritize clarity over cute/clever labels (e.g., "Send" over "Let's do it!"); avoid "Click here" for links in favor of descriptive phrases (e.g., "Learn more about UX Writing") — especially important for screen reader users.
- **Build language patterns** — consistency builds familiarity and cohesion, and makes future writing easier.
- **Adopt capitalization rules that align with your app's style, then apply them consistently** — title case reads as more formal, sentence case as more casual; choose one style per UI element type and apply it throughout.
- **Give clear guidance and use consistent language throughout multi-step processes** — start flows with language like "Get Started"; use consistent continuation language ("Continue"/"Next," or a hint at the next step); signal completion with language like "Done."
- **Use possessive pronouns sparingly** — e.g., "Favorites" is as clear and more succinct than "Your Favorites"; if used, stay consistent and don't switch perspectives; avoid "we" altogether (unclear referent), especially in error messages (prefer "Unable to load content" over "We're having trouble loading this content").
- **Write for how people use each device** — keep language consistent across devices but adjust text per device (e.g., "tap" not "click" on touch devices); iPhone/Apple Watch allow personalization but demand brevity for small screens; TVs are viewed by multiple people in shared spaces and require brevity for legibility at a distance.
- **Provide clear next steps on any blank screens** — empty states (e.g., an empty to-do list) are a chance to welcome people and showcase voice, but content must stay useful/contextual; guide people to available actions with a button or link since empty states are usually temporary and shouldn't carry crucial information that later disappears.
- **Write clear error messages** — help people avoid errors first; when necessary, display the error close to the problem, avoid blame, and be clear about the fix (e.g., "Choose a password with at least 8 characters" over "That password is too short"); avoid unnecessary interjections like "oops!"/"uh-oh"; if language alone can't fix a widely-affecting error, rethink the interaction.
- **Choose the right delivery method** — weigh urgency, importance, context, need for immediate action, and supporting information when picking a delivery method and tone (see Notifications, Alerts, Action sheets).
- **Keep settings labels clear and simple** — label practically; add an explanation only if the label alone is insufficient, describing what happens when the setting is on (the off state can be inferred); provide a direct link/button to a setting rather than describing its location.
- **Show hints in text fields** — clearly label all fields and use hint/placeholder text (e.g., "name@example.com" or "Your name"); show errors next to the field with instructions on correct entry rather than scolding (e.g., "Use only letters for your name" over "Don't use numbers or symbols"); avoid robotic messages like "Invalid name."

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.
