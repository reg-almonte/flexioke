---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: in-review
---

# TASK-0005: Stage 1 Separation Engine (Mel-Band RoFormer Integration)

## Parent Story
- `STORY-0002-two-stage-stem-separation.md`

## What to build
Implement the Stage 1 audio separation module wrapping `audio-separator` with the Mel-Band RoFormer model (`mel_band_roformer_vocals`) to separate input audio into `Instrumental` and `Combined Vocals` audio files.

## Acceptance Criteria
- [x] Separation service loads and executes Mel-Band RoFormer on an input audio file.
- [x] Generates isolated `Instrumental` and `Combined Vocals` audio stems in the job directory.
- [x] Handles model initialization, device placement (MPS/CUDA/CPU), and resource cleanup.
- [x] Unit tests verify separation execution (with mock audio/model harness).

## Blocked by
- TASK-0003: File Upload Ingestion API & Audio Validation
- TASK-0004: YouTube URL Ingestion Engine via yt-dlp

## Implementation
- **Branch:** `story/STORY-0002-two-stage-stem-separation`
- **Engine:** `src/services/separator.py` (`separate_stage_1`) using `audio-separator` with `model_mel_band_roformer_ep_3005_sdr_11.4360.ckpt` and automatic Apple Silicon MPS/CoreML hardware acceleration.
- **Tests:** `tests/test_stage1_separator.py` (2 unit tests passing, 16 suite-wide).
