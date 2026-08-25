# Pattern Catalog — Overlays / Feedback

Split from patterns.md (V2) for targeted retrieval; provenance tags unchanged. Selection
frameworks (where they exist) open each family before its catalog entries. The catalog-wide
meta-principle lives in patterns.md.

## Overlays

### Modal Panel `PTN-010`
Display a single focused panel and withhold other navigation until the user resolves the
immediate task; reserve for cases the app genuinely cannot proceed without (filename, login,
critical acknowledgment) — route low-importance input to an inline, non-blocking control
instead. On close, return the user to exactly the page/state they were on before, and on the
web prefer a lightweight custom overlay over an OS-level modal dialog. Exception:
sign-in/registration screens are sometimes presented as a whole stripped-down "modal" page
rather than a small overlay. Trade-off: a blocking modal guarantees input is captured
immediately; an inline non-blocking control risks the input being forgotten. Ask: does the app
genuinely need to block everything until this is resolved, or could the request be
deferred/hung inline instead? (DI ch3; IC ch12)

### Confirmation Dialog `PTN-112`
Gate an action behind a confirmation dialog only where its consequence is not easily reversible
or is high-stakes; where a mistake is cheap and quickly recoverable, skip confirmation and let
users learn by trial and error. Trade-off: confirmation adds friction to every legitimate use
in exchange for safety on the rare mistaken case. Ask: how costly is it, in time or
consequence, for a user to recover from performing this action by mistake? (IC ch3)

### True ARIA Menu Button Contract `PTN-115`
Pair a trigger button carrying a static `aria-haspopup="true"` (a fixed capability warning,
never toggled) with a dynamically toggled `aria-expanded="true"/"false"` reporting the menu's
actual open/closed state, plus a menu container with menu/menuitem roles; hide a decorative
disclosure-triangle glyph from assistive technology since `aria-haspopup` already communicates
a popup exists. (IC ch4; DI ch8; DI ch6)

### Toggletip `PTN-116`
A click-triggered info bubble whose content is announced only after activation, via an
initially-empty live region populated on click; the trigger is not a real toggle button —
clicking again does not hide it, and the live region is cleared and repopulated after a short
delay to force re-announcement, since a "toggled-on" state makes little sense once content has
already been read. (IC ch5)
## Feedback

### Live Region `PTN-117`
A container that announces added/changed content via screen reader without requiring
interaction or a focus move — pair `role="status"` with `aria-live="polite"` on the container
for widest compatibility; use it to deliver any state-change/FYI message that should be
announced but not focused. (IC ch10)

### Flash Messages `PTN-118`
Colored text strips above a page's primary action area, purely informational/non-actionable,
are adequately served by a single shared live region — they don't need the
dialog-with-focus-moved treatment reserved for actionable messages. (IC ch10)

### Prefer Automatic, Timed Disappearance `PTN-119`
Let a transient notification disappear by itself after a suitable elapsed duration rather than
requiring active dismissal, removing both the interaction burden and the focus-management
complexity a dismiss control introduces. (IC ch10)
