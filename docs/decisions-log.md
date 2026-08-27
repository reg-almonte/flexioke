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
