---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: pending
---

# TASK-0026: Dual Stage Header Layout with CSS Marquee on Overflow

## Parent Story
- `docs/tickets/STORY-0011-simultaneous-stage-header-and-stage-click.md`

## What to build
Update the Karaoke Stage header markup and styles to display "Now Singing: [Title] - [Artist]" on the left and "Up Next: [Next Title] - [Next Artist]" on the right simultaneously in single-line format. Remove the `A-` / `A+` toolbar buttons. Implement dynamic CSS marquee text animation when title/artist strings exceed container dimensions. Display "Up Next: — (Queue Empty)" when the queue is empty.

## Acceptance Criteria
- [ ] Left header shows "Now Singing: [Title] - [Artist]" in one row.
- [ ] Right header shows "Up Next: [Next Title] - [Next Artist]" in one row (or "Up Next: — (Queue Empty)" if queue is empty).
- [ ] Overflowing text automatically marquees smoothly.
- [ ] `A-` / `A+` buttons removed from stage header toolbar.

## Blocked by
- None (can start immediately)
