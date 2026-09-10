---
status: approved
approved_by: reg
approved_at: 2026-09-10
---


# ADR-0012: Native Video Streaming Engine, CSS Geometry Scaling & Dual-Stream Side A/B Ingestion

## Context
Version 0.4.0 introduces three major capabilities to Flexioke:
1. **Looping Video Stage Backgrounds:** Commercial karaoke visual immersion requires playing muted, looping background videos behind floating synchronized lyrics with directory auto-discovery (`/data/videos/`), upload capabilities, and per-song video offset synchronization.
2. **Fullscreen Lyrics Stage Geometry Customization:** Different display environments (monitors, TVs, projectors) require customizable bounding boxes (width, height, vertical center position) without disturbing windowed desktop layout.
3. **Direct Side A / Side B Dual-Track Ingestion:** Providing a direct upload path for pre-separated studio tracks (Side B instrumental + optional Side A vocal version) bypassing AI stem separation, with seamless, synchronized vocal hot-swapping during playback.

## Decision
We choose **Option 1: Native FastAPI Video Streaming, Reactive Dual-Stream WebAudio Architecture & CSS Variable Geometry Scaling**.

### Architecture Overview:
1. **Video Backend Service (`src/services/video_manager.py`):**
   - Thread-safe directory scanner for `./data/videos/` indexing `.mp4`, `.webm`, `.mov`, and `.mkv` files.
   - REST endpoints:
     - `GET /api/videos`: Returns available video objects with filenames, sizes, and stream URLs.
     - `POST /api/videos/upload`: Multipart upload writing to `./data/videos/`.
     - `GET /api/videos/{filename}`: Streamable HTTP Range `FileResponse` enabling seekable HTML5 video playback.
   - Initial seed / default association: `bg001.mp4` recognized as default video for library tracks without an explicit assignment.
2. **Karaoke Stage Video Renderer (`src/static/karaoke.js` & `index.html`):**
   - `<video id="karaoke-bg-video">` mounted inside `#karaoke-stage-card` with `pointer-events-none`, `muted`, `loop`, `playsinline`, and `opacity-40` backdrop styling behind lyrics (`z-0`).
   - Synchronized playback coordinator: video automatically starts, pauses, seeks, and loops matching audio timecode: `video.currentTime = (audio.currentTime + offset) % video.duration`.
3. **Fullscreen Stage Geometry Scaling (`src/static/styles.css` & `karaoke.js`):**
   - Range sliders in `#karaoke-settings-modal` update CSS custom properties:
     - `--karaoke-fullscreen-stage-width` (default `98%`, range `60%–100%`)
     - `--karaoke-fullscreen-stage-max-height` (default `56vh`, range `30vh–80vh`)
     - `--karaoke-fullscreen-stage-v-offset` (default `0%`, range `-20%–+20%`)
   - Scoped strictly to `#karaoke-stage-card:fullscreen` and `.stage-fullscreen`. Windowed stage layout remains untouched.
   - Geometry preferences persist in `localStorage` (`flexioke_stage_config`).
4. **Side A / Side B Ingestion & Playback Engine:**
   - Ingestion: `POST /api/jobs/upload-side-ab` saves Side B (Instrumental) and optional Side A (Vocal), generating a completed Job with `source_type: "side_ab"` and `progress: 100` immediately, bypassing separation workers.
   - Attachment: `POST /api/jobs/{job_id}/attach-side-a` allows uploading vocal track to an existing Side B track.
   - Playback Coordinator: Preloads both audio tracks; Lead Vocal button toggles mutual GainNode muting (`1.0 ⟷ 0.0`) in real-time with locked timecode sync. Button disabled states adapt gracefully when only one side is present.

## Options Considered

### Option 1: Native FastAPI Video Streaming, Reactive Dual-Stream WebAudio & CSS Variable Geometry (Chosen)
- **Pros:**
  - **Zero External Runtime Dependencies:** No FFmpeg daemons, transcode workers, or background queue overhead.
  - **Instant Availability:** Side A/B uploads are ready to sing immediately (0-second processing time).
  - **Zero-Latency Vocal Switching:** Seamless audio hot-swapping between instrumental and vocal streams with locked timecode sync.
  - **Smooth 60fps Rendering:** Hardware-accelerated browser video decoding and jitter-free CSS layout scaling.
- **Cons:**
  - Background videos must be encoded in standard HTML5 formats (`.mp4`, `.webm`, etc.).

### Option 2: Server-Side FFmpeg Video Transcoding & Audio Channel Muxing
- **Pros:**
  - Standardizes legacy or exotic video codecs.
- **Cons:**
  - Introduces heavy CPU/disk overhead and processing delays to Side A/B uploads (violating the instant-upload goal).
  - High complexity with external daemon dependencies.

## Consequences
- `./data/videos/` directory must be preserved and gitignored in `.gitignore`.
- Backing vocal toggle is disabled for `side_ab` tracks as they contain 2 stems (Instrumental / Vocal) rather than 3 stems.
- Existing 23 songs default to `bg001.mp4`.

## Related
- Functional spec: `docs/specs/version0.4.0.md`
- Requirement: `docs/requirements/version0.4.0.md`
- Related ADRs: Extends `docs/design/ADR-0001-stem-separation-player-architecture.md`, `docs/design/ADR-0002-karaoke-lyrics-synchronization.md`, `docs/design/ADR-0006-karaoke-stage-ux-and-catalog-modal.md`, and `docs/design/ADR-0011-ui-and-stage-experience-enhancements.md`.
