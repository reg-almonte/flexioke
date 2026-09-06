---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: in-review
---

# TASK-0057: Playlist Models, JSON Store & Thread-Safe Manager Service

## Parent Story
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`

## What to build
Implement Pydantic schemas and a thread-safe `PlaylistManager` singleton in the backend service layer:
- Define `Playlist`, `PlaylistSummary`, `PlaylistDetail`, `PlaylistCreate`, `PlaylistUpdate`, `PlaylistSongAdd`, and `PlaylistReorderRequest` models.
- Implement file-backed persistence to `./data/playlists.json` with temporary file atomic replacement (`os.replace`) protected by `threading.RLock`.
- Automatically initialize the immutable `favorites` system playlist (`is_system=True`) if missing.
- Implement methods: `get_all_playlists()`, `create_playlist()`, `get_playlist()`, `update_playlist()`, `delete_playlist()`, `add_song()`, `remove_song()`, `reorder_songs()`, `create_from_queue()`, and `prune_song_from_all_playlists()`.

## Acceptance Criteria
- [x] Thread-safe operations with zero data loss or file corruption under concurrent mutations.
- [x] Immutable system playlist protection preventing renaming or deleting `favorites`.
- [x] Duplicate song additions rejected or handled with conflict checks.
- [x] Unit tests verify storage, atomic writing, and pruning operations.

## Blocked by
- None (can start immediately)

## Implementation
- Branch: `story/STORY-0027-backend-playlist-store-and-api`
- Implemented models in `src/models.py` (`Playlist`, `PlaylistSummary`, `PlaylistDetail`, `PlaylistCreate`, `PlaylistUpdate`, `PlaylistSongAdd`, `PlaylistReorderRequest`, `PlaylistFromQueueRequest`).
- Implemented `PlaylistManager` in `src/services/playlist_manager.py` with atomic write safety, favorites bootstrap, orphan pruning, and cascading pruning.
- Added comprehensive unit tests in `tests/test_playlist_manager.py` (8/8 tests passing).
