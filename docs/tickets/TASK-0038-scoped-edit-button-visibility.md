---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0038: Scoped Edit Button Visibility (Stem Studio Only)

## Parent Story
- `docs/tickets/STORY-0016-fixed-sidebar-and-song-catalog-modal.md`

## What to build
Update `SongLibraryManager` card rendering logic to render the "Edit Details / Lyrics" button (`✏`, `.edit-lyrics-btn`) only on the Stem Studio page (Page 1), omitting it completely in Karaoke Mode (Page 2 sidebar and Catalog Modal).

## Acceptance Criteria
- [x] Song Library cards in Stem Studio show `▶ Play`, `➕ Queue`, and `✏ Edit Details/Lyrics`.
- [x] Song Library cards in Karaoke Mode show only `▶ Play` and `➕ Queue`.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0016-fixed-sidebar-and-song-catalog-modal`
- Implemented contextual check (`isStudio`) in `SongLibraryManager.render()` so `.lyrics-btn` is rendered exclusively within `#view-studio` containers.
- Omitted edit button from Karaoke Mode sidebar and `#song-catalog-modal`.
- Automated regression tests added in `tests/test_library_queue_frontend.py` (81/81 tests passing).

