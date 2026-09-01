---
status: approved
approved_by: reg
approved_at: 2026-09-01
---

# Version 0.2.5: Automated LRCLIB Synchronized Lyrics Integration

## Problem / Motivation
Currently in Flexioke, users must manually locate, format, and paste synchronized timestamped `.lrc` lyrics into the Song Details & Lyrics editor modal. While this works, manual transcription or external file hunting is tedious. LRCLIB (`https://lrclib.net/`) is a comprehensive, open-access, zero-authentication public database of timestamped synchronized lyrics (`.lrc`). Integrating LRCLIB into Flexioke will allow lyrics to be auto-populated effortlessly both during background stem separation and on-demand inside the lyrics editor.

## Target Users
- **Karaoke Singers & Host Users:** Want instant, synchronized lyrics for their tracks without manual hunting or pasting.
- **Stem Studio Creators:** Want automatic `.lrc` lyrics bundled inside their downloaded `.zip` stem packs without extra steps.

## Goals
1. **Automated Pipeline Ingestion Fetch:** Automatically query LRCLIB in the background during audio ingestion/separation using parsed Title & Artist metadata, persisting `lyrics.lrc` alongside generated stems if synchronized lyrics are found.
2. **Interactive 1-Click Fetch in Lyrics Modal:** Provide an instant `🌐 Auto-Fetch LRC` action inside the Song Details & Lyrics editor modal (`#lyrics-modal`) that queries LRCLIB in real time and loads timestamped lyrics directly into the editor textarea.
3. **Robust Fallback & Search Flexibility:** If background auto-fetching fails (e.g., misspelled filename or obscure track name), allow the user to edit the title/artist in the modal and retry on-demand.
4. **Resilience & Non-Blocking Pipeline:** If LRCLIB is unreachable, returns 404, or is rate-limited, audio separation continues uninterrupted without throwing fatal errors.

## Non-Goals (Out of Scope)
- Automatic AI audio-to-text alignment/transcription (Whisper alignment is a future major epic).
- User submission/uploading of lyrics back to the public LRCLIB database (read-only consumption).

## Functional Requirements
1. **Backend LRCLIB Service (`src/services/lrclib_client.py`):**
   - Provide helper methods `fetch_lyrics(title, artist, duration)` and `search_lyrics(query)`.
   - Send standardized `User-Agent: Flexioke/0.2.5 (https://github.com/reg-almonte/flexioke)` with SSL context and sensible timeout (5s).
   - Prefer `syncedLyrics` (LRC format), falling back to `plainLyrics` if synced lyrics are unavailable.

2. **Backend API Proxy Endpoints:**
   - `GET /api/lyrics/lrclib/get?title=...&artist=...` — exact track lookup.
   - `GET /api/lyrics/lrclib/search?q=...` — keyword search returning matching candidates with track name, artist, duration, and synced status.

3. **Background Separation Pipeline Integration:**
   - In `src/services/pipeline.py` (or post-ingestion job handler), automatically invoke `lrclib_client` to fetch lyrics for the job if `lyrics.lrc` does not already exist.
   - Save returned lyrics to `./data/jobs/{job_id}/lyrics.lrc` and update job metadata if lyrics were retrieved.

4. **Interactive Lyrics Editor UI Enhancements (`#lyrics-modal`):**
   - Add a `🌐 Auto-Fetch LRC` button next to the Title/Artist input fields.
   - Clicking triggers a search on LRCLIB using current Title and Artist values.
   - If lyrics found: populates the textarea with the `.lrc` content and displays a success notification (`"Synced lyrics fetched from LRCLIB!"`).
   - If not found or error: displays an informative inline status message (`"No lyrics found on LRCLIB for this title/artist. Try adjusting keywords."`).

## Acceptance Criteria
- [ ] Ingesting a known song with clean Title/Artist (e.g. *Valley - Last Birthday*) automatically downloads and saves `lyrics.lrc` with timestamps during separation.
- [ ] Clicking `🌐 Auto-Fetch LRC` in `#lyrics-modal` queries LRCLIB and populates the LRC textarea with timestamped lyrics.
- [ ] If LRCLIB returns no results or network is offline, separation pipeline completes successfully without failure.
- [ ] 100% automated test coverage for LRCLIB service, API routes, and frontend modal interactions.
