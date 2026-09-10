---
status: approved
approved_by: reg
approved_at: 2026-09-10
---


# Functional Specification: Version 0.4.0 (Video Backgrounds, Stage Geometry Controls & Side A/B Uploads)

## Related Requirements
- `docs/requirements/version0.4.0.md`

---

## 1. Overview
This specification details the technical architecture, REST contracts, DOM structures, state machines, and playback coordinator rules for:
1. **Looping Video Background Engine & Auto-Discovery** (`/data/videos/`, `#karaoke-bg-video`, `/api/videos`).
2. **Fullscreen Stage Geometry Customization** (`#karaoke-settings-modal`, CSS custom properties).
3. **Direct Side A / Side B Dual-Track Ingestion & Playback Hot-Swapping** (`source_type: side_ab`, vocal sync state machine).

---

## 2. Functional Flows

### Flow 1: Video Background Engine & Per-Song Synchronization
```
[User Selects Song in Library / Queue]
                 │
                 ▼
[KaraokeStageManager.onSongLoaded(job)]
   ├── Reads job.video_id (or defaults to "bg001.mp4" / global default)
   ├── Reads job.video_offset_seconds (default 0.0)
   ├── Sets #karaoke-bg-video src = `/api/videos/${job.video_id}`
   └── Sets #karaoke-bg-video.currentTime = video_offset_seconds
                 │
   ┌─────────────┴─────────────┐
   ▼                           ▼
[Song Plays]             [Song Pauses / Seeks]
   │                           │
   ├── video.play()            ├── video.pause()
   └── Synchronous loop:       └── video.currentTime = (audio.currentTime + offset) % video.duration
       if video ends -> loop
```

#### Detailed Flow 1 Specifications:
1. **Video Storage & Auto-Discovery:**
   - Directory: `./data/videos/`. Supported formats: `.mp4`, `.webm`, `.mov`, `.mkv`.
   - On backend startup and upon request, the server indexes all video files in `./data/videos/`.
   - If `./data/videos/` is empty or initial setup runs, `bg001.mp4` is recognized as the system default.
   - All existing library songs without an assigned `video_id` automatically fallback to `bg001.mp4`.
2. **REST API Endpoints:**
   - `GET /api/videos`: Returns list of available videos `[{"filename": "bg001.mp4", "size_bytes": 123456, "url": "/api/videos/bg001.mp4"}]`.
   - `POST /api/videos/upload`: Multipart video upload, saves to `./data/videos/<filename>` and returns metadata.
   - `GET /api/videos/{filename}`: HTTP Range streaming endpoint using FastAPI `FileResponse` supporting seekable HTML5 video streaming.
3. **Song Details Modal Video Assignment:**
   - Video Selector dropdown in `#lyrics-modal` listing all discovered videos from `GET /api/videos`.
   - Number input for **Video Start Offset** (in seconds, e.g. `0.0`, `12.5`).
   - Saved atomically via `PATCH /api/jobs/{job_id}/metadata`.
4. **DOM Rendering & Layering:**
   - In `#karaoke-stage-card`:
     ```html
     <video id="karaoke-bg-video" class="absolute inset-0 w-full h-full object-cover z-0 pointer-events-none opacity-40 transition-opacity duration-500" autoplay loop muted playsinline></video>
     ```
   - Floating glassmorphism header (`#karaoke-top-header`), lyrics stage (`#karaoke-lyrics-stage`), and transport bar (`#karaoke-transport-bar`) float on top with `z-10` / `z-20`.

---

### Flow 2: Fullscreen Stage Geometry Customization (`#karaoke-settings-modal`)
```
[User Opens Stage Settings in Fullscreen / Windowed]
                 │
                 ▼
[Adjusts Geometry Sliders]
   ├── Width Slider: (60% to 100%) ──► updates --karaoke-fullscreen-stage-width
   ├── Height Slider: (30vh to 80vh) ─► updates --karaoke-fullscreen-stage-max-height
   └── Vertical Offset: (-20% to +20%) ► updates --karaoke-fullscreen-stage-v-offset
                 │
                 ▼
[Real-Time DOM CSS Variable Update + LocalStorage Save]
   ├── Updates #karaoke-lyrics-stage dimensions immediately in Fullscreen
   └── Windowed default mode remains locked to standard responsive card layout
```

#### Detailed Flow 2 Specifications:
1. **Interactive Controls in `#karaoke-settings-modal`:**
   - `#settings-fullscreen-width`: Range `60%` to `100%`, step `1%`, default `98%`.
   - `#settings-fullscreen-height`: Range `30vh` to `80vh`, step `1vh`, default `56vh` (max ceiling).
   - `#settings-fullscreen-v-offset`: Range `-20%` to `+20%`, step `1%`, default `0%`.
2. **CSS Variables & Scoping:**
   ```css
   :root {
     --karaoke-fullscreen-stage-width: 98%;
     --karaoke-fullscreen-stage-max-height: 56vh;
     --karaoke-fullscreen-stage-v-offset: 0%;
   }

   #karaoke-stage-card:fullscreen #karaoke-lyrics-stage,
   #karaoke-stage-card.stage-fullscreen #karaoke-lyrics-stage {
     width: var(--karaoke-fullscreen-stage-width, 98%) !important;
     max-width: var(--karaoke-fullscreen-stage-width, 98%) !important;
     max-height: var(--karaoke-fullscreen-stage-max-height, 56vh) !important;
     top: calc(50% + var(--karaoke-fullscreen-stage-v-offset, 0%)) !important;
     left: 50% !important;
     transform: translate(-50%, -50%) !important;
     position: absolute !important;
   }
   ```
3. **Windowed Isolation:**
   - Windowed `#karaoke-lyrics-stage` uses static classes (`max-h-[350px] my-3 sm:my-4 w-full`) without CSS transform overrides.

---

### Flow 3: Direct Side A / Side B Dual-Track Ingestion & Vocal Hot-Swapping

```
[Stem Studio Upload Area]
        │
        ├── Mode: "Direct Side A/B (Instrumental & Vocal)"
        ├── Side B Input (Instrumental Audio) [Required]
        └── Side A Input (Vocal / Original Audio) [Optional]
        │
        ▼
[POST /api/jobs/upload-side-ab]
   ├── Creates Job: { source_type: "side_ab", status: "completed", progress: 100 }
   ├── Stores Side B as stems["instrumental"] = "/api/jobs/{id}/stems/instrumental"
   └── Stores Side A (if provided) as stems["lead_vocals"] = "/api/jobs/{id}/stems/lead_vocals"
        │
        ▼
[Playback Coordinator]
   ├── Both audio streams preloaded and timecode-locked
   ├── Lead Vocal Toggle ON  ──► Side A volume = 100%, Side B volume = 0%
   ├── Lead Vocal Toggle OFF ──► Side B volume = 100%, Side A volume = 0%
   └── Backing Vocal Toggle  ──► Disabled ("Backing: N/A")
```

#### Detailed Flow 3 Specifications:
1. **Ingestion Endpoint & Validation:**
   - `POST /api/jobs/upload-side-ab` accepts `file_side_b` (required, instrumental audio), optional `file_side_a` (vocal audio), `title`, `artist`.
   - Validates audio extensions (`.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`).
   - Generates `job_id`, writes audio files into `/data/jobs/{job_id}/`, builds stems dictionary, marks job `status: completed` immediately without spawning separation tasks.
2. **Synchronized Playback Engine:**
   - When playing `source_type === "side_ab"`:
     - `wavesurfer` / audio element loads both `instrumental` (Side B) and `lead_vocals` (Side A).
     - When user toggles `#karaoke-toggle-lead-btn`:
       - If Lead Vocal is ON: Mute Side B, Unmute Side A.
       - If Lead Vocal is OFF: Mute Side A, Unmute Side B.
       - Audio remains perfectly timecode synchronized.
   - Dynamic Button Adaptation:
     - If only Side B exists: `#karaoke-toggle-lead-btn` disabled with text `Lead: OFF (Side B Only)`.
     - If only Side A exists: `#karaoke-toggle-lead-btn` disabled with text `Lead: ON (Side A Only)`.
     - `#karaoke-toggle-backing-btn` disabled with text `Backing: N/A (Side A/B)`.
3. **Song Details Modal Side A/B Attachment:**
   - If a song was uploaded with Side B only, the user can upload/attach Side A later via `#lyrics-modal` (`POST /api/jobs/{job_id}/attach-side-a`).

---

## 3. Inputs & Outputs

| Endpoint / Action | Input | Output / Effect |
|---|---|---|
| `GET /api/videos` | None | JSON array of available video objects |
| `POST /api/videos/upload` | `multipart/form-data` (`file`) | JSON video metadata |
| `GET /api/videos/{filename}` | Range header | Streamable binary video stream |
| `PATCH /api/jobs/{job_id}/metadata` | `{ video_id, video_offset_seconds }` | Updated job JSON |
| `POST /api/jobs/upload-side-ab` | `file_side_b`, optional `file_side_a`, `title`, `artist` | Completed Job JSON (`source_type: "side_ab"`) |
| `POST /api/jobs/{job_id}/attach-side-a` | `multipart/form-data` (`file`) | Updated Job JSON with `lead_vocals` attached |

---

## 4. Business & Validation Rules
1. **Video Backgrounds:**
   - Background video is strictly muted in DOM (`video.muted = true`).
   - If a song has no video assigned, it uses `bg001.mp4`.
   - Video offsets can be positive float values clamped to `[0, video_duration]`.
2. **Fullscreen Geometry:**
   - Geometry settings cannot exceed sensible boundaries: Width `[60%, 100%]`, Height `[30vh, 80vh]`, Center Offset `[-20%, +20%]`.
   - Settings must never apply to windowed stage mode.
3. **Side A/B Tracks:**
   - Side A and Side B must be valid audio files.
   - AI separation workers are never invoked for `side_ab` jobs.
   - Single-sided tracks gracefully lock vocal buttons.

---

## 5. Data Entities & Schema Updates

### Job Model (`src/models.py`)
```python
class SourceType(str, Enum):
    UPLOAD = "upload"
    URL = "url"
    YOUTUBE = "youtube"
    SIDE_AB = "side_ab"

class Job(BaseModel):
    job_id: str
    source_type: SourceType
    source_name: str
    title: str
    artist: Optional[str] = None
    video_id: Optional[str] = "bg001.mp4"
    video_offset_seconds: float = 0.0
    status: JobStatus = JobStatus.QUEUED
    progress: int = 0
    current_stage: str = "Job created"
    error: Optional[str] = None
    duration_seconds: Optional[float] = None
    stems: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
```

---

## 6. Open Questions
- None. (All functional flows and contracts fully defined).
