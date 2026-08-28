---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: pending
---

# TASK-0022: Library Cards Artist Subtitle Display & Dual-Field Search Filter

## Parent Story
- `docs/tickets/STORY-0009-song-lyrics-editor-dual-search.md`

## What to build
Update song card templates in `src/static/library_queue.js` and `src/templates/index.html` across Stem Studio and Karaoke Mode to render the song title as the header and artist as the secondary subtitle (defaulting to `"Unknown Artist"` if empty). Update the live search filter to match search queries against both `title` and `artist` strings case-insensitively.

## Acceptance Criteria
- [ ] Stem Studio and Karaoke Mode library cards display Title and Artist subtitle.
- [ ] Unset artist renders as dimmed `"Unknown Artist"`.
- [ ] Search filter dynamically matches songs by either Title or Artist.
- [ ] Displays clear empty state message when no search matches are found.

## Blocked by
- TASK-0019: Model & JobStore Artist Field Extension with Legacy Deserialization
