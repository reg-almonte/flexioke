---
status: approved
approved_by: user
approved_at: 2026-08-27
---

# Flexioke: Audio Stem Separation & Multitrack Web Player

## Problem / Motivation
Singers, musicians, and karaoke enthusiasts often want to isolate or customize specific parts of a song—such as removing lead vocals while keeping backing harmonies, or isolating vocal harmonies for rehearsal. Existing generic vocal removers usually produce only a binary instrumental/vocal split, lacking granular control over backing vocals versus lead vocals. Furthermore, desktop separation tools often require complex setup and lack an instant, browser-based multitrack player to audition, balance, and manage a playlist/queue of processed songs.

Flexioke provides an end-to-end web application that ingests audio files or YouTube links, performs a 2-stage AI stem separation (Instrumental, Lead Vocals, Backing Vocals), indexes processed tracks in a searchable song library, and presents the tracks in an interactive, polished multitrack web player with real-time mute, solo, volume control, and dynamic song queuing.

## Target Users
- **Karaoke Singers & Performers:** Who need customized backing tracks with or without backing vocals and want a continuous session queue.
- **Vocalists & Choir Members:** Who want to isolate lead or backing vocal harmonies for practice from a library of processed songs.
- **Audio Enthusiasts & DJs:** Who want quick access to multi-stem playback and queue management.

## Goals
- Provide dual ingestion: direct audio file upload (`.mp3`, `.wav`, `.m4a`, `.flac`) and YouTube URL extraction via `yt-dlp`.
- Implement a 2-stage audio separation pipeline:
  - **Stage 1:** Separate raw audio into Instrumental (Music) and Combined Vocals using Mel-Band RoFormer.
  - **Stage 2:** Separate Combined Vocals into Lead Vocals and Backing Vocals using UVR_MDXNET_KARA_2.
- Generate and store 3 distinct stems per job encoded as MP3 for efficient streaming: `Instrumental`, `Lead Vocals`, and `Backing Vocals`.
- Provide a persistent **Song Library & History:**
  - Index all completed processed songs.
  - Search and filter songs by title or source.
- Provide a dynamic **Playback Queue:**
  - Queue songs from the library for continuous playback.
  - View queue, play next, reorder, and remove songs.
- Deliver a sleek, modern, responsive multitrack player with 3 stacked interactive waveforms (using Wavesurfer.js and MultiTrack plugin).
- Enable global playback controls (Play/Pause, seek/timeline, master volume) and per-track controls (Mute, Solo, Volume slider).
- Deliver a clear job processing status interface with lightweight REST polling.

## Non-Goals (Out of Scope / Pended for v2)
- Stem file export and .zip bundle packaging (Pended to v2).
- Multi-user authentication, accounts, and billing/payment subscriptions.
- 4-stem or 6-stem drum/bass/other separation.
- Real-time lyrics transcription or synchronized karaoke lyric rendering (CDG/LRC).
- Complex cloud cluster scaling / multi-worker distributed message brokers.
- Live microphone recording or real-time pitch correction.

## Functional Requirements
1. **Audio Ingestion:**
   - The system shall accept local audio uploads in common formats (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`).
   - The system shall accept valid YouTube video/music URLs and download the audio stream via `yt-dlp`.
   - The system shall validate inputs and reject unsupported formats or invalid URLs with clear error messages.
2. **Stem Separation Processing Pipeline:**
   - The system shall create an isolated job directory for each separation request with a unique Job ID.
   - **Stage 1 Separation:** The system shall execute `audio-separator` with Mel-Band RoFormer to produce `instrumental` and `vocals` stems.
   - **Stage 2 Separation:** The system shall pass the generated `vocals` stem into `audio-separator` with `UVR_MDXNET_KARA_2` to produce `lead_vocals` and `backing_vocals` stems.
   - The system shall output and store the 3 final stems as `.mp3` files (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`).
   - The pipeline shall record job states: `queued`, `downloading`/`uploading`, `separating_stage_1`, `separating_stage_2`, `completed`, `failed`.
3. **Song Library & Search:**
   - The system shall maintain an index of all completed separation jobs.
   - The user shall be able to view a list of all processed songs with title, source, duration, and completion date.
   - The user shall be able to search and filter the song library in real time by song title or filename.
4. **Playback Queue Management:**
   - The user shall be able to click on any song in the library to load it into the active player or add it to the Playback Queue.
   - The user shall be able to view the upcoming queue list, remove tracks from the queue, and skip to the next track in the queue upon song completion.
5. **Multitrack Web Player:**
   - The frontend shall render 3 synchronized, stacked waveform tracks corresponding to Instrumental, Lead Vocals, and Backing Vocals.
   - The player shall provide synchronous playback where all unmuted tracks play in exact lockstep.
   - The player shall provide a master transport bar: Global Play/Pause, Seek scrubber with current time / total duration display, and Master Volume.
   - The player shall provide individual track channel strips with:
     - Track name label (Instrumental, Lead Vocals, Backing Vocals).
     - Mute / Unmute toggle button.
     - Solo toggle button (soloing one or more tracks mutes all non-soloed tracks).
     - Individual track volume slider (0% to 100%).
6. **Job Status & Error Handling:**
   - The frontend shall poll the backend job status endpoint (`GET /api/jobs/{job_id}`) periodically while processing is active.
   - In case of failure (e.g., download failed, separation error, corrupted file), the system shall record the error message and display a clear error state in the UI.

## Acceptance Criteria
- [ ] User can upload an audio file or paste a YouTube URL to initiate separation.
- [ ] The backend executes both separation stages and produces 3 valid MP3 stem files (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`).
- [ ] Completed jobs appear in the Song Library with metadata (title, duration, date).
- [ ] User can search the Song Library by title/query and filter results in real time.
- [ ] User can add songs from the library to the Playback Queue.
- [ ] Multitrack player renders 3 stacked waveforms with synchronized playback, seek, mute, solo, and volume controls.
- [ ] When a song finishes playing, the player automatically transitions to the next song in the queue (if present).
- [ ] Invalid inputs or pipeline failures return descriptive error messages in the UI.

## Constraints & Assumptions
- **Backend Environment:** Python FastAPI.
- **Core Libraries:** `audio-separator` (Mel-Band RoFormer & UVR_MDXNET_KARA_2 models), `yt-dlp`, `ffmpeg`.
- **Frontend Stack:** HTML5, TailwindCSS, JavaScript with Wavesurfer.js + MultiTrack plugin.
- **Hardware Acceleration:** Automatic GPU/MPS acceleration if supported and available, with CPU fallback.
- **Local Storage:** Stems and job metadata persist indefinitely on disk under `./data/jobs/<job_id>/`.

## Open Questions
None.
