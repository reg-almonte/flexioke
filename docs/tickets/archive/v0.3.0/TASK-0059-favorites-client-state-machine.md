---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: in-review
---

# TASK-0059: Reactive Favorites Client State Machine & Global Event Bus

## Parent Story
- `docs/tickets/STORY-0028-favorites-system-and-heart-toggles.md`

## What to build
Implement client-side state management for favorites in frontend JavaScript:
- Initialize `window.flexiokeFavoritesSet = new Set()` on startup by fetching `GET /api/playlists/favorites`.
- Implement `toggleFavorite(songId)` helper handling optimistic updates, API dispatch (`POST` to add, `DELETE` to remove), and error rollbacks.
- Implement a custom DOM event bus (`flexioke:favorites-toggled`, `flexioke:playlists-updated`) to notify all listening components.

## Acceptance Criteria
- [x] Client state machine maintains an accurate set of favorited song IDs.
- [x] Event listeners update DOM elements when favorites are toggled.
- [x] Automated tests verify frontend logic and API contract.

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`

## Implementation
- Branch: `story/STORY-0028-favorites-system-and-heart-toggles`
- Implemented `FavoritesManager` in `src/static/playlists.js` with optimistic toggling, auto-rollback on error, and custom DOM event bus.
- Added automated tests in `tests/test_favorites_frontend.py`.
