# Typography, Color, Depth & Polish

Load when: choosing type scale/weight/color as hierarchy tools, setting line length/height or picking fonts, building a functional color system (HSL, grey/primary/accent palettes), checking contrast/accessibility, deciding borders vs shadows vs background contrast, defining an elevation system, choosing imagery/icons, or adding finishing polish.

Contents: Typography — Scale, Hierarchy & Readability · Color Systems — HSL, Palettes & Shades · Color Meaning, Contrast & Accessibility · Depth, Elevation & Borders · Imagery & Icons · Brand, Personality & Finishing Polish

## Typography — Scale, Hierarchy & Readability

### Typeface selection
Limit to 2 typefaces (heading + body); use italic/bold for emphasis, not a 3rd. Default body text to the OS system-font stack — custom fonts add load delay, FOUC, inconsistent rendering; reserve custom fonts for headings. When unsure, use a neutral sans-serif. Match a typeface's design intent to its usage size.
- Do: shortlist candidates by weight count (10+ suggests craft) or by studying admired sites.
- Avoid: custom fonts for body copy; a display face used at small body sizes.
⚖ Tension: serif vs sans → tradeoffs-decision-points.md (typo-d02)
⟨rui1-041, rui1-042, rui1-043, rui1-044, uxp1-001, uxp1-002⟩

### Font-size scale
Define a fixed set of allowed sizes up front. For interface (not editorial) work, hand-pick values aligned to the spacing scale rather than deriving purely from a modular ratio — ratio scales yield fractional pixels and still miss sizes UI work needs. Use px/rem, never em (compounds against the ancestor, can drift off-scale).
- Exception: editorial content can use a modular ratio scale; round values manually to avoid subpixel drift.
⟨rui1-038, rui1-039, rui1-040⟩

### Hierarchy via size and weight
Enlarge the single most valuable info conspicuously; cap to 2-3 distinct sizes per view. Pair contrasting weights (≥2 steps apart) — heavier for titles as real hierarchy, not decoration; weight contrast to distinguish labels from data, nav from content, selected from unselected.
- Avoid: enlarging many elements at once; near-identical font families that read as a mistake.
⟨uxp1-003, di4-063⟩

### Body-text baseline and font-scaling resilience
16px / 1.5 line-height / normal letter-spacing is a safe English baseline. Never disable device text scaling or pinch-zoom. Layouts must adapt as text scales up (deprioritize/hide low-importance elements) rather than break.
- Ask: "Is device text scaling disabled anywhere in this build?"
⟨uxp1-004, laws1-038⟩

### On-screen reading fundamentals
Use generous point size and larger-x-height typefaces (e.g. Verdana) — equal nominal size ≠ equal perceived size. Screens fatigue eyes more than paper; compensate with high contrast, generous size, short chunked text over unbroken paragraphs. Text so small it forces a squint can itself induce negative emotion (facial-feedback effect).
⟨psy1-023, psy1-024, psy2-038⟩

### Avoid decorative fonts for legibility-critical text
Don't use ornate, script, italic, or highly geometric (confusable e/c/d/o) faces for instructions or small legibility-critical text — they impede pattern recognition, slow reading, and make content feel harder/less trustworthy even with identical wording.
- Trade-off: decorative mood vs perceived and actual ease of following instructions.
⟨di4-048, psy1-022⟩

### All-caps and letter-spacing
Reserve all-caps for short headings, compact table/section labels, or genuine urgency (e.g. confirming an irreversible delete) — never body text. Context: dense operational UIs use small all-caps column/section labels legitimately; long marketing or reading surfaces should avoid all-caps beyond a short eyebrow. Trust default letter-spacing except: tighten it for a wide-spacing face used as a headline; loosen it for all-caps (default spacing reads cramped without mixed-case cues).
⟨di4-048, psy1-018, rui1-052⟩

### Constrain line/paragraph length
~45-75 characters per line (20-35em); wider should be deliberate, not default. When paragraph text shares an area with wider elements (images), keep the column narrower rather than stretching to match. Never force-justify without hyphenation.
⚖ Tension: line length → tradeoffs-decision-points.md (typo-d01)
⟨di4-048, rui1-045⟩

### Vertical rhythm: baseline and line-height
Align mixed-size text on one line by shared baseline, not vertical center. Scale line-height to context: increase with line length (~1.5 narrow, up to ~2 wide), decrease with font size (headline text can approach 1).
⟨rui1-046, rui1-047⟩

### Text alignment conventions
Left-align by default; center only headlines or blocks under ~2-3 lines. Right-align numeric table columns so digits line up for comparison. Justified text always needs hyphenation.
⟨rui1-049, rui1-050, rui1-051⟩

### Scale link emphasis to pervasiveness
An isolated link in prose should stand out (distinct color). Where links are pervasive, use subtler emphasis (weight, darker color) instead; defer to hover-only for truly ancillary links.
⟨rui1-048⟩

### Content design fundamentals
Always give content a clear heading — readers interpret new info by fitting it into a supplied frame. Keep general-audience copy near a 6th-grade reading level. Write active, not passive, voice. Write from the user's point of view, not the system's ("Edit customer details," not "Edit customer").
- Ask: "Is this sentence active voice, and clear who's doing the action?"
⟨psy1-019, psy1-020, uxp1-011, uxp1-012⟩

### Quick reference
- Design multi-language layouts for translations up to ~3x longer than source (e.g. Italian) and for differing reading direction (LTR/RTL/vertical); test against longer strings, not just the source language. ⟨laws1-037⟩

## Color Systems — HSL, Palettes & Shades

### Restrained palettes: few hues, many values
Build from 1-3 hues (gray counts as one); vary value/saturation within them rather than spreading hues. Pair 1-2 saturated accents against several muted hues — saturated reads closer, muted farther, creating layering.
- Do: lean gray slightly blue (cool) or beige (warm) for temperature.
⟨di4-047, di4-059⟩

### HSL model; greys/primary/accent structure
Use HSL, not hex/RGB — its axes map to perception, enabling deliberate adjustment. Structure the palette into greys (8-10 shades, most of the UI), primary color(s) (5-10 shades each), and accent/semantic colors (multiple shades each, used sparingly).
- Avoid: a small auto-generated 5-color palette as a complete system.
⟨rui1-053, rui1-054⟩

### Predefine each color's shade scale
Don't generate shades on the fly (lighten()/darken()) — predefine a fixed scale. Anchor the base shade by eye (button-background test), the darkest to real use (text), the lightest to real use (tinted background); bisect remaining gaps to ~9 steps. Hand-tune after, but avoid habitual one-off shades.
- Trade-off: strict systematic adherence vs the flexibility to hand-tune when something looks off.
⟨rui1-055, rui1-056, rui1-057⟩

### Preserve intensity in light/dark shades; grey temperature
Saturation's impact weakens near 0%/100% lightness — raise it as lightness moves from 50%, or shades look washed out. Bright hues (yellow, cyan, magenta) read brighter than dark ones at equal L/S — lighten/darken by rotating hue toward a bright/dark anchor instead of only shifting lightness.
- Exception: keep rotation ≤ ~20-30° or it reads as a different color.
⟨rui1-058, rui1-059, rui1-060⟩

### Accessible color on colored backgrounds
If accessible contrast forces an unintentionally dominant dark/saturated background, flip it: dark text on a light tint instead. For secondary text on a dark colored panel, don't lighten the panel's own hue toward white (makes primary/secondary text too similar) — rotate toward a brighter hue instead.
⟨rui1-061, rui1-062⟩

## Color Meaning, Contrast & Accessibility

### Never convey meaning through color/motion alone
Pair color-coded meaning (status, alerts, links, chart series) with a redundant channel — shape, icon, border, pattern, or text. For comparative data, prefer contrast/lightness over hue (colorblind users read light-dark better than hue-hue). Same for motion used as the sole channel for critical info — can trigger vestibular/epilepsy symptoms.
- Ask: "If color were removed entirely, would this still communicate the same meaning?"
⟨laws1-055, psy1-016, uxp1-086, rui1-064, laws1-057⟩

### WCAG minimum text contrast
≥4.5:1 normal text (3:1 for large 18pt+/bold 14pt+), targeting ~7.5:1 where practical. Solve this with technique (contrast flipping, hue rotation), not by accepting harsh color — reject branding requests that drop functional text below the floor.
- Exception: large/bold text gets the reduced threshold; logos are exempt from the strict minimum.
⟨laws1-056, uxp1-007, rui1-063⟩

### Guarantee readability before stylistic color choices
Pair dark foreground with light background (or vice versa); confirm by desaturating to grayscale. Avoid red directly adjacent to blue or green as text/background — causes chromostereopsis (perceived-depth "vibration," eye fatigue), unrelated to colorblindness.
⟨di4-045, psy1-015⟩

### Verify cultural color meanings against the target audience
Before assigning semantic meaning to a color, check what it means to the real target audience — don't assume your own culture's associations transfer (white/red mean opposite things, purity vs mourning, across cultures). Same for a cultural/stylistic reference: verify the audience actually recognizes it.
⟨psy1-017, di4-054⟩

### Quick reference
- Warm hues read energetic/hot, cool read calm/conservative (blue for credibility); light backgrounds read conventional, dark reads sharper; strong contrast reads tense/bold, weak reads calm; saturation reads energetic but fatigues if overused — reserve for 1-2 small accents against a muted base. ⟨di4-046⟩

## Depth, Elevation & Borders

### Simulate a consistent overhead light source
Determine edge profile, then apply light/dark consistent with an overhead source. Raised element: lighten only the top edge (hand-picked color, not translucent white) plus a small sharp dark shadow beneath (real ambient occlusion is compact, not soft). Inset element: light the bottom lip, dark inset shadow at top. Stop tuning once the read registers — over-tuning reads busier, not more polished.
⟨rui1-065, rui1-066, rui1-067, rui1-068⟩

### Shadow/elevation system
Decide z-axis prominence first, then pick a shadow sized to communicate it — not by isolated tweaking: small/tight for buttons, medium for dropdowns, large/soft for modals. Define a fixed ~5-step elevation scale. Change shadow dynamically on interaction (grow on drag, shrink on press). Layer a larger/softer cast shadow with a smaller/tighter contact shadow, fading the contact layer as elevation increases.
⟨rui1-069, rui1-070, rui1-071, rui1-072, rui1-073⟩

### Depth in flat design without shadows/gradients
Make an element lighter than its background to feel raised, darker to feel inset. Use a short, vertically-offset, zero-blur "solid" shadow for a flat-compatible sense of elevation.
⚖ Tension: decorative depth vs flat → tradeoffs-decision-points.md (typo-d03)
⟨rui1-074⟩

### Angle/curve choices and background texture
Right-angle layouts read calm/stable; varied angles read dynamic; curves add energy (a rule of thumb, not absolute). Texture behind small text must be extremely subtle or absent — it hurts readability and can distort letterforms; fade texture toward flat color near text.
- Avoid: loud checkerboard textures behind text; patterns that cause letterform misreads at small sizes.
⟨di4-051, di4-052⟩

### Prefer shadow/background-contrast/spacing over a border
Before adding a border to separate elements, try a subtle box shadow, differing adjacent background colors (remove the border if now redundant), or added spacing.
- Trade-off: a border is explicit/unambiguous vs subtler, less cluttered methods.
⟨rui1-093⟩

### Quick reference
- Two shadow-free depth patterns: Deep Background (soft-focus gradient behind content, smooth edges) and Overlap (let an element cross a background transition or extend past its parent, bordered in the background color to avoid seam clash) — test busy background candidates for foreground legibility. ⟨di4-058, rui1-075, rui1-076⟩
- Echo a deliberately-chosen display font in a few borders/rule lines (matching color, curve radius, a line weight thinner than its stroke); 1px hairlines near thin sans-serifs give a refined look — gray, dotted, or baseline-flush read lighter or tighter. ⟨di4-061, di4-062⟩

## Imagery & Icons

### Icon set consistency; restrained decorative imagery
Keep all icons in one visual style (color, texture, angle, curve) — draw a missing icon to match rather than mixing styles — while keeping icons individually distinguishable. Reserve emotive decorative imagery for contexts where mood genuinely matters; in utilitarian apps it reads as marketing excess.
- Ask: "Does this icon match the style of the rest of the set?"
⟨di4-053, uxp1-013⟩

### Photography quality and text-over-photo legibility
Commission a professional or source high-quality stock — never design against placeholders planning to swap real photos later. For text over photos, the problem is uneven light/dark regions: a semi-transparent overlay is simple but global; lowering the image's own contrast gives more local control; colorizing with a brand color aids cohesion; a soft zero-offset text shadow/glow preserves the most of the original look.
- Trade-off: overlay simplicity vs localized control vs brand cohesion vs preserving the original image.
⟨rui1-077, rui1-078, rui1-079, rui1-080, rui1-081, rui1-082⟩

### Respect an asset's intended rendering size
Small icons (16-24px) filling a larger space: keep near native size inside a larger surrounding shape, don't scale up. Detailed screenshots for small spaces: capture at smaller native resolution or crop, don't just shrink. Detailed logos at favicon size: hand-redraw simplified rather than relying on auto-downscale — test at 16x16px on a transparent background.
⟨rui1-083, rui1-084, rui1-085, rui1-086, uxp1-019⟩

### Constrain and contain user-uploaded images
Don't render uploads at raw intrinsic aspect ratio in a layout-sensitive context — center-crop into a fixed-aspect container. When an upload's background color is close to the surrounding UI, use a subtle inset box-shadow or semi-transparent border, not a plain solid border (clashes with arbitrary colors).
⟨rui1-087, rui1-088⟩

### Icon + text relationship
Never bake text into icon artwork — it can't be localized or read by screen readers. Add a persistent text label next to icons (especially in main nav/toolbars) rather than shipping icon-only controls, kept visible on mobile — icon meaning is inconsistent across products, so a label disambiguates it.
- Exception: well-established formatting controls (bold/italic/underline) can skip the label.
⟨uxp1-016, uxp1-017⟩

### Icon selection: respect established metaphors
Don't base icons on devices younger users never encountered (floppy disk, rotary phone). For a new concept, search icon libraries first rather than repurposing an existing meaning. Check whether a widely-used mark (e.g. "@", hamburger) already carries an inconsistent meaning elsewhere before adopting it. Consider standard emoji for simple, universal concepts.
- Exception: not every use case suits emoji.
⟨uxp1-014, uxp1-015, uxp1-020, uxp1-018⟩

### Quick reference
- For calming imagery, prefer pastoral nature scenes (hills, water, trees) — a stable, cross-cultural, attention-restoring preference — but expect a weaker effect from an on-screen image/video than an actual window view or real walk. ⟨psy2-041⟩

## Brand, Personality & Finishing Polish

### Brand personality via coordinated levers
Treat typeface, corner-radius treatment, and copy tone as one deliberate, coordinated personality, decided together — serif=elegant, rounded sans=playful, sharp corners=serious, large radius=playful, casual language=approachable. Apply consistently across color, type, icon, vocabulary. On mobile, carry the same brand color/type in shrunk form — a bare generic mobile page reads unfinished.
- Ask: "Do our color, type, icon, and word choices actually agree about who we are?"
⚖ Tension: serif vs sans → tradeoffs-decision-points.md (typo-d02)
⟨di4-041, di4-044, di4-049, di4-060, rui1-007, rui1-008, rui1-009, rui1-010, psy1-021⟩

### Don't let abstract brand personality override UX
Don't cede usability decisions to branding demands unless the product is a true global mega-brand. For everyone else, the actual UX is the real brand — reject brand-driven demands that conflict with UX principles.
- Avoid: unreadable branded fonts; illegible low-contrast branded colors; bespoke controls purely for differentiation.
⟨uxp1-098⟩

### Lean on familiar branding at high-stakes moments
At error recovery, financial/health decisions, or checkout under stress, lean into familiar established branding rather than novelty — familiarity signals safety under threat-sensitive processing.
⟨psy2-048⟩

### Aesthetic-Usability Effect
Treat visual polish as functional, not decorative — users form an aesthetic/trust judgment almost instantly that persists with use and gates further evaluation. Visual appeal makes users perceive (and even perform) as if the product were more usable, regardless of actual quality. Pursue it via functional minimalism — stripping ornamentation not tied to function — not decorative flourishes.
- Trade-off: perceived usability vs actual usability — a good first impression doesn't mean real problems don't exist.
⟨laws1-046, laws1-047, laws1-049, psy2-016, psy2-042, di4-042, di4-043⟩

### Whitespace vs density as emotional lever
Generous whitespace evokes calm/elegance. Tight layouts can evoke urgency (uncontrolled crowding) or cozy approachability (controlled small margins, trimmed line-height) — density alone doesn't determine the read; how it's handled does.
⚖ Tension: whitespace vs density → tradeoffs-decision-points.md (vh-d02)
⟨di4-050⟩

### Visual unity via a repeated motif; font-pairing discipline
Achieve unity through deliberate repetition of a chosen motif (corner treatment, font pairing, grouping rhythm). Use one body font + one heading font; a secondary font only in narrow contrast zones (sidebars, nav). Apply repeated rhythm only to genuinely parallel content — users infer similar-looking things function similarly.
⟨di4-055⟩

### Low-skill polish techniques
When a design feels plain and the team lacks illustration skill: supercharge defaults (icons instead of bullets, styled quote marks, custom link styling, brand-colored selected states); add a colored accent border to a bland region; decorate backgrounds per section (gradient hues within ~30°, low-contrast pattern, or a placed shape) — keep decoration's contrast low enough not to compete with content.
⟨rui1-089, rui1-090, rui1-091⟩

### Question a component's default shape when it matters
Don't assume a component must look conventional (a dropdown needn't be a plain link list; radio buttons can become selectable cards). Apply deliberately when the component is important/high-visibility.
- Exception: low-stakes components — convention is simpler and lower-risk.
⟨rui1-094⟩

### Predefine constrained systems for recurring properties
For any recurring property (color, size, weight, spacing, shadow, radius, opacity), define a small fixed value set up front rather than hand-picking freely — an unconstrained range is decision paralysis. Compare a candidate only against its immediate neighbors on the scale.
- Ask: "Am I about to hand-pick a value from an unlimited range I'll need to decide again later?"
⟨rui1-011, rui1-012⟩

### Quick reference
- Treat an attractive prototype as a usability-test confound — participants rate and even perform better on more attractive designs despite identical functionality; judge real usability from observed behavior, not self-reported ratings. ⟨laws1-048⟩
- Under a fixed native desktop control set, real levers remain (background treatment, heading color/font, border treatment, per-item icons) — verify custom styling under high-contrast accessibility themes, preserve screen-reader equivalents, and favor calm over intensity for full-screen, long, high-stress sessions. ⟨di4-056, di4-057⟩
- For power-user audiences, exposing skinnable themes satisfies a desire for ownership and can extend reach, but deliberately scope customization and invest in a strong base design first — a bad user-made skin can genuinely degrade usability. ⟨di4-064⟩
