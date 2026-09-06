---
status: fixed
filed_at: 2026-09-06
verified_at: 2026-09-06
---

# Bug Report: Native Fullscreen Display & Controller Auto-Hide in Cinema Stage

## Related
- Functional Spec: `docs/specs/version0.3.1.md` (§3 YouTube-Style Fullscreen Cinema Stage)
- Design: `docs/design/ADR-0011-ui-and-stage-experience-enhancements.md` (§3 Floating Chrome & Fullscreen)
- Story: `docs/tickets/archive/v0.3.1/STORY-0033-youtube-style-fullscreen-karaoke-stage.md`
- Tasks: `docs/tickets/archive/v0.3.1/TASK-0069-cinema-fullscreen-floating-chrome.md`, `docs/tickets/archive/v0.3.1/TASK-0070-inactivity-autohide-and-stage-shortcuts.md`

## Summary
1. **Viewport-only Fullscreen vs. Native OS/Browser Fullscreen:** Clicking Expand / Fullscreen mode (`F`) only applies CSS viewport styles (`width: 100vw; height: 100vh; position: fixed`), which expands inside the browser content area but leaves the browser frame (tabs, address bar, bookmarks, and OS window decorations) visible. Users expect full display takeover without browser frames, identical to standard video players (HTML5 Fullscreen API).
2. **Controller Auto-Hide Inactivity Timer Reset:** During active playback in fullscreen mode, floating top header and bottom transport controllers do not auto-hide after 3 seconds of inactivity as intended.

## Failures & Root Cause Analysis

### Failure 1: Missing HTML5 Fullscreen API Integration
- **Root Cause:** In `src/static/karaoke.js`, `enterFullscreen()` and `exitFullscreen()` strictly toggle CSS classes (`stage-fullscreen`, `karaoke-cinema-fullscreen`). They do not invoke the HTML5 Fullscreen API (`element.requestFullscreen()` / `document.exitFullscreen()`). As a result, the stage only expands within the webpage frame rather than taking over the entire physical screen.
- **Proposed Fix:**
  1. Add native fullscreen helpers `enterNativeFullscreen()` and `exitNativeFullscreen()` supporting standard `requestFullscreen()` and vendor prefixes (`webkitRequestFullscreen`, `msRequestFullscreen`).
  2. In `enterFullscreen()`, request native fullscreen on `#karaoke-stage-card`.
  3. In `exitFullscreen()`, exit native fullscreen if `document.fullscreenElement` is active.
  4. Attach `fullscreenchange` and `webkitfullscreenchange` event listeners to synchronize fullscreen UI state when the user enters or exits via browser shortcuts (such as browser `Esc` key).
  5. Provide seamless fallback to CSS fullscreen if native fullscreen permissions are restricted by the browser/environment.

### Failure 2: Inactivity Auto-Hide Timer Reset Loop
- **Root Cause:** In `src/static/karaoke.js`, `setInterval(() => this.onTimeCheck(), 100)` executes every 100ms. Inside `onTimeCheck()`, `this.updatePlayBtnUI()` is called on every tick, which directly invokes `this.handlePlaybackStateChange()`. `handlePlaybackStateChange()` calls `this.scheduleInactivityTimer()`, which immediately executes `this.clearInactivityTimer()` and creates a new 3000ms timer. Because this occurs every 100ms, the inactivity timer is continuously wiped out and reset 10 times per second, preventing `hideChrome()` from ever executing during playback.
- **Proposed Fix:**
  1. Cache `this._lastPlaybackState` in `KaraokeStageManager`.
  2. In `handlePlaybackStateChange()`, return immediately if `this._lastPlaybackState === this.isPlaying`, ensuring that `scheduleInactivityTimer()` is only called when playback state genuinely transitions (e.g., paused -> playing).
  3. Ensure user input listeners (`mousemove`, `pointermove`, `keydown`, `touchstart`, `wheel`) properly wake chrome and schedule the 3s auto-hide timer during active playback.
  4. Optimize `wakeChrome()` to guard against redundant DOM class manipulations when chrome is already visible.

## Applied Fixes (Pending Phase 6 Verification)
1. **HTML5 Native Fullscreen API Integration:**
   - Implemented `enterNativeFullscreen()` and `exitNativeFullscreen()` in `src/static/karaoke.js` supporting standard `requestFullscreen()` and vendor prefixes.
   - Added two-way event synchronization on `document` via `fullscreenchange`, `webkitfullscreenchange`, `mozfullscreenchange`, and `MSFullscreenChange`.
   - Updated `styles.css` with `:fullscreen` and `:-webkit-full-screen` selectors.
2. **Inactivity Timer Debouncing & Auto-Hide:**
   - Cached `this._lastPlaybackState` in `KaraokeStageManager`.
   - Guarded `handlePlaybackStateChange()` to only schedule/cancel inactivity timer on genuine playback transitions, preventing 100ms interval loops from resetting the timer.
   - Verified with unit and Node.js tests in `tests/test_karaoke_cinema_fullscreen.py`.
