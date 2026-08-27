---
status: fixed
filed_at: 2026-08-27
---

# Bug Report: Stem Separation Player — Playback & Queue Auto-Play Issues

## Related
- Functional Spec: `docs/specs/stem-separation-player.md`
- Requirements: `docs/requirements/stem-separation-player.md`
- Stories: `docs/tickets/STORY-0003-song-library-playback-queue.md`, `docs/tickets/STORY-0004-multitrack-web-player-ui.md`

## Summary
Testing of the web player identified 3 related playback and queue automation defects:
1. **Library "Play Now" Does Not Autoplay:** Clicking "Play" on a song in the library loads the stems into the waveforms but requires manually pressing the global transport Play button. *(Fix applied, pending verification)*
2. **Queue Auto-Advance Cleared Queue Without Playing Next Track:** When a song finishes, multiple `finish` events or unhandled async decoding cause the next queued track not to play and the queue to be prematurely drained. *(Fix applied, pending verification)*
3. **"Skip Next" Button Does Not Autoplay:** Clicking "Skip Next" loads the next queued song but does not start playback automatically. *(Fix applied, pending verification)*

## Failures & Applied Fixes

### Failure 1: Asynchronous WaveSurfer Decoding Prevents Autoplay on Song Load
- **Fix Applied:** In `src/static/player.js`, added `autoPlayPending` state tracking that triggers `play()` immediately once all multitrack stems finish decoding and fire the `ready` event.

### Failure 2: Duplicate `finish` Event Triggers and Premature Queue Draining
- **Fix Applied:** In `src/static/player.js` and `src/static/library_queue.js`, added a `finishedFired` debounce lock to emit exactly one `flexioke:track-ended` event per song, alongside an `isAdvancing` lock in `PlaybackQueueManager.advanceNext()` to prevent multiple rapid queue pops.

### Failure 3: "Skip Next" Lacks Synchronized Ready-to-Play Handling
- **Fix Applied:** In `src/static/library_queue.js`, updated `advanceNext()` and `playNow()` to call `loadSong(state.current_track, true)` to automatically trigger playback once decoded.
