---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0012: Interactive Song Library Search & Playback Queue UI with Auto-Advance

## Parent Story
- `STORY-0004-multitrack-web-player-ui.md`

## What to build
Build the frontend Song Library panel with real-time search filtering, song cards with "Play Now" and "Add to Queue" actions, and the Playback Queue panel with track removal and automated auto-advance loading the next song into the multitrack player when playback finishes.

## Acceptance Criteria
- [ ] Song library panel fetches and displays processed songs with metadata.
- [ ] Search input filters library cards in real time.
- [ ] Clicking "Play Now" loads stems into the player; clicking "Add to Queue" appends to the queue list.
- [ ] Queue panel displays active and upcoming songs with remove buttons.
- [ ] When the current song reaches its end, the multitrack player automatically dequeues and begins playing the next song in the queue.

## Blocked by
- TASK-0011: Wavesurfer Multitrack Player with Channel Strip Controls (Mute, Solo, Volume)
- TASK-0009: Playback Queue Service & Playlist State Logic
