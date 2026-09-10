---
status: approved
approved_by: reg
approved_at: 2026-09-10
implementation: in-progress
---


# TASK-0071: Video Manager Service, Auto-Discovery & Streaming Endpoints

## Parent Story
- `docs/tickets/STORY-0034-video-background-engine-and-stage-sync.md`

## What to build
Build the backend video management service and REST endpoints:
- Thread-safe directory scanner for `./data/videos/` supporting `.mp4`, `.webm`, `.mov`, `.mkv`.
- Endpoint to list available videos with metadata (`GET /api/videos`).
- Endpoint to upload new video files with validation (`POST /api/videos/upload`).
- Streamable HTTP Range video endpoint (`GET /api/videos/{filename}`).
- Initialize `bg001.mp4` as default video for library tracks without an explicit video assignment.
- Ensure `./data/videos/` is ignored by git and protected in tests.

## Acceptance Criteria
- [ ] `GET /api/videos` returns all video files in `./data/videos/`.
- [ ] `POST /api/videos/upload` safely saves uploaded video assets to disk and indexes them.
- [ ] `GET /api/videos/{filename}` supports HTTP 206 Partial Content range requests for video seeking.
- [ ] Job metadata model includes `video_id` (default `"bg001.mp4"`) and `video_offset_seconds` (default `0.0`).
- [ ] Comprehensive unit and endpoint integration tests pass cleanly.

## Blocked by
- None (can start immediately).
