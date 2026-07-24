# HIG — Patterns
charting-data, collaboration-and-sharing, drag-and-drop, entering-data, feedback, file-management, going-full-screen, launching, live-viewing-apps, loading, managing-accounts, managing-notifications, modality, multitasking, offering-help, onboarding, playing-audio, playing-haptics, playing-video, printing, ratings-and-reviews, searching, settings, undo-and-redo, workouts

## Charting data
Source: https://developer.apple.com/design/human-interface-guidelines/charting-data
Charts communicate complex information visually so people can analyze trends, compare data across categories, and view changing states at a glance without reading a lot of text.
- **Use a chart when you want to highlight important information** about a dataset — charts are visually prominent and draw attention.
- **Keep a chart simple, letting people choose when they want additional details.** Reveal data or functionality gradually (different detail levels, subsets, or progressively richer chart versions) instead of packing everything in at once.
- **Make every chart accessible.** Provide accessibility labels describing chart values/components and accessibility elements for interaction, in addition to visual descriptions.
- **Prefer common chart types** (e.g., bar, line charts) since people already know how to read them.
- **If a chart presents data in a novel way, help people learn to interpret it** — e.g., animate components individually the first time (Activity rings when Watch first pairs).
- **Examine the data from multiple levels or perspectives** — macro summaries/totals/averages, mid-level useful subsets, individual data points — to find details worth displaying.
- **Aid comprehension with descriptive text** — titles, subtitles, and annotations that emphasize important information; a headline/summary can help but doesn't replace accessibility labels.
- **Match chart size to its functionality, topic, and level of detail** — large enough for details and interactivity; small for glanceable info or previews.
- **Prefer consistency across multiple charts**, deviating only to highlight meaningful differences (type/style).
- **Maintain continuity among multiple charts that use the same dataset** — same chart type, colors, annotations, layouts, and descriptive text across compact and expanded versions.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Collaboration and sharing
Source: https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing
System interfaces and Messages provide consistent, convenient ways for people to share content and start or manage collaborations, whether backed by CloudKit, iCloud Drive, or a custom infrastructure (which must also support universal links).
- **Place the Share button in a convenient location**, like a toolbar. iOS 16's share sheet and the iPadOS 16/macOS 13 sharing popover let people choose a file-sharing method and set permissions for a new collaboration; SwiftUI apps can present a share link (`ShareLink`) to open the share sheet.
- **If necessary, customize the share sheet or sharing popover** to offer the file-sharing types you support. With CloudKit, pass both the file and your collaboration object to enable "send copy." iCloud Drive supports "send copy" by default. For custom collaboration, include a file (or a plain text representation) in your collaboration object.
- **Write succinct phrases that summarize the sharing permissions you support** (e.g., "Only invited people can edit," "Everyone can make changes") — the system uses this summary in a button that reveals sharing options.
- **Provide a set of simple sharing options** for collaboration setup (who can access, edit vs. read, whether collaborators can add participants) — keep custom choices minimal and grouped for at-a-glance understanding.
- **Prominently display the Collaboration button as soon as collaboration starts**, ideally next to the Share button — it reminds people the content is shared and identifies who's sharing it.
- **Provide custom actions in the collaboration popover only if needed.** The popover has three sections: collaborators list with Messages/FaceTime communication buttons (top), your custom items (middle), and a "manage shared file" button (bottom).
- **If it makes sense, customize the modal view's collaboration-management button title** (default "Manage Shared File"). CloudKit sharing provides a management view by default; otherwise create your own.
- **Consider posting collaboration event notifications in Messages** — content/membership changes or participant mentions — including a universal link into the relevant app view (`SWHighlightEvent`).
**Platforms:** No additional considerations for iOS, iPadOS, or macOS. Not available in tvOS. visionOS — by default the system streams the current window to collaborators for screen sharing in the Shared Space; if someone transitions to a Full Space mid-share, the stream pauses for others until the app returns to the Shared Space. watchOS — use `ShareLink` to present the system-provided share sheet.

## Drag and drop
Source: https://developer.apple.com/design/human-interface-guidelines/drag-and-drop
Drag and drop lets people move or duplicate a selection (photos, text, other content) by dragging it from a source to a destination, within the same container, across containers, or across apps.
- Dropping within the same container generally **moves** content (exists only at destination); dropping in a different container generally **copies** it (exists in both); dragging between apps always results in a copy.
- Interaction differs by platform: visionOS — pinch and hold while dragging, including along the z-axis; iOS/iPadOS — touchscreen gestures, pointing devices, full keyboard-access mode; Universal Control drags content between Mac and iPad; macOS — pointing device, full keyboard access, or VoiceOver.
- **As much as possible, support drag and drop throughout your app.** System components like text fields/views get built-in support.
- **Offer alternative ways to accomplish drag-and-drop actions** — e.g., menu commands to copy/move; use accessibility APIs (`accessibilityDragSourceDescriptors`, `accessibilityDropPointDescriptors`) in iOS/iPadOS for assistive technologies.
- **Determine when dragging within your app results in a move or a copy.** A move generally makes sense within the same container; a copy makes sense across different containers. Prefer whichever default is least likely to cause frustration or data loss.
- **Support multi-item drag and drop when it makes sense.** iOS, iPadOS, macOS, visionOS let people select and drag a group; macOS also allows multi-app selection dragged as a group; iPadOS lets people add items to an in-progress drag without stopping it.
- **Prefer letting people undo a drag-and-drop operation.** Consider confirmation before an irreversible drop (Finder confirms dragging into a write-only folder); provide a way to reverse results when undo isn't possible (Photos lets people cancel photo sharing after a drop into a shared photo stream).
- **Consider offering multiple versions of dragged content**, ordered highest to lowest fidelity, so the destination can pick the richest version it accepts (e.g., PDF vector > lossless PNG with transparency > lossy JPEG; native chart object > simple image).
- **Consider supporting spring loading** — dragging selected content over a button or segmented control activates it (e.g., dragging an event over Calendar's day/week/month/year toolbar segments). On Mac with Magic Trackpad, force-click while holding content activates it; on iPad, hovering while holding content activates it.

Providing feedback:
- **Display a drag image as soon as people drag a selection about three points.** Make it translucent to distinguish it from the original and let people see destinations underneath; keep it displayed until drop.
- **If it adds clarity, modify the drag image to help predict the result** (e.g., expand to show a photo's default size in the document). Use drag *flocking* to visually group multiple drag items and ungroup on drop. Avoid constant, radical drag-image changes.
- **Show whether a destination can accept dragged content** — an insertion point or highlighted container when it can, no visual feedback or an explicit "not allowed" image (`circle.slash` from SF Symbols) when it can't. Show highlighting only while positioned above the destination; with multiple possible destinations, cue one at a time.
- **When a drop lands on an invalid destination, or dropping fails, provide visual feedback** — the item can move back to its source (if visible) or scale up and fade out ("evaporate").

Accepting drops:
- **Scroll the contents of a destination when necessary** as people drag over a scrolling container with a lot of content; system text views/fields do this by default.
- **When there's a choice, pick the richest version of dropped content your app can accept**, falling back to a simpler version if unsupported.
- **Extract only the relevant portion of dropped content if necessary** (e.g., Mail extracts just the name and email from a dragged contact).
- **When a physical keyboard is attached, check for the Option key at drop time.** Holding Option while dragging forces a copy within the same container; releasing Option before dropping results in a move.
- **Provide feedback when dropped content needs time to transfer** — a progress indicator, and a placeholder at the drop location in collections/lists/tables; the system can alert for time-consuming cross-app transfers.
- **Provide feedback when dropped content initiates a task or action** (e.g., printing) — show that the task has begun and keep people informed of its progress.
- **Apply appropriate styling to dropped text** — preserve the original font/typeface/size when source and destination support the same styles; otherwise apply the destination's style.
- **After a drop, maintain the content's selection state in the destination, updating it in the source as needed.** Content disappears from the original location on a move within the same container; deselect remaining content on a copy within the same container; deselect content in the source when dragged to a different container.
**Platforms:** Not supported in tvOS or watchOS. iOS, iPadOS — let people perform multiple simultaneous drag activities: sequentially add items to an in-progress drag (iPadOS), with flocking feedback, and accept multiple simultaneous drops. macOS — consider letting people drag content into the Finder in an openable format (e.g., Calendar → `.ics` file); output as a *clipping* (temporary container, distinct from the Clipboard) when necessary. Let people drag a *background selection* (in an inactive window) to the active window without first activating that window. Let people drag individual unselected items from an inactive window without affecting its existing background selection. Consider a badge (small filled oval with an item count) during multi-item drags, updated if the destination can accept only a subset. Consider changing the pointer to indicate drop outcome — *copy*, *drag link*, *disappearing item*, *operation not allowed* pointers. Let people select and drag content with a single motion where possible. visionOS — when possible, launch your app to handle content dropped into empty space by associating a user activity with draggable content (`NSUserActivity`) — e.g., dropping a URL opens Safari, Quick Look–supported content opens Quick Look.

## Entering data
Source: https://developer.apple.com/design/human-interface-guidelines/entering-data
Data entry is often tedious, so design should minimize the amount of information people must supply and support every available input method.
- **Get information from the system whenever possible** (e.g., settings, or by requesting permission for location/calendar) instead of asking people to enter it.
- **Be clear about the data you need** — a prompt in a text field (e.g., "username@company.com"), an introductory label (e.g., "Email"), or reasonable prefilled defaults to speed entry.
- **Use a secure text-entry field when appropriate** for sensitive data (`SecureField`), which obscures input (typically as a filled circle per character). tvOS can obscure numerals in a digit entry view (`isSecureDigitEntry`). In visionOS, the system-provided text field shows entered data only to the wearer; a secure field automatically blurs when streaming via AirPlay.
- **Never prepopulate a password field.** Always require entry, or use biometric or keychain authentication (see Managing accounts).
- **When possible, offer choices instead of requiring text entry** — a picker, menu, or other selection component is usually easier and faster than typing.
- **As much as possible, let people provide data by dragging and dropping it or by pasting it.**
- **Dynamically validate field values** as soon as people enter them, giving feedback immediately rather than after a lengthy form. Use a number formatter for numeric data — it restricts input to numeric values and can format decimal places, percentages, or currency.
- **When data entry is necessary, make sure people understand they must provide the required data before proceeding** — e.g., disable a Next/Continue button until required fields are filled.
**Platforms:** No additional considerations for iOS, iPadOS, tvOS, visionOS, or watchOS. macOS — consider using an *expansion tooltip* to show the full version of clipped or truncated text in a field when the pointer rests on it.

## Feedback
Source: https://developer.apple.com/design/human-interface-guidelines/feedback
Feedback helps people know what's happening, discover what they can do next, understand the results of actions, and avoid mistakes, matching the significance of information to how intrusively it's delivered.
- **Make sure all feedback is accessible.** Combine color, text, sound, and haptics so people can receive it whether they silence their device, look away, or use VoiceOver (see Playing haptics).
- **Consider integrating status feedback into your interface** near the items it describes (e.g., Mail shows unread count and last update in the mailbox toolbar) so people get information without leaving their context.
- **Use alerts to deliver critical — and ideally actionable — information.** Alerts disrupt the current context, so match importance to interruption; overusing alerts or using them for unimportant information causes them to lose impact.
- **Warn people when they initiate a task that can cause data loss that's unexpected and irreversible.** Don't warn when data loss is the expected result (e.g., the Finder doesn't warn every time people throw away a file).
- **When it makes sense, confirm that a significant action or task has completed** (e.g., a successful Apple Pay transaction) — reserve this for sufficiently important activities, since people typically expect success and mainly need to know about failure.
- **Show people when a command can't be carried out and help them understand why** (e.g., Maps explains it can't provide directions to and from the same location).
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS. watchOS — avoid displaying an indeterminate progress indicator (loading indicator); reassure people they'll receive a notification when the process completes instead.

## File management
Source: https://developer.apple.com/design/human-interface-guidelines/file-management
Document-based apps help people create, edit, and save files, often with a custom browsing experience, while people also expect to manage documents outside those apps via the Finder or Files app (watchOS and tvOS don't provide document browsing).

Creating and opening files:
- **Use app menus and keyboard shortcuts** for creating/opening documents — iPadOS presents New/Open in the shortcuts interface (hold Command on a hardware keyboard); macOS presents them in the File menu. Regardless of shortcuts, include an Add (+) button to create a new document (macOS: put the add action in the File menu).
- **If your app requires a custom file browser, support people's understanding of the platform's file system.** Show the most relevant starting location (e.g., Documents/iCloud folder, most recent location) but let people navigate the rest of the file system.

Saving work:
- **Help people be confident their work is always preserved unless they cancel or delete it.** Avoid requiring an explicit save action — autosave periodically and when closing a file or switching apps.
- **Hide file extensions by default, but let people view them if they choose,** reflecting the current choice consistently across all save/open interfaces.

Quick Look previews:
- **Use a Quick Look viewer to let people preview a file even when your app can't open it.**
- **Consider implementing a Quick Look generator if your app produces custom file types**, so the Finder, Files, and Spotlight can also display previews.
**Platforms:** No additional considerations for tvOS, visionOS, or watchOS.
### iOS, iPadOS
Document launcher (iOS/iPadOS 18+, `DocumentGroupLaunchScene`): a full-screen browse/open/create experience with three parts — a *title card* (app title + two app-specific buttons), a background image plus optional surrounding *accessories*, and a sheet containing a file browser and optional app-specific controls.
- **Assign the title card's buttons to your app's most important functions** — primary typically creates a new document, secondary offers additional options (e.g., Numbers: Start Writing / Choose a Template).
- **Provide a background that's clearly distinct from the accessories and title card** — a solid color, gradient, or pattern; avoid complex or distracting images.
- **Be mindful of accessory placement** — accessories can sit in front of and behind the title card for depth, but the app name and both buttons must stay clearly visible; avoid clutter and test across screen sizes/orientations.
- **Use animation sparingly** — prefer gentle, repeating animations (e.g., an accessory that appears to breathe or sway softly).
File provider app extension: display only documents appropriate to the current context (e.g., only PDFs for a PDF editor), plus useful metadata (modification dates, sizes, local/remote status). Let people select a destination when exporting/moving, with a way to add subdirectories. Avoid a custom top toolbar — the extension loads within a modal view that already has one.
### macOS
Custom file management: use the default file browser unless there's an important reason to create a custom one.
- **Make your custom file-opening interface convenient** — an "open recent" action, filter criteria, multi-select; customize the Open button's title to reflect the task (e.g., "Insert").
- **Provide a save interface** to change a file's name, format, or location — new documents default to "Untitled" until named; offer a format choice if multiple formats are supported.
- **Consider extending the Save dialog** with a custom accessory view (e.g., Mail's option to include attachments).
Finder Sync extensions can display sync-status badges in the Finder, custom contextual menu items (favoriting, password-protection), and custom toolbar buttons (e.g., initiate a sync).
- **Help people avoid losing work if they turn off autosaving** (the "Ask to keep changes when closing documents" toggle in Desktop & Dock settings) — show unsaved changes and present a save dialog on close, quit, log out, or restart.
- **When autosaving is off, make sure people know when a document has unsaved changes** — a dot on the window's close button and next to the document name in the Window menu (don't show the dot when autosave is on). Regardless of autosave status, you can append "Edited" to the title bar, removing it as soon as autosave occurs or people save explicitly.

## Going full screen
Source: https://developer.apple.com/design/human-interface-guidelines/going-full-screen
iPhone, iPad, and Mac offer full-screen modes that expand a window to fill the screen and hide system controls for a distraction-free environment; Apple TV and Apple Watch already fill the screen by default, and Apple Vision Pro instead offers immersive experiences.
- **Support full-screen mode when it makes sense** — games, media viewing (video/photo slideshows), or an in-depth task benefiting from a distraction-free environment.
- **If necessary, adjust your layout in full-screen mode, but don't programmatically resize your window.** Keep essential content prominent, adjust proportions subtly, and avoid visually jarring transitions between modes.
- **Continue to provide access to essential features and controls** so people can complete their task without exiting full-screen mode (e.g., persistent or easily revealed playback controls).
- **Except in games, let people reveal the Dock while your iPadOS or macOS app is in full-screen mode.** To prevent accidental Dock reveals during a full-screen game, you can ask iPadOS to ignore an initial bottom-edge swipe or hide the Dock entirely in macOS (`preferredScreenEdgesDeferringSystemGestures`, `hideDock`).
- **After people switch away from your full-screen experience, help them resume where they left off** (e.g., auto-pause a game or slideshow).
- **Let people choose when to exit full-screen mode** — don't end it automatically on switching away or finishing an absorbing activity.
- **Prioritize content by temporarily hiding toolbars and navigation controls,** restorable via a familiar gesture (tapping, swiping down, moving the cursor to the top); keep controls visible when essential for navigation or tasks.
**Platforms:** Not supported in tvOS, visionOS, or watchOS.
### iOS, iPadOS
**Consider deferring system gestures to prevent accidental exits.** The Home Screen indicator normally hides shortly after switching to your app/game and reappears on bottom-screen interaction (a single swipe exits); retain this by default, but enable two swipes rather than one if it causes unexpected exits (`preferredScreenEdgesDeferringSystemGestures`).
### macOS
**Use the system-provided full-screen experience** (`toggleFullScreen(_:)`) — it automatically accommodates device variations (e.g., a camera housing). **In a game, don't change the display mode when players go full screen.** **Always let people choose when to enter full-screen mode** — the window's Enter Full Screen button, View menu item, or Control-Command-F shortcut; avoid a custom menu of window modes (a custom on/off toggle for games is fine).

## Launching
Source: https://developer.apple.com/design/human-interface-guidelines/launching
Launching begins when someone opens the app, includes an initial download, and ends when the first screen is ready; Onboarding, if any, follows.
- **Launch instantly** — people may not want to wait more than a couple of seconds.
- **If the platform requires it, provide a launch screen** (iOS, iPadOS, tvOS) that's quickly replaced by the first screen; macOS, visionOS, and watchOS don't require one.
- **If you need a splash screen, consider displaying it at the beginning of your onboarding flow** (or right after launch completes if there's no onboarding).
- **Restore the previous state when your app restarts** — scroll position, window state and location — so people continue where they left off.

Launch screens (not applicable to macOS, visionOS, or watchOS):
- **Downplay the launch experience** — it's not onboarding, not a splash screen, and not an opportunity for artistic expression; its sole function is to make the launch feel fast and ready.
- **Design a launch screen that's nearly identical to the first screen** to avoid an unpleasant flash between them; match the device's current orientation and appearance mode.
- **Avoid including text on your launch screen** — static content won't be localized.
- **Don't advertise** — no logos or branding elements unless they're a fixed part of the first screen.
**Platforms:** No additional considerations for macOS or watchOS.
### iOS, iPadOS
**Launch in the appropriate orientation** — the device's current orientation if both portrait and landscape are supported; otherwise the single supported orientation, responding correctly regardless of rotation direction.
### tvOS
> Note: Unlike layered images throughout much of a tvOS app, the launch screen is static.
**In a live-viewing app, consider automatically starting playback** of new or recently viewed live content after a few seconds of inactivity.
### visionOS
**Consider launching in the Shared Space even if your app is fully immersive** — it provides more context while loading and lets you present a control for transitioning to a Full Space when people choose.

## Live-viewing apps
Source: https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps
Live-viewing apps must prioritize live content in every screen and make sure people can distinguish it from video-on-demand (VOD) content at a glance.
- **Feature live content prominently and make it easy to access** — minimize the interval between starting the app and playing content; live content in the first tab needs only one tap.
- **Let people tap once — or not at all — to start playback** (e.g., a Watch Now button over featured/recently viewed content that disappears and immediately starts full-screen playback).
- **Make sure live content looks live** — mark it (e.g., a "Live" collection row with a badge, symbol, or sash) to help people distinguish it from VOD content.
- **Consider indicating the progress of currently playing live content** (a progress bar or similar) so people know how much remains.
- **Give people additional actions and viewing alternatives** beyond playback (record, restart, download, favorite) in a consistent order (e.g., Watch, Start Over, Record, Favorite); show rebroadcast times if applicable.
- **Consider using a content footer for browsing channels during playback.** Give it a subtle treatment (e.g., darkening) to keep text legible; badge or tint the currently playing thumbnail; match categories to the EPG; and design a simple, predictable way to invoke and dismiss it (e.g., swipe up to invoke, swipe down to dismiss).
- **Provide instant visual feedback when people change channels** — confirms arrival at the desired channel and buys time for content to load.
- **Match audio to the current context** — audio continues while browsing within the live tab, but stops once people navigate away from the live tab.

EPG experience:
- **Prominently display current information** (program, channel, time) and make it easy to return to playback.
- **Make browsing the EPG effortless** — support easy paging, scrolling, or jumping; consider a My Channels or Favorites group.
- **Group content into familiar categories** (e.g., Movies, TV Shows, Kids, Sports, Popular); match content footer categories to EPG categories.
- **Let people browse the EPG without leaving their current content** — e.g., continue playback via Picture in Picture or in the background.

Cloud DVR:
- **Let people start and stop recording from the info panel** while live-streaming.
- **Let people record a future program** from its details view, with the option to record only that program or all future episodes.
- **Help people adapt the recording experience to their needs** (e.g., current episode only, new episodes only, specific teams).
- **Allow playback and other content-specific actions** (play, delete, adjust recording settings) within the cloud DVR area.
- **Consider offering a control that lets people manage cloud DVR settings** — delete watched or old recordings, or set up automatic storage management that overwrites the oldest or already-viewed content.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Loading
Source: https://developer.apple.com/design/human-interface-guidelines/loading
The best content-loading experience finishes before people become aware of it, so loading behavior shouldn't disrupt or negatively impact the experience.
- **Show something as soon as possible.** A blank wait can read as a problem — show placeholder text, graphics, or animations, replacing them as content becomes available.
- **Let people do other things in your app or game while they wait for content to load** — load content in the background (e.g., a game loads content while players read next-level info or browse an in-game menu; see `Improving the player experience for games with large downloads`).
- **If loading takes an unavoidably long time, give people something interesting to view** — gameplay hints, tips, or feature introductions — while gauging the remaining time accurately so the placeholder content is neither too short nor repeated.
- **Improve installation and launch time by downloading large assets in the background** — the Background Assets framework can schedule downloads (level packs, 3D models, textures) immediately after installation, during updates, or at other nondisruptive times.

Showing progress:
- **Clearly communicate that content is loading and how long it might take.** Use a *determinate* progress indicator when the duration is known, and an *indeterminate* one when it isn't (see Progress indicators).
- **For games, consider creating a custom loading view** using animations/elements matching the game's style, since standard indicators can feel out of place.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS. watchOS — as much as possible avoid showing a loading indicator; aim for immediate content, but a loading indicator is better than a blank screen when content needs a second or two.

## Managing accounts
Source: https://developer.apple.com/design/human-interface-guidelines/managing-accounts
An account can conveniently let people access content and track personal details, but should only be required when core functionality demands it.
- **Ask people to create an account only if your core functionality requires it**; otherwise let people use the app without one. Consider Sign in with Apple for a consistent, trusted sign-in that avoids extra credentials.
- **Explain the benefits of creating an account and how to sign up** in a brief, friendly description shown in the sign-in view.
- **Delay sign-in for as long as possible** — let people get a sense of the app first (e.g., a shopping app can let people browse freely, requiring sign-in only at purchase).
- **If you don't use Sign in with Apple in iOS, iPadOS, macOS, or visionOS, prefer using a passkey** — no password to create or remember, just a username (`Supporting passkeys`). If you must keep using passwords, augment with two-factor authentication (`Securing Logins with iCloud Keychain Verification Codes`).
- **Always identify the authentication method you offer** (e.g., "Sign In with Face ID," not a generic "Sign In").
- **Refer only to authentication methods available in the current context** — check device capability (`LABiometryType`) rather than assuming.
- **In general, avoid offering an app-specific setting for opting in to biometric authentication** — it's already a system-level toggle.
- **Avoid using the term "passcode" to refer to account authentication** — reserve it for device/Apple-service unlock so people don't think you're asking them to reuse it in your app.

Deleting accounts: you must help people delete, not just deactivate, an account created within your app, complying with regional legal requirements around deletion and the right to be forgotten.
> Important: If legal requirements compel your app to maintain accounts or information (e.g., digital health records) or follow a specific deletion process, clearly describe the situation to people.
- **Provide a clear way to initiate account deletion within your app.** If not possible in-app, provide a direct, easily discoverable link to the deletion webpage — don't bury it in your Privacy Policy or Terms of Service.
> Developer note: If people used Sign in with Apple to create the account, revoke the associated tokens when they delete it (Token revocation).
- **Provide a consistent account-deletion experience** whether performed in-app or on the website.
- **Consider letting people schedule account deletion to occur in the future** (e.g., to use remaining services or wait for auto-renewal), alongside an immediate-deletion option.
- **Tell people when account deletion will complete, and notify them when it's finished.**
- **If you support in-app purchases, help people understand billing and cancellation on account deletion** — billing for an auto-renewable subscription continues through Apple until people cancel it, regardless of account deletion; after deleting their account, people still need to cancel the subscription or request a refund.
> Note: Even if people didn't use your app to purchase the subscription, you still need to support account deletion.

TV provider accounts: use TV Provider Authentication for the most efficient onboarding when sign-in is required.
- **Avoid displaying a sign-out option when people are signed in at the system level.** If your app must include one, invoking it should prompt people to go to Settings > TV Provider to sign out.
- **Never instruct people to sign out by adjusting privacy controls** — the Settings > Privacy TV provider controls manage app access, not sign-out.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, or visionOS. tvOS — ask for the minimum information necessary since most people use a remote, not a keyboard. Prefer letting people use another device to sign up or authenticate via associated domains (including Sign in with Apple credential suggestion). When signed in to a shared account, avoid re-prompting profile choice every time (tvOS 16+ can share credentials while storing individual profiles/data separately — `kSecUseUserIndependentKeychain`, User Management Entitlement). Minimize data entry — for more than a small amount of information, direct people to a website on another device; for email, show the email keyboard screen with recently entered addresses. watchOS — use iCloud synchronization for Keychain access, letting people autofill usernames/passwords and preserve app settings.

## Managing notifications
Source: https://developer.apple.com/design/human-interface-guidelines/managing-notifications
Notifications give people timely, important information whether the device is locked or in use; you must get permission before sending any, and people can adjust or silence them in Settings (except government alerts in some locales).
A Focus filters notifications during a reserved activity period (sleeping, working, reading, driving); delivery scheduling lets people choose immediate alerts vs. a delivered summary. People identify contacts/apps that can break through a Focus, and can choose to receive all Time Sensitive alerts during one.
> Important: Even if a Focus delays alert delivery, the notification itself is available as soon as it arrives.
Notification types: *communication* notifications (direct communications like calls/messages, via SiriKit intents such as `INSendMessageIntent`/`UNNotificationContentProviding`, letting people use Siri to customize behavior) vs. *noncommunication* notifications, which require a specified interruption level (the system uses the sender to determine delivery timing for communication notifications).

Interruption levels for noncommunication notifications:
| Level | Meaning |
| Passive | Information people can view at their leisure, like a restaurant recommendation |
| Active (default) | Information people might appreciate knowing when it arrives, like a score update |
| Time Sensitive | Information that directly impacts the person and requires immediate attention, like an account security issue or package delivery |
| Critical | Urgent health/safety information demanding immediate attention; extremely rare, typically from governmental/public agencies or health/home apps |

| Interruption level | Overrides scheduled delivery | Breaks through Focus | Overrides Ring/Silent switch on iPhone and iPad |
| Passive | No | No | No |
| Active | No | No | No |
| Time Sensitive | Yes | Yes | No |
| Critical | Yes | Yes | Yes |
> Note: Because a Critical notification can override the Ring/Silent switch and break through scheduled delivery and Focus, you must get an entitlement to send one.
- **Build trust by accurately representing the urgency of each notification** — don't use a high interruption level to interrupt with low-priority information.
- **Use the Time Sensitive interruption level only for notifications that are relevant in the moment** — happening now or within an hour (`UNNotificationInterruptionLevel`). The system explains the behavior on first arrival, lets people opt out, and periodically re-solicits feedback afterward.

Sending marketing notifications:
- **Don't use notifications to send marketing or promotional content unless people explicitly agree to receive it.**
- **Never use the Time Sensitive interruption level to send a marketing notification** — it must never break through a Focus or scheduled delivery, even with permission.
- **Get people's permission if you want to send them promotional or marketing notifications** via an alert, modal view, or other interface with a clear opt-in/opt-out.
- **Make sure people can manage their notification settings within your app**, in addition to the initial permission request.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS. watchOS — iPhone notification settings apply by default to the same apps on Apple Watch; manageable via the Apple Watch app on iPhone, or per-notification (e.g., Mute 1 Hour, Turn off Time Sensitive) by swiping left on an arriving notification.

## Modality
Source: https://developer.apple.com/design/human-interface-guidelines/modality
Modality presents content in a separate, dedicated mode that prevents interaction with the parent view and requires an explicit action to dismiss.
- Modal presentation can ensure people receive and act on critical information, let them confirm/modify a recent action, help them perform a distinct narrowly scoped task without losing prior context, or provide immersion/concentration for a complex task.
- Component types vary by platform: an *alert* is available on all platforms; *activity views*, *sheets*, *confirmation dialogs*/*action sheets* are context-specific; iOS/iPadOS/macOS apps tend to use sheets or popovers for distinct tasks, while iPadOS/macOS/visionOS may use a separate window; full-screen modal experiences suit temporary or multistep tasks.
- **Present content modally only when there's a clear benefit** — it removes people from their current context and requires an action to dismiss.
- **Aim to keep modal tasks simple, short, and streamlined** — overly complicated modal tasks risk people losing track of the suspended task, especially if the modal view obscures the previous context.
- **Take care to avoid creating a modal experience that feels like an app within your app.** If a modal task must contain subviews, provide a single path through the hierarchy and avoid buttons people might mistake for the dismiss button.
- **Consider using a full-screen modal style for in-depth content or a complex task** (videos, photos, camera views, multistep editing). In visionOS Shared Space it fills a window; transitioning to a Full Space can make it more immersive.
- **Always give people an obvious way to dismiss a modal view**, following platform conventions — iOS, iPadOS, watchOS: a button in the top toolbar or swipe down; macOS, tvOS: a button in the main content view.
- **When necessary, help people avoid data loss by getting confirmation before closing a modal view** whose closing could lose user-generated content (e.g., an action sheet with a save option).
- **Make it easy to identify a modal view's task** — a title naming the task, or descriptive text/guidance.
- **Let people dismiss a modal view before presenting another one.** Avoid multiple simultaneous modal views (visual clutter, cognitive load); an alert can appear atop all other content including other modal views, but never display more than one alert at the same time.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Multitasking
Source: https://developer.apple.com/design/human-interface-guidelines/multitasking
Multitasking lets people switch quickly between apps; with rare exceptions (some games, Apple Vision Pro apps in a Full Space), every app needs to work well with it.
- **Pause activities that require people's attention or active participation when they switch away** (games, media-viewing apps) so nothing is missed; let people continue as if they never left.
- **Respond smoothly to audio interruptions.** Pause audio indefinitely for primary audio interruptions (e.g., an incoming call interrupting music/podcasts/audiobooks); temporarily lower the volume or pause for shorter interruptions (e.g., GPS directional notifications), resuming original volume/playback when the interruption ends.
- **Finish user-initiated tasks in the background** (downloads, video processing) even if people switch away, if the task doesn't need additional input.
- **Use notifications sparingly.** Notify for important/time-sensitive task completion after people switch away, but avoid unnecessary notifications for routine/secondary task completion — let people check on it when they return.
**Platforms:** Not supported in watchOS.
### iOS
Multitasking lets people use FaceTime or watch video in Picture in Picture while using a different app.
### iPadOS
People view and interact with multiple app Windows simultaneously; an individual app can also support multiple open windows. Both full-screen and windowed apps are supported: full screen occupies the whole screen with app-switcher-based switching; windowed apps are resizable and arrangeable like macOS, with system window controls for tiling, entering full screen, minimizing, and closing — the frontmost window is identified by colored window controls and a drop shadow. Videos and FaceTime calls can play in a Picture in Picture overlay above other content regardless of full-screen or windowed state.
> Note: Apps don't control multitasking configurations or receive any indication of the ones that people choose.
Make sure your app adapts gracefully to different screen sizes for windowed launches (see Layout, Windows; `Multitasking on iPad, Mac, and Apple Vision Pro`).
### macOS
Multitasking is the default experience; drop shadows and other visual effects distinguish layered windows and window states (see macOS window states).
### tvOS
People can play or browse content while also playing movies or TV shows in Picture in Picture (where supported).
### visionOS
Multiple apps run simultaneously in the Shared Space. Only one window is active at a time — looking at a window activates it while the previous one becomes more translucent and recedes along the z-axis; closing a window transitions the app to the background without quitting it.
> Note: When an app is the Now Playing app, closing its window automatically pauses audio playback; people can resume in Control Center without opening the window.
**Avoid interfering with the system-provided multitasking behavior** — don't change a window's edge appearance, since visionOS applies a feathered mask to clarify a window's changed state when people look away. **Don't pause a window's video playback when people look away from it** — as in macOS, playback continues. **Be prepared for situations where your audio can duck** — unless your app is the Now Playing app, its audio can duck when people look away to another app.

## Offering help
Source: https://developer.apple.com/design/human-interface-guidelines/offering-help
Contextual help supports experiences that can't be entirely approachable and intuitive on their own.
- **Let your app's tasks inform the types of help people might need** — an inline view for simple 1–2 step tasks, a tutorial for complex/multistep tasks; directly relate help to the precise action/task at hand and make it easy to dismiss or avoid.
- **Use relevant and consistent language and images in your help content** — match the current context and platform (e.g., don't show a game-controller image for Siri Remote use; don't say "click" for iPhone or "tap" for Mac).
- **Make sure all help content is inclusive** (see Inclusion).
- **Avoid bloating your help content by explaining how standard components or patterns work.** Describe only the specific action/task a standard element performs in your app; for unique or nonstandard controls, orient people quickly with animation or graphics rather than lengthy description.

Creating tips (`TipKit`) — a tip is a small, transient view briefly describing how to use a feature:
- **Use the most appropriate tip type** — a popover tip preserves content flow; an inline tip keeps surrounding info visible; an annotation-style inline tip points to a specific UI element; a hint-style tip is used when unrelated to specific UI.
- **Use tips for simple features** — if a feature requires more than three actions, it's probably too complicated for a tip.
- **Make tips short, actionable, and engaging** — direct, action-oriented language; keep tips to one or two sentences; avoid promotional or off-context content.
- **Define rules to help ensure your tips reach the intended audience** — parameter-based or event-based eligibility rules; set display frequency for multiple tips at a reasonable cadence (e.g., once every 24 hours).
- **If there's an image or symbol people associate with the feature, consider including it, and prefer the filled variant.** Avoid repeating the same image in both the tip and the UI if the tip already connects directly to it.
- **Use buttons to direct people to information or options** (settings, or additional resources like a setup flow).
**Platforms:** No additional considerations for iOS, iPadOS, tvOS, or watchOS.
### macOS, visionOS
A *tooltip* (called a *help tag* in user documentation) briefly describes how to use a component — appears on pointer hover in Mac apps (including iPhone/iPad apps running on Mac), or on look or pointer hover in visionOS (`help(_:)`).
- **Describe only the control that people indicate interest in** — not nearby controls or the larger task.
- **Explain the action or task the control initiates**, often beginning with a verb (e.g., "Restore default settings").
- **In general, avoid repeating a control's name in its tooltip.**
- **Be brief** — limit content to a maximum of 60 to 75 characters (localization often changes length); use sentence fragments and omit articles.
- **Use sentence case**; omit ending punctuation in complete sentences unless required for consistency with your app's style.
- **Consider offering context-sensitive tooltips** (e.g., different text per control state).

## Onboarding
Source: https://developer.apple.com/design/human-interface-guidelines/onboarding
Onboarding gives people a quick start using the app; ideally people understand the app just by experiencing it, but when onboarding is necessary, it should be fast, fun, and optional, occurring after Launching completes (not part of the launch experience).
- **Teach through interactivity** — let people safely test an action, discover a feature, or try a game mechanic rather than just viewing instructional material.
- **Consider providing a collection of context-specific tips instead of a single onboarding flow** (`TipKit`) — display instructions near the relevant area of the interface.
- **If you need to present a prerequisite onboarding flow, design a brief, enjoyable experience** that doesn't require memorizing a lot of information — quick, entertaining onboarding is more likely to be completed.
- **If it makes sense to offer a separate tutorial, consider making it optional** — if people skip it on first launch, don't present it again on subsequent launches, but keep it easy to find later (help, account, or settings area).
- **Keep onboarding content focused on the experience you provide** — people don't need to learn how to use the system or the device.

Additional content:
- **Briefly display a splash screen if necessary** — a beautiful graphic that communicates succinctly, shown just long enough to absorb at a glance.
- **Don't let large downloads hinder onboarding** — include enough media/content in the software package to prevent wait times.
- **Avoid displaying licensing details within your onboarding flow.** Let the App Store display agreements/disclaimers; if you must include them, integrate them in a balanced way that doesn't disrupt the experience.

Additional requests:
- **Postpone nonessential setup flows or customization steps** — provide reasonable defaults so most people can start immediately.
- **If your app or game needs access to private data or resources before it can function, consider integrating the permission request into your onboarding flow** to explain the benefit; otherwise present the request when people first access the function that relies on it (see Requesting permission).
- **Prefer letting people experience your app or game before prompting them for ratings or purchases.**
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Playing audio
Source: https://developer.apple.com/design/human-interface-guidelines/playing-audio
Devices play audio through internal/external speakers, headphones, and wirelessly via Bluetooth or AirPlay, controlled through volume buttons, the Ring/Silent switch, headphone controls, Control Center, and third-party accessory controls; apps must behave as people expect as they change volume and output.
- **Silence**: a device in silent mode plays only audio people explicitly initiate (media playback, alarms, audio/video messaging); nonessential sounds (keyboard clicks, sound effects, soundtracks) are silenced.
- **Volume**: system volume governs all sound, including music and in-app effects, except the iPhone ringer volume, which is adjustable separately in Settings.
- **Headphones**: connecting reroutes sound automatically without interruption; disconnecting pauses playback immediately.
- **Adjust levels automatically when necessary — don't adjust the overall volume.** Your app can adjust relative, independent levels, but system volume always governs final output.
- **Permit rerouting of audio when possible** (e.g., to a living room stereo, car radio, Apple TV) unless there's a compelling reason not to.
- **Use the system-provided volume view** (`MPVolumeView`) for a volume slider and audio rerouting control; you can customize the slider's appearance.
- **Choose an audio category that fits the way your app or game uses sound** (`AVAudioSession.Category`):

| Category | Meaning | Behavior |
| Solo ambient | Sound isn't essential, but silences other audio (e.g., a game with a soundtrack) | Responds to silence switch; doesn't mix; doesn't play in background |
| Ambient | Sound isn't essential, doesn't silence other audio (e.g., a game letting people play music from another app instead of the soundtrack) | Responds to silence switch; mixes; doesn't play in background |
| Playback | Sound is essential, might mix (e.g., an audiobook or language-teaching app) | Ignores silence switch; may/may not mix; can play in background |
| Record | Sound is recorded (e.g., a note-taking app's audio recording mode) | Ignores silence switch; doesn't mix; can record in background |
| Play and record | Sound is recorded and played, potentially simultaneously (e.g., audio messaging or video calling) | Ignores silence switch; may/may not mix; can record and play in background |

- **Respond to audio controls only when it makes sense.** It's fine to respond when actively playing audio, in a clear audio-related context, or connected via Bluetooth/AirPlay; otherwise avoid halting audio playing from another app.
- **Avoid repurposing audio controls** — don't redefine a control's meaning; if your app doesn't support a given control, don't respond to it.
- **Consider creating custom audio player controls only if you need commands the system doesn't support** (e.g., custom skip increments, or content related to the playing audio like a sports score).
- **Let other apps know when your app finishes playing temporary audio** by flagging your audio session appropriately (`notifyOthersOnDeactivation`).

Handling interruptions:
- **Determine how to respond to audio-session interruptions.** E.g., tell the system to avoid interrupting for an incoming call unless accepted; a VoIP app must end a call when the iPad Smart Folio closes (which mutes the mic and by default interrupts the session), and must avoid auto-restarting/unmuting the session on Folio reopen without the person's knowledge (`Handling audio interruptions`).
- **When an interruption ends, determine whether to resume audio playback automatically.** Interruptions can be *resumable* (e.g., an incoming call) or *nonresumable* (e.g., a new music playlist) — a media playback app should check resumability before resuming; a game can resume unconditionally since it plays audio without an explicit user choice (`shouldResume`).
**Platforms:**
### iOS, iPadOS
Use the system's sound services (`Audio Services`) to play short sounds and vibrations.
### macOS
Notification sounds mix with other audio by default.
### tvOS
The system plays audio only when people initiate it, through app/game interactions or device calibrations — tvOS doesn't play sounds for components like alerts or notifications.
### visionOS
The system combines audio algorithms with information about physical surroundings to produce *Spatial Audio* — sound perceived as coming from specific locations, not just speakers.
> Important: As in every platform, avoid communicating important information using only sound — always provide additional ways to understand your app (see Accessibility).
Now Playing app audio pauses automatically when its window closes; audio from a non-Now-Playing app can duck when people look away from it.
- **Prefer playing sound** — an app without sound, especially in an immersive moment, can feel lifeless or broken.
- **Design custom sounds for custom UI elements** to help people locate and receive feedback from them.
- **Use Spatial Audio to create an intuitive, engaging experience** — *ambient audio* provides pervasive sounds that anchor people in a virtual world, and an *audio source* sounds like it comes from a specific object.
- **Consider defining a range of places from which your app sounds can originate** — sound continues from a window's location as people move it.
- **Consider varying sounds that people could perceive as repetitive over time** (e.g., the system subtly varies the virtual keyboard's pitch/volume) — randomize a sound file's pitch and volume during playback rather than creating different files.
- **Decide whether you need to play sound that's fixed to the wearer or tracked by the wearer.** *Fixed* sound is perceived as pointed at the person regardless of look direction; *tracked* sound is perceived as coming from a particular object. Tracked sound generally enhances realism; fixed sound suits certain cases (e.g., Mindfulness uses fixed sound to envelop the wearer in a peaceful setting).
### watchOS
The system manages audio playback; an app can play short clips in the foreground, or longer audio continuing even when the wrist lowers or people switch apps (`Playing Background Audio`).
- **Use the recommended encoding values for media assets** — 64 kbps HE-AAC for good quality with lower data requirements.
- **Consider presenting a Now Playing view** so people can control current/recently played audio without leaving your app — it displays info about the current source (possibly another app on Watch or iPhone) and auto-selects the current/most recent source (`Adding a Now Playing View`).

## Playing haptics
Source: https://developer.apple.com/design/human-interface-guidelines/playing-haptics
Playing haptics engages people's sense of touch, complementing visual and auditory feedback with tactile familiarity from the physical world.
- **Use system-provided haptic patterns according to their documented meanings.** If the documented use case doesn't fit your app, use a generic pattern or create your own instead of repurposing a standard one.
- **Use haptics consistently throughout your app or game** — build a clear causal relationship between each haptic and the action that causes it; reusing one pattern for opposite outcomes (e.g., failure and success) is confusing.
- **Prefer using haptics to complement other feedback in your app or game** — match the intensity and sharpness of a haptic to the animation it accompanies; you can synchronize sound with haptics (`Delivering Rich App Experiences with Haptics`).
- **Avoid overusing haptics** — occasional haptics feel right, but frequent ones become tiresome; user testing can help find the right balance (the best haptic experience is often one people aren't conscious of, but miss when it's off).
- **In most apps, prefer playing short haptics that complement discrete events.** Long-running haptics can enhance gameplay but can dilute meaning and distract in an app; on Apple Pencil Pro, continuous/long-lasting haptics don't clarify writing/drawing and can make holding the pencil less pleasant.
- **Make haptics optional** — let people turn off or mute haptics and still enjoy the app or game.
- **Be aware that playing haptics might impact other user experiences** — ensure vibrations don't disrupt features like the camera, gyroscope, or microphone.

Custom haptics — two basic building blocks:
- *Transient* events are brief and compact, feeling like taps or impulses (e.g., tapping the Flashlight button on the Home Screen).
- *Continuous* events feel like sustained vibrations (e.g., the lasers effect in a message).
- Both support control of *sharpness* (soft/rounded/organic vs. crisp/precise/mechanical) and *intensity* (strength). Combining transient/continuous events, varying sharpness/intensity, and adding optional audio produces a wide range of haptic experiences (`Core Haptics`).
**Platforms:**
### iOS
On supported iPhone models: standard UI components (toggles, sliders, pickers) play Apple-designed system haptics by default; a feedback generator (`UIFeedbackGenerator`) plays predefined patterns in three categories — Notification (feedback about a task/action outcome, e.g., depositing a check or unlocking a vehicle), Impact (a physical metaphor complementing a visual experience, e.g., a tap on snap-into-place or a thud on collision), Selection (feedback while a UI element's value is changing).
### macOS
With a Magic Trackpad, apps can provide one of three haptic patterns in response to a drag operation or force click (`NSHapticFeedbackPerformer`):
| Pattern | Description |
| Alignment | Indicates alignment of a dragged item (e.g., aligning shapes, scaling to fit, positioning, or reaching a scrubber's min/max) |
| Level change | Indicates movement between discrete pressure levels (e.g., fast-forward speed changes) |
| Generic | General feedback when the other patterns don't apply |
### watchOS
Apple Watch Series 4 and later provides haptic feedback for the Digital Crown — linear haptic detents by default; some system controls (e.g., table views) provide detents as new items scroll onto the screen (`WKHapticType`).

## Playing video
Source: https://developer.apple.com/design/human-interface-guidelines/playing-video
System-provided video players embed rich playback experiences in iOS, iPadOS, macOS, tvOS, and visionOS, supporting aspect-ratio playback modes and, on most platforms, Picture in Picture (PiP).
The system selects a default playback mode based on aspect ratio (people can switch during playback):
- Full-screen / *aspect-fill* mode — video scales to fill the display, some edge cropping may occur; default for wide video (2:1 through 2.40:1) (`resizeAspectFill`).
- Fit-to-screen / *aspect* mode — the entire video is visible, letterboxing/pillarboxing as needed; default for standard video (4:3, 16:9, up to 2:1) and ultrawide video (above 2.40:1) (`resizeAspect`).
In visionOS and tvOS, the built-in player also provides *transport controls* (e.g., subtitles, audio language, favoriting) and, below them, *content tabs* (Info, Episodes, Chapters); in visionOS, transport controls appear as Ornaments.
- **Use the system video player to give people a familiar and convenient experience.** If a custom player is truly required, reference the system player's behavior/interface — diverging can cause frustration since people won't know which habitual interactions still work.
- **Always display video content at its original aspect ratio.** Embedded letterbox/pillarbox padding can prevent the system from correctly scaling video for the current playback mode, making it appear smaller and preventing correct display in edge-to-edge, non-full-screen contexts like iPad PiP.
- **Provide additional information when it adds value** — image, title, description, and other metadata (`externalMetadata`) in iOS, iPadOS, tvOS, visionOS — but restrict it so it doesn't obscure media playback.
- **Support the interactions people expect, regardless of input device** — e.g., pressing Space to play/pause on Apple Vision Pro, Mac, iPhone, iPad, Apple TV; familiar Siri Remote gestures on Apple TV.
- **If people need to access playback options or content-specific information in your tvOS app, consider adding a transport control or a custom content tab** — keep actions to a step or two and content succinct so people return quickly to viewing.
- **Avoid allowing audio from different sources to mix as viewers switch between modes** (e.g., PiP video muted by the system, then unmuted while another app's background music plays without handling secondary audio correctly) (`silenceSecondaryAudioHintNotification`).

Integrating with the TV app:
- **Ensure a smooth transition to your app** — the TV app fades to black and doesn't show your launch screen; present your own black screen immediately before starting or resuming content.
- **Show the expected content immediately** — jump straight from your black screen into content; avoid splash screens, detail screens, or intro animations. If an interstitial element must appear first, let people choose Select to step through it or Play to skip straight to playback.
- **Avoid asking people if they want to resume playback** — resume automatically without confirmation.
- **Play or pause playback when people press Space on a connected Bluetooth keyboard.**
- **Make sure content plays for the correct viewer** — auto-switch to a profile the TV app's request specifies; if unspecified, ask the viewer to choose one before playback so future requests can use it.
- **Use the previous end time when resuming playback of a long video clip.**
Loading content: avoid loading screens if content loads quickly; if loading takes more than two seconds, show a black loading screen with a centered activity spinner and no surrounding content. Start playback immediately once enough content loads, continuing to load the rest in the background. Minimize loading screen content (minimal branding, keep the black background for a seamless transition).
Exiting playback: show a contextually relevant screen — a detail view for the content just watched with a resume option, or if unavailable, a menu listing that content or your app's main menu. Be prepared for an immediate exit by preparing the exit view as soon as possible after the playback notification.
**Platforms:** No additional considerations for iOS, iPadOS, or macOS.
### tvOS
**Defer to content when displaying logos or noninteractive overlays above video** — small/unobtrusive only; avoid large, distracting overlays. Some devices are prone to image retention, so keep overlays short and prefer translucent SDR graphics to bright, opaque content. **Show interactive overlays gracefully** (quizzes, surveys, progress check-ins) — implement a minimum delay of 0.5 seconds to pause playing media before displaying the overlay, and give a clear way to dismiss it and resume.
### visionOS
**Help people stay comfortable when playing video** — let them choose when to start playback, use a small resizable playback window, and make sure people can see their surroundings during playback. **In a fully immersive experience, avoid letting virtual content obscure playback or transport controls** — the system automatically places the player at a predictable, optimal-viewing location. **Avoid automatically starting a fully immersive video playback experience** without warning. **Create a thumbnail track if you want to support scrubbing** — supply thumbnails 160 px in width each (`HTTP Live Streaming (HLS) Authoring Specification for Apple Devices > Trick Play`). **Avoid expanding an inline video player to fill a window** — playback controls then appear in the player's plane, not floating in an ornament; inline video should stay 2D with window content visible around it. **Use a RealityKit video player** for video in a splash screen or transitional view — correct aspect ratio for 2D/3D, supports closed captions, and can play video as a surface effect on a custom view or object (`AVPlayerViewController`, `RealityKit`).
### watchOS
The system manages video playback; apps can play short clips in the foreground via an inline movie element or a separate interface (`VideoPlayer`).
- **Keep video clips short** — prefer no longer than 30 seconds; longer clips consume more disk space and require longer wrist-raised periods, causing fatigue.
- **Use the recommended sizes and encoding values for media assets** — avoid scaling video clips, which hurts performance and appearance:

| Attribute | Value |
| Video codec | H.264 High Profile |
| Video bit rate | 160 kbps at up to 30 fps |
| Resolution (full screen) | 208x260 px (portrait orientation) |
| Resolution (16:9) | 320x180 px (landscape orientation) |
| Audio | 64 kbps HE-AAC |

- **Avoid creating a poster image that looks like a system control** — people should understand it's tappable for playback.
- **Consider creating a poster image that represents a video clip's contents**, helping people decide whether to view it; avoid images unrelated to the content or mistakable for a control.

## Printing
Source: https://developer.apple.com/design/human-interface-guidelines/printing
An iOS, iPadOS, macOS, or visionOS app can integrate system-provided print functionality, presenting custom printer- and document-specific options if necessary.
- **Make printing discoverable** — a Print item in a macOS app's File menu, or a toolbar button that opens an action sheet in iOS/iPadOS. A macOS toolbar Print button can be optional and added during toolbar customization.
- **Present a printing option only when it's possible.** Dim the macOS File menu's Print item, or remove the Print action from the iOS/iPadOS action sheet, when there's nothing to print or no printers are available; dim or hide any custom print button similarly.
- **Present relevant printing options** (page range, multiple copies, double-sided) via the system-provided view when the printer supports them.
**Platforms:** No additional considerations for iOS, iPadOS, or visionOS. Not supported in tvOS or watchOS.
### macOS
- **If your app offers app-specific print options the system doesn't, consider creating a custom category for the print panel** alongside default categories like Layout, Paper Handling, and Media & Quality — give it a unique name (e.g., your app name) (e.g., Keynote's presenter-notes, slide-background, and skipped-slide options).
- **If your app supports document-specific page settings, consider presenting a page setup dialog** — rarely changed settings for page size, orientation, and scaling — while avoiding reimplementing options the system already provides (e.g., orientation, reverse-order printing).
- **Make sure interdependencies between options are clear** (e.g., enabling double-sided printing disables printing on transparencies).
- **Separate advanced features from frequently used features** — consider a disclosure control labeled "Advanced Options."
- **Consider letting people preview the effect of a setting** (e.g., a thumbnail updating to show a tone-control change).
- **Consider storing modified settings with the document** — at minimum until the document is closed, in case people print it again.

## Ratings and reviews
Source: https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews
People often view an app's ratings and reviews before downloading it; a great overall experience combined with well-timed feedback requests encourages positive ones.
- **Ask for a rating only after people have demonstrated engagement with your app or game** — e.g., completing a game level or a significant task. Never on first launch or during onboarding, since people haven't had time to form an opinion and may respond negatively.
- **Avoid interrupting people while they're performing a task or playing a game** — look for natural breaks or stopping points.
- **Avoid pestering people** — allow at least a week or two between requests, prompting again only after additional engagement.
- **Prefer the system-provided prompt** (iOS, iPadOS, macOS) — checks for previous feedback and displays an in-app prompt if there isn't any; people can respond or dismiss with a single tap/click, or opt out of all such prompts. The system automatically limits the prompt to three occurrences per app within a 365-day period (`RequestReviewAction`).
- **Weigh the benefits of resetting your summary rating** (reflects the current version) **against the potential disadvantage of showing fewer ratings** overall, which can discourage some downloads (`Reset app summary rating`).
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Searching
Source: https://developer.apple.com/design/human-interface-guidelines/searching
People use search fields, scoping/filtering, and Spotlight to find content on their device, within an app, and within a document or file.
- **If search is important, give it a primary position in your app or view** (e.g., a search field in the bottom toolbar alongside other important actions, or a dedicated Search tab in tab-bar apps).
- **Aim to make your app's content searchable through a single location.** For apps with clearly distinct sections, a local search that acts as a filter on the current view can still be useful.
- **Clearly display the current scope of a search** — descriptive placeholder text, scope bars and tokens, or a title.
- **Provide suggestions to make searching easier** — a person's recent searches before typing, or predictive suggestions while typing (`searchSuggestions(_:)`).
- **Take privacy into consideration before displaying search history** — provide a way to clear it if you show it.

Systemwide search:
- **Make your app's content searchable in Spotlight** by making it indexable and specifying descriptive metadata.
- **Define metadata for custom file types you handle** via a Spotlight File Importer plug-in (`CSImportExtension`).
- **Use Spotlight to offer advanced file-search capabilities within your app** — e.g., a button that instantly initiates a Spotlight search based on the current selection, with a custom results view.
- **Prefer using the system-provided open and save views**, which generally include a built-in search field for the entire system.
- **Implement a Quick Look generator if your app produces custom file types**, so Spotlight and other apps can show previews.
**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Settings
Source: https://developer.apple.com/design/human-interface-guidelines/settings
The system-provided Settings app handles systemwide and (on some platforms) per-app settings; a custom in-app settings area can hold general options, and task-specific options are best kept in-context.
- **Aim to provide default settings that give the best experience to the largest number of people** (e.g., auto-maximize game performance for the device rather than asking players to choose).
- **Minimize the number of settings you offer** — too many make the experience feel less approachable and harder to navigate.
- **Make settings available in ways people expect** — Command-Comma (,) with a connected physical keyboard, or Esc in a game.
- **Avoid using settings to ask for setup information you can get in other ways** (e.g., auto-detect a connected controller; detect Dark Mode automatically).
- **Respect people's systemwide settings and avoid including redundant versions of them** in your custom settings area (accessibility accommodations, scrolling behavior, authentication methods).

General settings:
- **Put general, infrequently changed settings in your custom settings area** (e.g., window configuration, game-saving behavior or keyboard mappings, account-related options).

Task-specific options:
- **When possible, prefer letting people modify task-specific options without going to your settings area** (show/hide view parts, reorder a collection, filter a list) — keep them discoverable in the screens they affect.
> Note: In games, players tend to adjust their approach to a specific task as part of gameplay, not as a settings option.

System settings:
- **Add only the most rarely changed options to the system-provided Settings app.** If you do, consider a button in your interface that opens it directly.
**Platforms:** No additional considerations for iOS, iPadOS, tvOS, or visionOS.
### macOS
Choosing Settings in the App menu opens a custom settings window, typically with a toolbar containing panes.
- **Include a settings item in the App menu.** Avoid adding settings buttons to a window's toolbar, which decreases space for essential frequent commands; document-level options go in the File menu.
- **Dim a settings window's minimize and maximize buttons** — quick to reopen via Command-Comma, no need to keep it in the Dock or expand it.
- **In your settings window, use a noncustomizable toolbar** that remains visible and always indicates the active toolbar button.
- **Update the window's title to reflect the currently visible pane** — if there are no multiple panes, use "*App Name* Settings."
- **Restore the most recently viewed pane** when the window reopens.
### watchOS
Apps and games don't add custom settings to the system-provided Settings app — instead make a small number of essential options available at the bottom of the main view, or let people use a More menu.

## Undo and redo
Source: https://developer.apple.com/design/human-interface-guidelines/undo-and-redo
Undo and redo give people easy ways to reverse recent actions, letting them explore and experiment safely, but people can lose track of which action is being targeted, so predictability matters.
- **Help people predict the results of undo and redo as much as possible** — describe the result in the shake-to-undo alert on iPhone; modify undo/redo menu item labels to identify the result (e.g., "Undo Typing," "Redo Bold").
- **Show the results of an undo or redo.** If the affected content or area is no longer visible, highlight the result (e.g., scroll to show a restored paragraph) so people don't think the action had no effect and repeat it needlessly.
- **Let people undo multiple times** — avoid unnecessary limits; people expect to undo every action since a logical step like opening a document or saving their work.
- **Consider giving people the option to revert multiple changes at once** — batch undo of related incremental adjustments, or undo everything since opening/saving.
- **Provide undo and redo buttons only when necessary.** People generally expect system-supported initiation (Edit menu items, keyboard shortcuts on Mac/iPad, shaking iPhone); if dedicated buttons are important, use standard system-provided symbols in a toolbar.
**Platforms:** No additional considerations for visionOS. Not supported in tvOS or watchOS.
### iOS, iPadOS
**Avoid redefining standard gestures for undo and redo** — a three-finger swipe or shaking the iPhone. **Briefly and precisely describe the operation to be undone or redone.** The undo/redo alert title automatically includes a prefix of "Undo " or "Redo " (with trailing space); provide an additional word or two describing what's being undone/redone (e.g., "Undo Name," "Redo Address Change").
### macOS
**Place undo and redo commands in the Edit menu and support the standard keyboard shortcuts** — Command-Z for undo, Shift-Command-Z for redo.

## Workouts
Source: https://developer.apple.com/design/human-interface-guidelines/workouts
A great workout or fitness experience encourages engagement with the current activity and helps people track progress across Apple Watch, iPhone, iPad, and larger or more stationary devices like iPad Pro, Mac, and Apple TV.
- **In a watchOS fitness app, use workout sessions to provide useful data and relevant controls** — watchOS keeps the app visible as time passes between wrist raises during an active session, so show the data people most care about (elapsed/remaining time, calories burned, distance traveled) and relevant controls (lap or interval markers).
- **Avoid distracting people from a workout with information that's not relevant** — e.g., don't require reviewing the workout list or accessing other app parts mid-workout.
- **Use a distinct visual appearance to indicate an active workout** — a metrics page with real-time updating values and a unique layout helps people recognize an active session at a glance.
- **Provide workout controls that are easy to find and tap** — pause, resume, and stop — with clear feedback indicating when a session starts or stops.
- **Help people understand the health information your app records if sensor data is unavailable during a workout** — e.g., water may prevent a heart-rate measurement, but distance and calories can still be tracked. If your app supports the *Swimming* or *Other* workout types, explain the situation using language similar to the system Workout app, e.g.:

| Example text from the Workout app |
| GPS is not used during a Pool Swim, and water may prevent a heart-rate measurement, but Apple Watch will still track your calories, laps, and distance using the built-in accelerometer. |
| In this type of workout, you earn the calorie equivalent of a brisk walk anytime sensor readings are unavailable. |
| GPS will only provide distance when you do a freestyle stroke. Water might prevent a heart-rate measurement, but calories will still be tracked using the built-in accelerometer. |

- **Provide a summary at the end of a session** confirming completion and displaying recorded information; consider enhancing it with Activity rings so people can check their current progress.
- **Discard extremely brief workout sessions** — if a session ends a few seconds after starting, either discard the data automatically or ask people if they want to record it as a workout.
- **Make sure text is legible for when people are in motion** — large font sizes, high-contrast colors, and the most important information arranged for easy reading.
- **Use Activity rings correctly.** The Activity rings view is an Apple-designed element whose colors and meanings match those in the Activity app — use it only for its documented purpose.
**Platforms:** No additional considerations for iOS, iPadOS, or watchOS. Not supported in macOS, tvOS, or visionOS.
