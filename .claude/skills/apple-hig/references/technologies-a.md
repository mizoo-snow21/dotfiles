# HIG — Technologies (AirPlay … In-app purchase)
Covers: airplay, always-on, app-clips, apple-pay, augmented-reality, carekit, carplay, game-center, generative-ai, healthkit, homekit, icloud, id-verifier, imessage-apps-and-stickers, in-app-purchase

## AirPlay
Source: https://developer.apple.com/design/human-interface-guidelines/airplay
AirPlay lets people stream media content wirelessly from iOS, iPadOS, macOS, and tvOS devices to Apple TV, HomePod, and TVs and speakers that support AirPlay.
- **Prefer the system-provided media player.** Supports chapter navigation, subtitles, closed captioning, AirPlay streaming; consider a custom player only if the system one doesn't meet your needs (`AVPlayerViewController`).
- **Provide content in the highest possible resolution.** Your HLS playlist needs the full range of resolutions so quality matches the streaming target device (e.g., 720p content looks low quality streamed to a 4K TV).
- **Stream only the content people expect.** Avoid streaming background loops/short experiences that only make sense in-app (`usesExternalPlaybackWhileExternalScreenIsActive`).
- **Support both AirPlay streaming and mirroring** for maximum flexibility.
- **Support remote control events** so people can play/pause/fast-forward from the lock screen, Siri, or HomePod (Remote command center events).
- **Don't stop playback when your app enters the background or the device locks.** Also avoid automatic mirroring in this scenario — people don't want other content streamed without explicitly choosing to.
- **Don't interrupt another app's playback unless your app is starting immersive content.** Auto-playing/inline videos should play locally only, letting current playback continue (`ambient`).
- **Let people use other parts of your app during playback.** The app must remain functional; other in-app videos shouldn't begin playing and interrupt the stream.
- **If necessary, provide a custom media-playback interface.** Match the system player's button appearance/behavior including distinct start/occurring/unavailable states; use only Apple-provided symbols; position the AirPlay icon in the lower-right corner (iOS/iPadOS 16+).

**Using AirPlay icons**
- Black icon: on white/light backgrounds when other tech icons also appear in black.
- White icon: on black/dark backgrounds when other tech icons also appear in white.
- Custom color icon: when other tech icons also appear in that same color.
- **Position the AirPlay icon consistently with other technology icons** (same shape treatment if others appear within shapes).
- **Don't use the AirPlay icon or name in custom buttons or interactive elements.** Noninteractive use only.
- **Pair the icon with the name AirPlay correctly.** Name below or beside the icon, same font as the rest of your layout; don't use the icon as a text replacement.
- **Emphasize your app over AirPlay.** Keep references less prominent than your app name/main identity.

**Referring to AirPlay**
- **Use correct capitalization:** "AirPlay" — uppercase A and P, rest lowercase; all-uppercase allowed only if the whole layout is all-uppercase.
- **Always use "AirPlay" as a noun** (e.g., "Use AirPlay to listen on your speaker").
- **Use terms like "works with," "use," "supports," "compatible"** (e.g., "AirPlay-enabled speaker").
- **Use the name "Apple" with "AirPlay" if desired** (e.g., "Compatible with Apple AirPlay").
- **Refer to AirPlay directly if it adds clarity** (e.g., "[App Name] now supports AirPlay").

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS. Not supported in watchOS.

## Always On
Source: https://developer.apple.com/design/human-interface-guidelines/always-on
On devices that include the Always On display, the system can continue to display an app's interface when people suspend their interactions with the device.
The system dims the display and minimizes onscreen motion to give glanceable, low-power, privacy-preserving info. iPhone 14 Pro/Pro Max show Lock Screen Widgets/Live Activities face-up; Apple Watch dims the watch face while the app is frontmost or running a background session. Notifications still display in either case; tapping exits Always On.
- **Hide sensitive information.** Redact personal info like bank balances or health data, including anything that might be visible in a notification (see Notifications).
- **Keep other types of personal information glanceable when it makes sense** (e.g., pace/heart rate on Apple Watch, flight arrival on iPhone). People can turn off Always On if they don't want any info visible.
- **Keep important content legible and dim nonessential content.** Increase dimming on secondary text, images, and color fills; remove rich images or dim large color-fill areas.
- **Maintain a consistent layout.** Avoid distracting changes at Always On start/end; transition interactive components to an unavailable appearance rather than removing them; make only infrequent, subtle updates within the Always On context (e.g., pause granular updates, update only on real change). Unnecessary changes are especially distracting on iPhone since it's often left face up.
- **Gracefully transition motion to a resting state; don't stop it instantly.** Smoothly finishing motion communicates the transition rather than suggesting something went wrong.

**Platforms:** No additional considerations for iOS or watchOS. Not supported in iPadOS, macOS, tvOS, or visionOS.

## App Clips
Source: https://developer.apple.com/design/human-interface-guidelines/app-clips
An App Clip is a lightweight version of your app or game that provides an on-the-go or demo experience that's instantly available, without requiring a full download from the App Store.

**Designing your App Clip**
- **Allow people to complete a task or a demo** without requiring the full app install.
- **Focus on essential features.** Reserve advanced/complex features for the full app.
- **Don't use App Clips solely for marketing purposes.** Must provide real value; no ads.
- **Avoid using web views.** Prefer native components; offer a quick website link instead if only web components are available.
- **Design a linear, easy-to-use, focused UI.** No tab bars/complex navigation/settings; minimize screens and entry forms.
- **On launch, show the most relevant part of your App Clip.** Skip unnecessary steps.
- **Ensure people can use your App Clip immediately.** Include all required assets, omit splash screens, never make people wait.
- **Ensure your App Clip is small.** Reduce unnecessary code/unused assets; avoid downloading extra data.
- **Make the App Clip shareable,** including links to specific points within it.
- **Make it easy to pay** — consider Apple Pay for express checkout/shipping info entry.
- **Avoid requiring an account before people benefit.** Defer account creation until after task completion if possible; if required, minimize info needed (e.g., Sign in with Apple).
- **Provide a familiar, focused experience in your full app after install** — no extra steps like re-login when transitioning from the App Clip.

*Preserving privacy* — App Clips can't perform background operations.
- **Limit the data you store and handle yourself.** Store securely; don't rely on data persisting between launches (the system may remove the App Clip and its data); store login info off-device securely.
- **Consider offering Sign in with Apple.**
- **Offer a secure, privacy-respecting way to pay** (e.g., Apple Pay).

*Showcasing your app* — App Clips don't appear on the Home Screen and are removed after inactivity; the App Clip card and system app banner let people visit the full app's App Store page; you can also display an overlay to prompt a download.
- **Don't compromise the UX by asking people to install the full app.** Weigh whether the card/banner already give enough incentive; for demos, let people fully experience the demo first.
- **Pick the right time to recommend your app.** Display an SKOverlay when someone completes a task or reaches a natural pause.
- **Recommend your app in a nonintrusive, polite way.** Don't ask repeatedly or interrupt a task; push notifications aren't appropriate for this.

*Limiting notifications* — App Clips can schedule/receive notifications for up to 8 hours after launch.
- **Only ask for extended notification permission if your App Clip's functionality spans more than a day.**
- **Keep notifications focused.** No purely promotional notifications; only send in response to an explicit user action.
- **Use notifications to help people complete a task.**

*Creating App Clips for businesses* (one App Clip powering several App Store Connect experiences)
- **Use consistent branding.** Tone down your own branding; the business's branding must be clearly visible.
- **Consider multiple businesses/locations.** Handle switching between recent businesses/locations and verify location at launch.

**Creating content for an App Clip card**
- **Be informative** about features/tasks/content offered.
- **Prefer photography and graphics.** Avoid app-UI screenshots.
- **Avoid using text** in the header image (not localizable, hard to read).
- **Adhere to image requirements:** 1800x1200 px PNG or JPEG, no transparency.
- **Use concise copy.** Title ≤30 characters, subtitle ≤56 characters.
- **Pick the right action verb:** *View* (media, informational/educational content), *Play* (games), *Open* (everything else).

**App Clip Codes** — distinct, immediately recognizable; always use Apple-provided designs. Two variants: *scan-only* (camera icon center) or *NFC-integrated* (iPhone icon center).
- Interacting: scan-only via Camera app or Control Center Code Scanner; NFC-integrated by holding the device close, or via NFC Tag Reader/Camera app/Code Scanner.
- Displaying: use NFC-integrated where physically accessible (tabletop, register, storefront window, signage, gift card/coupon); use scan-only where physically inaccessible or digital (posters, print ads, signage behind a counter, digital displays/emails/social media).
- **Include the App Clip logo when space allows.** Use the design without the logo if clear-space requirements can't be met, or on disposable paper/plastic items, or items tied to gambling/drinking (e.g., playing cards, poker chips, bar coasters). The logo is always part of the badge design below the code — never use it alone.
- **Place on a flat or cylindrical surface only.** On a cylinder, code width must not exceed 1/6 of the circumference.
- **Help the code remain as flat as possible.** Avoid deformable materials (paper/plastic/fabric) that fold/crumple; mount on something rigid (e.g., a card) if unavoidable; stickers must adhere well to flat surfaces.
- **Place it where reliable scanning is likely** (adequate light for scan-only codes, no requirement to scan from a wide angle).
- **Make sure the code is unobstructed.** No overlaying text/logos/images; never animate or dim it.
- **Display the code upright.** Don't rotate the code or angle the center glyph.
- **Don't create codes that are too small.**

| Type | Minimum size |
|---|---|
| Printed communications | Minimum diameter of 3/4 inch (1.9 cm) |
| Digital communications | Minimum 256×256 px; PNG or SVG |
| NFC-integrated | Embedded tag ≥35 mm diameter (or equivalent); e.g., a 35 mm tag needs a printed code ≥1.37 in / 3.48 cm diameter |

- Distance-to-code-size ratio: no more than 20:1, ideally 10:1 (e.g., a code scanned from 40 in/101 cm away needs ≥4 in/10.16 cm diameter).
- Next to a QR code or other scannable item, size the App Clip Code at least as large as that item.
- **Provide enough clear space** around the code — minimum equal to the space between the center glyph and the circular code; leave enough space between adjacent codes for reliable scanning of each.

*Using clear messaging*
- **Add a clear call to action,** especially without the logo — e.g. "Scan to [X]," "Scan using the camera on your iPhone or iPad to [X]," "Hold your iPhone near the [object] to launch an App Clip that [X]."
- **Adhere to Guidelines for Using Apple Trademarks.** No Apple trademarks in your app name/images; always use title case for "App Clips"/"App Clip Code."

*Customizing your App Clip Code* — via App Store Connect or the App Clip Code Generator CLI.
- **Always use the generated code as-is.** No custom design or modification (no filters, color augmentation, glows/shadows/gradients/reflections); when scaling, preserve aspect ratio and scale all attributes (e.g., stroke widths).
- **Choose colors with enough contrast for accurate scanning.** Three colors: foreground, background, and a generated third; use a default color pair or custom colors — tools refuse to generate codes with poor-scanning color choices and suggest alternatives.

**Printing guidelines** — always test printed codes before distribution.
- **Use high-quality, non-textured print materials.** Matte finishes; avoid shine/gloss/reflective/holographic overlays and thin laminate; matte laminate if laminating; UV-resistant materials/coatings outdoors; flexographic printing via a professional service, inkjet for desktop printers.
- **Use high-resolution images and printer settings.** Rasterize SVG at ≥600 ppi, print at minimum 300 dpi; calibrate/level the printer; avoid poor color-channel alignment/gamma errors/distortion; on receipt printers, print as close to the paper's max bounds as possible.
- **Use correct color settings converting sRGB SVG to CMYK.** Relative colorimetric (media-relative) intent; "Generic CMYK ICC profile" (CMYK printers) or "Gracol 2013 ICC profile" (CMYKOV printers); allow color tolerance CIELab Delta E of 2.5.
- **Grayscale-only printers:** generate grayscale App Clip Codes only — codes generated in color then printed grayscale scan less reliably.
- **For NFC-integrated codes, choose Type 5 NFC tags** (embedded tag ≥35 mm diameter).
- **For large batches, test the printing workflow and verify printed codes** — small test print runs, templates with padded regions showing the encoded URL/SVG filename for validation, careful file management/versioning/change tracking.
- Verify calibration: use Apple's printer calibration test sheets — one for text-box color-pair print quality, one with two grayscale bars (recalibrate/replace the printer if any gray is light or missing).

**Legal requirements**
- Only Apple-provided codes (via App Store Connect or the CLI tool) following these guidelines are approved for use; stop displaying a code once its App Clip is no longer active.
- Don't use App Clip Code elements (Apple Logo, App Clip mark, code designs) as part of your company/product name; don't seek copyright/trademark registration for them.
- Don't use them in ways that reduce/damage Apple's or App Clips' goodwill/reputation, infringe third-party rights, or cause source confusion.
- Don't add a symbol to generated codes; don't translate Apple trademarks (must stay in English even in non-English text; translated legal notice/credit lines allowed outside the U.S. with Apple's approval).

**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## Apple Pay
Source: https://developer.apple.com/design/human-interface-guidelines/apple-pay
Apple Pay is a secure, easy way to make payments for physical goods and services, donations, and subscriptions in apps and in any browser.
> Note: Use In-app purchase to sell virtual goods in your app, such as premium content, and subscriptions for digital content.

**Offering Apple Pay**
- **Offer Apple Pay on all devices/browsers that support it;** don't present it where unsupported (`PKPaymentAuthorizationController`, `applePayCapabilities`).
- **Make Apple Pay the primary payment option when credentials are available** — don't separate it into a different step/flow (e.g., pre-select it alongside other options).
- **Use Apple Pay buttons only to initiate payment or, when appropriate, the setup process.**
- **A custom Apple Pay-initiating button must not display "Apple Pay" or its logo.** Instead show the Apple Pay mark or reference Apple Pay in text on the same page.
- **Use the Apple Pay mark graphic only to communicate acceptance** — never as/positioned as a button.
- **Don't hide an Apple Pay button or make it appear unavailable.** If unusable (e.g., no size selected), gracefully surface the problem after tap/click.
- **Inform search engines Apple Pay is accepted** if your site uses semantic product markup.
> Important: All websites that offer Apple Pay must include a privacy statement and adhere to the Acceptable use guidelines for Apple Pay on the web.

**Streamlining checkout**
- **Provide a cohesive checkout experience** — integrated branding, avoid opening new pages/windows.
- **If Apple Pay is available, assume people want to use it** — consider first position, larger size, or a separating line.
- **Accelerate single-item purchases with Apple Pay buttons on product detail pages** — for that item only, excluding cart contents; remove it from the cart if already there.
- **Accelerate multi-item purchases with express checkout** (single shipping method/destination for everything in the cart).
- **Support coupons/promo codes directly on the payment sheet,** especially for express checkout.
- **Collect necessary info (e.g., color/size) before the Apple Pay button;** gracefully flag and auto-navigate to missing fields.
- **Collect optional info** (gift messages, delivery instructions) before checkout or after purchase — there's no way to input it on the payment sheet.
- **Gather multiple shipping methods/destinations before showing the payment sheet** (it supports only one method/destination per order).
- **For in-store pickup, help people choose a location before displaying the sheet,** then show that location's address on the sheet.
- **Prefer checkout information from Apple Pay** — fetch the latest even if you have existing data.
- **Avoid requiring account creation before purchase** — ask on the order confirmation page instead, prepopulating fields.
- **Report transaction results in the payment sheet** with clear error messages.
- **Display an order confirmation/thank-you page** after the sheet. Listing Apple Pay there is optional; if shown, place it after the last four digits or as a separate note (e.g., "1234 (Apple Pay)" or "Paid with Apple Pay").

*Customizing the payment sheet*
- **Only present/request essential information** — avoid implying physical delivery (e.g., asking for a shipping address) for electronically delivered items.
- **Display the active coupon/code, or let people enter one,** particularly in express checkout.
- **Let people choose the shipping method in the sheet** — description, cost, and estimated delivery/pickup date (or range) using calendar/time-zone-aware data (`PKDateComponentsRange`).
- **For in-store pickup, consider letting people choose a pickup window** via shipping-method date/time ranges.
- **Use line items for additional charges, discounts, pending costs, add-on donations, and recurring/future payments** (label + cost; frequency for recurring) — not for an itemized product list (`paymentSummaryItems`).
- **Keep line items short** — specific, understandable at a glance, ideally one line.
- **Provide a business name after "Pay" on the total line,** matching the name on bank/credit statements (e.g., "Pay [Business_Name]").
- **If you're not the end merchant, identify both businesses** (e.g., "Pay [End_Merchant_Business_Name (via Your_Business_Name)]").
- **Clearly disclose possible additional costs after authorization** (e.g., distance-based fares, post-delivery tips) via a subtotal marked "Amount Pending" where local regulations allow; ensure the sheet accurately reflects any preauthorized amount.
- **Handle data entry/payment errors gracefully** (see Data validation errors).
- **Defer to the payment sheet for progress information** — avoid extra spinners/progress indicators.

**Displaying a website icon** — sites supporting Apple Pay can show an icon during payment authorization (notably Handoff) and, for subscriptions, in Wallet.
| @2x | @3x |
|---|---|
| 60x60 pt (120x120 px @2x) | 60x60 pt (180x180 px @3x) |

**Handling problems**
- *Data validation errors:* check for problems when the sheet appears, on field changes, and after authentication; system highlights relevant fields — provide customized detail-view error messages (`PKPaymentAuthorizationViewControllerDelegate`, Apple Pay on the Web).
> Note: Before authorization, your app/website only has access to card type and a redacted shipping address, for privacy — still validate what's available and report problems pre-authorization when possible.
- **Avoid forcing compliance with your business logic.** Ignore irrelevant data / infer missing data (e.g., ignore a Zip+4 suffix; accept phone numbers with/without dashes or country code).
- **Accurately report problems to the system** with a custom error message and correct status code (`PKPaymentError`, Apple Pay Status Codes).
- **Explain problems clearly and succinctly.** Reference the field, state exactly what's expected (e.g., "Zip code doesn't match city," not "Address is invalid"); noun phrases, sentence-style capitalization, no ending punctuation; aim for ≤128 characters to avoid truncation.
- *Payment processing problems:* **handle interruptions correctly** — cancel any in-progress payment when the sheet dismisses (cancellation/timeout); people can restart via the Apple Pay button again (`PKPaymentAuthorizationViewControllerDelegate`, `oncancel`).

**Supporting subscriptions** — recurring payments can be fixed or (where local regulations allow) variable; initial authorization can include discounts/fees.
- **Clarify subscription details before showing the payment sheet** (billing frequency, terms); the sheet itself can show billing frequency.
- **Include line items reiterating billing frequency, discounts, and additional upfront fees;** disclose future billing timing if no payment is required now.
- **Clearly communicate trial period terms** via line items: trial amount (incl. $0 if free), regular amount after trial, and the date regular billing begins.
- **Clarify the current payment amount in the total line.**
- **Only show the payment sheet when a subscription change results in additional fees** — no reauthorization needed if cost decreases or stays the same.
> Important: Treat the billing agreement field as a plain-language summary, not a substitute for formal terms; be concise, avoid duplicating info shown elsewhere; leave it blank when in doubt.

**Supporting donations** (approved nonprofits only)
- **Use a line item to identify a donation** (e.g., "Donation $50.00").
- **Streamline checkout by offering predefined donation amounts** (e.g., $25/$50/$100) plus an "Other Amount" option.

**Using Apple Pay buttons** — Apple-provided APIs give Apple-approved captions/fonts/colors/styles, proportional scaling, automatic localization, corner-radius customization, and built-in VoiceOver support.
- **Always use the Apple-provided API to display buttons.** Never create or replicate custom designs (`PKPaymentButtonType`, `PKPaymentButtonStyle`, `WKInterfacePaymentButton`, Apple Pay on the Web).
> Tip: Use the Apple Pay mark graphic to communicate availability wherever payment options are highlighted.

*Button types* — choose to fit your flow's terminology: Apple Pay (generic), Pay (bills/invoices), Check Out with Apple Pay, Continue with Apple Pay, Book with Apple Pay (flights/trips), Donate with Apple Pay (approved nonprofits), Subscribe with Apple Pay, Reload with Apple Pay, Add Money with Apple Pay, Top Up with Apple Pay (all three for adding money to a card/account/service), Order with Apple Pay, Rent with Apple Pay, Support with Apple Pay, Contribute with Apple Pay, Tip with Apple Pay, and the plain Apple Pay button (stylistic/smaller-width fallback; also the system's automatic replacement for an unsupported button type on older OS versions).
- *Set Up Apple Pay button:* use when a device supports Apple Pay but isn't set up yet — shows acceptance and offers setup; display in Settings, a user profile, or an interstitial page.

*Button styles:* **automatic** (system-determined appearance; `PKPaymentButtonStyle.automatic`/`ApplePayButtonStyle`), or choose manually — **Black** (white/light backgrounds with sufficient contrast; not on dark backgrounds), **White with outline** (white/light backgrounds without sufficient contrast; not on dark/saturated backgrounds), **White** (dark backgrounds with sufficient contrast).

*Button size and position*
- **Prominently display the button** — no smaller than other payment buttons; avoid requiring scroll to see it.
- **Position correctly relative to an Add to Cart button** — to its right in a side-by-side layout, above it in a stacked layout.
- **Adjust corner radius to match other buttons** (square or capsule) via `cornerRadius`.
- **Maintain the minimum button size and margins** — title length varies by locale.
> Note: If the specified size can't fit the translated title, the system replaces it with the plain Apple Pay button (no automatic replacement exists for the Set Up Apple Pay button).

| Button | Minimum width | Minimum height | Minimum margins |
|---|---|---|---|
| Apple Pay | 100pt (100px @1x, 200px @2x) | 30pt (30px @1x, 60px @2x) | 1/10 of button's height |
| Book/Buy/Check Out/Donate/Set Up/Subscribe with Apple Pay | 140pt (140px @1x, 280px @2x) | 30pt (30px @1x, 60px @2x) | 1/10 of button's height |

*Apple Pay mark* — communicates acceptance only; not a button.
- **Use only Apple-provided artwork, height-adjustable only** — height ≥ other payment brand marks shown; don't change width/corner radius/aspect ratio, add a trademark symbol or effects (shadows/glows/reflections), remove the border, or flip/rotate/animate it.
- **Maintain a minimum clear space of 1/10 of its height;** don't let it share a border with another graphic/button.

**Referring to Apple Pay** — use exactly as in the Apple Trademark List, never plural or possessive.
- **Capitalize as "Apple Pay"** (uppercase A, uppercase P, rest lowercase); all-uppercase only for an all-caps typographic style.
- **Never use the Apple logo to represent "Apple" in text.** Use ® on first appearance in U.S. body text; omit it when Apple Pay appears as a checkout selection option.
- **Coordinate font face/size with your app/website** — don't mimic Apple typography.
- **Never translate "Apple Pay"** or other Apple trademarks.
- **In a payment-selection context, a text-only description is allowed only if all other options are also text-only** — otherwise use the Apple Pay mark graphic.
- **Follow App Store marketing guidelines** when promoting Apple Pay in an app.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, visionOS, or watchOS. Not supported in tvOS.

## Augmented reality
Source: https://developer.apple.com/design/human-interface-guidelines/augmented-reality
Augmented reality (AR) lets you deliver immersive, engaging experiences that seamlessly blend virtual objects with the real world, using the device's camera to superimpose 3D objects onto a live view (ARKit).
- **Offer AR features only on capable devices.** If AR is the app's primary purpose, restrict availability to ARKit-capable devices; if optional/partial, silently omit unsupported features rather than erroring (Verifying Device Support and User Permission).
> Note: This guidance applies to iOS/iPadOS apps; see ARKit for visionOS immersive AR guidance.

**Best practices**
- **Let people use the entire display** — devote max screen space to the world/objects, avoid control clutter.
- **Strive for convincing illusions** — detailed 3D assets with lifelike textures, proper scale/position on detected surfaces, environment-reflecting lighting/simulated camera grain, top-down diffuse shadows, visuals updated as the camera moves; update scenes 60 times/second to avoid jump/flicker.
- **Consider how reflective virtual surfaces show the environment** — prefer small/coarse reflective surfaces since ARKit reflections are approximations.
- **Use audio and haptics to enhance immersion** — confirm contact events, use background music (Playing audio, Playing haptics).
- **Minimize text in the environment** — only what's necessary.
- **Consider displaying additional info/controls in screen space** (a fixed location, easy to find since it stays put while the AR view moves).
- **Consider indirect (2D, screen-space) controls for persistent controls** — place reachable without adjusting device hold; consider translucency to avoid blocking the scene.
- **Anticipate a wide variety of real-world environments** — communicate app requirements/expectations up front; consider different feature sets per environment.
- **Be mindful of people's comfort** — reduce fatigue by placing objects at a distance that avoids needing to move closer; keep game levels short with downtime.
- **Introduce motion gradually if your app encourages movement** — let people adapt before progressively encouraging it.
- **Be mindful of people's safety** — avoid designs prompting rapid/sweeping/dangerous motions.

**Providing coaching** — the built-in coaching view shows people what to do during initialization and relocalization (`ARCoachingOverlayView`).
- **Hide unnecessary app UI while a coaching view is present** (it appears automatically).
- **If necessary, offer a custom coaching experience,** using the system view as reference.

**Helping people place objects**
- **Show people when to locate a surface and place an object** — use the coaching view; show a custom indicator once a surface is detected, aligned to the plane.
- **When people place an object, immediately integrate it** — don't wait for more accurate data; subtly refine position afterward (e.g., gently nudge back onto the surface) (`ARTrackedRaycast`).
- **Consider guiding people toward offscreen virtual objects** with visual/audible cues.
- **Avoid trying to precisely align objects with detected-surface edges** — boundaries are approximations.
- **Incorporate plane classification info to inform placement** (e.g., furniture only on "floor," game board only on "table").

**Designing object interactions**
- **Let people use direct manipulation when possible** — more immersive/intuitive than indirect controls; indirect controls work better when people are moving around.
- **Let people use standard, familiar gestures** (single-finger drag to move, two-finger rotate to spin) (Gestures).
- **Keep interactions simple** — touch gestures are 2D, AR is 3D.
- **Respond to gestures within reasonable proximity of interactive objects** — assume intent to affect nearby small/thin/distant objects.
- **Let people initiate object scaling when it makes sense** (not for real-world visualization use cases, e.g., furniture shopping).
> Tip: Don't use scaling to simulate distance adjustment — enlarging a distant object just yields a larger object that still looks far away.
- **Be wary of conflicting gestures** (e.g., two-finger pinch vs. two-finger rotate) — test thoroughly.
- **Strive for object movement consistent with the AR environment's physics** — keep moving objects attached to surfaces; avoid jump/vanish/reappear during resize/rotate/move.
- **Explore engaging interaction methods beyond gestures** — motion, proximity (e.g., a character turning its head as a person approaches).

**Offering a multiuser experience** — each participant maps the environment independently; ARKit merges maps automatically (`isCollaborationEnabled`).
- **Consider allowing people occlusion** — let people occlude virtual objects placed behind them.
- **When possible, let new participants join an ongoing multiuser experience** via implicit map merging, unless all must join before it starts.

**Reacting to real-world objects** — app supplies 2D reference images or 3D reference objects; ARKit reports detection (Detecting Images in an AR Experience).
- **When a detected image first disappears, consider delaying removal of attached virtual objects** up to one second, to prevent flicker (ARKit doesn't track position/orientation changes of detected images).
- **Limit reference images in use at once** — best performance at ≤100 distinct images; change the active set by context if more are needed (e.g., by museum location).
- **Limit reference images requiring accurate position tracking** — use a tracked image only when it may move or the attached content is small relative to the image, since position updates are resource-intensive.

**Communicating with people**
- **If instructional text is necessary, use approachable terminology** — avoid technical terms (ARKit, world detection, tracking); use friendly, conversational language (e.g., "Unable to find a surface. Try moving to the side or repositioning your phone" not "Unable to find a plane. Adjust tracking").
- **In a 3D context, prefer 3D hints over 2D text overlays** (e.g., a 3D rotation indicator) unless people aren't responding to contextual hints.
- **Make important text readable** — use screen space for critical labels/annotations/instructions; if displayed in 3D space, face people and use consistent type size regardless of distance.
- **If necessary, provide a way to get more information** via a fitting visual indicator.

**Handling interruptions** — ARKit can't track position/orientation during interruptions (app switch, phone call); *relocalization* restores previous object positions using new information (Managing Session Life Cycle and Tracking Quality).
- **Consider using the coaching view to help people relocalize** (return the device to its previous position/orientation).
- **Consider hiding previously placed virtual objects during relocalization** to avoid flickering, redisplaying them once repositioned.
- **Minimize interruptions if your app supports both AR and non-AR experiences** — e.g., embed non-AR tasks within the AR experience so people don't need to exit/re-enter.
- **Allow people to cancel relocalization** — provide a reset button if coaching doesn't succeed (otherwise it continues indefinitely).
- **Indicate when the front-facing camera can't track a face for more than ~half a second** with a visual indicator; keep any text instructions minimal.

**Suggesting problem resolutions**
- **Let people reset the experience if it doesn't meet expectations** — don't force waiting or struggling with object placement.
- **Suggest possible fixes** using straightforward, friendly language.

| Problem | Possible suggestion |
|---|---|
| Insufficient features detected. | Try turning on more lights and moving around. |
| Excessive motion detected. | Try moving your phone slower. |
| Surface detection takes too long. | Try moving around, turning on more lights, and making sure your phone is pointed at a sufficiently textured surface. |

**Icons and badges**
- **Use the AR glyph as intended** — strictly to initiate an ARKit-based experience; never alter it (other than size/color), repurpose it, or use it with non-ARKit AR experiences.
- **Maintain minimum clear space around the AR glyph:** 10% of the glyph's height.
- **Use AR badges as intended and don't alter them** — collapsed/expanded forms, exclusively to identify objects viewable in AR via ARKit; never recolor, repurpose, or pair with non-ARKit experiences.
- **Prefer the AR badge to the glyph-only badge;** use glyph-only only where space is constrained.
- **Use badging only when your app mixes AR-viewable and non-AR-viewable objects** — redundant if everything supports AR.
- **Keep badge placement consistent and clear** — same corner every time, large enough to see but not occluding photo detail.
- **Maintain minimum clear space around the AR badge:** 10% of the badge's height.

**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, or watchOS.
**visionOS:** ARKit can detect surfaces in a person's surroundings, use hand/finger positions to inform custom gestures, and support interactions incorporating nearby physical objects into immersive experiences.

## CareKit
Source: https://developer.apple.com/design/human-interface-guidelines/carekit
People can use CareKit apps to manage care plans related to a chronic illness like diabetes, recover from an injury or surgery, or achieve health and wellness goals.
CareKit 2.0 has two projects: CareKit UI (prebuilt views) and CareKit Store (a database schema for patients, care plans, tasks, contacts), synchronized seamlessly.

**Data and privacy**
- **Provide a coherent privacy policy** — a required URL during app submission, viewable from the App Store page.
- You must get permission before accessing data via iOS features/capabilities, and protect all data regardless of source (Protecting user privacy).

*HealthKit integration* — lets you request access to share health/fitness data with designated caregivers.
- **Request access to health data only when you need it,** tied to context (e.g., at weigh-in, not at launch); re-request every time access is needed since permissions can change (`requestAuthorization(toShare:read:completion:)`).
- **Clarify your app's intent with descriptive messages on the standard permission screen** — succinct explanation of why/benefit; avoid custom screens replicating it.
- **Manage health data sharing solely through the system's privacy settings** (Settings > Privacy) — don't build additional app screens affecting the flow.

*Motion data* — with permission, determine standing/walking/running/cycling/driving and, when walking/running, step count/pace/flights of stairs; can include custom physical-therapy data (e.g., ResearchKit flexibility/range-of-motion/ambulatory tasks) (Core Motion).

*Photos* — with permission, access camera/photos to share treatment-progress pictures with a care team (`UIImagePickerController`).

*ResearchKit integration* — a CareKit app can incorporate ResearchKit surveys/tasks/charts and its informed-consent module for data permission.

**CareKit views** — three categories, each with default styles: **Tasks** (present prescribed actions, support logging), **Charts** (graphical progress data), **Contact views** (contact info; phone/message/email/map). A view has a header (text, symbol, disclosure indicator, optional separator) and an optional vertical content-subview stack; CareKit UI manages all layout constraints.

*Tasks* — can include Title (required), Schedule (required), Instructions (optional), Group ID (optional). Five styles:
- **Use the simple style for a one-step task** — header with title/subtitle/button; custom completion image or default checkmark fill; no content stack (use another style if more content is needed).
- **Use the instructions style to add informative text to a simple task.**
- **Use the log style to help people log events,** with automatic timestamps.
- **Use the checklist style for a list of steps in a multistep task** — text + completion button per item; optional instructional text below the list.
- **Use the grid style for a compact multistep task** — succinct per-button titles; gives access to the underlying collection view for custom UI elements; optional instructional text below the grid.
- **Consider using color to reinforce task-item meaning,** never as the only signal.
- **Combine accuracy with simplicity** — e.g., marketing names not chemical names; minimize words when context clarifies meaning.
- **Consider supplementing multistep/complex tasks with videos or images.**

*Charts* — bar, scatter, line styles; each takes title, subtitle, axis markers, and data set; can show current + historical data and auto-update.
- **Consider highlighting narratives/trends** to illustrate progress and encourage adherence.
- **Label chart elements clearly and succinctly** — avoid long/repetitive labels.
- **Use distinct colors** — avoid different shades of the same color for different meanings; ensure sufficient contrast.
- **Consider providing a legend** if colors aren't immediately clear.
- **Clearly denote units of time** (seconds through years) in labels or elsewhere on the chart.
- **Consolidate large data sets for readability.**
- **If necessary, offset data to keep charts proportional** when data-point sizes vary greatly.

*Contact views* — simple and detailed styles. **Consider using color to categorize care team members** at a glance.

**Notifications** — can badge the app icon for unread caregiver messages.
- **Minimize notifications** — use sparingly, coalesce multiple items into one.
- **Consider providing a detail view** for immediate action without leaving the current context (e.g., mark tasks complete).

**Symbols and branding** — built-in symbols (phone, messaging, envelope, clock); the highly customizable grid-style task view can use SF Symbols.
- **Design a relevant care symbol** — closely related to your app or general health/wellness; avoid purely decorative symbols or corporate logos.
- **Incorporate refined, unobtrusive branding** via color/communication style — no advertising.

**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## CarPlay
Source: https://developer.apple.com/design/human-interface-guidelines/carplay
CarPlay lets people get directions, make calls, send and receive messages, listen to music, and more from their car's built-in display, all while staying focused on the road.
Apps download like any other from the App Store and appear on the CarPlay Home screen when the iPhone connects. Built using system-defined templates (audio, communication, navigation, fueling); the system handles layout/resolution/hardware input so you don't adjust per screen or input type (CarPlay App Programming Guide).

**iPhone interactions**
- **Eliminate app interactions on iPhone when CarPlay is active** — interactions occur via the car's controls/display; perform any iPhone-side setup before the vehicle is in motion.
- **Never lock people out of CarPlay because the connected iPhone requires input.** The app must function when iPhone is inaccessible (bag/trunk); defer iPhone-side problem resolution until the vehicle stops.
- **Make sure your app works without requiring people to unlock iPhone** (most people use CarPlay with iPhone locked).

*Audio* — coexists with other sources (car radio, nav voice prompts).
- **Let people choose when to start playback.** Avoid auto-play unless the app plays a single audio source or resumes previously interrupted audio; don't start an audio session (silences other sources) until ready to actually play.
- **Start playback as soon as audio has sufficiently loaded.** System shows a spinning activity indicator and keeps the selection highlighted meanwhile.
- **Display the Now Playing screen when audio is ready** — don't delay for descriptive info to finish loading; load it in background and show when available.
- **Resume audio after an interruption only when appropriate** — resumable (e.g., phone call) vs. nonresumable (e.g., Siri-initiated playlist) interruptions; resume only if audio was actively playing when interrupted.
- **When necessary, automatically adjust relative/independent audio levels, but don't change the overall output volume** (people control that).

**Layout** — system scales icons/interfaces so they appear roughly the same size regardless of display resolution/density/aspect ratio.

| Dimensions (pixels) | Aspect ratio |
|---|---|
| 800x480 | 5:3 |
| 960x540 | 16:9 |
| 1280x720 | 16:9 |
| 1920x720 | 8:3 |

- **Provide useful, high-value info in a clean, easy-to-scan layout** — no nonessential clutter/embellishments.
- **Maintain an overall consistent appearance** — similar functions look similar.
- **Ensure primary content stands out and feels actionable** — large items read as more important/easier to tap; place important content/controls in the upper half of the screen.

**Color**
- **Prefer a limited color palette that coordinates with your app logo.**
- **Avoid using the same color for interactive and noninteractive elements.**
- **Test your color scheme under varied real-car lighting conditions** (time of day, weather, window tint) — consider night brightness and sunlight washout; adjust as needed.
- **Ensure the app looks great in both dark and light appearances** (CarPlay may auto-switch based on lighting).
- **Choose colors that communicate effectively with everyone** (Inclusive color).

**Icons and images** — supports landscape/portrait, @2x and @3x.
- **Supply @2x and @3x high-resolution images for all CarPlay artwork** — the system selects/scales appropriately.
- **Mirror your iPhone app icon** — one design works for both.
- **Don't use black for your icon's background** — lighten it or add a border so it doesn't blend into the display background.

| @2x (pixels) | @3x (pixels) |
|---|---|
| 120x120 | 180x180 |

**Error handling**
- **Report errors in CarPlay, not on the connected iPhone** — never direct people to pick up iPhone to read/resolve an error.

**Platforms:** No additional considerations for iOS. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS.

## Game Center
Source: https://developer.apple.com/design/human-interface-guidelines/game-center
Game Center is Apple's social gaming network, which lets players track their progress and connect with friends across Apple platforms, and boosts the discovery of your game across players' devices.
Supporting it lets players discover friends' games, invite friends seamlessly, and see latest activity system-wide (Games app, App Store, notifications). Use the GameKit framework's full-featured UI, or build custom UI on GameKit data.

**Accessing Game Center**
- **Determine sign-in status at launch and initialize the player with Game Center if not signed in** — most seamless UX, maximizes discovery (Top Played chart, social recommendations).

*Integrating the access point* — an Apple-designed UI element for viewing Game Center profile/info without leaving the game; leads to the Game Overlay (iOS/iPadOS/macOS) or in-game dashboard (visionOS/tvOS).
- **Display the access point in menu screens** (main menu/settings) — avoid during active gameplay, splash screens, cinematics, or tutorials.
- **Avoid placing controls near the access point** — it can appear at any of the four corners in collapsed/expanded versions; check for overlap and adjust layout.
> Note: In visionOS, access point location varies by game type (immersive/volume-based).
- **Consider pausing the game while the Game Overlay/dashboard is present.**

*Using custom UI* — can deep-link into Game Overlay/dashboard areas (e.g., leaderboards, profile).
- **Use the official Game Center artwork** (Apple Design Resources) unaltered in custom links.
- **Use correct terminology in custom UI:**

| Term | Incorrect terms |
|---|---|
| Game Center | GameKit, GameCenter, game center |
| Game Center Profile | Profile, Account, Player Info |
| Achievements | Awards, Trophies, Medals |
| Leaderboards | Rankings, Scores, Leaders |
| Challenges | Competitions |
| Add Friends | Add, Add Profiles, Include Friends |

**Achievements** — four states: locked, in-progress, hidden, completed; displayed as collectible cards grouped Completed/Locked.
- **Align with the four Game Center achievement states** for a consistent experience.
- **Determine a display order** — upload order = display order (e.g., matching the game's common progression path).
- **Be succinct** — title and description each limited to two lines (truncates beyond); title-style capitalization for the title, sentence-style for the description.
- **Give players a sense of progress** — progressive achievements show progress plus encouraging system messages.
- **Design rich, high-quality, unique images** — no reuse across achievements (placeholder shown if none provided); system applies a circular mask, so keep content centered.

**Leaderboards** — two types:
- *Classic leaderboard:* tracks all-time best score, always active, no ending (e.g., most perfect score, most coins in a run, longest endless-runner time).
- *Recurring leaderboard:* resets on a defined interval (daily/weekly) — good for daily puzzles, seasonal events, weekly battle-mode boards.
- **Take advantage of leaderboard sets** to organize multiple leaderboards — group by difficulty, activity type, or genre/theme.
- **Add unique leaderboard images** reflecting each leaderboard's gameplay — single image for iOS/iPadOS/macOS; animating image set for tvOS focus effect (tvOS template in Apple Design Resources).
> Note: system crops leaderboard-set artwork on iOS/iPadOS/macOS; the tvOS focus effect may crop image edges — keep primary content comfortably visible in both cases.

**Challenges** — built on leaderboards, add time-limited multiplayer competitions.
- **Create engaging challenges** — short (1–5 min), individually completable, clear accomplishment metric (e.g., fastest lap, most enemies defeated, fewest mistakes).
- **Avoid challenges that track overall progress or personal-best scores** (unfair to new players) — track the most recent score per attempt instead.
- **Make it easy to jump into your challenge** — accessible via invitation links, Game Overlay, Games app; deep-link to the exact mode/level; onboard first-time players (e.g., tutorial) before dropping them in.
- **Create high-quality challenge artwork** — shown in Game Overlay, Games app, invitation-link previews; keep primary content clear of the title/description overlay area; provide localized text via App Store Connect/Xcode.

| Attribute | Value |
|---|---|
| Format | JPEG, JPG, or PNG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 1920x1080 pt (3840x2160 px @2x) |
| Cropped area | 1465x767 pt (2930x1534 px @2x) |

**Multiplayer activities** — real-time and turn-based; accessed via party codes, Game Overlay, dashboard, Games app.
- **Use party codes to invite players** — typically 8-char alphanumeric (e.g., "2MP4-9CMF"); allow joining late, leaving early, returning later; show the current code in-game; allow manual entry.
- **Support multiplayer activities through in-game UI** — default interface lets players invite nearby/recent players, friends, contacts; or build custom UI.
- **Provide engaging activity preview artwork** (shown in party code, Games app, in-game UI) — same specs as Challenges artwork above.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, or visionOS.
**tvOS:** Can display an optional image atop the dashboard — simple, recognizable at a distance (logo/word mark, not app icon).

| Attribute | Value |
|---|---|
| Image size | 600x180 pt (1200x360 px @2x) |
| Format | PNG, TIF, or JPG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |

**watchOS:** GameKit features/API are available, but there's no system-supported Game Center UI on watchOS — Game Center content for watchOS games appears on a connected iPhone.

## Generative AI
Source: https://developer.apple.com/design/human-interface-guidelines/generative-ai
Generative AI empowers you to enhance your app or game with dynamic content and offer intelligent features that unlock new levels of creativity, connection, and productivity.

**Best practices**
- **Design your experience responsibly.** Small/identical input changes can yield very different generative outcomes; orient design around inclusive, careful, privacy-protecting AI experiences.
- **Keep people in control.** Respect agency in decision-making; honor in-scope requests, handle sensitive content carefully; let people dismiss unwanted content and revert/retry transformations; clearly identify when/where AI is used.
- **Ensure an inclusive experience for all.** Models can amplify biases/stereotypes from training data — ask people to provide needed info rather than inferring personal/cultural characteristics; seek clarity before assuming gender/relationship-type stereotypes; test across a diverse set of people (Inclusion, Accessibility).
- **Design engaging and useful generative features.** Offer them only where they provide clear, specific value (time savings, better communication, enhanced creativity).
- **Ensure a great experience even when generative features aren't available or people opt not to use them.** Offer a non-AI fallback when possible (e.g., Genmoji vs. regular emoji; AI summarization vs. reading notifications directly).

**Transparency**
- **Communicate where your app uses AI.** Set expectations; never trick someone into thinking AI content/interaction is human-authored; align disclosure with regional regulations.
- **Set clear expectations about what your AI-powered feature can and can't do.** Brief tutorials; curated suggestions for open-ended features (search bar/generation prompt); disclose known limitations up front and explain inferior results (Limitations).

**Privacy**
- **Choose a model type that fits your feature's needs and protects people's privacy.** On-device models keep data local/respond fast/work offline; server-based models for more processing power/context. For server processing, minimize what's shared and be transparent that data may be sent/stored/used for training.
- **Ask permission before using personal information and usage data.** Use the minimum needed, offer a clear opt-out; get explicit permission for storage/model-improvement use; understand third parties' privacy approach if data is shared; be aware outputs can inadvertently leak sensitive info; apps for kids have stricter rules (Requesting permission).
- **Clearly disclose how your app and its model use and store personal information.** Concise, specific explanation of benefits; state whether personal info is used for training/improvement.

**Models and datasets**
- **Thoughtfully evaluate model capabilities** early — general-knowledge vs. task-specific; some model types are unavailable depending on device compatibility/network/battery (e.g., Foundation Models framework requires an Apple Intelligence-compatible device).
- **Be intentional when choosing or creating a dataset.** Diverse subject-matter representation; know data provenance/licensing; offer choices for use of people's data; allow time for testing/evaluation to mitigate bias/misinformation.

**Inputs**
- **Guide people on how to use your generative feature** — offer diverse predefined example inputs.
- **Raise awareness about and minimize the chance of hallucinations.** Clearly communicate AI content may contain errors; avoid requesting factual info unless the model has verified, up-to-date access; avoid AI content where a hallucination could misinform/harm.
- **Consider consequences and get permission before performing irreversible or potentially problematic tasks.** Avoid automating destructive actions (e.g., deleting photos) or hard-to-undo ones (e.g., purchases); ask for confirmation before significant actions on someone's behalf; review model-specific usage policies and applicable government/regulatory AI policy per locale.

**Outputs**
- **Make it easy for people to refine or revert generated results, and acknowledge when their corrections take effect.** Controls like Edit/Undo/Retry/Adjust preserve agency; give clear feedback when an adjustment lands.
- **Help people improve requests when blocked or undesirable results occur** — coach for better next attempts (e.g., Image Playground's "Unable to use that description"); offer example requests.
- **Reduce unexpected and harmful outcomes with thoughtful design and thorough testing.** Proactively identify risks, devise mitigation policies, test poorly phrased/vague/ambiguous/personal/sensitive/controversial/adversarial inputs.
- **Strive to avoid replicating copyrighted content.** Build on models that already protect against this; curate inputs (e.g., pre-approved prompts); explicitly instruct the model to avoid mimicking certain content/styles.
- **Factor processing time into your design.** *Latency* is typically higher for generative than non-generative models (e.g., ARKit body tracking, Vision) — design a loading experience or generate in background (Loading).
- **Consider giving specific, reassuring feedback during generation** — describe what's actually happening (e.g., "Finding substitutions for ingredients") rather than vague "Processing…"; describe errors in plain language with a clear next step.
- **Consider offering alternate versions of results** — single vs. multiple meaningfully different options increases sense of control (e.g., Image Playground generating multiple person-representing images) (Multiple options).

**Continuous improvement**
- **Consider ways to improve your model over time.** Frequent independent updates (e.g., blocked-word lists) vs. significant updates tied to app releases; plan fine-tuning/retesting/prompt engineering for base-model upgrades; retrain/fine-tune custom models with new data; thoroughly test all updates.
- **Let people share feedback on outputs.** Simple thumbs-up/down plus optional detailed feedback; place the feedback affordance clearly without interrupting the experience; take feedback seriously, resolve issues quickly, always make it voluntary (Explicit feedback, Implicit feedback).
- **Design flexible, adaptable features** — e.g., decouple the model from the UX so models can be swapped as capabilities improve while the UX stays the same.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## HealthKit
Source: https://developer.apple.com/design/human-interface-guidelines/healthkit
HealthKit is the central repository for health and fitness data in iOS, iPadOS, and watchOS.
> Important: If your app doesn't provide health and fitness functionality, don't request access to people's private health data.

**Privacy protection**
- **Provide a coherent privacy policy** — required URL during app submission, viewable from the App Store page.
- **Request access to health data only when you need it,** tied to context (e.g., at weigh-in, not at launch); re-request every time access is needed since permissions can change (`requestAuthorization(toShare:read:completion:)`).
- **Clarify your app's intent by adding descriptive messages to the standard permission screen** — succinct explanation of why/benefit; avoid custom screens replicating it.
- **Manage health data sharing solely through the system's privacy settings** (Settings > Privacy) — don't build additional app screens affecting the flow.

**Activity rings** — show progress toward Move/Exercise/Stand goals; the Activity app defines each ring's position/color.
- **Use Activity rings for Move, Exercise, and Stand information only** — never replicate/modify for other data, never show progress in another ring-like element.
- **Use Activity rings to show progress for a single person only** — make whose progress is shown obvious (label/photo/avatar).
- **Don't use Activity rings for ornamentation** — never in labels or background graphics.
- **Don't use Activity rings for branding** — never in an app icon or marketing materials.
- **Maintain Activity ring and background colors** — visual appearance must always be the same; never apply filters, recolor, or change opacity; design the surrounding interface to blend (e.g., enclose in a circle); scale rings appropriately.
- **Maintain Activity ring margins** — minimum outer margin no less than the distance between rings; nothing may crop/obstruct/encroach; adjust the enclosing view's corner radius rather than applying a circular mask.
- **Differentiate other ring-like elements from Activity rings** — use padding/lines/labels/color/scale for separation.
- **Provide app-specific information only in Activity notifications** — don't repeat Move/Exercise/Stand updates or show an Activity ring element in notifications (`HKActivityRingView`).

**Apple Health icon** — shows an app works with HealthKit/Health app.
- **Use only the Apple-provided icon** (Apple Design Resources) — don't create your own or mimic it.
- **Display the name "Apple Health" close to the icon.**
- **Display the Apple Health icon consistently with other health-related app icons** — no smaller than other icons in the same view.
- **Don't use the Apple Health icon as a button** — indicates compatibility only.
- **Don't alter its appearance** — no corner-radius masking, circular shape, borders, color overlays, gradients, shadows, or other effects.
- **Maintain a minimum clear space of 1/10 of its height;** don't composite it onto another graphic.
- **Don't use the icon within text or as a replacement for "Health," "Apple Health," or "HealthKit."**
- **Don't display Health app images/screenshots** (copyrighted) — use an Activity ring element instead if showing Move/Exercise/Stand progress.

**Editorial guidelines**
- **Refer to the Health app as "Apple Health" or "the Apple Health app."**
- **Don't use the term "HealthKit"** with people — it's developer-facing; say the app "works with the Apple Health app" or "uses data from the Apple Health app."
- **Use correct capitalization:** "Apple Health" — two words, uppercase A and H, rest lowercase; all-uppercase allowed only for an all-caps interface style.
- **Use the system-provided translation of "Health"** to avoid confusion.

**Platforms:** No additional considerations for iOS, iPadOS, or watchOS. Not supported in macOS, tvOS, or visionOS.

## HomeKit
Source: https://developer.apple.com/design/human-interface-guidelines/homekit
HomeKit lets people securely control connected accessories in their homes using Siri or the Home app on iPhone, iPad, Apple Watch, and Mac.
An app can integrate with HomeKit to help set up/name/organize accessories, allow fine-grained configuration/control, provide custom feature access, show automations, and provide support. (MFi licensees: see the MFi portal for accessory-packaging naming/messaging.)

**Terminology and layout** — HomeKit models the home as a hierarchy (home → rooms/zones/accessories); using its terminology/object model is crucial for consistency.
- **Acknowledge the hierarchical model** even if your app's UI doesn't organize by rooms/zones — needed for people to use Siri/HomePod voice commands (Siri interactions).
- **Make it easy to find an accessory's related HomeKit details** (zone/room) — don't hide in a settings screen; consider an accessory detail view.
- **Recognize that people can have more than one home** — provide relevant home info in an accessory detail view even if your app doesn't support multiple homes.
- **Don't present duplicate home settings** — always defer to Home app settings; surface them intuitively in your UI rather than re-asking people to set up their home.

*Object model terms:*
- **Home:** a physical home, office, or other relevant location; a person can have multiple.
- **Room:** a physical room, named for meaning (e.g., "Bedroom") not attributes like size/location; enables commands like "turn on the kitchen and hallway lights."
- **Accessory / category:** a physical connected device (e.g., ceiling fan, lamp, lock, camera); category = type (thermostat, fan, light), assigned by manufacturer or your app.
- **Service:** a controllable feature of an accessory (e.g., a light switch); named descriptively in UI (not "service"); Siri commands use service names, not accessory names.
- **Characteristic:** a controllable attribute of a service (e.g., speed, brightness); named descriptively in UI (not "characteristic").
- **Service group:** accessories' services grouped for unified control (e.g., "reading lamps").
- **Action:** change of a service's characteristic, initiated by people or automation.
- **Scene:** a group of actions across one or more accessories/services (e.g., "Movie Time," "Good Morning").
> Tip: The HomeKit API uses "action set" — in your app's UI, always use "scene."
- **Automation:** accessories reacting to situations (location change, time of day, another accessory's state, sensor detection).
- **Zone:** an area containing multiple rooms (e.g., "upstairs"); optional, but enables multi-accessory voice control.

**Setup**
- **Use the system-provided setup flow** — faster (naming, network join, pairing, categories, favorites in a few steps); lets you focus on unique accessory functionality (`performAccessorySetup(using:completionHandler:)`).
- **Provide context for why you need access to people's Home data** — a clear purpose string (e.g., "Lets you control this accessory with the Apple Home app and Siri across your Apple devices").
- **Don't require account creation or personal info** — defer to HomeKit; make any cloud-service account setup optional, offered after initial HomeKit setup.
- **Honor people's setup choices** — don't force cross-platform setup during the HomeKit flow.
- **Carefully consider a custom accessory setup experience** — always start with the system-provided flow; offer a custom post-setup experience afterward highlighting unique features.

*Help people choose useful names*
- **Suggest service names that suit your accessory** — recommend alternatives for suboptimal Siri names; never suggest company names/model numbers.
- **Check that names follow HomeKit naming rules** if people can rename services (alphanumeric/space/apostrophe characters only, start/end alphanumeric, no emojis) — explain problems and suggest working alternatives.
- **Help people avoid names that include location info** (e.g., "kitchen light") since it causes unpredictable voice-control results — detect and help fix such names, encouraging room/zone assignment instead.

**Siri interactions**
- **Present example voice commands during setup**, using the chosen service name.
- **After setup, consider teaching more complex Siri commands** elsewhere in the app (e.g., "You can say 'Hey Siri, set Movie Time.'").
- Siri also recognizes accessory category and characteristic even without an explicit service name (e.g., "brighter," "dim") — a wide range of natural phrases resolve to home/room/zone/service/scene/category/characteristic combinations.
- **Recommend creating zones/service groups when relevant,** and help set them up (e.g., "upstairs" zone or "media center" group).
- **Offer shortcuts only for accessory-specific functionality HomeKit doesn't already support** — don't duplicate native HomeKit voice control.
- **If supporting both HomeKit and Shortcuts, clearly distinguish them** — never encourage a shortcut duplicating HomeKit-native scene/action control.

**Custom functionality**
- **Be clear about what's possible in your app vs. the Home app** — e.g., guide people to build a partial scene in your app, then suggest completing it (adding other accessories) in the Home app (Referring to HomeKit).
- **Defer to HomeKit if your database differs from HomeKit's** — reflect changes made in the Home app/other HomeKit apps automatically; if conflicts must be surfaced, present them visually side by side for confirmation.
- **Ask permission before writing to the HomeKit database on people's behalf** — never overwrite settings without explicit direction.

*Cameras*
- **Don't block camera images** — supplement with useful overlays (e.g., activity alerts) but avoid covering portions of the feed.
- **Show a microphone button only if the camera supports bidirectional audio** — a nonfunctioning button wastes space and confuses people.

**Using HomeKit icons** — use in setup/instructional communications; can also use the Apple Home app icon when referencing the app or linking to its App Store page.
- **Use only Apple-provided icons** (Resources) — don't create your own or mimic them.
- Black icon: on white/light backgrounds when other tech icons are black. White icon: on black/dark backgrounds when other tech icons are white. Custom color icon: when other tech icons share that custom color.
- **Position the icon consistently with other technology icons.**
- **Use the icon noninteractively** — no custom buttons (except the Apple Home app icon, which may open its App Store page).
- **Don't use the icon within text or as a word replacement.**
- **Pair the icon with the name "HomeKit" correctly** — same font as the rest of your layout.

**Referring to HomeKit**
- **Emphasize your app over HomeKit/Apple Home** — keep references less prominent than your app identity.
- **Adhere to Apple's trademark guidelines** — no Apple trademarks in your app name/images; use Apple product names exactly per the Trademark List, singular/non-possessive only; don't translate Apple/Apple Home/HomeKit; don't use category descriptors (say iPad, not tablet); don't imply Apple sponsorship/partnership/endorsement; attribute correct credit lines; reference Apple devices/OSes only in technical-spec/compatibility contexts.
- **Use correct capitalization** — "HomeKit" one word, uppercase H and K; "Apple Home" two words, uppercase A and H; all-uppercase allowed only for an all-caps layout style.
- **Don't use "HomeKit" as a descriptor** — use "works with," "use," "supports," or "compatible" instead.
- **Don't suggest HomeKit itself is performing an action/function.**
- May pair with the name "Apple" (e.g., "Apple HomeKit"); may use "HomeKit" for setup/configuration/instructions.
- **Use the app name "Apple Home" on first mention** in body copy; subsequent mentions can say "the Home app."

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## iCloud
Source: https://developer.apple.com/design/human-interface-guidelines/icloud
iCloud is a service that lets people seamlessly access the content they care about — photos, videos, documents, and more — from any device, without performing explicit synchronization.
- **Make it easy to use your app with iCloud.** People expect apps to work with it automatically once turned on in Settings; if offering a choice, show a simple option the first time the app opens (iCloud for all data, or not at all).
- **Avoid asking which documents to keep in iCloud.** Most people expect all content available and don't want to manage individual document storage; automate file management where possible.
- **Keep content up to date when possible,** balanced against storage/bandwidth constraints — for very large documents, let people control download timing, indicate when a newer version is available, and show subtle feedback if a download takes more than a few seconds.
- **Respect iCloud storage space.** A finite, paid resource — use it for content people create/understand, not regenerable app resources; be picky about the Documents folder since iCloud backups include its entire contents even without explicit iCloud support.
- **Make sure your app behaves appropriately when iCloud is unavailable** (manually off, Airplane Mode) — no alert needed, but an unobtrusive note that changes won't sync until iCloud is restored can help.
- **Keep app state information in iCloud** when it should apply across all of a person's devices (e.g., last page read) — not all settings qualify (some are more useful at work than home).
- **Warn about the consequences of deleting a document.** Deletion removes it from iCloud and all devices — show a warning and require confirmation.
- **Make conflict resolution prompt and easy.** Detect/resolve automatically when possible; otherwise show an unobtrusive notification distinguishing the conflicting versions, ideally as early as possible.
- **Include iCloud content in search results** — people expect their content to be universally searchable.
- **For games, consider saving player progress in iCloud.** The GameSave framework syncs save data across devices and offers built-in alerts for offline/conflict handling, or you can build custom UI on GameSave data.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## ID Verifier
Source: https://developer.apple.com/design/human-interface-guidelines/id-verifier
ID Verifier lets your iPhone app read mobile IDs in person without requiring external hardware.
Since iOS 17, apps can read ISO18013-5 compliant mobile IDs for in-person verification (e.g., age verification at a venue). Customers present only the minimum data needed without handing over their ID or device; Apple manages certificate issuance/management/validation.

Two request types:
- **Display Only request** — shows data (e.g., name/age with photo portrait) in system-provided UI on the requester's iPhone for visual confirmation only; customer data stays in system UI and isn't transmitted to your app (`MobileDriversLicenseDisplayRequest`).
- **Data Transfer request** — use only with a legal verification requirement needing stored/processed data (e.g., address, date of birth); requires an additional entitlement (`MobileDriversLicenseDataRequest`, `MobileDriversLicenseRawDataRequest`; see Get started with ID Verifier).

**Best practices**
- **Ask only for the data you need** — e.g., use an age-threshold request (`ageAtLeast(_:)`) rather than requesting current age/birth date.
- **If your app qualifies, register for ID Verifier with Apple Business Register** so people see your organization's official name/logo in the ID-verification UI.
- **Provide a button that initiates the verification process** — label like "Verify Age" (simple age check) or "Verify Identity" (detailed data request); avoid symbols specifying a communication type (NFC/QR); never include the Apple logo in a button label.
- **In a Display Only request, help the person using your app provide feedback on the visual confirmation they perform** — e.g., "Matches Person" / "Doesn't Match Person" buttons feeding an approved/rejected response value.

**Platforms:** No additional considerations for iOS. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS.

## iMessage apps and stickers
Source: https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers
An iMessage app can help people share content, collaborate, and even play games with others in a conversation; stickers are images that people can use to decorate a conversation.
Available within a Messages conversation and in Messages/FaceTime effects; build as a standalone app or an app extension within an iOS/iPadOS app.

- **Prefer providing one primary experience in your iMessage app.** People are in conversational flow, so functionality/content must be immediately understandable; create a separate app for each distinct functionality/content collection.
- **Consider surfacing content from your iOS/iPadOS app** (e.g., a shopping list, trip itinerary) or supporting a simple collaborative task (e.g., deciding where to eat).
- **Present essential features in the compact view.** Reserve additional content/features for the expanded view.
- **In general, let people edit text only in the expanded view.** The compact view occupies roughly the keyboard's space, so display the keyboard in expanded view to keep content visible.
- **Create stickers that are expressive, inclusive, and versatile.** Legible against varied backgrounds and when rotated/scaled; use transparency to help integration with text/photos/other stickers.
- **For each sticker, provide a localized alternative description** — VoiceOver speaks it.

**Specifications** — icon sizes (square-cornered; system applies a rounded mask):

| Usage | @2x (pixels) | @3x (pixels) |
|---|---|---|
| Messages, notifications | 148x110 / 143x100 / 120x90 / 64x48 / 54x40 | — / — / 180x135 / 96x72 / 81x60 |
| Settings | 58x58 | 87x87 |
| App Store | 1024x1024 | 1024x1024 |

Sticker sizes — small, regular, large: pick one size for the whole pack (don't mix); create at @3x, system downscales for @2x/@1x (`MSStickerSize`).

| Sticker size | @3x dimensions (pixels) |
|---|---|
| Small | 300x300 |
| Regular | 408x408 |
| Large | 618x618 |

Sticker file size limit: 500 KB or smaller.

| Format | Transparency | Animation |
|---|---|---|
| PNG | 8-bit | No |
| APNG | 8-bit | Yes |
| GIF | Single-color | Yes |
| JPEG | No | No |

**Platforms:** No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.

## In-app purchase
Source: https://developer.apple.com/design/human-interface-guidelines/in-app-purchase
People can use in-app purchase to pay for virtual goods — like premium content, digital goods, and subscriptions — securely within your app.
> Tip: In-app purchase and Apple Pay serve different use cases. Use in-app purchase for virtual goods/subscriptions to digital content; use Apple Pay for physical goods, services (memberships, reservations, tickets), and donations.

Four content types: **Consumable** (depletes with use, repurchasable — e.g., game lives/gems), **Non-consumable** (doesn't expire — e.g., premium features), **Auto-renewable subscriptions** (renew automatically each period until canceled), **Non-renewing subscriptions** (limited-time access, repurchased each time to extend — e.g., an in-game battle pass).
> Note: Apps with exceptionally large/frequently updated catalogs, multi-creator content, or subscriptions with optional add-ons as a single purchase can use the Advanced Commerce API to manage the In-App Purchase catalog directly.

**Best practices**
- **Let people experience your app before making a purchase** — consider limited free access for auto-renewable subscriptions.
- **Design an integrated shopping experience** — mirror your app's style so browsing/purchasing doesn't feel like a different app.
- **Use simple, succinct product names and descriptions** — non-truncating/wrapping titles, plain direct language.
- **Display the total billing price for each in-app purchase,** regardless of type.
- **Display your store only when people can make payments** — hide it or explain unavailability (e.g., parental restrictions) (`canMakePayments`).
- **Use the default confirmation sheet** — don't modify or replicate it.

*Supporting Family Sharing* (shares purchased content, e.g. auto-renewable subscriptions and non-consumables, with up to five additional family members):
- **Prominently mention Family Sharing** where people learn about your content (e.g., "Family"/"Shareable" in a name, referencing it on sign-up screens).
- **Help people understand the benefits/how to participate** — system-sent notifications inform existing subscribers and family members of sharing changes.
- **Customize in-app messaging** for both purchasers and family members (e.g., "Your family subscription includes…").

*Providing help with in-app purchases* — custom UI can offer assistance/alternatives and initiate the system refund flow (`beginRefundRequest(for:in:)`).
- **Provide help viewable before requesting a refund** — tailored assistance, FAQs, feedback/contact options, alongside a link to the system refund flow.
- **Use a simple refund-action title** like "Refund" or "Request a Refund" — no need to reiterate that refunds come from Apple.
- **Help people find the problematic purchase** — show product image/name/description and original purchase date for each recent purchase.
- **Consider offering alternative solutions** (e.g., immediate fulfillment, conciliatory item) while still making refund requests clear.
- **Make it easy to request a refund** — don't bury the refund button behind scrolling/extra screens.
- **Avoid characterizing or providing guidance on Apple's refund policies** — link to Request a refund instead of speculating.

**Auto-renewable subscriptions**
- **Call attention to subscription benefits during onboarding** — strong call to action plus a clear terms summary (Making signup effortless; Onboarding).
- **Offer a range of content choices, service levels, and durations.**
- **Consider letting people try your content for free before signing up** — freemium app, metered paywall, or free trial.
- **Prompt people to subscribe at relevant times** (e.g., nearing a monthly free-content limit); include prompts at relevant points throughout the app.
- **Encourage a new subscription only when someone isn't already a subscriber** — provide sign-in if the same subscription is offered across multiple apps/website, so people don't pay twice.

*Making signup effortless*
- **Provide clear, distinguishable subscription options** — short self-explanatory names, price, and duration per option; list introductory price/duration and standard post-offer price if applicable.
- **Simplify initial signup by asking only for necessary information** — defer additional info until after signup.
- **In your tvOS app, help people sign up or authenticate using another device** — send a code rather than requiring in-app text input.
- **Give people more information on the sign-up screen** — links to Terms of Service/Privacy Policy; subscription name/duration/content-or-services per period; correctly localized billing amount; a way for existing subscribers to sign in or restore purchases.
- **Clearly describe how a free trial works** — duration and post-trial billed amount, since payment is automatically initiated when the trial ends.
- **Include a sign-up opportunity in your app's settings.**

*Supporting offer codes* (iOS/iPadOS) — free or discounted access via online/offline channels.
- **One-time use code** — unique, App Store Connect-generated; redeemable via redemption URL, in-app, or entered in the App Store (installs the app if needed); good for small/restricted distribution.
- **Custom code** — self-created (e.g., NEWYEAR, SPRINGSALE); redeemable via redemption URL or in-app (not via App Store account settings); good for large mass-distributed campaigns.
- **Clearly explain offer details** in marketing materials — straightforward, succinct.
- **Follow custom-code creation rules** — alphanumeric ASCII characters only, no special/Chinese/Arabic characters.
- **Tell people how to redeem a custom code** — via redemption URL or in-app (not App Store account settings).
- **Consider supporting offer redemption within your app** — the system provides the redemption-flow screens; your only custom UI need is a button that initiates the flow (`presentOfferCodeRedeemSheet(in:)`, `offerCodeRedemption(isPresented:onCompletion:)`); natural placements include the paywall, onboarding, or settings.
- **Supply an engaging, informative promotional image** for the code-redemption screens — falls back to your app icon if omitted.
- **Help people benefit from unlocked content as soon as they complete redemption** — align the post-redemption experience with new subscriber status (e.g., welcome flow, feature tour); smooth the process for people who subscribe before first opening the app.

*Helping people manage their subscriptions*
- **Provide summaries of the customer's subscriptions,** including the upcoming renewal date, near the subscription-management option (`Product.SubscriptionInfo`).
- **Consider using the system-provided subscription-management UI** for a consistent experience (`showManageSubscriptions(in:)`).
- **Consider ways to encourage a subscriber to keep their subscription or resubscribe later** — personalized retention offers, exit surveys when someone cancels (the app is notified via StoreKit).
- **Always make it easy for customers to cancel an auto-renewable subscription** — a hard-to-find management action feels like being discouraged from canceling.
- **Consider a branded, contextual experience alongside the system management UI** — e.g., promote a premium tier, personalized alternative-plan suggestions, discounted promotional offers, or offer codes for win-back/upgrade.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS.
**watchOS:** Sign-up screen must display the same required subscription info as other app versions (see Making signup effortless).
- **Clearly describe differences between watchOS and other-device app versions** — be straightforward about limitations without implying an identical experience.
- **Consider using a modal sheet to display required info** in a single view — the default Close button eases return to free content; if using a custom view instead, include a complete flow with a Close/Cancel button.
- **Make subscription options easy to compare on a small screen** — e.g., one button per payment option (locked up with its description), or a list of options followed by a single signup-start button whose title updates to reflect the chosen option.
