---
status: approved
approved_by: reg
approved_at: 2026-09-01
---

# Functional Specification: Version 0.2.5 (Automated LRCLIB Synchronized Lyrics Integration)

## 1. Overview
This specification defines the functional behaviors, API contracts, UI components, and background pipeline integrations for automated synchronized lyrics (`.lrc`) fetching from [LRCLIB](https://lrclib.net/). It enables automatic background lyric retrieval during song ingestion/separation as well as 1-click on-demand lyric auto-fetching inside the Song Details & Lyrics editor modal.

---

## 2. Architecture & Data Flow

```
[Audio Ingestion: Upload / URL]
        │
        ▼
[Smart Title/Artist Parser] ─── (Title, Artist)
        │                               │
        ▼                               ▼
[Stage 1 & 2 Stem Separation]     [LRCLIB Client Service]
        │                               │
        │                               ▼
        │                    GET https://lrclib.net/api/get
        │                    (Fallback: /api/search)
        │                               │
        ▼                               ▼
[Final Stems Encoded] ◄────── [lyrics.lrc Saved to Job Dir]
        │
        ▼
[Job Completed: Stems + Synchronized Lyrics Ready for Playback & Karaoke]
```

---

## 3. Detailed Functional Flows

### Flow 1: Backend LRCLIB Service (`src/services/lrclib_client.py`)
- **Client Configuration:**
  - Base URL: `https://lrclib.net/api`
  - Header: `User-Agent: Flexioke/0.2.5 (https://github.com/reg-almonte/flexioke)`
  - SSL verification using `certifi.where()`
  - Request Timeout: 5.0 seconds
- **Core Functions:**
  1. `get_lyrics(track_name: str, artist_name: Optional[str] = None, duration: Optional[float] = None) -> Optional[dict]`:
     - Calls `GET /api/get?track_name={track_name}&artist_name={artist_name}`.
     - If exact match fails (404 / empty), falls back to `search_lyrics(f"{track_name} {artist_name or ''}")` and picks the best matching record with `syncedLyrics` (or first result).
  2. `search_lyrics(query: str) -> List[dict]`:
     - Calls `GET /api/search?q={query}`.
     - Returns parsed list of matches with `id`, `trackName`, `artistName`, `duration`, `syncedLyrics`, and `plainLyrics`.

### Flow 2: Automated Background Pipeline Ingestion Fetch
- During song ingestion (`run_separation_pipeline` in `src/services/pipeline.py`):
  1. Pipeline checks if `./data/jobs/{job_id}/lyrics.lrc` already exists. If present and non-empty, skips fetching to preserve existing custom lyrics.
  2. If missing or empty:
     - Extracts job `title` and `artist`.
     - Calls `lrclib_client.get_lyrics(job.title, job.artist, job.duration_seconds)`.
     - If `syncedLyrics` (or `plainLyrics`) is found:
       - Atomically writes to `./data/jobs/{job_id}/lyrics.lrc`.
       - Logs info: `[pipeline] Automatically synchronized lyrics from LRCLIB for {title}`.
  3. **Fault Tolerance:** Any HTTP error, timeout, or empty response is logged as a non-fatal warning; separation pipeline proceeds without interruption.

### Flow 3: Interactive 1-Click Auto-Fetch in Lyrics Modal (`#lyrics-modal`)
- **Backend Proxy Endpoints:**
  - `GET /api/lyrics/lrclib/get?title={title}&artist={artist}`: Calls `lrclib_client.get_lyrics()` and returns `{ "found": bool, "lyrics": str, "has_timestamps": bool, "track_name": str, "artist_name": str }`.
  - `GET /api/lyrics/lrclib/search?q={query}`: Calls `lrclib_client.search_lyrics()` and returns candidate results.
- **Frontend Behavior (`src/static/library_queue.js` & `src/static/index.html`):**
  1. Inside `#lyrics-modal`, a button `#fetch-lrclib-btn` labeled `🌐 Auto-Fetch LRC` is placed alongside the Title/Artist inputs.
  2. When clicked:
     - Button enters loading state (`"Fetching..."` with spinner).
     - Sends `GET /api/lyrics/lrclib/get` with the modal's current Title and Artist values.
     - If lyrics found:
       - Sets `#lyrics-textarea` value to the returned `.lrc` content.
       - Displays a green success banner: `✓ Synchronized lyrics loaded from LRCLIB! Click "Save Changes" to apply.`
     - If no match found:
       - Displays an inline amber alert: `⚠️ No exact match found on LRCLIB. Try modifying Title/Artist keywords.`
     - Restores button state.

---

## 4. UI Specifications

### `#lyrics-modal` Layout Additions
```html
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
    <div>
        <label for="lyrics-edit-title">Song Title</label>
        <input id="lyrics-edit-title" type="text" ... />
    </div>
    <div>
        <label for="lyrics-edit-artist">Artist (Optional)</label>
        <input id="lyrics-edit-artist" type="text" ... />
    </div>
</div>

<!-- Auto-Fetch LRC Action Bar -->
<div class="flex items-center justify-between p-2.5 bg-surface-950 border border-slate-800 rounded-xl">
    <div class="flex items-center gap-2 text-xs text-slate-300">
        <span>🌐</span>
        <span>Auto-populate lyrics from online database</span>
    </div>
    <button id="fetch-lrclib-btn" class="px-3 py-1.5 rounded-lg bg-brand-600/90 hover:bg-brand-500 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
        <span>⚡</span> Auto-Fetch LRC
    </button>
</div>

<!-- Inline Fetch Status Alert -->
<div id="lrclib-fetch-alert" class="hidden text-xs p-2 rounded-lg font-medium"></div>
```

---

## 5. API Contracts

### `GET /api/lyrics/lrclib/get`
- **Query Parameters:**
  - `title` (string, required)
  - `artist` (string, optional)
- **Response `200 OK`:**
  ```json
  {
    "found": true,
    "lyrics": "[00:08.02] I wanted to talk, you wanted to sleep\n[00:12.03] ...",
    "has_timestamps": true,
    "track_name": "Last Birthday",
    "artist_name": "Valley",
    "duration": 237.0
  }
  ```
- **Response `200 OK` (Not Found):**
  ```json
  {
    "found": false,
    "lyrics": "",
    "has_timestamps": false,
    "message": "No matching lyrics found on LRCLIB"
  }
  ```

### `GET /api/lyrics/lrclib/search`
- **Query Parameters:**
  - `q` (string, required)
- **Response `200 OK`:**
  ```json
  {
    "results": [
      {
        "id": 31384765,
        "track_name": "Last Birthday",
        "artist_name": "Valley",
        "duration": 237.0,
        "has_synced_lyrics": true
      }
    ]
  }
  ```

---

## 6. Acceptance Criteria
- [ ] Backend client connects to `https://lrclib.net/api/` with `User-Agent` and SSL validation.
- [ ] During ingestion/separation, if `lyrics.lrc` is empty, background pipeline queries LRCLIB and writes synchronized lyrics to disk automatically.
- [ ] Clicking `#fetch-lrclib-btn` in `#lyrics-modal` fetches LRC lyrics and fills `#lyrics-textarea`.
- [ ] Offline / 404 / rate-limit responses fail gracefully without crashing separation or throwing unhandled errors in UI.
- [ ] Automated tests cover LRCLIB client mock scenarios, API routes, and frontend modal integration.
