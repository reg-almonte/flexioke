---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0049: In-Library Song Deletion with Cascade Cleanup

## Parent Story
- `docs/tickets/STORY-0021-stem-zip-export-and-cleanup.md`

## What to build
Build backend endpoint `DELETE /api/jobs/{job_id}` that deletes `./data/jobs/{job_id}/`, removes job from `jobs.json` store, cleans any associated archive file, and purges from playback queues. Add `🗑 Delete Track` button with confirmation prompt in Edit Details / Lyrics modal.

## Acceptance Criteria
- [x] Deleting a track deletes files and removes record from library and queues.
- [x] Confirmation prompt prevents accidental deletion.

## Implementation
- Added `delete_job()` in `src/services/job_manager.py` and `remove_jobs_from_queue()` in `src/services/queue_manager.py`.
- Added `DELETE /api/jobs/{job_id}` in `src/api/routes.py`.
- Added `#delete-track-btn` and confirmation flow in `src/static/index.html` and `src/static/library_queue.js`.
- Verified in `tests/test_track_export_and_cleanup.py`.

## Blocked by
- None (can start immediately)
