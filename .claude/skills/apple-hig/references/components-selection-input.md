# HIG — Components: selection & input
color-wells, combo-boxes, digit-entry-views, image-wells, pickers, segmented-controls, sliders, steppers, text-fields, toggles, virtual-keyboards

## Color wells
Source: https://developer.apple.com/design/human-interface-guidelines/color-wells
A color well lets people adjust the color of text, shapes, guides, and other onscreen elements, displaying a color picker (system-provided or custom) when tapped or clicked.
- **Consider the system-provided color picker for a familiar experience** — consistent experience, lets people save a set of colors accessible from any app, and helps provide a familiar experience across iOS, iPadOS, and macOS.
**Platforms:** No additional considerations for iOS, iPadOS, or visionOS. Not supported in tvOS or watchOS.
- **macOS:** Clicking a color well highlights it to confirm activation, then opens a color picker; after selection, the well updates to show the new color. Color wells support drag and drop — dragging colors between wells, and from the color picker to a well.

## Combo boxes
Source: https://developer.apple.com/design/human-interface-guidelines/combo-boxes
A combo box combines a text field with a pull-down button in a single control; people can enter a custom value or click the button to choose from a list of predefined values, and an entered custom value is not added to the list.
- **Populate the field with a meaningful default value from the list** — the field can be empty by default, but it's best when the default value refers to the hidden choices; it doesn't have to be the first item.
- **Use an introductory label to let people know what types of items to expect** — generally title-style capitalization, ending with a colon.
- **Provide relevant choices** — people appreciate both entering a custom value and choosing from a list of the most likely choices.
- **Make sure list items aren't wider than the text field** — an overly wide item may be truncated by the field, which is hard to read.
**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## Digit entry views
Source: https://developer.apple.com/design/human-interface-guidelines/digit-entry-views
A digit entry view fills the entire screen and prompts people to enter a series of digits, like a PIN, using a digit-specific keyboard, with an optional title and prompt above the line of digits.
- **Use secure digit fields** — displays asterisks instead of the entered digit; always use when asking for sensitive data.
- **Clearly state the purpose of the digit entry view** — use a title and prompt that explains why digits are needed.
**Platforms:** Not supported in iOS, iPadOS, macOS, visionOS, or watchOS (tvOS only).

## Image wells
Source: https://developer.apple.com/design/human-interface-guidelines/image-wells
An image well is an editable version of an image view; after selecting it, people can copy and paste its image or delete it, and can drag a new image in without selecting first.
- **Revert to a default image when necessary** — if the image well requires an image, redisplay the default image when people clear its content.
- **If your image well supports copy and paste, make sure the standard copy and paste menu items are available** — people expect to use these menu items, or the standard keyboard shortcuts.
**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## Pickers
Source: https://developer.apple.com/design/human-interface-guidelines/pickers
A picker displays one or more scrollable lists of distinct values that people can choose from; the system provides several styles, each with different selectable-value types and appearance, and the exact values shown (and their order) depend on device language.
Prefer pull-down buttons for fairly short lists (a picker adds too much visual weight); prefer pickers for medium-to-long lists; prefer lists and tables (adjustable height, optional index) for very large sets.
- **Consider using a picker to offer medium-to-long lists of items.**
- **Use predictable and logically ordered values** — e.g., an alphabetized list of countries — so people can predict hidden values and move through items quickly.
- **Avoid switching views to show a picker** — works well displayed in context, below or near the field being edited; typically appears at the bottom of a window or in a popover.
- **Consider providing less granularity when specifying minutes in a date picker** — default minute list has 60 values (0–59); you can increase the interval as long as it divides evenly into 60 (e.g., quarter-hour intervals: 0, 15, 30, 45).
**Platforms:** No additional considerations for visionOS.
- **iOS, iPadOS:** A date picker efficiently selects a date, time, or both, via touch, keyboard, or pointer. Values/order depend on device location.

  | Style | Description |
  |---|---|
  | Compact | Button showing editable date/time content in a modal view |
  | Inline | Time only: wheels of values; dates and times: inline calendar view |
  | Wheels | Scrolling wheels, also supports entry via built-in/external keyboards |
  | Automatic | System-determined style based on current platform and mode |

  | Mode | Description |
  |---|---|
  | Date | Months, days of the month, and years |
  | Time | Hours, minutes, and (optionally) AM/PM |
  | Date and time | Dates, hours, minutes, and (optionally) AM/PM |
  | Countdown timer | Hours and minutes, up to 23h 59m; unavailable in inline/compact styles |

  **Use a compact date picker when space is constrained** — button shows current value in the app's accent color; tapping opens a modal calendar-style editor/time picker where people can make multiple edits before dismissing.
- **macOS:** **Choose a date picker style that suits your app** — textual style for limited space and specific date/time selections; graphical style for browsing days in a calendar, selecting a date range, or when a clock-face look is appropriate.
- **tvOS:** Available via SwiftUI `Picker`.
- **watchOS:** Displays lists of items navigated via the Digital Crown. Can display date/time pickers using the wheels style. Configurable outline, caption, and scrolling indicator. For longer lists, a navigation link displays the picker as a button; tapping shows the list of options, and people can also scrub through options via the Digital Crown without tapping the button.

## Segmented controls
Source: https://developer.apple.com/design/human-interface-guidelines/segmented-controls
A segmented control is a linear set of two or more segments, each functioning as a button, usually equal in width, containing text or images (and optionally labels beneath each segment or the control as a whole).
Offers a single choice from a set of options (in macOS, a single choice or multiple choices); can also function as a set of buttons performing actions without showing selection state (momentary; see `isMomentary` / `NSSegmentedControl.SwitchTracking.momentary`).
- **Use a segmented control to provide closely related choices that affect an object, state, or view.**
- **Consider a segmented control when it's important to group functions together, or to clearly show their selection state** — unlike other button styles, segmented controls preserve grouping regardless of view size or placement.
- **Keep control types consistent within a single segmented control** — don't assign actions to segments in a control that otherwise represents selection state, and vice versa.
- **Limit the number of segments in a control** — aim for no more than about five to seven segments in a wide interface, and no more than about five on iPhone.
- **In general, keep segment size consistent** — equal widths feel balanced; keep icon and title widths consistent too.

Content:
- **Prefer using either text or images — not a mix of both — in a single segmented control** — mixing leads to a disconnected, confusing interface.
- **As much as possible, use content with a similar size in each segment** — since segments are typically equal width.
- **Use nouns or noun phrases for segment labels** — title-style capitalization; a text-labeled segmented control doesn't need introductory text.
**Platforms:** Not supported in watchOS.
- **iOS, iPadOS:** **Consider a segmented control to switch between closely related subviews** (e.g., Calendar's New Event sheet). Use tab bars instead for switching between completely separate sections of an app.
- **macOS:** **Consider using introductory text to clarify the purpose of a segmented control** — when using symbols/icons, add a label below each segment, and provide a tooltip per segment if your app uses tooltips. **Use a tab view in the main window area — instead of a segmented control — for view switching**; reserve segmented controls for switching views in a toolbar or inspector pane. **Consider supporting spring loading** — on a Magic Trackpad, lets people activate a segment by dragging selected items over it and force clicking without dropping them, then continue dragging after activation.
- **tvOS:** **Consider using a split view instead of a segmented control** on screens that perform content filtering. **Avoid putting other focusable elements close to segmented controls** — segments select on focus (not click), so nearby elements risk accidental focus.
- **visionOS:** Looking at an icon-based segmented control displays a tooltip with the descriptive text you supply.

## Sliders
Source: https://developer.apple.com/design/human-interface-guidelines/sliders
A slider is a horizontal track with a thumb control that people adjust between a minimum and maximum value; the track between the minimum and the thumb fills with color as the value changes, and left/right icons can illustrate the meaning of the minimum and maximum.
- **Customize a slider's appearance if it adds value** — track color, thumb image/tint color, left/right icons — to blend with your app's design and communicate intent.
- **Use familiar slider directions** — minimum on the leading side, maximum on the trailing side (horizontal); minimum at the bottom, maximum at the top (vertical).
- **Consider supplementing a slider with a corresponding text field and stepper** — especially for wide ranges, people appreciate seeing/entering the exact value; a stepper adds convenient whole-value increments.
**Platforms:** Not supported in tvOS.
- **iOS, iPadOS:** **Don't use a slider to adjust audio volume** — use a volume view instead (customizable, includes a volume-level slider and an audio-output-device control).
- **macOS:** Sliders can include tick marks for pinpointing specific values. Linear slider: thumb is a narrow lozenge shape, track fills with color between minimum and thumb, often with supplementary min/max icons. Circular slider: thumb appears as a small circle; tick marks (if present) appear as evenly spaced dots around the circumference.
  - **Consider giving live feedback as the value of a slider changes** — e.g., Dock icons dynamically scale while adjusting the Size slider in Dock settings.
  - **Choose a slider style that matches peoples' expectations** — horizontal slider for a fixed starting/ending point (e.g., opacity 0–100%); circular slider when values repeat or continue indefinitely (e.g., rotation 0–360°, or spins where 4 rotations = 1440°).
  - **Consider using a label to introduce a slider** — sentence-style capitalization, ending with a colon.
  - **Use tick marks to increase clarity and accuracy** — helps convey scale and locate specific values.
  - **Consider adding labels to tick marks for even greater clarity** — numbers or words; needn't label every tick (often only min/max is sufficient); nonlinear slider values benefit from periodic labels; also provide a tooltip showing the thumb's value on hover.
- **visionOS:** **Prefer horizontal sliders** — easier to gesture side to side than up and down.
- **watchOS:** A slider is a horizontal track (discrete steps or a continuous bar) representing a finite range; people tap buttons on the sides to increase/decrease by a predefined amount. **If necessary, create custom glyphs to communicate what the slider does** (system default: plus/minus signs).

## Steppers
Source: https://developer.apple.com/design/human-interface-guidelines/steppers
A stepper is a two-segment control people use to increase or decrease an incremental value; it sits next to a field that displays its current value, since the stepper itself doesn't display a value.
- **Make the value that a stepper affects obvious** — ensure people know which value they're changing.
- **Consider pairing a stepper with a text field when large value changes are likely** — steppers alone work well for small changes (a few taps/clicks); a field lets people enter specific values when they can vary widely (e.g., a printing screen's number of copies).
**Platforms:** No additional considerations for iOS, iPadOS, or visionOS. Not supported in watchOS or tvOS.
- **macOS:** **For large value ranges, consider supporting Shift-click to change the value quickly** — e.g., by 10 times the default increment.

## Text fields
Source: https://developer.apple.com/design/human-interface-guidelines/text-fields
A text field is a rectangular area in which people enter or edit small, specific pieces of text.
Use for small amounts of information (a name or email address); use text views instead for larger amounts of text.
- **Show a hint in a text field to help communicate its purpose** — placeholder text (e.g., "Email," "Password") appears when the field is otherwise empty; since it disappears once typing starts, also consider a separate descriptive label.
- **Use secure text fields to hide private data** — always use for sensitive data, such as a password.
- **To the extent possible, match the size of a text field to the quantity of anticipated text** — helps people visually gauge how much information to provide.
- **Evenly space multiple text fields** — leave enough space so people can see which field belongs with each label; stack fields vertically when possible, and use consistent widths for an organized layout (e.g., first/last name one width, address/city another).
- **Ensure that tabbing between multiple fields flows as people expect** — move focus in a logical sequence (the system usually achieves this automatically).
- **Validate fields when it makes sense** — e.g., alert people if a digits-only field contains other characters. Timing depends on context: validate an email address when people switch to another field; validate a username or password before allowing the switch.
- **Use a number formatter to help with numeric data** — auto-configures the field to accept only numeric values, and can display it in a specific way (decimal places, percentage, currency); don't assume the actual presentation, since formatting varies by locale.
- **Adjust line breaks according to the needs of the field** — by default the system clips overflowing text; alternatively wrap at the character or word level, or truncate (with an ellipsis) at the beginning, middle, or end.
- **Consider using an expansion tooltip to show the full version of clipped or truncated text** — behaves like a regular tooltip, appearing on pointer hover.
- **In iOS, iPadOS, tvOS, and visionOS apps, show the appropriate keyboard type** — several keyboard types facilitate different input (numbers, URLs, etc.); display the one matching the content being entered.
- **Minimize text entry in your tvOS and watchOS apps** — entering long passages or many fields is time-consuming; gather information more efficiently, e.g., with buttons.
**Platforms:** No additional considerations for tvOS or visionOS.
- **iOS, iPadOS:** **Display a Clear button in the trailing end of a text field** to help people erase input without repeatedly tapping Delete. **Use images and buttons to provide clarity and functionality** — custom images at both ends, or a system-provided button (e.g., Bookmarks); generally use the leading end to indicate the field's purpose and the trailing end for additional features.
- **macOS:** **Consider using a combo box if you need to pair text input with a list of choices.**
- **watchOS:** **Present a text field only when necessary** — prefer displaying a list of options over requiring text entry.

## Toggles
Source: https://developer.apple.com/design/human-interface-guidelines/toggles
A toggle lets people choose between a pair of opposing states, like on and off, using a different appearance for each state; styles include switch and checkbox, used differently by platform. All platforms also support buttons that behave like toggles via a different appearance per state (see `ToggleStyle`).
- **Use a toggle to help people choose between two opposing values that affect the state of content or a view** — use a different component (e.g., pop-up buttons) for choosing from a list of items.
- **Clearly identify the setting, view, or content the toggle affects** — surrounding context is usually enough; macOS apps can also supply a descriptive label. A toggle-behaving button generally uses an interface icon communicating its purpose and updates its appearance (typically the background) based on state.
- **Make sure the visual differences in a toggle's state are obvious** — add/remove a color fill, show/hide the background shape, or change inner details (checkmark, dot); avoid relying solely on color, since not everyone can perceive the difference.
**Platforms:** No additional considerations for tvOS, visionOS, or watchOS.
- **iOS, iPadOS:**
  - **Use the switch toggle style only in a list row** — no label needed, since row content provides context.
  - **Change the default color of a switch only if necessary** — default green works well in most cases; if using the app's accent color instead, ensure enough contrast with the uncolored appearance.
  - **Outside of a list, use a button that behaves like a toggle, not a switch** — e.g., Phone's filter button adds a blue highlight when active and removes it when inactive.
  - **Avoid supplying a label that explains the button's purpose** — the interface icon plus alternative background appearances communicate the function (see `changesSelectionAsPrimaryAction`).
- **macOS:** Also supports the checkbox style and radio buttons. **Use switches, checkboxes, and radio buttons in the window body, not the window frame** — avoid toolbars or status bars.
  - **Switches:** **Prefer a switch for settings you want to emphasize** — more visual weight than a checkbox, suited to controlling a group of settings rather than just one (see `switch`). **Within a grouped form, consider using a mini switch to control the setting in a single row** — its height matches other controls for row-height consistency; use a regular switch for the primary setting and mini switches for subordinate settings in a hierarchy (see `GroupedFormStyle`, `ControlSize`). **In general, don't replace a checkbox with a switch** — if already using a checkbox, keep it.
  - **Checkboxes:** A small, square button — empty when off, containing a checkmark when on, and a dash for mixed state; typically has a trailing title (can appear without title/content in an editable checklist). **Use a checkbox instead of a switch if you need to present a hierarchy of settings** — alignment (generally along the leading edge) and indentation shows dependencies. **Consider using radio buttons if you need to present a set of more than two mutually exclusive options.** **Consider using a label to introduce a group of checkboxes if their relationship isn't clear** — align the label's baseline with the first checkbox. **Accurately reflect a checkbox's state in its appearance** — on, off, or mixed (e.g., a style-group checkbox shown mixed when subordinate bold/italic/underline checkboxes differ; see `allowsMixedState`).
  - **Radio buttons:** A small, circular button followed by a label, typically displayed in groups of two to five, presenting mutually exclusive choices. State is selected (filled circle) or deselected (empty circle); a mixed state (dash) is rarely useful. **Prefer a set of radio buttons to present mutually exclusive options** — use checkboxes if multiple selections are allowed. **Avoid listing too many radio buttons in a set** — for more than about five options, consider a pop-up button instead. **To present a single setting that can be on or off, prefer a checkbox** — the presence/absence of a checkmark reads more clearly at a glance than a single radio button; in rare cases use a pair of radio buttons, each labeled with the state it controls. **Use consistent spacing when you display radio buttons horizontally** — measure the space needed for the longest label and apply it consistently.

## Virtual keyboards
Source: https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards
On devices without physical keyboards, the system offers various types of virtual keyboards for entering data, each providing a set of keys optimized for the current task (e.g., an email keyboard includes "@" and a period or ".com"); a virtual keyboard doesn't support keyboard shortcuts.
- **Choose a keyboard that matches the type of content people are editing** — e.g., a numbers-and-punctuation keyboard for numeric data; specifying a semantic meaning for an input area lets the system auto-provide a matching keyboard and refine its corrections (see `keyboardType(_:)`, `textContentType(_:)` in SwiftUI; `UIKeyboardType`, `UITextContentType` in UIKit).
- **Consider customizing the Return key type if it helps clarify the text-entry experience** — based on keyboard type by default, but changeable (e.g., a search Return key for a search-initiating app; see `submitLabel(_:)`, `UIReturnKeyType`).

Custom input views:
- An *input view* replaces the system keyboard with custom functionality while people are in your app (e.g., Numbers' custom numeric input view for spreadsheets; see `inputViewController`).
- **Make sure your custom input view makes sense in the context of your app** — otherwise people may wonder why they can't regain the system keyboard.
- **Play the standard keyboard sound while people type** — people expect the familiar tap feedback (can be turned off in Settings > Sounds; see `playInputClick()`).

Custom keyboards (app extension):
- **In iOS, iPadOS, and tvOS, you can provide a custom keyboard that replaces the system keyboard by creating an app extension** — code people can install to extend a specific area of system functionality.
- After choosing a custom keyboard in Settings, people can use it for text entry within any app, except when editing secure text fields and phone number fields; they can install and switch between multiple custom keyboards at any time.
- Custom keyboards make sense to expose unique keyboard functionality systemwide (a novel text-input method, or a language the system doesn't support); use a custom input view instead if the keyboard is only needed within your own app.
- **Provide an obvious and easy way to switch between keyboards** — people expect the Globe key experience.
- **Avoid duplicating system-provided keyboard features** — the Emoji/Globe key and Dictation key appear automatically even with custom keyboards active, and your app can't affect them.
- **Consider providing a keyboard tutorial in your app** — help people learn to choose, activate, use, and switch back from your keyboard; avoid displaying help content within the keyboard itself.
**Platforms:** Not supported in macOS.
- **iOS, iPadOS:** **Use the keyboard layout guide to make the keyboard feel like an integrated part of your interface** — also keeps important UI visible while the keyboard is onscreen. **Place custom controls above the keyboard thoughtfully** — an input accessory view can offer app-specific controls relevant to the current task (e.g., Numbers' spreadsheet calculation controls); apply Liquid Glass to the containing view if other views use it or it would otherwise look out of place (a standard toolbar automatically adopts Liquid Glass); use the keyboard layout guide and standard padding for expected positioning.
- **tvOS:** Displays a linear virtual keyboard when people select a text field using the Siri Remote.
  > Note: A grid keyboard screen appears when people use devices other than the Siri Remote, and content layout automatically adapts to the keyboard.

  Activating a digit entry view displays a digit-specific keyboard.
- **visionOS:** The system-provided virtual keyboard supports both direct and indirect gestures and appears in a separate, movable window; you don't need to account for keyboard location in your layouts.
- **watchOS:** A text field can show a keyboard if the device screen is large enough; otherwise the system offers dictation or Scribble. You can't change the keyboard type, but you can set the text field's content type, which the system uses to ease entry (e.g., offering suggestions; see `textContentType(_:)`). People can also use a nearby paired iPhone to enter text.
