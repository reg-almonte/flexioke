---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0012: Interactive Song Library Search & Playback Queue UI with Auto-Advance

## Parent Story
- `STORY-0004-multitrack-web-player-ui.md`

## What to build
Build the frontend Song Library panel with real-time search filtering, song cards with "Play Now" and "Add to Queue" actions, and the Playback Queue panel with track removal and automated auto-advance loading the next song into the multitrack player when playback finishes.

## Acceptance Criteria
- [x] Song library panel fetches and displays processed songs with metadata.
- [x] Search input filters library cards in real time.
- [x] Clicking "Play Now" loads stems into the player; clicking "Add to Queue" appends to the queue list.
- [x] Queue panel displays active and upcoming songs with remove buttons.
- [x] When the current song reaches its end, the multitrack player automatically dequeues and begins playing the next song in the queue.

## Blocked by
- TASK-0011: Wavesurfer Multitrack Player with Channel Strip Controls (Mute, Solo, Volume)
- TASK-0009: Playback Queue Service & Playlist State Logic

## Implementation
- **Branch:** `story/STORY-0004-multitrack-web-player-ui`
- **UI Logic:** `src/static/library_queue.js` (`SongLibraryManager` and `PlaybackQueueManager`) providing debounced real-time library search, song card actions, queue ordering/removal, and automatic track-ended queue auto-advance.
- **Tests:** `tests/test_library_queue_frontend.py` (2 tests passing, 33 suite-wide).
