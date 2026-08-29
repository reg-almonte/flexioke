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
## 2026-08-28 — Approved Requirements: Version 0.2.1 Karaoke Mode Enhancements & Metadata Separation
- artifact: docs/requirements/karaoke-mode-enhancements.md
- approved_by: reg
- notes: Approved requirements covering structured artist/title separation with backwards-compatible migration, unified dual-field search, song & lyrics editor modal, configurable stage settings (transition interval, highlight color, font size), remaining time badge, and visual countdown intro/interlude cues.
## 2026-08-28 — Approved Functional Spec: Version 0.2.1 Karaoke Mode Enhancements & Metadata Separation
- artifact: docs/specs/karaoke-mode-enhancements.md
- approved_by: reg
- notes: Functional spec approved detailing backward-compatible job model schema migration, atomic metadata/lyrics update endpoints, dual-field client-side search, CSS-animated alternating header transitions, intro/interlude visual countdown cues, and client-persisted stage settings.
## 2026-08-28 — Approved ADR-0004: Unified Song Metadata Model Extension & Reactive Karaoke Stage Enhancements
- artifact: docs/design/ADR-0004-karaoke-metadata-and-stage-enhancements.md
- approved_by: reg
- notes: Approved Option 1 (Unified REST Model Extension with Client-Side Reactive Stage Coordinator & LocalStorage Preferences) for zero external dependencies, robust backwards-compatible job.json migration, and real-time client-side stage controls.
## 2026-08-28 — Approved Ticket Breakdown: EPIC-0003 Karaoke Mode Enhancements & Metadata Separation
- artifact: docs/tickets/EPIC-0003-karaoke-metadata-and-stage-enhancements.md
- approved_by: reg
- notes: Approved ticket breakdown comprising STORY-0008 to STORY-0010 and TASK-0019 to TASK-0025 covering backend model/store/API metadata extensions, song & lyrics editor modal, dual-field library search, alternating stage header, visual countdown cues, and stage customization controls.
## 2026-08-29 — Approved Release v0.2.1: Karaoke Mode Enhancements & Metadata Separation
- artifact: docs/releases/v0.2.1.md
- approved_by: reg
- notes: Version 0.2.1 fully approved and released. Includes Song Title and Artist metadata separation with backwards compatibility, unified song details & lyrics modal, dual-field search, auto-sort by song title, alternating stage banner ("Now Singing" ⟷ "Up Next"), timecode countdown badge, visual 3-beat countdown cues, and customizable stage settings modal.
## 2026-08-29 — Approved Requirements: Version 0.2.2 Karaoke UI Refinements & Stage Controls
- artifact: docs/requirements/karaoke-ui-refinements.md
- approved_by: reg
- notes: Requirements approved for Version 0.2.2 covering simultaneous Now Singing & Up Next header, modernized transport bar with expanding volume slider and restart button, click-to-play on stage background, queue reordering (up/down) with top position in sidebar, and auto-hiding navbar.
## 2026-08-29 — Approved Functional Spec: Version 0.2.2 Karaoke UI Refinements & Stage Controls
- artifact: docs/specs/karaoke-ui-refinements.md
- approved_by: reg
- notes: Functional spec approved detailing simultaneous dual stage header with marquee, bottom transport bar (expanding volume, toggleable timecode, restart, settings, expand/collapse), stage background click-to-play with bounded lyric pills, queue reorder endpoint (POST /api/queue/reorder), and auto-hiding navbar.
## 2026-08-29 — Approved ADR-0005: Directional Queue Reordering API with Reactive Stage Transport & CSS Marquee Engine
- artifact: docs/design/ADR-0005-karaoke-stage-transport-queue-reordering.md
- approved_by: reg
- notes: Approved Option 1 (Directional Queue Reordering API with Reactive DOM Event Bus & CSS Marquee Engine) providing atomic thread-safe queue mutation, simultaneous dual stage header with marquee, modernized transport bar with expanding volume and restart, stage click-to-play, and auto-hiding navbar.


