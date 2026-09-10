---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: pending
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
- [ ] Adjusting geometry sliders in settings updates the fullscreen lyrics stage instantly.
- [ ] Windowed mode retains standard fixed responsive classes and does not stretch or shift.
- [ ] Settings persist across browser refreshes and restore accurately.
- [ ] Automated CSS and Node.js regression tests pass cleanly.

## Blocked by
- None (can start immediately in parallel).
