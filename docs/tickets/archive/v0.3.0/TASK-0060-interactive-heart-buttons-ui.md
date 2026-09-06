---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: in-review
---

# TASK-0060: Interactive Heart Buttons on Song Cards and Modals

## Parent Story
- `docs/tickets/STORY-0028-favorites-system-and-heart-toggles.md`

## What to build
Render and style 1-click interactive Heart (♥ / ♡) toggle buttons:
- Add heart toggle button to song cards in Stem Studio library (`#studio-library-list`).
- Add heart toggle button to song cards in Karaoke Mode library (`#karaoke-library-list`).
- Add heart toggle button to song rows in the Song Catalog modal (`#catalog-songs-list`).
- Connect click events to `toggleFavorite(songId)` with smooth CSS scale and color transitions.

## Acceptance Criteria
- [x] Favorited songs display a vibrant red filled heart (♥) with appropriate aria-label and tooltip.
- [x] Unfavorited songs display a subtle outline heart (♡) on hover.
- [x] Clicking toggles state instantly without triggering parent card click events.

## Blocked by
- `docs/tickets/TASK-0059-favorites-client-state-machine.md`

## Implementation
- Branch: `story/STORY-0028-favorites-system-and-heart-toggles`
- Rendered 1-click Heart toggle buttons in library cards and Song Catalog modal in `src/static/library_queue.js`.
- Bound `toggleFavorite` handlers with `e.stopPropagation()` and live DOM updates.
- Added tests in `tests/test_favorites_frontend.py`.
