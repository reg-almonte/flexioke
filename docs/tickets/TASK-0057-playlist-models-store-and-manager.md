---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
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
- [ ] Thread-safe operations with zero data loss or file corruption under concurrent mutations.
- [ ] Immutable system playlist protection preventing renaming or deleting `favorites`.
- [ ] Duplicate song additions rejected or handled with conflict checks.
- [ ] Unit tests verify storage, atomic writing, and pruning operations.

## Blocked by
- None (can start immediately)
