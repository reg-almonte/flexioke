---
status: pending-approval
approved_by:
approved_at:
---

# Version 0.2.4 — Stem Studio Upgrade & Separation Job Queue

## Problem / Motivation
1. **Flaky Audio Ingestion:** The current YouTube audio extraction tool (`yt-dlp`) frequently fails with `403 Forbidden` bot detection errors in local environments, preventing reliable remote audio importation.
2. **Blocking Single-Task Pipeline:** Users cannot upload or queue additional songs while a separation job is actively running on the GPU.
3. **Sidebar Space Contention:** Stem Studio left sidebar cards ("Add Song", "Studio Song Library", "Studio Queue") take substantial vertical space and cannot be collapsed when focusing on multitrack waveforms.
4. **Limited Studio Library Navigation:** Unlike Karaoke Mode's Jukebox Modal, Stem Studio lacks an expanded full-screen catalog modal with sorting and direct access to metadata/lyrics editing.
5. **Manual Title & Artist Entry:** Uploaded filenames with standard naming formats (e.g. `Song Title - Artist.mp3`) require manual editing to split Title and Artist.
6. **No Scratchpad for Reference Links:** Producers often need to keep track of lyric sites, source links, and notes while working in Stem Studio.
7. **No Combined Stem Export:** Users have no 1-click method to download their separated stems and lyrics as a single package.
8. **Unorganized Raw Audio Storage:** Raw input files remain scattered across individual job folders after separation finishes without centralized archiving for future maintenance or pruning.

## Target Users
- Audio producers, karaoke track creators, and musicians using Stem Studio to separate, inspect, edit, and organize multitrack stems.

## Goals
1. Replace YouTube extraction with a resilient **Direct Audio URL Downloader** accepting valid `.mp3`, `.wav`, `.m4a`, `.flac`, and generic audio stream URLs.
2. Provide **Collapsible Accordion Cards** in the Stem Studio sidebar with persistent toggle states.
3. Introduce an **Expanded Studio Song Catalog Modal** with real-time search, sorting, and direct `▶ Play`, `➕ Queue`, and `📝 Edit Details/Lyrics` actions.
4. Configure the Studio Song Library to default to **Recently Added** (`created_at` descending) sort order.
5. Implement **Multi-File Batch Upload & Asynchronous Separation Job Queue** (FIFO queue, sequential 1-at-a-time GPU execution, live queue position, and cancel buttons).
6. Enable **Smart Title & Artist Auto-Extraction** from filenames containing `" - "` delimiters.
7. Add a persistent **Stem Studio Notes / Scratchpad Modal** (accessible via header button) with markdown/link support.
8. Provide a **Combined Stem Export (`.zip`)** endpoint and UI button packaging separated stems (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`) and `lyrics.lrc` (if available).
9. Add a **Delete Track** action with confirmation prompt inside the Edit Details / Lyrics modal.
10. Allow **Active / Queued Job Cancellation** directly from the processing queue UI.
11. Automatically **Archive Raw Input Audio** into a centralized `./data/archive/` folder once stem separation completes.

## Non-Goals (Out of Scope)
- Individual stem file download buttons (only combined `.zip` package is offered).
- Parallel / multi-GPU concurrent separation processing (sequential FIFO queue is used to avoid GPU VRAM exhaustion and out-of-memory errors).
- Automatic cloud storage syncing (remains local filesystem-based).

## Functional Requirements
1. **Direct Audio URL Downloader:**
   - URL input field replaces the YouTube card.
   - Validates URL syntax and initiates streaming download with background task progress.
   - Saves file to `./data/jobs/{job_id}/input.mp3` and automatically enters the separation queue.
2. **Collapsible Sidebar Accordions:**
   - Three sidebar cards in Stem Studio (`Add Song for Separation`, `Studio Song Library`, `Studio Queue`) feature a toggle header with chevron icon (`▾` / `▸`).
   - Clicking a header smoothly toggles collapse/expand of its body.
   - Collapsed states are remembered across page reloads in `localStorage["flexioke_studio_accordions"]`.
3. **Expanded Studio Song Catalog Modal:**
   - Expand button (`⛶`) in the Studio Song Library header opens `#studio-catalog-modal`.
   - Includes real-time search bar with quick clear (`✕`), sort selector (`Latest Added`, `Title A-Z/Z-A`, `Artist A-Z`), total song count, and actions: `▶ Play Now`, `➕ Add to Queue`, and `📝 Edit Details / Lyrics`.
4. **Studio Song Library Default Sort:**
   - Studio Song Library automatically renders in descending order of `created_at` (newest songs at the top).
5. **Multi-File Upload & FIFO Separation Queue:**
   - File input accepts multiple audio files (`multiple accept="audio/*"`), and a dashed drag-and-drop zone accepts single or multiple dropped files.
   - Submitting multiple files or URLs assigns each a unique `job_id` with `status: QUEUED`.
   - The queue worker processes jobs sequentially: 1 active `PROCESSING` job at a time, while others wait in `QUEUED` state.
   - Live queue status list displays the active job with stage progress and pending jobs with their position (e.g. `Position #2 in queue`).
6. **Smart Title & Artist Filename Parser:**
   - If an uploaded or downloaded filename contains `" - "`:
     - Part 1 is assigned to `title` (trimmed, underscores converted to spaces).
     - Part 2 is assigned to `artist` (trimmed, extension removed).
   - If no `" - "` delimiter exists, full filename without extension becomes `title`, and `artist` defaults to `"Unknown Artist"`.
7. **Stem Studio Scratchpad Notes Modal (Option B):**
   - A `📝 Notes` button in the Stem Studio navigation/header bar opens a modal scratchpad.
   - Contains a rich textarea for saving notes, resource links, and lyrics sources.
   - Content auto-saves on input to `localStorage["flexioke_studio_notes"]` with clickable links.
8. **Combined Stem & Lyrics `.zip` Export:**
   - Adds a `📦 Export Stems (.zip)` button on the Stem Studio multitrack controls and in the track menu.
   - Backend endpoint `GET /api/jobs/{job_id}/export/zip` generates a zip archive containing:
     - `instrumental.mp3`
     - `lead_vocals.mp3`
     - `backing_vocals.mp3`
     - `lyrics.lrc` (if lyrics exist for the song)
9. **Track Deletion:**
   - A `🗑 Delete Track` button in the Edit Details / Lyrics modal prompts for confirmation, then calls `DELETE /api/jobs/{job_id}` to remove all job files and purge from the library.
10. **Separation Job Cancellation:**
    - A `✕ Cancel` button on queued or processing items terminates the job and removes it from the separation queue.
11. **Post-Processing Audio Archiving:**
    - When `run_separation_pipeline(job_id)` successfully finishes, the original input audio file is moved to `./data/archive/{job_id}_{original_filename}`.

## Acceptance Criteria
- [ ] Direct audio URL download successfully ingests remote MP3/audio files into the pipeline.
- [ ] Stem Studio sidebar cards collapse and expand cleanly with persistent state.
- [ ] Studio Song Library features an expanded catalog modal with search, sort, and `📝 Edit Details/Lyrics`.
- [ ] Studio Song Library sorts by latest added song by default.
- [ ] Multiple files can be selected or dragged-and-dropped simultaneously, queuing sequentially without GPU race conditions.
- [ ] Filenames formatted as `Title - Artist.mp3` auto-populate Title and Artist fields.
- [ ] Notes button in Stem Studio header opens a persistent auto-saving scratchpad.
- [ ] Clicking `Export Stems (.zip)` downloads a zip containing all 3 stem MP3s and `lyrics.lrc` (if present).
- [ ] Deleting a track purges its stems, metadata, and lyrics from disk and UI.
- [ ] Cancelling a queued job removes it from the processing queue immediately.
- [ ] Finished jobs have their original input files safely moved to `./data/archive/`.

## Constraints & Assumptions
- Audio separation relies on existing 2-stage PyTorch pipeline (Mel-Band RoFormer + UVR_MDXNET_KARA_2).
- Batch processing queue runs strictly sequentially in-process to guarantee stability on 8GB/16GB Unified Memory Apple Silicon and CUDA GPUs.

## Open Questions
- None. All 8 items and architectural decisions aligned with user directives.
