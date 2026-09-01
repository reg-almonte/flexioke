---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0043: Multi-File Drag-and-Drop Batch Dropzone & Live Queue Progress UI

## Parent Story
- `docs/tickets/STORY-0018-multi-upload-and-fifo-separation-queue.md`

## What to build
Update Stem Studio dropzone to support multiple files simultaneously (`<input type="file" multiple>`), batch upload them to `POST /api/jobs/upload`, and render a live queue status UI showing:
- Currently active job with progress bar, stage indicator, and cancel button.
- Waiting queued jobs list with `#N in queue` badges and cancel buttons.

## Acceptance Criteria
- [x] Users can select or drag multiple audio files simultaneously.
- [x] Multi-file batches are uploaded and enqueued sequentially.
- [x] Queued jobs list dynamically displays waiting items and allows one-click cancellation.

## Implementation
- Added `multiple` attribute and multi-file selection badge to `src/static/index.html`.
- Added `#queued-jobs-section`, `#queued-jobs-count`, `#queued-jobs-list`, and `#cancel-active-job-btn` in `src/static/index.html`.
- Implemented batch uploading loop and multi-job queue polling manager in `src/static/app.js`.
- Verified in `tests/test_frontend_routes.py` and test suite.

## Blocked by
- `docs/tickets/TASK-0042-fifo-separation-worker-and-cancellation.md` (in-review)
