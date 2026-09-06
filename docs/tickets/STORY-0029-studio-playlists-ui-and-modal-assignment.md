---
status: approved
approved_by: reg
approved_at: 2026-09-06
implementation: pending
---

# STORY-0029: Stem Studio Playlists Management UI & Song Modal Assignment

## Parent Epic
- `docs/tickets/EPIC-0009-playlists-management-and-favorites.md`

## What it delivers
Provides complete playlist curation controls in Stem Studio via a dedicated collapsible sidebar card (`#studio-card-playlists`) for creating, viewing, searching within, and editing playlists, alongside a multi-playlist selector inside the Song Details & Lyrics modal (`#lyrics-modal`) for fast playlist assignments.

## Acceptance Criteria
- [ ] Users can browse playlists with stats, create new playlists, and delete custom playlists in Stem Studio.
- [ ] Users can inspect a playlist's tracks, search within the playlist, reorder songs with up/down arrows, and remove tracks.
- [ ] In `#lyrics-modal`, users can check/uncheck playlists to add or remove the song dynamically.
- [ ] 100% automated test coverage.

## Tasks
- [ ] TASK-0061: Stem Studio Playlists Accordion & Detail Editor
- [ ] TASK-0062: Multi-Playlist Selection in Song Details & Lyrics Modal

## Blocked by
- `docs/tickets/STORY-0027-backend-playlist-store-and-api.md`
