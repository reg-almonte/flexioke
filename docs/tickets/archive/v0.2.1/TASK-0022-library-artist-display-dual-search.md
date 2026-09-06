---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: in-review
---

# TASK-0022: Library Cards Artist Subtitle Display & Dual-Field Search Filter

## Parent Story
- `docs/tickets/STORY-0009-song-lyrics-editor-dual-search.md`

## What to build
Update song card templates in `src/static/library_queue.js` and `src/templates/index.html` across Stem Studio and Karaoke Mode to render the song title as the header and artist as the secondary subtitle (defaulting to `"Unknown Artist"` if empty). Update the live search filter to match search queries against both `title` and `artist` strings case-insensitively.

## Acceptance Criteria
- [x] Stem Studio and Karaoke Mode library cards display Title and Artist subtitle.
- [x] Unset artist renders as dimmed `"Unknown Artist"`.
- [x] Search filter dynamically matches songs by either Title or Artist.
- [x] Displays clear empty state message when no search matches are found.

## Blocked by
- TASK-0019: Model & JobStore Artist Field Extension with Legacy Deserialization

## Implementation
- **Branch:** `story/STORY-0009-song-lyrics-editor-dual-search`
- **Changes:**
  - Updated `createJobCard` in `src/static/library_queue.js` to render the artist subtitle (with dimmed `"Unknown Artist"` fallback) on all library cards across Stem Studio and Karaoke Mode.
  - Updated search input placeholders in `src/static/index.html` to `"Search by song title or artist..."`.
  - Added unit and frontend tests in `tests/test_library_queue_frontend.py`.

