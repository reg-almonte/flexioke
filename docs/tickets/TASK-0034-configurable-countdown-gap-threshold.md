---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0034: Configurable Countdown Cue Gap Threshold (3s–5s) & Instrumental Interlude Evaluator

## Parent Story
- `docs/tickets/STORY-0014-intro-splash-and-countdown-threshold.md`

## What to build
Add a "Countdown Cue Threshold" slider in Stage Settings (3s–5s, step 1s, default 3s). Update the countdown evaluator in the stage manager to evaluate gaps between lines (or song start) and trigger the 3-beat visual pulse (● ○ ○ → ● ● ○ → ● ● ●) starting at T - 3.0s only when the gap >= configured threshold.

## Acceptance Criteria
- [x] Stage Settings includes Countdown Cue Threshold slider (3s–5s, step 1s, default 3s) with live display and localStorage persistence.
- [x] Gaps shorter than the chosen threshold do not trigger the countdown cue.
- [x] Gaps >= threshold trigger the 3-beat countdown starting 3.0s before singing resumes.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0014-intro-splash-and-countdown-threshold`
- Added `#settings-countdown-threshold` slider in Stage Settings modal (`3s`–`5s`, default `3s`).
- Enhanced `updateCountdownCue(currentTime)` in `src/static/karaoke.js` to evaluate intro and instrumental gaps against `this.config.countdownThreshold`.
- Added automated regression tests in `tests/test_karaoke_stage.py` (76/76 tests passing).

