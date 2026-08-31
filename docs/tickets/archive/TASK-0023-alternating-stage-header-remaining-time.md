---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# TASK-0023: Alternating "Now Singing" ⟷ "Up Next" Header & Remaining Time Badge

## Parent Story
- `docs/tickets/STORY-0010-stage-header-countdown-controls.md`

## What to build
Enhance the stage header in `src/static/karaoke_stage.js` and `src/templates/index.html`. Format the header to show `"Now Singing: [Title] • [Artist]"` and a time badge showing `MM:SS / MM:SS (-MM:SS remaining)`. If upcoming songs exist in the queue, run a timer that alternates between "Now Singing" and "Up Next: [Next Title] • [Next Artist]" using smooth CSS opacity cross-fades on a configurable interval.

## Acceptance Criteria
- [x] Displays Title and Artist in stage header during playback.
- [x] Displays total duration and real-time remaining countdown `(-MM:SS)`.
- [x] Smoothly cross-fades between "Now Singing" and "Up Next" when queue is non-empty.
- [x] Resets immediately to "Now Singing" when queue becomes empty or playback changes.

## Blocked by
- None (can start immediately)

## Implementation
- **Branch:** `story/STORY-0010-stage-header-countdown-controls`
- **Changes:**
  - Updated stage header in `src/static/index.html` with `#karaoke-header-banner`, `#karaoke-banner-label`, `#karaoke-song-artist`, and updated timecode display.
  - Added alternating banner cycle (`startAlternatingBannerCycle`, `toggleAlternatingBanner`, `setBannerContent`) with CSS opacity cross-fade in `src/static/karaoke.js`.
  - Added real-time remaining countdown timecode badge `(-MM:SS)` in `onTimeCheck()`.
  - Added test coverage in `tests/test_karaoke_stage.py`.

