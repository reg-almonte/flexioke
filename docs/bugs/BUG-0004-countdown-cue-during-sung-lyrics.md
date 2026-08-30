---
status: in-progress
filed_at: 2026-08-31
---

# Bug Report: Visual Countdown Cue Triggering During Active Sung Lyrics

## Related
- Functional Spec: `docs/specs/version0.2.3.md` (§2 Configurable Visual Countdown Cue Flow)
- Requirements: `docs/requirements/version0.2.3.md` (§2 Visual Countdown Cues)
- Story: `docs/tickets/STORY-0014-intro-splash-and-countdown-threshold.md`
- Task: `docs/tickets/TASK-0034-configurable-countdown-gap-threshold.md`

## Summary
During manual testing of Version 0.2.3, the visual countdown cue (`● ○ ○` → `● ● ○` → `● ● ●`) was observed displaying in the middle of active singing when the gap between two sung lyric lines was >= 3s, even though lyrics were actively being sung on the current line or transitioning directly between sung lines. *(Fix applied, pending verification)*

## Root Cause Analysis
In `src/static/karaoke.js`, `updateCountdownCue(currentTime)` evaluated `isInterlude` solely on the time delta between `lyricsData.lines[nextIndex].time` and `lyricsData.lines[nextIndex - 1].time` (`(nextLine.time - prevLineTime) >= threshold`), without verifying:
1. Whether `nextLine` is actually a sung lyric line (rather than an instrumental break marker or empty line).
2. Whether the current playback position is in an intro or an explicit non-lyric empty line / instrumental break (`isInstrumental` / empty string).
When a sung lyric line was spaced >= 3s from the subsequent lyric line, the countdown cue triggered 3 seconds before the next line while the user was still actively singing the current line.

## Applied Fix
1. In `LrcParser.parse()`, recorded `isInstrumental` and `rawText` on parsed line objects.
2. In `updateCountdownCue(currentTime)`:
   - Target line `targetLine` is identified as the next upcoming **sung lyric line** (`!line.isInstrumental && line.rawText.length > 0`).
   - Trigger countdown cue **only** during:
     - **Intro:** All lines prior to `targetLine` are non-lyric / intro, `targetLine.time >= threshold`, and `targetLine.time - currentTime <= 3.0s`.
     - **Instrumental Break / Empty Line:** The immediately preceding line `prevLine` is an explicit non-lyric / empty string line, `(targetLine.time - prevLine.time) >= threshold`, `currentTime >= prevLine.time`, and `targetLine.time - currentTime <= 3.0s`.
   - In all other situations, countdown cue remains hidden.
- Automated reproduction unit test `test_countdown_cue_only_triggers_on_intro_or_empty_line_interlude` added and passing in `tests/test_karaoke_stage.py` (83/83 tests passing).
