---
status: approved
approved_by: reg
approved_at: 2026-09-01
implementation: pending
---

# STORY-0022: LRCLIB Client Service & Background Separation Pipeline Auto-Sync

## Parent Epic
- `docs/tickets/EPIC-0007-lrclib-lyrics-integration.md`

## What it delivers
Provides an in-process HTTP LRCLIB client module with proxy endpoints and integrates automated synchronized `.lrc` lyric retrieval directly into the background stem separation pipeline upon audio ingestion.

## Acceptance Criteria
- [ ] LRCLIB client connects to `https://lrclib.net/api/` with custom `User-Agent` and SSL validation.
- [ ] Direct `/api/get` lookup with automatic `/api/search` fallback returns synchronized `.lrc` content.
- [ ] Ingesting a known song without existing lyrics automatically writes `lyrics.lrc` during pipeline execution.
- [ ] Network errors, 404s, or rate limits fail gracefully without crashing or stopping separation.

## Tasks
- [ ] TASK-0051: In-Process LRCLIB Client Module & REST Proxy Endpoints
- [ ] TASK-0052: Background Separation Pipeline Lyrics Auto-Sync

## Blocked by
- None (can start immediately)
