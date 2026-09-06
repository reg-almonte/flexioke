---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: completed
---

# TASK-0068: UI Iconography Overhaul & Hotkey Tooltips

## Parent Story
- `docs/tickets/STORY-0032-modular-svg-icon-dictionary.md`

## What to build
Integrate the SVG icon system across the UI:
- Replace static emoji and Unicode symbols in `src/static/index.html` across transport buttons, stage buttons, volume toggles, collapse chevrons, and Stem Studio channel headers.
- Update dynamic JavaScript renderers in `src/static/player.js`, `src/static/karaoke.js`, `src/static/library_queue.js`, and `src/static/playlists.js` to use `window.getIconHtml()`.
- Add rich tooltips with hotkey prompts (e.g. `Play / Pause (Space)`, `Restart (R)`, `Next (N)`, `Fullscreen (F)`).

## Acceptance Criteria
- [x] All interactive buttons utilize consistent SVG icons.
- [x] Tooltips include accurate hotkey cues.
- [x] Hover and active states remain smooth and visually responsive.

## Blocked by
- `docs/tickets/TASK-0067-svg-icon-dictionary-module.md`
