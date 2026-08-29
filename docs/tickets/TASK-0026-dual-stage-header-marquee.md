---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0026: Dual Stage Header Layout with CSS Marquee on Overflow

## Parent Story
- `docs/tickets/STORY-0011-simultaneous-stage-header-and-stage-click.md`

## What to build
Update the Karaoke Stage header markup and styles to display "Now Singing: [Title] - [Artist]" on the left and "Up Next: [Next Title] - [Next Artist]" on the right simultaneously in single-line format. Remove the `A-` / `A+` toolbar buttons. Implement dynamic CSS marquee text animation when title/artist strings exceed container dimensions. Display "Up Next: — (Queue Empty)" when the queue is empty.

## Acceptance Criteria
- [x] Left header shows "Now Singing: [Title] - [Artist]" in one row.
- [x] Right header shows "Up Next: [Next Title] - [Next Artist]" in one row (or "Up Next: — (Queue Empty)" if queue is empty).
- [x] Overflowing text automatically marquees smoothly.
- [x] `A-` / `A+` buttons removed from stage header toolbar.

## Blocked by
- None (can start immediately)

## Implementation
- Branch: `story/STORY-0011-simultaneous-stage-header-and-stage-click`
- Changes: Dual header markup in `index.html`, marquee animation CSS rules in `styles.css`, header state coordination in `karaoke.js`, and comprehensive integration tests in `tests/test_karaoke_stage.py`.

