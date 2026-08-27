# Decisions Log

Append-only record of every HITL approval in this project (requirements, design/ADR,
ticket scope, releases). One entry per approval, newest at the bottom.

Format:

```markdown
## YYYY-MM-DD — <what was approved>
- artifact: <path>
- approved_by: <name/email>
- notes: <anything relevant>
```

This file is intentionally empty of entries on the template's default
branch. See [TEMPLATE-CHANGELOG.md](../TEMPLATE-CHANGELOG.md) for decisions
made while building the template itself.

## 2026-08-27 — Approved Requirements: Flexioke Audio Stem Separation & Multitrack Player
- artifact: docs/requirements/stem-separation-player.md
- approved_by: user
- notes: Approved requirements covering 2-stage audio stem separation (Mel-Band RoFormer + UVR_MDXNET_KARA_2), dual ingestion (file upload + YouTube via yt-dlp), MP3 stems, and Wavesurfer multitrack web player.
## 2026-08-27 — Approved Functional Spec: Flexioke Audio Stem Separation & Multitrack Player
- artifact: docs/specs/stem-separation-player.md
- approved_by: user
- notes: Functional spec approved detailing dual ingestion endpoints (file upload and YouTube via yt-dlp), 2-stage separation pipeline, song library & search, playback queue with auto-advance, and Wavesurfer multitrack player. Stem export pended to v2.
## 2026-08-27 — Approved ADR-0001: Modular FastAPI Architecture with In-Process Async Task Pool & Multitrack Web Player
- artifact: docs/design/ADR-0001-stem-separation-player-architecture.md
- approved_by: user
- notes: Approved Option 1 (Modular FastAPI monolith with in-process async task pool, direct audio-separator and yt-dlp integrations, filesystem JSON store with in-memory library index, and Wavesurfer multitrack SPA) for zero external dependencies and local simplicity.
## 2026-08-27 — Approved Ticket Breakdown: EPIC-0001 Audio Stem Separation & Multitrack Web Player
- artifact: docs/tickets/EPIC-0001-stem-separation-player.md
- approved_by: user
- notes: Approved EPIC-0001 work breakdown comprising STORY-0001 to STORY-0004 and TASK-0001 to TASK-0012 covering backend foundation, 2-stage separation pipeline, song library & queue services, and Wavesurfer multitrack web player.
## 2026-08-27 — Approved Release: Release Manifest v0.1.0 (Flexioke MVP)
- artifact: docs/releases/v0.1.0.md
- approved_by: user
- notes: Approved Release Manifest v0.1.0 covering full EPIC-0001 implementation (Stories 1 through 4), all 12 tasks, and verification of bugfixes with clean 33/33 test suite.
## 2026-08-27 — Approved Requirements & Functional Spec: Version 2 Synchronized Lyrics & Karaoke Mode
- artifact: docs/requirements/karaoke-lyrics-mode.md, docs/specs/karaoke-lyrics-mode.md
- approved_by: user
- notes: Approved Version 2 requirements and functional spec covering timestamped .lrc lyrics management, dedicated Karaoke Mode tab, real-time synchronized active line display, smart playback interruption guard, and quick vocal mute toggles.
## 2026-08-27 — Approved ADR-0002: Client-Side LRC Lyrics Synchronization & Dedicated Karaoke Mode Architecture
- artifact: docs/design/ADR-0002-karaoke-lyrics-synchronization.md
- approved_by: user
- notes: Approved Option 1 (Client-side LRC parsing, DOM synchronizer bound to Wavesurfer timecode, atomic backend lyrics storage, top-level tab switcher, and smart play interruption guard).
## 2026-08-27 — Approved Ticket Breakdown: EPIC-0002 Synchronized Lyrics & Dedicated Karaoke Mode
- artifact: docs/tickets/EPIC-0002-karaoke-lyrics-mode.md
- approved_by: reg
- notes: Approved EPIC-0002 work breakdown comprising STORY-0005 to STORY-0007 and TASK-0013 to TASK-0018 covering backend lyrics persistence, song library lyrics editor modal, top navigation tab switcher, real-time synchronized karaoke display, and smart play interruption guard.
## 2026-08-27 — Approved ADR-0003: Independent Page System for Stem Studio & Karaoke Mode with Lyrics Engine Overhaul
- artifact: docs/design/ADR-0003-independent-karaoke-page-and-lyrics-overhaul.md
- approved_by: reg
- notes: Approved independent page systems with dedicated Song Library & Playback Queue per mode, mutual exclusion playback coordinator, and high-contrast, robust lyrics rendering engine.
## 2026-08-28 — Approved Release v0.2.0: Synchronized Lyrics & Dedicated Karaoke Player Mode
- artifact: docs/releases/v0.2.0.md
- approved_by: reg
- notes: Version 2 fully approved and released. Includes independent page systems for Stem Studio and Karaoke Mode, synchronized LRC lyrics engine with glowing active-line auto-scroll, fullscreen expand mode, quick vocal mutes, and cue-stop controls.
