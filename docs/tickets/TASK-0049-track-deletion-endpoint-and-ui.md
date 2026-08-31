---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0049: In-Library Song Deletion with Cascade Cleanup

## Parent Story
- `docs/tickets/STORY-0021-stem-zip-export-and-cleanup.md`

## What to build
Build backend endpoint `DELETE /api/jobs/{job_id}` that deletes `./data/jobs/{job_id}/`, removes job from `jobs.json` store, cleans any associated archive file, and purges from playback queues. Add `🗑 Delete Track` button with confirmation prompt in Edit Details / Lyrics modal.

## Acceptance Criteria
- [ ] Deleting a track deletes files and removes record from library and queues.
- [ ] Confirmation prompt prevents accidental deletion.

## Blocked by
- None (can start immediately)
