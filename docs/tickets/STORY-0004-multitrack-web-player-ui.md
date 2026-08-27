---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# STORY-0004: Interactive Multitrack Web Player & UI

## Parent Epic
- `EPIC-0001-stem-separation-player.md`

## What it delivers
A polished single-page web player featuring 3 stacked Wavesurfer waveforms for Instrumental, Lead Vocals, and Backing Vocals, channel mixing strips (Mute, Solo, Volume), audio ingestion forms with live stage progress, searchable song library sidebar, and queue manager with automatic next-song advance.

## Acceptance Criteria
- [ ] User can upload files or paste YouTube URLs directly through an interactive ingestion panel with dynamic progress feedback.
- [ ] Multitrack player loads and renders 3 stacked waveforms with synchronized playback, global play/pause, and timeline seek.
- [ ] Individual channel strips support Mute, Solo (including multi-solo), and volume slider adjustments in real time.
- [ ] Song library panel enables instant searching and clicking a song to "Play Now" or "Add to Queue".
- [ ] Queue panel displays upcoming songs and automatically advances playback to the next song when current track ends.

## Tasks
- [ ] TASK-0010: Modern SPA Shell, Audio Ingestion Forms & Job Progress Feedback UI
- [ ] TASK-0011: Wavesurfer Multitrack Player with Channel Strip Controls (Mute, Solo, Volume)
- [ ] TASK-0012: Interactive Song Library Search & Playback Queue UI with Auto-Advance

## Blocked by
- STORY-0002: 2-Stage Audio Stem Separation Pipeline
- STORY-0003: Song Library & Playback Queue Services
