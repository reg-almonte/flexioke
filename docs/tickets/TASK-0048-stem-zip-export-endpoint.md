---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0048: Dynamic Combined Stem & Lyrics .zip Streaming Endpoint

## Parent Story
- `docs/tickets/STORY-0021-stem-zip-export-and-cleanup.md`

## What to build
Build backend endpoint `GET /api/jobs/{job_id}/export/zip` that streams a dynamic `.zip` archive containing `instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`, and `lyrics.lrc` (if available). Add `📦 Export Stems (.zip)` button to multitrack controls in Stem Studio.

## Acceptance Criteria
- [x] Endpoint streams valid `.zip` containing all 3 stem MP3s and `lyrics.lrc` (if present).
- [x] UI button triggers download cleanly with sanitized song title filename (`{title}_stems.zip`).

## Implementation
- Added `GET /api/jobs/{job_id}/export/zip` (and `/download-all.zip` alias) in `src/api/routes.py` with in-memory dynamic zip streaming.
- Added `#export-stems-zip-btn` in `src/static/index.html` and wired event handling in `src/static/player.js`.
- Verified in `tests/test_track_export_and_cleanup.py` and `tests/test_frontend_routes.py`.

## Blocked by
- None (can start immediately)
