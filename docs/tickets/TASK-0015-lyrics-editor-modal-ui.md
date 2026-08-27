---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: pending
---

# TASK-0015: Song Library Lyrics Editor Modal & Paste UI

## Parent Story
- `STORY-0006-frontend-lyrics-editor-ui.md`

## What to build
Create the Lyrics Editor modal in `src/static/index.html` and JavaScript controller in `src/static/library_queue.js` / `src/static/lyrics.js` to open the modal, load existing lyrics via API, and save updated lyrics.

## Acceptance Criteria
- [ ] Clicking "📝 Lyrics" on any song card opens the lyrics modal.
- [ ] Form displays current lyrics or empty textarea with syntax tips.
- [ ] Submitting form sends `POST /api/jobs/{job_id}/lyrics` and dispatches `flexioke:lyrics-updated` event.

## Blocked by
- TASK-0014: Lyrics REST Endpoints
