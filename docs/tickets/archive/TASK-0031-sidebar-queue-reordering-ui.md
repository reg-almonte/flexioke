---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0031: Karaoke Sidebar Reorganization (Queue on Top) with Reordering Controls

## Parent Story
- `docs/tickets/STORY-0013-queue-reordering-and-auto-hiding-navbar.md`

## What to build
Reorder the Karaoke Mode sidebar layout so the Playback Queue container is at the top and the Song Library is below. Add `▲` and `▼` buttons to each queued track card in the UI. Wire up clicks to call `POST /api/queue/reorder` and update the local queue list. When the track at index 0 changes, ensure the "Up Next" stage header updates immediately.

## Acceptance Criteria
- [x] Playback Queue is positioned above the Song Library in the Karaoke Mode sidebar.
- [x] Each queued song item displays `▲` and `▼` buttons (disabled at top/bottom boundaries).
- [x] Clicking `▲` or `▼` reorders the queue in real-time.
- [x] Reordering the top queue item immediately updates the "Up Next" header text.

## Blocked by
- `docs/tickets/TASK-0030-backend-queue-reorder-endpoint.md`

## Implementation
- Branch: `story/STORY-0013-queue-reordering-and-auto-hiding-navbar`
- Changes: Reordered `#view-karaoke` sidebar in `index.html` to place Playback Queue at the top and Song Library below. Added `reorderItem()` and `▲`/`▼` reordering controls with boundary disabling in `library_queue.js`, emitting `flexioke:queue-updated` to keep the stage header in sync. Added integration tests in `test_library_queue_frontend.py`.

