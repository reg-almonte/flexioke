---
status: approved
approved_by: reg
approved_at: 2026-08-28
---

# Requirements: Version 0.2.1 — Karaoke Mode Enhancements & Metadata Separation

## Problem / Motivation
In Flexioke v0.2.0, songs in the library and on the karaoke stage only have a single `title` field (often containing raw file names like `Rachel Taylor - Come Alive.mp3`). There is no structured separation between Song Title and Artist. As a result:
- The Song Library displays a static `"Stems ready (3 tracks)"` subtext instead of the artist name.
- Library search only matches against the raw title string.
- The Karaoke stage header is static and does not show upcoming queue info or song timing countdowns.
- Visual elements (active lyric highlight RGB color, font size, and "Now Singing" vs. "Up Next" transition interval) are hardcoded rather than user-customizable.
- Singers lack visual countdown cues during long instrumental intros or interludes before singing starts.

## Target Users
- **Karaoke Singers & Performers:** Want clear artist/title presentation, visual countdown cues before vocals resume, custom lyric font sizes for easy reading at a distance, and previews of what song is up next.
- **Party Hosts & Audio Curators:** Want to easily organize, search, and edit both Artist and Song Title metadata alongside LRC lyrics, and customize stage aesthetic colors and timing transitions.

## Goals
1. **Artist & Title Separation:** Separate song metadata into distinct `title` and `artist` fields across the backend model, store, and UI. Existing records default to `artist: null` / `""` with an `"Unknown Artist"` fallback.
2. **Dual-Field Library Search & Display:** Update both Stem Studio and Karaoke Mode song libraries to display Title prominently with Artist as the subtitle, enabling instant multi-field search against both attributes.
3. **Song Details & Lyrics Editor:** Expand the lyrics modal into an "Edit Song Details & Lyrics" interface allowing simultaneous editing of Title, Artist, and LRC lyrics.
4. **Dynamic Stage Banner with Alternating "Now Singing" & "Up Next":** Implement a smooth cross-fade stage banner that alternates between the active song ("Now Singing: [Title] • [Artist]") and the next queued song ("Up Next: [Title] • [Artist]") when a queue is active.
5. **Configurable Stage Settings:** Provide a configuration mechanism (with sensible defaults) for:
   - Header alternate transition interval (in seconds, default `6s`)
   - Active lyric highlight RGB / hex color (default glowing cyan `#06b6d4`)
   - Active lyric font size and baseline font scale
6. **Singing Countdown & Stage Polish:**
   - Visual countdown cue indicator (e.g. 3-beat visual pulse or countdown badge) before the first lyric line starts and during instrumental interludes (> 5s of silence before next line).
   - In-stage font size controls (`A-` / `A+`) for rapid stage scaling.
   - Song duration and remaining time countdown badge displayed in the stage header.

## Non-Goals (Out of Scope)
- Automatic web-scraping / internet metadata tagging (e.g. querying MusicBrainz/Spotify APIs for metadata).
- User authentication, multi-tenant accounts, or cloud database storage (continues using local JSON store).
- Video background playback behind lyrics (reserved for future milestone).

## Functional Requirements

### 1. Song Metadata & Persistence
- 1.1 `Job` model and `job.json` must include an optional `artist` string field (defaulting to empty string / null for legacy jobs).
- 1.2 Library listing API (`GET /api/jobs`) and job detail API must return `title` and `artist`.
- 1.3 `PATCH` / `POST` endpoint must accept updates to `title` and `artist`.

### 2. Library Presentation & Dual Search
- 2.1 Both Stem Studio and Karaoke Mode library cards must display the song `title` as the header and `artist` (or dimmed `"Unknown Artist"`) as the secondary line.
- 2.2 Library search filter must match queries against both `title` and `artist` (case-insensitive substring match).

### 3. Song Details & Lyrics Editor Modal
- 3.1 Modal must be titled **"Edit Song & Lyrics"**.
- 3.2 Top section must contain editable text inputs for **Song Title** and **Artist Name**.
- 3.3 Middle section retains the full LRC lyrics editor textarea with timestamp formatting guide.
- 3.4 Saving updates both metadata and `lyrics.lrc` atomically and immediately refreshes library cards and stage displays.

### 4. Karaoke Stage Header & "Now Singing" / "Up Next" Transition
- 4.1 When playback is active and the queue is empty: Header displays `"Now Singing: [Title] • [Artist]"` alongside total and remaining time badges.
- 4.2 When playback is active and the queue has upcoming tracks: Header smoothly cross-fades between `"Now Singing: [Title] • [Artist]"` and `"Up Next: [Next Title] • [Next Artist]"` on a configurable interval (default: 6 seconds).
- 4.3 Transition animation must be smooth (CSS opacity cross-fade, 500ms ease-in-out) without jarring layout shifts.

### 5. Configurable Stage Settings & Toolbar Controls
- 5.1 System must maintain configurable settings (stored in `localStorage` with fallback defaults):
  - `headerTransitionInterval`: integer seconds (default `6`, range `3`–`30`)
  - `activeHighlightColor`: color string/hex (default `#06b6d4`)
  - `lyricsFontSize`: base font size in px / rem (default `1.75rem` / `28px`, scalable)
- 5.2 Karaoke stage toolbar must include `A-` / `A+` font size buttons that immediately rescale the rendered lyric lines and save the preference.
- 5.3 Stage settings button / modal to customize the transition interval and active highlight glow color.

### 6. Visual Intro & Interlude Countdown Cues
- 6.1 When a track starts or when an instrumental break between lyric lines exceeds 5 seconds, display a visual countdown indicator (e.g. 3.. 2.. 1.. pulse cue) 3 seconds prior to the next active line timestamp.
- 6.2 Countdown disappears cleanly as the active lyric line begins playing.

## Acceptance Criteria
- [ ] Existing songs without an artist field display `"Unknown Artist"` gracefully without runtime errors.
- [ ] Users can edit Title and Artist in the modal; saved changes immediately reflect in both Stem Studio and Karaoke libraries.
- [ ] Searching for either artist or song title filters the library accurately in both tabs.
- [ ] If a queue exists, stage header smoothly alternates between "Now Singing" and "Up Next" every N seconds (configurable).
- [ ] Users can adjust lyric font size dynamically via `A-` / `A+` buttons on the stage.
- [ ] Active lyric glowing color and transition duration can be configured and persist across page reloads.
- [ ] Visual countdown indicator fires reliably 3 seconds before the first line and before lines following musical breaks > 5s.
- [ ] Remaining time countdown updates accurately in sync with audio playback.

## Constraints & Assumptions
- Backward compatible with existing `./data/jobs/*` directory structure and `job.json` schemas.
- Client-side configuration persisted via `localStorage` for zero-server friction.
- No external internet connectivity required for metadata or configuration.

## Open Questions
- None identified at this stage.
