---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0018: Multi-File Batch Ingestion & Asynchronous Separation FIFO Queue

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Enables users to select or drag multiple audio files at once for batch separation, enqueues them sequentially into an in-process thread-safe FIFO worker without freezing the UI or dropping requests, and provides live queue inspection with one-click cancellation.

## Acceptance Criteria
- [x] Multi-file drag-and-drop batch upload supported in Stem Studio.
- [x] In-process FIFO worker processes jobs sequentially without concurrency race conditions.
- [x] Live queue progress card renders active job progress, waiting queue order (#N), and cancellation triggers.

## Tasks
- [x] TASK-0042: In-Process Thread-Safe FIFO Separation Worker & Queue Cancellation
- [x] TASK-0043: Multi-File Drag-and-Drop Batch Dropzone & Live Queue Progress UI

## Implementation
- Branch: `story/STORY-0018-multi-upload-and-fifo-separation-queue`
- Delivered TASK-0042 and TASK-0043, verified by 96 passing tests.

## Blocked by
- `docs/tickets/STORY-0017-direct-audio-url-and-smart-naming.md` (in-review)
