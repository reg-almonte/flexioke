---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# TASK-0063: Karaoke Mode Playlists Accordion & 3-Way Queue Dispatch Engine

## Parent Story
- `docs/tickets/STORY-0030-karaoke-playlist-dispatch-and-queue-save.md`

## What to build
Implement Karaoke Mode playlist browsing and queue dispatching:
- Add collapsible sidebar card `#karaoke-card-playlists` in `src/static/index.html` under `#view-karaoke`.
- Render playlist items with song count, duration, and expand trigger.
- Implement 3 dispatch actions for a selected playlist:
  1. `➕ Queue All (In Order)`: Append songs sequentially to `window.flexiokeQueue`.
  2. `🔀 Queue All (Shuffle)`: Randomize song list and append to queue.
  3. `▶ Play Now (Replace)`: Stop current track, clear queue, play first track, and enqueue remainder.

## Acceptance Criteria
- [ ] Sequential queueing appends all tracks in original playlist order.
- [ ] Shuffled queueing appends tracks in randomized order.
- [ ] Replace & Play Now starts playback of first track immediately.

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`
