---
status: approved
approved_by: reg
approved_at: 2026-08-28
implementation: pending
---

# STORY-0009: Song Details & Lyrics Editor Modal & Dual-Field Search

## Parent Epic
- `docs/tickets/EPIC-0003-karaoke-metadata-and-stage-enhancements.md`

## What it delivers
Provides a unified "Edit Song Details & Lyrics" interface allowing users to edit Title, Artist, and LRC lyrics in one modal. Updates library cards across Stem Studio and Karaoke Mode to display Title as header and Artist as subtitle, with instant search matching against both fields.

## Acceptance Criteria
- [ ] Clicking "Edit Lyrics" or "Edit Song" opens the unified modal with fields for Title, Artist, and Lyrics.
- [ ] Saving updates both metadata and lyrics, updating in-memory store and re-rendering cards and active headers immediately.
- [ ] Song library cards in both Stem Studio and Karaoke Mode show the Title in bold and Artist below (or dimmed "Unknown Artist").
- [ ] Library search input filters cards matching either Title or Artist.

## Tasks
- [ ] TASK-0021: Unified "Edit Song Details & Lyrics" Modal UI & Atomic Save Workflow
- [ ] TASK-0022: Library Cards Artist Subtitle Display & Dual-Field Search Filter

## Blocked by
- STORY-0008: Backend Song Metadata Model, Persistence & Patch API
