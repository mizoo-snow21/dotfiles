# Pattern Catalog — Mobile & Touch

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

## Mobile & Touch

### Vertical Stack `PTN-100`
Lay out a mobile page as a single column that reflows regardless of actual screen width; when
moving between pages carries a real cost (a downloaded web page), prefer one long scrollable
page over discrete per-page splits — for content already local (installed app), discrete
one-screen-at-a-time pages can be reasonable instead. When: avoid for immersive full-screen
experiences (video, games) that don't scroll like text. Trade-off: one long page avoids
repeated load-wait cost but requires more scrolling; discrete pages reduce scrolling but each
transition may cost a wait unless content is local. (DI ch10)

### Filmstrip `PTN-101`
Lay a small number of conceptually parallel top-level pages side by side, moved between with a
horizontal swipe, as an alternative to tabs/menu/nav page; unlike Carousel it typically omits
neighbor metadata — show a dot-style page indicator to signal multiple pages exist. When:
avoid when the number of pages is large, or discoverability matters with no plan to teach the
gesture. Trade-off: gives content the full screen with no nav chrome but doesn't scale to many
pages and isn't self-evident to new users. (DI ch10)

### Touch Tools `PTN-102`
Keep controls hidden by default over full-screen immersive content (video, photo, map),
surfacing them as an overlay only on tap and auto-hiding after inactivity or a tap elsewhere —
the touch-primary counterpart to Hover Tools, which relies on a mouse-hover state Touch Tools
cannot use. Do: show a one-time onboarding dialog to new users, since the tap-to-reveal gesture
isn't otherwise discoverable. (DI ch10; DI ch6)

### Bottom Navigation `PTN-103`
Place global/site navigation as a vertically stacked list of large, tappable items at the very
bottom of a scrollable mobile page, reserving the highest-value top screen real estate for
actual content — the mobile-scroll counterpart to the desktop Sitemap Footer. (DI ch10)

### Thumbnail-and-Text List `PTN-104`
Pair a small thumbnail with text in each list row, optionally adding vivid color/icon/badge
markers; small mobile screens tolerate more saturated color than desktop without feeling
aggressive, so this pattern can lean on stronger color than an equivalent desktop list. (DI ch10)

### Infinite List `PTN-105`
Load only an appropriately-sized initial chunk of a very long list, adding more on demand via
"Load More" or auto lazy-load as the user scrolls to the end, rather than paginating to a
separate page or downloading everything up front. (DI ch10)

### Touch Target Hit Area Beyond Visible Boundary `PTN-106`
A tappable control's effective touch-sensitive hit area doesn't have to match its rendered
visual size — extend it invisibly into surrounding margin/whitespace so it's easy to hit with a
finger while the visual footprint stays as small as the design calls for. Do: target roughly
1cm square (or a platform minimum, e.g. 44x44px) for the effective, not necessarily visible,
hit area. (DI ch10)

### Text Clear Button `PTN-107`
Place a small "×"/Clear control inside a text field (typically trailing edge) that empties its
entire contents in one tap; use the platform's own default clear-button convention when one
exists, and usability-test any custom one, since users may misread it as Go/Search. (DI ch10)

### Loading Indicators `PTN-108`
Show progress feedback exactly at the location the awaited content will render (or the spot the
user tapped), rather than as a generic global indicator elsewhere; render already-available
parts immediately, reserving the indicator only for parts still pending — the mobile analog of
the desktop Progress Indicator, scoped tightly to its object. (DI ch10; DI ch6)

### Hamburger Navigation Menu Button `PTN-113`
A button toggling a collapsed/off-canvas navigation list on small screens must be a real
`<button>` (not a link or generic clickable div) and communicate its expanded/collapsed state
via `aria-expanded`. (IC ch4)

### Native `<select>` as a Condensed Navigation Menu `PTN-114`
A native `<select>` used to condense navigation options for narrow viewports is a legitimate
menu whose semantics closely parallel a true button-triggered menu, and should be preferred
over a custom scripted dropdown when its semantics genuinely match the navigation-condensing
need — distinct from repurposing a select to invoke actions (see Action: Don't Repurpose a
Dropdown-Select for Actions), since here it's choosing a destination, a value-selection role it
already fits. (IC ch4)
