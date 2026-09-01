---
status: draft
approved_by:
approved_at:
---

# Version 0.2.6: Synchronized Lyrics Timestamp Adjustment & Time-Shift Tools

## Problem / Motivation
Synchronized `.lrc` lyrics from online databases or manual creation may occasionally be slightly out of sync with the audio track (e.g., leading or lagging by ±0.5s to ±2.0s due to track intro silence or differing master cuts). Currently, users must manually edit every timestamp line by line or use external scripts. Adding an in-app global and directional time-shifting tool inside the Lyrics Editor modal will allow users to instantly calibrate lyric timing with 1 click.

## Target Users
- **Karaoke Singers & Host Users:** Want tight, perfectly aligned lyrics timing for tracks that lead or lag by a fraction of a second.
- **Stem Studio Creators:** Need quick calibration tools to fine-tune timestamped LRC files without leaving the application.

## Goals
1. **Global Time-Shift Controls in Lyrics Modal (`#lyrics-modal`):**
   - Provide 1-click time-shift buttons (e.g., `+0.5s`, `+0.1s`, `-0.1s`, `-0.5s`) and custom offset input to shift all timestamps in the active `.lrc` text forward or backward.
   - Clamp adjusted timestamps so no line falls below `00:00.00`.
2. **Interactive Audio-Synced Preview:**
   - Allow previewing the time-shifted lyrics with audio playback directly within the editor before saving.
3. **Optional Auto-Alignment Assistant:**
   - Explore automated audio-onset alignment or vocal activity detection (VAD) offset estimation against the separated lead vocal stem.

## Non-Goals (Out of Scope)
- Manual full-song word-by-word karaoke syllable mapping (syllable-level enhanced LRC).
- Automatic AI speech-to-text generation from scratch (remains in future major roadmap).

## Functional Requirements
1. **Frontend Time-Shift Toolbar in `#lyrics-modal`:**
   - Quick shift buttons: `[-0.5s]`, `[-0.1s]`, `[+0.1s]`, `[+0.5s]`.
   - Custom delta input with `Apply Shift` button.
   - Textarea recalculates all `[MM:SS.xx]` timestamps in place with instantaneous DOM preview.
2. **Backend Time-Shift Endpoint (Optional/Alternative):**
   - `POST /api/jobs/{job_id}/lyrics/shift?offset_seconds=...`
