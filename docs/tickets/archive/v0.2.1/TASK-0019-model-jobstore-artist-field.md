---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# TASK-0019: Model & JobStore Artist Field Extension with Legacy Deserialization

## Parent Story
- `docs/tickets/STORY-0008-backend-metadata-persistence.md`

## What to build
Extend the `Job` Pydantic model and `JobStore` service to include an optional `artist` field (`Optional[str] = None`). Ensure `JobStore` deserializes legacy `job.json` records that omit `artist` without throwing validation errors, setting `artist` to `None`. Update serialization to persist `artist` when present.

## Acceptance Criteria
- [x] `Job` model has `artist: Optional[str] = None`.
- [x] Loading legacy `job.json` files without `artist` field initializes `artist` as `None` without errors.
- [x] Updating or saving a job correctly writes `artist` to `job.json`.
- [x] Unit tests pass covering model instantiation, legacy JSON loading, and persistence.

## Blocked by
- None (can start immediately)

## Implementation
- **Branch:** `story/STORY-0008-backend-metadata-persistence`
- **Changes:**
  - Added `artist: Optional[str] = None` to `JobRecord` and `QueueItem` in `src/models.py`.
  - Added `artist` parameter to `JobManager.create_job` and updated `list_jobs` query matching in `src/services/job_manager.py`.
  - Added `artist` parameter to `QueueManager.add_to_queue` and `play_now` in `src/services/queue_manager.py`.
  - Added unit tests for artist assignment, legacy JSON loading without artist, and persistence in `tests/test_job_manager.py`.

