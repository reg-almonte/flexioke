---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0015: Song Library Lyrics Editor Modal & Paste UI

## Parent Story
- `STORY-0006-frontend-lyrics-editor-ui.md`

## What to build
Create the Lyrics Editor modal in `src/static/index.html` and JavaScript controller in `src/static/library_queue.js` / `src/static/lyrics.js` to open the modal, load existing lyrics via API, and save updated lyrics.

## Acceptance Criteria
- [x] Clicking "📝 Lyrics" on any song card opens the lyrics modal.
- [x] Form displays current lyrics or empty textarea with syntax tips.
- [x] Submitting form sends `POST /api/jobs/{job_id}/lyrics` and dispatches `flexioke:lyrics-updated` event.

## Blocked by
- TASK-0014: Lyrics REST Endpoints

## Implementation
- **Branch:** `story/STORY-0006-frontend-lyrics-editor-ui`
- **Modal HTML:** `src/static/index.html` (`#lyrics-modal`, `#lyrics-textarea`, `#save-lyrics-btn`).
- **UI Logic:** `src/static/library_queue.js` adding `📝` lyrics button to song cards, opening modal, loading via `GET /api/jobs/{job_id}/lyrics`, and saving via `POST /api/jobs/{job_id}/lyrics` with `flexioke:lyrics-updated` event dispatch.
- **Tests:** `tests/test_lyrics_modal_frontend.py` (2 tests passing, 42 suite-wide).
