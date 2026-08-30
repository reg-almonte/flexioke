---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0035: Stage Restart Lyrics Scroll-to-Top, Highlight Reset & Keyboard Shortcut (R/Home)

## Parent Story
- `docs/tickets/STORY-0015-restart-lyrics-reset-and-dual-colors.md`

## What to build
Update the "Restart Song" action in the karaoke stage manager so that triggering restart immediately scrolls the lyrics stage container to the top (`scrollTop = 0`), resets `activeLineIndex = -1`, and removes active highlight classes from all line elements. Add keyboard event listeners for `R` and `Home` to restart the song during active Karaoke Mode.

## Acceptance Criteria
- [ ] Clicking Restart Song (🔄) seeks audio to 0.00s, scrolls lyrics container to top, and clears active line highlighting.
- [ ] Pressing `R` or `Home` on the keyboard during Karaoke view triggers song restart.

## Blocked by
- None (can start immediately in parallel)
