---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# STORY-0003: Song Library & Playback Queue Services

## Parent Epic
- `EPIC-0001-stem-separation-player.md`

## What it delivers
A persistent song catalog and playlist queue manager allowing users to search previously processed songs by title/source, retrieve full stem collections, and manage an ordered playback queue.

## Acceptance Criteria
- [ ] Completed jobs are indexed and discoverable in the Song Library.
- [ ] `GET /api/jobs` returns all completed songs with support for real-time text query filtering (`?q=...`).
- [ ] Playback queue state and ordering operations (enqueue, dequeue, clear, next) are supported cleanly.

## Tasks
- [ ] TASK-0008: Song Library Indexing & Search API
- [ ] TASK-0009: Playback Queue Service & Playlist State Logic

## Blocked by
- STORY-0001: Backend Foundation, Job Manager & Ingestion APIs
