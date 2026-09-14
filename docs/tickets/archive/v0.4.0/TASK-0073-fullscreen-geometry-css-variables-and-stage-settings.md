---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: completed
---

# TASK-0073: Fullscreen Geometry CSS Variables & Stage Settings Sliders

## Parent Story
- `docs/tickets/STORY-0035-fullscreen-stage-geometry-customization.md`

## What to build
Build the CSS variables, settings controls, and persistence for fullscreen stage geometry:
- Define CSS custom properties: `--karaoke-fullscreen-stage-width` (default `98%`), `--karaoke-fullscreen-stage-max-height` (default `56vh`), and `--karaoke-fullscreen-stage-v-offset` (default `0%`).
- Update `src/static/styles.css` with scoped fullscreen selectors using `calc(50% + var(--karaoke-fullscreen-stage-v-offset))`.
- Add interactive range sliders and live number readouts in `#karaoke-settings-modal`.
- Bind real-time input events in `KaraokeStageManager` to update CSS variables immediately and persist in `localStorage`.
- Reset button restores default dimensions cleanly.

## Acceptance Criteria
- [x] Adjusting geometry sliders in settings updates the fullscreen lyrics stage instantly.
- [x] Windowed mode retains standard fixed responsive classes and does not stretch or shift.
- [x] Settings persist across browser refreshes and restore accurately.
- [x] Automated CSS and Node.js regression tests pass cleanly.

## Blocked by
- None (can start immediately in parallel).

## Implementation
- **Branch:** `story/STORY-0035-fullscreen-stage-geometry-customization`
- **Files Modified/Created:**
  - `src/static/styles.css`: Defined `:root` CSS variables for stage geometry and updated `.stage-fullscreen #karaoke-lyrics-stage` rules.
  - `src/static/index.html`: Added stage geometry sliders (width, height, v-offset) in `#karaoke-settings-modal` with scrolling support.
  - `src/static/karaoke.js`: Added geometry properties to `defaultConfig`, live input bindings, and CSS variable updates in `applySettings()`.
  - `tests/test_stage_geometry.py`: Added 4 automated unit and Node.js simulation tests for geometry scaling, persistence, and scoping.

