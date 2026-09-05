---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: in-review
---

# STORY-0024: In-Modal Synchronized Lyrics Timestamp Calibration Tool

## Parent Epic
- `docs/tickets/EPIC-0008-lyrics-calibration-and-karaoke-ux.md`

## What it delivers
Provides a real-time timestamp time-shift toolbar inside `#lyrics-modal` allowing users to calibrate `.lrc` timing with 1-click quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) or custom delta offsets, with minimum `00:00.00` clamping.

## Acceptance Criteria
- [x] Quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) shift all timestamp lines in `#lyrics-textarea` instantly.
- [x] Custom offset input applies positive and negative delta shifts on `Apply`.
- [x] Clamping prevents any timestamp from being negative (minimum `[00:00.00]`).
- [x] Non-timestamp lines and metadata tags are left untouched.
- [x] Ephemeral status banner confirms lines shifted.

## Tasks
- [x] TASK-0054: Client-Side LRC Timestamp Shift Parser & Calibration Toolbar UI

## Implementation
- Added Time-Shift Calibration Toolbar (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`, custom offset input, `Apply` button) and status alert in `#lyrics-modal`.
- Implemented `shiftLrcTimestamps` in `src/static/library_queue.js` with instant in-place DOM updates.
- Verified with automated tests in `tests/test_lyrics_modal_frontend.py`.
