---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0029: Right Transport Cluster: Restart Button, Stop & Cue, Fullscreen Settings Access & Arrow Icons

## Parent Story
- `docs/tickets/STORY-0012-modernized-bottom-transport-and-timecode.md`

## What to build
Reorganize the right side of the bottom Karaoke transport bar: add a Restart button (🔄) that seeks to 0:00 and resumes playing, preserve Next and Stop & Cue buttons, ensure the Stage Settings button (⚙) remains visible and accessible in Fullscreen mode with high modal z-index (`z-[10000]`), and update the Expand/Collapse button to show outward arrows (`⛶`) in standard mode and inward arrows (`🗗`) in Fullscreen mode.

## Acceptance Criteria
- [x] Restart button seeks to 0:00 and immediately starts/resumes playback.
- [x] Settings button (⚙) is clickable and opens Settings modal in both standard and Fullscreen modes.
- [x] Expand/Collapse button toggles between outward `⛶` and inward `🗗` arrow icons.
- [x] Stop & Cue and Next buttons function smoothly in the right cluster.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0012-modernized-bottom-transport-and-timecode`
- Changes: Added `#karaoke-restart-btn` in right transport cluster, bound restart seek & play action in `karaoke.js`, updated `#karaoke-settings-modal` to `z-[10000]`, and added tests in `tests/test_karaoke_stage.py`.

