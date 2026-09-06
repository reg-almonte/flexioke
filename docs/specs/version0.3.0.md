---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# Functional Specification: Version 0.3.0 (Playlists Management & Favorites System)

## Related Requirements
- `docs/requirements/version0.3.0.md`

---

## 1. Overview
This specification details the technical workflows, REST APIs, UI components, state machines, and data validation rules for:
1. **Persistent Backend Playlist Store & REST CRUD Services** (`./data/playlists.json`).
2. **Permanent Built-in Favorites System** with 1-click Heart (♥ / ♡) toggles across all song cards and catalog modals.
3. **Multi-Playlist Assignment** inside the Song Details & Lyrics editor modal (`#lyrics-modal`).
4. **Stem Studio Playlists Management UI** (`#studio-card-playlists`) with track reordering, removal, and stats.
5. **Karaoke Mode Playlist 3-Way Queue Dispatch** (`In Order`, `Shuffle`, `Play Now Replace`) & Queue-to-Playlist saving.
6. **Cascading Deletion Integrity** across all playlist references.

---

## 2. Data Entities & Schemas

### Entity 1: `Playlist`
```json
{
  "id": "favorites",
  "name": "Favorites",
  "description": "Your favorite songs",
  "is_system": true,
  "song_ids": ["job_123", "job_456"],
  "created_at": "2026-09-06T10:00:00Z",
  "updated_at": "2026-09-06T10:00:00Z"
}
```

### Entity 2: `PlaylistSummary` (Response DTO)
```json
{
  "id": "favorites",
  "name": "Favorites",
  "description": "Your favorite songs",
  "is_system": true,
  "song_count": 2,
  "total_duration_seconds": 384.5,
  "created_at": "2026-09-06T10:00:00Z",
  "updated_at": "2026-09-06T10:00:00Z"
}
```

### Entity 3: `PlaylistDetail` (Response DTO)
```json
{
  "id": "favorites",
  "name": "Favorites",
  "description": "Your favorite songs",
  "is_system": true,
  "song_count": 2,
  "total_duration_seconds": 384.5,
  "songs": [
    {
      "id": "job_123",
      "title": "Bohemian Rhapsody",
      "artist": "Queen",
      "status": "completed",
      "duration": 354.0,
      "stems": { ... }
    }
  ],
  "created_at": "2026-09-06T10:00:00Z",
  "updated_at": "2026-09-06T10:00:00Z"
}
```

---

## 3. REST API Specification

| HTTP Method | Path | Request Body | Success Response | Error Codes | Description |
|---|---|---|---|---|---|
| `GET` | `/api/playlists` | — | `List[PlaylistSummary]` | 500 | Lists all playlists with calculated song counts and duration stats. |
| `POST` | `/api/playlists` | `{"name": str, "description": str?}` | `Playlist` (201) | 400, 409 | Creates a new custom playlist. |
| `GET` | `/api/playlists/{id}` | — | `PlaylistDetail` (200) | 404 | Retrieves playlist with resolved song objects (pruning orphaned IDs). |
| `PUT` | `/api/playlists/{id}` | `{"name": str?, "description": str?}` | `Playlist` (200) | 400, 404 | Updates playlist metadata. Rejects renaming of `favorites`. |
| `DELETE` | `/api/playlists/{id}` | — | `{"status": "deleted"}` (200) | 400, 404 | Deletes custom playlist. Rejects deletion of `favorites`. |
| `POST` | `/api/playlists/{id}/songs` | `{"song_id": str}` | `PlaylistDetail` (200) | 400, 404, 409 | Adds a song to the playlist. Returns 409 if already present. |
| `DELETE` | `/api/playlists/{id}/songs/{song_id}`| — | `PlaylistDetail` (200) | 404 | Removes a song from the playlist. |
| `PUT` | `/api/playlists/{id}/reorder` | `{"song_ids": List[str]}` | `PlaylistDetail` (200) | 400, 404 | Updates ordering of songs within the playlist. |
| `POST` | `/api/playlists/from-queue` | `{"name": str, "description": str?, "song_ids": List[str]}` | `PlaylistDetail` (201) | 400 | Creates a new playlist from active queue track IDs. |

---

## 4. Functional Flows

### Flow 1: Built-in Favorites System & 1-Click Heart Toggles
```
[User Clicks Heart Icon on Song Card]
               │
               ▼
   {Is song in favoritesSet?}
      ├── YES ──► [Optimistic UI: Heart -> ♡] ──► [DELETE /api/playlists/favorites/songs/{id}]
      └── NO  ──► [Optimistic UI: Heart -> ♥] ──► [POST /api/playlists/favorites/songs {"song_id": id}]
               │
               ▼
  [Update Global Window Favorites State]
  [Update Heart Icons in Library, Karaoke, Catalog Modals]
  [Update Favorites Playlist Count Badge]
```

### Flow 2: Multi-Playlist Management in `#lyrics-modal`
1. User clicks `✏ Edit Details / Lyrics` on any song card.
2. Modal loads active song metadata and queries `GET /api/playlists`.
3. Modal renders a scrollable checkbox group showing each playlist name, song count, and checked state:
   - Checked if `playlist.song_ids.includes(activeJobId)`.
4. Checking a box triggers `POST /api/playlists/{id}/songs` and displays an inline toast: `"Added to {Playlist Name}"`.
5. Unchecking a box triggers `DELETE /api/playlists/{id}/songs/{activeJobId}` and displays: `"Removed from {Playlist Name}"`.

### Flow 3: Stem Studio Playlists Management Interface (`#studio-card-playlists`)
- **Structure:**
  - Header: `#accordion-header-studio-playlists` with title `"📁 Playlists"`, count badge, and `+ New` button.
  - Body: `#accordion-body-studio-playlists`
    - View A (Playlists Directory): List of playlist cards with name, description, duration badge, song count, `View` button, and `Delete` button (disabled/hidden on Favorites).
    - View B (Playlist Detail / Editor):
      - Header with playlist name, edit button, back button (`← All Playlists`), and `➕ Queue All` button.
      - Search filter input to search within the open playlist.
      - List of songs with index numbers, title/artist, duration, reorder buttons (▲ / ▼), and remove button (`✕`).

### Flow 4: Karaoke Mode 3-Way Playlist Queue Dispatch
- **Structure in `#view-karaoke`:**
  - Sidebar accordion `#accordion-header-karaoke-playlists` with `#accordion-body-karaoke-playlists`.
  - Lists available playlists with song counts and estimated duration.
  - Clicking a playlist opens a lightweight action drawer with 3 primary buttons:
    1. **`➕ Queue All (In Order)`:** Calls `window.flexiokeQueue.addMultiple(playlist.song_ids, false)`.
    2. **`🔀 Queue All (Shuffle)`:** Randomizes array via Fisher-Yates shuffle and appends to queue.
    3. **`▶ Play Now (Replace & Start)`:**
       - Pauses and clears current queue.
       - Dispatches `startPlayback(playlist.song_ids[0])`.
       - Enqueues `playlist.song_ids.slice(1)`.
  - Playback Queue Card (`#accordion-header-karaoke-queue`) adds a `💾 Save Queue as Playlist` button that prompts for a title and calls `POST /api/playlists/from-queue`.

### Flow 5: Cascading Pruning on Song Deletion
1. User clicks `🗑 Delete Track` on a song.
2. Backend endpoint `DELETE /api/jobs/{job_id}` calls `job_manager.delete_job(job_id)`.
3. `job_manager` invokes `playlist_manager.prune_song_from_all_playlists(job_id)`.
4. `playlist_manager` iterates all playlists, removes `job_id` from `song_ids`, updates `updated_at`, and writes `./data/playlists.json` atomically.

---

## 5. Business Rules & Validation
1. **System Playlist Protection:**
   - The `favorites` playlist cannot be deleted (`400 Bad Request: Cannot delete system playlist`).
   - The `favorites` playlist name cannot be changed (`400 Bad Request: Cannot rename system playlist`).
2. **Duplicate Prevention:**
   - A `song_id` can only appear once in a given playlist (`409 Conflict: Song already exists in playlist`).
3. **Orphan Resilience:**
   - When loading a playlist detail (`GET /api/playlists/{id}`), if any `song_id` no longer exists in `job_manager`, the playlist service automatically prunes the ID and saves the cleansed array.
4. **Thread Safety & Durability:**
   - All mutations to `./data/playlists.json` use a thread lock (`threading.Lock`) and atomic file replacement via a temporary file (`./data/playlists.json.tmp` -> `./data/playlists.json`).

---

## 6. Open Questions
- None. All behavior validated against requirements.
