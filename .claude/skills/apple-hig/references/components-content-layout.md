# HIG — Components: content & layout/organization
charts, image-views, text-views, web-views, boxes, collections, column-views, disclosure-controls, labels, lists-and-tables, lockups, outline-views, split-views, tab-views

## Charts
Source: https://developer.apple.com/design/human-interface-guidelines/charts
Organize data in a chart to communicate information with clarity and visual appeal — a chart highlights a few key pieces of information in a dataset to help people gain insights and make decisions.

**Anatomy:** a *mark* visually represents a data value (bar, line, point, etc.); the process of depicting values is *plotting*, and the area containing marks is the *plot area*. A *scale* maps data values (numbers, dates, categories) to visual attributes (position, color, height). An *axis* defines a frame of reference (commonly one horizontal + one vertical); axes can include *ticks* (reference points) and charts often show *grid lines* extending from ticks across the plot area. Descriptive content includes *labels* (name axes/grid lines/ticks/marks), *accessibility labels*, titles/subtitles/annotations, and a *legend* (for non-positional properties like color or shape).

- **Marks: choose a mark type based on the information you want to communicate.** *Bar* marks suit comparing categories or relative proportions of a whole (work well for sums, e.g., total daily steps). *Line* marks show change over time via slope, revealing trends. *Point* marks depict individual values distinctly, useful for showing relationships between two properties and spotting outliers/clusters.
- **Consider combining mark types** (e.g., points atop a line) when it adds clarity — helps show overall trend while highlighting individual data points.
- **Use a fixed or dynamic axis range depending on the meaning of the chart.** Fixed range: bounds never change (e.g., battery charge 0–100%). Dynamic range: bounds vary with current data so marks fill the plot area (e.g., Health Steps chart Y-axis upper bound).
- **Define the lower bound based on mark type and usage.** Bar charts often work well with a zero lower bound for easy relative-height comparison; but a zero lower bound can obscure meaningful differences far from zero (e.g., heart rate).
- **Prefer familiar sequences of values in tick and grid-line labels** (e.g., 0, 5, 10…) over uncommon sequences (e.g., 1, 6, 11…) that require extra thought.
- **Tailor the density/visual weight of grid lines and labels to the chart's use cases** — too many overwhelm, too few make estimating values hard; consider context, supported interactions, and tasks (e.g., fewer grid lines and light label colors if people can inspect points interactively).
- **Write descriptions that help people understand what a chart does before they view it** — information-rich titles/labels are especially important for VoiceOver users and people with cognitive disabilities.
- **Summarize the main message of the chart** so people can grasp the key takeaway quickly, without needing to examine details.
- **Establish a consistent visual hierarchy** — data should generally be most prominent; descriptions and axes provide context without competing with it.
- **In a compact environment, maximize the plot area width** — keep vertical-axis labels as short as possible without losing clarity; consider describing units elsewhere (e.g., a title) and placing longer axis labels (e.g., category names) inside the plot area when it doesn't obscure data.
- **Make every chart fully accessible** — support VoiceOver; supply accessibility labels for chart components; consider Audio Graphs (constructs tones representing data values/trend, plus optional text summaries).
- **Let people interact with data when it makes sense, but don't require interaction to reveal critical information.**
- **Make it easy for everyone to interact with a chart** — if marks are too small to target, consider expanding the hit target to the entire plot area so people can scrub across it.
- **Make an interactive chart easy to navigate via keyboard/full keyboard access/Switch Control** — default linear traversal order is often fine; for custom order use accessibility APIs (e.g., `accessibilityRespondsToUserInteraction(_:)`) to define a logical path (e.g., navigate along X axis); for very large datasets, let focus move among subsets of values instead of all individual points.
- **Help people notice important changes in a chart** — animate changes, but also signal them another way so VoiceOver users and people with animations off are aware (see `UIAccessibility.Notification` / `NSAccessibility.Notification`).
- **Align a chart with surrounding interface elements** — e.g., align leading edge with other views; display vertical grid-line labels on their trailing side to keep a clean leading edge; consider shifting the Y axis to the trailing side so tick labels don't protrude past the leading edge; use a tick to anchor an otherwise-unassociated label to a grid line.
- **Avoid relying solely on color to differentiate data or communicate essential information** — supplement with shapes or patterns (e.g., Health uses two point-mark shapes for blood-pressure components).
- **Add visual separation between contiguous areas of color** (e.g., separators between stacked bar-chart marks) to help distinguish them.
- **Consider using Audio Graphs** to give VoiceOver users more chart information; customize with a chart title and descriptive summary; without Audio Graphs, provide an overview identifying chart type, what each axis represents, and axis bounds.
> Important: Unlike an image (one descriptive label), a chart often needs an accessibility label per important/interactive element — decide whether to describe each mark or groups of marks, or in some cases use one succinct high-level label (e.g., a small chart inside a button that reveals a detailed version).
- Accessibility-label writing guidelines: **prioritize clarity and comprehensiveness** (include context like date/location, don't repeat info available elsewhere); **avoid subjective terms** (e.g., "rapidly," "gradually," "almost") — use actual values; **maximize clarity, avoid ambiguous formats/abbreviations** ("June 6" not "6/6," "60 minutes" not "60m"); **describe what details represent, not what they look like** (identify what a color-coded series means, not the color itself); **be consistent when referring to a specific axis** (e.g., always mention the X axis first).
- **Hide visible text labels for axes and ticks from assistive technologies** — VoiceOver users get values/trends via accessibility labels and Audio Graphs instead.

**Platforms:**
- watchOS: avoid requiring complex chart interactions; prefer glanceable info and simple interactions; if a companion app exists on another platform, use it for more detail/interaction (e.g., Heart Rate app vs. iPhone Health).
- No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS.

## Image views
Source: https://developer.apple.com/design/human-interface-guidelines/image-views
An image view displays a single image — or in some cases an animated sequence of images — on a transparent or opaque background; content can be stretched, scaled, sized to fit, or pinned, and image views are typically not interactive.

- **Use an image view when the primary purpose of the view is simply to display an image.** In rare cases needing interactivity, configure a system-provided button to display the image rather than adding button behaviors to an image view.
- **If you want to display an icon, consider a symbol or interface icon instead of an image view.** SF Symbols provides streamlined, vector-based images renderable with various colors/opacities; an icon (glyph/template image) is typically a bitmap whose nontransparent pixels receive color — both can use accent colors.
- Image views can contain rich image data (PNG, JPEG, PDF, etc.).
- **Take care when overlaying text on images** — compositing can reduce image clarity and text legibility; ensure contrast, and consider a text shadow or background layer.
- **Aim to use a consistent size for all images in an animated sequence** — prescaling to fit the view avoids system scaling work; when scaling is unavoidable, same size/shape images perform better.

**Platforms:**
- macOS: for an editable image view, use an *image well* (supports copy/paste/drag/Delete-key clearing). Use an *image button* (not an image view) to make a clickable image.
- tvOS: many images combine multiple transparent layers to create depth (see Layered images).
- visionOS: windows can use image views for 2D and stereoscopic images and spatial photos; RealityKit apps can display images of any type outside image views next to 3D content, or generate a spatial scene from an existing 2D image.
- watchOS: use SwiftUI to create animations when possible; alternatively use WatchKit to animate an image sequence (`WKImageAnimatable`).
- No additional considerations for iOS or iPadOS.

## Text views
Source: https://developer.apple.com/design/human-interface-guidelines/text-views
A text view displays multiline, styled text content, which can optionally be editable.
Use for displaying long, editable, or specially formatted text; prefer a label for small amounts of static text, or a text field for small amounts of editable text.

- Text views can be any height and scroll when content exceeds the view; content is by default leading-aligned and uses the system label color; in iOS/iPadOS/visionOS an editable text view brings up a keyboard when selected.
- **Use a text view when you need to display text that's long, editable, or in a special format.**
- **Keep text legible** — adopt Dynamic Type so text scales with device text-size settings; test with accessibility options (e.g., bold text) turned on.
- **Make useful text selectable** — e.g., an error message, serial number, or IP address, so people can copy it for pasting elsewhere.

**Platforms:**
- iOS, iPadOS: **show the appropriate keyboard type** for the content being edited, to streamline data entry.
- tvOS: text input is minimal by design; tvOS uses text fields for editable text instead of text views.
- No additional considerations for macOS, visionOS, or watchOS.

## Web views
Source: https://developer.apple.com/design/human-interface-guidelines/web-views
A web view loads and displays rich web content, such as embedded HTML and websites, directly within your app (e.g., Mail uses one to show HTML message content).

- **Support forward and back navigation when appropriate** — not available by default; provide it plus corresponding controls if people are likely to visit multiple pages.
- **Avoid using a web view to build a web browser.** Briefly accessing a site without leaving your app's context is fine, but Safari is the primary way people browse the web; replicating Safari's functionality is unnecessary and discouraged.

**Platforms:** Not supported in tvOS or watchOS. No additional considerations for iOS, iPadOS, macOS, or visionOS.

## Boxes
Source: https://developer.apple.com/design/human-interface-guidelines/boxes
A box creates a visually distinct group of logically related information and components, by default using a visible border or background color to separate its contents; it can include a title.

- **Prefer keeping a box relatively small compared with its containing view.** As a box approaches the size of the containing window/screen, it communicates grouping less effectively and can crowd other content.
- **Consider using padding and alignment to communicate additional grouping within a box** rather than nesting boxes — a box's border is a distinct visual element, and nested boxes can make an interface feel busy and constrained.
- **Provide a succinct introductory title if it helps clarify the box's contents** — also helps VoiceOver users predict content within the box.
- **If you need a title, write a brief phrase describing the contents.** Use sentence-style capitalization; avoid ending punctuation unless the box is in a settings pane, where you append a colon.

**Platforms:**
- iOS, iPadOS: use secondary and tertiary background colors in boxes by default.
- macOS: displays a box's title above it by default.
- Not supported in tvOS or watchOS. No additional considerations for visionOS.

## Collections
Source: https://developer.apple.com/design/human-interface-guidelines/collections
A collection manages an ordered set of content and presents it in a customizable, highly visual layout — ideal for showing image-based content.
Prefer a table instead of a collection for text — text is generally simpler and more efficient to view/digest in a scrollable list.

- **Use the standard row or grid layout whenever possible** — these default appearances are simple, effective, and expected; avoid a custom layout that could confuse people or draw undue attention to itself.
- **Make it easy to choose an item** — use adequate padding around images to keep focus/hover effects easy to see and prevent content from overlapping; otherwise people get frustrated and lose interest.
- **Add custom interactions when necessary.** By default people can tap to select, touch and hold to edit, and swipe to scroll; add more gestures if your app requires custom actions.
- **Consider using animations to provide feedback** when people insert, delete, or reorder items — collections support standard animations for these, and custom animations are also possible.

**Platforms:**
- iOS, iPadOS: **use caution when making dynamic layout changes** — be sure changes make sense and are easy to track; avoid changing the layout while people are viewing/interacting with it unless in response to an explicit action.
- Not supported in watchOS. No additional considerations for macOS, tvOS, or visionOS.

## Column views
Source: https://developer.apple.com/design/human-interface-guidelines/column-views
A column view (also called a *browser*) lets people view and navigate a data hierarchy using a series of vertical columns, each representing one level of the hierarchy with horizontal rows of data items; a parent item with nested children is marked with a triangle icon, and selecting a parent displays its children in the next column.
Use for a deep data hierarchy where people navigate back and forth frequently between levels and you don't need the sorting a list/table provides; for hierarchical content presentation in iPadOS/visionOS, consider Split views instead.

- **Show the root level of your data hierarchy in the first column** — people know they can scroll back to it to restart navigation from the top.
- **Consider showing information about the selected item when there are no nested items to display** (e.g., Finder shows a preview plus creation date, modification date, file type, and size).
- **Let people resize columns** — especially important when some item names are too long to fit the default column width.

**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

## Disclosure controls
Source: https://developer.apple.com/design/human-interface-guidelines/disclosure-controls
Disclosure controls reveal and hide information and functionality related to specific controls or views.

- **Use a disclosure control to hide details until they're relevant** — place controls people are most likely to use at the top of the disclosure hierarchy (always visible), hiding more advanced functionality by default.
- **Disclosure triangle**: shows/hides information and functionality for a view or list of items (e.g., Keynote's export advanced options; Finder's hierarchy navigation in list view). Points inward from the leading edge when content is hidden, and down when visible; clicking/tapping toggles state and expands/collapses the view. **Provide a descriptive label** indicating what is disclosed/hidden (e.g., "Advanced Options"). For developer guidance, see `NSButton.BezelStyle.disclosure`.
- **Disclosure button**: shows/hides functionality for a specific control (e.g., macOS Save sheet's button next to the Save As field expanding to advanced navigation options). Points down when content is hidden, up when visible; toggles on click/tap. **Place a disclosure button near the content it shows and hides** to establish a clear relationship. **Use no more than one disclosure button in a single view** — multiple add complexity and confusion. For developer guidance, see `NSButton.BezelStyle.pushDisclosure`.

**Platforms:**
- iOS, iPadOS, visionOS: available via the SwiftUI `DisclosureGroup` view.
- Not supported in tvOS or watchOS. No additional considerations for macOS.

## Labels
Source: https://developer.apple.com/design/human-interface-guidelines/labels
A label is a static piece of text that people can read and often copy, but not edit — appearing in buttons, menu items, and views to help people understand context and what they can do next.
Use a label for a small amount of text people don't need to edit; use a text field if they need to edit a small amount of text; use a text view to display a large amount of text (optionally editable).

- **Use a label to display a small amount of text that people don't need to edit.**
- **Prefer system fonts.** A label can display plain or styled text and supports Dynamic Type (where available) by default; if you adjust style or use custom fonts, keep text legible.
- **Use system-provided label colors to communicate relative importance** — four system label colors vary in appearance for different levels of visual importance.
- **Make useful label text selectable** (e.g., an error message, a location, or an IP address), so people can copy it for pasting elsewhere.

| System color | Example usage | iOS, iPadOS, tvOS, visionOS | macOS |
| --- | --- | --- | --- |
| Label | Primary information | label | labelColor |
| Secondary label | A subheading or supplemental text | secondaryLabel | secondaryLabelColor |
| Tertiary label | Text that describes an unavailable item or behavior | tertiaryLabel | tertiaryLabelColor |
| Quaternary label | Watermark text | quaternaryLabel | quaternaryLabelColor |

**Platforms:**
- macOS: to display uneditable text in a label, use the `isEditable` property of `NSTextField`.
- watchOS: date and time text components display the current date, time, or both, configurable in various formats/calendars/time zones; a countdown timer text component displays a precise countdown or count-up timer in various formats. When using system-provided date/timer text components, watchOS automatically adjusts presentation to fit available space and updates content without further app input. Consider using date/timer components in complications.
- No additional considerations for iOS, iPadOS, tvOS, or visionOS.

## Lists and tables
Source: https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
Lists and tables present data in one or more columns of rows; they can represent data organized in groups or hierarchies and can support selecting, adding, deleting, and reordering.
Prefer displaying text in a list or table over a collection — the row-based format is well suited to making text easy to scan and read; if items vary widely in size or you need to display many images, use a collection instead.

- **Let people edit a table when it makes sense** — people appreciate reordering even without add/remove. In iOS/iPadOS, people must enter an edit mode before selecting table items.
- **Provide appropriate feedback when people select a list item** — varies by whether selection reveals a new view or toggles state: a hierarchy-navigation table persistently highlights the selected row; an options-list table often briefly highlights the row before showing a checkmark or similar indicating selection.
- **Keep item text succinct so row content is comfortable to read** — minimizes truncation/wrapping. For large text amounts, consider listing item titles only and revealing content in a detail view.
- **Consider ways to preserve readability of text that might otherwise get clipped or truncated** — e.g., a middle ellipsis can make an item more distinguishable by preserving both beginning and end.
- **Use descriptive column headings in a multicolumn table** — nouns or short noun phrases, title-style capitalization, no ending punctuation. In a single-column table without a heading, use a label or header for context.
- **Choose a table or list style that coordinates with your data and platform.** Examples: iOS/iPadOS *grouped* style uses headers/footers/extra space to separate groups; watchOS *elliptical* style makes items appear to roll off a rounded surface while scrolling; macOS *bordered* style uses alternating row backgrounds for large tables. See `ListStyle`.
- **Choose a row style that fits the information you need to display** — e.g., a leading small image followed by a brief label; platforms provide built-in row-content APIs (e.g., `UIListContentConfiguration` for rows/headers/footers in iOS, iPadOS, tvOS).

**Platforms:**
- iOS, iPadOS, visionOS: **use an info button only to reveal more information about a row's content** — an info button (called a *detail disclosure button* in a list row) does not support navigating a hierarchical table/list; use a disclosure indicator accessory control (`UITableViewCell.AccessoryType.disclosureIndicator`) for drilling into subviews. **Avoid adding an index to a table that displays trailing-edge controls** like disclosure indicators — both appear on the trailing side, making it hard to use one without activating the other.
- macOS: **let people click a column heading to sort** (re-sort in the opposite direction on a second click of an already-sorted heading). **Let people resize columns.** **Consider alternating row colors** in a multicolumn table, especially wide ones. **Use an outline view instead of a table view to present hierarchical data** — looks like a table view but with disclosure triangles for nested levels (e.g., folders and their contents).
- tvOS: **confirm images near a table still look good** as each row highlights and enlarges slightly when focused (corners may round) — account for this and don't add your own corner masks.
- watchOS: **when possible, limit the number of rows** — short lists are easier to scan; for long lists (e.g., many podcast subscriptions), show the most relevant items and provide a way to view more. **Constrain the length of detail views if you want to support vertical page-based navigation** — this lets people swipe vertically among row detail items without returning to the list, but only works when detail views are short (non-scrolling).

## Lockups
Source: https://developer.apple.com/design/human-interface-guidelines/lockups
Lockups combine multiple separate views — a content view, a header, and a footer — into a single, interactive unit; headers appear above the main content and footers below, and all three expand/contract together as the lockup gets focus. Four types: cards, caption buttons, monograms, and posters.

- **Allow adequate space between lockups** — a focused lockup expands in size, so leave enough room to avoid overlapping or displacing other lockups.
- **Use consistent lockup sizes within a row or group** — matching widths/heights across a group of buttons or a row of content images is more visually appealing.
- **Cards** combine a header, footer, and content view to present ratings and reviews for media items (`TVCardView`).
- **Caption buttons** can include a title and subtitle beneath the button, and can contain either an image or text. Ensure caption buttons tilt with swipe motion when focused: vertically aligned buttons tilt up/down, horizontally aligned tilt left/right, and grid-displayed buttons tilt both ways (`TVCaptionButtonView`).
- **Monograms** identify people (usually cast/crew) via a circular picture and their name; if no image is available, initials appear instead. **Prefer images over initials** — an image creates a more intimate connection than text (`TVMonogramContentView`).
- **Posters** consist of an image and an optional title/subtitle, hidden until the poster comes into focus; posters can be any size, but size must suit the content (`TVPosterView`).

**Platforms:** Not supported in iOS, iPadOS, macOS, visionOS, or watchOS (tvOS-only component).

## Outline views
Source: https://developer.apple.com/design/human-interface-guidelines/outline-views
An outline view presents hierarchical data in a scrolling list of cells organized into columns and rows; it includes at least one column with primary hierarchical data (e.g., parent containers and children), plus optional columns for supplemental attributes (e.g., sizes, modification dates); parent containers have disclosure triangles to reveal children. (Finder windows use one to navigate the file system.)
Use a table instead of an outline view to present data that isn't hierarchical.

- Outline views work well for text-based content and often appear on the leading side of a split view, with related content on the opposite side.
- **Expose data hierarchy in the first column only** — other columns display attributes applying to the hierarchical data in the primary column.
- **Use descriptive column headings to provide context** — nouns or short noun phrases, title-style capitalization, no punctuation (avoid a trailing colon). Always provide column headings in a multi-column outline view; in a single-column view without a heading, use a label or other means to ensure context.
- **Consider letting people click column headings to sort an outline view** — clicking performs ascending/descending sort on that column; you can layer secondary-column sorting behind the scenes. Clicking the primary column heading sorts at each hierarchy level (e.g., in Finder, top-level folders sort, then items within each folder sort). Clicking an already-sorted heading reverses the sort direction.
- **Let people resize columns** — outline-view data widths vary, so let people adjust column width to reveal data wider than the column.
- **Make it easy for people to expand or collapse nested containers** — e.g., clicking a folder's disclosure triangle expands only that folder, while Option-clicking expands all its subfolders.
- **Retain people's expansion choices** — store state so the same expanded structure appears again next time, avoiding renavigation.
- **Consider using alternating row colors in multi-column outline views** — makes it easier to track row values across columns, especially in wide views.
- **Let people edit data if it makes sense** — in an editable cell, people expect a single click to edit contents; a cell can respond differently to a double click (e.g., single-click a file name to edit it, double-click to open it). You can also let people reorder, add, and remove rows.
- **Consider using a centered ellipsis to truncate cell text instead of clipping it** — preserves both the beginning and end of the text, making content more distinct and recognizable.
- **Consider offering a search field** to help people find values quickly in a lengthy outline view — often placed in the toolbar of windows where the outline view is the primary feature.

**Platforms:** Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS (macOS-only component).

## Split views
Source: https://developer.apple.com/design/human-interface-guidelines/split-views
A split view manages the presentation of multiple adjacent panes of content — tables, collections, images, custom views, etc. — typically used to show multiple levels of an app's hierarchy at once and support navigation between them (selecting an item in the primary pane displays its contents in the secondary pane; a tertiary pane can show additional content from the secondary pane's items). Commonly pairs with a Sidebar for navigation (leading pane lists top-level items/collections; secondary/tertiary panes present child collections and item details). Rarely, used to present supplementary functionality groups (e.g., Keynote's slide navigator, presenter notes, and inspector panes around the main slide canvas).

- **To support navigation, persistently highlight the current selection in each pane that leads to the detail view** — clarifies the relationship between panes' content and helps people stay oriented.
- **Consider letting people drag and drop content between panes** — split views expose multiple hierarchy levels, so dragging items between panes is a convenient way to move content.

**Platforms:**
- iOS: **prefer using a split view in a regular — not a compact — environment.** A split view needs horizontal space for multiple panes; in a compact environment (e.g., iPhone portrait), displaying multiple panes without wrapping/truncating is difficult, hurting legibility and interaction.
- iPadOS: can include two vertical panes (e.g., Mail) or three vertical panes (e.g., Keynote). **Account for narrow, compact, and intermediate window widths** since iPad windows are fluidly resizable — ensure logical navigation between panes at multiple widths (`NavigationSplitView`, `UISplitViewController`).
- macOS: panes can be arranged vertically, horizontally, or both, with dividers supporting drag-to-resize (`VSplitView`, `HSplitView`). **Set reasonable defaults for minimum and maximum pane sizes** — if panes are resizable, keep sizes that keep the divider visible (a too-small pane can make the divider seem to disappear). **Consider letting people hide a pane when it makes sense** (e.g., Keynote lets people hide the navigator and presenter-notes panes while editing). **Provide multiple ways to reveal hidden panes** (e.g., a toolbar button or menu command with a keyboard shortcut). **Prefer the thin divider style** — measures 1 point in width, maximizing content space while remaining easy to use; avoid thicker styles unless needed (e.g., both sides show strong linear table-row elements that make a thin divider hard to distinguish) (`NSSplitView.DividerStyle`).
- tvOS: works well to help people filter content — choosing a filter category in the primary pane displays results in the secondary pane. **Choose a split view layout that keeps the panes looking balanced** — default devotes 1/3 screen width to the primary pane and 2/3 to the secondary, but a half-and-half layout is also available. **Display a single title above a split view** describing the content as a whole — people already know how to navigate/filter, so per-pane titles aren't needed. **Choose the title's alignment based on the secondary pane's content type** — center the title in the window when the secondary pane contains a content collection; place the title above the primary view when the secondary pane contains a single main view of important content, to give it more room.
- visionOS: **to display supplementary information, prefer a split view instead of a new window** — gives convenient access to more info without leaving the current context, whereas a new window may confuse navigation/repositioning and requires managing view relationships. If requesting a small amount of information or a simple task before returning to the main task, use a Sheet instead.
- watchOS: displays either the list view or a detail view as a full-screen view. **Automatically display the most relevant detail view** on launch (e.g., based on location, time, or recent actions). **If your app displays multiple detail pages, place the detail views in a vertical Tab view** — people use the Digital Crown to scroll between the detail view's tabs, with a page indicator next to the Digital Crown showing tab count and current selection.

## Tab views
Source: https://developer.apple.com/design/human-interface-guidelines/tab-views
A tab view presents multiple mutually exclusive panes of content in the same area, which people can switch between using a tabbed control.

- **Use a tab view to present closely related areas of content** — its appearance strongly indicates enclosure, and people expect each tab's content to be similar or related to the others'.
- **Make sure the controls within a pane affect content only in the same pane** — panes are mutually exclusive, so ensure each is fully self-contained.
- **Provide a label for each tab that describes the contents of its pane** — a good label helps people predict pane contents before clicking/tapping. Use nouns or short noun phrases generally (a verb/short verb phrase may fit some contexts); use title-style capitalization.
- **Avoid using a pop-up button to switch between tabs** — a tabbed control needs a single click/tap versus two for a pop-up button, and presents all choices onscreen at once; a pop-up button can be a reasonable alternative when there are too many panes to display as tabs.
- **Avoid providing more than six tabs in a tab view** — more can overwhelm and create layout issues; for six-plus panes, consider another interface, such as presenting each as a view option in a pop-up button menu.
- **Anatomy**: the tabbed control appears on the top edge of the content area; you can hide it (appropriate for an app that switches panes programmatically). When hidden, the content area can be borderless, bezeled, or bordered with a line; a borderless view can be solid or transparent.
- **In general, inset a tab view by leaving a margin of window-body area on all sides** — looks clean and leaves room for additional controls unrelated to the tab view's contents. Extending a tab view to meet the window edges is unusual but possible.

**Platforms:**
- iOS, iPadOS: for similar functionality, consider using a segmented control instead.
- watchOS: displays tab views using page controls (`TabView`).
- Not supported in tvOS or visionOS.
