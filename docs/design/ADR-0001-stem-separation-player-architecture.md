---
status: approved
approved_by: user
approved_at: 2026-08-27
---

# ADR-0001: Modular FastAPI Architecture with In-Process Async Task Pool & Multitrack Web Player

## Context
Flexioke requires a unified, lightweight, and responsive web application to handle:
1. Audio ingestion via file uploads and YouTube URL extraction.
2. A sequential 2-stage deep learning stem separation pipeline (Mel-Band RoFormer for Instrumental/Vocals $\rightarrow$ UVR_MDXNET_KARA_2 for Lead/Backing Vocals).
3. Persistent storage and indexed retrieval of processed songs for searching and queue management.
4. An interactive browser-based multitrack player with synchronized 3-track waveform rendering, channel mixing (mute/solo/volume), and seamless queue playback.

The system needs to run reliably in local and single-server environments without requiring heavy external infrastructure (such as dedicated message brokers or database servers).

## Decision
We adopt **Option 1: Modular FastAPI Monolith with In-Process Async Task Pool & Filesystem JSON Store**.

### Key Architectural Decisions:
1. **Backend Framework & Server:**
   - Python 3.10+ with **FastAPI** and **Uvicorn**, serving both the REST API and static frontend assets from a single unified server.
2. **Audio Processing Pipeline:**
   - **`audio-separator` Python API:** Direct programmatic usage of `Separator` class to run Mel-Band RoFormer (`mel_band_roformer_vocals`) for Stage 1 and UVR MDX-Net Karaoke (`UVR_MDXNET_KARA_2`) for Stage 2.
   - **`yt-dlp` Integration:** Direct Python API integration for fast YouTube audio extraction with format and duration verification.
   - **Output Encoding:** Stems encoded as 320kbps MP3 for fast browser streaming and compact storage.
3. **Concurrency & Execution Management:**
   - In-process `ThreadPoolExecutor` with bounded worker concurrency (default: 1 concurrent separation job) to prevent GPU memory allocation conflicts and CPU thrashing.
   - Non-blocking async endpoints responding immediately with HTTP 202 and `job_id`.
4. **Data Persistence & Song Library Index:**
   - File-based persistence under `./data/jobs/{job_id}/` storing `input.*`, `job.json`, and output stem files (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`).
   - `JobManager` maintains an in-memory cached index of `job.json` records refreshed on startup and write, providing zero-overhead, sub-millisecond search and filtering for the Song Library.
5. **Frontend Architecture:**
   - Buildless modern single-page application (SPA) using HTML5, TailwindCSS (via CDN/pre-bundled), and ES Modules (`app.js`, `player.js`, `library.js`, `queue.js`).
   - **Wavesurfer.js v7** with the official MultiTrack plugin coordinating the 3 audio tracks, handling synchronous timeline scrubbing, play/pause, and per-track gain/solo/mute routing.

## Options Considered

### Option 1: Modular FastAPI with In-Process Async Task Pool & JSON Store (Chosen)
- **Pros:**
  - Zero external dependencies (no Redis, Celery, or SQL database daemon required).
  - Single-command local startup (`uvicorn main:app --reload`).
  - Fast in-memory model execution without subprocess restart overhead.
  - Fully portable and self-contained disk storage.
- **Cons:**
  - Background jobs share memory and CPU/GPU resources with the web server process.
  - Scaling beyond a single host requires moving to external worker queues.

### Option 2: Decoupled Multi-Service with Celery, Redis, and SQLite (Rejected)
- **Pros:** Clean process isolation between HTTP API and ML inference; multi-node worker distribution capability.
- **Cons:** High operational complexity; requires managing 3 concurrent services (Redis daemon, Celery worker process, FastAPI server); unnecessary overhead for local and single-server deployments.

### Option 3: Subprocess CLI Execution Wrapper (Rejected)
- **Pros:** Total process isolation for ML execution without Celery; worker crashes do not impact the web server.
- **Cons:** Subprocess startup and teardown overhead; model files must be reloaded on every separation job; fragile stdout log scraping for progress calculation.

## Consequences
- **Positive:**
  - Minimal developer onboarding friction and streamlined local testing.
  - Unified codebase in `src/` with clear modular boundaries between routing, pipeline execution, persistence, and static assets.
  - Responsive multitrack UI with zero build step required.
- **Negative / Mitigations:**
  - High-intensity ML tasks may load the CPU/GPU heavily. *Mitigation:* Single-worker serialization queue ensures system stability during heavy separation requests.

## Related
- Functional spec: `docs/specs/stem-separation-player.md`
- Requirement: `docs/requirements/stem-separation-player.md`
- Supersedes / related ADRs: None (Initial Architecture Decision)
