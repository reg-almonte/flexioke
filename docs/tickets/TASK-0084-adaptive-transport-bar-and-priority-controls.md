---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# TASK-0084: Adaptive Transport Bar & Priority Control Overflow

## Parent Story
- `docs/tickets/STORY-0041-responsive-stage-and-adaptive-transport-bar.md`

## What to build
Refactor bottom transport bar layout and button states for container responsiveness:
- Update CSS styling and DOM structure of `#karaoke-transport-bar` to respond to stage container classes.
- Implement responsive label collapsing on Lead Vocal and Backing Vocal toggle buttons (collapses text to icon chips on narrow widths).
- Prioritize Play/Pause, Restart, Volume hover slider, and Lead Vocal toggle; compact secondary buttons (Settings gear, Timecode mode toggle, Fullscreen button) into a compact icon group or overflow menu on narrow screens (< 480px).

## Acceptance Criteria
- [ ] Transport bar adjusts smoothly across wide, compact, and narrow container widths without overflowing or line-wrapping.
- [ ] Primary controls remain prominent and clickable at all times.
- [ ] Vocal buttons collapse text labels to compact chips cleanly.

## Blocked by
- `TASK-0083`
