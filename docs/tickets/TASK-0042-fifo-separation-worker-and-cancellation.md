---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0042: In-Process Thread-Safe FIFO Separation Worker & Queue Cancellation

## Parent Story
- `docs/tickets/STORY-0018-multi-upload-and-fifo-separation-queue.md`

## What to build
Ensure `JobManager` handles multiple jobs concurrently submitted by queuing them sequentially in a single FIFO worker thread pool (`ThreadPoolExecutor(max_workers=1)`). Implement `cancel_job(job_id)` method and `POST /api/jobs/{job_id}/cancel` endpoint to cancel queued or in-flight jobs, updating state to `CANCELLED`.

## Acceptance Criteria
- [x] Multiple jobs submitted are queued in order of submission timestamp.
- [x] `POST /api/jobs/{job_id}/cancel` cancels queued or in-progress jobs immediately.
- [x] Cancellation state is persisted to disk and in-memory cache.

## Implementation
- Implemented `JobStatus.CANCELLED` in `src/models.py`.
- Implemented `cancel_job()` and `get_queue_position()` in `src/services/job_manager.py`.
- Implemented `POST /api/jobs/{job_id}/cancel` endpoint in `src/api/routes.py`.
- Added cancellation guards in `src/services/pipeline.py:run_separation_pipeline()`.
- Unit tests verified in `tests/test_job_cancellation.py`.

## Blocked by
- None (can start immediately)
