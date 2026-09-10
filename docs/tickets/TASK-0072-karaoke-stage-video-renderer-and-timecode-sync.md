---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: completed
---

# TASK-0072: Karaoke Stage Video Renderer, Per-Song Offset & Modal Selector

## Parent Story
- `docs/tickets/STORY-0034-video-background-engine-and-stage-sync.md`

## What to build
Build the frontend video renderer and synchronization engine:
- Mount `<video id="karaoke-bg-video">` inside `#karaoke-stage-card` with `pointer-events-none`, `muted`, `loop`, `playsinline`, and `opacity-40` backdrop styling.
- Coordinate video playback with audio playback state (play, pause, restart, seek, loop) using `(audio.currentTime + offset) % video.duration`.
- Add video selector dropdown and numeric start offset input in Song Details & Lyrics modal (`#lyrics-modal`) saving via `PATCH /api/jobs/{id}/metadata`.
- Add manual verification instructions for browser testing.

## Acceptance Criteria
- [x] Video renders smoothly behind floating lyrics on `#karaoke-stage-card`.
- [x] Video starts, pauses, seeks, and loops synchronously with song audio.
- [x] Video selection and start offset timestamp save and reload per song.
- [x] Manual test in browser verifies visual quality and looping playback.

## Blocked by
- `TASK-0071`
