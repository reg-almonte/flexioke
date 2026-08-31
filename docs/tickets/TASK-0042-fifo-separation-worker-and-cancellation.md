---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0042: In-Process Thread-Safe FIFO Separation Worker & Queue Cancellation

## Parent Story
- `docs/tickets/STORY-0018-multi-upload-and-fifo-separation-queue.md`

## What to build
Extend `JobManager` with an in-process thread-safe FIFO queue worker (`asyncio.Queue` / background thread) that processes `JobStatus.QUEUED` items sequentially (1 at a time). Add `POST /api/jobs/{job_id}/cancel` endpoint to mark tasks `CANCELLED` and skip execution.

## Acceptance Criteria
- [ ] Ingestion endpoints enqueue jobs without blocking HTTP responses.
- [ ] Sequential FIFO execution guarantees only 1 job executes separation at any time.
- [ ] `POST /api/jobs/{job_id}/cancel` removes or cancels in-flight/queued tasks cleanly.

## Blocked by
- None (can start immediately)
