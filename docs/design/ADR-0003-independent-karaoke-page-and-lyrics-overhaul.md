---
status: approved
approved_by: reg
approved_at: 2026-08-27
---

# ADR-0003: Independent Page System for Stem Studio & Karaoke Mode with Lyrics Engine Overhaul

## Status
Pending Approval

## Context
User feedback requires two fundamental architectural and UX improvements:
1. **Independent Page Systems:** Stem Studio and Karaoke Mode must each function as self-contained page systems. Each page has its own dedicated Song Library panel, Playback Queue panel, and Player transport. When playback starts in one mode, playback in the other mode pauses/stops immediately (mutual exclusion).
2. **Lyrics Rendering Engine Overhaul:** The lyrics viewer CSS layout and parser must be overhauled to fix rendering issues, eliminate overflow-centering layout bugs, ensure crystal-clear text readability with high-contrast active line indicators, handle instrumental breaks gracefully, and provide reliable timecode auto-scrolling.

## Decision

### 1. Dual Independent Page System Architecture
- **Stem Studio View (`#view-stem-studio`):**
  - Left: Dual Ingestion forms (Upload/YouTube) + Studio Song Library + Studio Playback Queue.
  - Right: 3-track WaveSurfer multitrack mixer with individual Mute/Solo/Volume channel strips.
- **Karaoke Mode View (`#view-karaoke`):**
  - Left: Dedicated Karaoke Song Library + Dedicated Karaoke Playback Queue (with Lyrics editor button `📝`).
  - Right: Full-height Center Stage Lyrics Viewer + Dedicated Karaoke Transport with Quick Lead/Backing Vocal Mute Toggles.
- **Playback Coordinator (Mutual Exclusion):**
  - Both views share the underlying audio engine backend, but switching pages or starting playback in one mode automatically suspends/pauses the other player instance.

### 2. Lyrics Rendering Engine Overhaul
- Overhaul `#karaoke-lyrics-stage` layout:
  - Remove flex centering on scrolling containers to prevent CSS overflow clipping.
  - Use structured lyric row cards with high contrast text:
    - Default lines: `text-slate-300 font-medium text-base` (easily readable).
    - Active line: `text-white font-black text-2xl bg-brand-500/20 border border-brand-500/40 rounded-xl px-4 py-2.5 shadow-lg shadow-brand-500/20 scale-105 transition-all`.
    - Instrumental pauses / empty lines: `[ Instrumental Break ♪ ]`.
  - Fix timecode parsing for standard LRC formats (`[mm:ss.xx]`, `[mm:ss.xxx]`, `[mm:ss]`).
  - Auto-scroll with debounced `scrollIntoView({ behavior: 'smooth', block: 'center' })`.

## Consequences
- **Positive:** Clean separation of concerns between sound engineering (Stem Studio) and performance/singing (Karaoke Mode); rock-solid lyrics display with high contrast and zero visual clipping.
- **Negative:** Slightly expanded HTML structure for dual library/queue panels (managed by shared JavaScript components).
