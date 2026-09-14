---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: completed
---


# STORY-0034: Looping Video Background Engine & Stage Synchronization

## Parent Epic
- `docs/tickets/EPIC-0011-video-backgrounds-stage-geometry-and-side-ab.md`

## What it delivers
Provides visual ambience for the karaoke stage by playing muted, looping background videos behind floating synchronized lyrics. Supports auto-discovering local video files in `/data/videos/`, uploading new videos, assigning videos and start timestamps per song, and synchronizing video playback (play, pause, seek, loop) with audio tracks.

## Acceptance Criteria
- [x] Server auto-indexes video files in `/data/videos/` and provides video listing, upload, and streaming endpoints.
- [x] Existing songs default to `bg001.mp4` as initial background video.
- [x] Video elements mount in `#karaoke-stage-card` behind floating lyrics with proper layering and opacity.
- [x] Video plays, pauses, seeks, and seamlessly loops in lockstep with song audio playback.
- [x] Song Details modal allows selecting video assets and configuring start offset timestamps.
- [x] **Mandatory Story Milestone Gate:** Requires explicit human manual verification in the browser before advancing to subsequent stories.

## Tasks
- [x] TASK-0071: Video Manager Service, Auto-Discovery & Streaming Endpoints
- [x] TASK-0072: Karaoke Stage Video Renderer, Per-Song Offset & Modal Selector

## Blocked by
- None (can start immediately).
