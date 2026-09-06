---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0008: Song Library Indexing & Search API

## Parent Story
- `STORY-0003-song-library-playback-queue.md`

## What to build
Implement the Song Library indexing service and `GET /api/jobs` endpoint to list all completed jobs with metadata (title, duration, source, stems, timestamp), supporting query parameter filtering (`?q=...` and `?status=...`).

## Acceptance Criteria
- [x] `GET /api/jobs` returns a JSON list of all completed songs with stem URLs and metadata.
- [x] Query parameter `?q=<term>` filters songs case-insensitively by title or source name.
- [x] Cached index in memory updates automatically when new jobs complete.
- [x] Unit/API tests verify library listing, filtering, and indexing accuracy.

## Blocked by
- TASK-0002: Job State Store, Metadata Persistence & Concurrency Manager

## Implementation
- **Branch:** `story/STORY-0003-song-library-playback-queue`
- **Models:** `JobListResponse` in `src/models.py`.
- **API Route:** `GET /api/jobs` with query parameter filtering (`status`, `q`) in `src/api/routes.py`.
- **Tests:** `tests/test_library_api.py` (4 tests passing, 24 suite-wide).
