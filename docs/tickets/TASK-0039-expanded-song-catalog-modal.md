---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0039: Expanded Song Catalog Modal with Instant Search, Sorting & 1-Click Actions

## Parent Story
- `docs/tickets/STORY-0016-fixed-sidebar-and-song-catalog-modal.md`

## What to build
Add an Expand button (`⛶` / `↗`) to the Karaoke Song Library header, moving the `N songs` badge to its left. Implement `#song-catalog-modal` with search filter, clear button, sort dropdown (Title A-Z/Z-A, Artist A-Z, Recent), and direct `▶ Play Now` and `➕ Add to Queue` actions. Add `Esc` key and backdrop click dismissal.

## Acceptance Criteria
- [x] Clicking Expand opens the full-screen Song Catalog Modal.
- [x] Modal includes real-time search with clear button, sorting dropdown, and full song list.
- [x] Each song row features `▶ Play Now` and `➕ Add to Queue` buttons.
- [x] Modal closes cleanly on `Esc`, close button (`✕`), or backdrop click.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0016-fixed-sidebar-and-song-catalog-modal`
- Added Expand button (`#open-catalog-modal-btn`) in Karaoke Song Library card header.
- Implemented `#song-catalog-modal` markup in `src/static/index.html` and modal controller in `src/static/library_queue.js`.
- Features real-time search, sorting (`title_asc`, `title_desc`, `artist_asc`, `recent`), instant 1-click `▶ Play Now` and `➕ Add to Queue`, and `Esc` / backdrop dismissal.
- Automated tests added in `tests/test_library_queue_frontend.py` (81/81 tests passing).

