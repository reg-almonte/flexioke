---
status: approved
approved_by: user
approved_at: 2026-08-27
---

# ADR-0002: Client-Side LRC Lyrics Synchronization & Dedicated Karaoke Mode Architecture

## Status
Pending Approval

## Context
Version 2 introduces timestamped LRC lyrics storage, a dedicated full-screen Karaoke stage with real-time active line highlighting and smooth scrolling, quick vocal toggle strips for singers, and a smart play interruption guard.

## Options Considered

### Option 1: Client-Side LRC Parser & DOM Synchronizer with Atomic Backend Store (Recommended)
- **Backend:** `LyricsStore` manages `.lrc` text files in each job's directory (`./data/jobs/{job_id}/lyrics.lrc`) via `GET/POST /api/jobs/{job_id}/lyrics`.
- **Frontend Architecture:**
  - `LrcParser`: Parses LRC timestamps (`[mm:ss.xx]`) into structured intervals `[{ time: float, text: str }]`.
  - `KaraokeSynchronizer`: Listens directly to `FlexiokePlayer`'s audio `timeupdate` events to compute the active line in $O(\log N)$ / $O(1)$.
  - `KaraokeStageRenderer`: Magnifies active lyrics, applies gradient glow effects, and auto-scrolls the active line to vertical center stage with smooth CSS scrolling.
  - `SmartInterruptionGuard`: Intercepts song starts during active playback to prompt the user while preserving the queue.
- **Pros:** Zero network latency during playback, sub-millisecond visual sync, zero server CPU overhead, persistent audio across tab switches.
- **Cons:** Client handles DOM line rendering and scrolling.

### Option 2: Server-Sent Events (SSE) / WebSocket Broadcast
- Server maintains timecode clock and broadcasts current lyric lines over a live WebSocket stream.
- **Pros:** Server controls lyrics timeline.
- **Cons:** Network jitter causes desynchronization with audio; massive server resource overhead; complex state reconciliation.

## Decision
Adopt **Option 1**: Pure client-side LRC parsing and DOM synchronization connected to the Wavesurfer audio clock, backed by atomic file-based lyrics storage.

## Consequences
- **Positive:** Perfect audio-to-lyric synchronization with zero latency; instantaneous tab switching between Stem Studio and Karaoke Mode; simple file-based storage.
- **Negative:** LRC format parsing must handle malformed timestamps gracefully (handled by fallback plain-text rendering).
