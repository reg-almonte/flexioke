---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# ADR-0011: In-Modal Song Navigation, Modular SVG Iconography & In-Place Cinema Fullscreen

## Context
Following the delivery of Version 0.3.0 (Playlists Management & Favorites System), three key user experience challenges were identified:
1. **Modal Song Navigation Friction:** When inspecting or editing metadata, synchronized lyrics, and playlist assignments in `#lyrics-modal`, users were forced to close the modal and reopen it for each song in their library, slowing down batch curation workflows.
2. **Iconography Quality & Maintainability:** Disparate emojis and Unicode character symbols were used for buttons (Play, Pause, Restart, Stop, Next, Volume, Settings, Fullscreen, Collapse). These varied in visual weight across operating systems, lacked high-DPI crispness, and were difficult to substitute centrally.
3. **Static Full-Screen Presentation:** Live karaoke requires an edge-to-edge cinema experience where lyric visibility is maximized. The existing fullscreen view displayed persistent static cards that distracted from the performance.

## Decision
We choose **Option 1: Unified Client State Coordinator with Centralized SVG Dictionary & Reactive In-Place Cinema Fullscreen**.

### Architecture & Implementation Details:
1. **In-Modal Song Navigator (`src/static/library_queue.js`):**
   - `SongLibraryManager` maintains an active navigation context `{ items: Array, activeIndex: number, isDirty: boolean, baseline: Object }`.
   - Context is populated based on the calling view (active filtered library, sorted catalog modal, or open playlist).
   - Real-time `input` listeners track dirty state across Title, Artist, and Lyrics inputs.
   - Confirmation prompt intercepts `◀ Prev`, `▶ Next`, `✕ Close`, and `Esc` when `isDirty === true` to prevent accidental loss of edits.
   - Dynamic track position badge (`Track X of Y`) and button disabled states (`activeIndex === 0`, `activeIndex === items.length - 1`).
   - Keyboard shortcuts (`Alt + Left Arrow`, `Alt + Right Arrow`).

2. **Centralized Modular SVG Icon Dictionary (`src/static/icons.js`):**
   - Standalone module `src/static/icons.js` defining `window.flexiokeIcons` dictionary mapping semantic keys to clean inline SVG templates (`viewBox="0 0 24 24"`, `currentColor`).
   - Utility function `window.getIconHtml(name, extraClasses, extraAttrs)` provides unified markup rendering across static and dynamic templates.
   - Comprehensive icon coverage: `play`, `pause`, `restart`, `next`, `stop`, `volume_high`, `volume_low`, `volume_muted`, `settings`, `fullscreen_enter`, `fullscreen_exit`, `chevron_down`, `chevron_right`, `chevron_left`, `instrumental`, `lead_vocals`, `backing_vocals`, `zip_export`, `heart_filled`, `heart_outline`, `search`, `edit`, `delete`, `notes`.
   - Accessible hotkey cues integrated into tooltips (`Play / Pause (Space)`, `Restart (R)`, `Next (N)`, `Fullscreen (F)`).
   - Isolated architecture allows developers and users to easily customize or replace icons in one central file without altering component DOM templates.

3. **In-Place Cinema Fullscreen Stage & Inactivity Auto-Hide Engine (`src/static/karaoke.js`):**
   - Reuses the existing `#karaoke-stage-card` DOM tree, applying `.karaoke-cinema-fullscreen` to expand edge-to-edge (`100vw × 100vh`) with a cinema backdrop.
   - Renders Top Header (*Now Singing* marquee + *Up Next* + Exit Fullscreen) and Bottom Transport Bar as floating glassmorphism overlays (`backdrop-blur-md bg-surface-950/80 border border-slate-800/80 rounded-2xl shadow-2xl`).
   - Inactivity Auto-Hide Controller in `KaraokeStageManager`:
     - 3-second inactivity timer (`3000ms`).
     - When `is_playing === true` in fullscreen, 3s of idle mouse/keyboard input adds `.karaoke-chrome-hidden` (`opacity: 0; pointer-events: none; transition: opacity 0.4s ease`) and `.karaoke-cursor-hidden` (`cursor: none`).
     - Activity (`mousemove`, `touchstart`, `keydown`) instantly restores visibility (`opacity: 1`, `cursor: default`) and resets the timer.
     - Controls remain permanently visible when playback is paused or stopped.
   - Interactive stage shortcuts: Double-click stage canvas or press `F` to toggle fullscreen; single click on stage wakes floating chrome.

## Options Considered

### Option 1: Unified Client State Coordinator with Centralized SVG Dictionary & Reactive In-Place Cinema Fullscreen (Chosen)
- **Pros:**
  - Zero DOM duplication: maintains single audio player instance, synchronized lyric smooth auto-scroller, and Web Audio channel volume bindings.
  - Pure SVG vector rendering ensures razor-sharp clarity across retina / 4K displays with zero external CDN dependencies.
  - Centralized icon dictionary makes theme styling and icon customization trivial.
  - Highly performant and responsive: smooth CSS transitions and debounced event listeners.
- **Cons:**
  - Requires precise CSS absolute positioning and z-index coordinate management during fullscreen transitions.

### Option 2: Isolated Secondary Fullscreen Modal & External Icon Font/Sprite Sheet
- **Pros:**
  - Standard stage DOM markup remains completely separated from fullscreen DOM markup.
- **Cons:**
  - Duplicates audio transport bindings, volume controls, and lyric scrolling engines across two distinct DOM trees.
  - Substantial risk of audio state desynchronization and memory leaks.
  - External icon font dependencies reduce offline reliability.

## Consequences
- **Positive:**
  - Library curators can rapidly review and edit entire song libraries without modal friction.
  - Visual polish is significantly elevated with uniform, modern SVG icons and rich hotkey tooltips.
  - Live karaoke singers enjoy a true cinema-grade distraction-free full-screen stage with auto-hiding controls.
- **Neutral:**
  - Pure client-side enhancement: zero breaking changes or migrations to backend APIs or storage schemas.

## Related
- Functional spec: `docs/specs/version0.3.1.md`
- Requirement: `docs/requirements/version0.3.1.md`
- Supersedes / related ADRs: Extends `docs/design/ADR-0006-karaoke-stage-ux-and-catalog-modal.md` and `docs/design/ADR-0009-lyrics-calibration-and-karaoke-ux.md`.
