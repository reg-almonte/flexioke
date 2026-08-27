---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: pending
---

# STORY-0005: Lyrics Storage Service & API Endpoints

## Parent Epic
- `EPIC-0002-karaoke-lyrics-mode.md`

## What it delivers
A backend service and REST endpoints allowing retrieval and atomic persistence of `.lrc` and plain-text lyrics files associated with any processed song job.

## Acceptance Criteria
- [ ] `GET /api/jobs/{job_id}/lyrics` returns the song's lyrics text and format detection flags.
- [ ] `POST /api/jobs/{job_id}/lyrics` atomically saves lyrics content to `./data/jobs/{job_id}/lyrics.lrc`.
- [ ] Unit and API tests verify successful storage, retrieval, and error handling for missing jobs.

## Tasks
- [ ] TASK-0013: Lyrics File Store & Pydantic Models
- [ ] TASK-0014: Lyrics REST Endpoints (`GET/POST /api/jobs/{job_id}/lyrics`)

## Blocked by
- None
