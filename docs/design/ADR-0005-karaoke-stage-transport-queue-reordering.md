---
status: approved
approved_by: reg
approved_at: 2026-08-29
---

# ADR-0005: Directional Queue Reordering API with Reactive Stage Transport & CSS Marquee Engine

## Context
In Flexioke v0.2.1, Karaoke Mode introduced basic metadata separation, a 3-beat countdown cue, and stage customization modal. However, user experience testing highlighted several workflow friction points:
1. The alternating header required waiting for a timed cross-fade cycle to see upcoming tracks rather than displaying both "Now Singing" and "Up Next" simultaneously.
2. The stage transport bar lacked dedicated volume control, a direct "Restart Song" action, and interactive timecode mode switching.
3. Queued songs could not be reordered once added, and the sidebar placed the Song Library above the live Playback Queue.
4. Clicking the lyrics stage background did not provide intuitive click-to-play/pause affordances.
5. The static application header reduced vertical lyrics visibility during karaoke performances.

## Decision
Adopt **Option 1: Directional Queue Reordering API with Reactive DOM Event Bus & CSS Marquee Engine**:

1. **Backend Queue Reordering (`POST /api/queue/reorder`):**
   - Implement `POST /api/queue/reorder` accepting `{ "queue_id": str, "direction": "up" | "down" }`.
   - `QueueManager.reorder_queue(queue_id, direction)` performs atomic in-place swapping of adjacent items under thread lock.
   - Returns the updated `QueueResponse` immediately to sync queue state across all connected views.

2. **Dual Simultaneous Stage Header & CSS Marquee Engine:**
   - Redesign stage header into a split layout:
     - Left: `"Now Singing: [Title] - [Artist]"`
     - Right: `"Up Next: [Next Title] - [Next Artist]"` (or `"Up Next: — (Queue Empty)"`)
   - If text overflows container dimensions (`scrollWidth > clientWidth`), attach dynamic CSS marquee animation (`transform: translateX(...)`).
   - Remove `A-` / `A+` buttons from stage header and consolidate font scaling exclusively within Stage Settings modal (`⚙`).

3. **Modernized Bottom Transport Bar:**
   - **Left Cluster:**
     - `Play/Pause` toggle button.
     - Expanding volume control: hovering/focusing the speaker icon (🔊) expands a horizontal volume slider (0–100%) connected to Web Audio master gain, persisted in `localStorage['flexioke_master_volume']`.
     - Click-toggleable Timecode badge: clicking switches between `<Current> / <Total>` and `<Remaining> / <Total>`.
   - **Right Cluster:**
     - `Restart` button (🔄): calls `player.syncSeek(0.0)` and triggers `play()`.
     - `Next Track` (⏭) and `Stop & Cue` (⏹) transport buttons.
     - `Stage Settings` (⚙): accessible in both standard and Fullscreen/Expanded modes with elevated modal z-index (`z-[10000]`).
     - `Expand / Collapse` (⛶ / 🗗): updated with outward/inward arrow iconography.

4. **Event-Delegated Stage Click-to-Play/Pause:**
   - Add click listener to `#karaoke-lyrics-stage` background.
   - Style `.karaoke-line` elements as inline-block/pill containers with `e.stopPropagation()` on direct line clicks to preserve timestamp seeking while allowing background clicks to toggle Play/Pause.

5. **Karaoke Sidebar Reorganization:**
   - Place **Playback Queue** container at the top of the Karaoke sidebar and **Song Library** below.
   - Render `▲` and `▼` reordering buttons on each queue card.
   - Reordering the first queue item immediately dispatches `flexioke:queue-updated` and updates the "Up Next" header.

6. **Auto-Hiding App Header:**
   - Implement CSS translation transition on `#main-header` (`-translate-y-full` / `translate-y-0`) with a transparent top hover detection bar at `top: 0`.

## Options Considered

### Option 1: Directional Queue Reordering API with Reactive DOM Event Bus & CSS Marquee Engine (Chosen)
- **Pros:**
  - Zero external client dependencies; pure vanilla ES6+ and Tailwind CSS.
  - Atomic in-memory server state guarantees thread safety during background auto-advancing.
  - Highly responsive event coordination via custom DOM events (`flexioke:queue-updated`).
- **Cons:**
  - Moving an item multiple positions requires sequential directional moves.

### Option 2: Full Queue Batch Array Replacement (`PUT /api/queue`)
- **Pros:**
  - Supports multi-index repositioning in a single request.
- **Cons:**
  - Prone to race conditions if playback auto-advances concurrently while client edits order.
  - Increased payload and validation complexity.

## Consequences
- **Positive:**
  - Dramatic usability boost for karaoke performers and hosts: immediate visibility of upcoming tracks, effortless stage play/pause, and complete queue control.
  - Fullscreen mode gains access to settings without obscuring UI controls.
  - Clean separation preserved: Stem Studio unaffected except for shared auto-hiding navbar.
- **Negative / Neutral:**
  - Additional CSS keyframe rules for marquee animations in `styles.css`.

## Related
- Functional spec: [`docs/specs/karaoke-ui-refinements.md`](../specs/karaoke-ui-refinements.md)
- Requirement: [`docs/requirements/karaoke-ui-refinements.md`](../requirements/karaoke-ui-refinements.md)
- Supersedes / related ADRs: Extends [`docs/design/ADR-0004-karaoke-metadata-and-stage-enhancements.md`](ADR-0004-karaoke-metadata-and-stage-enhancements.md)
