---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0014: Lyrics REST Endpoints (GET / POST /api/jobs/{job_id}/lyrics)

## Parent Story
- `STORY-0005-lyrics-storage-api.md`

## What to build
Implement `GET /api/jobs/{job_id}/lyrics` to retrieve lyrics and `POST /api/jobs/{job_id}/lyrics` to update lyrics for a specific song in `src/api/routes.py`.

## Acceptance Criteria
- [x] `GET /api/jobs/{job_id}/lyrics` returns `200 OK` with lyrics payload or empty indicator if none exists.
- [x] `POST /api/jobs/{job_id}/lyrics` saves lyrics and returns `200 OK`.
- [x] Returns `404 Not Found` if `job_id` does not exist.
- [x] Integration tests verify API behavior.

## Blocked by
- TASK-0013: Lyrics File Store & Pydantic Models

## Implementation
- **Branch:** `story/STORY-0005-lyrics-storage-api`
- **Endpoints:** `GET /api/jobs/{job_id}/lyrics` and `POST /api/jobs/{job_id}/lyrics` in `src/api/routes.py`.
- **Tests:** `tests/test_lyrics_api.py` (3 tests passing, 40 suite-wide).
