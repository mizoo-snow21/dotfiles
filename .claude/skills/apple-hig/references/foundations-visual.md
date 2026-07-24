# HIG — Foundations: visual (icons, color, materials, motion, typography)
Covered: app-icons, branding, color, dark-mode, icons, images, materials, motion, sf-symbols, typography

## App icons
Source: https://developer.apple.com/design/human-interface-guidelines/app-icons
A unique, memorable icon expresses your app's or game's purpose and personality and helps people recognize it at a glance.
- **Layer design.** Layers (vs. a flattened image) give the most control and produce depth/vitality; the system applies visual effects that respond to environment and interaction.
  - iOS, iPadOS, macOS, watchOS: background layer + one or more foreground layers; take on Liquid Glass attributes (specular highlights, refraction, translucency) that adapt with icon size, apply consistently across platforms, and can look different between system versions.
  - tvOS: 2-5 layers create dynamism as the icon comes into focus — it elevates to the foreground, sways with remote finger movement, and its surface illuminates; layer separation + transparency produce depth during the parallax effect.
  - visionOS: background layer + one or two layers on top produce a 3D object that subtly expands when viewed; the system adds shadows for depth and uses the alpha channel of upper layers for an embossed appearance.
  - Use Icon Composer (in Xcode / Apple Developer site) for iOS/iPadOS/macOS/watchOS icons: define the background, adjust foreground placement, apply effects, annotate default/dark/mono variants, preview across system versions, export for Xcode. For tvOS/visionOS, add layers directly to an image stack in Xcode.
  - **Prefer clearly defined edges in foreground layers** — avoid soft/feathered edges so system-drawn highlights and shadows look best.
  - **Vary opacity in foreground layers** to increase depth/liveliness (e.g. Photos icon separates its centerpiece into translucent layers); import fully opaque layers and adjust transparency in Icon Composer.
  - **Design a background that stands out and emphasizes foreground content** — gradients should respond well to system lighting; Icon Composer supports solid colors/gradients so custom background images are usually unnecessary; if you do import one, it must be full-bleed and opaque.
  - **Prefer vector graphics (SVG/PDF)** when bringing layers into Icon Composer — outline artwork and convert text to outlines; prefer PNG (lossless) for mesh gradients and raster artwork.
- **Icon shape** varies by platform: iOS/iPadOS/macOS icons are square with system-applied rounded-corner masking matching device bezel curvature; tvOS icons are rectangular with concentric edges; visionOS/watchOS icons are square with circular masking.
  - **Produce appropriately shaped, unmasked layers** — square layers for iOS/iPadOS/macOS (system rounds corners) and for visionOS/watchOS (system creates circular shape); rectangular layers for tvOS. Pre-masked layers degrade specular highlights and look jagged.
  - **Keep primary content centered** to avoid truncation from corner/mask adjustments, especially in visionOS/watchOS; use the grids in the app icon production templates (Apple Design Resources).
- **Design.** Embrace simplicity — simple icons are easiest to recognize; fine details look busy under system shadows/highlights and are hard to discern at small sizes. Find one core concept, express it with a minimal number of shapes; a simple background (solid color/gradient) is fine — no need to fill the whole canvas.
  - **Provide a visually consistent icon design across all supported platforms** to help people find your app and avoid confusion with other apps.
  - **Consider basing the design around filled, overlapping shapes** — with transparency/blurring this gives a sense of depth.
  - **Include text only when essential** to your experience or brand — text hurts accessibility/localization, is often too small to read, and clutters; a mnemonic (e.g. first letter) is fine, but avoid nonessential words ("Watch," "Play") or context terms ("New," "For visionOS"); in tvOS, put text above other layers so parallax cropping doesn't cut it.
  - **Prefer illustrations to photos and avoid replicating UI components** — photos carry too much detail for different appearances/small sizes/layering; avoid extremely thin line weights and sharp corners (lose detail at small sizes); don't replicate standard UI components or use app screenshots.
  - **Don't use replicas of Apple hardware products** — they're copyrighted.
- **Visual effects.** **Let the system handle blurring and other visual effects** — don't add specular highlights, drop shadows, bevels, blurs, or glows yourself; custom effects are static where system ones are dynamic, and can conflict. If you do add custom effects, test carefully in Icon Composer, Device Hub, or on a physical device.
  - **Create layer groupings to apply effects to multiple layers at once** in Icon Composer or your design tool; groups get additional Liquid Glass customization (specular highlights, refraction, translucency).
- **Appearances.** iOS/iPadOS/macOS let people choose default, dark, clear, or tinted Home Screen icon appearance (e.g. to complement wallpaper); you can design variants for each, and the system auto-generates any you don't provide.
  - **Keep the icon's features consistent across appearances** — don't swap elements in/out per variant, which can make your app harder to find when people switch appearances.
  - **Design dark and tinted icons that feel at home beside system icons/widgets** — you can preserve your default palette, but dark icons are more subdued and clear/tinted even more so; the icon must stay visible, legible, and recognizable in every variant.
  - **Use your light app icon as the basis for your dark icon** — choose complementary colors, avoid excessively bright images; color backgrounds generally give the greatest contrast in dark icons.
  - **Consider offering alternate app icons** (iOS, iPadOS, tvOS, compatible visionOS apps) — e.g. a sports app offering team icons; keep each closely related to your content/experience and avoid ones people could mistake for another app.
  > Note: Alternate app icons in iOS and iPadOS require their own dark, clear, and tinted variants; all alternate and variant icons are subject to app review under the App Review Guidelines.
- **Specifications** — layout, size, style, and appearances vary by platform:

| Platform | Layout shape | Icon shape after system masking | Layout size | Style | Appearances |
|---|---|---|---|---|---|
| iOS, iPadOS, macOS | Square | Rounded rectangle (square) | 1024x1024 px | Layered | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | Rectangle (landscape) | Rounded rectangle (rectangular) | 800x480 px | Layered (Parallax) | N/A |
| visionOS | Square | Circular | 1024x1024 px | Layered (3D) | N/A |
| watchOS | Square | Circular | 1088x1088 px | Layered | N/A |

  - The system automatically scales your icon to smaller variants for locations like Settings and notifications.
  - Supported color spaces: sRGB (color), Gray Gamma 2.2 (grayscale), Display P3 (wide-gamut; iOS, iPadOS, macOS, tvOS, watchOS only).

**Platforms:** No additional considerations for iOS, iPadOS, or macOS beyond the above. tvOS — include a safe zone since the system may crop content around the edges as the focused icon scales/moves (varies by image size, layer depth, motion; foreground layers get cropped more than background). visionOS — avoid a shape on the background layer meant to look like a hole/concave area (system shadow/specular highlights can make it stand out instead of recede). watchOS — avoid using black for the icon's background (lighten it so the icon doesn't blend into the display background).

## Branding
Source: https://developer.apple.com/design/human-interface-guidelines/branding
Apps and games express their unique brand identity in ways that make them instantly recognizable while feeling at home on the platform and giving people a consistent experience.
- **Use your brand's unique voice and tone** in all written communication (e.g. encouragement/optimism via plain words, occasional exclamation marks/emoji, simple sentence structures).
- **Consider choosing an accent color** — on most platforms the system applies it to interface icons, buttons, and text; in macOS people can choose their own accent color that overrides the app's.
- **Consider using a custom font** — ensure it's legible at all sizes and supports accessibility features like bold text and larger type; it can work well to pair a custom font for headlines/subheadings with the system font for body/captions, since system fonts are optimized for small-size legibility.
- **Ensure branding always defers to content** — using screen space for a brand asset that does nothing else means less room for content people care about; keep branding refined and unobtrusive.
- **Help people feel comfortable by using standard patterns consistently** — place UI components in expected locations and use standard symbols for common actions, even in a highly stylized interface.
- **Resist displaying your logo throughout the app** unless essential for context — people rarely need reminding which app they're using; use the space for valuable information/controls instead.
- **Avoid using a launch screen as a branding opportunity** — it disappears too quickly to convey anything; consider a welcome/onboarding screen for branding content instead.
- **Follow Apple's trademark guidelines** — Apple trademarks must not appear in your app name or images (see the Apple Trademark List and Guidelines for Using Apple Trademarks).

**Platforms:** No additional platform considerations.

## Color
Source: https://developer.apple.com/design/human-interface-guidelines/color
Judicious use of color can enhance communication, evoke your brand, provide visual continuity, communicate status and feedback, and help people understand information.
- **Avoid using the same color to mean different things** — use color consistently, especially when it communicates status or interactivity.
- **Make sure all colors work well in light, dark, and increased-contrast contexts.** iOS, iPadOS, macOS, tvOS offer light and Dark Mode; system colors adjust subtly per appearance, and Increase Contrast makes differences more apparent. Prefer system colors (already define these variants); for custom colors, supply light and dark variants plus a significantly-higher-differentiation increased-contrast option for each. Provide light and dark variants even for a single-appearance app, to support Liquid Glass adaptivity.
- **Test your color scheme under a variety of lighting conditions** — bright surroundings make colors look darker/muted, dark environments make colors look brighter/saturated; in visionOS, colors are also affected by reflected light from physical surroundings; adjust for the majority of use cases.
- **Test your app on different devices** — True Tone (iPhone/iPad/Mac) auto-adjusts display white point; apps for reading/photos/video/gaming can specify a white point adaptivity style (`UIWhitePointAdaptivityStyle`); test tvOS on multiple TV brands/settings; test Mac color profiles (P3 vs. sRGB) via System Settings > Displays.
- **Consider how artwork and translucency affect nearby colors** — e.g. Maps switches light/dark color schemes between map and satellite mode; colors look different behind or applied to a translucent element like a toolbar.
- **If people can choose colors, prefer system-provided color controls** (e.g. `ColorPicker`) — consistent experience, plus a saved palette accessible from any app.
- **Inclusive color:**
  - **Avoid relying solely on color** to differentiate objects, indicate interactivity, or communicate essential information — provide alternatives (text labels, glyph shapes) for people with color blindness or other visual disabilities.
  - **Avoid colors that make content hard to perceive** — insufficient contrast blends icons/text with the background; some color combinations aren't distinguishable to color-blind people.
  - **Consider how colors are perceived across countries and cultures** — e.g. red signals danger in some cultures, positive connotations in others.
- **System colors:**
  - **Avoid hard-coding system color values** — documented values are for reference only and fluctuate release to release; use APIs like `Color` to apply system colors.
  - iOS, iPadOS, macOS, visionOS define *dynamic system colors* matching standard UI components, adapting automatically to light/dark; each is semantically defined by purpose, not appearance.
  - **Avoid redefining the semantic meanings of dynamic system colors** — e.g. don't use the separator color as a text color, or secondary label color as a background.
- **Liquid Glass color:** By default Liquid Glass has no inherent color and takes color from content behind it; you can apply color to some elements (e.g. a primary call-to-action / prominent button styling) for emphasis; symbols/text on Liquid Glass controls can also carry color. For smaller elements (toolbars, tab bars) the system adapts Liquid Glass light/dark per underlying content, with symbols/text defaulting to a monochromatic scheme (darker on light content, lighter on dark); Liquid Glass is more opaque in larger elements (sidebars) to preserve legibility over complex backgrounds.
  - **Apply color sparingly to the Liquid Glass material and to symbols/text on it** — reserve it for elements that truly benefit (status indicators, primary actions); to emphasize primary actions apply color to the background rather than symbols/text (e.g. the accent color on a Done button's background); avoid coloring the background of multiple controls at once.
  - **Avoid similar colors in control labels if your app has a colorful background** — prefer a monochromatic toolbar/tab bar, or an accent color with sufficient differentiation, when content/background is colorful; conversely, in mostly monochromatic apps your brand color can work well as the app accent color.
  - **Be aware of color placement in the content layer** — avoid overlapping similar colors between content and controls; ensure the default/resting state (e.g. top of scrollable content) keeps clear legibility.
- **Color management:** a *color space* (gamut, e.g. sRGB, Display P3) represents colors in a color model (RGB, CMYK); a *color profile* describes those colors mathematically so devices reproduce them correctly; images embed their profile.
  - **Apply color profiles to your images** — sRGB produces accurate colors on most displays.
  - **Use wide color (Display P3) to enhance visuals on compatible displays** — richer/more saturated than sRGB; use the Display P3 profile at 16 bits per pixel (per channel) and export as PNG; requires a wide color display to design.
  - **Provide color space–specific image/color variations if necessary** — very similar P3 colors, or P3 gradients, can clip or be indistinguishable on sRGB displays; use the Xcode asset catalog to supply per-color-space versions.
- **Platform — iOS, iPadOS:** two sets of dynamic background colors, system and grouped, each with primary/secondary/tertiary variants; use the grouped set (`systemGroupedBackground`, `secondarySystemGroupedBackground`, `tertiarySystemGroupedBackground`) for grouped table views, otherwise the system set (`systemBackground`, `secondarySystemBackground`, `tertiarySystemBackground`). Hierarchy convention: primary = overall view, secondary = grouping within the overall view, tertiary = grouping within secondary elements. Foreground dynamic colors:

| Color | Use for… | UIKit API |
|---|---|---|
| Label | Text label with primary content | label |
| Secondary label | Text label with secondary content | secondaryLabel |
| Tertiary label | Text label with tertiary content | tertiaryLabel |
| Quaternary label | Text label with quaternary content | quaternaryLabel |
| Placeholder text | Placeholder text in controls/text views | placeholderText |
| Separator | Separator that allows underlying content to show | separator |
| Opaque separator | Separator with no underlying content visible | opaqueSeparator |
| Link | Text that functions as a link | link |

- **Platform — macOS:** dynamic system colors (also viewable in the Developer palette of the standard Color panel):

| Color | Use for… | AppKit API |
|---|---|---|
| Alternate selected control text color | Text on a selected surface in a list/table | alternateSelectedControlTextColor |
| Alternating content background colors | Backgrounds of alternating rows/columns | alternatingContentBackgroundColors |
| Control accent | Accent color chosen in System Settings | controlAccentColor |
| Control background color | Background of a large element (browser/table) | controlBackgroundColor |
| Control color | Surface of a control | controlColor |
| Control text color | Text of an available control | controlTextColor |
| Current control tint | System-defined control tint | currentControlTint |
| Unavailable control text color | Text of an unavailable control | disabledControlTextColor |
| Find highlight color | Color of a find indicator | findHighlightColor |
| Grid color | Gridlines of an element (e.g. table) | gridColor |
| Header text color | Text of a header cell in a table | headerTextColor |
| Highlight color | Virtual light source onscreen | highlightColor |
| Keyboard focus indicator color | Ring around the focused control (keyboard nav) | keyboardFocusIndicatorColor |
| Label color | Text of a label with primary content | labelColor |
| Link color | A link to other content | linkColor |
| Placeholder text color | Placeholder string in a control/text view | placeholderTextColor |
| Quaternary label color | Text less important than tertiary (e.g. watermark) | quaternaryLabelColor |
| Secondary label color | Text less important than primary (subheading, etc.) | secondaryLabelColor |
| Selected content background color | Background for selected content in a key window/view | selectedContentBackgroundColor |
| Selected control color | Surface of a selected control | selectedControlColor |
| Selected control text color | Text of a selected control | selectedControlTextColor |
| Selected menu item text color | Text of a selected menu | selectedMenuItemTextColor |
| Selected text background color | Background of selected text | selectedTextBackgroundColor |
| Selected text color | Color for selected text | selectedTextColor |
| Separator color | Separator between content sections | separatorColor |
| Shadow color | Virtual shadow cast by a raised object | shadowColor |
| Tertiary label color | Text less important than secondary label | tertiaryLabelColor |
| Text background color | Background color behind text | textBackgroundColor |
| Text color | Text in a document | textColor |
| Under page background color | Background behind a document's content | underPageBackgroundColor |
| Unemphasized selected content background color | Selected content in a non-key window/view | unemphasizedSelectedContentBackgroundColor |
| Unemphasized selected text background color | Background for selected text in a non-key window/view | unemphasizedSelectedTextBackgroundColor |
| Unemphasized selected text color | Selected text in a non-key window/view | unemphasizedSelectedTextColor |
| Window background color | Background of a window | windowBackgroundColor |
| Window frame text color | Text in the window's title bar area | windowFrameTextColor |

  - App accent colors: since macOS 11, apps can specify an accent color for buttons, selection highlighting, and sidebar icons, applied when General > Accent color is *multicolor*. If people choose a non-multicolor accent, the system replaces the app's accent color throughout — except a sidebar icon using a fixed, meaning-bearing color, which the system never overrides.
- **Platform — tvOS:** consider a limited color palette that coordinates with your app logo (subtle color communicates brand while deferring to content); avoid using only color to indicate focus (subtle scaling and responsive animation are the primary ways to denote interactivity in focus).
- **Platform — visionOS:** use color sparingly, especially on glass (standard windows use system glass Materials that let physical surroundings show through, affecting legibility of colorful content) — prefer color to call attention to important info or relationships; prefer color in bold text and large areas (lightweight text/small areas with color are harder to see); in fully immersive experiences, keep brightness balanced for visual comfort — avoid bright objects on very dark/black backgrounds, especially if flashing or moving.
- **Platform — watchOS:** use background color to support content or supply information (e.g. Activity ring infographics match ring color) rather than as pure decoration; avoid full-screen background color in views that stay onscreen a long time (workout, audio-playing apps); people might prefer graphic complications to use tinted mode (a single wearer-selected color) instead of full color.
- **Specifications — system colors** (SwiftUI API names): Red (`red`), Orange (`orange`), Yellow (`yellow`), Green (`green`), Mint (`mint`), Teal (`teal`), Cyan (`cyan`), Blue (`blue`), Indigo (`indigo`), Purple (`purple`), Pink (`pink`), Brown (`brown`). visionOS system colors use the default dark color values. iOS/iPadOS system gray colors: `systemGray` through `systemGray6` (UIKit); the SwiftUI equivalent of `systemGray` is `gray`.

**Platforms:** iOS/iPadOS, macOS, tvOS, visionOS, and watchOS each have material differences, detailed above.

## Dark Mode
Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode
Dark Mode is a systemwide appearance setting that uses a dark color palette to provide a comfortable viewing experience tailored for low-light environments.
- **Avoid offering an app-specific appearance setting** — it creates extra work adjusting more than one setting, and an app that doesn't respond to the systemwide choice can appear broken.
- **Ensure your app looks good in both appearance modes** — people can also choose Auto, which switches between light and dark as conditions change through the day, potentially while your app is running.
- **Test content for legibility in both appearance modes** — e.g. with Increase Contrast and Reduce Transparency on (separately and together) in Dark Mode, dark text can become less legible on a dark background; turning on Increase Contrast in Dark Mode can sometimes *reduce* visual contrast between dark text and a dark background.
- **In rare cases, consider using only a dark appearance** — e.g. an immersive-media-viewing app that wants the UI to recede.
- **Dark Mode colors:** the palette includes dimmer backgrounds and brighter foregrounds; not simple inversions — some colors invert, some don't.
  - **Embrace colors that adapt to the current appearance** — semantic colors (`labelColor`, `controlColor` in macOS; `separator` in iOS/iPadOS) auto-adapt; for a custom color, add a Color Set asset in Xcode's asset catalog specifying bright and dim variants; avoid hard-coded, non-adaptive color values.
  - **Aim for sufficient color contrast in all appearances** — system-defined colors help; minimum contrast ratio 4.5:1; for custom foreground/background colors strive for 7:1, especially in small text.
  - **Soften the color of white backgrounds** — slightly darken content images with white backgrounds to prevent glow in the surrounding Dark Mode context.
- **Icons and images:** the system uses SF Symbols (auto-adapt to Dark Mode) and full-color images optimized for both appearances.
  - **Use SF Symbols wherever possible** — work in both modes via dynamic color tinting or vibrancy.
  - **Design separate interface icons for light and dark appearances if necessary** — e.g. a full-moon icon may need a subtle dark outline on a light background but none on dark; an oil-drop icon may need a slight border for edge visibility on a dark background.
  - **Make sure full-color images/icons look good in both appearances** — use the same asset if it works in both; otherwise modify it or create separate light/dark assets combined via asset catalogs.
- **Text:** the system uses vibrancy and increased contrast to maintain legibility on darker backgrounds.
  - **Use the system-provided label colors for labels** — primary, secondary, tertiary, quaternary label colors auto-adapt.
  - **Use system views to draw text fields/text views** — they auto-adjust for the presence/absence of vibrancy; prefer a system-provided view over drawing text yourself.

**Platforms:** No additional considerations for tvOS. Dark Mode isn't supported in visionOS or watchOS. iOS, iPadOS — uses two sets of Dark Mode background colors, *base* and *elevated*, to enhance depth perception when one dark interface layers above another (base = dimmer/recedes, elevated = brighter/advances); prefer system background colors, since Dark Mode dynamically switches base→elevated for foreground interfaces (popover, modal sheet) and for visual separation between apps in multitasking or between windows — a custom background color makes these distinctions harder to perceive. macOS — choosing the graphite accent color causes window backgrounds to pick up color from the desktop picture ("desktop tinting"); include some transparency in custom component backgrounds when appropriate, so they pick up window background color during desktop tinting — add transparency only to a component with a visible background/bezel, and only in a neutral (non-color) state, since a colored state would visibly fluctuate as the desktop picture/tinting changes.

## Icons
Source: https://developer.apple.com/design/human-interface-guidelines/icons
An effective icon is a graphic asset that expresses a single concept in ways people instantly understand.
- Interface icons (aka *glyphs*) differ from app icons — they use streamlined shapes and touches of color for a straightforward idea; design custom ones or use SF Symbols as-is or customized; both use black and clear colors to define shape, and the system applies other colors to the black areas.
- **Create a recognizable, highly simplified design** — too many details make an icon confusing/unreadable; use familiar visual metaphors directly related to the action/content.
- **Maintain visual consistency across all interface icons in your app** — whether custom-only or mixed with system icons, keep size, level of detail, stroke thickness/weight, and perspective consistent; adjust dimensions per icon's visual weight as needed.
- **In general, match the weights of interface icons and adjacent text** — unless intentionally emphasizing one, matching weight gives a consistent appearance and level of emphasis.
- **Add padding to a custom interface icon for optical alignment if necessary** — asymmetric icons can look unbalanced when geometrically centered (e.g. a download icon with more visual weight on the bottom); bake the adjustment into the asset as padding so geometric centering of the asset achieves optical centering of the icon. Adjustments are typically small but impactful.
- **Provide a selected-state icon version only if necessary** — standard system components (toolbars, tab bars, buttons) update the selected-state appearance automatically.
- **Use inclusive images** — prefer gender-neutral human figures, avoid images hard to recognize across cultures/languages.
- **Include text only when essential for conveying meaning** — e.g. a character representing text formatting; localize any individual characters shown; for suggesting a passage of text, use an abstract representation plus a flipped icon for right-to-left contexts.
- **Use a vector format (PDF or SVG) for custom interface icons** — auto-scales for high-resolution displays, unlike PNG (used for app icons/effects-laden images), which requires multiple versions; alternatively, create a custom SF Symbol with a specified scale to match emphasis with adjacent text.
- **Provide alternative text labels for custom interface icons** — accessibility descriptions let VoiceOver describe onscreen content for people with visual disabilities.
- **Avoid using replicas of Apple hardware products** — hardware designs change frequently and can date your icons; if you must show Apple hardware, use only Apple Design Resources images or the SF Symbols that represent Apple products.
- **Standard icons** — SF Symbols for common actions:

| Category | Action → Symbol name |
|---|---|
| Editing | Cut `scissors`, Copy `document.on.document`, Paste `document.on.clipboard`, Done `checkmark`, Cancel `xmark`, Delete `trash`, Undo `arrow.uturn.backward`, Redo `arrow.uturn.forward`, Compose `square.and.pencil`, Duplicate `plus.square.on.square`, Rename `pencil`, Move to `folder`, Attach `paperclip`, Add `plus`, More `ellipsis` |
| Selection | Select `checkmark.circle`, Deselect `xmark`, Delete `trash` |
| Text formatting | Superscript `textformat.superscript`, Subscript `textformat.subscript`, Bold `bold`, Italic `italic`, Underline `underline`, Align Left `text.alignleft`, Center `text.aligncenter`, Justified `text.justify`, Align Right `text.alignright` |
| Search | Search `magnifyingglass`, Find `text.page.badge.magnifyingglass`, Filter `line.3.horizontal.decrease` |
| Sharing/exporting | Share `square.and.arrow.up`, Print `printer` |
| Users and accounts | Account `person.crop.circle` |
| Ratings | Dislike `hand.thumbsdown`, Like `hand.thumbsup` |
| Layer ordering | Bring to Front `square.3.layers.3d.top.filled`, Send to Back `square.3.layers.3d.bottom.filled`, Bring Forward `square.2.layers.3d.top.filled`, Send Backward `square.2.layers.3d.bottom.filled` |
| Other | Alarm `alarm`, Archive `archivebox`, Calendar `calendar` |

**Platforms:** No additional considerations for iOS, iPadOS, tvOS, visionOS, or watchOS. macOS — **document icons**: traditionally a piece of paper with a folded top-right corner, distinguishing documents from apps even at small sizes; if you don't supply one, macOS composites your app icon and the file's extension automatically (e.g. Preview's system-generated JPG icon); you can create a set of document icons for a range of file types (e.g. Xcode's project/AR/Swift file icons). A custom document icon combines background fill, center image, and text, which the system layers/positions/masks onto the folded-corner shape (template in Apple Design Resources). **Design simple images that clearly communicate the document type** — uncomplicated shapes, a reduced distinct color palette; smallest size is 16x16 px, so stay recognizable at every size. A single expressive background-fill image (no center image) can be an effective document-type identifier (e.g. Xcode, TextEdit). **Consider reducing complexity in small icon versions** — fewer/thicker lines aligned to the pixel grid at intermediate sizes, remove lines altogether at 16x16 px. **Avoid placing important content in the top-right corner of the background fill** — the system draws the white folded corner over it. Background fill sizes: 512x512 px @1x / 1024x1024 px @2x; 256x256 px @1x / 512x512 px @2x; 128x128 px @1x / 256x256 px @2x; 32x32 px @1x / 64x64 px @2x; 16x16 px @1x / 32x32 px @2x. Center image measures half the overall document icon canvas (e.g. 16x16 px center image for a 32x32 px icon); available sizes: 256x256 px @1x / 512x512 px @2x; 128x128 px @1x / 256x256 px @2x; 32x32 px @1x / 64x64 px @2x; 16x16 px @1x / 32x32 px @2x. **Define a margin ~10% of the canvas** and keep most of the image within it — image should occupy about 80% of the canvas (e.g. ~205x205 px within a 256x256 px canvas). **Specify a succinct term if it helps identify the document type** — the system displays the file extension at the bottom edge by default, but a more descriptive term can replace it (e.g. "scene" instead of "scn"); the system auto-scales and capitalizes the text, so keep the term short.

## Images
Source: https://developer.apple.com/design/human-interface-guidelines/images
To make sure your artwork looks great on all devices you support, learn how the system displays content and how to deliver art at the appropriate scale factors.
- **Resolution.** A *point* is an abstract unit keeping visual content consistent regardless of display; in 2D platforms a point maps to a variable pixel count per the display's resolution, while in visionOS a point is an angular value that scales content with viewer distance. A *scale factor* sets bitmap resolution: @1x = 1:1 pixel density, @2x = 2:1, @3x = 3:1 — higher-resolution displays need images with more pixels.
  - **Provide high-resolution assets for all bitmap images, for every device you support** — append "@1x," "@2x," or "@3x" to filenames in the asset catalog:

| Platform | Scale factors |
|---|---|
| iPadOS, watchOS | @2x |
| iOS | @2x and @3x |
| visionOS | @2x or higher |
| macOS, tvOS | @1x and @2x |

  - **In general, design images at the lowest resolution and scale up to create high-resolution assets** — for resizable vector shapes, position control points at whole values so they stay cleanly aligned at 1x (and therefore at 2x/3x, which are multiples of 1x).
- **Formats:**

| Image type | Format |
|---|---|
| Bitmap or raster work | De-interlaced PNG files |
| PNG graphics that don't require full 24-bit color | An 8-bit color palette |
| Photos | JPEG files, optimized as necessary, or HEIC files |
| Stereo or spatial photos | Stereo HEIC |
| Flat icons, interface icons, and other flat artwork requiring high-resolution scaling | PDF or SVG files |

- **Include a color profile with each image** — helps ensure colors appear as intended on different displays.
- **Always test images on a range of actual devices** — an image that looks great at design time may appear pixelated, stretched, or compressed on real devices.

**Platforms:** No additional considerations for iOS, iPadOS, or macOS.
### tvOS
- *Parallax* is a subtle depth/dynamism effect when an element gains focus — it elevates to the foreground, sways gently, illuminates; after inactivity, out-of-focus content dims and the focused element expands. Layered images (2-5 distinct layers) are required to support parallax — layer separation + transparency create depth; interaction elevates/scales nearer layers over farther ones for a 3D effect.
> Important: Your tvOS top shelf image must use a layered image; for other focusable images, including additional Top Shelf images, layered images are strongly encouraged but optional.
> Developer note: apps that retrieve layered images from a content server at runtime must provide runtime layered images (`.lcr`), generated from LSR/Photoshop files via the `layerutil` command-line tool — these are meant to be downloaded, not embedded.
- **Use standard interface elements to display layered images** — standard views + system focus APIs (e.g. `FocusState`) auto-apply the parallax treatment when focused.
- **Identify logical foreground, middle, and background elements** — foreground for prominent elements (a character, poster/album text); middle for secondary content/effects like shadows; background as an opaque backdrop showcasing the rest without upstaging.
- **Generally keep text in the foreground** for clarity, unless you want to obscure it.
- **Keep the background layer opaque** — required (you'll get an error otherwise); varying opacity in higher layers is fine.
- **Keep layering simple and subtle** — parallax should be almost unnoticeable; excessive 3D effects look unrealistic and jarring.
- **Leave a safe zone around foreground layers** — content can be cropped as the image scales/moves when focused.
- **Always preview layered images** — throughout the design process via Xcode, Parallax Previewer (macOS), or the Parallax Exporter Photoshop plug-in, watching for scaling/clipping; preview on an actual TV for final accuracy.
### visionOS
- Images can be viewed across a much larger size range than other platforms; the system dynamically scales resolution to match current size; pixels may not line up 1:1 with screen pixels since images can be positioned at angles.
- **Create a layered app icon** — visionOS app icons use 2-3 layers moving at subtly different rates in focus for depth.
- **Prefer vector-based art for 2D images** — avoid bitmap content, which may not scale well.
- **If rasterized images are necessary, balance quality with performance** — a @2x image is fine at common viewing distances but isn't dynamically scaled and may not look sharp up close; higher resolutions increase file size and can impact runtime performance, especially above @6x; apply high-quality image filtering above @2x.
- **Spatial photos and spatial scenes:** a spatial photo is a stereoscopic photo with spatial metadata (captured on iPhone 15 Pro+, Apple Vision Pro, or a compatible camera); a spatial scene is a 3D image generated from a 2D image, adding a head-movement parallax effect (via RealityKit).
  - **Make sure spatial photos render correctly** — use the stereo HEIC format; spatial metadata lets visionOS apply treatments that minimize stereo-viewing discomfort.
  - **Prefer the feathered glass background effect** for text over spatial photos — adds contrast for readability and blurs detail to reduce discomfort.
  - **Take visual comfort into account** when converting existing 2D content to spatial photos — metadata like disparity adjustment alters 3D perception and can cause discomfort from certain viewing positions.
  - **Display spatial photos/scenes in standalone views** — avoid inline display (causes discomfort); if inline is unavoidable, provide generous spacing.
  - **Use spatial scenes for specific moments** — generation can take several seconds; avoid displaying too many at once; use scroll views/pagination/explicit actions and keep the hierarchy simple.
  - **Prefer minimal UI** when displaying immersively.
  - **Prefer larger spatial scenes centered in the field of view** — smaller scenes provide less parallax impact.
### watchOS
- **In general, avoid transparency to keep image files small** — more efficient to bake in the background if always composited on the same solid color; transparency is still needed for complication images, menu icons, and other template interface icons (the system uses it to determine where to apply color).
- **Use autoscaling PDFs for a single asset across all screen sizes** — design for the 40mm/42mm screens at 2x; WatchKit auto-scales per device:

| Screen size | Image scale |
|---|---|
| 38mm | 90% |
| 40mm | 100% |
| 41mm | 106% |
| 42mm | 100% |
| 44mm | 110% |
| 45mm | 119% |
| 49mm | 119% |

## Materials
Source: https://developer.apple.com/design/human-interface-guidelines/materials
A material is a visual effect that creates a sense of depth, layering, and hierarchy between foreground and background elements.
- Materials visually separate foreground elements (text, controls) from background elements (content, solid colors); letting color pass through establishes hierarchy and helps people retain a sense of place. Two types: **Liquid Glass** (dynamic material unifying the design language across platforms, presenting controls/navigation without obscuring content) and **Standard materials** (help with visual differentiation within the content layer).
- **Liquid Glass** forms a distinct functional layer for controls/navigation (tab bars, sidebars) that floats above the content layer; content scrolls/peeks through beneath while controls stay legible.
  - **Don't use Liquid Glass in the content layer** — use Standard materials there instead (e.g. app backgrounds); exception: transient interactive content-layer elements like Sliders/Toggles take on Liquid Glass when activated, to emphasize interactivity.
  - **Use Liquid Glass effects sparingly** — standard system-framework components pick it up automatically; if applying to a custom control, limit it to the most important functional elements (overuse distracts from the underlying content).
  - **Only use clear Liquid Glass for components over visually rich backgrounds.** Two variants: *regular* blurs and adjusts luminosity of background content to maintain legibility (scroll edge effects further blur/reduce background opacity); most system components use it — use for components where background content risks legibility issues, or with significant text (alerts, sidebars, popovers). *Clear* is highly translucent, prioritizing visibility of underlying content — use for components floating over media backgrounds (photos/videos) for a more immersive experience. For clear-variant contrast: if underlying content is bright, consider a dark dimming layer of 35% opacity (`clear` API); if underlying content is sufficiently dark, or you use standard AVKit media playback controls (which provide their own dimming layer), no dimming layer is needed.
- **Standard materials:** use `UIBlurEffect`, `UIVibrancyEffect`, `NSVisualEffectView.BlendingMode` to convey structure in content beneath Liquid Glass.
  - **Choose materials/effects based on semantic meaning and recommended usage**, not the apparent color they impart — system settings can change appearance/behavior.
  - **Use vibrant colors on top of materials** for legibility — system-defined vibrant colors avoid concerns about being too dark/bright/saturated/low-contrast in different contexts.
  - **Consider contrast and visual separation when combining a material with blur/vibrancy** — thicker (more opaque) materials give better contrast for text/fine features; thinner (more translucent) materials help retain context via a visible reminder of background content.

**Platforms:**
- **iOS, iPadOS:** four standard materials remain available alongside Liquid Glass — ultra-thin, thin, regular (default), thick. Vibrant colors are tuned per material for labels (`UIVibrancyEffectStyle.label` default, `.secondaryLabel`, `.tertiaryLabel`, `.quaternaryLabel` — generally avoid quaternary on thin/ultraThin, contrast too low), fills (`.fill` default, `.secondaryFill`, `.tertiaryFill`, usable on all materials), and a single default separator vibrancy that works on all materials.
- **macOS:** several standard materials (`NSVisualEffectView.Material`) with designated purposes, plus vibrant versions; choose when to allow vibrancy in custom views/controls (test across contexts); choose a background blending mode complementing your design — behind window or within window (`NSVisualEffectView.BlendingMode`). Choosing the graphite accent color triggers *desktop tinting* (window backgrounds pick up color from the desktop picture) — see Dark Mode.
- **tvOS:** Liquid Glass appears throughout navigation elements and system experiences (Top Shelf, Control Center); some elements (image views, buttons) adopt it on focus. Standard materials remain available for content-layer structure:

| Material | Recommended for |
|---|---|
| ultraThin | Full-screen views requiring a light color scheme |
| thin | Overlay views partially obscuring content, requiring a light color scheme |
| regular | Overlay views partially obscuring content |
| thick | Overlay views partially obscuring content, requiring a dark color scheme |

- **visionOS:** windows generally use an unmodifiable system-defined material called *glass*, letting light, the current Environment, virtual content, and physical surroundings show through; glass limits background color information so windows keep content contrast while brightening/darkening with surroundings.
> Note: visionOS doesn't have a distinct Dark Mode setting — glass automatically adapts to the luminance of objects/colors behind it.
  - **Prefer translucency to opaque colors in windows** — opacity can feel constricting and reduce spatial awareness.
  - If needed for visual separation or interactivity: thin material brings attention to interactive elements (buttons, selected items); regular material visually separates sections (sidebar, grouped table view); thick material creates a dark element that stays visually distinct on top of a `regular` background.
  - visionOS applies vibrancy to text/symbols/fills on materials: `UIVibrancyEffectStyle.label` (standard text), `.secondaryLabel` (footnotes/subtitles), `.tertiaryLabel` (inactive elements, only when high legibility isn't needed).
- **watchOS:** **use materials to provide context in full-screen modal views** (common in watchOS) — material-layer contrast orients people and distinguishes controls/system elements from other content; avoid removing/replacing default modal-sheet material backgrounds.

## Motion
Source: https://developer.apple.com/design/human-interface-guidelines/motion
Beautiful, fluid motions bring the interface to life, conveying status, providing feedback and instruction, and enriching the visual experience of your app or game.
- Many system components include motion automatically, adjusting to accessibility settings or input method (e.g. Liquid Glass movement responds more emphatically to direct touch than to trackpad interaction).
- **Add motion purposefully, supporting the experience without overshadowing it** — gratuitous/excessive animation distracts or causes physical discomfort.
- **Make motion optional** — not everyone can or wants to experience it; supplement visual feedback with haptics/audio so motion isn't the only channel for important information.
- **Providing feedback:**
  - **Strive for realistic feedback motion that follows people's gestures and expectations** — motion that doesn't make sense disorients (e.g. sliding a view down to reveal it means sliding it up, not sideways, to dismiss).
  - **Aim for brevity and precision in feedback animations** — brief/precise animation feels lightweight and unobtrusive, and often communicates more effectively than prominent animation.
  - **In apps, generally avoid adding motion to frequently occurring UI interactions** — the system already animates standard elements subtly; avoid extra motion people must watch every time they use a custom element.
  - **Let people cancel motion** — don't make people wait for an animation to finish before acting, especially for repeated animations.
  - **Consider using animated symbols where it makes sense** — SF Symbols 5+ supports animating SF Symbols or custom symbols.
- **Leveraging platform capabilities:**
  - **Make sure your game's motion looks great by default on each platform** — maintaining 30-60 fps typically gives a smooth, visually appealing experience; use each platform's graphics capabilities for good defaults without requiring people to change settings.
  - **Let people customize the visual experience to optimize performance/battery life** — e.g. switching power modes when external power is detected.

**Platforms:** No additional considerations for iOS, iPadOS, macOS, or tvOS.
### visionOS
Motion can combine with Depth to provide essential feedback when people look at interactive elements; motion is likely a large part of the experience, so avoiding distraction, confusion, or discomfort is crucial.
- **Avoid displaying motion at the edges of the field of view as much as possible** — peripheral motion is distracting and can cause discomfort (feels like self/surroundings moving); if an object must move in the periphery during immersion, match its brightness to the rest of the visible content.
- **Help people stay comfortable when showing movement of large virtual objects** — an object large enough to fill much of the field of view can be perceived as part of the surroundings; increase its translucency or lower its contrast to make motion less noticeable.
> Note: people can feel discomfort even moving a large virtual object themselves (e.g. a window); adjusting translucency/contrast helps, but also consider keeping the window fairly small.
- **Consider using fades when relocating an object** if the movement itself communicates nothing useful — fade out before moving, fade back in at the new location.
- **In general, avoid letting people rotate a virtual world** — rotating the whole world upsets people's sense of stability even when subtle and self-controlled; prefer instantaneous directional changes during a quick fade-out instead.
- **Consider giving people a stationary frame of reference** — movement is easier to handle within an area that itself doesn't move; if the entire surrounding area moves (e.g. auto-moving a player through space), people can feel unwell.
- **Avoid showing objects that oscillate in a sustained way** — particularly avoid a frequency around 0.2 Hz (people are very sensitive to it); if needed, keep amplitude low and consider translucency.
### watchOS
SwiftUI provides a powerful, streamlined way to add motion; use `WKInterfaceImage` for WatchKit-based layout/appearance animation or animated image sequences.
> Note: all layout- and appearance-based animations automatically include built-in easing at start and end; this easing cannot be turned off or customized.

## SF Symbols
Source: https://developer.apple.com/design/human-interface-guidelines/sf-symbols
SF Symbols provides thousands of consistent, highly configurable symbols that integrate seamlessly with the San Francisco system font, automatically aligning with text in all weights and sizes.
- Use a symbol to convey an object/concept anywhere interface icons appear (toolbars, tab bars, context menus, within text). Symbol/feature availability varies by targeted system version. Understand the terms/conditions — symbols (or confusingly similar images) are prohibited in app icons, logos, or other trademarked use.
- **Rendering modes** — symbols organize paths into distinct layers (e.g. `cloud.sun.rain.fill`: primary = cloud, secondary = sun/rays, tertiary = raindrops) to support four modes:
  - **Monochrome** — one color applied to all layers; paths render in the specified color or as a transparent shape within a color-filled path.
  - **Hierarchical** — one color applied to all layers, varying opacity by each layer's hierarchical level, creating depth.
  - **Palette** — two or more colors applied, one per layer; specifying only two colors for a three-level symbol makes secondary and tertiary share a color.
  - **Multicolor** — intrinsic colors applied to some symbols to enhance meaning (e.g. `leaf` uses green, `trash.slash` uses red); some multicolor symbols include layers that can still receive other colors.
  - Regardless of mode, use system-provided colors so symbols auto-adapt to accessibility accommodations and appearance modes (vibrancy, Dark Mode).
  - **Confirm that a symbol's rendering mode works well in every context** — size and background contrast affect discernibility; the automatic setting picks a preferred mode, but check whether a different mode improves legibility.
- **Gradients** (SF Symbols 7+): generates a smooth linear gradient from a single source color; usable across all rendering modes, for system/custom colors and custom symbols; renders at any size but looks best larger.
- **Variable color:** represents a characteristic that changes over time (capacity, strength) regardless of rendering mode, applying color to different layers as a value crosses thresholds between zero and 100 percent (e.g. `speaker.wave.3` mapping wave layers to decibel ranges). Some layers can opt out (e.g. the speaker shape itself doesn't change). **Use variable color to communicate change — don't use it to communicate depth** (use Hierarchical rendering for depth/hierarchy instead).
- **Weights and scales:** nine symbol weights (ultralight to black) correspond to San Francisco font weights for precise weight matching with adjacent text. Three scales per symbol — small, medium (default), large — defined relative to the SF font's cap height; specifying a scale adjusts emphasis relative to adjacent text without disrupting weight matching (`imageScale(_:)` SwiftUI, `UIImage.SymbolScale` UIKit, `NSImage.SymbolConfiguration` AppKit).
- **Design variants:** fill, slash, enclosed (circle/square/rectangle), and language/script-specific variants (Latin, Arabic, Hebrew, Hindi, Thai, Chinese, Japanese, Korean, Cyrillic, Devanagari, several Indic numeral systems — auto-adapt to device language) communicate precise states/actions while keeping visual consistency. Outline is the most common (no solid areas, resembles text); slash and enclosed variants can combine with outline or fill. Usage guidance: outline works well in toolbars/lists alongside text; enclosing shapes improve legibility at small sizes; fill gives more visual emphasis (good for iOS tab bars, swipe actions, accent-color selection). Many views auto-determine outline vs. fill (e.g. iOS tab bar prefers fill, toolbar takes outline).
- **Animations** — work on all SF Symbols across rendering modes/weights/scales and on custom symbols; control playback (once or repeating), speed, and reverse-before-repeat:
  - **Appear** — symbol gradually emerges into view. **Disappear** — symbol gradually recedes out of view.
  - **Bounce** — briefly scales with an elastic movement up or down then returns to initial state; plays once by default; communicates an action occurred or needs to occur.
  - **Scale** — changes symbol size persistently (unlike bounce) until reset or removed; for drawing attention to a selection or as choice feedback.
  - **Pulse** — varies opacity over time, by default only on layers annotated to pulse (optionally all layers); communicates ongoing activity, played continuously until a condition is met.
  - **Variable color (animation)** — incrementally varies layer opacity, cumulative (persists per layer until cycle completes) or iterative (one layer at a time); communicates progress/ongoing activity (playback, connecting, broadcasting); can autoreverse and hide inactive layers instead of reducing opacity. Layer arrangement determines repeat behavior: *open loop* (linear, start/end don't meet) vs. *closed loop* (complete shape, start/end meet, e.g. circular progress) — closed loop gives seamless continuous playback.
  - **Replace** — replaces one symbol with another, works between arbitrary symbols/weights/rendering modes; three configurations: down-up (outgoing scales down, incoming scales up — state change), up-up (both scale up — forward progression), off-up (outgoing hides immediately, incoming scales up — emphasizes the next state/action).
  - **Magic Replace** — smart transition between two symbols with related shapes (slashes draw on/off, badges appear/disappear or replace independently of the base symbol); new default replace animation, but falls back to down-up between unrelated symbols (with a choosable custom fallback direction).
  - **Wiggle** — moves the symbol back and forth along a directional axis; highlights a change or an overlookable call-to-action; can reinforce meaning (e.g. a directional arrow).
  - **Breathe** — smoothly increases/decreases symbol presence for a "living" quality; conveys status changes or ongoing activity (e.g. active recording); similar to Pulse but changes both opacity and size (Pulse changes opacity only).
  - **Rotate** — rotates the symbol as a visual indicator or to imitate real-world behavior (e.g. confirming an in-progress task); some symbols rotate entirely, others only certain parts (By Layer rotation, e.g. desk-fan blades only).
  - **Draw On / Draw Off** (SF Symbols 7+) — draws the symbol along a path through guide points, offscreen-to-onscreen (Draw On) or onscreen-to-offscreen (Draw Off); all layers at once, staggered, or one at a time; conveys progress (e.g. download) or reinforces meaning (e.g. directional arrow).
  - **Apply symbol animations judiciously** — no hard limit, but too many overwhelm an interface.
  - **Make sure animations serve a clear purpose** in communicating a symbol's intent — consider how people might interpret an animation or combination.
  - **Use symbol animations to communicate information more efficiently** — present complex info simply, without much visual space.
  - **Consider your app's tone when adding animations** — align with brand identity and overall style.
- **Custom symbols:** export a template for a similar symbol, then modify with a vector-editing tool.
> Important: SF Symbols includes copyrighted symbols depicting Apple products/features — you can display but not customize them; the SF Symbols app badges noncustomizable symbols with an Info icon.
  - *Annotating* assigns a specific color or hierarchical level (primary/secondary/tertiary) to each layer; you can use a different rendering mode per instance depending on supported modes.
  - **Use the template as a guide** — match system symbols in level of detail, optical weight, alignment, position, perspective; aim for simple, recognizable, inclusive, and directly related to the action/content.
  - **Assign negative side margins if necessary** — aids optical horizontal alignment when a symbol has a badge or other width-increasing element; name margins per the configuration pattern (e.g. "left-margin-Regular-M").
  - **Optimize layers to use animations with custom symbols** — annotate layers in the SF Symbols app for layer-based animation; Z-order determines color-application order for variable color (front-to-back or back-to-front); can animate by layer groups.
  - **Test animations for custom symbols** — draw with whole shapes (e.g. draw the full shape of a person rather than a cutout, then add an offset path annotated as an erase layer) to preserve layer info needed for correct animation.
  - **Avoid making custom symbols that include common variants** (enclosures, badges) — use the SF Symbols app's component library instead, for design consistency.
  - **Provide alternative text labels for custom symbols** — accessibility descriptions for VoiceOver.
  - **Don't design replicas of Apple products** — copyrighted; also can't customize a symbol SF Symbols identifies as representing an Apple feature/product.

**Platforms:** No additional platform considerations.

## Typography
Source: https://developer.apple.com/design/human-interface-guidelines/typography
Your typographic choices can help you display legible text, convey an information hierarchy, communicate important content, and express your brand or style.
- **Ensuring legibility:**
  - **Use font sizes most people can read easily** — follow recommended default/minimum text sizes per platform (custom and system fonts); thin custom-font weights need larger-than-recommended sizes:

| Platform | Default size | Minimum size |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

  - **Test legibility in different contexts** — e.g. test game text on each supported platform; if hard to read, use a larger size, increase text/background contrast, or use legibility-optimized typefaces like the system fonts.
  - **In general, avoid light font weights** — prefer Regular, Medium, Semibold, or Bold system font weights; avoid Ultralight, Thin, Light (hard to see, especially small).
- **Conveying hierarchy:**
  - **Adjust font weight, size, and color to emphasize important information and visualize hierarchy** — maintain relative hierarchy/visual distinction as people adjust text sizes.
  - **Minimize the number of typefaces you use**, even in a highly customized interface — too many typefaces obscure hierarchy, hinder readability, and feel inconsistent.
  - **Prioritize important content when responding to text-size changes** — not all content is equally important (e.g. increasing text size shouldn't necessarily enlarge tab titles or a game's transient hit-damage values).
- **Using system fonts:** **San Francisco (SF)** — sans serif family including SF Pro, SF Compact, SF Arabic, SF Armenian, SF Georgian, SF Hebrew, SF Mono; SF Pro/Compact/Arabic/Armenian/Georgian/Hebrew also offer rounded variants. **New York (NY)** — serif family designed to work alone or alongside SF. Both are provided as *variable* fonts (combine styles in one file, support interpolation between styles).
  > Note: variable fonts support optical sizing — *dynamic optical sizes* merge discrete optical sizes (Text, Display) and weights into a single continuous design, interpolating each glyph to fit the point size precisely; discrete optical sizes are only needed with a design tool lacking full variable-font support.
  - System fonts offer weights (Ultralight to Black) and — for SF — widths (Condensed, Expanded); SF Symbols use equivalent weights for precise matching with adjacent text.
  - *Text styles* specify font weight + point size + leading per text size, working with both typeface families (e.g. body = comfortable multi-line reading values; headline = size/weight distinguishing a heading), forming a typographic hierarchy that scales with system text size / accessibility adjustments.
  - **Consider using the built-in text styles** — convenient, consistent hierarchy; ensures Dynamic Type and larger accessibility type size support.
  - **Modify built-in text styles if necessary via symbolic traits** — e.g. the bold trait adds a hierarchy level; adjust leading for readability/space (loose leading aids line-tracking in wide columns/long passages; tight leading helps fit lines in constrained-height areas like list rows, but avoid tight leading for three-plus lines even when height is limited).
  > Developer note: use `Font.Design` constants to access system fonts (e.g. `Font.Design.default` for the system font on all platforms, `Font.Design.serif` for NY) — don't embed system fonts in your app or game.
  - **Adjust tracking in interface mockups if necessary** — a running app dynamically adjusts tracking at every point size; mockups may need manual tracking adjustment (see Tracking values below).
- **Using custom fonts:**
  - **Make sure custom fonts are legible** at various viewing distances/conditions — follow the recommended minimum sizes per style/weight.
  - **Implement accessibility features for custom fonts** — system fonts auto-support Dynamic Type and accessibility features (e.g. Bold Text); custom fonts must implement the same behaviors; in Unity-based games use Apple's Unity plug-ins for Dynamic Type support, or otherwise let players adjust text size.
- **Supporting Dynamic Type** — a system-level feature (iOS, iPadOS, tvOS, visionOS, watchOS) letting people adjust visible text size for readability/comfort:
  - **Make sure your app's layout adapts to all font sizes** — verify scaling/legibility at all sizes; test with Larger Accessibility Text Sizes (Settings > Accessibility > Display & Text Size > Larger Text) on iPhone/iPad.
  - **Increase the size of meaningful interface icons as font size increases** — SF Symbols auto-scale with Dynamic Type changes.
  - **Keep text truncation to a minimum as font size increases** — show as much useful text at the largest accessibility size as at the largest standard size; avoid truncating in scrollable regions unless a separate view offers the rest; configure labels to use as many lines as needed (`numberOfLines`).
  - **Consider adjusting layout at large font sizes** — in horizontally constrained contexts, inline items (glyphs, timestamps) and container boundaries can crowd/truncate/overlap text; consider a stacked layout (text above secondary items); reduce multicolumn text's column count as font size increases (`isAccessibilityCategory`).
  - **Maintain a consistent information hierarchy regardless of current font size** — e.g. keep primary elements toward the top of a view even at very large font sizes.
- **Specifications:** emphasized variants of system text styles are available via symbolic traits (SwiftUI `bold()`; UIKit `traitBold` in `UIFontDescriptor`); emphasized weights can be medium, semibold, bold, or heavy.

macOS built-in text styles:

| Text style | Weight | Size (pt) | Line height (pt) | Emphasized weight |
|---|---|---|---|---|
| Large Title | Regular | 26 | 32 | Bold |
| Title 1 | Regular | 22 | 26 | Bold |
| Title 2 | Regular | 17 | 22 | Bold |
| Title 3 | Regular | 15 | 20 | Semibold |
| Headline | Bold | 13 | 16 | Heavy |
| Body | Regular | 13 | 16 | Semibold |
| Callout | Regular | 12 | 15 | Semibold |
| Subheadline | Regular | 11 | 14 | Semibold |
| Footnote | Regular | 10 | 13 | Semibold |
| Caption 1 | Regular | 10 | 13 | Medium |
| Caption 2 | Medium | 10 | 13 | Semibold |

tvOS built-in text styles:

| Text style | Weight | Size (pt) | Leading (pt) | Emphasized weight |
|---|---|---|---|---|
| Title 1 | Medium | 76 | 96 | Bold |
| Title 2 | Medium | 57 | 66 | Bold |
| Title 3 | Medium | 48 | 56 | Bold |
| Headline | Medium | 38 | 46 | Bold |
| Subtitle 1 | Regular | 38 | 46 | Medium |
| Callout | Medium | 31 | 38 | Bold |
| Body | Medium | 29 | 36 | Bold |
| Caption 1 | Medium | 25 | 32 | Bold |
| Caption 2 | Medium | 23 | 30 | Bold |

macOS and tvOS tracking values (identical table for both platforms):

| Size (pt) | Tracking (1/1000 em) | Tracking (pt) |
|---|---|---|
| 6 | +41 | +0.24 |
| 7 | +34 | +0.23 |
| 8 | +26 | +0.21 |
| 9 | +19 | +0.17 |
| 10 | +12 | +0.12 |
| 11 | +6 | +0.06 |
| 12 | 0 | 0.0 |
| 13 | -6 | -0.08 |
| 14 | -11 | -0.15 |
| 15 | -16 | -0.23 |
| 16 | -20 | -0.31 |
| 17 | -26 | -0.43 |
| 18 | -25 | -0.44 |
| 19 | -24 | -0.45 |
| 20 | -23 | -0.45 |
| 21 | -18 | -0.36 |
| 22 | -12 | -0.26 |
| 23 | -4 | -0.10 |
| 24 | +3 | +0.07 |
| 25 | +6 | +0.15 |
| 26 | +8 | +0.22 |
| 27 | +11 | +0.29 |
| 28 | +14 | +0.38 |
| 29 | +14 | +0.40 |
| 30 | +14 | +0.40 |
| 31 | +13 | +0.39 |
| 32 | +13 | +0.41 |
| 33 | +12 | +0.40 |
| 34 | +12 | +0.40 |
| 35 | +11 | +0.38 |
| 36 | +10 | +0.37 |
| 37 | +10 | +0.36 |
| 38 | +10 | +0.37 |
| 39 | +10 | +0.38 |
| 40 | +10 | +0.37 |
| 41 | +9 | +0.36 |
| 42 | +9 | +0.37 |
| 43 | +9 | +0.38 |
| 44 | +8 | +0.37 |
| 45 | +8 | +0.35 |
| 46 | +8 | +0.36 |
| 47 | +8 | +0.37 |
| 48 | +8 | +0.35 |
| 49 | +7 | +0.33 |
| 50 | +7 | +0.34 |
| 51 | +7 | +0.35 |
| 52 | +6 | +0.31 |
| 53 | +6 | +0.33 |
| 54 | +6 | +0.32 |
| 56 | +6 | +0.30 |
| 58 | +5 | +0.28 |
| 60 | +4 | +0.26 |
| 62 | +4 | +0.24 |
| 64 | +4 | +0.22 |
| 66 | +3 | +0.19 |
| 68 | +2 | +0.17 |
| 70 | +2 | +0.14 |
| 72 | +2 | +0.14 |
| 76 | +1 | +0.07 |
| 80 | 0 | 0 |
| 84 | 0 | 0 |
| 88 | 0 | 0 |
| 92 | 0 | 0 |
| 96 | 0 | 0 |

**Platforms:** iOS, iPadOS — SF Pro is the system font; apps can also use NY. macOS — SF Pro is the system font; NY is available for Mac Catalyst apps; macOS doesn't support Dynamic Type. Use dynamic system font variants to match standard-control text:

| Dynamic font variant | API |
|---|---|
| Control content | controlContentFont(ofSize:) |
| Label | labelFont(ofSize:) |
| Menu | menuFont(ofSize:) |
| Menu bar | menuBarFont(ofSize:) |
| Message | messageFont(ofSize:) |
| Palette | paletteFont(ofSize:) |
| Title | titleBarFont(ofSize:) |
| Tool tips | toolTipsFont(ofSize:) |
| Document text (user) | userFont(ofSize:) |
| Monospaced document text (user fixed pitch) | userFixedPitchFont(ofSize:) |
| Bold system font | boldSystemFont(ofSize:) |
| System font | systemFont(ofSize:) |

tvOS — SF Pro is the system font; apps can also use NY. visionOS — SF Pro is the system font; if using NY, specify the type styles you want; visionOS uses bolder versions of the Dynamic Type body/title styles and introduces Extra Large Title 1 and Extra Large Title 2 for wide, editorial-style layouts. **In general, prefer 2D text** — more visual depth makes text harder to read (a small amount of 3D text can be a fun accent, but content people need to read/understand should have little or no visual depth). **Make sure text looks good and stays legible when scaled** — pick a text style that looks good at full scale, then test at different scales. **Maximize contrast between text and its container background** — the system defaults to white text for strong contrast with the default system background material; test any different color across contexts. **If text isn't on a background, consider bolding it to improve legibility** — generally avoid shadows for contrast in this case, since there may be no accurate surface to cast a shadow onto. **Keep text facing people as much as possible** — use billboarding (text rotates to face the wearer regardless of movement) for text tied to a point in space; without it, text viewed from the side/an oblique angle becomes unreadable. watchOS — SF Compact is the system font; apps can also use NY; complications use SF Compact Rounded.
