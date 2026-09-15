---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# STORY-0041: Container-Aware Responsive Stage & Adaptive Transport Bar

## Parent Epic
- `docs/tickets/EPIC-0013-resizable-sidebar-activity-bar-and-karaoke-ui.md`

## What it delivers
Provides container-aware responsive scaling for the central Karaoke Stage, header banners ("Now Singing" / "Up Next"), and bottom transport controls as the sidebar is resized, ensuring controls remain neatly organized and prioritized without visual clutter or awkward wrapping.

## Acceptance Criteria
- [ ] Main stage dynamically occupies available viewport width as the sidebar expands, shrinks, or collapses.
- [ ] Dual header marquee banners recalculate container bounding boxes in real-time.
- [ ] Transport bar buttons adapt responsively across container breakpoints (>= 640px full, 480–639px compact, < 480px minimal).
- [ ] Primary controls (Play/Pause, Restart, Volume, Lead Vocal) remain accessible across all widths.
- [ ] Vocal button labels collapse to compact chips on narrow widths.

## Tasks
- [ ] TASK-0083: ResizeObserver Stage Coordinator & Dynamic Header Marquee
- [ ] TASK-0084: Adaptive Transport Bar & Priority Control Overflow

## Blocked by
- `STORY-0040`
