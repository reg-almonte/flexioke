---
status: approved
approved_by: user
approved_at: 2026-08-27
---

# Flexioke: Audio Stem Separation & Multitrack Web Player — Functional Spec

## Related Requirements
- `docs/requirements/stem-separation-player.md`

## Functional Flows

### Main Flow 1: File Upload & Ingestion Pipeline
1. **User Action:** User navigates to Flexioke, selects the "Upload Audio" tab, drops or chooses an audio file (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`).
2. **Submission:** User clicks "Separate Stems".
3. **Request:** Frontend sends `POST /api/jobs/upload` multipart request containing the file.
4. **Backend Ingestion:**
   - Generates a UUID `job_id`.
   - Validates file size (max 100MB) and audio extension.
   - Extracts metadata/title from filename.
   - Saves file to `./data/jobs/{job_id}/input.<ext>`.
   - Writes `job.json` with status `queued`, progress `0`.
   - Enqueues background separation task.
5. **Response:** Backend returns HTTP 202 `{ "job_id": "<uuid>", "status": "queued" }`.
6. **Frontend Tracking:** Frontend displays a processing progress card and begins polling `GET /api/jobs/{job_id}` every 2 seconds.
7. **Background Pipeline Execution:**
   - **Stage 1 (RoFormer):** Updates status to `separating_stage_1` (progress ~25%). Executes Mel-Band RoFormer $\rightarrow$ produces `instrumental` and `vocals`.
   - **Stage 2 (UVR MDX-Net Kara 2):** Updates status to `separating_stage_2` (progress ~65%). Executes `UVR_MDXNET_KARA_2` on `vocals` $\rightarrow$ produces `lead_vocals` and `backing_vocals`.
   - **Encoding & Verification:** Encodes all 3 stems as MP3 (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`).
   - Updates `job.json` with status `completed`, progress `100`, audio duration, and stem streaming URLs.
8. **Completion:** When status becomes `completed`, the song is automatically registered in the Song Library and loaded into the Multitrack Player.

### Main Flow 2: YouTube URL Ingestion Pipeline
1. **User Action:** User selects the "YouTube Link" tab, enters a valid YouTube video/music URL, and clicks "Separate Stems".
2. **Submission:** Frontend sends `POST /api/jobs/youtube` with `{ "url": "<youtube_url>" }`.
3. **Backend Ingestion:**
   - Validates URL syntax.
   - Generates UUID `job_id`.
   - Initializes job state to `downloading` (progress ~10%).
   - Invokes `yt-dlp` to extract video title, duration, and best audio stream to `./data/jobs/{job_id}/input.mp3`.
4. **Pipeline Execution:** On download completion, executes Stage 1 and Stage 2 separation identically to Flow 1.

### Main Flow 3: Song Library & Search
1. **Library View:** The sidebar/panel displays the list of all completed songs retrieved via `GET /api/jobs?status=completed`.
2. **Search / Filter:** User types a query into the Library search box (e.g. artist or track name).
   - Frontend filters list in real time or calls `GET /api/jobs?status=completed&q={query}`.
3. **Actions on Library Item:**
   - **"Play Now":** Immediately loads the 3 stems of the selected song into the active multitrack player.
   - **"Add to Queue":** Appends the selected song to the playback queue.

### Main Flow 4: Playback Queue Management
1. **Queue Panel:** Displays current active song plus the list of upcoming queued songs.
2. **Queue Operations:**
   - User can add any song from the library to the queue.
   - User can remove an item from the queue.
   - User can click "Play Next" on any queue item to skip immediately to that track.
3. **Auto-Advance:** When the active multitrack playback reaches the end of the song duration, if there are songs in the queue:
   - The next song is dequeued and automatically loaded into the multitrack player.
   - Playback starts automatically.

### Main Flow 5: Multitrack Audio Playback & Channel Control
1. **Waveform Rendering:** Frontend renders 3 synchronized stacked waveforms (Instrumental, Lead Vocals, Backing Vocals) using Wavesurfer.js + MultiTrack plugin.
2. **Synchronized Play/Pause:** Global Play/Pause triggers synchronized playback across all unmuted stems.
3. **Scrubbing/Seeking:** Clicking anywhere on any waveform or master seekbar syncs playheads across all 3 tracks.
4. **Mute Control:** Clicking Mute toggles the mute state of that specific stem in real time.
5. **Solo Control:**
   - Clicking Solo on track $A$ isolates track $A$ and mutes all non-soloed tracks.
   - Clicking Solo on multiple tracks isolates all selected solo tracks while keeping non-soloed tracks muted.
   - Disabling all Solos restores each track to its prior individual Mute state.
6. **Volume Control:**
   - Per-track volume slider (0.0 - 1.0) adjusts gain node for that stem in real time.
   - Master volume slider adjusts total output gain.

---

### Alternate / Error Flows

#### Error Flow 1: Invalid File Upload
- *Trigger:* User uploads unsupported file type or size > 100MB.
- *Response:* HTTP 400 Bad Request `{ "detail": "Unsupported file format. Please upload MP3, WAV, FLAC, M4A, or OGG under 100MB." }`. Frontend displays error banner.

#### Error Flow 2: YouTube Extraction Failure
- *Trigger:* Invalid URL, private/deleted video, geo-blocked, or duration > 15 minutes.
- *Response:* Job marked as `failed` with descriptive reason. Polling returns `status: "failed"`, `error: "<reason>"`. Frontend displays error card with retry button.

#### Error Flow 3: Separation Failure
- *Trigger:* Separation error or out-of-memory.
- *Response:* Background worker catches error, updates `job.json` to `status: "failed"`. Frontend surfaces error message.

---

## Inputs & Outputs

### API Endpoints

#### 1. `POST /api/jobs/upload`
- **Request:** `multipart/form-data` with `file: UploadFile`.
- **Response (HTTP 202 Accepted):**
  ```json
  {
    "job_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "status": "queued",
    "title": "Bohemian Rhapsody",
    "created_at": "2026-08-27T11:20:00Z"
  }
  ```

#### 2. `POST /api/jobs/youtube`
- **Request:** `application/json`
  ```json
  {
    "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"
  }
  ```
- **Response (HTTP 202 Accepted):**
  ```json
  {
    "job_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "status": "downloading",
    "source_url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
    "created_at": "2026-08-27T11:20:00Z"
  }
  ```

#### 3. `GET /api/jobs/{job_id}`
- **Response (HTTP 200 OK):**
  ```json
  {
    "job_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "status": "completed",
    "progress": 100,
    "current_stage": "completed",
    "title": "Queen - Bohemian Rhapsody",
    "duration_seconds": 354.2,
    "error": null,
    "stems": {
      "instrumental": "/api/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stems/instrumental",
      "lead_vocals": "/api/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stems/lead_vocals",
      "backing_vocals": "/api/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stems/backing_vocals"
    },
    "created_at": "2026-08-27T11:20:00Z",
    "updated_at": "2026-08-27T11:21:45Z"
  }
  ```

#### 4. `GET /api/jobs` (Song Library & Search)
- **Query Parameters:**
  - `status` (optional, default: `completed`)
  - `q` (optional search query string)
- **Response (HTTP 200 OK):**
  ```json
  {
    "total": 5,
    "jobs": [
      {
        "job_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "title": "Queen - Bohemian Rhapsody",
        "source_type": "youtube",
        "duration_seconds": 354.2,
        "status": "completed",
        "created_at": "2026-08-27T11:20:00Z",
        "stems": {
          "instrumental": "/api/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stems/instrumental",
          "lead_vocals": "/api/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stems/lead_vocals",
          "backing_vocals": "/api/jobs/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stems/backing_vocals"
        }
      }
    ]
  }
  ```

#### 5. `GET /api/jobs/{job_id}/stems/{stem_type}`
- **Parameters:** `stem_type` $\in$ `[instrumental, lead_vocals, backing_vocals]`
- **Response:** `audio/mpeg` binary stream.

---

## Business & Validation Rules
1. **File Upload Restrictions:**
   - Supported extensions: `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`.
   - Max file size: 100 MB.
2. **YouTube Restrictions:**
   - Standard YouTube URL patterns (`youtube.com`, `youtu.be`, `music.youtube.com`).
   - Max duration: 15 minutes.
3. **Pipeline Stages:**
   - `queued` $\rightarrow$ `downloading` $\rightarrow$ `separating_stage_1` $\rightarrow$ `separating_stage_2` $\rightarrow$ `completed` | `failed`.
4. **Stem Models:**
   - Stage 1: Mel-Band RoFormer (`model_name: "mel_band_roformer_vocals"`).
   - Stage 2: UVR MDX-Net Karaoke (`model_name: "UVR_MDXNET_KARA_2"`).
5. **Storage & Persistence:**
   - Job files stored in `./data/jobs/{job_id}/`.
   - `job.json` persists metadata for library discovery and search.

---

## Data Entities

### `JobRecord`
| Field | Type | Description |
|---|---|---|
| `job_id` | `UUID` / `str` | Unique job identifier |
| `source_type` | `enum ("upload", "youtube")` | Ingestion method |
| `source_name` | `str` | Original file name or source URL |
| `title` | `str` | Display title of the song |
| `status` | `enum ("queued", "downloading", "separating_stage_1", "separating_stage_2", "completed", "failed")` | Current status |
| `progress` | `int (0-100)` | Progress percentage |
| `current_stage` | `str` | Description of active processing step |
| `error` | `str | null` | Error details if failed |
| `duration_seconds` | `float | null` | Audio duration in seconds |
| `stems` | `dict[str, str]` | Map of stem keys (`instrumental`, `lead_vocals`, `backing_vocals`) to stream URLs |
| `created_at` | `ISO 8601 str` | Job creation timestamp |
| `updated_at` | `ISO 8601 str` | Last updated timestamp |

### `QueueItem` (Frontend Model)
| Field | Type | Description |
|---|---|---|
| `queue_id` | `str` | Unique queue entry instance ID |
| `job_id` | `str` | Target song job ID |
| `title` | `str` | Song display title |
| `duration_seconds` | `float` | Song duration |
| `stems` | `dict[str, str]` | Stem stream URLs |

---

## Open Questions
None.
