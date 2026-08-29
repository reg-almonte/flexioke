---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: pending
---

# TASK-0028: Left Transport Cluster: Play/Pause, Expanding Hover Volume Slider & Click-Toggleable Timecode

## Parent Story
- `docs/tickets/STORY-0012-modernized-bottom-transport-and-timecode.md`

## What to build
Reorganize the left side of the bottom Karaoke transport bar. Implement an expanding volume control on hover/focus over the speaker icon with a horizontal slider (0–100%) that adjusts master gain across stems and persists in `localStorage`. Enhance the timecode badge so clicking it toggles between Elapsed/Total (`MM:SS / MM:SS`) and Remaining/Total (`(-MM:SS) / MM:SS`).

## Acceptance Criteria
- [ ] Left transport cluster contains Play/Pause, Expanding Volume, and Timecode badge.
- [ ] Hovering or focusing the volume speaker icon reveals a smooth horizontal slider.
- [ ] Volume adjustments scale master output and persist across tracks.
- [ ] Clicking timecode badge toggles between Elapsed and Remaining time modes.

## Blocked by
- None (can start immediately in parallel)
