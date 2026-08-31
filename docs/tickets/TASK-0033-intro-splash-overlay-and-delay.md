---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0033: Title & Artist Intro Splash Overlay with Pre-buffered Audio Delay (0–5s)

## Parent Story
- `docs/tickets/STORY-0014-intro-splash-and-countdown-threshold.md`

## What to build
Implement an animated Song Title and Artist intro splash overlay on the Karaoke Stage. Add an "Intro Splash Duration" slider in Stage Settings (0–5s, default 3s). When starting a song, audio stems pre-buffer while the splash card displays for the configured duration, starting playback automatically at 0.00s once elapsed (0s starts immediately).

## Acceptance Criteria
- [x] Intro splash overlay displays Song Title and Artist in prominent typography.
- [x] Stage Settings includes Intro Splash Duration slider (0–5s, step 1s, default 3s) with live display and localStorage persistence.
- [x] Audio playback start is delayed by the configured duration while stems pre-buffer.
- [x] Setting 0s bypasses the intro splash and starts playback immediately.

## Blocked by
- None (can start immediately)

## Implementation
- Branch: `story/STORY-0014-intro-splash-and-countdown-threshold`
- Delivered animated `#karaoke-intro-splash` overlay in `src/static/index.html` and `#settings-intro-splash` slider in Stage Settings.
- Implemented `triggerIntroSplash(job, autoPlay)` with pre-buffering audio delay and cancellation cleanup in `src/static/karaoke.js`.
- Automated regression tests added in `tests/test_karaoke_stage.py` (76/76 tests passing).

