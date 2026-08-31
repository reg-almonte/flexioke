---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0036: Dual Stage Highlight Color Pickers (Border Glow & Background Fill Tint)

## Parent Story
- `docs/tickets/STORY-0015-restart-lyrics-reset-and-dual-colors.md`

## What to build
Split the Stage Settings color customization into two independent controls: "Highlight Glow & Border Color" (`--karaoke-highlight-color`) and "Highlight Fill & Background Color" (`--karaoke-highlight-fill`). Update active lyric styling to apply both custom properties dynamically with real-time preview and localStorage persistence.

## Acceptance Criteria
- [x] Stage Settings includes two color pickers with hex code displays.
- [x] Active lyric lines use `--karaoke-highlight-color` for borders/glow and `--karaoke-highlight-fill` for background tint.
- [x] Changes apply immediately to rendered lyrics in real time and persist across sessions.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0015-restart-lyrics-reset-and-dual-colors`
- Split Stage Settings color controls into `#settings-highlight-glow-color` and `#settings-highlight-fill-color` with live hex readouts.
- Bound `--karaoke-highlight-color` and `--karaoke-highlight-fill` dynamically in `applySettings()` and `highlightLine(index)`.
- Automated tests added in `tests/test_karaoke_stage.py` (78/78 tests passing).

