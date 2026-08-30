---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0032: Top Application Header Auto-Hide & Reveal with Top Hover Sensor

## Parent Story
- `docs/tickets/STORY-0013-queue-reordering-and-auto-hiding-navbar.md`

## What to build
Implement an auto-hiding behavior for `#main-header` in the SPA shell. Style the header to smoothly translate off-screen when not focused, and add a top-edge hover sensor bar (`top: 0`) that triggers smooth slide-down into view when the cursor approaches the top of the viewport.

## Acceptance Criteria
- [x] Main header slides off-screen smoothly during active interaction in Karaoke Mode.
- [x] Hovering near the top edge of the viewport smoothly slides the header down into view.
- [x] Navigation remains fully usable and responsive.

## Blocked by
- None (can start immediately in parallel)

## Implementation
- Branch: `story/STORY-0013-queue-reordering-and-auto-hiding-navbar`
- Changes: Added `#top-nav-sensor` and `#app-header` in `index.html`. Added CSS translateY slide-up / slide-down transitions and hover styling in `styles.css`. Implemented `karaoke-active` body class toggle, mouse sensor listeners, and auto-hide scheduling in `app.js`. Added integration tests in `test_karaoke_navigation.py`.

