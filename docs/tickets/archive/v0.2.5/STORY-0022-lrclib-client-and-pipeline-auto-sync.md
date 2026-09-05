---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: in-review
---

# STORY-0022: LRCLIB Client Service & Background Separation Pipeline Auto-Sync

## Parent Epic
- `docs/tickets/EPIC-0007-lrclib-lyrics-integration.md`

## What it delivers
Provides an in-process HTTP LRCLIB client module with proxy endpoints and integrates automated synchronized `.lrc` lyric retrieval directly into the background stem separation pipeline upon audio ingestion.

## Acceptance Criteria
- [x] LRCLIB client connects to `https://lrclib.net/api/` with custom `User-Agent` and SSL validation.
- [x] Direct `/api/get` lookup with automatic `/api/search` fallback returns synchronized `.lrc` content.
- [x] Ingesting a known song without existing lyrics automatically writes `lyrics.lrc` during pipeline execution.
- [x] Network errors, 404s, or rate limits fail gracefully without crashing or stopping separation.

## Tasks
- [x] TASK-0051: In-Process LRCLIB Client Module & REST Proxy Endpoints
- [x] TASK-0052: Background Separation Pipeline Lyrics Auto-Sync

## Implementation
- Implemented `src/services/lrclib_client.py` and proxy endpoints `GET /api/lyrics/lrclib/get` & `/search` in `src/api/routes.py`.
- Integrated background lyrics synchronization in `src/services/pipeline.py`.
- Verified in `tests/test_lrclib_client.py`, `tests/test_lrclib_api.py`, and `tests/test_pipeline_and_stems.py`.

## Blocked by
- None (can start immediately)
