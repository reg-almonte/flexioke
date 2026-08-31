---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0045: Persistent Header Notes / Resource Links Scratchpad Modal

## Parent Story
- `docs/tickets/STORY-0019-collapsible-accordions-and-notes-modal.md`

## What to build
Add a `📝 Notes` button to the Stem Studio header toolbar opening `#studio-notes-modal`. Build auto-saving textarea (`localStorage["flexioke_studio_notes"]`) with automatic HTTP/HTTPS link parsing and dismissal via `Esc`, `✕`, or backdrop click.

## Acceptance Criteria
- [ ] Notes modal opens via header button and auto-saves typed content.
- [ ] Embedded URLs render as clickable external links.
- [ ] Dismisses cleanly via `Esc`, close button, or backdrop click.

## Blocked by
- None (can start immediately)
