---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# STORY-0005: Lyrics Storage Service & API Endpoints

## Parent Epic
- `EPIC-0002-karaoke-lyrics-mode.md`

## What it delivers
A backend service and REST endpoints allowing retrieval and atomic persistence of `.lrc` and plain-text lyrics files associated with any processed song job.

## Acceptance Criteria
- [x] `GET /api/jobs/{job_id}/lyrics` returns the song's lyrics text and format detection flags.
- [x] `POST /api/jobs/{job_id}/lyrics` atomically saves lyrics content to `./data/jobs/{job_id}/lyrics.lrc`.
- [x] Unit and API tests verify successful storage, retrieval, and error handling for missing jobs.

## Tasks
- [x] TASK-0013: Lyrics File Store & Pydantic Models
- [x] TASK-0014: Lyrics REST Endpoints (`GET/POST /api/jobs/{job_id}/lyrics`)

## Blocked by
- None

## Implementation Summary
- **Branch:** `story/STORY-0005-lyrics-storage-api`
- **Modules:** `src/models.py`, `src/services/job_manager.py`, `src/api/routes.py`.
- **Tests:** 40 unit & integration tests passing across all test suites.
