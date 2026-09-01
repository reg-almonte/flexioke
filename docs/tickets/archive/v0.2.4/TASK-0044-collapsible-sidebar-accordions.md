---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: in-review
---

# TASK-0044: Collapsible Sidebar Accordions with LocalStorage State

## Parent Story
- `docs/tickets/STORY-0019-collapsible-accordions-and-notes-modal.md`

## What to build
Add collapsible accordion header wrappers with transition chevrons (`▾` / `▸`) to `#studio-card-add-song`, `#studio-card-library`, and `#studio-card-queue`. Bind click events to toggle body height/visibility and persist states in `localStorage["flexioke_studio_accordions"]`.

## Acceptance Criteria
- [x] Clicking accordion headers collapses and expands card bodies smoothly.
- [x] Collapsed states persist across browser reloads.

## Implementation
- Added `#accordion-header-<section>`, `#accordion-body-<section>`, and animated chevron spans to `src/static/index.html`.
- Implemented accordion state manager in `src/static/app.js` with `localStorage["flexioke_studio_accordions"]` persistence.
- Verified in `tests/test_frontend_routes.py`.

## Blocked by
- None (can start immediately)
