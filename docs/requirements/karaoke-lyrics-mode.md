---
status: approved
approved_by: user
approved_at: 2026-08-27
---

# Requirements: Version 2 — Synchronized Lyrics & Dedicated Karaoke Player

## Overview
Expand Flexioke with timestamped LRC lyrics management, a dedicated full-screen Karaoke display with real-time synchronized line scrolling, smart playback interruption prompts, and simplified vocal mute/unmute toggles tailored for live singing.

## User Personas
- **Karaoke Singers / Performers:** Want a distraction-free, large lyrics display synchronized with the music, with instant buttons to mute or unmute the lead vocals for solo singing or keep backing harmonies active.
- **Audio Enthusiasts / Curators:** Want to paste timestamped LRC lyrics or plain-text lyrics for any processed song in their library so it is ready for karaoke sessions.

## Key Capabilities & User Flows

### 1. Timestamped Lyrics (.lrc) Management
- Users can click an action on any song card in the Song Library to open the **"Lyrics Editor"** modal.
- Supports standard LRC format with timestamp prefixes (e.g. `[00:05.17] Lyrics line`) or plain text.
- Saving lyrics persists the `.lrc` file under `./data/jobs/{job_id}/lyrics.lrc`.
- Provides an endpoint `GET /api/jobs/{job_id}/lyrics` and `POST /api/jobs/{job_id}/lyrics`.

### 2. Top-Level Tab Navigation: "Stem Studio" & "Karaoke Mode"
- Top navigation bar provides seamless switching between:
  - **Stem Studio (v1):** 3-channel waveform view with audio ingestion forms and detailed mixing sliders.
  - **Karaoke Mode (v2):** Center-stage synchronized lyrics view, quick vocal toggle strips, and shared queue.
- Audio playback persists without interruption when switching between tabs.

### 3. Synchronized Karaoke Display
- **Synchronized LRC Lyrics:** When playing a song with timestamped lyrics, the current singing line is magnified, highlighted with glowing colors, centered on screen, and smoothly auto-scrolled as the time advances.
- **Plain Text Fallback:** If lyrics lack timestamps, displays a clean, scrollable lyrics card.
- **No Lyrics Fallback:** If no lyrics are found, displays: *"No lyrics available. You can add lyrics from the Song Library."*

### 4. Smart Playback Interruption Guard
- If a user clicks "Play" on a song in the library while music is actively playing:
  - Pauses the active track.
  - Displays a confirmation alert: *"A track is currently playing. Starting a new track will pause current playback. The existing queue will be preserved. Proceed?"*
  - If confirmed: sets the new track as active and begins playback; upcoming queued songs remain intact.

### 5. Karaoke Quick Channel Strip Controls
- In Karaoke Mode, the transport provides dedicated quick toggles:
  - **Play / Pause**
  - **Skip Next ⏭**
  - **Lead Vocals:** Quick Mute / Unmute toggle button (turns lead vocals off for karaoke singing).
  - **Backing Vocals:** Quick Mute / Unmute toggle button (keeps or mutes backing harmonies).
  - Master Volume slider.

### 6. Shared Song Library & Queue
- Song Library search and Playback Queue remain fully functional and synchronized across both Stem Studio and Karaoke views.

## Success Criteria
- [ ] Users can save and retrieve LRC lyrics for any processed song.
- [ ] Karaoke mode syncs lyrics to audio timecode with sub-second accuracy.
- [ ] Switching between Stem Studio and Karaoke views preserves audio and playback position.
- [ ] Vocal mute toggles immediately adjust Lead and Backing vocal channels during karaoke sessions.
