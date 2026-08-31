---
status: approved
approved_by: reg
approved_at: 2026-08-28
---

# ADR-0004: Unified Song Metadata Model Extension & Reactive Karaoke Stage Enhancements

## Context
In Flexioke v0.2.0, songs in the local job store and library only track a single `title` attribute, lacking structured `artist` metadata. Additionally, the Karaoke stage header is static and does not communicate upcoming queue information or song timing countdowns, active lyric highlight styling is hardcoded, and singers do not have visual countdown cues prior to the start of singing lines after long instrumental breaks.

The functional specification (`docs/specs/karaoke-mode-enhancements.md`) outlines requirements to:
1. Separate song metadata into `title` and `artist` across backend storage and frontend displays with zero-friction backwards compatibility.
2. Enable dual-field searching across both Title and Artist.
3. Provide a unified "Edit Song Details & Lyrics" modal to edit Title, Artist, and LRC lyrics simultaneously.
4. Implement a dynamic stage header that smoothly cross-fades between `"Now Singing: [Title] • [Artist]"` and `"Up Next: [Next Title] • [Next Artist]"`.
5. Deliver configurable stage settings (header transition interval, active lyric RGB highlight glow color, base lyrics font size with toolbar `A-` / `A+` buttons).
6. Provide visual countdown intro and interlude cues before singing begins.

## Decision
Adopt **Option 1: Unified REST Model Extension with Client-Side Reactive Stage Coordinator & LocalStorage Preferences**.

### Architectural Details:
1. **Backend Metadata Extension (`src/models.py`, `src/services/job_store.py`, `src/api/jobs.py`):**
   - Extend Pydantic `Job` schema with `artist: Optional[str] = None`.
   - Update `JobStore` serialization and deserialization routines to preserve `artist`. Existing legacy `job.json` files missing `artist` load as `None` without validation exceptions.
   - Implement `PATCH /api/jobs/{job_id}` accepting `JobUpdateMetadataRequest(title=..., artist=...)` to update and persist metadata.
2. **Dual-Field Search & Card Rendering (`src/static/library_queue.js`, `src/templates/index.html`):**
   - Update `JobCard` template to render `title` on the primary header row and `artist || 'Unknown Artist'` on the secondary subtitle row.
   - Update library search filtering to match queries against `title.toLowerCase()` and `(artist || 'Unknown Artist').toLowerCase()`.
3. **Unified Edit Modal (`src/static/library_queue.js`):**
   - Transform the lyrics modal into an "Edit Song Details & Lyrics" modal with title and artist input inputs above the LRC editor.
   - When the user saves, perform atomic API calls to update metadata and lyrics, updating in-memory state and re-rendering active cards and stage headers.
4. **Reactive Karaoke Stage Coordinator (`src/static/karaoke_stage.js`):**
   - **Alternating Header Manager:** Manages a timer cycle that executes CSS opacity cross-fades between "Now Singing" and "Up Next" whenever 1 or more songs exist in the playback queue.
   - **Countdown Cue Controller:** Inspects `currentTime` vs `T_next` lyric line timestamp; renders a 3-dot visual pulse badge (`● ○ ○` -> `● ● ○` -> `● ● ●`) during the 3 seconds preceding the first line or lines following an instrumental break > 5s.
   - **Dynamic Stage Styler & Toolbar Controls:** Binds `--karaoke-font-size` and `--karaoke-highlight-color` CSS custom properties, allowing live adjustments via `A-` / `A+` toolbar buttons and settings modal, persisted to `localStorage`.

## Options Considered

### Option 1: Unified REST Model Extension + Reactive Client Stage Coordinator with LocalStorage Settings (Chosen)
- **Pros:**
  - Zero external dependencies or database overhead; keeps the single-process local architecture clean and portable.
  - 100% backward compatible with existing jobs and file-based storage.
  - Sub-millisecond response time for stage animations, font scaling, and countdown visual cues since state is coordinated client-side directly with the Web Audio / Wavesurfer clock.
  - Settings persist instantly per client browser session without extra server endpoints.
- **Cons:**
  - Stage visual preferences (font size, highlight color) are stored per browser rather than centrally in a server database.

### Option 2: Server-Side Preferences Store (`config.json`) + WebSocket Stage Synchronization (Rejected)
- **Pros:**
  - Centralized stage preferences that synchronize across multiple remote browser displays.
- **Cons:**
  - Significant architectural complexity, requiring new configuration endpoints, server file locking, and WebSocket channels for visual state.
  - Unnecessary overhead for local desktop karaoke deployments.

## Consequences
- `Job` data model now includes `artist: Optional[str] = None`.
- `job.json` files will serialize `artist` upon update.
- Existing job records without `artist` continue to load flawlessly with `"Unknown Artist"` fallback.
- Client applications gain dynamic header cross-fading, stage countdown cues, and real-time font resizing without any audio playback glitches.

## Related
- Functional spec: `docs/specs/karaoke-mode-enhancements.md`
- Requirement: `docs/requirements/karaoke-mode-enhancements.md`
- Supersedes / related ADRs: Related to `docs/design/ADR-0001-stem-separation-player-architecture.md`, `docs/design/ADR-0002-karaoke-lyrics-synchronization.md`, `docs/design/ADR-0003-independent-karaoke-page-and-lyrics-overhaul.md`
