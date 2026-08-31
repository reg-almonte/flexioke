---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# TASK-0024: Visual Intro & Interlude 3-Beat Countdown Cue Engine

## Parent Story
- `docs/tickets/STORY-0010-stage-header-countdown-controls.md`

## What to build
Implement visual countdown cue logic inside `KaraokeStage` in `src/static/karaoke_stage.js`. Calculate the time delta until the next upcoming lyric timestamp. If `0.0s < delta <= 3.0s` and the line is the first line or follows an instrumental break > 5s, render a pulsating 3-dot countdown badge (`● ○ ○` -> `● ● ○` -> `● ● ●`). Fade out seamlessly when the lyric line starts.

## Acceptance Criteria
- [x] Detects song intro and interludes > 5.0s between lines.
- [x] Triggers 3-second countdown visual cue prior to the lyric line timestamp.
- [x] Displays animated 3-dot visual badge (`3`, `2`, `1`).
- [x] Cleans up and disappears when singing starts, on seek, or on pause.

## Blocked by
- None (can start immediately)

## Implementation
- **Branch:** `story/STORY-0010-stage-header-countdown-controls`
- **Changes:**
  - Added `#karaoke-countdown-cue` badge container in `src/static/index.html`.
  - Implemented `updateCountdownCue(currentTime)` and `hideCountdownCue()` in `src/static/karaoke.js` detecting intros and interludes > 5.0s and rendering animated 3-dot countdown cues 3 seconds prior to singing.
  - Added automated tests in `tests/test_karaoke_stage.py`.

