# HIG — Components: navigation/search & presentation
path-controls, search-fields, sidebars, tab-bars, token-fields, action-sheets, alerts, page-controls, panels, popovers, scroll-views, sheets, windows

## Path controls
Source: https://developer.apple.com/design/human-interface-guidelines/path-controls
A path control shows the file system path of a selected file or folder.
- **Use a path control in the window body, not the window frame.** Not intended for toolbars or status bars — e.g., Finder's path bar appears at the bottom of the window body, not in the status bar.
**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## Search fields
Source: https://developer.apple.com/design/human-interface-guidelines/search-fields
A search field lets people search a collection of content for specific terms they enter — an editable text field with a Search icon, Clear button, and placeholder text, optionally paired with scope bars and tokens.
- **Use placeholder text** to reinforce search scope or educate people about searchable content.
- **If possible, start search immediately as a person types** for a more responsive feel.
- **Consider showing suggested search terms** — recent searches before search begins, or predictive suggestions while typing.
- **Simplify search results** — surface the most relevant first; consider categorizing to aid discovery.
- **Consider letting people filter search results**, e.g. a scope bar in the results content area.
- A *scope bar* is a control for filtering and adjusting the scope of a search; a *token* is a visual representation of a search term that people can select and edit, acting as a filter.
- **Use a scope bar to filter among clearly defined search categories** (e.g. Mail moving from entire mailbox to one mailbox).
- **Default to a broader scope and let people refine it as needed.**
- **Use tokens to filter by common search terms or items** (e.g. filtering by a contact or by photos).
- **Consider pairing tokens with search suggestions**, since people may not know which tokens are available.
**Platforms:**
- iOS: three entry points — tab in a tab bar, a toolbar (top or bottom), or inline with content. Search as a tab has two styles: **Standard tab** (uniform with rest of bar; opens a search landing page) — choose to provide suggestions, promote discovery, and encourage exploration; **Button appearance** (separate button; tapping focuses the field and shows the keyboard immediately) — choose to help people quickly find what they need with a transient, resolve-fast experience. **Place search at the bottom of a toolbar if there's room** (keeps it easy to reach); **place at the top when it's important to defer to content at the bottom, or there's no bottom toolbar.** **Place search as an inline field when its position beside the content it searches strengthens that relationship**; when at the top, position it above the list it searches and consider pinning it to the top toolbar when scrolling.
- iPadOS, macOS: keep search experience consistent across both if your app is on both. **Put a search field at the trailing side of the toolbar** for split-view apps searching across multiple columns (Mail, Notes, Voice Memos) or filtering a detail view (Freeform). **Include search at the top of the sidebar** when filtering content/navigation there. **Include search as an item in the sidebar or tab bar** for a dedicated discovery area pairing rich suggestions/categories/content (Music, TV). **In a dedicated search area, consider immediately focusing the field on navigation** — exception: iPad with only a virtual keyboard, where leaving it unfocused avoids unexpectedly covering the view. **Account for window resizing** — search resizes fluidly like Mac; in compact iPad views, place search where contextually useful (e.g. above the content list, as in Notes/Mail).
- tvOS: a search screen is a specialized keyboard screen with fully customizable results beneath it. **Provide suggestions** (popular, context-specific, recent) since people don't want to type much.
- watchOS: tapping the search field shows a full-screen text-input control; the app returns to the search field only after Cancel or Search is tapped.
- No additional considerations for visionOS.

## Sidebars
Source: https://developer.apple.com/design/human-interface-guidelines/sidebars
A sidebar appears on the leading side of a view and lets people navigate between areas of your app or top-level collections of content, like folders and playlists.
Use for large-space navigation; prefer a more compact control such as a tab bar when space is limited or more screen is needed for content — many apps instead adopt a tab-bar style that also converts to a sidebar.
- **Extend visually rich content beneath the sidebar** — sidebars can float above content in the Liquid Glass layer; reinforce separation via horizontal scrolling or a *background extension effect* (mirrors adjacent content to simulate stretching under the sidebar).
- **When possible, let people customize sidebar contents** so they can prioritize the areas most important to them.
- **Group hierarchy with disclosure controls** if there's a lot of content, to keep vertical space manageable.
- **Consider using familiar symbols (SF Symbols)** to represent items; prefer custom symbols over bitmap images for custom icons.
- **Consider letting people hide the sidebar**, using platform-specific interactions (iPadOS edge swipe; macOS show/hide button or View menu commands; visionOS windows typically expand to accommodate a sidebar, so hiding is rarely needed). Avoid hiding it by default — keep it discoverable.
- **In general, show no more than two levels of hierarchy in a sidebar.** For deeper hierarchies, use a split view interface with a content list between sidebar and detail view.
- **If two levels are needed, use succinct, descriptive labels** for each group, omitting unnecessary words.
- **Make sure sidebar icon colors serve a clear purpose.** Icons default to the app's accent color; in macOS people can change the system accent color and expect sidebar icons to follow. Sparingly used fixed colors can clarify meaning or draw attention (e.g. Mail's yellow VIP icon).
**Platforms:**
- iOS, iPadOS: the `sidebarAdaptable` tab-view style lets you choose sidebar or tab bar at launch, with a button to switch between them, adapting to platform and responding to rotation/resizing. (Developer note: for sidebar-only presentation, use `NavigationSplitView` or `UISplitViewController`.) **Consider using a tab bar first** — it offers more room for content and enough flexibility for most apps; if more areas are needed than fit, the tab bar's convertible sidebar-style appearance can expose less-frequently-used content. **If necessary, apply the correct appearance** via `UICollectionLayoutListConfiguration.Appearance.sidebar` when not using SwiftUI.
- macOS: sidebar row height, text, and glyph size depend on an overall size setting (small/medium/large), settable programmatically or by people via General settings. **Consider automatically hiding/revealing the sidebar when its container window resizes.** **Avoid putting critical information or actions at the bottom of a sidebar** — people often relocate windows in ways that hide the bottom edge.
- visionOS: **if your app's hierarchy is deep, consider a sidebar within a tab** for secondary navigation — prevent sidebar selections from changing which tab is open.
- No additional considerations for tvOS. Not supported in watchOS.

## Tab bars
Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars
A tab bar lets people navigate between top-level sections of your app.
Use for navigation, not actions — use a toolbar for controls that act on the current view's elements.
- **Use a tab bar to support navigation, not to provide actions.**
- **Make sure the tab bar is visible when people navigate between sections** — exception: a modal view temporarily covering it is fine.
- **Use the appropriate number of tabs** — weigh complexity against frequency of access; fewer tabs are easier to navigate. Consider a sidebar or sidebar-adaptable tab bar for complex information structures.
- **Avoid overflow tabs.** When horizontal space limits visible tabs, the trailing tab becomes a More tab (iOS/iPadOS) revealing the rest in a list — this hinders discovery, so limit scenarios that trigger it.
- **Don't disable or hide tab bar buttons**, even when content is unavailable — an unstable-looking interface results; instead explain why a section is empty.
- **Include tab labels** — beneath or beside the icon; use single words whenever possible.
- **Consider using SF Symbols** for scalable icons that adapt automatically (icon above label in compact views, side by side in regular views); prefer filled symbols/icons for platform consistency.
- **Use a badge** (a red oval with white text — a number or exclamation point) to indicate critical new/updated information; reserve for critical info to avoid diluting meaning.
- **Avoid applying a similar color to tab labels and content layer backgrounds** — prefer a monochromatic tab bar appearance, or an accent color with sufficient differentiation, if content is already bright/colorful.
**Platforms:**
- iOS: the tab bar floats above content at the bottom on a Liquid Glass background that lets content peek through. Tab bars with an attached accessory (e.g. Music's MiniPlayer) can minimize and move the accessory inline when scrolling down; exit the minimized state by tapping a tab or scrolling to the top. Can include a dedicated search tab at the trailing end.
- iPadOS: displays near the top of the screen, either fixed or with a button converting it to a sidebar. (Note: to present a sidebar without conversion, use a navigation split view instead of a tab view.) **Prefer a tab bar for navigation**; provide the option to convert to a sidebar for wider navigation in complex apps. **Let people customize the tab bar** — select frequently-used items to add/remove; if customizable, aim for a default list of five or fewer to preserve continuity across compact/regular sizes.
- tvOS: highly customizable — tint/color/image for background, per-item font (including selected item), tints for selected/unselected items, button icons (settings, search). Translucent by default with only the selected tab opaque; the focused selected tab shows a drop shadow. Height is 68 points, top edge 46 points from the top of the screen (fixed values). Overflow items are truncated with a fade effect from the right (and from the left too, if scrollable). **Be aware of tab bar scrolling behaviors** — by default the tab bar scrolls offscreen when the current tab has a single main view (e.g. TV app's Watch Now/Movies/TV Show/Sports/Kids tabs); exception: screens containing a split view (e.g. Library tab, Settings) keep the tab bar pinned at the top while content scrolls. Focus always returns to the tab bar on Menu press. **In a live-viewing app, organize tabs consistently**: live content, then Cloud DVR/recorded content, then other content.
- visionOS: always vertical, floats fixed relative to the window's leading side; automatically expands when looked at, opened by looking + tapping; can temporarily obscure content behind it while expanded. **Supply a symbol and a text label for each tab** — the symbol is always visible, labels reveal on look; keep labels short. **Consider using a sidebar within a tab** if hierarchy is deep, for secondary navigation — prevent sidebar selections from changing the open tab.
- No additional considerations for macOS. Not supported in watchOS.

## Token fields
Source: https://developer.apple.com/design/human-interface-guidelines/token-fields
A token field is a type of text field that can convert text into tokens that are easy to select and manipulate (e.g. Mail's compose-window address fields).
- **Add value with a context menu** offering additional options or information about a token.
- **Consider providing additional ways to convert text into tokens** — by default, typing a comma converts text; add shortcuts like Return.
- **Consider customizing the delay before showing suggested tokens** — suggestions appear immediately by default, but too-fast suggestions can distract while typing.
**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, and watchOS.

## Action sheets
Source: https://developer.apple.com/design/human-interface-guidelines/action-sheets
An action sheet is a modal view that presents choices related to an action people initiate.
Use for choices related to an intentional action; use an alert instead for unexpected problems or confirmations without additional choices.
> Developer note: SwiftUI's confirmation dialog presentation modifier offers action sheet functionality on all platforms; UIKit uses `UIAlertController.Style.actionSheet` for iOS, iPadOS, and tvOS.
- **Use an action sheet — not an alert — to offer choices related to an intentional action.** An alert is usually unexpected and doesn't provide additional choices related to the action.
- **Use action sheets sparingly** — they interrupt the current task.
- **Aim to keep titles short enough to display on a single line.**
- **Provide a message only if necessary** — title plus context is usually enough.
- **If necessary, provide a Cancel button** to reject a potentially destructive action — place it at the bottom of the sheet (upper-left corner in watchOS). SwiftUI confirmation dialogs include Cancel by default.
- **Make destructive choices visually prominent** — use the destructive style and place these buttons at the top of the action sheet, where they're most noticeable.
**Platforms:**
- iOS, iPadOS: **Use an action sheet — not a menu — for action-related choices**; people expect an action sheet after performing an action, and a menu only when they choose to reveal it. **Avoid letting an action sheet scroll** — more buttons take more effort to choose among, and scrolling risks inadvertent taps.
- watchOS: system style includes a title, optional message, Cancel button, and one or more additional buttons (appearance varies by device). Three system-defined button styles:

| Style | Meaning |
| --- | --- |
| Default | The button has no special meaning. |
| Destructive | The button destroys user data or performs a destructive action in the app. |
| Cancel | The button dismisses the view without taking any action. |

  **Avoid displaying more than four buttons including Cancel** — aim for no more than three additional choices, so people can view all options at once.
- No additional considerations for macOS or tvOS. Not supported in visionOS.

## Alerts
Source: https://developer.apple.com/design/human-interface-guidelines/alerts
An alert gives people critical information they need right away — a modal view that can look different across platforms and devices.
- **Use alerts sparingly** — make certain each one offers only essential information and useful actions.
- **Avoid using an alert merely to provide information** — prefer an alternative way to communicate non-actionable info in context (e.g. Mail's server-connection indicator).
- **Avoid displaying alerts for common, undoable actions, even when destructive** — reserve alerts for uncommon, non-undoable destructive actions people might have triggered accidentally.
- **Avoid showing an alert when your app starts** — make important info discoverable another way (e.g. cached/placeholder data plus a nonintrusive label describing the problem).

**Content:** In all platforms, an alert displays a title, optional informative text, and up to three buttons.
- iOS, iPadOS, macOS, visionOS: can include a text field.
- macOS, visionOS: can include an icon and an accessory view.
- macOS: can add a suppression checkbox and a Help button.
- **Be direct, and use a neutral, approachable tone** in all alert copy — avoid being oblique, accusatory, or masking severity.
- **Write a title that clearly and succinctly describes the situation** — describe what happened, its context, and why, without being verbose. Avoid uninformative titles ("Error," "Error 329347 occurred") and titles wrapping past two lines. Use sentence-style capitalization and ending punctuation if the title is a complete sentence; title-style capitalization and no ending punctuation if it's a fragment.
- **Include informative text only if it adds value** — keep it short, use complete sentences, sentence-style capitalization, and appropriate punctuation.
- **Avoid explaining alert buttons** if the text and titles are already clear; if guidance is needed, use a term like *choose* and refer to a button by its exact title without quotes.
- **If supported, include a text field only if you need people's input** to resolve the situation (e.g. a secure text field for a password).

**Buttons:**
- **Create succinct, logical button titles** — aim for one or two words describing the result (e.g. "View All," "Reply," "Ignore"); "OK" is acceptable only in purely informational alerts (avoid "Yes"/"No"); always use "Cancel" to cancel the alert's action; sentence-style capitalization, no ending punctuation.
- **Avoid using OK as the default button title unless the alert is purely informational** — its meaning can be ambiguous; use a specific title like "Erase," "Convert," "Clear," or "Delete" instead.
- **Place buttons where people expect** — the most likely choice goes on the trailing side of a row or at the top of a stack; always place the default button on the trailing side/top. Cancel buttons are typically on the leading side of a row or at the bottom of a stack.
- **Use the destructive style to identify a button that performs a destructive action people didn't deliberately choose.** When people deliberately choose a destructive action (e.g. Empty Trash), the resulting confirm button is not styled destructive, since it performs their original intent — the convenience of pressing Return outweighs reaffirming destructiveness there.
- **If there's a destructive action, include a Cancel button.** Always title it "Cancel." Never make Cancel the default button. To encourage people to actually read the alert rather than reflexively press Return, avoid making any button the default. If a single default button must be shown, use "Done," not "Cancel."
- **Provide alternative ways to cancel an alert:**

| Action | Platform |
| --- | --- |
| Exit to the Home Screen | iOS, iPadOS |
| Pressing Escape (Esc) or Command-Period (.) on an attached keyboard | iOS, iPadOS, macOS, visionOS |
| Pressing Menu on the remote | tvOS |

**Platforms:**
- iOS, iPadOS: **Use an action sheet — not an alert — to offer choices related to an intentional action** (e.g. Mail's cancel-edit action sheet offers delete edits/draft, save draft, or return to editing). **When possible, avoid displaying an alert that scrolls** — keep titles short and messages brief.
- macOS: automatically shows the app icon in an alert (a custom icon/symbol can be supplied instead); also supports configuring repeating alerts with suppression, appending a custom accessory view (`accessoryView`), and including a Help button. **Use a caution symbol (`exclamationmark.triangle`) sparingly** — only when extra attention is truly needed (e.g. confirming an action risking unexpected data loss); don't use it for tasks whose only purpose is to overwrite/remove data (save, empty trash).
- visionOS: in the Shared Space, the alert displays in front of the app's window, slightly forward on the z-axis, and stays anchored to the window if moved; in a Full Space, it's centered in the wearer's field of view. An accessory view must have a maximum height of 154 pt and a 16-pt corner radius.
- No additional considerations for tvOS or watchOS.

## Page controls
Source: https://developer.apple.com/design/human-interface-guidelines/page-controls
A page control displays a row of indicator images, each representing a page in a flat list; a solid dot denotes the current page.
Use for movement between an ordered list of pages, not for hierarchical or nonsequential relationships — consider a sidebar or split view for more complex navigation.
- **Use page controls to represent movement between an ordered list of pages** only.
- **Center a page control at the bottom of the view or window** so people always know where to find it.
- **Don't display too many dots** — more than about 10 are hard to count at a glance; consider a grid or other arrangement instead for more than ~10 peer pages.
- **Make custom indicator images simple and clear** — avoid complex shapes, negative space, text, or inner lines, which become muddy at small sizes.
- **Customize the default indicator image only when it enhances the page control's overall meaning** (e.g. `bookmark.fill` if every page lists bookmarks).
- **Avoid using more than two different indicator images** in a page control — more becomes hard to memorize and looks messy.
- **Avoid coloring indicator images** — let the system automatically color them to preserve contrast between the current-page indicator and the background.
**Platforms:**
- iOS, iPadOS: can highlight the current-page indicator and shrink indicators at both sides when more exist than fit. Tapping (a *discrete interaction*) the leading/trailing side of the current indicator reveals the next/previous page; iPadOS pointer can target a specific indicator. Scrubbing (a *continuous interaction* — touch and drag) opens pages in sequence, and scrubbing past an edge quickly reaches the first/last page. **Avoid animating page transitions during scrubbing** — use the animated scrolling transition only for tapping, since scrubbing can be fast and cause lag/visual flashes. Background styles: **Automatic** — shows background only on interaction; use when the page control isn't the primary navigational element. **Prominent** — always shows background; use only when the control is the screen's primary navigational control. **Minimal** — never shows background; use when you just want to show current-page position without scrub feedback. **Avoid supporting the scrubber with the minimal background style** — it gives no visual feedback during scrubbing; use automatic or prominent instead.
- tvOS: **use page controls on collections of full-screen pages** that are peers in the page hierarchy; avoid additional controls, which make it hard to maintain focus while moving between pages.
- visionOS: page controls represent and indicate available pages, but people don't interact with them.
- watchOS: can appear at the bottom for horizontal pagination, or next to the Digital Crown for a vertical tab view (showing position within the current page and within the page set; transitions between scrolling a page's content and scrolling to other pages). **Use vertical pagination to separate views into distinct, purposeful pages** — more effective in watchOS than horizontal pagination or deep hierarchical navigation. **Consider limiting an individual page's content to a single screen height** for a more glanceable design; use variable-height pages judiciously, placing them after fixed-height pages where possible.
Not supported in macOS.

## Panels
Source: https://developer.apple.com/design/human-interface-guidelines/panels
In a macOS app, a panel typically floats above other open windows, providing supplementary controls, options, or information related to the active window or current selection.
Use for macOS supplementary controls; on other platforms, use a modal view instead (see Modality).
- **Use a panel to give quick access to important controls or information** related to the content being worked with.
- **Consider using a panel to present inspector functionality** — an inspector auto-updates to show details of the current selection. Use a regular window instead for an *Info* window that always shows the same content regardless of selection; depending on layout, a split-view pane can also present an inspector.
- **Prefer simple adjustment controls in a panel** — avoid controls requiring typing or item selection (multi-step); prefer sliders and steppers for more direct control.
- **Write a brief title that describes the panel's purpose** — a short noun or noun phrase in title-style capitalization (e.g. "Fonts," "Colors," "Inspector"), since the panel needs a title bar for repositioning.
- **Show and hide panels appropriately** — bring all open panels to the front when your app becomes active (regardless of which window was active when it opened); hide all panels when the app is inactive.
- **Avoid including panels in the Window menu's documents list** — commands to show/hide panels are fine in the Window menu, but panels aren't documents or standard app windows.
- **In general, avoid making a panel's minimize button available** — panels display only when needed and disappear when the app is inactive.
- **Refer to panels by title** in interface and help documentation — omit the term "panel" in menus (e.g. "Show Fonts," "Show Colors," "Show Inspector"). In help docs, refer by title alone, or append "window" for clarity ("Fonts window," "Colors window") where "Inspector" alone may already be clear enough.

**HUD-style panels:** A HUD-style panel serves the same function as a standard panel but with a darker, translucent appearance; works well for media-oriented or immersive apps (e.g. QuickTime Player's inspector HUD).
- **Prefer standard panels.** Use a HUD only: in a media-oriented app presenting movies/photos/slides; when a standard panel would obscure essential content; or when no controls are needed beyond a disclosure triangle (most system controls don't match a HUD's appearance).
- **Maintain one panel style when your app switches modes** (e.g. keep the HUD style if used in full-screen mode, even after leaving full screen).
- **Use color sparingly in HUDs** — small amounts of high-contrast color to highlight important information.
- **Keep HUDs small** — don't let them obscure the content they adjust or compete with it for attention.
**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## Popovers
Source: https://developer.apple.com/design/human-interface-guidelines/popovers
A popover is a transient view that appears above other content when people click or tap a control or interactive area.
- **Use a popover to expose a small amount of information or functionality** — limit content to a few related tasks, since it disappears after interaction.
- **Consider using popovers when you want more room for content** — sidebars/panels take a lot of space; a popover streamlines the interface for temporary content.
- **Position popovers appropriately** — the arrow should point as directly as possible to the revealing element; ideally the popover doesn't cover that element or other essential content.
- **Use a Close button for confirmation and guidance only** (e.g. Cancel/Done for exiting with or without saving). Otherwise a popover closes on click/tap outside its bounds or on selecting an item; if multiple selections are possible, keep it open until explicitly dismissed or clicked/tapped outside.
- **Always save work when automatically closing a nonmodal popover** — discard work only via an explicit Cancel button, since people can unintentionally dismiss it by clicking/tapping outside.
- **Show one popover at a time** — never a cascade or hierarchy of popovers; close the open one before showing a new one.
- **Don't show another view over a popover** — nothing should display on top of a popover except an alert.
- **When possible, let people close one popover and open another with a single click or tap**, especially when several bar buttons each open a popover.
- **Avoid making a popover too big** — only as big as needed for its content and to point to its origin; the system can adjust its size to fit the interface.
- **Provide a smooth transition when changing a popover's size** — animate the change so it doesn't look like a new popover replaced the old one.
- **Avoid using the word "popover" in help documentation** — refer to the specific task or selection instead.
- **Avoid using a popover to show a warning** — people can miss or accidentally close it; use an alert instead.
**Platforms:**
- iOS, iPadOS: **Avoid displaying popovers in compact views** — adjust layout dynamically by size class; reserve popovers for wide views, and use a full-screen modal (e.g. a sheet) for compact views.
- macOS: popovers can be made detachable, becoming a separate panel when dragged that remains visible while people interact with other content. **Consider letting people detach a popover.** **Make minimal appearance changes to a detached popover** so people maintain context.
- No additional considerations for visionOS. Not supported in tvOS or watchOS.

## Scroll views
Source: https://developer.apple.com/design/human-interface-guidelines/scroll-views
A scroll view lets people view content that's larger than the view's boundaries by moving the content vertically or horizontally.
The scroll view itself has no appearance, but can display a translucent scroll indicator (typically appearing after scrolling begins) showing whether visible content is near the beginning, middle, or end.
- **Support default scrolling gestures and keyboard shortcuts** — if building custom scrolling, ensure scroll indicators use the expected elastic behavior.
- **Make it apparent when content is scrollable** — e.g. show partial content at a view's edge to indicate more content in that direction.
- **Avoid putting a scroll view inside another scroll view with the same orientation** — creates an unpredictable, hard-to-control interface. It's fine to nest a horizontal scroll view inside a vertical one, or vice versa.
- **Consider supporting page-by-page scrolling** if it fits your content — define a page (typically the view's current height/width) and an interaction that scrolls one page at a time; optionally define a unit of overlap (a line of text, row of glyphs, part of a picture) subtracted from the page size to maintain context (`PagingScrollTargetBehavior`).
- **In some cases, scroll automatically to help people find their place** — e.g. when an operation selects content or places the insertion point somewhere hidden (scroll the new selection into view); when people start entering info in a non-visible location (scroll back to the insertion point as they begin typing); when the pointer moves past a view's edge during a selection (follow the pointer by scrolling); or when people select something and scroll elsewhere before acting on it (scroll the selection into view before performing the operation). In all cases, scroll only as much as necessary to retain context.
- **If you support zoom, set appropriate maximum and minimum scale values** (e.g. don't let zoom make a single character fill the screen).

**Scroll edge effects** (iOS, iPadOS, macOS): a *scroll edge effect* visually separates elements like toolbars from the scrolling content behind them.
- **Prefer the automatic scroll edge effect style** — provides more opaque separation for top toolbars with many controls, text outside Liquid Glass controls, and pinned table headers. If using the soft style instead, thoroughly test legibility across contexts.
- **Only use a scroll edge effect when a scroll view is behind floating interface elements** — it's not decorative, doesn't block/darken like an overlay; it exists purely to keep controls visually distinct.
- **Apply one scroll edge effect per view** — in split-view layouts, each pane can have its own; keep their heights consistent for alignment.
**Platforms:**
- iOS, iPadOS: **Consider showing a page control when a scroll view is in page-by-page mode**; don't show a scroll indicator on the same axis as the page control to avoid redundant controls.
- macOS: a scroll indicator is commonly called a *scroll bar*. **If necessary, use small or mini scroll bars in a panel** where space is tight — use the same size for all controls in such a panel.
- tvOS: views scroll but aren't distinct objects with scroll indicators; the system automatically scrolls to keep focused items visible.
- visionOS: the scroll indicator has a small, fixed size and appears in a predictable location — vertically centered at the trailing edge during vertical scrolling, horizontally centered at the bottom edge during horizontal scrolling. It appears at the window edge as swiping begins, reinforcing the gesture and showing position/length. Looking at the indicator and beginning a drag gesture enables a *jog bar* experience (manipulating scroll speed instead of content position), revealing tick marks that speed up/slow down with small gesture adjustments. **If necessary, account for the size of the scroll indicator** — slightly thicker than iOS's — by increasing tight margins to prevent overlap.
  - *Look to Scroll*: scrolling using only the eyes, starting when people look near the scroll view's boundary (top/bottom for vertical, sides for horizontal); works alongside existing gesture-based scrolling. **Support Look to Scroll for reading or browsing views** (must be added per view; doesn't work by default). **Avoid using Look to Scroll for secondary content** — support standard gestures instead for views with UI controls or dense info needing quick, precise scrolling. **Maintain consistency across content** — support it for all similar views if used for one. **Define clear scroll areas** — prefer full window width/height for generous scroll space and clear edges; if inset, provide clear boundaries. **Remove custom scroll effects or animations** (e.g. parallax) before supporting Look to Scroll, as they can cause unexpected behavior.
- watchOS: **Prefer vertically scrolling content** — the Digital Crown scrolls vertically when content is taller than the display. **Use tab views to provide page-by-page scrolling** — in a vertical stack, the Digital Crown moves through full-screen pages, with a page indicator next to the Crown showing position within the page and page set. **When displaying paged content, consider limiting an individual page to a single screen height** for a more glanceable design — use variable-height pages judiciously, placed after fixed-height pages; the page indicator expands into a scroll indicator when a page needs to scroll.

## Sheets
Source: https://developer.apple.com/design/human-interface-guidelines/sheets
A sheet helps people perform a scoped task that's closely related to their current context (e.g. attaching a file or choosing a save location).
**Anatomy:** In macOS, tvOS, visionOS, and watchOS, a sheet is always *modal*, preventing interaction with the parent view until dismissed. In iOS and iPadOS, a sheet can be modal or *nonmodal* — a nonmodal sheet lets people use its functionality to affect the parent view without dismissing it (e.g. Notes' formatting sheet).
Common buttons: **Cancel** (or Close) dismisses without saving changes; **Done** dismisses after completing/saving; **Back** navigates to a previous step or parent view (not intended to dismiss the sheet). Placement varies by platform.
- **For complex or prolonged user flows, consider alternatives to sheets** — iOS/iPadOS full-screen modal style (`UIModalPresentationStyle.fullScreen`) for video/photo/camera content or multistep tasks; in macOS, a new window or full-screen mode (self-contained tasks like document editing suit a separate window; media viewing suits full screen); in visionOS, transition to a Full Space for content/task immersion.
- **Display only one sheet at a time from the main interface** — closing a sheet should return to the parent view/window; if an action within a sheet triggers another sheet, close the first before showing the new one (you can redisplay the first after the second is dismissed).
- **Use a nonmodal view to present supplementary items that affect the main task in the parent view** — Split views in visionOS, Panels in macOS, or a nonmodal sheet in iOS/iPadOS.
- **Provide an alternative to the Done button** — always pair it with Cancel (dismiss without saving) or Back (previous step); relying solely on Done implies completing the task is the only way to exit.
- **Avoid showing all three buttons — Cancel, Done, and Back — together.**
**Platforms:**
- iOS, iPadOS: for single-view sheets, Cancel belongs on the leading edge of the top toolbar, Done (when present) on the trailing edge; for multi-step flows, button placement can vary across steps. A resizable sheet expands via scrolling its contents or dragging the *grabber* (small horizontal indicator at the top edge). *Detents* are particular heights at which a sheet naturally rests — the system defines **large** (fully expanded) and **medium** (about half of fully expanded). Sheets automatically support the large detent; adding medium allows resting at both heights, while specifying only medium prevents expanding to full height. **Consider supporting the medium detent** for progressive disclosure (e.g. a share sheet showing relevant items at medium, expandable for more) — but not if the content is more useful at full height (e.g. Messages/Mail compose sheets display only at full height). **Include a grabber in a resizable sheet** — shows resizability, lets people tap to cycle detents, and works with VoiceOver. **Support swiping to dismiss a sheet** — if there are unsaved changes, use an action sheet to confirm on swipe-dismiss. **Prefer the page or form sheet presentation styles in an iPadOS app** — each uses a default size, centering content on a dimmed background for a consistent experience.
- macOS: a sheet is a cardlike view with rounded corners floating on top of the parent window, which dims to signal it can't be interacted with until dismissed — though people expect to interact with *other* app windows before dismissing the sheet. **Present a sheet in a reasonable default size** — resizing isn't generally expected, but support it when appreciated (e.g. to expand for a clearer view). **Let people interact with other app windows without first dismissing a sheet** — bring the parent window (and its modeless document-related panels, if a document window) forward when the sheet opens; ensure other app windows can still be brought forward. **Use a panel instead of a sheet if people need to repeatedly provide input and observe results** (e.g. a find-and-replace panel).
- visionOS: a sheet floats in front of the parent window, dimming it and becoming the target of interaction. **Avoid displaying a sheet that emerges from the bottom edge of a window** — prefer centering it in the person's field of view. **Present a sheet in a default size that helps people retain context** — avoid covering most/all of the window; consider letting people resize it.
- watchOS: a sheet is a full-screen view sliding over current content, semitransparent, with a material that blurs/desaturates the covered content. **Use a sheet only when your modal task requires a custom title or custom content presentation** — otherwise consider an alert or action sheet. **Keep sheet interactions brief and occasional** — a temporary interruption for an important task, not for navigating app content. **If you change the default label, prefer SF Symbols to represent the action** — avoid text resembling a hierarchical nav title, or people won't know how to dismiss the sheet.
- No additional considerations for tvOS.

## Windows
Source: https://developer.apple.com/design/human-interface-guidelines/windows
A window presents UI views and components in your app or game. In iPadOS, macOS, and visionOS, windows define the visual boundaries of app content, separate it from other system areas, and enable multitasking within and between apps, with system-provided frames and controls to open/close/resize/relocate them.
Two conceptual types: a *primary* window presents an app's main navigation, content, and associated actions; an *auxiliary* window is dedicated to one specific task/area, doesn't allow navigation to other app areas, and typically includes a close button.
- **Make sure windows adapt fluidly to different sizes** to support multitasking and multiwindow workflows.
- **Choose the right moment to open a new window** — good for multitasking/preserving context (e.g. Mail's Compose opens a new window so the new message and existing email are both visible), but avoid opening new windows excessively or as default behavior unless it fits your app.
- **Consider providing the option to view content in a new window**, e.g. via a context-menu or File-menu command, while avoiding making new-window opening the default behavior unless beneficial.
- **Avoid creating custom window UI** — system-provided windows are recognized and understood; imperfect custom frames/controls can make an app feel broken.
- **Use the term "window" in user-facing content** — the system refers to app windows as windows regardless of type; other terms like "scene" (an implementation term) are likely to confuse people.
**Platforms:**
- iPadOS: windows present as **Full screen** (fill the entire screen; switch via the app switcher) or **Windowed** (freely resizable, repositionable, brought to front; system remembers size/placement even after the app closes), per the person's Multitasking & Gestures settings. **Make sure window controls don't overlap toolbar items** — in windowed mode, window controls appear at the leading edge of the toolbar, so move leading-edge toolbar buttons inward instead of placing them directly there. **Consider letting people use a gesture to open content in a new window** (e.g. pinch to expand a Notes item into a new window). > Tip: to let people view just one file, you can present it without creating your own window, but you must support multiple windows in your app (`QLPreviewSceneActivationConfiguration`).
- macOS: people typically run several apps simultaneously, viewing/switching windows across apps on one desktop.
  - *Window anatomy*: the *frame* appears above the body area and can include window controls and a toolbar (rarely, also a bottom bar below body content); people move a window by dragging the frame and resize by dragging its edges.
  - *Window states*: **Main** — the frontmost window a person views; only one per app. **Key** (active window) — accepts input; only one onscreen at a time; usually the front app's main window, but a floating panel might be key instead; clicking a window makes it key, and clicking a Dock icon to bring an app's windows forward makes only the most-recently-accessed window key. **Inactive** — not in the foreground. (Note: some windows, like Colors/Fonts panels, become key only when clicking the title bar or a component requiring keyboard input.) The system gives main/key/inactive windows different appearances (color vs. gray window-control icons; inactive windows don't use Materials, appearing subdued/farther away).
  - **Make sure custom windows use system-defined appearances** — system-provided components auto-update background/button appearance on state change; custom implementations must replicate this.
  - **Avoid putting critical information or actions in a bottom bar** — people often relocate windows in ways that hide the bottom edge. If used, keep it to a small amount of info related to window content or selection (e.g. Finder's status bar showing item/selection counts and disk space); for more info, consider an inspector (typically on the trailing side of a split view).
- visionOS: two main window styles — **default** (a *window*) and **volumetric** (a *volume*) — both can display 2D and 3D content, viewable simultaneously in the Shared Space and a Full Space. (Note: visionOS also defines the *plain* window style, like default but without the glass background on the upright plane.) The system defines the initial position of the first window/volume opened; people can move them afterward.
  - *Windows*: the default style is an upright plane with an unmodifiable glass background material, close button, window bar, and resize controls; can include a Share button, tab bars, toolbars, and ornaments; uses dynamic scale by default so size appears consistent regardless of viewer proximity. **Prefer using a window** for a familiar interface/familiar tasks, reserving immersive experiences for meaningful content — use a volume for bounded 3D content like a game board. **Retain the window's glass background** — helps content feel part of the surroundings and adapts to lighting via specular reflections/shadows communicating scale/position; removing it reduces legibility, and an opaque background feels constricting. **Choose an initial window size that minimizes empty areas** — default window measures 1280×720 pt, opening ~2 meters in front of the wearer (apparent width ~3 meters); too much empty space looks unnecessarily large and obscures other content. **Aim for an initial shape that suits the content** (e.g. a wide Keynote window for wide slides, a tall Safari window for long webpages; a tower-building game taller than a driving game). **Choose a minimum and maximum size for each window** — without them, people could shrink it until UI overlaps or enlarge it until the app becomes unusable. **Minimize the depth of 3D content displayed in a window** — the system clips content that extends too far from the window's surface; use a volume for content needing greater depth.
  - *Volumes*: display 2D or 3D content viewable from any angle; include window-management controls like a window, but the close button/window bar shift to face the viewer as they move around it. **Prefer a volume for rich 3D content** (use a window instead for a familiar, UI-centric interface). **Place 2D content so it looks good from multiple angles** — use an attachment to pin 2D content to specific areas of 3D content inside a volume, since perspective changes as the viewer moves. **In general, use dynamic scaling** to keep content legible/interactable even far from the viewer; use fixed scaling (the default) if content should represent a real-world object (e.g. a retail product). **Take advantage of the default baseplate appearance** — visionOS 2+ automatically shows a glow around a volume's floor/baseplate border when looked at, helping people discern edges (useful for finding the resize control) unless content is full bleed/fills the bounds or uses a custom baseplate. **Consider offering high-value content in an ornament** (visionOS 2+) — a volume can include an ornament plus a toolbar and tab bar to reduce clutter and elevate important content; an attachment anchor (e.g. `topBack`, `bottomFront`) keeps the ornament in the same relative position as the viewer moves; avoid placing an ornament on the same edge as a toolbar/tab bar, and prefer only one additional ornament. **Choose an alignment that supports how people interact with your volume** — a baseplate that stays parallel to the floor works well for content people don't interact with much, while one that tilts to match the viewer's angle keeps content usable even when reclining.
- Not supported in iOS, tvOS, or watchOS.
