---
status: approved
approved_by: reg
approved_at: 2026-08-29
implementation: in-review
---

# TASK-0030: Backend Queue Reordering Endpoint (POST /api/queue/reorder)

## Parent Story
- `docs/tickets/STORY-0013-queue-reordering-and-auto-hiding-navbar.md`

## What to build
Implement `reorder_queue(queue_id: str, direction: str)` in the backend queue manager with thread safety. Expose `POST /api/queue/reorder` accepting `{ queue_id, direction: "up" | "down" }` and returning the updated `QueueResponse`. Validate bounds and reject invalid queue IDs with HTTP 400.

## Acceptance Criteria
- [x] `POST /api/queue/reorder` with `direction: "up"` swaps target item with preceding item.
- [x] `POST /api/queue/reorder` with `direction: "down"` swaps target item with subsequent item.
- [x] Out-of-bounds requests and missing queue IDs return HTTP 400.
- [x] Returns refreshed queue state atomically under thread lock.

## Blocked by
- None (can start immediately)

## Implementation
- Branch: `story/STORY-0013-queue-reordering-and-auto-hiding-navbar`
- Changes: Added `QueueReorderRequest` model in `models.py`, implemented atomic thread-safe `reorder_queue()` in `QueueManager` (`queue_manager.py`), exposed `POST /api/queue/reorder` in `routes.py`, and added unit tests in `test_queue_service.py`.

