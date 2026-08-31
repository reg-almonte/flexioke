---
status: approved
approved_by: reg
approved_at: 2026-08-31
---

# ADR-0007: In-Process Async FIFO Separation Worker, Streaming Zip Engine & Reactive Studio UI

## Context
In Version 0.2.4, Stem Studio is upgraded to eliminate several operational limitations:
1. YouTube audio extraction with `yt-dlp` frequently fails with `403 Forbidden` bot detection errors in local environments.
2. The stem separation pipeline currently handles only 1 task at a time without an asynchronous queue for subsequent uploads.
3. Left-column sidebar cards in Stem Studio lack collapsible controls, creating vertical space contention with the multitrack waveforms.
4. Stem Studio lacks an expanded full-screen song catalog modal with search, sorting, and direct access to metadata/lyrics editing.
5. Uploaded filenames with standard `<Song Title> - <Artist>.<ext>` formats require manual cleanup.
6. Users lack a quick-access scratchpad in Stem Studio for keeping track of lyric links and audio bookmarks.
7. Users lack a 1-click export mechanism to download their separated stems and lyrics as a single package.
8. Raw input audio files accumulate across individual job folders without centralized archiving.

## Decision
We choose **Option 1: In-Process Async FIFO Separation Worker, Streaming Zip Engine & Reactive Studio UI**.

### 1. In-Process FIFO Separation Task Worker
- Extend `JobManager` with an in-process thread-safe task queue (`asyncio.Queue` / background task coordinator).
- Ingested files via multi-file upload (`POST /api/jobs/upload`) and direct audio URL downloads (`POST /api/jobs/download-url`) are immediately persisted in `jobs.json` with `status: QUEUED`.
- The worker executes separation jobs strictly one-at-a-time (1 active `PROCESSING` job) to prevent GPU VRAM exhaustion on local hardware (Apple Silicon MPS / CUDA), automatically advancing to the next queued job upon completion or cancellation (`POST /api/jobs/{job_id}/cancel`).

### 2. Direct Audio URL Downloader & Smart Filename Parser
- Replace YouTube downloader with an asynchronous HTTP streaming downloader that verifies audio MIME types / magic bytes (max 100MB limit).
- Implement a smart filename parser that splits `<Song Title> - <Artist>.<ext>` into `title` and `artist`, normalizing underscores and stripping track numbers.

### 3. Combined Stem & Lyrics `.zip` Dynamic Streamer
- Add endpoint `GET /api/jobs/{job_id}/export/zip` that dynamically packages `instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`, and `lyrics.lrc` into an in-memory/spooled archive using Python's `zipfile` and `StreamingResponse` (`{title}_stems.zip`), avoiding duplicate zip files on disk.

### 4. Post-Separation Input Archiving & Track Deletion
- Move original input audio from `./data/jobs/{job_id}/input.mp3` to `./data/archive/{job_id}_{filename}` once Stage 2 separation succeeds.
- Implement `DELETE /api/jobs/{job_id}` to purge job folders, archive files, metadata, and queue entries upon confirmation.

### 5. Reactive Studio UI Components
- **Collapsible Sidebar Accordions:** Accordion headers with transition chevrons (`▾` / `▸`) persisted in `localStorage["flexioke_studio_accordions"]`.
- **Multi-File Batch Drag-and-Drop:** Native HTML5 Drag and Drop zone and multi-file input dispatching parallel upload jobs.
- **Separation Queue Progress Card:** Live status tracking showing the active job progress bar, queued items with position indicators (`Position #2 in queue`), and cancel buttons.
- **Expanded Studio Catalog Modal:** Full-screen modal (`#studio-catalog-modal`) with real-time search, sorting (default: `Recently Added`), and direct `▶ Play Now`, `➕ Queue`, and `📝 Edit Details/Lyrics` actions.
- **Studio Notes Scratchpad Modal (Option B):** Persistent notes modal in the Stem Studio navigation header auto-saving to `localStorage["flexioke_studio_notes"]` with live clickable link detection.

## Options Considered

### Option 1 (Selected): In-Process Async FIFO Separation Worker, Streaming Zip Engine & Reactive Studio UI
- **Pros:**
  - Zero external infrastructure dependencies (no Redis, Celery, or RabbitMQ required).
  - Guarantees memory safety and prevents GPU VRAM out-of-memory crashes by serializing separation tasks.
  - On-the-fly zip streaming eliminates disk storage duplication.
  - Centralized raw audio archiving facilitates future storage maintenance.
  - Pure client-side persistence for accordions and scratchpad notes gives instant zero-latency UI reactivity.
- **Cons:**
  - In-process queue states in memory are reconstructed from `jobs.json` upon server restart.

### Option 2: External Task Queue Broker (Celery + Redis) with Pre-Generated Disk Zip Archives
- **Pros:** Process-independent task state persistence.
- **Cons:** Introduces heavy external dependencies (Redis server), high disk bloat storing duplicate zip files for all library songs, and increased setup complexity for local usage.

## Consequences
- **Positive:**
  - Robust audio URL ingestion replaces flaky YouTube scraping.
  - Users can batch-upload dozens of songs and let them process unattended in the background.
  - Studio workspace is uncluttered with collapsible sidebars and an expanded catalog modal.
  - 1-click combined `.zip` export allows effortless sharing and backup of separated tracks with lyrics.
  - Original input files are cleanly archived in `./data/archive/`.
- **Neutral:**
  - GPU processing remains strictly serial to ensure stability across hardware tiers.

## Related
- Functional spec: [`docs/specs/version0.2.4.md`](../specs/version0.2.4.md)
- Requirement: [`docs/requirements/version0.2.4.md`](../requirements/version0.2.4.md)
- Related ADRs: Extends [`ADR-0001`](ADR-0001-stem-separation-player-architecture.md), [`ADR-0003`](ADR-0003-independent-karaoke-page-and-lyrics-overhaul.md), and [`ADR-0006`](ADR-0006-karaoke-stage-ux-and-catalog-modal.md).
