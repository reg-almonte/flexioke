---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# STORY-0012: Modernized Karaoke Stage Bottom Transport Bar & Interactive Timecode

## Parent Epic
- `docs/tickets/EPIC-0004-karaoke-stage-transport-and-queue-refinements.md`

## What it delivers
Overhauls the bottom transport controls under the Karaoke Stage with an expanding YouTube-style master volume slider on speaker hover, click-toggleable elapsed vs. remaining timecode display, a dedicated "Restart Song" button (seek to 0:00 and auto-play), accessible Stage Settings in Fullscreen mode, and updated inward/outward expand icons.

## Acceptance Criteria
- [x] Left transport cluster contains Play/Pause, expanding hover volume slider (0–100%), and interactive timecode badge.
- [x] Clicking timecode badge switches between `<Current> / <Total>` and `<Remaining> / <Total>` (`-MM:SS / MM:SS`).
- [x] Right transport cluster contains Restart button (🔄), Next Track, Stop & Cue, Stage Settings (⚙), and Expand/Collapse.
- [x] Restart button seeks to 0.00s and resumes playback immediately.
- [x] Stage Settings modal is accessible and fully functional in both standard and Fullscreen mode.
- [x] Expand button displays outward arrows `⛶` in default mode and inward arrows `🗗` in Fullscreen mode.

## Tasks
- [x] TASK-0028: Left Transport Cluster: Play/Pause, Expanding Hover Volume Slider & Click-Toggleable Timecode
- [x] TASK-0029: Right Transport Cluster: Restart Button, Stop & Cue, Fullscreen Settings Access & Arrow Icons

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0012-modernized-bottom-transport-and-timecode`
- Complete implementation of TASK-0028 and TASK-0029.

