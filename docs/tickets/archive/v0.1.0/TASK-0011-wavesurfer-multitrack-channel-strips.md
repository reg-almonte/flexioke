---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0011: Wavesurfer Multitrack Player with Channel Strip Controls (Mute, Solo, Volume)

## Parent Story
- `STORY-0004-multitrack-web-player-ui.md`

## What to build
Integrate Wavesurfer.js v7 and the MultiTrack plugin to render 3 stacked, interactive waveforms (Instrumental, Lead Vocals, Backing Vocals) with master transport controls (Play/Pause, Seekbar, Master Volume) and per-channel controls (Mute, Solo with multi-solo state matrix, and Gain slider).

## Acceptance Criteria
- [x] Loads and renders 3 stacked waveforms aligned in time.
- [x] Global Play/Pause and scrubber seek all tracks in perfect synchronization.
- [x] Mute toggle silences specific tracks; Solo button isolates selected tracks and silences non-soloed tracks; un-soloing restores prior mute states.
- [x] Per-track volume slider scales individual stem volume in real time.

## Blocked by
- TASK-0010: Modern SPA Shell, Audio Ingestion Forms & Job Progress Feedback UI

## Implementation
- **Branch:** `story/STORY-0004-multitrack-web-player-ui`
- **Player Core:** `src/static/player.js` (`FlexiokePlayer`) providing synchronized 3-track WaveSurfer rendering, scrubbing, global Play/Pause, timecode tracking, and real-time Mute/Solo/Volume matrix calculation.
- **Tests:** `tests/test_player_module.py` (2 tests passing, 31 suite-wide).
