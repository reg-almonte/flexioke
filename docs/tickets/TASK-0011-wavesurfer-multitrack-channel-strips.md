---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0011: Wavesurfer Multitrack Player with Channel Strip Controls (Mute, Solo, Volume)

## Parent Story
- `STORY-0004-multitrack-web-player-ui.md`

## What to build
Integrate Wavesurfer.js v7 and the MultiTrack plugin to render 3 stacked, interactive waveforms (Instrumental, Lead Vocals, Backing Vocals) with master transport controls (Play/Pause, Seekbar, Master Volume) and per-channel controls (Mute, Solo with multi-solo state matrix, and Gain slider).

## Acceptance Criteria
- [ ] Loads and renders 3 stacked waveforms aligned in time.
- [ ] Global Play/Pause and scrubber seek all tracks in perfect synchronization.
- [ ] Mute toggle silences specific tracks; Solo button isolates selected tracks and silences non-soloed tracks; un-soloing restores prior mute states.
- [ ] Per-track volume slider scales individual stem volume in real time.

## Blocked by
- TASK-0010: Modern SPA Shell, Audio Ingestion Forms & Job Progress Feedback UI
