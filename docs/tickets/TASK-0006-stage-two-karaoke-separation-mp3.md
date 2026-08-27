---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0006: Stage 2 Karaoke Separation Engine (UVR MDX-Net Kara 2) & MP3 Encoding

## Parent Story
- `STORY-0002-two-stage-stem-separation.md`

## What to build
Implement the Stage 2 audio separation module using `audio-separator` with `UVR_MDXNET_KARA_2` to split the `Combined Vocals` stem into `Lead Vocals` and `Backing Vocals`, followed by MP3 encoding/normalization of all 3 final stems (`instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`).

## Acceptance Criteria
- [x] Stage 2 executes `UVR_MDXNET_KARA_2` on the vocals output from Stage 1.
- [x] Produces `lead_vocals` and `backing_vocals` stems.
- [x] Stems are verified, converted/encoded to standard MP3 format (320kbps), and placed in the job directory.
- [x] Unit tests verify Stage 2 execution and MP3 output generation.

## Blocked by
- TASK-0005: Stage 1 Separation Engine (Mel-Band RoFormer Integration)

## Implementation
- **Branch:** `story/STORY-0002-two-stage-stem-separation`
- **Engine:** `src/services/separator.py` (`separate_stage_2`, `convert_to_mp3`, `encode_final_stems`) implementing Stage 2 Karaoke isolation and standard 320kbps MP3 stem generation.
- **Tests:** `tests/test_stage2_separator.py` (2 unit tests passing, 18 suite-wide).
