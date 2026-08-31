---
status: approved
approved_by: reg
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0016: Top Navigation Bar Tabs (Stem Studio vs Karaoke Mode)

## Parent Story
- `STORY-0007-karaoke-page-synchronized-stage.md`

## What to build
Implement the persistent top-level navigation tabs in `src/static/index.html` allowing users to switch between the Stem Studio layout and the new full-screen Karaoke layout without interrupting or re-mounting active audio players.

## Acceptance Criteria
- [x] Segmented tab bar in header toggles active container views.
- [x] Audio playback continues smoothly across tab transitions.

## Blocked by
- None

## Implementation
- **Branch:** `story/STORY-0007-karaoke-page-synchronized-stage`
- **UI Markup:** Persistent top-level navigation tabs (`#nav-tab-studio`, `#nav-tab-karaoke`) and container views (`#view-stem-studio`, `#view-karaoke`) in `src/static/index.html`.
- **View Logic:** `src/static/app.js` managing view switching without pausing audio playback.
- **Tests:** `tests/test_karaoke_navigation.py` (1 test passing, 43 suite-wide).
