---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0039: Expanded Song Catalog Modal with Instant Search, Sorting & 1-Click Actions

## Parent Story
- `docs/tickets/STORY-0016-fixed-sidebar-and-song-catalog-modal.md`

## What to build
Add an Expand button (`⛶` / `↗`) to the Karaoke Song Library header, moving the `N songs` badge to its left. Implement `#song-catalog-modal` with search filter, clear button, sort dropdown (Title A-Z/Z-A, Artist A-Z, Recent), and direct `▶ Play Now` and `➕ Add to Queue` actions. Add `Esc` key and backdrop click dismissal.

## Acceptance Criteria
- [ ] Clicking Expand opens the full-screen Song Catalog Modal.
- [ ] Modal includes real-time search with clear button, sorting dropdown, and full song list.
- [ ] Each song row features `▶ Play Now` and `➕ Add to Queue` buttons.
- [ ] Modal closes cleanly on `Esc`, close button (`✕`), or backdrop click.

## Blocked by
- None (can start immediately in parallel)
