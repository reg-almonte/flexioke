---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0047: Studio Song Library Default "Recently Added" Sort Order

## Parent Story
- `docs/tickets/STORY-0020-studio-catalog-modal-and-default-sort.md`

## What to build
Configure `SongLibraryManager` so that when rendering within Stem Studio (`#view-stem-studio` / `#studio-library-list`), songs are sorted by `created_at` descending by default (newest songs first), while preserving alphabetical title sorting in Karaoke Mode.

## Acceptance Criteria
- [x] Stem Studio library list renders latest added songs at the top.
- [x] Karaoke Mode library list remains sorted alphabetically by Title.

## Implementation
- Updated `render()` in `src/static/library_queue.js` to sort by `created_at` descending for Stem Studio containers and alphabetical by title for Karaoke mode.
- Verified in `tests/test_library_queue_frontend.py`.

## Blocked by
- None (can start immediately)
