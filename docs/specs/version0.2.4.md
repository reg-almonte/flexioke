---
status: pending-approval
approved_by:
approved_at:
---

# Version 0.2.4 — Stem Studio Upgrade & Separation Job Queue — Functional Spec

## Related Requirements
- [`docs/requirements/version0.2.4.md`](../requirements/version0.2.4.md)

---

## Functional Flows

### 1. Direct Audio URL Download & Ingestion Flow
#### Main Flow
1. User enters a direct HTTP/HTTPS audio URL (e.g. `https://example.com/audio/song.mp3`) into `#audio-url-input` and clicks **Download & Separate**.
2. Frontend validates non-empty URL format (`^https?://...`) and emits `POST /api/jobs/download-url` with payload `{ "url": "<url>" }`.
3. Backend creates a `JobRecord` with `status: QUEUED`, extracts a candidate title from the URL path, and returns HTTP 202 (`JobRecord`).
4. In background, the server streams the audio file to `./data/jobs/{job_id}/input.mp3`:
   - Validates `Content-Type` header or file magic bytes (must be supported audio format: MP3, WAV, M4A, FLAC, OGG, AAC).
   - Enforces max file size limit (100 MB).
   - If filename contains `" - "`, executes smart Title & Artist parser.
5. Job enters the sequential separation queue.

#### Alternate / Error Flows
- **Invalid URL / Network Error / Timeout:** Job status updates to `FAILED` with error message `"Failed to download audio from URL: <error>"`.
- **Non-Audio File:** If downloaded content is not valid audio, job status updates to `FAILED` (`"URL does not point to a supported audio file"`).

---

### 2. Collapsible Sidebar Accordions Flow
#### Main Flow
1. The Stem Studio left sidebar contains 3 collapsible card sections:
   - `#studio-card-add-song` (Add Song for Separation)
   - `#studio-card-library` (Studio Song Library)
   - `#studio-card-queue` (Studio Queue)
2. Each section header contains a clickable toggle chevron button (`.accordion-toggle-btn` with icon `▾` when open, `▸` when closed).
3. Clicking a header toggles visibility of the section body (`.accordion-body`) with a smooth height transition.
4. On toggle, the state is persisted in `localStorage["flexioke_studio_accordions"]` as a JSON object:
   ```json
   { "add_song": true, "library": true, "queue": true }
   ```
5. On page load, Stem Studio restores the user's saved accordion states.

---

### 3. Expanded Studio Song Catalog Modal Flow
#### Main Flow
1. User clicks the Expand button (`#open-studio-catalog-btn`, icon `⛶`) at the top right of the Studio Song Library card.
2. The full-screen `#studio-catalog-modal` opens with backdrop blur and focuses the search input (`#studio-catalog-search-input`).
3. Modal displays:
   - Header with total song count (`#studio-catalog-count`).
   - Real-time search bar with quick-clear button (`✕`).
   - Sort dropdown (`#studio-catalog-sort-select`): `Recently Added` (default), `Title (A-Z)`, `Title (Z-A)`, `Artist (A-Z)`.
   - Scrollable grid/table of song cards (`#studio-catalog-songs-list`).
4. Each song item displays:
   - Source icon (`📁` or `🌐`), Song Title, Artist name, duration, and source file info.
   - Action buttons:
     - `▶ Play Now`: Loads stems into Stem Studio multitrack player.
     - `➕ Queue`: Adds song to the Studio playback queue.
     - `📝 Edit Details / Lyrics`: Opens the Lyrics & Metadata editor modal (`#lyrics-modal`).
5. Modal closes via `Esc` key, close button (`✕`), or clicking outside on the backdrop.

---

### 4. Multi-File Drag-and-Drop Batch Ingestion & FIFO Separation Queue Flow
#### Main Flow
1. User selects multiple audio files via file picker (`<input type="file" multiple accept="audio/*">`) or drags multiple files into `#studio-dropzone`.
2. Frontend iterates over selected files and sends parallel upload requests `POST /api/jobs/upload`.
3. Backend receives each file:
   - Validates audio format and length.
   - Applies smart Title & Artist parser to the filename.
   - Creates a `JobRecord` with `status: JobStatus.QUEUED`.
   - Returns HTTP 202 immediately.
4. Frontend updates the **Separation Queue Progress Card** (`#processing-queue-container`), listing:
   - Currently active job (with stage text, progress %, and pulsing indicator).
   - Queued waiting jobs with position badge (e.g. `⏳ Position #1 in queue`).
   - `✕ Cancel` button on each item.
5. Backend **Separation Worker** runs in-process:
   - Executes 1 job at a time sequentially (`PROCESSING`).
   - Runs Stage 1 (Mel-Band RoFormer) $\to$ Stage 2 (MDX-Net Karaoke 2) $\to$ generates stems (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`).
   - Moves original raw audio file to `./data/archive/{job_id}_{filename}`.
   - Marks job `COMPLETED` and automatically dequeues the next `QUEUED` job.
   - Emits `flexioke:job-completed` event triggering library auto-refresh.

#### Alternate / Error Flows
- If user clicks `✕ Cancel` on a queued job: Emits `POST /api/jobs/{job_id}/cancel`. Backend sets status to `CANCELLED` and skips it.
- If a separation stage throws an error: Job status updates to `FAILED`, and worker immediately advances to process the next queued job.

---

### 5. Smart Title & Artist Filename Parsing Flow
#### Main Flow
1. When a filename string $F$ is processed:
   - Strip extension (e.g. `.mp3`, `.wav`, `.m4a`, `.flac`).
   - Replace underscores `_` with spaces.
   - Trim leading track numbers if present (e.g. `01. `, `02 - ` $\to$ cleaned).
2. Check for `" - "` delimiter:
   - If present:
     - `title = parts[0].trim()`
     - `artist = parts[1].trim()`
   - If no delimiter is found:
     - `title = cleaned_name.trim()`
     - `artist = "Unknown Artist"`
3. Persisted in `JobRecord.title` and `JobRecord.artist`.

---

### 6. Persistent Notes Scratchpad Flow (Option B)
#### Main Flow
1. User clicks the `📝 Notes` button in the Stem Studio header toolbar.
2. `#studio-notes-modal` opens with a clean markdown/links text editor.
3. User types notes, paste URLs for lyric resources or audio bookmarks.
4. Input listener auto-saves content immediately to `localStorage["flexioke_studio_notes"]`.
5. Links typed with `http://` or `https://` are automatically detected and rendered as clickable external links in a live preview pane or rendered links tab.
6. Modal closes cleanly on `Esc`, `✕`, or backdrop click without losing any typed data.

---

### 7. Combined Stem & Lyrics `.zip` Export Flow
#### Main Flow
1. User clicks `📦 Export Stems (.zip)` on the multitrack toolbar or inside the track menu for a completed job.
2. Browser initiates `GET /api/jobs/{job_id}/export/zip`.
3. Backend:
   - Checks that all 3 stems (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`) exist.
   - Checks if `lyrics.json` / LRC exists; if present, extracts `lyrics.lrc`.
   - Streams an in-memory or spooled `.zip` archive named `{clean_title}_stems.zip` with `Content-Disposition: attachment`.
   - Archive contains:
     - `instrumental.mp3`
     - `lead_vocals.mp3`
     - `backing_vocals.mp3`
     - `lyrics.lrc` (if available)

---

### 8. Track Deletion Flow
#### Main Flow
1. User opens `📝 Edit Details / Lyrics` on any song card and clicks `🗑 Delete Track`.
2. A confirmation modal prompts: *"Are you sure you want to delete '[Title]'? This will permanently remove all audio stems, lyrics, and metadata."*
3. On confirmation, frontend calls `DELETE /api/jobs/{job_id}`.
4. Backend:
   - Halts any active playback if currently playing.
   - Removes job folder `./data/jobs/{job_id}/` and associated archive file.
   - Purges job from `jobs.json` store and in-memory index.
   - Removes track from queue if present.
   - Returns `{ "success": true, "deleted_job_id": "{job_id}" }`.
5. Frontend refreshes library lists across both Stem Studio and Karaoke Mode.

---

### 9. Post-Separation Raw Audio Ingestion Archiving Flow
#### Main Flow
1. Upon successful completion of Stage 2 separation for `job_id`:
2. The pipeline manager moves `./data/jobs/{job_id}/input.mp3` to `./data/archive/{job_id}_{sanitized_source_name}.mp3`.
3. The job directory keeps only the generated stem files (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`) and metadata/lyrics.
4. Storage footprint is optimized and raw inputs are safely consolidated in `./data/archive/` for easy manual or batch cleanup.

---

## Inputs & Outputs

### API Endpoints
| Endpoint | Method | Input | Output / Status |
|---|---|---|---|
| `/api/jobs/download-url` | `POST` | `{ "url": "https://..." }` | `JobRecord` (HTTP 202) |
| `/api/jobs/upload` | `POST` | `multipart/form-data` (`file`) | `JobRecord` (HTTP 202) |
| `/api/jobs/{job_id}/cancel` | `POST` | None | `{ "status": "cancelled", "job_id": "..." }` |
| `/api/jobs/{job_id}/export/zip` | `GET` | None | `application/zip` stream (`{title}_stems.zip`) |
| `/api/jobs/{job_id}` | `DELETE` | None | `{ "status": "deleted", "job_id": "..." }` |

---

## Business & Validation Rules
1. **Concurrency Protection:** Stem separation pipeline worker is strictly serial (FIFO queue, max 1 active separation task) to ensure stable GPU memory utilization.
2. **Audio Format Enforcement:** URL downloader and file upload accept only audio MIME types / valid audio magic bytes with a 100MB limit.
3. **Archive Integrity:** Ingestion file archiving happens only after all 3 stems are verified and written to disk.
4. **Delete Cascade:** Deleting a job purges job folder, stems, lyrics, and any pending queue references atomically.

---

## Open Questions
- None. All functional flows and edge cases defined.
