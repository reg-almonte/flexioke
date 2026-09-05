---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: in-review
---

# TASK-0054: Client-Side LRC Timestamp Shift Parser & Calibration Toolbar UI

## Parent Story
- `docs/tickets/STORY-0024-lyrics-modal-timestamp-calibration.md`

## What to build
1. Implement `shiftLrcTimestamps(text, deltaSeconds)` in `src/static/library_queue.js` supporting standard `[MM:SS.xx]` and `[MM:SS.xxx]` timestamp tokens with `00:00.00` clamping.
2. In `src/static/index.html`, add the calibration toolbar above `#lyrics-textarea` with quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`), custom delta input, and ephemeral feedback banner.
3. Wire event handlers in `SongLibraryManager` in `src/static/library_queue.js`.
4. Add automated tests in `tests/test_lyrics_modal_frontend.py`.

## Acceptance Criteria
- [x] `shiftLrcTimestamps` correctly shifts timestamp lines and clamps at 0.
- [x] Toolbar UI renders properly in `#lyrics-modal`.
- [x] Quick buttons and custom input update `#lyrics-textarea` in place.
- [x] Automated tests pass cleanly.

## Implementation
- Added Time-Shift Calibration Toolbar (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`, custom offset input, `Apply` button) and `#lyrics-shift-alert` banner in `#lyrics-modal` in `src/static/index.html`.
- Implemented `shiftLrcTimestamps(text, deltaSeconds)`, `handleShiftLrc()`, and `showLyricsShiftAlert()` in `src/static/library_queue.js`.
- Added test coverage in `tests/test_lyrics_modal_frontend.py`.
