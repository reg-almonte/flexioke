---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: pending
---

# TASK-0031: Karaoke Sidebar Reorganization (Queue on Top) with Reordering Controls

## Parent Story
- `docs/tickets/STORY-0013-queue-reordering-and-auto-hiding-navbar.md`

## What to build
Reorder the Karaoke Mode sidebar layout so the Playback Queue container is at the top and the Song Library is below. Add `▲` and `▼` buttons to each queued track card in the UI. Wire up clicks to call `POST /api/queue/reorder` and update the local queue list. When the track at index 0 changes, ensure the "Up Next" stage header updates immediately.

## Acceptance Criteria
- [ ] Playback Queue is positioned above the Song Library in the Karaoke Mode sidebar.
- [ ] Each queued song item displays `▲` and `▼` buttons (disabled at top/bottom boundaries).
- [ ] Clicking `▲` or `▼` reorders the queue in real-time.
- [ ] Reordering the top queue item immediately updates the "Up Next" header text.

## Blocked by
- `docs/tickets/TASK-0030-backend-queue-reorder-endpoint.md`
