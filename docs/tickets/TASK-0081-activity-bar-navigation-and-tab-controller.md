---
status: approved
approved_by: user
approved_at: 2026-09-16
implementation: pending
---

# TASK-0081: Activity Bar Navigation & Tab View Controller

## Parent Story
- `docs/tickets/STORY-0040-vscode-style-activity-bar-and-resizable-panel.md`

## What to build
Build the Activity Bar UI and tabbed panel switching coordinator in Karaoke Mode:
- Construct `#karaoke-activity-bar` container with 3 vertical icon buttons (`#tab-karaoke-queue`, `#tab-karaoke-playlists`, `#tab-karaoke-library`).
- Mount dynamic badge elements (`#badge-karaoke-queue`, `#badge-karaoke-playlists`, `#badge-karaoke-library`) bound to live queue count, playlist count, and total library song count.
- Update `#karaoke-sidebar-content` to display 100% full-height views per tab, transitioning active indicators smoothly.
- Implement active tab re-click toggle logic (collapses panel when active tab is clicked again).

## Acceptance Criteria
- [ ] Activity Bar renders on the left edge with 3 distinct icon tabs and live badges.
- [ ] Clicking tabs seamlessly switches between Queue, Playlists, and Library full-height views.
- [ ] Clicking the active tab toggles panel collapse.

## Blocked by
- None (can start immediately).
