---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0044: Collapsible Sidebar Accordions with LocalStorage State

## Parent Story
- `docs/tickets/STORY-0019-collapsible-accordions-and-notes-modal.md`

## What to build
Add collapsible accordion header wrappers with transition chevrons (`▾` / `▸`) to `#studio-card-add-song`, `#studio-card-library`, and `#studio-card-queue`. Bind click events to toggle body height/visibility and persist states in `localStorage["flexioke_studio_accordions"]`.

## Acceptance Criteria
- [ ] Clicking accordion headers collapses and expands card bodies smoothly.
- [ ] Collapsed states persist across browser reloads.

## Blocked by
- None (can start immediately)
