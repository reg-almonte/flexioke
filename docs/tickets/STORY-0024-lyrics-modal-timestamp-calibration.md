---
status: approved
approved_by: reg
approved_at: 2026-09-05
implementation: pending
---

# STORY-0024: In-Modal Synchronized Lyrics Timestamp Calibration Tool

## Parent Epic
- `docs/tickets/EPIC-0008-lyrics-calibration-and-karaoke-ux.md`

## What it delivers
Provides a real-time timestamp time-shift toolbar inside `#lyrics-modal` allowing users to calibrate `.lrc` timing with 1-click quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) or custom delta offsets, with minimum `00:00.00` clamping.

## Acceptance Criteria
- [ ] Quick buttons (`-0.5s`, `-0.1s`, `+0.1s`, `+0.5s`) shift all timestamp lines in `#lyrics-textarea` instantly.
- [ ] Custom offset input applies positive and negative delta shifts on `Apply`.
- [ ] Clamping prevents any timestamp from being negative (minimum `[00:00.00]`).
- [ ] Non-timestamp lines and metadata tags are left untouched.
- [ ] Ephemeral status banner confirms lines shifted.

## Tasks
- [ ] TASK-0054: Client-Side LRC Timestamp Shift Parser & Calibration Toolbar UI
