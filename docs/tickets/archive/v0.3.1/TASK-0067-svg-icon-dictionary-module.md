---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: completed
---

# TASK-0067: SVG Icon Dictionary Module & Renderer Utility

## Parent Story
- `docs/tickets/STORY-0032-modular-svg-icon-dictionary.md`

## What to build
Implement the core SVG icon dictionary module:
- Create standalone `src/static/icons.js` loaded across the application.
- Define `window.flexiokeIcons` dictionary mapping icon names to clean inline SVGs (`viewBox="0 0 24 24"`, `currentColor`).
- Implement helper `window.getIconHtml(name, extraClasses, extraAttrs)` to generate standard icon markup.
- Include all required symbols: `play`, `pause`, `restart`, `next`, `stop`, `volume_high`, `volume_low`, `volume_muted`, `settings`, `fullscreen_enter`, `fullscreen_exit`, `chevron_down`, `chevron_right`, `chevron_left`, `instrumental`, `lead_vocals`, `backing_vocals`, `zip_export`, `heart_filled`, `heart_outline`, `search`, `edit`, `delete`, `notes`.

## Acceptance Criteria
- [x] Module initializes on page load and exposes `window.flexiokeIcons` and `window.getIconHtml`.
- [x] Unknown icon names degrade gracefully to empty string without throwing errors.
- [x] Icons render correctly with customizable classes and sizing.

## Blocked by
- None (can start immediately)
