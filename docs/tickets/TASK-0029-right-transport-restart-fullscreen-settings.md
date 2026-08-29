---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: pending
---

# TASK-0029: Right Transport Cluster: Restart Button, Stop & Cue, Fullscreen Settings Access & Arrow Icons

## Parent Story
- `docs/tickets/STORY-0012-modernized-bottom-transport-and-timecode.md`

## What to build
Reorganize the right side of the bottom Karaoke transport bar: add a Restart button (🔄) that seeks to 0:00 and resumes playing, preserve Next and Stop & Cue buttons, ensure the Stage Settings button (⚙) remains visible and accessible in Fullscreen mode with high modal z-index (`z-[10000]`), and update the Expand/Collapse button to show outward arrows (`⛶`) in standard mode and inward arrows (`🗗`) in Fullscreen mode.

## Acceptance Criteria
- [ ] Restart button seeks to 0:00 and immediately starts/resumes playback.
- [ ] Settings button (⚙) is clickable and opens Settings modal in both standard and Fullscreen modes.
- [ ] Expand/Collapse button toggles between outward `⛶` and inward `🗗` arrow icons.
- [ ] Stop & Cue and Next buttons function smoothly in the right cluster.

## Blocked by
- None (can start immediately in parallel)
