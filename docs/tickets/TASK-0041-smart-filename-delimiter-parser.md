---
status: approved
approved_by: reg
approved_at: 2026-08-31
implementation: pending
---

# TASK-0041: Smart Filename Delimiter (Title - Artist) Parser

## Parent Story
- `docs/tickets/STORY-0017-direct-audio-url-and-smart-naming.md`

## What to build
Implement smart filename parser utility function that inspects incoming filenames (from uploads and URL downloads) for `" - "` delimiter:
- Part 1 $\to$ `title` (trimmed, underscores converted to spaces, leading track numbers removed).
- Part 2 $\to$ `artist` (trimmed, file extension removed).
- Fallback to clean filename as `title` and `"Unknown Artist"` if no delimiter exists.

## Acceptance Criteria
- [ ] `Title - Artist.mp3` parses cleanly to `title="Title"` and `artist="Artist"`.
- [ ] Underscores and track prefixes (`01. `, `02 - `) are normalized.
- [ ] Applied automatically across upload and URL download routes.

## Blocked by
- None (can start immediately)
