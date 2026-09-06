---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: in-review
---

# TASK-0058: Playlist REST Endpoints & Route Handlers

## Parent Story
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`

## What to build
Implement the REST API route handlers for playlists under `/api/playlists` and wire cascading deletion integrity:
- `GET /api/playlists`: Return list of `PlaylistSummary` with calculated `song_count` and `total_duration_seconds`.
- `POST /api/playlists`: Create new custom playlist.
- `GET /api/playlists/{id}`: Return `PlaylistDetail` with resolved `Job` objects (auto-pruning non-existent song IDs).
- `PUT /api/playlists/{id}`: Update playlist name and description (enforce 400 on system playlist rename).
- `DELETE /api/playlists/{id}`: Delete custom playlist (enforce 400 on system playlist delete).
- `POST /api/playlists/{id}/songs`: Add song ID (return 409 if already present, 404 if song does not exist).
- `DELETE /api/playlists/{id}/songs/{song_id}`: Remove song ID from playlist.
- `PUT /api/playlists/{id}/reorder`: Reorder songs in playlist.
- `POST /api/playlists/from-queue`: Create a new playlist from a list of song IDs.
- Integrate `playlist_manager.prune_song_from_all_playlists(job_id)` inside `job_manager.delete_job()` in `routes.py`.

## Acceptance Criteria
- [x] All 9 REST endpoints handle request payloads and return appropriate HTTP status codes (200, 201, 400, 404, 409).
- [x] Integration tests verify route behavior, error handling, and cascading deletion.

## Blocked by
- `docs/tickets/TASK-0057-playlist-models-store-and-manager.md`

## Implementation
- Branch: `story/STORY-0027-backend-playlist-store-and-api`
- Implemented all 9 REST route handlers in `src/api/routes.py` with error code mapping (400, 404, 409).
- Integrated cascading playlist song pruning in `delete_job` endpoint.
- Added comprehensive integration tests in `tests/test_playlist_api.py` (9/9 tests passing).
