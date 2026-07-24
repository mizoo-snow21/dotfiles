---
name: apple-hig
description: Use when designing, building, or reviewing UI for any Apple platform (iOS, iPadOS, macOS, watchOS, tvOS, visionOS) — apps, games, widgets, complications, Live Activities, app icons, App Store assets — or when choosing components, navigation, layout, typography, color, materials (Liquid Glass), motion, haptics, or accessibility behavior that must follow Apple's Human Interface Guidelines.
---

# Apple Human Interface Guidelines

Complete distillation of Apple's HIG (all 157 guideline articles, crawled 2026-07-23, includes the Liquid Glass design language and the June 2026 design principles). Coverage manifest: [INDEX.md](INDEX.md).

## How to use

1. Identify the target platform(s) and read the matching part of `references/platforms.md`.
2. Load ONLY the reference files relevant to the task (routing table below). Each file contains per-page distilled rules with source URLs; each `##` heading is one HIG article.
3. Apply the design principles below as tiebreakers when guidelines compete.
4. Before signing off, run the review checklist at the bottom.

## Routing table

| Task involves | Read |
|---|---|
| Platform conventions, what makes an app feel native, games | `references/platforms.md` |
| App icons, color, dark mode, icons/images, materials & Liquid Glass, motion, SF Symbols, typography, branding | `references/foundations-visual.md` |
| Accessibility, inclusion, layout & safe areas, spatial layout (visionOS), privacy, right-to-left, immersive experiences, UX writing | `references/foundations-experience.md` |
| Flows: onboarding, launching, loading, feedback, search, settings, data entry, file management, notifications management, modality, multitasking, drag & drop, undo, charts/data, audio/video/haptics playback, collaboration, ratings, printing, help, accounts, workouts, live-viewing | `references/patterns.md` |
| Charts, image/text/web views, boxes, collections, labels, lists & tables, outline/column views, split views, tab views, lockups, disclosure controls | `references/components-content-layout.md` |
| Buttons, menus, the menu bar, context/edit/Dock menus, toolbars, ornaments (visionOS), pop-up/pull-down buttons, activity views (share sheets), Home Screen quick actions | `references/components-menus-actions.md` |
| Tab bars, sidebars, search fields, path/token fields, alerts, action sheets, sheets, popovers, panels, windows, scroll views, page controls | `references/components-nav-presentation.md` |
| Text fields, toggles, sliders, steppers, pickers, segmented controls, combo boxes, color/image wells, digit entry, virtual keyboards | `references/components-selection-input.md` |
| Widgets, complications, watch faces, Live Activities, notifications, controls, App Shortcuts, status bars, progress indicators, gauges, activity rings, rating indicators, top shelf (tvOS), snippets (Siri) | `references/components-status-system.md` |
| Touch gestures, keyboards & shortcuts, pointing devices, Apple Pencil & Scribble, Digital Crown, Action button, Camera Control, eyes (visionOS), game controls, focus & selection (tvOS), remotes, gyro/accelerometer, nearby interactions | `references/inputs.md` |
| AirPlay, Always On, App Clips, Apple Pay, AR, CareKit, CarPlay, Game Center, generative AI, HealthKit, HomeKit, iCloud, ID Verifier, iMessage apps, in-app purchase | `references/technologies-a.md` |
| Live Photos, Mac Catalyst, machine learning, maps, NFC, photo editing, ResearchKit, SharePlay, ShazamKit, Sign in with Apple, Siri, Tap to Pay, VoiceOver, Wallet | `references/technologies-b.md` |

## Design principles (the tiebreakers)

- **Purpose** — create value; keep focused on the features people actually use; differentiate rather than re-create existing solutions.
- **Agency** — stay out of the way; let people explore without locked flows (guided flows must be skippable); make mistakes cheap to reverse.
- **Responsibility** — be transparent about what the product does and why; collect only the data it needs and protect it.
- **Familiarity** — use concepts people know; keep visuals and interactions consistent; give clear feedback via system patterns.
- **Flexibility** — design for everyone (accessibility from the start); preserve context across platforms/configurations; support many input methods; give every platform the same care.
- **Simplicity** — include just what's necessary (simplicity ≠ minimalism); be concise; establish hierarchy so people know where they are and what comes next.
- **Craft** — quality sets the tone; prototype, iterate, discard what doesn't work; shipping isn't the finish line.
- **Delight** — know the emotion you want to inspire; create defining moments; never let delight become decoration that blocks the task.

## Universal specs (memorize)

- Control sizes (default / minimum): iOS & iPadOS **44x44 / 28x28 pt**, macOS **28x28 / 20x20 pt**, tvOS **66x66 / 56x56 pt**, visionOS **60x60 / 28x28 pt**, watchOS **44x44 / 28x28 pt**. Pad ~12 pt around bezeled elements, ~24 pt around bezel-less ones.
- Support **Dynamic Type**; test layouts at accessibility text sizes. Minimum text contrast **4.5:1** (large text 3:1).
- Never rely on color alone to convey information; respect **Reduce Motion**, **Reduce Transparency**, **Increase Contrast**, VoiceOver, and Switch Control.
- Respect **safe areas** and system-defined margins; never obscure the status bar, Dynamic Island, or Home indicator with content people need.
- Use **system components, standard gestures, SF Symbols, and semantic (system) colors** before custom ones — they adapt automatically to platforms, appearances (Dark Mode), and accessibility settings.
- **Liquid Glass**: system component layers (bars, sheets, controls) use the Liquid Glass material; keep it in the control layer and out of the content layer — in content, convey structure with standard materials (blur/vibrancy effects) instead. Avoid glass-on-glass stacking, and don't tint labels colors that fight colorful content behind them.
- Test every design in **light and dark**, at **smallest and largest supported window/screen sizes**, and in **RTL** if localized.

## Review checklist

Before approving any Apple-platform design:

- [ ] Correct component chosen for the job (each reference file states "Use for / Prefer X" per component)?
- [ ] Platform considerations section of every used component checked for the target platform?
- [ ] Hit targets, contrast, Dynamic Type, VoiceOver labels verified?
- [ ] Dark Mode + light mode both designed?
- [ ] System patterns used for alerts/feedback/undo instead of custom ones?
- [ ] Text follows `writing` guidance (concise labels, sentence/title case per platform conventions)?

## Common mistakes

- Designing iOS-first and porting pixel-identical layouts to iPad/Mac — each platform gets its own idioms (sidebar vs tab bar, toolbars, menu bar, pointer vs touch).
- Custom-styling a system component until it loses its built-in accessibility and adaptivity — if you fight the component, you chose the wrong component.
- Burying key actions in menus on touch platforms, or exposing every action as a toolbar button on macOS instead of using the menu bar.
- Using alerts for non-critical information (use feedback patterns), or sheets for tasks that aren't self-contained.
- Skipping the technology- and system-experience pages (Apple Pay buttons, Sign in with Apple buttons, widget update-frequency rules, notification etiquette) — these carry hard rules that reviews flag. (Numeric widget reload budgets live in WidgetKit developer docs, not the HIG.)
