---
status: approved
approved_by: reg
approved_at: 2026-09-10
---


# Version 0.4.0: Video Backgrounds, Stage Geometry Controls & Side A/B Uploads — Requirements

## Problem / Motivation
1. **Visual Immersion on Karaoke Stage:** The dark floating karaoke stage in v0.3.1 provides a clean aesthetic, but lacks dynamic visual accompaniment (such as looping cinematic background videos) commonly seen in commercial karaoke setups (DAM, JOYSOUND, TJ Media).
2. **Customizable Fullscreen Lyrics Stage Geometry:** Different display setups (projectors, TVs, wide monitors) and singer preferences require customizable lyrics bounding boxes (height, width, and vertical positioning) during fullscreen playback without altering the windowed desktop layout.
3. **Imperfect AI Separation vs. High-Quality Pre-Separated / Karaoke Tracks:** While automated 2-stage AI stem separation is versatile, users often possess official instrumental tracks (Side B) and vocal/original counterparts (Side A). Currently, users are forced through AI separation even when clean studio instrumentals already exist. A direct Side A/B upload mode enables zero-artifact karaoke playback with synchronized vocal switching.

## Target Users
- **Karaoke Singers & Home Enthusiasts:** Want vibrant, immersive visual backdrops behind floating synchronized lyrics and flexible stage sizing for external monitors/TVs.
- **Audiophiles & Content Collectors:** Want to upload studio-grade instrumental/vocal track pairs directly without processing delay or AI artifacts.

## Goals
1. **Looping Video Stage Backgrounds:**
   - Play muted, looping video backdrops beneath floating karaoke lyrics on `#karaoke-stage-card` in both windowed and fullscreen cinema modes.
   - Support dedicated video file uploads (`.mp4`, `.webm`, `.mov`, `.mkv`) and automatic local directory scanning (`/data/videos/`).
   - Allow assigning a specific background video (and optional start offset timestamp) per song in Song Details, with a fallback global default video.
   - Associate all existing library songs with `/data/videos/bg001.mp4` by default.
2. **Fullscreen Stage Geometry Controls:**
   - Provide real-time sliders in Stage Settings to customize the width, height, and vertical center position of `#karaoke-lyrics-stage` in Fullscreen / Cinema mode.
   - Enforce that default/windowed mode retains its existing standard dimensions without changes.
3. **Direct Side A / Side B Dual-Track Upload Mode:**
   - Introduce a direct dual-track upload flow in Stem Studio: Side B (Instrumental only) and optional Side A (Vocal / Original version).
   - Seamlessly toggle between Side A and Side B audio streams using the Lead Vocal button while maintaining synchronized playback timecode.
   - Dynamically adapt vocal toggle button states:
     - Side B only: Lead Vocal locked to "Off".
     - Side A only: Lead Vocal locked to "On".
     - Side A + Side B: Lead Vocal toggles between vocal and instrumental tracks. Backing vocals locked to "Off".

## Non-Goals (Out of Scope)
- Video audio playback: Background videos are strictly muted visual ambience; audio is exclusively delivered by Flexioke multi-stem/song players.
- Real-time video encoding or transcoding in backend: Videos must be playable by standard HTML5 `<video>` browser decoders.
- AI stem separation on Side A/B uploads: Side A/B files bypass Demucs/RoFormer pipelines entirely.

## Functional Requirements

### 1. Video Background Engine & Management
- **1.1 Video Storage & Auto-Discovery:**
  - Local directory `/data/videos/` stores video assets.
  - Server automatically indexes files placed in `/data/videos/` (`.mp4`, `.webm`, `.mov`, `.mkv`) and exposes them via REST API.
  - Default video `bg001.mp4` is initialized and pre-assigned to all existing songs.
- **1.2 Video Upload & API:**
  - Add API endpoint and UI action to upload new background video files to `/data/videos/`.
  - Add API endpoint to list available videos and stream video content.
- **1.3 Per-Song Video Assignment & Start Offset:**
  - Song metadata model supports `video_id` (or `video_filename`) and `video_offset_seconds` (default `0.0`).
  - Song Details & Lyrics modal provides a video selector dropdown and start offset input.
- **1.4 Karaoke Stage Video Renderer:**
  - An HTML5 `<video>` element is embedded in `#karaoke-stage-card` behind the lyrics layer (`z-index: 0`), set to `autoplay`, `loop`, `muted`, `playsinline`, and `object-fit: cover`.
  - Transparent floating lyrics and glassmorphism overlays render on top of the playing video.
  - Video starts, pauses, resumes, and seeks in synchronization with song playback. If the video reaches its end before the song, it seamlessly loops.

### 2. Fullscreen Stage Geometry Customization
- **2.1 Setting Controls in Stage Settings Modal:**
  - Add sliders for:
    - **Stage Width:** (e.g., 60% – 100%, default 98%).
    - **Stage Height / Max Height:** (e.g., 30vh – 80vh, with current 56vh as initial setting).
    - **Vertical Position / Center Offset:** (e.g., -20% to +20% vertical translation from center).
- **2.2 Scope Isolation:**
  - Geometry settings strictly apply to Fullscreen / Cinema mode via CSS custom properties.
  - Windowed/default stage retains standard responsive card constraints.
- **2.3 Persistence:**
  - Geometry values persist in `localStorage` (`flexioke_stage_config`) and apply immediately in real-time.

### 3. Direct Side A / Side B (Instrumental & Vocal) Upload Flow
- **3.1 Ingestion Selection:**
  - In Stem Studio upload section, provide an option to select upload mode: "AI Separation (Standard)" vs "Direct Side A/B (Instrumental & Vocal)".
- **3.2 Dual File Ingestion:**
  - User can upload Side B (Instrumental), Side A (Vocal/Full), or both simultaneously.
  - If a song is created with Side B only, the user can later upload/attach Side A (and vice-versa) via Song Details.
- **3.3 Playback Engine Vocal Switching:**
  - When playing a Side A/B track:
    - Both audio elements/sources are preloaded and synchronized.
    - If Lead Vocal is ON: Side A audio is unmuted/active; Side B is muted.
    - If Lead Vocal is OFF: Side B audio is active; Side A is muted.
    - Backing Vocal button is disabled (or grayed out with tooltip indicating Side A/B mode).
  - If only Side B exists: Lead Vocal button is disabled in "OFF" state.
  - If only Side A exists: Lead Vocal button is disabled in "ON" state.
- **3.4 Metadata & Library Indicators:**
  - Songs indicate `source_type: "side_ab"` with badges in Song Library and Catalog modals.

## Acceptance Criteria
1. **Video Playback & Looping:**
   - Background video plays smoothly and muted behind floating lyrics on `#karaoke-stage-card` for songs with an assigned video.
   - Videos shorter than song length loop continuously without interrupting audio.
   - Start timestamp offset correctly offsets initial video position.
   - Existing library songs default to `bg001.mp4`.
2. **Video Upload & Discovery:**
   - Uploading a video file via UI or adding a file directly to `/data/videos/` makes it selectable across songs.
3. **Stage Geometry:**
   - Adjusting width, height, and vertical alignment sliders in Stage Settings instantly alters the fullscreen lyrics box.
   - Exiting fullscreen returns stage to standard windowed layout.
4. **Side A/B Upload & Playback:**
   - Side A/B upload bypasses AI separation, creating a ready-to-play track immediately.
   - Lead Vocal button cleanly switches between Side A and Side B without audio stutter or desynchronization.
   - Single-sided uploads lock the Lead Vocal toggle appropriately.
5. **Quality & Regression:**
   - Automated pytest suite passes 100% with no regression in existing features.

## Constraints & Assumptions
- Video files in `/data/videos/` are not tracked in git (enforced in `.gitignore`).
- Browser compatibility relies on standard HTML5 video formats supported across Chrome, Safari, Firefox, and Edge.
- Side A and Side B audio files must have identical track lengths and alignment for synchronous switching.

## Open Questions
- None.
