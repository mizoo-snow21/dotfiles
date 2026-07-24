# HIG — Inputs
Covers: action-button, apple-pencil-and-scribble, camera-control, digital-crown, eyes, focus-and-selection, game-controls, gestures, gyro-and-accelerometer, keyboards, nearby-interactions, pointing-devices, remotes

## Action button
Source: https://developer.apple.com/design/human-interface-guidelines/action-button
A hardware button on supported iPhone and Apple Watch models that gives quick access to a person-chosen favorite function.
- People choose the Action button's function during device setup and can change it later in Settings; assigning an App Shortcut makes pressing it run that shortcut like Siri or Spotlight would.
- **Support the Action button with a set of your app's essential functions** (e.g., "Start Egg Timer"). No need to offer an App Shortcut that just opens your app — the system already provides that, and your icon/widgets/complications cover it.
- **For each action you support, write a short label** using title-style capitalization, starting with a verb, present tense, no articles/prepositions, max three words (e.g., "Start Race," not "Started Race" or "Start the Race").
- **Prefer letting the system show people how to use the Action button with your app** — avoid duplicating Settings' configuration guidance.
**Platforms:**
- Not supported in iPadOS, macOS, tvOS, or visionOS.
- iOS: **Let people use your actions without leaving their current context** — use Live Activities/custom snippets instead of launching the app (e.g., "Set Timer" prompts for a duration and launches a Live Activity countdown rather than opening Clock).
- watchOS: first press can drop a waypoint, start a dive, or begin a workout; it also supports secondary actions (mark a segment, advance workout modality). Apps don't respond to Action button presses beyond this system-assigned behavior model — **consider a secondary function that supports/advances the primary action** (be cautious offering more than one, to limit cognitive load). **Prefer subsequent presses for additional functionality, not to stop/conclude** a function — offer stopping within your interface instead. **Pause the current function when Action button + side button are pressed together**, except where pausing is dangerous (e.g., a dive).

## Apple Pencil and Scribble
Source: https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble
Apple Pencil is a pixel-precision drawing/marking/pointing tool for iPad, and Scribble lets people enter text anywhere via on-device handwriting recognition.
- **Support behaviors people intuitively expect** from a real marking instrument (e.g., writing in margins).
- **Let people choose when to switch between Apple Pencil and finger input** — controls should respond to both, or they may seem broken (Scribble only supports Apple Pencil input).
- **Let people make a mark the moment Apple Pencil touches the screen** — no special mode or button tap required first.
- **Help people express themselves by responding to tilt (altitude), force (pressure), orientation (azimuth), and Barrel roll** — vary stroke thickness/intensity; keep pressure response simple/intuitive (e.g., affecting ink opacity or brush size).
- **Provide visual feedback indicating direct connection with content** — avoid disconnected actions or effects on other screen areas.
- **Design a great left- and right-handed experience** — avoid controls that either hand may obscure; consider letting people reposition them.

Hover:
- **Use hover to help people predict what will happen** when Apple Pencil touches down (e.g., preview mark dimensions/color); avoid continuously changing the preview with height — distracting.
- **Avoid using hover to initiate an action**, especially a destructive one.
- **Prefer showing a preview value near the middle of a dynamic range** — extremes (max pressure occludes; min pressure is hard to see/invisible) make poor previews.
- **Consider using hover to support relevant interactions close to where people are marking** (e.g., a tool-size menu via Squeeze or a modifier key).
- **Prefer showing hover previews for Apple Pencil, not for a pointing device** — restrict to Pencil if it avoids confusion.

Double tap:
- **Respect people's settings for the double-tap gesture** when they make sense (default: toggle current tool/eraser; can be set to toggle current/previous tool, show/hide color picker, or do nothing). If systemwide settings don't fit, you can still use double tap to change interaction mode (e.g., toggle raise/lower mesh-edit modes).
- **Give people a way to specify custom double-tap behavior if necessary**, with a discoverable control — don't turn it on by default.
- **Avoid using double tap for actions that modify content** — people can double-tap accidentally; prefer easily undoable actions and avoid destructive/data-loss actions.

Squeeze (Apple Pencil Pro):
> Note: Squeeze is available only when the paired iPad screen is on and Apple Pencil Pro is not directly contacting it, so people might not always see the gesture's onscreen result.
- **Treat squeeze as a single, quick, discrete (not continuous) action** — holding or repeated squeezing is tiring.
- **If squeeze reveals app UI (e.g., a contextual menu), display it close to Apple Pencil Pro.**
- **Define squeeze actions that are nondestructive and easy to undo** — people can squeeze unintentionally.

Barrel roll:
- **Use barrel roll only to modify marking behavior**, not for navigation or displaying other controls — unlike double tap/squeeze, it isn't suited to interface actions.

Scribble:
- **Make text entry feel fluid and effortless** — works by default in standard text components (text fields, text views, search fields, editable web content) except password fields; avoid requiring a tap/select first in custom text fields.
- **Make Scribble available everywhere people might want to enter text**, even areas without a visible text field (e.g., writing a new reminder below the last item in Reminders). See `UIIndirectScribbleInteraction`.
- **Avoid distracting people while they write** — e.g., avoid autocompletion text overlapping their writing; hide placeholder text the moment writing begins.
- **While people write in a text field, keep it stationary** — movement/resizing that's fine for keyboard input can feel disorienting during writing; delay changes until they pause.
- **Prevent autoscrolling text while people are writing/editing** — autoscroll can cause writing on top of text or selecting the wrong range.
- **Give people enough space to write** — enlarge a small text field before/when writing pauses; avoid resizing while writing. See `UIScribbleInteraction`.

Custom drawing (PencilKit):
- **Help people draw on top of existing content** — by default PencilKit canvas colors adjust for Dark Mode, but prevent that dynamic adjustment when marking up existing content (PDF, photo) so markup stays sharp/visible.
- **Consider displaying custom undo/redo buttons in a compact environment** (tool picker's built-in undo/redo isn't shown there); also consider supporting the standard 3-finger undo/redo gesture in any environment.
**Platforms:** Not supported in iOS, macOS, tvOS, visionOS, or watchOS.

## Camera Control
Source: https://developer.apple.com/design/human-interface-guidelines/camera-control
A hardware control on iPhone 16/16 Pro models providing direct, adjustable access to an app's camera experience via an overlay from the device bezel.
- A light press opens an overlay; a light double-press cycles/views available controls; sliding a finger on the Camera Control adjusts the selected control's value.
- Anatomy: a **slider** offers a continuous range (e.g., contrast); a **picker** offers discrete options (e.g., grid on/off). The system also provides standard zoom/exposure controls you can optionally include.
- **Use SF Symbols to represent control functionality** — no custom symbols supported; symbols don't represent current state.
- **Keep names of controls short** — labels follow Dynamic Type and can obscure the viewfinder if long.
- **Include units or symbols with slider values** for context (e.g., EV, %). See `localizedValueFormat`.
- **Define prominent values for a slider control** — frequently chosen or evenly spaced values (e.g., major zoom increments) that the system helps people land on. See `prominentValues`.
- **Make space for the overlay in the viewfinder** — overlay and labels occupy screen area adjacent to the Camera Control in both orientations; keep your UI outside the overlay area and maximize viewfinder height/width.
- **Minimize distractions in the viewfinder** — avoid duplicating sliders/toggles in both your UI and the overlay.
- **Enable or disable controls depending on the camera mode** (e.g., disable video controls when taking photos) — controls can't be added/removed at runtime.
- **Consider how to arrange your controls** — order commonly used controls toward the middle; the system remembers the last control used in your app when the overlay reopens.
- **Allow people to use the Camera Control to launch your experience from anywhere** via a locked camera capture extension (locked device, Home Screen, or from within other apps).
**Platforms:** Not supported in iPadOS, macOS, watchOS, tvOS, or visionOS.

## Digital Crown
Source: https://developer.apple.com/design/human-interface-guidelines/digital-crown
A rotatable hardware input on Apple Vision Pro and Apple Watch used for system interaction and, on Apple Watch, app interaction.
- Apple Vision Pro: used to adjust volume, adjust immersion level (portal/Environment/app/game in a Full Space), recenter content in front of the person, open Accessibility settings, and exit an app to the Home View.
- Apple Watch: since watchOS 10, turning the Digital Crown is the primary navigation input — viewing widgets in the Smart Stack, moving vertically through Home Screen apps, switching between vertically paginated tabs, and scrolling list views/variable-height pages. Beyond navigation, turns can drive data inspection or custom/standard control operation.
> Note: Apps don't respond to presses on the Digital Crown — watchOS reserves presses for system functionality like revealing the Home Screen.
- Most Apple Watch models provide haptic feedback (linear *detents*/taps) as the Crown turns a specific distance; some system controls (e.g., table views) provide detents as new items scroll on.
- **Anchor your app's navigation to the Digital Crown** — list/tab/scroll views should be vertically oriented; back Crown interactions with corresponding touch-screen interactions.
- **Consider using the Digital Crown to inspect data** where navigation isn't needed (e.g., World Clock advances time of day at a selected location as the Crown turns).
- **Provide visual feedback in response to Digital Crown interactions** (e.g., pickers update the displayed value) — without it, people assume turning has no effect.
- **Update your interface to match the speed with which people turn the Digital Crown** — precise control is expected; avoid update rates that make selecting values hard.
- **Use the default haptic feedback when it makes sense** — turn off detents if they don't match your app's animation; tables can use linear detents instead of row-based ones (e.g., for rows of significantly different heights).
**Platforms:** Not supported in iOS, iPadOS, macOS, or tvOS.

## Eyes
Source: https://developer.apple.com/design/human-interface-guidelines/eyes
In visionOS, people look at a virtual object to target it for interaction, and the system highlights it with a *hover effect*.
- Looking at an interactive element triggers the hover effect (visual feedback that a tap-like gesture will work); some components auto-expand on look (e.g., a tab bar reveals text labels; a button can reveal a tooltip).
> Important: visionOS doesn't provide direct information about where people are looking before they tap, to preserve privacy; system components tell you only when people tap.
- *Focus effects* (for connected keyboard/game controller navigation) are unrelated to the eyes hover effect — see Focus and selection.
- **Always give people multiple ways to interact with your app** — support accessibility personalization.
- **Design for visual comfort** — keep needed objects within Field of view; the system places the first window/volume conveniently in Shared Space/Full Space; avoid requiring multiple quick eye adjustments across large areas or depth levels.
- **Place content at a comfortable viewing distance** — aim for at least one meter away for content viewed/engaged over time.
- **Prefer using standard UI components** — custom components with different visual cues are harder to learn/remember.

Making items easy to see:
- **Minimize visual distractions** — visual noise and especially movement (peripheral vision) can involuntarily pull gaze away from the target.
- **Provide enough space around each item** — use a margin of at least 16 points around an item's bounds, or place items so centers are at least 60 points apart, to prevent unwanted jumping between crowded items.
- **Avoid a repeating pattern/texture that fills the field of view** — eyes can lock onto different elements, creating false depth; use the pattern in a smaller area instead.

Encouraging interaction:
- **Consider subtle visual cues** to draw attention to the most likely-wanted item (central placement, gentle motion, contrast, color/scale variation) — noticeable but not flashy/harsh.
- **In general, give an interactive item a rounded shape** — eyes are drawn to corners, so rounder shapes are easier to keep looking at.
- **Provide an overall containing shape for multi-element interactive components** so visionOS can highlight the whole region when either element is looked at.

Custom hover effects:
- Built from two states/appearances (with/without effect); the system applies the effect out-of-process, so you don't know when it's applied or the element's exact state at that moment — a custom hover effect can't itself perform an action or code that depends on knowing when someone is looking.
- **Prefer using a custom hover effect to emphasize a special moment** — overuse or use where standard effects suffice dilutes design impact and can cause visual discomfort.
- **Choose the right delay**: no delay (default) for subtle/inviting effects (e.g., a slider knob); short delay to let people look and quickly interact (e.g., tab bar expansion); long delay for additional information (e.g., a tooltip), since most people won't need it every time.
- **Aim to keep one or more primary views unchanged across both states** — total change in all views can disorient.
- **Thoroughly test custom hover effects**, ideally while wearing Apple Vision Pro.
**Platforms:** Not supported in iOS, iPadOS, macOS, tvOS, or watchOS.

## Focus and selection
Source: https://developer.apple.com/design/human-interface-guidelines/focus-and-selection
Focus helps people visually confirm the object their interaction with a remote, game controller, or keyboard currently targets.
- Focusing an item often also selects it, except where automatic selection would cause a distracting context shift (e.g., tvOS requires a separate gesture to select/activate a focused item, since selection opens/activates it).
- Focus is communicated differently per platform: iPadOS/macOS draw a ring or highlight; tvOS generally uses the Parallax effect for depth/liveliness. The combined effects+interactions are called a *focus system*/*focus model*.
- **Rely on system-provided focus effects** — precisely tuned and consistent; create custom focus effects only if absolutely necessary.
- **Avoid changing focus without people's interaction** — they rely on the focus system to know their place. Exception: when people move focus via discrete directional input (keyboard/remote/game controller) and the previously focused item disappears — move focus to a nearby remaining item within one discrete step. Otherwise (no such input device), hide the focus indicator when the focused object disappears rather than guessing the next target.
- **Be consistent with the platform** for how focus is reached: iPadOS/macOS Full Keyboard Access reaches every control, so you need only support focus for content elements (list items, text/search fields), not controls (buttons, sliders, toggles); tvOS requires every onscreen element to be reachable via directional gestures/arrow keys.
- **Indicate focus using platform-consistent visual appearances** (e.g., iPadOS/macOS: white text + accent-color background highlight for focused list items vs. standard text + gray highlight for unfocused; see `UICollectionView`/`NSTableView`).
- **In general, use a focus ring for a text or search field, but use a highlight in a list or collection** — an entire highlighted row is easier to scan than a ring around a cell.
**Platforms:**
- Not supported in iOS or watchOS.
- iPadOS: iPadOS 15+ defines a focus system for text fields/views/sidebars/collection views/custom views. Similar underlying system to tvOS but different UX — tvOS uses *directional focus* (same interaction reaches every component); iPadOS defines *focus groups* (specific app areas like sidebar/grid/list) supporting two keyboard interactions: Tab moves among focus groups; arrow keys move directionally within the same focus group. Components indicate focus via the *halo* effect (customizable outline, aka focus ring — apply to custom views/opaque cell content) or the *highlighted* appearance (accent-colored text, occurs automatically on selecting a configured collection view cell — not itself a focus effect). **Customize the halo focus effect when necessary** (shape/position, e.g., rounded corners, Bézier paths, badge occlusion) — see `UIFocusHaloEffect`. **Ensure focus moves through custom views sensibly** — default order is reading order (leading-to-trailing, top-to-bottom) through focus groups; group a vertical stack via `focusGroupIdentifier` if needed. **Adjust an item's priority to reflect importance within a focus group** — a group's *primary item* auto-receives focus when the group is focused; increase priority via `UIFocusGroupPriority`.
- tvOS: **In a full-screen experience, let gestures interact with content, not move focus** — full-screen items don't show focus. **Avoid displaying a pointer** — use the focus model for menus/interface navigation (free-form movement may suit gameplay only); if a pointer is required, make it highly visible/integrated. **Design your interface to accommodate up to five distinct focus states** (unfocused, focused, selected/chosen with instant feedback, selected/deselected persistent state, unavailable) — supply larger assets for the focused scale and avoid crowding.
- visionOS: supports the same focus system as iPadOS/tvOS for connected keyboard/game controller input.
> Note: the visionOS *hover effect* (from looking at an object) is unrelated to the focus system — see Eyes.

## Game controls
Source: https://developer.apple.com/design/human-interface-guidelines/game-controls
Precise, intuitive controls — physical controllers or a platform's default interaction (touch, remote, mouse/keyboard) — enhance gameplay and immersion.
- Support a platform's default interaction method too: not every player has a physical game controller, and players appreciate using what they're familiar with (every iPhone/iPad has touch, every Mac has keyboard+trackpad/mouse, every Apple TV has a remote, every Apple Vision Pro responds to eye/hand gestures).

Touch controls (iOS/iPadOS, via the Touch Controller framework):
- **Determine whether virtual controls on top of game content make sense** — they benefit games with many actions or movement control; look for chances to use in-game gestures (e.g., tap to select) instead of overlapping virtual buttons.
- **Place virtual buttons where they're easy to access** — respect device boundaries, Guides and safe areas, and comfortable hand positions; avoid overlapping the Home indicator/Dynamic Island; place frequently used buttons near a thumb, avoiding circular movement/camera regions; place secondary controls (menus) at the top.
- **Make sure controls are large enough** — frequently used controls at least 44x44 pt; less important controls (e.g., menus) at least 28x28 pt.
- **Always include visible and tactile press states** — a visual press effect (e.g., glow) visible even under a covering finger, combined with sound/haptics.
- **Use symbols that communicate the actions they perform** (e.g., a weapon graphic for attack) — avoid abstract shapes or controller-based naming (A, X, R1) as artwork.
- **Show and hide virtual controls to reflect gameplay** — hide controls when an action isn't relevant to reduce clutter (e.g., hide movement controls until the player touches the screen).
- **Combine functionality into a single control** — redesign mechanics needing simultaneous/sequential multi-button presses; use gestures like double tap and touch-and-hold for action variants (e.g., touch-and-hold for a powered-up attack); combine related actions (walking/sprinting) into one control.
- **Map movement and camera controls to predictable behavior** — movement on the left side of the screen, camera direction on the right; maximize the controllable area; for movement, show a virtual thumbstick wherever the thumb lands rather than a static position; for camera, prefer direct touch panning over a virtual thumbstick.

Physical controllers:
- **Support the platform's default interaction method** as a fallback, since a game controller is an optional purchase. See `Adding virtual controls to games that support game controllers in iOS`.
- **Tell people about game controller requirements** — tvOS/visionOS can require a physical controller (App Store shows a "Game Controller Required" badge); check for presence and gracefully prompt to connect one, since people can open the game without a connected controller. See `GCRequiresControllerUserInteraction`.
- **Automatically detect whether a controller is paired** and get its profile (Game Controller framework) rather than requiring manual setup.
- **Customize onscreen content to match the connected game controller's actual labeling scheme** — the framework assigns standard element names, but real colors/symbols vary by controller. See `GCControllerElement`.
- **Map controller buttons to expected UI behavior** outside of gameplay, per this table:

| Button | Expected behavior for UI |
| --- | --- |
| A | Activates a control |
| B | Cancels an action or returns to previous screen |
| X | — |
| Y | — |
| Left shoulder | Navigates left to a different screen or section |
| Right shoulder | Navigates right to a different screen or section |
| Left trigger | — |
| Right trigger | — |
| Left/right thumbstick | Moves selection |
| Directional pad | Moves selection |
| Home/logo | Reserved for system controls |
| Menu | Opens game settings or pauses gameplay |

- **Support multiple connected controllers** — use labels/glyphs matching the actively used controller; in multiplayer, use the correct labels per player's controller; list buttons together if referring to multiple controllers.
- **Prefer using symbols, not text, to refer to game controller elements** — the Game Controller framework provides SF Symbols for most elements across controller brands, helping players unfamiliar with controllers.

Keyboards (in games):
- **Prioritize single-key commands** — faster, especially while using a mouse/trackpad simultaneously (e.g., first-letter shortcuts like I for Inventory, M for Map; main action mapped to Space bar).
- **Test key binding comfort using an Apple keyboard** — e.g., remap a non-Apple keyboard's Control-based binding to Command (⌘), which sits conveniently next to Space bar near WASD.
- **Take the proximity of keys into account** — map high-value commands to keys near WASD; map closely related actions to physically close keys (e.g., number keys for inventory categories).
- **Let players customize key bindings** for personal comfort/play style, beyond reasonable defaults.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS. visionOS: **Match spatial game controller behavior to hand input** — support spatial controllers (e.g., PlayStation VR2 Sense) similarly to hands: look at an object + press left/right trigger to interact indirectly, or reach out + press trigger to interact directly.

## Gestures
Source: https://developer.apple.com/design/human-interface-guidelines/gestures
A gesture is a physical motion — on a touchscreen, in the air, or via a trackpad/mouse/remote/game controller touch surface — used to directly affect an onscreen object.
- Every platform supports basic gestures (tap, swipe, drag); precise movements vary by platform/device but the underlying functionality is familiar everywhere.
- **Give people more than one way to interact with your app** — voice, keyboard, Switch Control, etc.; don't assume a specific gesture is available.
- **In general, respond to gestures consistently with expectations** — e.g., tap activates/selects; avoid repurposing a familiar gesture for an app-unique action, and avoid a unique gesture for a standard action.
- **Handle gestures as responsively as possible** — provide feedback predicting results and, if needed, the extent/type of movement required.
- **Indicate when a gesture isn't available** — otherwise people think the app froze or they're doing it wrong (e.g., show a locked object's state, or a clearly distinct unavailable button state).

Custom gestures:
- **Add custom gestures only when necessary** — best for frequent, specialized tasks not covered by existing gestures (games, drawing apps); must be discoverable, straightforward, distinct from other gestures, and never the *only* way to perform an important action.
- **Make custom gestures easy to learn** — provide learning moments, test in real scenarios; difficulty describing a gesture in simple language/graphics signals it'll be hard to learn.
- **Use shortcut gestures to supplement standard gestures, not replace them** — e.g., keep a Back button available even if a swipe shortcut also exists.
- **Avoid conflicting with gestures that access system UI** (e.g., edge swiping in watchOS, hand-roll-over in visionOS) — in specific circumstances (games/immersive experiences) developers can defer the system gesture.

Standard gestures (all platforms):

| Gesture | Supported in | Common action |
| --- | --- | --- |
| Tap | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Activate a control; select an item. |
| Swipe | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Reveal actions and controls; dismiss views; scroll. |
| Drag | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Move a UI element. |
| Touch (or pinch) and hold | iOS, iPadOS, tvOS, visionOS, watchOS | Reveal additional controls or functionality. |
| Double tap | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Zoom in; zoom out if already zoomed in; perform a primary action on Apple Watch Series 9 and Apple Watch Ultra 2. |
| Zoom | iOS, iPadOS, macOS, tvOS, visionOS | Zoom a view; magnify content. |
| Rotate | iOS, iPadOS, macOS, tvOS, visionOS | Rotate a selected item. |

**Platforms:**
- iOS, iPadOS — additional gestures:

| Gesture | Common action |
| --- | --- |
| Three-finger swipe | Initiate undo (left swipe); initiate redo (right swipe). |
| Three-finger pinch | Copy selected text (pinch in); paste copied text (pinch out). |
| Four-finger swipe (iPadOS only) | Switch between apps. |
| Shake | Initiate undo; initiate redo. |

  **Consider allowing simultaneous recognition of multiple gestures if it enhances the experience** — unlikely useful in nongame apps, but a game might need simultaneous joystick + fire-button controls.
- macOS: primary interaction is keyboard + mouse; also supports standard gestures via Magic Trackpad/Magic Mouse or a touch-surface game controller.
- tvOS: uses standard gestures via a compatible remote (Siri Remote) or a touch-surface game controller — see Remotes.
- visionOS: supports *indirect* gestures (look at an object to target it, then manipulate from a distance with hands, e.g., look + pinch tap-and-thumb to select) and *direct* gestures (physically touch the object, e.g., typing on the visionOS keyboard) — direct gestures work best within reach and are best for infrequent use since raised arms tire people; visionOS also supports direct versions of all standard gestures.

  Standard direct gestures in visionOS:

  | Direct gesture | Common use |
  | --- | --- |
  | Touch | Directly select or activate an object. |
  | Touch and hold | Open a contextual menu. |
  | Touch and drag | Move an object to a new location. |
  | Double touch | Preview an object or file; select a word in an editing context. |
  | Swipe | Reveal actions and controls; dismiss views; scroll. |
  | With two hands, pinch and drag together or apart | Zoom in or out. |
  | With two hands, pinch and drag in a circular motion | Rotate an object. |

  **Support standard gestures everywhere you can** — tap is the first gesture people try after looking at an object.
  **Offer both indirect and direct interactions when possible** — prefer indirect for UI/common components; reserve direct/custom gestures for close-up or specific-motion interactions.
  **Avoid requiring specific body movements or positions for input** — offer alternative inputs for accessibility/environmental reasons.
  Custom gestures in visionOS require running in a Full Space and requesting hand-tracking permission (see `Setting up access to ARKit data`). **Prioritize comfort** — test ergonomics continually; raised-arm and repetitive-motion interactions stress muscles/joints. **Carefully consider complex multi-finger/two-hand custom gestures** — offer a lower-movement alternative. **Avoid custom gestures that require using a specific hand** — increases cognitive load and excludes hand-dominant/limb-different people.
  System overlays (visionOS 2+): looking at the palm of one hand + a gesture opens Home/Control Center overlays systemwide (visionOS 1's look-upward gesture remains as an accessibility setting for Control Center). **Reserve the area around a person's hand for system overlays** — avoid anchoring content to hands/wrists, or place hand-anchored game content outside the immediate hand area to avoid colliding with the Home indicator. **Consider deferring the system overlay behavior** for immersive apps/games via `persistentSystemOverlays(_:)` (visionOS 1-built apps defer by default, requiring a tap first). **Use caution designing custom gestures involving a hand/wrist/forearm rolling motion** — reserved for revealing system overlays, which display on top of app content without the app's awareness.
- watchOS: **Double tap** (watchOS 11+) scrolls lists/scroll views and advances vertical tab views; a toggle/button can be specified as a view's primary action (also honored in widgets/Live Activities shown in the Smart Stack) — double-tapping highlights then performs it; also supported for custom Notification actions (acts on the first nondestructive action). **Avoid setting a primary action in views with lists, scroll views, or vertical tabs** — conflicts with default double-tap navigation. **Choose the most commonly used button as the primary action** in nonscrolling views (e.g., play/pause in a media controls view). See `handGestureShortcut(_:isEnabled:)` and `primaryAction`.

## Gyroscope and accelerometer
Source: https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer
On-device gyroscopes and accelerometers supply real-world device-movement data for motion-based experiences.
- Available for apps/games in iOS, iPadOS, and watchOS; tvOS apps can use gyroscope data from the Siri Remote. See `Core Motion`.
- **Use motion data only to offer a tangible benefit** (e.g., fitness feedback, enhanced gameplay) — avoid gathering data simply to have it.
> Important: accessing motion data requires copy explaining why, shown in the system's permission request the first time your app/game tries to access it.
- **Outside of active gameplay, avoid using accelerometers/gyroscopes for direct interface manipulation** — motion-based gestures can be hard to replicate precisely, physically challenging for some people, and affect battery usage.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Keyboards
Source: https://developer.apple.com/design/human-interface-guidelines/keyboards
A physical keyboard is an essential input device for text entry, gaming, and app control on every device except Apple Watch.
- A *keyboard shortcut* combines a primary key with one or more modifier keys (Control, Option, Shift, Command) mapped to a command; a game's shortcut (*key binding*) is often a single key. Apple defines standard shortcuts for cross-app/system consistency.
- **Support Full Keyboard Access when possible** (iOS, iPadOS, macOS, visionOS) — lets people navigate/activate windows, menus, controls, and system features via keyboard only; test it via Accessibility settings. See `Support Full Keyboard Access in your iOS app`, `isFullKeyboardAccessEnabled`.
> Important: iPadOS supports keyboard navigation in text fields/views/sidebars (and via API in collection/custom views), but avoid supporting keyboard navigation for controls (buttons, segmented controls, switches) — let Full Keyboard Access handle activating controls, reaching all components, and gesture-based interactions like drag and drop. See `Focus-based navigation`.
- **Respect standard keyboard shortcuts** — prefer a new custom shortcut over repurposing a standard one people associate with a different action; in games people expect some standards (e.g., Command-Q to quit) but also expect to customize key bindings.

Standard keyboard shortcuts:
- **In general, don't repurpose standard keyboard shortcuts for custom actions** — only redefine one if its standard action doesn't make sense in your experience (e.g., an app without text editing could repurpose Command-I, normally Italic, for Get Info).

| Primary key | Keyboard shortcut | Action |
| --- | --- | --- |
| Space | Command-Space | Show or hide the Spotlight search field. |
|  | Shift-Command-Space | Varies. |
|  | Option-Command-Space | Show the Spotlight search results window. |
|  | Control-Command-Space | Show the Special Characters window. |
| Tab | Shift-Tab | Navigate through controls in a reverse direction. |
|  | Command-Tab | Move forward to the next most recently used app in a list of open apps. |
|  | Shift-Command-Tab | Move backward through a list of open apps (sorted by recent use). |
|  | Control-Tab | Move focus to the next group of controls in a dialog or the next table (when Tab moves to the next cell). |
|  | Control-Shift-Tab | Move focus to the previous group of controls. |
| Esc | Esc | Cancel the current action or process. |
| Esc | Option-Command-Esc | Open the Force Quit dialog. |
| Eject | Control-Command-Eject | Quit all apps (after changes have been saved) and restart the computer. |
|  | Control-Option-Command-Eject | Quit all apps (after changes have been saved) and shut the computer down. |
| F1 | Control-F1 | Toggle full keyboard access on or off. |
| F2 | Control-F2 | Move focus to the menu bar. |
| F3 | Control-F3 | Move focus to the Dock. |
| F4 | Control-F4 | Move focus to the active (or next) window. |
|  | Control-Shift-F4 | Move focus to the previously active window. |
| F5 | Control-F5 | Move focus to the toolbar. |
|  | Command-F5 | Turn VoiceOver on or off. |
| F6 | Control-F6 | Move focus to the first (or next) panel. |
|  | Control-Shift-F6 | Move focus to the previous panel. |
| F7 | Control-F7 | Temporarily override the current keyboard access mode in windows and dialogs. |
| F8 |  | Varies. |
| F9 |  | Varies. |
| F10 |  | Varies. |
| F11 |  | Show desktop. |
| F12 |  | Hide or display Dashboard. |
| Grave accent (`) | Command-Grave accent | Activate the next open window in the frontmost app. |
|  | Shift-Command-Grave accent | Activate the previous open window in the frontmost app. |
|  | Option-Command-Grave accent | Move focus to the window drawer. |
| Hyphen (-) | Command-Hyphen | Decrease the size of the selection. |
|  | Option-Command-Hyphen | Zoom out when screen zooming is on. |
| Left bracket ({) | Command-Left bracket | Left-align a selection. |
| Right bracket (}) | Command-Right bracket | Right-align a selection. |
| Pipe (\|) | Command-Pipe | Center-align a selection. |
| Colon (:) | Command-Colon | Display the Spelling window. |
| Semicolon (;) | Command-Semicolon | Find misspelled words in the document. |
| Comma (,) | Command-Comma | Open the app's settings window. |
|  | Control-Option-Command-Comma | Decrease screen contrast. |
| Period (.) | Command-Period | Cancel an operation. |
|  | Control-Option-Command-Period | Increase screen contrast. |
| Question mark (?) | Command-Question mark | Open the app's Help menu. |
| Forward slash (/) | Option-Command-Forward slash | Turn font smoothing on or off. |
| Equal sign (=) | Shift-Command-Equal sign | Increase the size of the selection. |
|  | Option-Command-Equal sign | Zoom in when screen zooming is on. |
| 3 | Shift-Command-3 | Capture the screen to a file. |
|  | Control-Shift-Command-3 | Capture the screen to the Clipboard. |
| 4 | Shift-Command-4 | Capture a selection to a file. |
|  | Control-Shift-Command-4 | Capture a selection to the Clipboard. |
| 8 | Option-Command-8 | Turn screen zooming on or off. |
|  | Control-Option-Command-8 | Invert the screen colors. |
| A | Command-A | Select every item in a document or window, or all characters in a text field. |
|  | Shift-Command-A | Deselect all selections or characters. |
| B | Command-B | Boldface the selected text or toggle boldfaced text on and off. |
| C | Command-C | Copy the selection to the Clipboard. |
|  | Shift-Command-C | Display the Colors window. |
|  | Option-Command-C | Copy the style of the selected text. |
|  | Control-Command-C | Copy the formatting settings of the selection and store on the Clipboard. |
| D | Option-Command-D | Show or hide the Dock. |
|  | Control-Command-D | Display the definition of the selected word in the Dictionary app. |
| E | Command-E | Use the selection for a find operation. |
| F | Command-F | Open a Find window. |
|  | Option-Command-F | Jump to the search field control. |
|  | Control-Command-F | Enter full screen. |
| G | Command-G | Find the next occurrence of the selection. |
|  | Shift-Command-G | Find the previous occurrence of the selection. |
| H | Command-H | Hide the windows of the currently running app. |
|  | Option-Command-H | Hide the windows of all other running apps. |
| I | Command-I | Italicize the selected text or toggle italic text on or off; also, display an Info window. |
|  | Option-Command-I | Display an inspector window. |
| J | Command-J | Scroll to a selection. |
| M | Command-M | Minimize the active window to the Dock. |
|  | Option-Command-M | Minimize all windows of the active app to the Dock. |
| N | Command-N | Open a new document. |
| O | Command-O | Display a dialog for choosing a document to open. |
| P | Command-P | Display the Print dialog. |
|  | Shift-Command-P | Display the Page Setup dialog. |
| Q | Command-Q | Quit the app. |
|  | Shift-Command-Q | Log out the person currently logged in. |
|  | Option-Shift-Command-Q | Log out the person currently logged in without confirmation. |
| S | Command-S | Save a new document or save a version of a document. |
|  | Shift-Command-S | Duplicate the active document or initiate a Save As. |
| T | Command-T | Display the Fonts window. |
|  | Option-Command-T | Show or hide a toolbar. |
| U | Command-U | Underline the selected text or turn underlining on or off. |
| V | Command-V | Paste the Clipboard contents at the insertion point. |
|  | Shift-Command-V | Paste as (Paste as Quotation, for example). |
|  | Option-Command-V | Apply the style of one object to the selection. |
|  | Option-Shift-Command-V | Paste the Clipboard contents and apply the style of the surrounding text to the inserted object. |
|  | Control-Command-V | Apply formatting settings to the selection. |
| W | Command-W | Close the active window. |
|  | Shift-Command-W | Close a file and its associated windows. |
|  | Option-Command-W | Close all windows in the app. |
| X | Command-X | Remove the selection and store on the Clipboard. |
| Z | Command-Z | Undo the previous operation. |
|  | Shift-Command-Z | Redo (when Undo and Redo are separate commands rather than toggled using Command-Z). |
| Right arrow | Command-Right arrow | Change the keyboard layout to current layout of Roman script. |
|  | Shift-Command-Right arrow | Extend selection to the next semantic unit, typically the end of the current line. |
|  | Shift-Right arrow | Extend selection one character to the right. |
|  | Option-Shift-Right arrow | Extend selection to the end of the current word, then to the end of the next word. |
|  | Control-Right arrow | Move focus to another value or cell within a view, such as a table. |
| Left arrow | Command-Left arrow | Change the keyboard layout to current layout of system script. |
|  | Shift-Command-Left arrow | Extend selection to the previous semantic unit, typically the beginning of the current line. |
|  | Shift-Left arrow | Extend selection one character to the left. |
|  | Option-Shift-Left arrow | Extend selection to the beginning of the current word, then to the beginning of the previous word. |
|  | Control-Left arrow | Move focus to another value or cell within a view, such as a table. |
| Up arrow | Shift-Command-Up arrow | Extend selection upward in the next semantic unit, typically the beginning of the document. |
|  | Shift-Up arrow | Extend selection to the line above, to the nearest character boundary at the same horizontal location. |
|  | Option-Shift-Up arrow | Extend selection to the beginning of the current paragraph, then to the beginning of the next paragraph. |
|  | Control-Up arrow | Move focus to another value or cell within a view, such as a table. |
| Down arrow | Shift-Command-Down arrow | Extend selection downward in the next semantic unit, typically the end of the document. |
|  | Shift-Down arrow | Extend selection to the line below, to the nearest character boundary at the same horizontal location. |
|  | Option-Shift-Down arrow | Extend selection to the end of the current paragraph, then to the end of the next paragraph (include the paragraph terminator, such as Return, in cut/copy/paste). |
|  | Control-Down arrow | Move focus to another value or cell within a view, such as a table. |

- Input-source/localization shortcuts (don't map to menu commands): Control-Space toggles current/last input source; Control-Option-Space switches to the next input source; [Modifier key]-Command-Space varies; Command-Right arrow / Command-Left arrow change keyboard layout to Roman/system script respectively.

Custom keyboard shortcuts:
- **Define custom keyboard shortcuts only for the most frequently used app-specific commands** — too many new shortcuts makes an app seem hard to learn.
- **Use modifier keys in ways people expect** — e.g., Command while dragging moves items as a group; Shift while drag-resizing constrains to aspect ratio; holding an arrow key moves selection by the smallest app-defined unit until released.

| Modifier key | Recommended usage |
| --- | --- |
| Command | Prefer as the main modifier key in a custom keyboard shortcut. |
| Shift | Prefer as a secondary modifier that complements a related shortcut. |
| Option | Use sparingly, for less-common commands or power features. |
| Control | Avoid using as a modifier — the system uses Control extensively for systemwide features/shortcuts (e.g., moving focus, capturing screenshots). |

> Tip: Some languages require modifier keys to generate certain characters (e.g., French keyboard Option-5 generates "{"). Command as a modifier is usually safe; avoid pairing an additional modifier with characters not on all keyboards, and if you must use a non-Command modifier, prefer it only with alphabetic characters.
- **List modifier keys in the correct order**: Control, Option, Shift, Command.
- **Avoid adding Shift to a shortcut using the upper character of a two-character key** — e.g., Command-Slash for Hide Status Bar, but Command-Question mark (not Shift-Command-Slash) for Help.
- **Let the system localize and mirror your keyboard shortcuts as needed** — auto-localizes for the connected keyboard, auto-mirrors for right-to-left layouts.
- **Avoid creating a new shortcut by adding a modifier to an existing shortcut for an unrelated command** — e.g., avoid Shift-Command-Z for something unrelated to undo/redo.
**Platforms:**
- No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS.
- visionOS: keyboard shortcuts appear in a shortcut interface shown when holding Command on a connected keyboard, organized like the menu bar (File, Edit, View, etc.) but shown as a flat, all-categories-at-once view listing only available commands with shortcuts. **Write descriptive shortcut titles** — no submenu titles provide context in the flat list. See `discoverabilityTitle`. Connecting a physical keyboard shows a virtual keyboard overlay with typing completion and other controls.

## Nearby interactions
Source: https://developer.apple.com/design/human-interface-guidelines/nearby-interactions
Nearby interactions build on-device experiences around the physical presence of nearby people and objects (e.g., bringing an iPhone near a HomePod mini to transfer audio).
- Available on Ultra Wideband devices via the Nearby Interaction framework; requires people's permission and relies on randomly generated, session-scoped device identifiers to preserve privacy.
- **Consider a task from the perspective of the physical world** to find inspiration — grounding a task in a physical action (e.g., bringing devices close to transfer audio) makes it feel natural.
- **Use distance, direction, and context to inform an interaction** — prioritize nearby, contextually relevant info (e.g., share sheet suggesting the closest facing contact via U1-equipped nearby devices).
- **Consider how changes in physical distance can guide a nearby interaction** — mirror real-world sharpening perception as objects get closer (e.g., AirTag search transitions from a directional arrow to a pulsing circle).
- **Provide continuous feedback** reflecting the physical world's dynamism (e.g., Find My's continuous direction/proximity updates).
- **Consider using multiple feedback types** (visual, audible, haptic) for a holistic experience, varying by task/context (visual while looking at the screen; audible/haptic while interacting with the environment).
- **Avoid using a nearby interaction as the only way to perform a task** — provide alternative ways to accomplish it.

Device usage:
- **Encourage people to hold the device in portrait orientation** — landscape decreases accuracy/availability of distance and direction info; prefer implicit visual feedback over explicitly telling people to hold it in portrait.
- **Design for the device's directional field of view** — relies on a sensor similar to the Ultra Wide camera's field of view (iPhone 11+); a device outside this field of view may still yield distance but not relative direction.
- **Help people understand how intervening objects can affect the experience** — people, animals, or large objects between two devices can decrease accuracy/availability; consider covering this in onboarding/tutorial content.
**Platforms:** No additional considerations for iPadOS. Not supported in macOS, tvOS, or visionOS. iOS: Nearby Interaction APIs provide a peer device's distance and direction. watchOS: APIs provide distance only, and all participating apps must be in the foreground.

## Pointing devices
Source: https://developer.apple.com/design/human-interface-guidelines/pointing-devices
A trackpad or mouse lets people navigate the interface and initiate actions with precision and flexibility.
- On Mac, a pointing device is typically combined with a keyboard; on iPad and Apple Vision Pro, it's an additional interaction method alongside touch, eyes, or gestures — not a replacement.
- **Be consistent when responding to mouse and trackpad gestures** — people expect systemwide gestures (e.g., "Swipe between pages") to behave the same everywhere.
- **Avoid redefining systemwide trackpad gestures** — even app-specific games should leave systemwide gestures (e.g., reveal Dock/Mission Control) available; note people can customize these themselves.
- **Provide a consistent experience whether people use gestures, eyes, a pointing device, or a keyboard** — people expect fluid movement between input types without relearning interactions.
- **Let people use the pointer to reveal/hide auto-minimizing or fading controls** (e.g., hover to reveal a minimized Safari toolbar; move the pointer to reveal/hide full-screen video playback controls).
- **Provide a consistent experience for press-and-hold modifier-key interactions** regardless of touch vs. pointer (e.g., Option-drag-to-duplicate should behave the same either way).
**Platforms:**
- No additional considerations for iOS. Not supported in tvOS or watchOS.
- iPadOS: the pointing system adapts to context and provides rich visual feedback, without replacing touch. **Allow multiple selection in custom views when necessary** — iPadOS 15+ supports click-and-drag band selection by default in standard nonlist collection views; implement it yourself for custom views (see `UIBandSelectionInteraction`). **Distinguish between pointer and finger input only if it provides value** (e.g., a scrubber lets both touch-drag the playhead and pointer-click a precise seek destination).

  Pointer shape and content effects: default pointer shape is a circle, adapting to a system-defined or custom shape over specific elements/regions (e.g., I-beam over text). A *content effect* changes the underlying element's appearance when hovered; iPadOS defines three: **highlight** (translucent rounded-rectangle background with gentle parallax; default on bar buttons, tab bars, segmented controls, edit menus), **lift** (parallax + elevation illusion via scale-up, shadow, specular highlight; default on app icons and Control Center buttons), and **hover** (generic — custom scale/tint/shadow, doesn't transform the default pointer shape).

  Pointer accessories: small secondary visual indicators combinable with any pointer (e.g., resize arrows). **Use clear, simple images for custom accessories** — small size demands minimal detail. **Consider using the accessory transition to signal a state/behavior change** (e.g., `plus` transitioning to `circle.slash` to show an add action became unavailable). See `UIPointerAccessory`.

  Pointer magnetism: elements appear to attract the pointer as it nears their hit region (typically larger than visible bounds) or when flicked toward them (trajectory-based target detection pulls toward the element's center). Applied by default to lift-effect (app icons) and highlight-effect (bar buttons) elements and to text-entry areas (helps avoid skipping lines while selecting text) — not applied to hover elements, since that could feel like losing pointer control.

  Standard pointers and effects: **When possible, support the system-provided content effects** — use highlight for a small element with a transparent background, lift for a small element with an opaque background, and hover for large elements (customizing scale/tint/shadow). **Prefer the system-provided pointer appearances for standard buttons and text-entry areas.** **Add padding around interactive elements for comfortable hit regions** — about 12 pt around elements with a bezel; about 24 pt around elements without a bezel. **Create contiguous hit regions for custom bar buttons** — gaps cause a distracting pointer-shape revert between buttons. **Specify the corner radius of a nonstandard element receiving the lift effect** if it isn't the system-defined rounded rectangle (e.g., a circle) — see `UIPointerShape.roundedRect(_:radius:)`.

  Customizing pointers: **Prefer system-provided pointer effects for custom elements that behave like standard elements** — otherwise people may think they're broken. **Use pointer effects consistently throughout your app.** **Avoid creating gratuitous pointer/content effects** — purely decorative effects distract/irritate without practical value. **Keep custom pointer shapes simple** — the shape should signal the available action without demanding interpretation. **Consider enhancing the pointer with custom annotations** providing useful information (e.g., X/Y values over a graphing area; Keynote shows width/height while resizing). **Avoid displaying instructional text with a pointer** — prioritize interface clarity instead. **Consider the interplay of shadow, scale, and element spacing for custom hover effects** — reserve scaling for elements that can grow without crowding neighbors (e.g., avoid scaling table rows); for elements with little surrounding space, use tint without scale/shadow (shadow without scale looks wrong, since an unscaled element doesn't appear closer despite an elevated shadow).

- macOS: standard mouse/trackpad interactions, many customizable —

| Click or gesture | Expected behavior | Mouse | Trackpad |
| --- | --- | --- | --- |
| Primary click | Select or activate an item, such as a file or button. | ● | ● |
| Secondary click | Reveal contextual menus. | ● | ● |
| Scrolling | Move content up, down, left, or right within a view. | ● | ● |
| Smart zoom | Zoom in or out on content, such as a web page or PDF. | ● | ● |
| Swipe between pages | Navigate forward or backward between individually displayed pages. | ● | ● |
| Swipe between full-screen apps | Navigate forward or backward between full-screen apps and spaces. | ● | ● |
| Mission Control (double-tap the mouse with two fingers or swipe up on the trackpad with three or four fingers) | Activate Mission Control. | ● | ● |
| Lookup and data detectors (force click with one finger or tap with three fingers) | Display a lookup window above selected content. |  | ● |
| Tap to click | Perform the primary click action using a tap rather than a click. |  | ● |
| Force click | Click then press firmly to display a Quick Look/lookup window; apply variable pressure for pressure-sensitive controls (e.g., variable-speed media controls). |  | ● |
| Zoom in or out (pinch with two fingers) | Zoom in or out. |  | ● |
| Rotate (move two fingers in a circular motion) | Rotate content, such as an image. |  | ● |
| Notification Center (swipe from the edge of the trackpad) | Display Notification Center. |  | ● |
| App Exposé (swipe down with three or four fingers) | Display the current app's windows in Exposé. |  | ● |
| Launchpad (pinch with thumb and three fingers) | Display the Launchpad. |  | ● |
| Show Desktop (spread with thumb and three fingers) | Slide all windows out of the way to reveal the desktop. |  | ● |

  Pointers (AppKit): Arrow (`arrow`, standard selection/interaction), Closed hand (`closedHand`, dragging to reposition content, e.g., Maps), Contextual menu (`contextualMenu`, shown generally only with Control held), Crosshair (`crosshair`, precise rectangular selection, e.g., Preview), Disappearing item (`disappearingItem`, dragged item disappears when dropped but the referenced original is unaffected, e.g., dragging a mailbox out of Mail's favorites bar), Drag copy (`dragCopy`, Option held during drag, duplicates rather than moves), Drag link (`dragLink`, Option+Command held during drag, creates an alias of the original file), Horizontal I beam (`iBeam`, text selection/insertion in horizontal layout), Open hand (`openHand`, content repositioning possible), Operation not allowed (`operationNotAllowed`, item can't be dropped here), Pointing hand (`pointingHand`, content is a URL link), Resize down/left/left-right/right/up/up-down (`resizeDown`/`resizeLeft`/`resizeLeftRight`/`resizeRight`/`resizeUp`/`resizeUpDown`), Vertical I beam (`iBeamCursorForVerticalLayout`, text selection/insertion in vertical layout).

- visionOS: people can attach an external pointing device or keyboard alongside continued eye/hand use. Looking at an element then moving the pointer brings focus to the element under the pointer automatically — no extra app work needed. The area people are looking at determines the pointer's context (e.g., shifting eyes between windows seamlessly moves the pointer's context). With a gesture-capable pointing device (trackpad/mouse) attached, the pointer hides while gesturing (minimizing distraction) and reappears where people are looking once they move it.

## Remotes
Source: https://developer.apple.com/design/human-interface-guidelines/remotes
The Siri Remote is the primary input for Apple TV, combining specific buttons with a clickpad/touch surface for familiar gestures like swipe and press.
- Used to navigate tvOS apps, browse channels/content, play/pause media, and make selections.
- **Prefer using standard gestures to perform standard actions** — unless actively playing a game, people expect standard remote behavior everywhere; redefining it causes confusion.
- **Be consistent with the tvOS focus experience** — combine gestures with focus in familiar ways, e.g., always moving focus in the same direction as the gesture. See Focus and selection.
- **Provide clear feedback showing what gestures do** (e.g., a thumb resting on the remote shows where to swipe down to reveal an info area).
- **Define new gestures only when it makes sense** — mainly within gameplay; elsewhere people expect standard gestures.
- **Differentiate between press and tap, and avoid responding to an inadvertent tap** — pressing is intentional (good for choosing/confirming/initiating during gameplay); taps are fine for navigation/showing info, but avoid responding to taps during live video playback since resting/moving/handing off the remote can cause accidental taps.
- **Consider using the position of a tap to aid navigation or gameplay** — the remote differentiates up/down/left/right positional taps on the touch surface; use only where intuitive/discoverable.
- **In almost all cases, open the parent of the current screen when people press the Back button** — at the top level, parent is the Apple TV Home Screen; within an app, parent is defined by app hierarchy (not necessarily the previous screen). Exception: during active gameplay, respond to Back by opening an in-game pause menu (to avoid disrupting gameplay from accidental repeated presses) — closing the menu resumes the game on a subsequent Back press. Pressing and holding Back always goes to the Home Screen from any location. See Buttons.
- **Respond correctly to the Play/Pause button during media playback** — play, pause, or resume as expected.

Gestures: **Swipe** scrolls through large item counts with speed based on swipe strength (edge swipes up/down speed through items quickly). **Press** activates a control/selects an item, and pressing before swiping activates scrubbing mode.

Buttons:

| Button or area | Expected behavior in an app | Expected behavior in a game |
| --- | --- | --- |
| Touch surface (swipe) | Navigates. Changes focus. | Performs directional pad behavior. |
| Touch surface (press) | Activates a control or an item. Navigates deeper. | Performs primary button behavior. |
| Back | Returns to previous screen. Exits to Apple TV Home Screen. | Pauses/resumes gameplay. Returns to previous screen, exits to main game menu, or exits to Apple TV Home Screen. |
| Play/Pause | Activates media playback. Pauses/resumes media playback. | Performs secondary button behavior. Skips intro video. |

Compatible remotes: some remotes compatible with Apple TV add buttons for browsing live TV/channel-based content (e.g., an EPG button; guide-browsing/channel-change buttons). See `Providing Channel Navigation`; for design guidance, `EPG experience`.
- **If your live-viewing app provides an EPG, respond to a remote's EPG-browsing buttons as expected** — a "guide"/"browse" button opens your EPG; "page up"/"page down" navigate through it (tapping the Touch surface's upper/lower area also browses the EPG); avoid other responses to these buttons while browsing. If your app doesn't support an EPG, the system routes these presses to the default guide app.
- **While your content plays, respond to a compatible remote's "page up"/"page down" button by changing the channel** — different expected behavior than while browsing an EPG.
**Platforms:** Not supported in iOS, iPadOS, macOS, visionOS, or watchOS.
