---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Requirements: Version 0.3.0 — Playlists Management & Favorites System

## Problem / Motivation
In Flexioke v0.2.6, users can only access processed songs either through the general Song Library or by manually queueing tracks one by one into the Playback Queue. As a song library grows to dozens or hundreds of tracks:
1. There is no way to group songs into curated collections (e.g., "Rock Anthems", "Duets", "Party 90s", "Warmup Vocals").
2. There is no quick "Favorites / Likes" mechanism to bookmark frequently performed tracks without manual searching.
3. Queueing multiple related songs for a karaoke session requires repetitive individual track additions.
4. Active queues cannot be saved or exported for future replay.

Flexioke v0.3.0 introduces a persistent **Playlists Management System** and a permanent built-in **Favorites Playlist**, enabling users to organize songs into custom collections in Stem Studio and deploy them as sequenced or shuffled queues in Karaoke Mode.

---

## Target Users
- **Karaoke Hosts & Singers:** Want to build custom song sets in advance, toggle favorite songs with 1-click heart buttons, and instantly queue or play full playlists in order or shuffled.
- **Audio Enthusiasts & Rehearsal Vocalists:** Want to categorize multitrack stems by practice routine, vocal range, or genre, and save active multitrack queues as reusable playlists.

---

## Goals
1. **Backend Playlist Storage & CRUD API:**
   - Store playlists in a persistent JSON database (`./data/playlists.json`) managed by a thread-safe `PlaylistManager` service.
   - Support creating, renaming, deleting playlists, reordering tracks, and adding/removing songs.
2. **Permanent Built-in "Favorites" Playlist:**
   - Automatically initialize an immutable `Favorites` playlist (`id: "favorites"`, name: `"Favorites"`) that cannot be deleted or renamed.
   - Provide 1-click Heart (♥ / ♡) toggle buttons across library song cards and modals for instant addition/removal.
3. **Song Details & Lyrics Modal Assignment:**
   - Allow assigning any song to one or multiple playlists directly within `#lyrics-modal`.
4. **Stem Studio Playlists Management UI:**
   - Provide a dedicated Playlists accordion/card in Stem Studio to browse playlists, view track lists, create new playlists, and delete/rename existing playlists.
5. **Karaoke Mode Playlist Queue Actions:**
   - Display playlists in Karaoke Mode with 3 dynamic queue/play options:
     1. **Add to Queue (In Order):** Sequentially appends all playlist songs to the active playback queue.
     2. **Add to Queue (Shuffle / Random):** Shuffles playlist tracks and appends them to the queue.
     3. **Play Now (Replace & Start):** Clears the active queue, loads the first song onto the stage immediately, and enqueues the remainder.
6. **Playlist Metadata & Search:**
   - Display song count and cumulative duration stats (`X songs • Y mins`).
   - Filter/search songs within an opened playlist view.
7. **Save Current Queue as Playlist:**
   - Allow 1-click creation of a new playlist populated from the active Playback Queue.
8. **Cascading Integrity on Deletion:**
   - Deleting a song via `DELETE /api/jobs/{id}` automatically prunes that song ID from all playlists.

---

## Non-Goals (Out of Scope)
- Multi-user authentication, cloud syncing, or user-specific permissions (Flexioke is a single-user / local-network workstation).
- Nested playlists / playlist folders.
- Automatic smart playlists based on rules/genres (all playlist assignments are explicit).
- External Spotify/Apple Music playlist sync (audio stems are local to the Flexioke library).

---

## Functional Requirements

### 1. Data Model & REST Endpoints
- **Playlist Entity Schema:**
  - `id`: Unique string identifier (UUID or `"favorites"` for system playlist).
  - `name`: String title (e.g. `"Pop Hits"`).
  - `description`: Optional text description.
  - `is_system`: Boolean flag (`true` for Favorites, `false` for custom playlists).
  - `song_ids`: Ordered array of job IDs (`List[str]`).
  - `created_at`: ISO 8601 timestamp string.
  - `updated_at`: ISO 8601 timestamp string.
- **REST Endpoints:**
  - `GET /api/playlists`: List all playlists with summary stats (`song_count`, `total_duration_seconds`).
  - `POST /api/playlists`: Create a new custom playlist.
  - `GET /api/playlists/{id}`: Retrieve detailed playlist object including resolved song details.
  - `PUT /api/playlists/{id}`: Update playlist name or description (disallowed for `favorites` name).
  - `DELETE /api/playlists/{id}`: Delete a custom playlist (disallowed for `favorites`).
  - `POST /api/playlists/{id}/songs`: Add a song ID to the playlist (enforcing no duplicate song IDs).
  - `DELETE /api/playlists/{id}/songs/{song_id}`: Remove a song from the playlist.
  - `PUT /api/playlists/{id}/reorder`: Reorder song IDs within a playlist.
  - `POST /api/playlists/from-queue`: Create a new playlist populated from the current queue's job IDs.

### 2. Built-in Favorites System
- System automatically provisions `favorites` playlist if not present in `./data/playlists.json`.
- Song cards in Stem Studio and Karaoke Mode render a quick toggle heart icon:
  - ♡ (Unfavorited): Click sends `POST /api/playlists/favorites/songs` and changes state to filled red ♥.
  - ♥ (Favorited): Click sends `DELETE /api/playlists/favorites/songs/{song_id}` and changes state to empty ♡.
- Real-time client state synchronization across all views when favoriting/unfavoriting.

### 3. Song Details & Lyrics Modal (`#lyrics-modal`) Integration
- Includes a **"Playlists"** section showing checkboxes for all available playlists.
- Checking/unchecking a box immediately adds or removes the active song from that playlist.

### 4. Stem Studio Playlists Management UI
- New dedicated sidebar accordion card **"Playlists"** (`#studio-card-playlists`) with:
  - Header with total playlist count badge and `+ New Playlist` button.
  - List of playlists showing name, song count, duration, and action buttons (View, Edit, Delete).
  - Expanded playlist view with search bar, drag/reorder/delete controls for individual songs, and `▶ Queue All` action.

### 5. Karaoke Mode Playlist Selector & Queue Dispatch
- Dedicated **"Playlists"** accordion card (`#karaoke-card-playlists`) and/or Playlist filter tab in the Song Library.
- Clicking a playlist reveals track previews and a 3-button action cluster:
  - `➕ Queue (In Order)`
  - `🔀 Queue (Shuffle)`
  - `▶ Play Now (Replace)`
- Supports saving the active Karaoke queue as a new playlist via a `💾 Save Queue as Playlist` button.

### 6. Cascading Integrity
- `job_manager.delete_job(job_id)` cascades to `playlist_manager.prune_song_from_all_playlists(job_id)` to ensure no orphaned song references remain.

---

## Acceptance Criteria
- [ ] Users can create, rename, and delete custom playlists via backend API and Stem Studio UI.
- [ ] System prevents deletion or renaming of the built-in `Favorites` playlist.
- [ ] Clicking the Heart (♥ / ♡) icon on any song card toggles favorite status instantly without full page reload.
- [ ] A song can only be added to a playlist once (duplicate additions return 409 or are ignored gracefully).
- [ ] In `#lyrics-modal`, users can check/uncheck playlist assignments for the active song.
- [ ] In Karaoke Mode, users can queue an entire playlist in order, queue in randomized shuffle order, or replace the queue and start playing immediately.
- [ ] Users can save the current playback queue as a new named playlist.
- [ ] Deleting a song from the library automatically removes it from all playlists containing it.
- [ ] All automated unit and integration tests pass without regression.

---

## Constraints & Assumptions
- Backend data persistence uses atomic JSON file writes (`./data/playlists.json`) with thread locking, consistent with `job_store.py`.
- Playlists reference songs strictly by `job_id`.
- Single-instance local execution (no distributed cache or multi-tenant database required).

---

## Open Questions
- None (All core flows and questions clarified during requirements interview).
