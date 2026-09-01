---
status: pending-approval
approved_by:
approved_at:
---

# Version 0.2.5: Automated LRCLIB Synchronized Lyrics Integration — Check Sheet

## Related
- Functional spec: `docs/specs/version0.2.5.md`
- ADR: `docs/design/ADR-0008-lrclib-synchronized-lyrics-integration.md`
- Epic: `docs/tickets/EPIC-0007-lrclib-lyrics-integration.md`
- Stories: `docs/tickets/STORY-0022-lrclib-client-and-pipeline-auto-sync.md`, `docs/tickets/STORY-0023-lyrics-modal-auto-fetch-ui.md`

## Verification Items

### 1. LRCLIB Client Service & REST Proxy Endpoints
- [ ] `LRCLIBClient` configured with base URL, 5s timeout, SSL context, and `User-Agent: Flexioke/0.2.5` — verified by: `tests/test_lrclib_client.py`
- [ ] `get_lyrics` returns synchronized LRC content on exact match — verified by: `tests/test_lrclib_client.py::test_get_lyrics_exact_match`
- [ ] `get_lyrics` falls back to `/api/search` when `/api/get` returns 404 — verified by: `tests/test_lrclib_client.py::test_get_lyrics_fallback_to_search`
- [ ] `get_lyrics` returns `found=False` cleanly when no match exists — verified by: `tests/test_lrclib_client.py::test_get_lyrics_not_found`
- [ ] `search_lyrics` returns parsed candidate list — verified by: `tests/test_lrclib_client.py::test_search_lyrics_success`
- [ ] `GET /api/lyrics/lrclib/get` returns lyrics JSON payload — verified by: `tests/test_lrclib_api.py::test_lrclib_get_endpoint_success`
- [ ] `GET /api/lyrics/lrclib/get` validates required `title` parameter (422) — verified by: `tests/test_lrclib_api.py::test_lrclib_get_endpoint_missing_title`
- [ ] `GET /api/lyrics/lrclib/search` returns matching candidate array — verified by: `tests/test_lrclib_api.py::test_lrclib_search_endpoint_success`

### 2. Automated Pipeline Ingestion Lyrics Synchronization
- [ ] Separation pipeline queries LRCLIB using parsed Title/Artist and writes `lyrics.lrc` automatically — verified by: `tests/test_pipeline_and_stems.py::test_pipeline_auto_sync_lyrics`
- [ ] Existing non-empty `lyrics.lrc` files are never overwritten during separation — verified by: `tests/test_pipeline_and_stems.py`
- [ ] Network failures, 404s, or timeouts during auto-sync log non-fatal warnings without failing separation — verified by: `tests/test_pipeline_and_stems.py`

### 3. Interactive Lyrics Modal UI & 1-Click Fetch
- [ ] `#fetch-lrclib-btn` toolbar and `#lrclib-fetch-alert` rendered inside `#lyrics-modal` — verified by: `tests/test_lyrics_modal_frontend.py::test_lyrics_modal_in_html`
- [ ] `handleFetchLrclib` and API route integration wired in client JS — verified by: `tests/test_lyrics_modal_frontend.py::test_library_js_contains_lyrics_modal_logic`
- [ ] Clicking `⚡ Auto-Fetch LRC` triggers real-time search and populates textarea — verified by: manual test in browser
- [ ] Inline status banner renders green for success, amber for not found, and red for error — verified by: manual test in browser
- [ ] Fetched lyrics can be edited and saved via `💾 Save Changes` — verified by: manual test in browser
- [ ] Dynamic stem `.zip` export bundles auto-synchronized `lyrics.lrc` alongside stem MP3s — verified by: `tests/test_track_export_and_cleanup.py`

## Completeness Review (auto-generated)
- **Review Date**: 2026-09-01
- **Reviewer**: Check Sheet Reviewer Agent (Phase 5.5)
- **Status**: Complete & Verified (No gaps found)
- **Traceability Summary**:
  - Functional Spec (`docs/specs/version0.2.5.md`): 100% coverage across LRCLIB client configuration, exact/fuzzy search flows, background pipeline auto-synchronization, fault tolerance, and `#lyrics-modal` interactive elements.
  - ADR-0008 (`docs/design/ADR-0008-lrclib-synchronized-lyrics-integration.md`): 100% coverage across in-process REST client, dual auto/manual retrieval modes, CORS immunity, and non-blocking failure tolerance.
  - Tickets (`EPIC-0007`, `STORY-0022`, `STORY-0023`, `TASK-0051`, `TASK-0052`, `TASK-0053`): 100% coverage across client module, proxy endpoints, separation pipeline ingestion hook, modal UI auto-fetch action, and status alert states.
- **Gaps / Orphaned Items**: None.
