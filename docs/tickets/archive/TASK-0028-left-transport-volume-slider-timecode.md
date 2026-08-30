---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0028: Left Transport Cluster: Play/Pause, Expanding Hover Volume Slider & Click-Toggleable Timecode

## Parent Story
- `docs/tickets/STORY-0012-modernized-bottom-transport-and-timecode.md`

## What to build
Reorganize the left side of the bottom Karaoke transport bar. Implement an expanding volume control on hover/focus over the speaker icon with a horizontal slider (0–100%) that adjusts master gain across stems and persists in `localStorage`. Enhance the timecode badge so clicking it toggles between Elapsed/Total (`MM:SS / MM:SS`) and Remaining/Total (`(-MM:SS) / MM:SS`).

## Acceptance Criteria
- [x] Left transport cluster contains Play/Pause, Expanding Volume, and Timecode badge.
- [x] Hovering or focusing the volume speaker icon reveals a smooth horizontal slider.
- [x] Volume adjustments scale master output and persist across tracks.
- [x] Clicking timecode badge toggles between Elapsed and Remaining time modes.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0012-modernized-bottom-transport-and-timecode`
- Changes: Added left transport cluster with expanding hover volume slider in `index.html` and `styles.css`, implemented `toggleTimecodeMode()` and persisted `flexioke_master_volume` and `flexioke_timecode_mode` in `karaoke.js`, and added integration tests in `tests/test_karaoke_stage.py`.

