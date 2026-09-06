---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# STORY-0030: Karaoke Mode Playlist Ingestion, 3-Way Queue Dispatch & Queue Saving

## Parent Epic
- `docs/tickets/EPIC-0009-playlists-management-and-favorites.md`

## What it delivers
Provides seamless playlist integration for live karaoke performances: browse playlists in Karaoke Mode, dispatch playlists into the active Playback Queue via 3 modes (`➕ Queue (In Order)`, `🔀 Queue (Shuffle)`, and `▶ Play Now (Replace)`), and convert the active live queue into a newly saved playlist with one click.

## Acceptance Criteria
- [ ] Users can browse playlists and view track previews in Karaoke Mode.
- [ ] Users can queue all songs in sequential order or randomized shuffle order without wiping the existing queue.
- [ ] Users can select "Play Now (Replace)" to clear the active queue and immediately begin playing the playlist from track 1.
- [ ] Users can save the active Karaoke playback queue as a new named playlist via `POST /api/playlists/from-queue`.
- [ ] 100% automated test coverage.

## Tasks
- [ ] TASK-0063: Karaoke Mode Playlists Accordion & 3-Way Queue Dispatch Engine
- [ ] TASK-0064: Save Active Playback Queue as Playlist Action

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`
