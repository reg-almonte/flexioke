---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: pending
---

# TASK-0025: Stage Toolbar Lyric Resizing (A-/A+) & Configurable Settings Modal

## Parent Story
- `docs/tickets/STORY-0010-stage-header-countdown-controls.md`

## What to build
Add `A-` and `A+` buttons to the Karaoke stage toolbar in `src/templates/index.html` and `src/static/karaoke_stage.js` that adjust `--karaoke-font-size` on the fly. Create a Stage Settings modal offering controls for header transition interval (seconds), active lyric glow color (color picker / hex), and base font size. Save all preferences to `localStorage` and apply immediately to CSS custom properties.

## Acceptance Criteria
- [ ] `A-` / `A+` buttons dynamically increment/decrement lyric line font size.
- [ ] Stage Settings modal allows customizing transition interval (3-30s), active lyric glow color, and base font size.
- [ ] Selected settings persist in `localStorage` across page reloads.
- [ ] Active lyric highlights dynamically adopt the configured color without CSS glitches.

## Blocked by
- None (can start immediately)
