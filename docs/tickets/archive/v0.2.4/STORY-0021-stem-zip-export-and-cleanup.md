---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# STORY-0021: Combined Stem Zip Export, Track Deletion & Post-Processing Archiving

## Parent Epic
- `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

## What it delivers
Provides 1-click combined `.zip` stem and lyrics export, in-library track deletion with cascading storage cleanup, and automatic post-separation raw audio archiving to `./data/archive/`.

## Acceptance Criteria
- [x] `GET /api/jobs/{job_id}/export/zip` streams `{title}_stems.zip` with all 3 stems and `lyrics.lrc` (if present).
- [x] `DELETE /api/jobs/{job_id}` deletes job files, stems, lyrics, and metadata upon confirmation.
- [x] Completed jobs have their original input audio moved to `./data/archive/`.

## Tasks
- [x] TASK-0048: Dynamic Combined Stem & Lyrics .zip Streaming Endpoint
- [x] TASK-0049: In-Library Song Deletion with Cascade Cleanup
- [x] TASK-0050: Post-Separation Raw Input Audio Archiving to ./data/archive/

## Implementation
- Branch: `story/STORY-0021-stem-zip-export-and-cleanup`
- Completed TASK-0048, TASK-0049, and TASK-0050, verified by 103 passing automated tests.

## Blocked by
- `docs/tickets/STORY-0020-studio-catalog-modal-and-default-sort.md` (in-review)
