---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: in-review
---

# TASK-0051: In-Process LRCLIB Client Module & REST Proxy Endpoints

## Parent Story
- `docs/tickets/STORY-0022-lrclib-client-and-pipeline-auto-sync.md`

## What to build
Build backend LRCLIB client in `src/services/lrclib_client.py` using standard `urllib` + `certifi` SSL context and custom `User-Agent`. Expose proxy endpoints `GET /api/lyrics/lrclib/get` (exact lookup with fuzzy search fallback) and `GET /api/lyrics/lrclib/search` in `src/api/routes.py`.

## Acceptance Criteria
- [x] `lrclib_client.get_lyrics(title, artist, duration)` queries LRCLIB and returns synchronized lyrics.
- [x] Endpoints `/api/lyrics/lrclib/get` and `/api/lyrics/lrclib/search` return standardized JSON responses.
- [x] Handles 404, timeouts, and network disconnects gracefully without exceptions.

## Implementation
- Created `src/services/lrclib_client.py` with `LRCLIBClient` handling `get_lyrics` and `search_lyrics` with fallback.
- Added `GET /api/lyrics/lrclib/get` and `GET /api/lyrics/lrclib/search` in `src/api/routes.py`.
- Verified in `tests/test_lrclib_client.py` and `tests/test_lrclib_api.py`.

## Blocked by
- None (can start immediately)
