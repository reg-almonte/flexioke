---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# TASK-0020: Song Metadata Update REST Endpoint (PATCH /api/jobs/{job_id})

## Parent Story
- `docs/tickets/STORY-0008-backend-metadata-persistence.md`

## What to build
Implement a `PATCH /api/jobs/{job_id}` endpoint in `src/api/jobs.py` that accepts a `JobUpdateMetadataRequest` with optional `title` and `artist` strings. Validate inputs, update the job in `JobStore`, persist to disk, and return the updated `Job` representation.

## Acceptance Criteria
- [x] `JobUpdateMetadataRequest` schema validates `title` (1-200 chars if provided) and `artist` (0-200 chars).
- [x] `PATCH /api/jobs/{job_id}` returns 200 with the updated job object when valid.
- [x] Returns 404 Not Found if `job_id` does not exist.
- [x] Returns 422 if validation fails.
- [x] Integration tests verify metadata update via HTTP client and persistence to disk.

## Blocked by
- TASK-0019: Model & JobStore Artist Field Extension with Legacy Deserialization

## Implementation
- **Branch:** `story/STORY-0008-backend-metadata-persistence`
- **Changes:**
  - Added `JobUpdateMetadataRequest` schema with `title` (1-200 chars) and `artist` (0-200 chars) in `src/models.py`.
  - Implemented `@router.patch("/jobs/{job_id}", response_model=JobRecord)` in `src/api/routes.py` with 404/422 handling.
  - Added integration tests covering full update, partial update, 404, and 422 validation in `tests/test_library_api.py`.

