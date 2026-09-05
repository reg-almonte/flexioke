---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: pending
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
- [ ] `shiftLrcTimestamps` correctly shifts timestamp lines and clamps at 0.
- [ ] Toolbar UI renders properly in `#lyrics-modal`.
- [ ] Quick buttons and custom input update `#lyrics-textarea` in place.
- [ ] Automated tests pass cleanly.
