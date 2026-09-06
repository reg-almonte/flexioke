---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# TASK-0064: Save Active Playback Queue as Playlist Action

## Parent Story
- `docs/tickets/STORY-0030-karaoke-playlist-dispatch-and-queue-save.md`

## What to build
Implement the Queue-to-Playlist feature:
- Add a `💾 Save Queue as Playlist` button to the Playback Queue card header in both Stem Studio and Karaoke Mode.
- On click, prompt user for a playlist name (and optional description).
- Call `POST /api/playlists/from-queue` with active queue track IDs.
- Refresh playlists across all active views and display a success notification.

## Acceptance Criteria
- [ ] Button disabled or hidden when the active playback queue is empty.
- [ ] Submitting creates the playlist with the exact songs currently in the queue.
- [ ] Toast notification confirms creation and newly created playlist appears in directory.

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`
