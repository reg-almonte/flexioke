---
status: approved
approved_by: reg
approved_at: 2026-08-29
---

# Karaoke UI Refinements & Stage Controls (v0.2.2)

## Problem / Motivation
While Flexioke v0.2.1 delivered core metadata separation and synchronized lyrics playback, user testing identified opportunities to streamline the Karaoke Mode user experience:
1. The bottom transport controls were fragmented, lacking a dedicated volume slider, a direct "Restart Song" action, and interactive timecode mode toggles.
2. The alternating stage header ("Now Singing" ⟷ "Up Next") required waiting for a timed cross-fade cycle to check upcoming tracks, rather than displaying both simultaneously at a glance.
3. Queue order in Karaoke Mode was fixed after addition, with no ability to promote or demote upcoming songs. Furthermore, the Song Library occupied the top of the sidebar above the Playback Queue, forcing users to scroll past the library to monitor their live performance lineup.
4. Clicking the lyrics stage area had no playback control affordance, unlike common media player standards (e.g., YouTube video click-to-pause).
5. The top navigation bar occupied persistent vertical screen space, reducing lyrics visibility during karaoke sessions.

## Target Users
- **Karaoke Singers & Hosts:** Users actively performing or queueing up tracks who need instant visibility of what is playing and what is next, full transport control, and an immersive lyrics stage.

## Goals
- Provide simultaneous top-header visibility of both **Now Singing** (left) and **Up Next** (right) with marquee text scrolling for long titles.
- Modernize the Karaoke Stage transport bar with an expanding YouTube-style volume slider, click-toggleable timecode display, restart button, and outward/inward expand icons.
- Support click-to-play/pause on the stage background while preserving precision click-to-seek on compact lyric line pills.
- Re-position the Playback Queue above the Song Library in Karaoke Mode, and provide `▲` / `▼` reordering controls for queued songs.
- Implement an auto-hiding top application navbar with hover trigger to maximize lyrics viewport height.

## Non-Goals (Out of Scope)
- Modifying Stem Studio player workflows or channel strip layouts (changes restricted to Karaoke Mode and shared top navigation auto-hide).
- Complex drag-and-drop queue reordering (discrete `▲` / `▼` buttons fulfill requirement with higher touch/click reliability).
- Remote multi-device synchronized queue voting (remains local/in-session).

## Functional Requirements

### 1. Karaoke Stage Header Refinement
- **Simultaneous Dual Display:** Replace the alternating cross-fade cycle with simultaneous headers:
  - **Left Header:** `"Now Singing: [Title] - [Artist]"` in a single streamlined row.
  - **Right Header:** `"Up Next: [Next Title] - [Next Artist]"` (or `"Up Next: — (Queue Empty)"` in dimmed text when queue is empty).
- **Auto-Marquee:** If title/artist strings exceed container width, smoothly marquee scroll on overflow/hover.
- **Stage Toolbar Cleanup:** Remove `A-` / `A+` buttons from the header (font size is managed exclusively inside the Stage Settings modal).

### 2. Modernized Karaoke Bottom Transport Bar
- **Left Cluster:**
  - `Play / Pause` button (▶ / ⏸).
  - Expanding Volume button (🔊) revealing a smooth horizontal volume slider on hover/focus (YouTube style).
  - Timecode display showing `<Current Time> / <Total Time>`, which toggles to `<Remaining Time> / <Total Time>` (`-MM:SS / MM:SS`) upon click.
- **Right Cluster:**
  - `Restart` button (🔄) to seek immediately to `0:00` and auto-play.
  - `Next Song` button (⏭) to advance queue.
  - `Stop & Cue` button (⏹).
  - `Stage Settings` button (⚙), which remains visible and accessible in both default and Expanded/Fullscreen modes.
  - `Expand / Collapse` button (⛶ / 🗗) with updated outward/inward arrow iconography.

### 3. Stage Background Click-to-Play/Pause
- Clicking anywhere on the lyrics stage background or padding toggles Play / Pause.
- Lyric line elements are rendered with bounded inline-block/pill clickable areas so clicking a lyric text seeks to that timestamp, whereas clicking around lyric lines toggles Play/Pause.

### 4. Karaoke Sidebar Reorganization & Queue Reordering
- **Sidebar Ordering:** Swap sidebar sections in Karaoke Mode so **Playback Queue** is positioned at the top, and **Song Library** is placed below.
- **Queue Reordering:** Each queued song item displays `▲` (move up) and `▼` (move down) buttons.
- **Live Sync:** Reordering the top item in the queue immediately updates the "Up Next" display in the stage header.

### 5. Auto-Hiding Main Navigation Bar
- Main navbar smoothly translates off-screen when not focused.
- Moving the cursor to the top edge (`top: 0` hover zone) slides the navbar smoothly into view.

## Acceptance Criteria
- [ ] Top stage header displays both "Now Singing" on the left and "Up Next" on the right simultaneously in single-line `Title - Artist` format with marquee on overflow.
- [ ] Header displays `"Up Next: — (Queue Empty)"` when no songs remain in queue.
- [ ] `A-` / `A+` buttons removed from stage header; font size adjustments in Settings modal update lyrics size immediately.
- [ ] Stage bottom transport bar features: Play/Pause, expanding hover volume slider, click-toggleable timecode, Restart button (seeks to 0:00 and plays), Next, Stop, Settings `⚙` (available in Fullscreen), and Expand/Collapse icons.
- [ ] Clicking lyrics stage background toggles Play/Pause without interfering with lyric line timestamp seeks.
- [ ] Karaoke sidebar places Playback Queue at the top and Song Library below.
- [ ] Queued songs have `▲` and `▼` buttons that dynamically reposition tracks in queue and update "Up Next" immediately.
- [ ] Main header auto-hides and reveals smoothly on top hover.

## Constraints & Assumptions
- Stem Studio layout and channel strips remain intact.
- Existing `localStorage['flexioke_stage_config']` continues to persist stage settings across reloads.
- No external frontend frameworks added; vanilla ES6+ and Tailwind CSS.

## Open Questions
- None identified. All scope items and user directives mapped directly into requirements.
