---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0010: Modern SPA Shell, Audio Ingestion Forms & Job Progress Feedback UI

## Parent Story
- `STORY-0004-multitrack-web-player-ui.md`

## What to build
Build the modern, responsive web application shell using HTML5, TailwindCSS, and JavaScript with tabbed audio ingestion (file upload drag & drop and YouTube URL input), form submission handlers, and a dynamic progress card displaying real-time pipeline status via REST polling.

## Acceptance Criteria
- [ ] Responsive, dark-themed dashboard layout styled with TailwindCSS.
- [ ] Tabbed ingestion view supporting file drop/browse and YouTube URL input.
- [ ] Submitting a job initiates polling and displays visual step indicators (Ingesting $\rightarrow$ Stage 1 $\rightarrow$ Stage 2 $\rightarrow$ Ready).
- [ ] Displays clear error alerts with retry option on failure.

## Blocked by
- TASK-0007: End-to-End Separation Worker Orchestration & Stem Streaming Endpoints
