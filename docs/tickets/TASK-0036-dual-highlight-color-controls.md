---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0036: Dual Stage Highlight Color Pickers (Border Glow & Background Fill Tint)

## Parent Story
- `docs/tickets/STORY-0015-restart-lyrics-reset-and-dual-colors.md`

## What to build
Split the Stage Settings color customization into two independent controls: "Highlight Glow & Border Color" (`--karaoke-highlight-color`) and "Highlight Fill & Background Color" (`--karaoke-highlight-fill`). Update active lyric styling to apply both custom properties dynamically with real-time preview and localStorage persistence.

## Acceptance Criteria
- [ ] Stage Settings includes two color pickers with hex code displays.
- [ ] Active lyric lines use `--karaoke-highlight-color` for borders/glow and `--karaoke-highlight-fill` for background tint.
- [ ] Changes apply immediately to rendered lyrics in real time and persist across sessions.

## Blocked by
- None (can start immediately in parallel)
