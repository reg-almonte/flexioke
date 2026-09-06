---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# TASK-0062: Multi-Playlist Selection in Song Details & Lyrics Modal

## Parent Story
- `docs/tickets/STORY-0029-studio-playlists-ui-and-modal-assignment.md`

## What to build
Integrate playlist assignments into `#lyrics-modal`:
- Add a scrollable **"Playlists"** section to `#lyrics-modal` in `src/static/index.html`.
- When opening `#lyrics-modal` for a track, query available playlists and render checkboxes indicating inclusion.
- Toggling a checkbox sends `POST /api/playlists/{id}/songs` or `DELETE /api/playlists/{id}/songs/{song_id}` and shows ephemeral feedback.

## Acceptance Criteria
- [ ] All existing playlists are displayed with correct checked state for the active song.
- [ ] Checking/unchecking updates playlist membership immediately without closing the modal.

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`
