---
status: approved
approved_by: user
approved_at: 2026-08-27
implementation: pending
---

# TASK-0005: Stage 1 Separation Engine (Mel-Band RoFormer Integration)

## Parent Story
- `STORY-0002-two-stage-stem-separation.md`

## What to build
Implement the Stage 1 audio separation module wrapping `audio-separator` with the Mel-Band RoFormer model (`mel_band_roformer_vocals`) to separate input audio into `Instrumental` and `Combined Vocals` audio files.

## Acceptance Criteria
- [ ] Separation service loads and executes Mel-Band RoFormer on an input audio file.
- [ ] Generates isolated `Instrumental` and `Combined Vocals` audio stems in the job directory.
- [ ] Handles model initialization, device placement (MPS/CUDA/CPU), and resource cleanup.
- [ ] Unit tests verify separation execution (with mock audio/model harness).

## Blocked by
- TASK-0003: File Upload Ingestion API & Audio Validation
- TASK-0004: YouTube URL Ingestion Engine via yt-dlp
