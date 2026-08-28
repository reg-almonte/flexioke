---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: pending
---

# TASK-0021: Unified "Edit Song Details & Lyrics" Modal UI & Atomic Save Workflow

## Parent Story
- `docs/tickets/STORY-0009-song-lyrics-editor-dual-search.md`

## What to build
Upgrade the lyrics editor modal in `src/templates/index.html` and `src/static/library_queue.js` into an "Edit Song Details & Lyrics" modal. Add input fields for Song Title and Artist Name above the lyrics textarea. On save, call `PATCH /api/jobs/{job_id}` for metadata and `POST /api/jobs/{job_id}/lyrics` for lyrics, update local state, close modal, and dispatch refresh events.

## Acceptance Criteria
- [ ] Modal displays inputs for Title and Artist alongside LRC lyrics textarea.
- [ ] Pre-fills current Title, Artist, and LRC lyrics when opened for a song.
- [ ] Saves metadata and lyrics atomically, displaying confirmation toast on success.
- [ ] Re-renders active track banner and library cards immediately upon save.

## Blocked by
- TASK-0020: Song Metadata Update REST Endpoint (PATCH /api/jobs/{job_id})
