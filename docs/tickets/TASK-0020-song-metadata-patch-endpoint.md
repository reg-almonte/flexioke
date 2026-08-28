---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: pending
---

# TASK-0020: Song Metadata Update REST Endpoint (PATCH /api/jobs/{job_id})

## Parent Story
- `docs/tickets/STORY-0008-backend-metadata-persistence.md`

## What to build
Implement a `PATCH /api/jobs/{job_id}` endpoint in `src/api/jobs.py` that accepts a `JobUpdateMetadataRequest` with optional `title` and `artist` strings. Validate inputs, update the job in `JobStore`, persist to disk, and return the updated `Job` representation.

## Acceptance Criteria
- [ ] `JobUpdateMetadataRequest` schema validates `title` (1-200 chars if provided) and `artist` (0-200 chars).
- [ ] `PATCH /api/jobs/{job_id}` returns 200 with the updated job object when valid.
- [ ] Returns 404 Not Found if `job_id` does not exist.
- [ ] Returns 422 if validation fails.
- [ ] Integration tests verify metadata update via HTTP client and persistence to disk.

## Blocked by
- TASK-0019: Model & JobStore Artist Field Extension with Legacy Deserialization
