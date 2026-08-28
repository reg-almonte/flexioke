---
status: approved
approved_by: reg
approved_at: 2026-08-28
---

# Functional Specification: Version 0.2.1 — Karaoke Mode Enhancements & Metadata Separation

## Related Requirements
- `docs/requirements/karaoke-mode-enhancements.md`

## Functional Flows

### Flow 1: Song Metadata Persistence & Migration
- **Trigger:** System startup, library listing (`GET /api/jobs`), job loading, or file ingestion.
- **Behavior:**
  1. Backend reads `job.json` for each job directory.
  2. If `artist` key is absent or `null`, it is treated as `""` without crashing or corrupting data.
  3. API responses include both `title: string` and `artist: Optional[str]`.
  4. On audio ingestion (upload or YouTube extraction), default `title` is sanitized from source name; `artist` is initialized to `null` or extracted if formatted as `"Artist - Title"`.

### Flow 2: Editing Song Details & Lyrics
- **Trigger:** User clicks `"Edit Lyrics"` / `"Edit Song"` on a song card or transport menu.
- **Behavior:**
  1. Modal opens with title **"Edit Song Details & Lyrics"**.
  2. Inputs pre-populated with:
     - **Song Title** (text input)
     - **Artist Name** (text input, placeholder: *"e.g. Queen, Adele, etc."*)
     - **Lyrics** (multiline textarea with LRC formatting guide)
  3. User modifies title, artist, or lyrics and clicks **"Save Changes"**.
  4. Client submits metadata update payload (`PATCH /api/jobs/{job_id}` or `POST /api/jobs/{job_id}/metadata`) and lyrics payload (`POST /api/jobs/{job_id}/lyrics`).
  5. On 200 OK:
     - In-memory library state updates.
     - Song cards in both Stem Studio and Karaoke Mode re-render.
     - If the modified song is currently loaded on stage, the stage header and lyrics reload immediately.
     - Modal closes with a success confirmation toast.

### Flow 3: Dual-Field Library Search
- **Trigger:** User enters text into search filter on either Stem Studio or Karaoke Mode tab.
- **Behavior:**
  1. Search input captures query in real time on `input` event.
  2. Filter function checks each job:
     - `matches = (job.title.toLowerCase().includes(query) || (job.artist && job.artist.toLowerCase().includes(query)))`
  3. If `job.artist` is empty/null, query also matches against `"unknown artist"`.
  4. Matching cards are rendered; non-matching cards are hidden.
  5. If no items match, displays `"No songs found matching '<query>'."`

### Flow 4: Dynamic Stage Header & "Now Singing" / "Up Next" Transition
- **Trigger:** Track playback starts or queue state changes on the Karaoke Stage.
- **Behavior:**
  1. If playback queue is **empty**:
     - Header displays static text: `"Now Singing: [Title] • [Artist]"` (or `"Unknown Artist"` if empty).
     - Displays elapsed time and remaining countdown: `MM:SS / MM:SS (-MM:SS)`.
  2. If playback queue contains **1 or more upcoming tracks**:
     - Cycle timer initiates with duration = `config.headerTransitionInterval` (default `6s`).
     - Every interval, the header executes a 250ms CSS fade-out transition.
     - While hidden (opacity 0), content swaps to `"Up Next: [Next Title] • [Next Artist]"`.
     - Header executes a 250ms CSS fade-in transition.
     - After another interval, header fades out, swaps back to `"Now Singing: [Title] • [Artist]"`, and fades in.
  3. Adding/removing items in queue, clicking "Skip Next", or song ending resets the cycle cleanly.

### Flow 5: Visual Intro & Interlude Countdown Cue
- **Trigger:** Timeupdate event during audio playback in Karaoke Mode.
- **Behavior:**
  1. The lyrics synchronizer monitors the timestamp of the *upcoming* lyric line `T_next`.
  2. Let `Delta = T_next - currentTime`.
  3. If `0.0s < Delta <= 3.0s` AND either:
     - `T_next` is the first lyric line of the song (intro break), OR
     - Time since previous line ended > 5.0 seconds (interlude break),
  4. A pulsating countdown badge appears centered above the active stage:
     - `2.0s < Delta <= 3.0s`: displays `● ○ ○  (3)`
     - `1.0s < Delta <= 2.0s`: displays `● ● ○  (2)`
     - `0.0s < Delta <= 1.0s`: displays `● ● ●  (1)`
  5. When `Delta <= 0`, countdown badge fades out and the active lyric line is highlighted and scrolled into center view.

### Flow 6: Configurable Stage Settings & Lyric Sizing Controls
- **Trigger:** User clicks `A-`, `A+`, or Settings button on the Karaoke stage toolbar.
- **Behavior:**
  1. **Font Sizing (`A-` / `A+`):**
     - Clicking `A-` decreases base lyrics font size by `0.125rem` (min `1.0rem`).
     - Clicking `A+` increases base lyrics font size by `0.125rem` (max `3.5rem`).
     - Applied immediately via CSS variable `--karaoke-font-size` on stage container.
     - Saved to `localStorage.flexioke_settings.lyricsFontSize`.
  2. **Stage Settings Modal:**
     - Opened via gear icon in Karaoke Stage toolbar.
     - Allows setting:
       - **Transition Interval:** Slider / number input (3 to 30 seconds, default 6).
       - **Active Lyric Glow Color:** Color picker / HEX input (default `#06b6d4`).
       - **Base Font Size:** Slider (16px to 56px).
     - Changes update CSS custom properties in real time and persist to `localStorage`.

## Inputs & Outputs

### API Endpoints

#### 1. Update Song Metadata
- **Method / Path:** `PATCH /api/jobs/{job_id}` (or `POST /api/jobs/{job_id}/metadata`)
- **Request Body:**
  ```json
  {
    "title": "Come Alive",
    "artist": "Rachel Taylor"
  }
  ```
- **Validation Rules:**
  - `title`: String, 1-200 characters, required.
  - `artist`: String, 0-200 characters, optional (nullable).
- **Responses:**
  - `200 OK`: Returns updated `JobResponse` schema with `title` and `artist`.
  - `404 Not Found`: Job does not exist.
  - `422 Unprocessable Entity`: Title missing or invalid length.

#### 2. Get Job Details & Listing
- **Method / Path:** `GET /api/jobs` and `GET /api/jobs/{job_id}`
- **Response Shape (per job):**
  ```json
  {
    "job_id": "7543a66c-e7a3-4f55-88b9-6ecf83a0318d",
    "title": "Come Alive",
    "artist": "Rachel Taylor",
    "source_type": "upload",
    "source_name": "Rachel Taylor - Come Alive.mp3",
    "status": "completed",
    "progress": 100,
    "current_stage": "Ready for playback",
    "error": null,
    "duration_seconds": 236.75,
    "stems": { ... },
    "created_at": "2026-08-28T05:19:41.559337+00:00",
    "updated_at": "2026-08-28T05:26:16.945757+00:00"
  }
  ```

### Client-Side Settings Schema (`localStorage['flexioke_stage_config']`)
```json
{
  "headerTransitionInterval": 6,
  "activeHighlightColor": "#06b6d4",
  "lyricsFontSizeRem": 1.75
}
```

## Business Rules
1. **Backward Compatibility Guarantee:** Any job created in v0.1.0 or v0.2.0 missing the `artist` attribute must load seamlessly, defaulting `artist` to `null` on the backend and rendering `"Unknown Artist"` on the frontend.
2. **Atomic Metadata & Lyrics Updates:** When the user saves the "Edit Song Details & Lyrics" modal, both metadata and lyrics updates must succeed or report clear error messages to the user.
3. **Responsive Stage Layout:** All stage components (time countdown, alternating header banner, lyrics auto-scroller, countdown cue) must render cleanly in both regular window and fullscreen expand modes without overflowing or clipping.
4. **Non-Blocking Visual Cues:** Countdown pulses and cross-fade animations must use hardware-accelerated CSS transitions (`opacity`, `transform`) without locking JavaScript audio synchronizer loops.

## Data Entities
- **`Job` (Model Update in `src/models.py`):**
  - Add `artist: Optional[str] = None`
- **`JobUpdateMetadataRequest` (New Model in `src/models.py`):**
  - `title: Optional[str] = None`
  - `artist: Optional[str] = None`

## Open Questions
- None. All requirements and behaviors verified with user specifications.
