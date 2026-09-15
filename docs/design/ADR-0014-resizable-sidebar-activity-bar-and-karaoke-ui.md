---
status: approved
approved_by: user
approved_at: 2026-09-16
---

# ADR-0014: PointerEvent Splitter Controller, Activity Bar Tab Manager & Responsive Cinema Stage Architecture

## Context
In previous versions (v0.2.2 through v0.4.1), Karaoke Mode organized sidebar controls into vertically stacked accordion cards (Playback Queue, Playlists, Song Library) with fixed layout geometry. As features expanded (video backgrounds, Side A/B dual tracks, in-modal song navigation), user feedback identified several architectural limitations:
1. **Vertical Space Competition:** Stacked accordions forced constant vertical scrolling and card collapsing when managing playlists and queues concurrently.
2. **Fixed Split Geometry:** Desktop and laptop users could not resize the partition between sidebar curation tools and the central lyrics stage.
3. **Transport Bar Adaptability:** The bottom transport bar and vocal buttons lacked responsive container-aware breakpoints when stage width was constrained.
4. **Fullscreen Cinema Readability:** Floating transport buttons and icons remained compact in fullscreen cinema mode, reducing visibility and click targets from a 10-foot party distance.
5. **Keyboard Spacebar Disruption:** Spacebar play/pause handling lacked centralized focus guarding against text inputs.

## Decision
Adopt **Option 1: Native PointerEvent Splitter Controller + ResizeObserver Adaptive Transport Bar + Fullscreen Cinema CSS Scaling**:
1. **VS Code-Style 48px Activity Bar & Tabbed View Controller:**
   - Dedicated left Activity Bar (`#karaoke-activity-bar`) with 3 distinct icon tabs (`#tab-karaoke-queue`, `#tab-karaoke-playlists`, `#tab-karaoke-library`) featuring real-time dynamic count badges (`#badge-karaoke-queue`, `#badge-karaoke-playlists`, `#badge-karaoke-library`).
   - `#karaoke-sidebar-content` renders 100% full-height views for the selected tab.
   - Clicking the active tab or pressing `Ctrl+B` / `Cmd+B` / `Alt+S` collapses the side panel to `width: 0px` (or `display: none`), preserving the 48px Activity Bar.
2. **PointerEvent Splitter Controller:**
   - `#karaoke-splitter-handle` implements horizontal dragging via native `PointerEvent` API (`setPointerCapture`, `pointermove`, `pointerup`), clamped between 48px and 50% viewport width.
   - Double-clicking the splitter handle instantly resets to default `320px` width.
   - Sidebar geometry, active tab, and collapsed state persist synchronously in `localStorage` (`flexioke_karaoke_sidebar_state`).
3. **Container-Aware Responsive Stage & Transport Bar:**
   - Use `ResizeObserver` on `#karaoke-stage-container` to dynamically apply responsive classes (`stage-narrow`, `stage-compact`, `stage-full`) to the transport bar and recalculate dual header marquee bounding boxes.
   - Prioritize essential transport controls (Play/Pause, Restart, Volume hover slider, Lead Vocal toggle), gracefully collapsing vocal button text to compact icon chips on constrained widths (< 540px) and compacting secondary icons on narrow screens (< 480px).
4. **Scaled-Up Fullscreen Cinema Chrome:**
   - In Cinema Fullscreen mode (`.stage-fullscreen`), floating transport bar `#karaoke-cinema-transport` widens to **85% stage width** (up to 1200px).
   - SVG icons scale from 18px to **26px** (`w-6.5 h-6.5`), timecode badge enlarges to `text-base font-bold`, and vocal toggle buttons receive elevated touch/click padding.
5. **Universal Focus-Guarded Spacebar Play/Pause Shortcut:**
   - Global `keydown` handler intercepts `Space` key, checks `document.activeElement` against `INPUT`, `TEXTAREA`, `SELECT`, and `isContentEditable` fields, and safely executes `togglePlay()` while calling `event.preventDefault()` to eliminate browser page scroll jumps.

## Options Considered

### Option 1: Native PointerEvent Splitter Controller + ResizeObserver Adaptive Transport Bar + Fullscreen Cinema CSS Scaling (Selected)
- **Pros:**
  - Zero external dependencies (vanilla JavaScript DOM, PointerEvents, and CSS flexbox).
  - Buttery smooth 60fps dragging with native pointer capture.
  - Container-aware responsiveness accurately reacts to actual stage width rather than global window dimensions.
  - Synchronous `localStorage` hydration prevents flash-of-unstyled-content (FOUC).
  - Robust text-input focus guarding for Spacebar shortcuts.
- **Cons:**
  - Requires explicit pointer boundary clamping math and ResizeObserver debouncing.

### Option 2: CSS Grid Layout with Viewport Media Queries & Floating Toolbars (Rejected)
- **Pros:**
  - Pure CSS layout.
- **Cons:**
  - Viewport media queries (`@media`) fail to react when the user drags the sidebar wider on a fixed desktop monitor, breaking responsive transport button wrapping.
  - Less flexible for dynamic tab collapse and activity bar animations.

## Consequences

### Positive
- Delivers a clean, professional, VS Code-style experience for karaoke session management.
- Maximizes screen real estate for lyrics rendering when side panel is collapsed.
- Vastly enhances party/TV visibility in Fullscreen Cinema mode with 26px icons and wide transport chrome.
- Eliminates page scroll jump annoyances via universal Spacebar play/pause shortcut.
- Preserves 100% backward compatibility with existing Stage Settings, geometry custom properties, and Side A/B dual tracks.

### Negative / Trade-offs
- Adds a small client-side state schema in `localStorage` (`flexioke_karaoke_sidebar_state`) which must be cleanly hydrated and validated on startup.

## Related
- Functional spec: `docs/specs/version0.4.2.md`
- Requirement: `docs/requirements/version0.4.2.md`
- Related ADRs: `docs/design/ADR-0005-karaoke-stage-transport-queue-reordering.md`, `docs/design/ADR-0006-karaoke-stage-ux-and-catalog-modal.md`, `docs/design/ADR-0009-lyrics-calibration-and-karaoke-ux.md`, `docs/design/ADR-0011-ui-and-stage-experience-enhancements.md`, `docs/design/ADR-0012-video-backgrounds-stage-geometry-and-side-ab.md`
