---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# STORY-0040: VS Code-Style Activity Bar & Resizable Side Panel

## Parent Epic
- `docs/tickets/EPIC-0013-resizable-sidebar-activity-bar-and-karaoke-ui.md`

## What it delivers
Transforms the windowed Karaoke Mode sidebar from vertically stacked accordion cards into a sleek, VS Code-inspired two-panel workspace featuring a 48px left Activity Bar with dynamic count badges, full-height tabbed views for Queue, Playlists, and Library, and a smooth draggable splitter divider with double-click reset and keyboard collapse shortcuts.

## Acceptance Criteria
- [ ] 48px left Activity Bar renders 3 tab icons (Queue, Playlists, Library) with live numeric count badges.
- [ ] Clicking a tab displays that view at 100% full panel height.
- [ ] Clicking the active tab collapses the panel to the Activity Bar only; clicking an inactive tab expands it.
- [ ] Vertical splitter handle allows smooth horizontal dragging between 48px and 50% viewport width.
- [ ] Double-clicking the splitter handle instantly resets width to default 320px.
- [ ] `Ctrl+B` / `Cmd+B` / `Alt+S` toggles sidebar collapse/expand.
- [ ] Sidebar width, active tab, and collapsed state persist in `localStorage` across page reloads.

## Tasks
- [ ] TASK-0081: Activity Bar Navigation & Tab View Controller
- [ ] TASK-0082: PointerEvent Splitter Controller & Persistence

## Blocked by
- None (can start immediately).
