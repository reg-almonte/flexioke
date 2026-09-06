---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# TASK-0065: Modal Navigation Context & Track Position Counter

## Parent Story
- `docs/tickets/STORY-0031-in-modal-song-navigation.md`

## What to build
Implement in-modal list context tracking and navigation controls:
- Add Previous and Next navigation buttons (`#modal-nav-prev-btn`, `#modal-nav-next-btn`) and a position badge (`#modal-nav-counter-badge`) to `#lyrics-modal` header.
- Pass and store the active song sequence and current index when opening the modal from Stem Studio library, Karaoke library, Song Catalog modal, or Playlist detail view.
- Update modal contents, form fields, and playlist checkboxes when Previous or Next is clicked.
- Manage button disabled states on boundary indices (`index === 0`, `index === list.length - 1`).

## Acceptance Criteria
- [ ] Clicking Previous loads the preceding song in the current view order.
- [ ] Clicking Next loads the succeeding song in the current view order.
- [ ] Badge displays `Track X of Y` matching active position.
- [ ] Boundary buttons disable appropriately.

## Blocked by
- None (can start immediately)
