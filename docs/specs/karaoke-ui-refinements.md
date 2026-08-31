---
status: approved
approved_by: reg
approved_at: 2026-08-29
---

# Karaoke UI Refinements & Stage Controls — Functional Spec

## Related Requirements
- `docs/requirements/karaoke-ui-refinements.md`

## Functional Flows

### 1. Stage Header: Simultaneous Now Singing & Up Next
- **Main Flow:**
  1. When a song is active, the left header displays `"Now Singing: [Title] - [Artist]"` in a single streamlined row.
  2. If tracks exist in the playback queue, the right header displays `"Up Next: [Next Title] - [Next Artist]"`.
  3. If title/artist text overflows the allocated half-width of the header, the container activates a CSS marquee animation to scroll text smoothly.
  4. If the queue is empty, the right header displays `"Up Next: — (Queue Empty)"` in muted slate styling.
  5. The `A-` and `A+` buttons are omitted from the header; font sizing is configured via the Stage Settings modal (`⚙`).

### 2. Modernized Bottom Transport Bar & Interactive Timecode
- **Main Flow:**
  1. **Play/Pause (Left):** Primary ▶ / ⏸ button toggles playback.
  2. **Expanding Volume Slider (Left):** Hovering or focusing on the speaker icon (🔊) expands a horizontal slider smoothly (0% to 100%). Dragging the slider adjusts `window.flexiokePlayer.setMasterVolume(val)` and persists the level in `localStorage`.
  3. **Timecode Mode Toggle (Left):**
     - Default display: `MM:SS / MM:SS` (Elapsed / Total).
     - Clicking the badge toggles mode to `(-MM:SS) / MM:SS` (Remaining / Total).
     - Choice is remembered during the session.
  4. **Restart Button (Right):** Clicking the restart icon (🔄) seeks playback to `0.00s` and immediately resumes/initiates playback.
  5. **Next Track (Right):** Advances queue (`window.flexiokeQueue.advanceNext(true)`).
  6. **Stop & Cue (Right):** Pauses and cues next track (`window.flexiokeQueue.stopAndCueNext()`).
  7. **Stage Settings (Right):** Clicking `⚙` opens the Stage Settings modal in both default view and Fullscreen/Expanded view.
  8. **Expand / Collapse (Right):** Toggles `.stage-fullscreen` mode; displays outward arrows `⛶` in default mode and inward arrows `🗗` in expanded mode.

### 3. Stage Click-to-Play/Pause with Bounded Lyric Pills
- **Main Flow:**
  1. User clicks any background or padding area of `#karaoke-lyrics-stage`.
  2. The stage click handler triggers `window.flexiokePlayer.togglePlayPause()`.
- **Alternate / Seek Flow:**
  1. User clicks directly on a `.karaoke-line` text pill.
  2. The event handler seeks playback directly to the line timestamp `line.time` (`stopPropagation()` prevents the stage background play/pause toggle from firing).

### 4. Sidebar Layout & Queue Reordering
- **Main Flow:**
  1. In Karaoke Mode sidebar, the **Playback Queue** container is rendered at the top, and the **Song Library** container is rendered below.
  2. Each queued item includes `▲` (Move Up) and `▼` (Move Down) buttons:
     - Clicking `▲` on index `i` swaps item `i` with item `i-1` via `POST /api/queue/reorder`.
     - Clicking `▼` on index `i` swaps item `i` with item `i+1` via `POST /api/queue/reorder`.
     - `▲` is disabled on the first item; `▼` is disabled on the last item.
  3. When the item at index `0` changes (promoted or demoted), a `flexioke:queue-updated` event is dispatched and the right stage header immediately reflects the new "Up Next" song.

### 5. Auto-Hiding Navigation Bar
- **Main Flow:**
  1. Top navigation header smoothly translates upwards off-screen (`-translate-y-full` / `opacity-0` transition) when the user is interacting with the main workspace.
  2. A thin invisible trigger zone at `top: 0` detects mouse movement or hover.
  3. When the pointer enters the top trigger zone, the header slides smoothly down into view (`translate-y-0` / `opacity-100`).

## Inputs & Outputs

### 1. `POST /api/queue/reorder`
- **Request Body:**
  ```json
  {
    "queue_id": "string (UUID)",
    "direction": "up | down"
  }
  ```
  *(or alternative array order payload: `{"ordered_ids": ["uuid1", "uuid2", ...]}`)*
- **Response:** `200 OK` with full `QueueResponse` schema:
  ```json
  {
    "current_track": { ... } | null,
    "queue": [ ... ],
    "history": [ ... ]
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: `queue_id` not found or movement out of bounds.

### 2. Client Stage Settings (LocalStorage: `flexioke_stage_config`)
- **Schema:**
  ```json
  {
    "headerTransitionInterval": 6,
    "activeHighlightColor": "#06b6d4",
    "baseFontSizePx": 20,
    "timecodeMode": "elapsed | remaining"
  }
  ```

## Business Rules
1. **Lyric Line Click Boundary:** `.karaoke-line` must be styled as an inline-block / bounded pill so that whitespace around the text does not trigger seeks, ensuring effortless background clicking for Play/Pause.
2. **Settings in Fullscreen:** `#karaoke-settings-modal` z-index must be higher than `.stage-fullscreen` (`z-[10000]`) and `#karaoke-settings-btn` must remain visible in the bottom transport bar during fullscreen mode.
3. **Volume Persistence:** Master volume adjusted via the expanding slider persists across tracks and sessions via `localStorage['flexioke_master_volume']`.
4. **Queue Reordering Safety:** Reordering operations are atomic in the in-memory queue manager under thread lock; invalid indices or target bounds are rejected with HTTP 400.

## Data Entities
- **`QueueItem`:** `{ queue_id: str, job_id: str, title: str, artist: Optional[str], duration_seconds: Optional[float], stems: Dict[str, str], added_at: datetime }`
- **`QueueReorderRequest`:** `{ queue_id: str, direction: str }`

## Open Questions
- None. All functional flows and edge cases specified.
