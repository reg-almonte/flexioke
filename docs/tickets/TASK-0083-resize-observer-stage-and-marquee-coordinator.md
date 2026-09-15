---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# TASK-0083: ResizeObserver Stage Coordinator & Dynamic Header Marquee

## Parent Story
- `docs/tickets/STORY-0041-responsive-stage-and-adaptive-transport-bar.md`

## What to build
Build the container-aware ResizeObserver coordinator and marquee manager:
- Attach `ResizeObserver` to `#karaoke-stage-container` to monitor real-time bounding width during sidebar dragging or window resizing.
- Dispatch container breakpoint classes (`stage-narrow`, `stage-compact`, `stage-full`) to `#karaoke-stage-container`.
- Trigger recalculation of marquee overflow thresholds in "Now Singing" and "Up Next" headers when stage width changes.

## Acceptance Criteria
- [ ] `ResizeObserver` accurately detects stage width changes and toggles responsive CSS classes.
- [ ] Marquee scrolling in stage header cards recalculates instantly on resize.

## Blocked by
- None (can start immediately).
