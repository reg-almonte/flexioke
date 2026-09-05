---
status: approved
approved_by: reg
approved_at: 2026-09-05
---

# EPIC-0008: Synchronized Lyrics Calibration & Karaoke UX Enhancements

## Parent ADR
- `docs/design/ADR-0009-lyrics-calibration-and-karaoke-ux.md`

## What it delivers
Delivers Version 0.2.6 enhancements: an interactive in-modal timestamp time-shift calibration tool for `.lrc` lyrics in `#lyrics-modal`, collapsible Playback Queue and Song Library sidebar cards in Karaoke Mode with localStorage persistence, and smart idle stage play dispatch from queue with catalog modal fallback.

## Stories
- `docs/tickets/STORY-0024-lyrics-modal-timestamp-calibration.md`
- `docs/tickets/STORY-0025-karaoke-sidebar-accordions.md`
- `docs/tickets/STORY-0026-smart-idle-stage-play-dispatch.md`

## Definition of Done
- [ ] Users can shift all `.lrc` timestamps forward or backward using quick buttons (`±0.1s`, `±0.5s`) or custom delta input with real-time DOM update and clamping at `00:00.00`.
- [ ] Playback Queue and Song Library sidebar cards in Karaoke Mode can be collapsed and expanded with animated chevrons and persistent state.
- [ ] Clicking Play or the stage canvas on an idle stage starts the first queued song, or opens the Song Catalog modal if the queue is empty.
- [ ] 100% automated test suite passing with zero regressions.
