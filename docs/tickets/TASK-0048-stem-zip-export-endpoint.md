---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0048: Dynamic Combined Stem & Lyrics .zip Streaming Endpoint

## Parent Story
- `docs/tickets/STORY-0021-stem-zip-export-and-cleanup.md`

## What to build
Build backend endpoint `GET /api/jobs/{job_id}/export/zip` that streams a dynamic `.zip` archive containing `instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`, and `lyrics.lrc` (if available). Add `📦 Export Stems (.zip)` button to multitrack controls in Stem Studio.

## Acceptance Criteria
- [ ] Endpoint streams valid `.zip` containing all 3 stem MP3s and `lyrics.lrc` (if present).
- [ ] UI button triggers download cleanly with sanitized song title filename (`{title}_stems.zip`).

## Blocked by
- None (can start immediately)
