---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# STORY-0027: Backend Playlist Store & REST API Services

## Parent Epic
- `docs/tickets/EPIC-0009-playlists-management-and-favorites.md`

## What it delivers
Provides a robust, thread-safe backend playlist management engine storing playlists in `./data/playlists.json` with in-memory caching, atomic write safety, automatic initialization of the immutable `favorites` system playlist, cascading deletion integrity upon track removal, and a full suite of REST API endpoints.

## Acceptance Criteria
- [ ] Pydantic models validate playlist creation, updates, song additions, and reordering.
- [ ] `./data/playlists.json` is automatically created and bootstrapped with the `favorites` playlist on startup.
- [ ] CRUD endpoints for playlists and playlist songs function with proper error status codes (400 on system playlist mutation, 404 on missing entities, 409 on duplicate additions).
- [ ] Deleting a track via `DELETE /api/jobs/{id}` automatically prunes that track from all playlists.
- [ ] 100% automated test coverage for models, store, manager, and API endpoints.

## Tasks
- [ ] TASK-0057: Playlist Models, JSON Store & Thread-Safe Manager Service
- [ ] TASK-0058: Playlist REST Endpoints & Route Handlers

## Blocked by
- None (can start immediately)
