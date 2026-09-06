---
status: approved
approved_by: reg
approved_at: 2026-09-06
---

# ADR-0010: File-Backed In-Memory Playlist Manager with REST API & Reactive Favorites State Machine

## Context
In Flexioke v0.2.6, songs are presented in a flat library list without the ability to curate playlists or mark favorite songs. Users performing karaoke or rehearsing stems need to organize tracks into themed sets, toggle favorites with 1-click controls, and deploy playlists directly into the playback queue with sequential or shuffled ordering.

## Decision
Adopt **Option 1: File-Backed In-Memory Playlist Manager with REST API & Reactive State Machine**.

### Architectural Architecture & Component Design:

1. **Backend Service (`src/services/playlist_manager.py`):**
   - Implements a singleton `PlaylistManager` class backed by atomic JSON storage at `./data/playlists.json`.
   - In-memory dictionary cache `self._playlists: Dict[str, Playlist]` for zero-latency lookups and updates.
   - Concurrency protection via `threading.RLock()`.
   - Atomic file persistence: writes serialized JSON to a temporary file (`./data/playlists.json.tmp`) and atomically replaces `./data/playlists.json` via `os.replace()`.
   - Automatic Bootstrap: If `./data/playlists.json` is missing or does not contain `favorites`, automatically provisions the immutable system playlist:
     ```json
     {
       "id": "favorites",
       "name": "Favorites",
       "description": "Your favorite songs",
       "is_system": true,
       "song_ids": [],
       "created_at": "...",
       "updated_at": "..."
     }
     ```
   - Cascading Integrity: `job_manager.delete_job(job_id)` calls `playlist_manager.prune_song_from_all_playlists(job_id)` to prevent dangling song IDs.

2. **REST Endpoints (`src/api/routes.py`):**
   - `GET /api/playlists` -> `List[PlaylistSummary]` (with calculated `song_count` and `total_duration_seconds`).
   - `POST /api/playlists` -> Create new custom playlist.
   - `GET /api/playlists/{id}` -> `PlaylistDetail` with resolved song objects (and auto-pruning).
   - `PUT /api/playlists/{id}` -> Update name/description (rejects renaming `favorites` with 400).
   - `DELETE /api/playlists/{id}` -> Delete custom playlist (rejects deleting `favorites` with 400).
   - `POST /api/playlists/{id}/songs` -> Add song ID (returns 409 if already present).
   - `DELETE /api/playlists/{id}/songs/{song_id}` -> Remove song from playlist.
   - `PUT /api/playlists/{id}/reorder` -> Reorder song IDs within playlist.
   - `POST /api/playlists/from-queue` -> Convert active queue tracks into a new playlist.

3. **Frontend Client State Machine (`src/static/playlists.js` / `library_queue.js`):**
   - Global reactive cache: `window.flexiokePlaylists` and `window.flexiokeFavoritesSet = new Set(...)`.
   - Event-driven UI updates via custom DOM events (`flexioke:playlists-updated`, `flexioke:favorites-toggled`).
   - Heart Icon (♥ / ♡) rendering across Stem Studio library cards, Karaoke library cards, and Song Catalog modal with optimistic UI toggling.
   - Multi-playlist checkboxes in `#lyrics-modal` for instant assignment.
   - Dedicated accordions: `#studio-card-playlists` in Stem Studio and `#karaoke-card-playlists` in Karaoke Mode.
   - 3-Way Queue Dispatch in Karaoke Mode: `➕ Queue All (In Order)`, `🔀 Queue All (Shuffle)`, and `▶ Play Now (Replace)`.

## Options Considered

### Option 1: File-Backed In-Memory Playlist Manager with REST API & Reactive State Machine (Chosen)
- **Pros:**
  - 100% architectural alignment with existing Flexioke patterns (`job_store.py`).
  - Zero external database or ORM dependencies.
  - Sub-millisecond response times with crash-resilient atomic file writes.
  - Reactive event-driven frontend synchronizes Heart toggles across all views without page reloads.
- **Cons:**
  - File-based persistence tailored for single-workstation usage (fits the project design).

### Option 2: Embedded SQLite Relational Store with Foreign Key Constraints
- **Pros:**
  - Relational table schemas (`playlists`, `playlist_tracks`) and SQL cascading deletes.
- **Cons:**
  - Introduces a dual persistence paradigm (SQLite alongside existing JSON stores and `.lrc` files).
  - Unnecessary schema migration complexity for a local single-user application.

## Consequences
- Clean, reliable playlist management across both Stem Studio and Karaoke Mode.
- Heart toggles update instantaneously across all open tabs and modals.
- Deleting audio tracks cleanly cascades across all playlists without leaving broken references.

## Related
- Functional spec: `docs/specs/version0.3.0.md`
- Requirement: `docs/requirements/version0.3.0.md`
- Supersedes / related ADRs: Extends `docs/design/ADR-0001-stem-separation-player-architecture.md`, `docs/design/ADR-0003-independent-karaoke-page-and-lyrics-overhaul.md`, and `docs/design/ADR-0007-stem-studio-upgrade-and-job-queue.md`.
