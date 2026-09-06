---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0009: Playback Queue Service & Playlist State Logic

## Parent Story
- `STORY-0003-song-library-playback-queue.md`

## What to build
Implement the playlist queue management domain model and state coordinator to handle queue operations: enqueueing songs, dequeueing, removing items, reordering, and advancing to the next track.

## Acceptance Criteria
- [x] Supports queue state operations (add, remove, clear, next, get queue).
- [x] Maintains song metadata and stem references for each queued item.
- [x] Unit tests verify queue operations, boundary cases (empty queue, duplicate additions), and sequence integrity.

## Blocked by
- TASK-0008: Song Library Indexing & Search API

## Implementation
- **Branch:** `story/STORY-0003-song-library-playback-queue`
- **Models:** `QueueItem`, `QueueResponse` in `src/models.py`.
- **Service:** `src/services/queue_manager.py` handling thread-safe FIFO queue operations, play now, and track transitions.
- **Endpoints:** `GET /api/queue`, `POST /api/queue/add`, `POST /api/queue/play-now`, `POST /api/queue/next`, `DELETE /api/queue/{queue_id}`, `DELETE /api/queue` in `src/api/routes.py`.
- **Tests:** `tests/test_queue_service.py` (3 tests passing, 27 suite-wide).
