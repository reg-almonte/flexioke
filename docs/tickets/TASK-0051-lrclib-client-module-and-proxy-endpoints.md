---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: pending
---

# TASK-0051: In-Process LRCLIB Client Module & REST Proxy Endpoints

## Parent Story
- `docs/tickets/STORY-0022-lrclib-client-and-pipeline-auto-sync.md`

## What to build
Build backend LRCLIB client in `src/services/lrclib_client.py` using standard `urllib` + `certifi` SSL context and custom `User-Agent`. Expose proxy endpoints `GET /api/lyrics/lrclib/get` (exact lookup with fuzzy search fallback) and `GET /api/lyrics/lrclib/search` in `src/api/routes.py`.

## Acceptance Criteria
- [ ] `lrclib_client.get_lyrics(title, artist, duration)` queries LRCLIB and returns synchronized lyrics.
- [ ] Endpoints `/api/lyrics/lrclib/get` and `/api/lyrics/lrclib/search` return standardized JSON responses.
- [ ] Handles 404, timeouts, and network disconnects gracefully without exceptions.

## Blocked by
- None (can start immediately)
