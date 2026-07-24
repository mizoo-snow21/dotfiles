# HIG — Components: menus & actions
Covers: activity-views, buttons, context-menus, dock-menus, edit-menus, home-screen-quick-actions, menus, ornaments, pop-up-buttons, pull-down-buttons, the-menu-bar, toolbars

## Activity views
Source: https://developer.apple.com/design/human-interface-guidelines/activity-views
An activity view — often called a *share sheet* — presents a range of tasks people can perform in the current context (sharing activities like messaging, actions like Copy and Print, and quick access to frequently used apps).
Use the Share button to reveal it; people typically choose it while viewing a page/document or after selecting an item. It can appear as a sheet or a popover depending on device and orientation.
- App-specific activities appear before actions available in multiple apps or system-wide (e.g., Add to Files, AirPlay); people can edit the list of actions to reorder/add favorites.
- App extensions let you provide custom share/action activities usable in other apps; even though macOS has no activity view, you can still create share and action extensions for use there.
- **Avoid creating duplicate versions of common actions** already in the activity view (e.g., a duplicate Print action is confusing). If similar app-specific functionality is needed, give it a custom, distinguishing title (e.g., "Print Transaction").
- **Consider using a symbol to represent your custom activity.** Prefer SF Symbols; for a custom interface icon, center it in an area of about 70x70 pixels.
- **Write a succinct, descriptive title for each custom action** — a single verb or brief verb phrase; avoid company/product name in the action title (contrast: a share activity's title, typically a company name, appears below its icon).
- **Make sure activities are appropriate for the current context** — you can't reorder system-provided tasks but can exclude inapplicable ones (e.g., exclude Print if printing doesn't apply), and control which custom tasks show at a given time.
- **Use the Share button to display an activity view** — don't provide an alternative way to do the same thing.
- Share extensions let people share info from the current context with apps/social accounts/services; action extensions let people initiate content-specific tasks (add a bookmark, copy a link, edit an inline image, translate selected text) without leaving the current context.
- **If necessary, create a custom interface that feels familiar** — prefer the system-provided composition view for a share extension; include your app name for an action extension; if you must present an interface, include elements of your app's interface.
- **Streamline and limit interaction** — e.g., a share extension might post an image with a single tap.
- **Avoid placing a modal view above your extension** — the system already displays an extension within a modal view; an alert above it may be necessary, but avoid additional modal views.
- **If necessary, provide an image that communicates the purpose of your extension** — a share extension automatically uses your app icon; for an action extension, prefer a symbol or a clear custom interface icon.
- **Use your main app to denote progress of a lengthy operation** — an activity view dismisses immediately after the share/action task completes; continue time-consuming tasks in the background and let people check status in your main app; don't notify people just because the task completes (only for problems).
**Platforms:** Not supported in macOS, tvOS, or watchOS (no additional considerations for iOS, iPadOS, or visionOS) — but macOS still supports share/action extensions, accessed via a Share button in the toolbar, Share in a context menu, hovering over embedded content, a toolbar button, or a Finder quick action, not via an activity view.

## Buttons
Source: https://developer.apple.com/design/human-interface-guidelines/buttons
A button initiates an instantaneous action, combining **style** (size/color/shape), **content** (symbol/text label/both), and **role** (system-defined semantic meaning that can affect appearance).
Related button-like components with distinct appearances/behaviors: Toggles, Pop-up buttons, Segmented controls.
- **Make buttons easy for people to use** — give a button a hit region of at least 44x44 pt (60x60 pt in visionOS) and enough surrounding space to visually distinguish it, regardless of input method (fingertip, pointer, eyes, remote).
- **Always include a press state for a custom button** — without one, a button can feel unresponsive.
- **Use a prominent visual style for the most likely action in a view** — draws attention via accent color; keep prominent buttons to one or two per view (more increases cognitive load).
- **Use style — not size — to distinguish the preferred choice among multiple options** — same-size buttons signal a coherent set of choices; use a more prominent style for the preferred option, less prominent for the rest.
- **Avoid applying a similar color to button labels and content layer backgrounds** — prefer the default monochromatic label appearance if the content layer is already bright/colorful (see Liquid Glass color).
- **Ensure each button clearly communicates its purpose** via symbol/icon, text label, or both.
> Note: In macOS and visionOS, the system displays a tooltip after people hover over a button for a moment.
- **Try to associate familiar actions with familiar icons** (e.g., `square.and.arrow.up` for share); see Standard icons for a list.
- **Consider using text when a short label communicates more clearly than an icon** — title-style capitalization, consider starting with a verb (e.g., "Add to Cart").
- Roles: **Normal** (no specific meaning), **Primary** (the default/most-likely button), **Cancel** (cancels current action), **Destructive** (can result in data destruction; uses system red).
- **Assign the primary role to the button people are most likely to choose** — it responds to the Return key; in a temporary view (Sheets, an editable view, Alerts) the view can auto-close when Return is pressed.
- **Don't assign the primary role to a destructive button**, even if it's the most likely choice — people sometimes choose a primary button without reading it; assign primary to nondestructive buttons instead.
**Platforms:** No additional considerations for tvOS.
- **iOS, iPadOS:** Configure a button to show an activity indicator for actions that don't complete instantly; optionally change the label too (e.g., "Checkout" → "Checking out…"); the system hides the button's image (if any) while the indicator shows.
- **macOS:** Several button types are unique to macOS.
  - *Push buttons* — the standard type; can show text/symbol/icon/image or combinations; can be the default button; tintable. Use a **flexible-height push button** only for tall/variable-height content (same corner radius/padding as standard, `NSButton.BezelStyle.flexiblePush`); otherwise use standard. **Append a trailing ellipsis** when a push button opens another window/view/app. **Consider supporting spring loading** — on Magic Trackpad, force-clicking while dragging selected items over a button activates it without dropping the items, and dragging can continue afterward.
  - *Square buttons* (aka gradient buttons) — initiate view-related actions (e.g., add/remove table rows); contain symbols/icons, not text; can behave like push/toggle/pop-up buttons; appear near their associated view. **Use square buttons in a view, not the window frame** (use a toolbar item for toolbars). **Prefer a symbol.** **Avoid introducing them with labels.** (`NSButton.BezelStyle.smallSquare`)
  - *Help buttons* — circular, contain a question mark, open app-specific help. **Use the system-provided help button.** **Open the context-related help topic when possible**, else the top level of help documentation. **Include no more than one help button per window.** **Position help buttons** per: Dialog with dismissal buttons (OK/Cancel) → lower corner, opposite and vertically aligned with them; Dialog without dismissal buttons → lower-left or lower-right corner; Settings window/pane → lower-left or lower-right corner. **Use within a view, not the window frame.** **Avoid introductory text.**
  - *Image buttons* — display an image/symbol/icon; can behave like push/toggle/pop-up buttons. **Use in a view, not the window frame** (use a toolbar item for toolbars). **Include about 10 pixels of padding** between image edges and button edges (edges define the clickable area even when invisible); generally avoid a system-provided border (`isBordered`). **If a label is needed, position it below the image button.**
- **visionOS:** Buttons typically show a visible background and play sound on interaction. Three standard shapes: icon-only → circle; text-only → roundedRectangle or capsule; icon+text → capsule. Four visual styles communicate interaction states.
  > Note: visionOS buttons don't support custom hover effects.
  - A button can reveal a tooltip on gaze (text-containing buttons usually don't need one).
  - Sizes: | Shape | Mini (28 pt) | Small (32 pt) | Regular (44 pt) | Large (52 pt) | Extra large (64 pt) | across Circular, Capsule (text only), Capsule (text and icon), Rounded rectangle.
  - **Prefer buttons with a discernible background shape and fill** — exception: buttons in a toolbar, context menu, alert, or Ornaments, where the larger component's shape/material already makes them visible. When a button appears on top of glass visionOS content, use the thin material as its background; when floating in space, use the visionOS material for its background.
  - **Avoid a custom button with a white background fill and black text/icons** — reserved for the toggled state.
  - **Prefer circular or capsule-shape buttons** — more rounded shapes are easier to keep looking at; prefer capsule for a standalone button.
  - **Provide enough space around a button** — keep centers at least 60 pt apart; if buttons are ≥60 pt, add 4 pt padding to avoid hover-effect overlap; avoid small/mini buttons in a vertical stack or horizontal row.
  - **Choose the right shape for text-labeled stacks/rows** — rounded-rectangle in a vertical stack, capsule in a horizontal row.
  - **Use standard controls** to get the audible feedback sounds people already know (visionOS has no haptics).
- **watchOS:** All inline buttons use the capsule shape and gain a material effect against the background. **Use a toolbar to place buttons in the corners** (system moves time/title to accommodate; Liquid Glass applied to toolbar buttons). **Prefer full-width buttons for primary actions**; if two buttons share a row, use the same height for both, with images or short text titles. **Use toolbar buttons for navigation to related areas or contextual actions.** **Use the same height for vertical stacks of one- and two-line text buttons.**

## Context menus
Source: https://developer.apple.com/design/human-interface-guidelines/context-menus
A context menu provides access to functionality directly related to an item, without cluttering the interface — hidden by default, revealed by touch/pinch and hold (visionOS, iOS, iPadOS), Control-key + click (macOS, iPadOS), or a secondary click on a Magic Trackpad (macOS, iPadOS).
- **Prioritize relevancy** — a context menu is for the commands people are most likely to need right now, not advanced or rarely used items.
- **Aim for a small number of menu items** — a long menu is hard to scan and scroll.
- **Support context menus consistently throughout your app** — inconsistent support makes people think there's a problem.
- **Always make context menu items available in the main interface too** (e.g., toolbar items in iOS/iPadOS; an app's menu bar menus list all commands in macOS).
- **If submenus are needed to manage complexity, keep them to one level**, with an intuitive title that helps people predict contents without opening it.
- **Hide unavailable menu items, don't dim them** — unlike a regular menu, a context menu shows only relevant actions (exception: in macOS, Cut/Copy/Paste may appear unavailable if inapplicable).
- **Aim to place the most frequently used items where people encounter them first** — people read from where their finger/pointer revealed the menu; you may need to reverse item order depending on whether the menu opens above or below the selection.
- **Show keyboard shortcuts in your app's main menus, not context menus** — redundant there.
- **Follow separator best practices** — group items with separators; aim for no more than about three groups in a context menu (see Menus).
- **In iOS, iPadOS, and visionOS, warn about destructive items** — list them at the end and identify as destructive (`destructive`); the system can show them in red.
- A context menu seldom has a title; each item needs a short, clear label. **Include a title only if it clarifies the menu's effect** (e.g., stating the number of selected messages).
- **Represent menu item actions with familiar icons** — same icons as the system for Copy, Share, Delete, etc. (see Standard icons).
**Platforms:** No additional considerations for tvOS. Not supported in watchOS.
- **iOS, iPadOS:** **Provide either a context menu or an edit menu for an item, not both** (confusing to people, hard for the system to detect intent). In iPadOS, **consider using a context menu to let people create a new object** (e.g., Files creates a new folder via a context menu in empty space). A context menu can show a content preview near the commands; people can tap it to open or drag it elsewhere. **Prefer a graphical preview that clarifies the target** of the menu's commands. **Ensure the preview animates well** — adjust its clipping path to match the preview shape (e.g., rounded corners) so contours don't visibly change during the animation (`UIContextMenuInteractionDelegate`).
- **macOS:** Also called a *contextual* menu.
- **visionOS:** **Consider using a context menu instead of a panel or inspector window** to keep space uncluttered. **Avoid letting a context menu's height exceed the window's height** — a window has system components (e.g., window-management controls, Share menu) above/below its edges that a too-tall menu could obscure.

## Dock menus
Source: https://developer.apple.com/design/human-interface-guidelines/dock-menus
On a Mac, secondary-clicking an app's or game's icon in the Dock reveals a Dock menu that presents both system-provided and custom items; the system-provided items can vary depending on whether the app is open.
> Note: iOS and iPadOS don't support a Dock menu, but a similar menu — Home Screen quick actions — appears on long press of an app icon on the Home Screen or in the Dock.
- Label items succinctly and organize logically, as with all menus (see Menus).
- **Make custom Dock menu items available in other places too** (e.g., menu bar menus or within your interface) — not everyone uses a Dock menu.
- **Prefer high-value custom items** — e.g., list currently/recently open windows for quick jumping, and actions likely useful when the app isn't frontmost or has no open windows (Mail: Get new mail, compose a new message, plus a list of open windows).
**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## Edit menus
Source: https://developer.apple.com/design/human-interface-guidelines/edit-menus
An edit menu lets people make changes to selected content in the current view, plus related commands like Copy, Select, Translate, and Look Up.
In iOS, iPadOS, and visionOS the system auto-detects the data type of a selected item and may add a related action to the menu (e.g., selecting an address can add *Get directions*).
- **Prefer the system-provided edit menu** — a custom menu with the same commands is redundant and likely confusing; standard commands are listed in `UIResponderStandardEditActions`.
- **Let people reveal an edit menu using the system-defined interactions they already know** (touch and hold, pinch and hold in visionOS, secondary click with a trackpad/keyboard) — avoid a custom interaction for this standard task.
- **Offer commands relevant to the current context**, removing or dimming ones that don't apply (no Copy/Cut without a selection, no Paste with nothing to paste).
- **List custom commands near relevant system-provided ones** (e.g., custom formatting commands after system ones in the format section); avoid overwhelming people with too many custom commands.
- **When it makes sense, let people select and copy noneditable text** (e.g., an image caption) — copy content text, but not control labels.
- **Support undo and redo when possible** — an edit menu doesn't require confirmation, so undo/redo lets people recover a previous state.
- **In general, avoid implementing other controls that duplicate edit menu functions** — redundant controls crowd the interface.
- **Differentiate different types of deletion commands** — e.g., Delete behaves like the Delete key, while Cut copies to the pasteboard before deleting.
- **Create short labels for custom commands** — verbs or short verb phrases (see Labels).
**Platforms:** No additional considerations for visionOS. Not supported in tvOS or watchOS (editing content is rare there).
- Presentation differs by platform: **iOS** — compact horizontal list on touch-and-hold/double-tap select, with a chevron on the trailing edge to expand into a Context menu. **iPadOS** — compact horizontal style via touch, or opens directly as a context menu via keyboard/pointing device. **macOS** — a context menu during an editing task, plus the app's Edit menu in the menu bar. **visionOS** — the standard gesture opens it as a horizontal bar, or it opens in a context menu.
- **iOS, iPadOS:** **Ensure your edit menu works well in both styles** (compact horizontal via Multi-Touch; vertical via keyboard/pointing device). **Adjust placement if necessary** — default position is above/below the insertion point/selection with a visual indicator pointing to the content; menu shape/pointer can't change, but position can (e.g., to avoid covering important content).
- **macOS:** For the order of items in a macOS app's Edit menu, see the Edit menu table under The menu bar.

## Home Screen quick actions
Source: https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions
Home Screen quick actions give people a way to perform app-specific actions from the Home Screen, revealed by touch and hold on an app icon (or, on a 3D Touch device, increased-pressure press); the menu also lists items for removing the app and editing the Home Screen.
Each quick action has a title, an interface icon on the left or right (depending on the app's Home Screen position), and an optional subtitle; title/subtitle are always left-aligned in left-to-right languages. Quick actions can update dynamically (e.g., Messages surfaces recent conversations).
- **Create quick actions for compelling, high-value tasks** — you can provide up to four; most apps should offer at least one.
- **Avoid making unpredictable changes to quick actions** — dynamic updates (by location, recent activity, time of day, settings) are fine as long as changes are predictable.
- **For each quick action, provide a succinct title that instantly communicates the result** (e.g., "Directions Home," "Create New Contact," "New Message"); add a subtitle for more context if needed (e.g., Mail shows unread counts). Don't include your app name or extraneous info; keep text short to avoid truncation; account for localization.
- **Provide a familiar interface icon** — prefer SF Symbols; for a custom icon, use the Quick Action Icon Template in Apple Design Resources for iOS and iPadOS.
- **Don't use an emoji in place of a symbol or interface icon** — emoji are full color, whereas quick action symbols are monochromatic and adapt in Dark Mode.
**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## Menus
Source: https://developer.apple.com/design/human-interface-guidelines/menus
A menu reveals its options when people interact with it, a space-efficient way to present commands; opening it reveals one or more *menu items*, each representing a command, option, or state affecting the current selection or context.
Related components with built-in menus: Pop-up buttons, Pull-down buttons, Context menus (a few frequently used actions), and The menu bar (all app commands, in macOS/iPadOS).
- **For each menu item, write a label that clearly and succinctly describes it** — use a verb or verb phrase for an action (View, Close, Select); for show/hide or state labels, see Toggled items below. Depending on menu layout, iOS/iPadOS/visionOS can show a few unlabeled items using only a symbol/icon.
- **Use title-style capitalization** for consistency with platform experiences (capitalizes every word except articles, coordinating conjunctions, and short prepositions, and always capitalizes the last word).
- **Remove articles** (a, an, the) from menu-item labels to save space — they rarely enhance understanding.
- **Show people when a menu item is unavailable** — dimmed and non-responsive; if all items in a menu are unavailable, the menu itself must remain available so people can open it and learn what it contains.
- **Append an ellipsis to a menu item's label** when the action needs more input/another view before it can complete.
- **Represent common actions consistently** with standard icons (Share, Print, Search — see Standard icons).
- **Use menu item icons sparingly and with purpose** — for the most common actions/key features, file system locations, connected devices, visual concepts (rotate, flip), and user-generated content (folders, documents); don't add an icon if none clearly represents the item.
- **Apply a uniform visual treatment across menu items in the same group** — icons for all items in a group, or none.
- **Prefer listing important or frequently used menu items first** — people scan from the top.
- **Consider grouping logically related items**, using a separator (a horizontal line or short gap) to distinguish groups.
- **Prefer keeping logically related commands in the same group** even if they differ in importance (e.g., Paste and Match Style stays with the more-used Copy/Cut group).
- **Be mindful of menu length** — divide a too-long menu into separate menus, or use a submenu (e.g., difficulty levels under New Game); exception: user-defined/dynamically generated content (History, Bookmarks in Safari), where a long, scrollable menu is expected and fine.
- A *submenu* is a menu item revealing a subordinate list, indicated by a symbol (e.g., chevron) after the label; functionally identical to a menu. **Use submenus sparingly** — consider one when a term repeats across more than two items in the same group (e.g., a "Sort by" submenu listing Date/Score/Time instead of three separate items); reuse the repeated term in the parent item's label.
- **Limit the depth and length of submenus** — restrict to a single level; if a submenu exceeds about five items, consider a new menu instead.
- **Make sure a submenu remains available even when its nested items are unavailable.**
- **Prefer using a submenu to indenting menu items** — indentation is inconsistent with the system and doesn't clearly express relationships.
- **Consider a changeable label describing an item's current state** instead of two separate items (e.g., one item toggling between Show Map / Hide Map).
- **Include a verb if a changeable label isn't clear enough** (e.g., HDR On/Off → Turn HDR On / Turn HDR Off).
- **If necessary, display both items instead of one toggled item** (e.g., Take Account Online and Take Account Offline, with only the applicable one available).
- **Consider a checkmark to show an attribute is currently in effect** (e.g., Format > Font styles).
- **Consider offering an item to remove multiple toggled attributes at once** (e.g., "Plain" to clear all formatting).
- In-game menus: **let players navigate using the platform's default interaction method** they already use elsewhere on the device. **Make sure your menus remain easy to open and read on all platforms** — adjust tap target size and consider alternate ways to communicate content if scaled content becomes too small (see Typography, Touch controls).
**Platforms:** No additional considerations for macOS, tvOS, or watchOS.
- **iOS, iPadOS:** Three layouts (`preferredElementSize`): | Layout | Description | | Small | Row of 4 items at top (symbol/icon only, no label), remaining items in a list below | | Medium | Row of 3 items at top (symbol/icon + short label), remaining items in a list below | | Large (default) | All items in a list |. **Choose a small or medium layout to streamline choices** — medium for ~3 important, frequently used actions (e.g., Notes: Scan, Lock, Pin); small only for closely related grouped actions with recognizable symbols and no label (e.g., Bold, Italic, Underline, Strikethrough).
- **visionOS:** Can use the small or large iOS/iPadOS layout styles; present a menu from 3D content via a SwiftUI view; apply a breakthrough effect to keep the menu visible when occluded; as in macOS, an open menu in a window can appear outside the window's boundaries. **Prefer displaying a menu near the content it controls** — people must look at an item before tapping it. **Prefer the subtle breakthrough effect in most cases** (blends with surrounding content; `automatic` defaults to subtle when the menu overlaps 3D content); use `prominent` only when it's important to display the menu prominently over the entire scene (can disrupt/cause discomfort); use `none` to fully occlude the menu behind other 3D content (may make it hard to access).

## Ornaments
Source: https://developer.apple.com/design/human-interface-guidelines/ornaments
In visionOS, an ornament presents controls and information related to a window, without crowding or obscuring the window's contents — it floats parallel to and slightly in front of its window along the z-axis, moves with the window, and stays unchanged as the window's content scrolls.
Ornaments can appear on any edge of a window and contain UI components (buttons, segmented controls, other views); the system uses ornaments for Toolbars, Tab bars, and video playback controls, and you can use one to create a custom component.
- **Consider using an ornament for frequently needed controls or information** in a consistent location that doesn't clutter the window (e.g., Music's Now Playing controls).
- **In general, keep an ornament visible** — it can make sense to hide one when people dive into content (e.g., watching a video, viewing a photo), but otherwise keep consistent access.
- **If you display multiple ornaments, prioritize overall visual balance** — constrain the total number to avoid increasing visual weight and complexity; if you remove an ornament, relocate its elements into the main window.
- **Aim to keep an ornament's width the same as or narrower than its window** — a wider ornament can interfere with a tab bar or other vertical content on the window's side.
- **Consider using borderless buttons in an ornament** — an ornament's background is glass by default, so a button placed directly on it may not need a visible border; the system automatically applies the hover effect to borderless buttons.
- **Use system-provided toolbars and tab bars unless you need custom components** — they automatically appear as ornaments in visionOS.
**Platforms:** Not supported in iOS, iPadOS, macOS, tvOS, or watchOS.

## Pop-up buttons
Source: https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons
A pop-up button displays a menu of mutually exclusive options; after a choice, the menu closes and the button can update its content to show the current selection.
Use for a flat list of mutually exclusive options/states. Prefer a pull-down button instead if you need to offer a list of actions, let people select multiple items, or include a submenu.
- **Provide a useful default selection** — shown until people choose, so pick the item most people are likely to want.
- **Give people a way to predict a pop-up button's options without opening it** — e.g., an introductory label or a button label describing its effect.
- **Consider using a pop-up button when space is limited** and not all options need to be visible at once.
- **If necessary, include a Custom option** in the menu for additional items useful only occasionally, avoiding interface clutter; you can display explanatory text below the list to help people understand the options.
**Platforms:** No additional considerations for iOS, macOS, or visionOS. Not supported in tvOS or watchOS.
- **iPadOS:** Within a popover or modal view, **consider using a pop-up button instead of a disclosure indicator** for a list item with multiple options — lets people choose quickly without navigating to a detail view; best for a fairly small, well-defined option set.

## Pull-down buttons
Source: https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons
A pull-down button displays a menu of items or actions directly related to the button's purpose; after a choice, the menu closes and the app performs the chosen action.
Use for commands or items directly related to the button's action (e.g., an Add button offering item types to add, a Sort button offering sort attributes, a Back button offering specific locations to revisit). Use a pop-up button instead for a list of mutually exclusive choices that aren't commands.
- **Avoid putting all of a view's actions in one pull-down button** — a view's primary actions need to be easily discoverable, not hidden behind a button people must open first.
- **Balance menu length with ease of use** — list a minimum of three items so the interaction feels worthwhile (for one or two items, use alternative components like buttons or toggles/switches instead); too many items slows people down.
- **Display a succinct menu title only if it adds meaning** — usually the button's content plus descriptive items give enough context.
- **Let people know when a menu item is destructive, and ask them to confirm intent** — destructive items use red text; choosing one shows an Action sheet (iOS) or Popover (iPadOS) to confirm or cancel, helping avoid accidental data loss (separate location, deliberate dismissal).
- **Include an interface icon with a menu item when it provides value** — SF Symbols stay aligned with text at every scale.
**Platforms:** No additional considerations for macOS or visionOS. Not supported in tvOS or watchOS.
- **iOS, iPadOS:**
> Note: You can also let people reveal a pull-down menu via a specific gesture on a button (e.g., in iOS 14+, Safari shows tab-related actions like New Tab and Close All Tabs on touch-and-hold of the Tabs button).
- **Consider using a More pull-down button** for items that don't need prominent positions in the main interface — helps offer more items in constrained space, but the ellipsis icon doesn't help predict contents, so weigh convenience against discoverability.

## The menu bar
Source: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar
On a Mac or an iPad, the menu bar at the top of the screen displays the top-level menus in your app or game; iPad menu bars mirror macOS order and item sets, and iPadOS keyboard shortcuts follow the same patterns as macOS (see Standard keyboard shortcuts).
**Anatomy — menu order:** *YourAppName* (short app name) → File → Edit → Format → View → App-specific menus, if any → Window → Help. (macOS also shows the Apple menu on the leading side and menu bar extras on the trailing side.)
- **Support the default system-defined menus and their ordering** — the system implements standard item functionality itself in many cases (e.g., Edit > Copy auto-enables on text selection in a standard text field).
- **Always show the same set of menu items** — disable an unactionable item rather than hide it, so people can learn what your app supports.
- **Represent menu item actions with familiar icons** — same icons as the system for Copy, Share, Delete, etc.
- **Support the keyboard shortcuts defined for standard menu items** (Copy, Cut, Paste, Save, Print); define custom shortcuts only when necessary (see Standard keyboard shortcuts).
- **Prefer short, one-word menu titles** — use title-style capitalization if more than one word is needed.

**App menu** — items in order:
| Menu item | Action | Guidance |
|---|---|---|
| About *YourAppName* | Displays the About window (copyright/version info) | Prefer a short name of 16 characters or fewer; don't include a version number |
| Settings… | Opens your Settings window, or the app's page in iPadOS Settings | Use only for app-level settings; document-specific settings go in the File menu |
| Optional app-specific items | Custom app-level setting/configuration actions | List after the Settings item, in the same group |
| Services (macOS only) | Submenu of services from the system and other apps applicable to the current context | |
| Hide *YourAppName* (macOS only) | Hides the app and its windows, activates the most recently used app | Use the same short app name as the About item |
| Hide Others (macOS only) | Hides all other open apps and windows | |
| Show All (macOS only) | Shows all other open apps/windows behind your app's windows | |
| Quit *YourAppName* | Quits the app; Option changes it to Quit and Keep Windows | Use the same short app name as the About item |

**Display the About menu item first**, with a separator after it so it appears alone in its group.

**File menu** — items in order:
| Menu item | Action | Guidance |
|---|---|---|
| New *Item* | Creates a new document, file, or window | Use a term naming the item type your app creates (e.g., Calendar: *Event*, *Calendar*) |
| Open | Opens the selected item or presents a selection interface | Ellipsis follows if a separate interface is required |
| Open Recent | Submenu of recently opened documents/files, typically with a *Clear Menu* item | List recognizable names, not file paths; most recently opened first |
| Close | Closes the current window/document; Option → Close All; in a tab-based window, Close Tab replaces Close | Consider adding a Close Window item for tab-based windows |
| Close Tab | Closes the current tab; Option → Close Other Tabs | |
| Close File | Closes the current file and all its associated windows | Support if your app can open multiple views of the same file |
| Save | Saves the current document/file | Autosave periodically; for a new document, prompt for name/location; for multiple formats, prefer a pop-up menu in the Save sheet |
| Save All | Saves all open documents | |
| Duplicate | Duplicates the current document, both remain open; Option → Save As | Prefer Duplicate over Save As/Export/Copy To/Save To, which don't clarify the relationship between original and new file |
| Rename… | Changes the current document's name | |
| Move To… | Prompts for a new document location | |
| Export As… | Prompts for name/output location/export format; original stays open, exported file doesn't open | Reserve for exporting to a format your app doesn't typically handle |
| Revert To | With autosave on, submenu of recent document versions plus a version browser option | |
| Page Setup… | Panel for paper size/orientation, savable per document | Include if you support document-specific print parameters |
| Print… | Opens the standard Print panel (printer, fax, or PDF) | |

**Determine whether Find menu items belong in the Edit menu or the File menu** (e.g., if your app searches files/objects, Find may fit better in File).

**Edit menu** — top-level items in order:
| Menu item | Action | Guidance |
|---|---|---|
| Undo | Reverses the previous operation | Clarify the target, e.g. Undo Paste and Match Style, or Undo Typing |
| Redo | Reverses the previous Undo | Clarify the target, e.g. Redo Paste and Match Style, or Redo Typing |
| Cut | Removes selection to the Clipboard, replacing its previous contents | |
| Copy | Duplicates selection to the Clipboard | |
| Paste | Inserts Clipboard contents at the insertion point; Clipboard unchanged (repeatable) | |
| Paste and Match Style | Inserts Clipboard contents, matching surrounding text style | |
| Delete | Removes selection without placing it on the Clipboard | Use Delete, not Erase/Clear — matches Delete key behavior |
| Select All | Highlights all selectable content | |
| Find | Submenu: Find, Find and Replace, Find Next, Find Previous, Use Selection for Find, Jump to Selection | |
| Spelling and Grammar | Submenu: Show Spelling and Grammar, Check Document Now, Check Spelling While Typing, Check Grammar With Spelling, Correct Spelling Automatically | |
| Substitutions | Submenu: Show Substitutions, Smart Copy/Paste, Smart Quotes, Smart Dashes, Smart Links, Data Detectors, Text Replacement | |
| Transformations | Submenu: Make Uppercase, Make Lowercase, Capitalize | |
| Speech | Submenu: Start Speaking, Stop Speaking | |
| Start Dictation | Opens the dictation window, inserts spoken text at the insertion point | System auto-adds at the bottom of the Edit menu |
| Emoji & Symbols | Opens the Character Viewer | System auto-adds at the bottom of the Edit menu |

**Format menu** — top-level items (exclude this menu if you don't support formatted text editing):
| Menu item | Action |
|---|---|
| Font | Submenu: Show Fonts, Bold, Italic, Underline, Bigger, Smaller, Show Colors, Copy Style, Paste Style |
| Text | Submenu: Align Left, Align Center, Justify, Align Right, Writing Direction, Show Ruler, Copy Ruler, Paste Ruler |

**View menu** lets people customize the appearance of all an app's windows.
> Important: The View menu doesn't navigate or manage specific windows — that's the Window menu.
- **Provide a View menu even if your app supports only a subset of standard view functions** (e.g., only Enter/Exit Full Screen if no tab bar/toolbar/sidebar).
- **Ensure each show/hide item title reflects the current state** (Show Toolbar when hidden, Hide Toolbar when visible).

| Menu item | Action |
|---|---|
| Show/Hide Tab Bar | Toggles the tab bar's visibility above the body area in a tab-based window |
| Show All Tabs/Exit Tab Overview | Enters/exits a Mission-Control-like overview of all open tabs |
| Show/Hide Toolbar | Toggles the toolbar's visibility |
| Customize Toolbar | Opens a view to customize toolbar items |
| Show/Hide Sidebar | Toggles the sidebar's visibility |
| Enter/Exit Full Screen | Opens the window at full-screen size in a new space |

**App-specific menus** appear between View and Window.
- **Provide app-specific menus for custom commands** — makes them discoverable, lets you assign keyboard shortcuts, and makes them accessible via Full Keyboard Access; don't exclude infrequent/advanced commands from the menu bar.
- **As much as possible, reflect your app's hierarchy in app-specific menu order** (e.g., Mail lists Mailbox, Message, Format mirroring their containment relationship).
- **Aim to list app-specific menus from most to least general or commonly used.** (People tend to expect menus toward the leading end of the list to be more specialized than menus toward the trailing end.)

**Window menu** lets people navigate, organize, and manage an app's windows.
> Important: The Window menu doesn't customize window appearance (View menu) or close windows (File menu's Close).
- **Provide a Window menu even if your app has only one window** — include Minimize and Zoom so Full Keyboard Access users can invoke them.
- **Consider including items for showing/hiding panels** (no need for the font or text color panel — the Format menu lists those).

| Menu item | Action | Guidance |
|---|---|---|
| Minimize | Minimizes the active window to the Dock; Option → Minimize All | |
| Zoom | Toggles between a predefined size and the window size people set; Option → Zoom All | Avoid using Zoom to enter/exit full-screen mode — that's the View menu's job |
| Show Previous Tab | Shows the tab before the current one | |
| Show Next Tab | Shows the tab after the current one | |
| Move Tab to New Window | Opens the current tab in a new window | |
| Merge All Windows | Combines all open windows into a single tabbed window | |
| Enter/Exit Full Screen | Opens the window at full-screen size in a new space | Include only if your app has no View menu; still provide separate Minimize/Zoom items |
| Bring All to Front | Brings all the app's windows to front, preserving position/size/layering (same as clicking its Dock icon); Option → Arrange in Front (neatly tiled) | |
| *Name of an open app-specific window* | Brings the selected window to front | List open windows alphabetically; avoid listing panels or modal views |

**Help menu** (trailing end of the menu bar) — Help Book format auto-adds a search field at the top.
| Menu item | Action | Guidance |
|---|---|---|
| Send *YourAppName* Feedback to Apple | Opens the Feedback Assistant | |
| *YourAppName* Help | Opens Help Book content in the built-in Help Viewer | |
| *Additional Item* | — | Use a separator between primary help documentation and additional items (e.g., registration info, release notes); keep the total small, or link to extra items from within your help documentation instead |

**Dynamic menu items** change behavior when chosen while pressing a modifier key (Control, Option, Shift, Command) — e.g., Minimize → Minimize All with Option.
- **Avoid making a dynamic menu item the only way to accomplish a task** — hidden by default, best suited as shortcuts to advanced actions achievable another way.
- **Use dynamic menu items primarily in menu bar menus** — avoid in contextual or Dock menus (harder to discover there).
- **Require only a single modifier key to reveal a dynamic menu item** (`isAlternate`) — more than one is physically awkward and less discoverable.
> Tip: macOS automatically sets a menu's width to hold the widest item, including dynamic menu items.
**Platforms:** Not supported in iOS, tvOS, visionOS, or watchOS.
- **iPadOS:** The menu bar shows top-level system-provided and custom menus; revealed by moving the pointer to the top edge or swiping down from it; occupies the same vertical space as the Status bar when visible.

| | iPadOS | macOS |
|---|---|---|
| Menu bar visibility | Hidden until revealed | Visible by default |
| Horizontal alignment | Centered | Leading side |
| Menu bar extras | Not available | System default and custom |
| Window controls | In the menu bar when the app is full screen | Never in the menu bar |
| Apple menu | Not available | Always available |
| App menu | About, Services, and app visibility-related items not available | Always available |

  - **Because the menu bar is often hidden in full screen, ensure people can access all your app's functions through its UI** — always offer alternatives to dynamic-menu-item tasks (available only with a hardware keyboard); avoid using the menu bar as a catch-all for functionality that doesn't fit elsewhere.
  - **Reserve YourAppName > Settings for opening your app's page in iPadOS Settings** — if you have your own internal preferences area, link to it with a separate item beneath Settings in the same group, and place other custom app-wide config options there too.
  - **For apps with tab-style navigation, consider adding each tab as a menu item in the View menu**, optionally with key bindings for faster navigation.
  - **Consider grouping menu items into submenus to conserve vertical space** — iPad menu rows use more space than Mac's for tappability, and screens can be smaller.
- **macOS:** The Apple menu is always first on the leading side, contains always-available system-defined items, and can't be modified or removed. Menu bar extras can appear on the trailing end, space permitting. **When menu bar space is constrained, the system prioritizes menus and essential menu bar extras**, possibly decreasing title spacing or truncating titles. In full-screen mode, the menu bar hides until revealed by moving the pointer to the top of the screen.
  - *Menu bar extras* (`MenuBarExtra`) expose app-specific functionality via an icon in the menu bar while your app is running, even when not frontmost; opposite side of the menu bar from your app's menus. The system may hide extras to make room for app menus, or if there are too many extras.
  - **Consider using a symbol to represent your menu bar extra** — black/clear colors define its shape so the system can recolor it for dark/light menu bars and the selected state; menu bar height is 24 pt.
  - **Display a menu — not a popover — when people click your menu bar extra**, unless the functionality is too complex for a menu.
  - **Let people — not your app — decide whether to put your menu bar extra in the menu bar** — typically via an app settings toggle; consider offering the option during setup for discoverability.
  - **Avoid relying on the presence of menu bar extras** — the system hides/shows them regularly, and you can't predict which others are shown or where.
  - **Consider exposing app-specific functionality other ways too** — e.g., a Dock menu (Control-click) is always available while your app is running, unlike a menu bar extra people can hide.

## Toolbars
Source: https://developer.apple.com/design/human-interface-guidelines/toolbars
A toolbar provides convenient access to frequently used commands, controls, navigation, and search — one or more sets of controls arranged horizontally along the top or bottom edge of a view, grouped into logical sections.
Toolbars act on view content, facilitate navigation, and orient people; they include three content types: the current view's title; navigation controls (back/forward, search fields); and actions/bar items (buttons, menus). In contrast, a Tab bar is specifically for navigating between areas of an app.
- **Choose items deliberately to avoid overcrowding** — define which items move to the overflow menu as the toolbar narrows.
> Note: The system automatically adds an overflow menu in macOS or iPadOS when items no longer fit — don't add one manually, and avoid layouts that cause overflow by default.
- **Add a More menu to contain additional actions** — prioritize less important actions there; include everything you can directly in the toolbar and add this menu only if you really need it.
- **In iPadOS and macOS apps, consider letting people customize the toolbar** with their most common items — especially useful for apps with many items, advanced functionality, or long usage sessions.
- **Reduce the use of toolbar backgrounds and tinted controls** — custom backgrounds/appearances can overlay or interfere with system background effects; use the content layer to inform color/appearance, and a `ScrollEdgeEffectStyle` when needed to distinguish toolbar from content.
- **Avoid applying a similar color to toolbar item labels and content layer backgrounds** — prefer the default monochromatic toolbar appearance if the content layer is already colorful (see Liquid Glass color).
- **Prefer using standard components in a toolbar** — standard buttons/text fields/headers/footers have corner radii concentric with the bar's corners by default; match this in any custom component.
- **Consider temporarily hiding toolbars for a distraction-free experience** — do so contextually, and offer reliable ways to restore hidden elements (see Going full screen; visionOS: Immersive experiences).

**Titles:**
- **Provide a useful title for each window** — helps confirm location and differentiate multiple open windows; leave it empty if redundant (e.g., Notes skips a title for a single open note, since the first line of content already provides context).
- **Don't title windows with your app name** — provides no useful hierarchy information.
- **Write a concise title** — a word or short phrase, kept under 15 characters, to leave room for other controls.

**Navigation:**
- A toolbar with navigation controls sits at the top of a window and often includes a search field for quick navigation (in iOS, sometimes called a navigation bar).
- **Use the standard Back and Close buttons** — standard symbols, no "Back"/"Close" text label; a custom version must still look the same, behave as expected, match your interface, and be implemented consistently throughout your app.

**Actions:**
- **Provide actions that support the main tasks people perform** — prioritize the commands people are most likely to want (often the most frequent, or those mapping to the most important objects).
- **Make sure the meaning of each control is clear** — prefer simple, recognizable symbols over text, except for actions (like "edit") poorly represented by symbols.
- **Prefer system-provided symbols without borders** — familiar, auto-colored/vibrant, and consistent in interaction; borders are unnecessary since the section provides a visible container and the system defines hover/selection appearances automatically.
- **Use the `.prominent` style for key actions such as Done or Submit** — separates and tints the action for a clear focal point; specify only one primary action, on the trailing side of the toolbar.

**Item groupings** — three locations: leading edge, center area, trailing edge.
- **Leading edge:** elements to return to the previous document and show/hide a sidebar sit at the far leading edge, followed by the view title; can include a document menu (standard/app-specific commands affecting the document as a whole, e.g. Duplicate, Rename, Move, Export) next to the title; not customizable, so these items are always available.
- **Center area:** common, useful controls; the view title can appear here if not on the leading edge; in macOS/iPadOS, people can add/remove/rearrange items here if customizable, and items automatically collapse into the system-managed overflow menu as the window shrinks.
- **Trailing edge:** important items that must remain available, buttons opening nearby inspectors, an optional search field, and the More menu (additional items plus toolbar customization); includes a primary action like Done when one exists; items here remain visible at all window sizes.
- **Group toolbar items logically by function and frequency of use** (e.g., Keynote separates presentation-level, playback, and object-insertion commands).
- **Group navigation controls and critical actions like Done, Close, or Save in dedicated, familiar, visually distinct sections.**
- **Keep consistent groupings and placement across platforms** to build familiarity and trust.
- **Minimize the number of groups** — aim for a maximum of three.
- **Keep actions with text labels separate** — an adjacent text-labeled action and symbol action can look like one combined control, and multiple text-labeled buttons' text may run together; add fixed space between them (`UIBarButtonItem.SystemItem.fixedSpace`).
**Platforms:** No additional considerations for tvOS.
- **iOS:** **Prioritize only the most important items for the main toolbar area** (space is limited); create a More menu for additional items. **Use a large title to help orientation** while navigating/scrolling — transitions to a standard title on scroll, back to large at the top (`prefersLargeTitles`).
- **iPadOS:** **Consider combining a toolbar with a tab bar** — they can coexist in the same horizontal space at the top of the view, useful for navigating a few main app areas while keeping the full window width for content.
- **macOS:** The toolbar sits in the frame at the top of a window, below or integrated with the title bar; window titles can display inline with controls, and toolbar items have no bezel. **Make every toolbar item available as a command in the menu bar** — a toolbar can be customized or hidden, so it can't be the only place a command appears (the reverse isn't required — not every menu item needs a toolbar item).
- **visionOS:** The system-provided toolbar appears along the bottom edge of a window, above the window-management controls, in a plane slightly in front of the window along the z-axis. A variable blur in the bar background maintains legibility of toolbar items as content scrolls behind them, anchoring the bar while the window's glass material stays uniform/undivided. You can supply a symbol or text label for each item; looking at a symbol item reveals its text label. **Prefer using a system-provided toolbar** — consistent, familiar, optimized for eye/hand input, and automatically placed correctly relative to its window. **Avoid creating a vertical toolbar** — Tab bars are vertical in visionOS, so a vertical toolbar could confuse people. **Try to prevent windows from resizing below the toolbar's width** — visionOS has no menu bar listing all app actions, so the toolbar must reliably provide access to essential controls at any window size. **If your app can enter a modal state, consider offering contextually relevant toolbar controls**, and reinstate the standard toolbar controls when exiting the modal state. **Avoid using a pull-down menu in a toolbar** — hard to discover, can clutter the interface, and since the toolbar sits at the bottom edge, a pull-down menu might obscure the window controls below it.
- **watchOS:** A toolbar button offers important functionality in a view displaying related content; place buttons in the top corners or along the bottom — if placed above scrolling content, they remain visible as content scrolls under them (`topBarLeading`, `topBarTrailing`, `bottomBar`). You can also place a button in the scrolling view itself, hidden by default until revealed by scrolling up (`primaryAction`) — since people frequently scroll to the top, discovery is automatic. **Use a scrolling toolbar button for an important action that isn't a primary app function** (e.g., Mail's New Message button atop the Inbox, whose primary purpose is displaying a scrollable message list).
