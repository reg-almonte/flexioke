---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: in-review
---

# STORY-0028: Built-in Favorites System & 1-Click Heart Toggles

## Parent Epic
- `docs/tickets/EPIC-0009-playlists-management-and-favorites.md`

## What it delivers
Provides an intuitive 1-click Favorites experience allowing singers and audio producers to bookmark tracks instantly with interactive Heart (♥ / ♡) icons on song cards across Stem Studio, Karaoke Mode, and the Song Catalog modal, synchronized across all active views via a reactive client-side state machine and event bus.

## Acceptance Criteria
- [x] Global client state `window.flexiokeFavoritesSet` initializes on page load and reflects favorite tracks.
- [x] Clicking a Heart icon toggles optimistic UI state immediately and sends the appropriate API call (`POST` or `DELETE /api/playlists/favorites/songs`).
- [x] Toggling a favorite track synchronizes all instances of that song's Heart icon across Stem Studio, Karaoke Mode, and Song Catalog modal without reloading.
- [x] 100% automated test coverage.

## Tasks
- [x] TASK-0059: Reactive Favorites Client State Machine & Global Event Bus
- [x] TASK-0060: Interactive Heart Buttons on Song Cards and Modals

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`

## Implementation
- Branch: `story/STORY-0028-favorites-system-and-heart-toggles`
- Completed TASK-0059 (Client State Machine & Event Bus in `src/static/playlists.js`) and TASK-0060 (Heart Buttons in `src/static/library_queue.js` and `index.html`).
