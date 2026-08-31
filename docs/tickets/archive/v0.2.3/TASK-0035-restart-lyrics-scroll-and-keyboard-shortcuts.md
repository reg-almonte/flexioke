---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0035: Stage Restart Lyrics Scroll-to-Top, Highlight Reset & Keyboard Shortcut (R/Home)

## Parent Story
- `docs/tickets/STORY-0015-restart-lyrics-reset-and-dual-colors.md`

## What to build
Update the "Restart Song" action in the karaoke stage manager so that triggering restart immediately scrolls the lyrics stage container to the top (`scrollTop = 0`), resets `activeLineIndex = -1`, and removes active highlight classes from all line elements. Add keyboard event listeners for `R` and `Home` to restart the song during active Karaoke Mode.

## Acceptance Criteria
- [x] Clicking Restart Song (🔄) seeks audio to 0.00s, scrolls lyrics container to top, and clears active line highlighting.
- [x] Pressing `R` or `Home` on the keyboard during Karaoke view triggers song restart.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0015-restart-lyrics-reset-and-dual-colors`
- Implemented `restartSong()` method in `KaraokeStageManager` atomically scrolling lyrics to top (`scrollTop = 0`), resetting `activeLineIndex = -1`, clearing all active highlight styles, and coordinating with audio stems and intro splash.
- Added document keydown listener for `R` / `Home` shortcuts in Karaoke Mode and `Esc` for modal/fullscreen dismissals.
- Automated tests added in `tests/test_karaoke_stage.py` (78/78 tests passing).

