# HIG — Getting started / Platforms
design-principles, designing-for-ios, designing-for-ipados, designing-for-macos, designing-for-tvos, designing-for-visionos, designing-for-watchos, designing-for-games

## Design principles
Source: https://developer.apple.com/design/human-interface-guidelines/design-principles
Foundational principles — Purpose, Agency, Responsibility, Familiarity, Flexibility, Simplicity, Craft, Delight — for weighing competing priorities and making key design decisions across all Apple platforms.

**Purpose**
- **Create value.** At every stage, ask what the product is for and whether the design serves that purpose.
- **Keep focused.** Prioritize the most important features by aligning with how people want to use the app; a clear use helps people meet their goals more effectively.
- **Find new ways to solve the problem.** Investigate existing solutions and avoid re-creating them; define what sets the product apart.

**Agency**
- **Stay out of the way.** Get people directly to the task or content at hand; the best designs are unobtrusive and present only when needed.
- **Give people the freedom to explore.** Let people move through the interface and access features without being locked into flows or modes; make guided flows easy to skip or escape.
- **Help people recover from mistakes.** Build forgiveness into the design so people feel free to explore; recovering from the unexpected shouldn't cost time or work.

**Responsibility**
- **Be fully transparent about what your product does and why.** Make intentions clear from the first interaction; give a clear rationale when asking for permission, and be clear about what data is collected and how it's used.
- **Keep people's information safe.** Only collect what the product needs to function; anticipate misuse and put protections in place against abuse and unintended consequences.

**Familiarity**
- **Use concepts that people know.** Draw on real-world and software knowledge to make the interface feel familiar and intuitive.
- **Keep visuals and interactions consistent.** Apply an established behavior or appearance throughout the design so people learn faster and trust new interactions to work as expected.
- **Provide clear feedback.** Show when controls are available, indicate when content changes, and use system patterns to display alerts and offer choices.

**Flexibility**
- **Design for everyone.** Treat accessibility as a priority from the start; design inclusively for the broadest possible audience.
- **Preserve a person's context.** Keep content and controls in consistent, predictable positions, and use natural animations to ease transitions across platforms and configurations.
- **Consider a variety of input methods.** Design for voice, touch, keyboard, and more so more people can use the product the way that works best for them.
- **Approach every platform with intention.** Give each supported platform the same level of care so the software feels polished and at home wherever it runs.

**Simplicity**
- **Include just what's necessary.** Simplicity isn't minimalism — aim for a focused, useful experience, keep important things close, and let the rest fall away.
- **Be concise.** Choose exactly the words needed to convey a concept or label a control.
- **Establish hierarchy.** Prioritize recognizable controls and a consistent structure so people know where they are and what comes next.

**Craft**
- **Quality sets the tone.** Be deliberate with each decision; strive for stunning visuals, smooth animations, precise wording, and thoughtful audio.
- **Experiment and iterate.** Prototype early, try new approaches, discard what doesn't work, and test in real-world settings for durability, reliability, and performance.
- **Maintain your craft.** Keep the interface current with the latest platform capabilities and design patterns — design is an ongoing commitment.

**Delight**
- **Identify the emotion you want to inspire.** Know the feeling you want to evoke and let it shape the design.
- **Create defining moments.** Treat every interaction — from a button press to an error message — as a chance to reflect the software's character.
- **Don't mistake delight for decoration.** Don't let pursuit of delight get in the way of the product's core purpose; balance a practical touch against whimsy per design.
- **Consider the whole.** Delight is the sum of the freedom to act, the safety to explore, the comfort of familiar metaphors, and the flexibility to transition across contexts.

## Designing for iOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ios
iOS is the platform for iPhone, where people stay connected, play games, view media, accomplish tasks, and track personal data in any location while on the go.
- **Display:** medium-size, high-resolution.
- **Ergonomics:** held in one or both hands, switching between portrait and landscape; viewing distance typically no more than 1–2 feet.
- **Inputs:** Multi-Touch gestures, virtual keyboards, voice control; personal data and gyroscope/accelerometer input; possible spatial interactions.
- **App interactions:** sessions range from a minute or two (checking updates, tracking data, messaging) to an hour or more (browsing, gaming, media); people typically keep multiple apps open and switch among them frequently.
- **System features:** Widgets, Home Screen quick actions, Spotlight, Shortcuts, Activity views.
- Limit the number of onscreen controls to help people concentrate on primary tasks and content; make secondary details and actions discoverable with minimal interaction.
- Adapt seamlessly to appearance changes — device orientation, Dark Mode, Dynamic Type — letting people choose configurations that work best for them.
- Support interactions that accommodate how people usually hold the device: place controls in the middle or bottom area for easier reach, and let people swipe to navigate back or initiate actions in a list row.
- With people's permission, integrate platform capabilities (payments, biometric authentication, location) to enhance the experience without asking people to enter data.

## Designing for iPadOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados
iPadOS is the platform for iPad, valued for power, mobility, and flexibility across media, games, detailed productivity tasks, and content creation.
- **Display:** large, high-resolution.
- **Ergonomics:** held, set on a surface, or placed on a stand; viewing distance typically about 3 feet.
- **Inputs:** Multi-Touch gestures, virtual keyboards, an attached keyboard or pointing device, Apple Pencil, or voice — often combined.
- **App interactions:** from a few quick actions to hours immersed in games, media, content creation, or productivity; multiple apps onscreen at once, with drag and drop between them.
- **System features:** Multitasking, Widgets, Drag and drop.
- Take advantage of the large display to elevate content people care about, minimizing modal interfaces and full-screen transitions, and position onscreen controls where they're easy to reach but not in the way.
- Use viewing distance and input mode to help determine the size and density of onscreen content.
- Let people use Multi-Touch gestures, a physical keyboard or trackpad, or Apple Pencil, and consider supporting interactions that combine multiple input modes.
- Adapt seamlessly to appearance changes — device orientation, multitasking modes, Dark Mode, Dynamic Type — and transition effortlessly to running in macOS.

## Designing for macOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-macos
macOS is the platform for Mac, relied on for power, spaciousness, and flexibility in productivity, media, and games, often across several apps at once.
- **Display:** large, high-resolution; workspace can extend across additional displays, including an iPad.
- **Ergonomics:** stationary use, typically on a desk or table; viewing distance about 1 to 3 feet.
- **Inputs:** any combination of physical keyboards, pointing devices, game controls, and Siri.
- **App interactions:** minutes of quick tasks to several hours of deep concentration; multiple apps open at once with smooth transitions between active and inactive states.
- **System features:** the menu bar, file management, going full screen, Dock menus.
- Leverage large displays to present more content in fewer nested levels and with less modality, while maintaining comfortable information density.
- Let people resize, hide, show, and move windows to fit their work style and device configuration; support full-screen mode for a distraction-free context.
- Use the menu bar to give people easy access to all the commands they need.
- Help people take advantage of high-precision input for pixel-perfect selections and edits.
- Handle keyboard shortcuts to accelerate actions and support keyboard-only work styles.
- Support personalization — customizable toolbars, windows configured to show the views used most, and chosen colors and fonts.

## Designing for tvOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos
tvOS is the platform for Apple TV, delivering vibrant content, immersive experiences, and streamlined interactions across media, games, fitness, education, and home utility apps.
- **Display:** very large, high-resolution.
- **Ergonomics:** stationary, typically 8 feet or more away, sometimes interacting while moving around the room.
- **Inputs:** remote, game controller, voice, and apps running on other devices.
- **App interactions:** deep immersion often lasting hours, with picture-in-picture used to simultaneously follow an alternative app or video.
- **System features:** Integrating with the TV app, SharePlay, Top Shelf, TV provider accounts.
- Support powerful, delightful interactions through the fluid, familiar gestures people make with the Siri Remote.
- Embrace the tvOS focus system, letting it gently highlight and expand onscreen items as people move among them.
- Deliver beautiful, edge-to-edge artwork, subtle and fluid animations, and engaging audio for a rich, cinematic experience that's clear, legible, and captivating from across the room.
- Enhance multiuser support by making sign-in easy and infrequent, handling shared sign-in, and automatically switching profiles when the current viewer changes.

## Designing for visionOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos
visionOS is the platform for Apple Vision Pro, an infinite 3D spatial computing space where people engage with apps and games while staying connected to their surroundings.
- **Space:** a limitless canvas for viewing Windows, visionOS volumes, and 3D objects, with the option to enter deeply immersive experiences.
- **Immersion:** apps launch by default in the *Shared Space*, where multiple apps run side-by-side and windows can be opened, closed, and relocated; people can transition an app to a *Full Space*, where it's the only app running and 3D content can blend with surroundings, open a portal to another place, or enter a different world.
- **Passthrough:** live video from the device's external cameras lets people interact with virtual content while seeing their actual surroundings; the Digital Crown controls the amount of passthrough.
- **Spatial Audio:** combines acoustic and visual-sensing technologies to model the sonic characteristics of a person's surroundings so audio sounds natural; with permission, an app can fine-tune this to bring custom experiences to life.
- **Eyes and hands:** most actions use an *indirect* gesture (look at an object, then tap to activate); people can also use a *direct* gesture (touching a virtual object with a finger).
- **Ergonomics:** the system automatically places content relative to the wearer's head regardless of height or whether they're sitting, standing, or lying down, so people can remain at rest while content comes to them.
- **Accessibility:** supports VoiceOver, Switch Control, Dwell Control, Guided Access, Head Pointer, and more; system-provided UI components build in accessibility support by default.
> Important: Pay special attention to user safety given the device's spatial computing characteristics. Apple Vision Pro should not be used while operating a vehicle or heavy machinery, and is not designed for use while moving around unsafe environments such as balconies, streets, stairs, or other hazards. It's designed to be fit and used only by individuals 13 years of age or older.
- **Embrace the unique features of Apple Vision Pro.** Take advantage of space, Spatial Audio, and immersion, integrating passthrough and spatial input from eyes and hands in ways that feel at home on the device.
- **Consider different types of immersion for your app's most distinctive moments.** Present experiences windowed, fully immersive, or in between; find the minimum level of immersion that suits each key moment rather than assuming everything needs to be fully immersive.
- **Use windows for contained, UI-centric experiences.** Prefer standard windows that appear as planes in space with familiar controls; people can relocate windows anywhere, and the system's scale keeps window content legible whether near or far.
- **Prioritize comfort:**
  - Display content within a person's field of view, positioned relative to their head; avoid places that require turning the head or changing position to interact.
  - Avoid content that's overwhelming, jarring, too fast, or missing a stationary frame of reference.
  - Support interactions that let people's hands rest in their lap or at their sides.
  - For direct gestures, keep interactive content within reach and avoid requiring extended interaction periods.
  - Avoid encouraging people to move too much during fully immersive experiences.
- **Help people share activities with others.** Support shared activities so people can view the *spatial Personas* of other participants, making it feel like everyone is together in the same space.

## Designing for watchOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos
watchOS is the platform for Apple Watch, giving people quick access to essential information and simple, timely tasks whether stationary or in motion.
- **Display:** small, fits on the wrist, easy-to-read and high-resolution.
- **Ergonomics:** usually no more than a foot away, raised to view and operated with the opposite hand; the Always On display lets people view information when they drop their wrist.
- **Inputs:** the Digital Crown for vertical navigation and inspecting data (watch face, Home Screen, and within apps); tap, swipe, and drag gestures usable while in motion; the Action button initiates an essential action without looking at the screen; shortcuts for routine tasks; device sensors — GPS, blood oxygen and heart function, altimeter, accelerometer, gyroscope.
- **App interactions:** many glances at the Always On display per day, each interaction typically under a minute; related experiences — complications, notifications, Siri — are used more than the app itself.
- **System features:** Complications, Notifications, Always On, Watch faces.
- Support quick, glanceable, single-screen interactions that deliver critical information succinctly with a simple gesture or two.
- Minimize the depth of the app's navigation hierarchy, and use the Digital Crown for vertical navigation (scrolling or switching between screens).
- Personalize the experience by proactively anticipating people's needs and using on-device data for content relevant now or very soon.
- Use complications to provide relevant, potentially dynamic data and graphics on the watch face, viewable on every wrist raise and tappable to dive straight into the app.
- Use notifications to deliver timely, high-value information and let people perform important actions without opening the app.
- Use background content such as color to convey useful supporting information, and materials to illustrate hierarchy and a sense of place.
- Design the app to function independently, complementing notifications and complications with additional details and functionality.

## Designing for games
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-games
Cross-platform guidance for making a game feel at home on every Apple device by integrating the platform characteristics, accessibility practices, and Apple technologies people love.

**Jump into gameplay**
- **Let people play as soon as installation completes.** Include as much playable content as possible in the initial install, keep download time to 30 minutes or less, and download additional content in the background.
- **Provide great default settings.** Use device info to choose the best defaults (graphics resolution, automatic recognition of paired accessories/game controllers, a player's accessibility settings), and support the platform's most common interaction methods.
- **Teach through play.** Integrate configuration and onboarding into a playable tutorial that engages people quickly and helps them feel successful right away; offer a written tutorial as an optional reference rather than a prerequisite.
- **Defer requests until the right time.** Get the player's permission before using sensors or personalizing gameplay with data like hand-tracking, integrating the request into the scenario that requires it; wait until people have spent quality time with the game before asking for a rating or review.

**Look stunning on every display**
- **Make sure text is always legible.** Ensure text contrasts well with the background and uses at least the platform's recommended minimum text size.

| Platform | Default text size | Minimum text size |
| --- | --- | --- |
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

- **Make sure buttons are always easy to use.** Each platform defines a recommended minimum button size based on its default interaction method — e.g., buttons in iOS must be at least 44x44 pt to accommodate touch.

| Platform | Default button size | Minimum button size |
| --- | --- | --- |
| iOS, iPadOS | 44x44 pt | 28x28 pt |
| macOS | 28x28 pt | 20x20 pt |
| tvOS | 66x66 pt | 56x56 pt |
| visionOS | 60x60 pt | 28x28 pt |
| watchOS | 44x44 pt | 28x28 pt |

- **Prefer resolution-independent textures and graphics.** If that isn't possible, match asset resolution to the device's; in visionOS prefer vector-based art that continues to look good as the system dynamically scales it for different viewing distances and angles.
- **Integrate device features into your layout.** Accommodate features like rounded corners or a camera housing during layout, relying on platform-provided safe areas when possible.
- **Make sure in-game menus adapt to different aspect ratios.** Support ratios such as 16:10, 19.5:9, and 4:3 — and both orientations on iPhone and iPad where supported — keeping menus legible and easy to use without obscuring other content; prefer dynamic layouts with relative constraints over fixed layouts, and create device-specific layouts only when necessary.
- **Design for the full-screen experience.** In macOS, iOS, and iPadOS, full-screen mode hides other apps and system UI; in visionOS, a game running in a Full Space can completely surround people.

**Enable intuitive interactions**
- **Support each platform's default interaction method.** Pay special attention to control sizing and menu behavior, especially when bringing a game from a pointer-based context to a touch-based one.

| Platform | Default interaction methods | Additional interaction methods |
| --- | --- | --- |
| iOS | Touch | Game controller |
| iPadOS | Touch | Game controller, keyboard, mouse, trackpad, Apple Pencil |
| macOS | Keyboard, mouse, trackpad | Game controller |
| tvOS | Remote | Game controller, keyboard, mouse, trackpad |
| visionOS | Touch | Game controller, keyboard, mouse, trackpad, spatial game controller |
| watchOS | Touch | – |

- **Support physical game controllers, while also giving people alternatives.** Every platform except watchOS supports physical game controllers; since not every player can use one, also offer alternative ways to interact.
- **Offer touch-based game controls that embrace the touchscreen experience on iPhone and iPad.** In iOS and iPadOS, allow direct interaction with game elements and virtual controls overlaid on game content.

**Welcome everyone**
- **Prioritize perceivability.** Ensure content can be perceived through sight, hearing, or touch — e.g., avoid relying solely on color to convey an important detail, and provide descriptive subtitles or other ways to read cutscene content.
- **Help players personalize their experience.** Let players customize parameters like type size, game control mapping, motion intensity, and sound balance; use built-in Apple accessibility technologies (system frameworks or Unity plug-ins) to support personalization.
- **Give players the tools they need to represent themselves.** Support the spectrum of self-identity in avatars, names, and descriptions.
- **Avoid stereotypes in your stories and characters.** Review characters and scenarios to uncover and remove biases and stereotypes; when referencing real-life cultures and languages, be respectful.

**Adopt Apple technologies**
- **Integrate Game Center** to help players discover the game across devices, connect with friends, track progress and achievements, and set up leaderboards, challenges, and multiplayer activities.
- **Let players pick up their game on any of their devices** by supporting `GameSave`, using a single iCloud account to save state and resume elsewhere.
- **Support haptics** by adopting `Core Haptics` to compose and play custom haptic patterns, optionally combined with custom audio; available in iOS, iPadOS, tvOS, and visionOS, and supported on many game controllers.
- **Use Spatial Audio** to let multichannel audio adapt automatically to the current device for an immersive experience where supported.
- **Take advantage of Apple technologies for unique gameplay mechanics** — e.g., augmented reality, machine learning, HealthKit, and access to location, camera, or microphone.
**Platforms:** Text-size, button-size, and default/additional interaction-method specs differ per platform per the tables above; every platform except watchOS supports physical game controllers; touch-based virtual controls are specific to iOS/iPadOS; full-screen behavior differs (hides other apps/system UI on macOS/iOS/iPadOS vs. a fully surrounding Full Space on visionOS).
