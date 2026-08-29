---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: pending
---

# TASK-0030: Backend Queue Reordering Endpoint (POST /api/queue/reorder)

## Parent Story
- `docs/tickets/STORY-0013-queue-reordering-and-auto-hiding-navbar.md`

## What to build
Implement `reorder_queue(queue_id: str, direction: str)` in the backend queue manager with thread safety. Expose `POST /api/queue/reorder` accepting `{ queue_id, direction: "up" | "down" }` and returning the updated `QueueResponse`. Validate bounds and reject invalid queue IDs with HTTP 400.

## Acceptance Criteria
- [ ] `POST /api/queue/reorder` with `direction: "up"` swaps target item with preceding item.
- [ ] `POST /api/queue/reorder` with `direction: "down"` swaps target item with subsequent item.
- [ ] Out-of-bounds requests and missing queue IDs return HTTP 400.
- [ ] Returns refreshed queue state atomically under thread lock.

## Blocked by
- None (can start immediately)
