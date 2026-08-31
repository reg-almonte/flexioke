---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# STORY-0018: Multi-File Batch Ingestion & Asynchronous Separation FIFO Queue

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Enables batch uploading of multiple audio tracks via file picker and drag-and-drop zone, processing them sequentially in a thread-safe FIFO background queue with queue position indicators and cancellation actions.

## Acceptance Criteria
- [ ] Multiple audio files can be selected or dropped simultaneously, queuing in `status: QUEUED`.
- [ ] Backend FIFO worker executes exactly 1 active `PROCESSING` job at a time, auto-advancing to subsequent queued items upon completion.
- [ ] UI shows active job progress alongside waiting items with queue positions and `✕ Cancel` buttons.

## Tasks
- [ ] TASK-0042: In-Process Thread-Safe FIFO Separation Worker & Queue Cancellation
- [ ] TASK-0043: Multi-File Drag-and-Drop Batch Dropzone & Live Queue Progress UI

## Blocked by
- None (can start immediately)
