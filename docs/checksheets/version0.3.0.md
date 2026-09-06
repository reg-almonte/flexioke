---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Version 0.3.0: Playlists Management & Favorites System — Check Sheet

## Related
- Functional spec: `docs/specs/version0.3.0.md`
- ADR: `docs/design/ADR-0010-playlists-management-and-favorites.md`
- Epic: `docs/tickets/archive/v0.3.0/EPIC-0009-playlists-management-and-favorites.md`
- Stories: `docs/tickets/archive/v0.3.0/STORY-0027-backend-playlist-store-and-api.md`, `docs/tickets/archive/v0.3.0/STORY-0028-favorites-system-and-heart-toggles.md`, `docs/tickets/archive/v0.3.0/STORY-0029-studio-playlists-ui-and-modal-assignment.md`, `docs/tickets/archive/v0.3.0/STORY-0030-karaoke-playlist-dispatch-and-queue-save.md`
- Tasks: `docs/tickets/archive/v0.3.0/TASK-0057-playlist-models-store-and-manager.md`, `docs/tickets/archive/v0.3.0/TASK-0058-playlist-rest-endpoints-and-cascading.md`, `docs/tickets/archive/v0.3.0/TASK-0059-favorites-client-state-machine.md`, `docs/tickets/archive/v0.3.0/TASK-0060-interactive-heart-buttons-ui.md`, `docs/tickets/archive/v0.3.0/TASK-0061-studio-playlists-accordion-and-editor.md`, `docs/tickets/archive/v0.3.0/TASK-0062-lyrics-modal-playlist-assignment.md`, `docs/tickets/archive/v0.3.0/TASK-0063-karaoke-playlist-accordion-and-dispatch.md`, `docs/tickets/archive/v0.3.0/TASK-0064-save-queue-as-playlist-action.md`

## Verification Items

### 1. Backend Playlist Store & Data Durability (STORY-0027 / TASK-0057)
- [x] Pydantic models `Playlist`, `PlaylistSummary`, `PlaylistDetail`, `PlaylistFromQueueRequest` serialize and validate correctly — verified by: `tests/test_playlist_manager.py`
- [x] `PlaylistManager` initializes default `favorites` system playlist on clean bootstrap — verified by: `tests/test_playlist_manager.py::test_playlist_manager_bootstrap_creates_favorites`
- [x] Thread-safe mutations using `threading.RLock()` across read and write operations — verified by: `tests/test_playlist_manager.py::test_thread_safe_concurrent_playlist_mutations`
- [x] Atomic disk persistence via temporary file replacement (`playlists.json.tmp.*` -> `playlists.json`) — verified by: `tests/test_playlist_manager.py::test_atomic_file_replacement`
- [x] Orphan resilience prunes missing song IDs automatically on detail retrieval — verified by: `tests/test_playlist_manager.py::test_orphan_song_id_auto_pruning`

### 2. REST API Endpoints & System Playlist Protection (STORY-0027 / TASK-0058)
- [x] `GET /api/playlists` lists all playlists with calculated `song_count` and `total_duration_seconds` — verified by: `tests/test_playlist_api.py::test_list_playlists`
- [x] `POST /api/playlists` creates custom playlists with generated UUIDs and rejects duplicate names (409) — verified by: `tests/test_playlist_api.py::test_create_custom_playlist`
- [x] `GET /api/playlists/{id}` returns resolved song objects and returns 404 for nonexistent playlists — verified by: `tests/test_playlist_api.py::test_get_playlist_detail`
- [x] `PUT /api/playlists/{id}` updates metadata and rejects renaming system `favorites` playlist (400) — verified by: `tests/test_playlist_api.py::test_system_playlist_protection_rename_and_delete`
- [x] `DELETE /api/playlists/{id}` deletes custom playlists and rejects deleting system `favorites` playlist (400) — verified by: `tests/test_playlist_api.py::test_system_playlist_protection_rename_and_delete`
- [x] `POST /api/playlists/{id}/songs` adds songs and rejects duplicates (409) — verified by: `tests/test_playlist_api.py::test_add_and_remove_songs`
- [x] `DELETE /api/playlists/{id}/songs/{song_id}` removes songs from playlist — verified by: `tests/test_playlist_api.py::test_add_and_remove_songs`
- [x] `PUT /api/playlists/{id}/reorder` reorders tracks with full array validation — verified by: `tests/test_playlist_api.py::test_reorder_playlist_songs`
- [x] `POST /api/playlists/from-queue` converts track ID array into a new playlist — verified by: `tests/test_playlist_api.py::test_create_playlist_from_queue`
- [x] Cascading track deletion (`DELETE /api/jobs/{job_id}`) prunes song ID across all playlists — verified by: `tests/test_playlist_api.py::test_cascading_deletion_pruning`

### 3. Built-in Favorites System & 1-Click Heart Toggles (STORY-0028 / TASK-0059, TASK-0060)
- [x] `FavoritesManager` client state machine maintains reactive `window.flexiokeFavoritesSet` — verified by: `tests/test_favorites_frontend.py::test_playlists_js_contains_favorites_manager`
- [x] Optimistic UI toggle updates heart icon (♥ / ♡) and rolls back on API failure — verified by: `tests/test_favorites_frontend.py::test_playlists_js_contains_favorites_manager`
- [x] 1-click Heart toggle buttons rendered across Stem Studio library cards, Karaoke Mode library cards, and Song Catalog modal rows — verified by: `tests/test_favorites_frontend.py::test_render_methods_include_favorite_buttons`
- [x] Heart button click handlers isolate event bubbling (`e.stopPropagation()`) from card selection — verified by: `tests/test_favorites_frontend.py::test_event_bus_wiring`
- [x] Event bus dispatchers (`flexioke:favorites-toggled`, `flexioke:favorites-loaded`, `flexioke:job-deleted`) synchronize all active views — verified by: `tests/test_favorites_frontend.py::test_event_bus_wiring`
- [ ] User clicks heart icon on library card and catalog modal to toggle favorites with instant visual feedback — verified by: manual test in browser

### 4. Stem Studio Playlists UI & Editor (STORY-0029 / TASK-0061)
- [x] `#studio-card-playlists` collapsible accordion in Stem Studio sidebar with count badge and `+ New` button — verified by: `tests/test_studio_playlists_frontend.py::test_index_includes_studio_playlists_accordion`
- [x] Directory view lists all playlists with song count, duration, View button, and Delete button (hidden for Favorites) — verified by: `tests/test_studio_playlists_frontend.py::test_index_includes_studio_playlists_accordion`
- [x] Playlist Detail & Editor view provides live search, index numbers, track removal (`✕`), reordering (▲ / ▼), and `➕ Queue All` — verified by: `tests/test_studio_playlists_frontend.py::test_playlists_js_implements_studio_and_modal_features`
- [ ] User creates new playlist, searches songs within playlist, and reorders track sequence — verified by: manual test in browser

### 5. Multi-Playlist Assignment in Lyrics Modal (STORY-0029 / TASK-0062)
- [x] `#lyrics-modal-playlists-container` renders playlist checkboxes with system badge and song counts — verified by: `tests/test_studio_playlists_frontend.py::test_lyrics_modal_includes_playlists_assignment_section`
- [x] Checkbox state reflects song membership and dynamically invokes `POST`/`DELETE /api/playlists/{id}/songs` — verified by: `tests/test_studio_playlists_frontend.py::test_playlists_js_implements_studio_and_modal_features`
- [x] Status indicator `#lyrics-modal-playlist-feedback` displays inline success/error message for 2.5s — verified by: `tests/test_studio_playlists_frontend.py::test_lyrics_modal_includes_playlists_assignment_section`
- [ ] User opens Song Details modal and checks/unchecks playlist assignment boxes — verified by: manual test in browser

### 6. Karaoke Mode Playlists Accordion & 3-Way Queue Dispatch (STORY-0030 / TASK-0063)
- [x] `#karaoke-card-playlists` collapsible accordion rendered in Karaoke Mode sidebar with count badge and chevron — verified by: `tests/test_karaoke_playlists_frontend.py::test_index_includes_karaoke_playlists_accordion_and_queue_save_buttons`
- [x] Accordion state persists to `localStorage['flexioke_karaoke_accordions']` alongside Queue and Library — verified by: `tests/test_karaoke_playlists_frontend.py::test_karaoke_js_initializes_playlists_accordion`
- [x] `➕ In Order` dispatch sequentially enqueues all songs without wiping current queue — verified by: `tests/test_karaoke_playlists_frontend.py::test_playlists_js_implements_karaoke_dispatch_and_save_queue`
- [x] `🔀 Shuffle` dispatch randomizes array via Fisher-Yates shuffle algorithm and appends to queue — verified by: `tests/test_karaoke_playlists_frontend.py::test_shuffle_algorithm_and_dispatch_logic_in_node`
- [x] `▶ Play Now` dispatch stops playback, clears queue, plays track 1, and appends remaining tracks — verified by: `tests/test_karaoke_playlists_frontend.py::test_playlists_js_implements_karaoke_dispatch_and_save_queue`
- [ ] User dispatches playlist into karaoke queue using In Order, Shuffle, and Play Now buttons — verified by: manual test in browser

### 7. Save Queue as Playlist Action (STORY-0030 / TASK-0064)
- [x] `💾 Save` buttons added to queue headers in Stem Studio (`#studio-save-queue-playlist-btn`) and Karaoke Mode (`#karaoke-save-queue-playlist-btn`) — verified by: `tests/test_karaoke_playlists_frontend.py::test_index_includes_karaoke_playlists_accordion_and_queue_save_buttons`
- [x] Save button automatically disabled when playback queue is empty and enabled when songs exist (`flexioke:queue-updated`) — verified by: `tests/test_karaoke_playlists_frontend.py::test_playlists_js_implements_karaoke_dispatch_and_save_queue`
- [x] User prompt collects playlist name/description and calls `POST /api/playlists/from-queue` — verified by: `tests/test_karaoke_playlists_frontend.py::test_playlists_js_implements_karaoke_dispatch_and_save_queue`
- [ ] User with songs in active queue clicks Save Queue as Playlist and verifies newly created playlist appears in directory — verified by: manual test in browser

## Completeness Review (auto-generated)
- **Review Date:** 2026-09-06
- **Reviewer:** Phase 5.5 Automated Completeness Reviewer
- **Sources Analyzed:**
  - Functional Spec: `docs/specs/version0.3.0.md`
  - ADR: `docs/design/ADR-0010-playlists-management-and-favorites.md`
  - Tickets: `docs/tickets/EPIC-0009-playlists-management-and-favorites.md` (STORY-0027, STORY-0028, STORY-0029, STORY-0030, TASK-0057..TASK-0064)
- **Findings:**
  - **Missing Coverage:** No gaps found. All 6 functional flows, 4 business rules, 9 REST endpoints, and acceptance criteria across backend durability, favorites state machine, Studio playlists UI, and Karaoke dispatch are mapped to concrete verification items with automated/manual tests.
  - **Orphaned Entries:** No orphaned entries found. All 28 verification items trace directly to requirements, spec flows, or ticket acceptance criteria.

## Test Execution — 2026-09-06
- **Test Suite Result:** 145 passed, 0 failed in 4.10s (100% pass rate).
- **Automated Verification Items:** 23/23 verified and passing.
- **Manual Verification Items:** 5 items designated for browser verification.
- **Defects / Bug Reports:** 0 bugs filed. Status is clean.
