---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0015: Stage Restart Lyrics/Highlight Reset & Dual Highlight Color Customization

## Parent Epic
- `docs/tickets/EPIC-0005-karaoke-stage-ux-and-song-catalog.md`

## What it delivers
Eliminates state drift when restarting a track by instantly scrolling the lyrics stage to the top (`scrollTop = 0`) and resetting highlighted lines, introduces keyboard shortcuts (`R` / `Home` for Restart), and provides dual color pickers in Stage Settings for customizing both the active glow/border color and the background fill tint.

## Acceptance Criteria
- [x] Clicking "Restart Song" (🔄) or pressing `R` / `Home` resets audio stems to 0.00s, scrolls the lyrics stage immediately to `scrollTop = 0`, and clears active line highlighting.
- [x] Stage Settings provides two color pickers: "Highlight Glow & Border Color" (`--karaoke-highlight-color`) and "Highlight Fill & Background Color" (`--karaoke-highlight-fill`).
- [x] Changing colors updates rendered stage lyrics immediately in real-time and persists in localStorage.

## Tasks
- [x] TASK-0035: Stage Restart Lyrics Scroll-to-Top, Highlight Reset & Keyboard Shortcut (R/Home)
- [x] TASK-0036: Dual Stage Highlight Color Pickers (Border Glow & Background Fill Tint)

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0015-restart-lyrics-reset-and-dual-colors`
- Delivered `restartSong()` method with immediate `scrollTop = 0` scroll, active highlight reset, and keyboard shortcuts (`R` / `Home` / `Esc`).
- Delivered dual Stage Settings color pickers for `--karaoke-highlight-color` and `--karaoke-highlight-fill`.
- Full test suite passing (78/78 tests).

