---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# TASK-0061: Stem Studio Playlists Accordion & Detail Editor

## Parent Story
- `docs/tickets/STORY-0029-studio-playlists-ui-and-modal-assignment.md`

## What to build
Implement the Stem Studio Playlists UI component:
- Add collapsible sidebar card `#studio-card-playlists` in `src/static/index.html`.
- Render Playlists Directory view showing all playlists, song count badges, and cumulative duration.
- Add `+ New Playlist` modal or inline creation prompt calling `POST /api/playlists`.
- Implement Playlist Detail view with search input, song list with reorder buttons (▲ / ▼), remove buttons (`✕`), and `▶ Queue All` action.
- Add delete button for custom playlists with confirmation prompt.

## Acceptance Criteria
- [ ] Playlists accordion toggles and persists open/closed state.
- [ ] Creating, editing, and deleting playlists functions seamlessly with real-time UI refresh.
- [ ] Reordering tracks sends `PUT /api/playlists/{id}/reorder` and maintains order.

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`
