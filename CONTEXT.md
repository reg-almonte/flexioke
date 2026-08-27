# Flexioke Domain Context & Glossary

This document establishes the ubiquitous language and domain model for the Flexioke stem separation and multitrack player application.

## Domain Glossary

| Term | Definition |
|---|---|
| **Stem** | An isolated individual audio component extracted from a full mix. Flexioke focuses on three target stems: `Instrumental` (Music), `Lead Vocals`, and `Backing Vocals`. |
| **Stage 1 Separation** | The primary AI separation step using Mel-Band RoFormer (`mel_band_roformer_vocals`) which splits input audio into `Instrumental` (Music) and `Combined Vocals`. |
| **Stage 2 Separation** | The secondary AI separation step using UVR MDX-Net Karaoke (`UVR_MDXNET_KARA_2`) which takes `Combined Vocals` and splits them into `Lead Vocals` and `Backing Vocals`. |
| **JobRecord** | The state and metadata representation of a single audio ingestion and separation workflow, tracked by a unique UUID `job_id`. |
| **Song Library** | The persistent, indexed catalog of all successfully processed songs, searchable by title and source metadata. |
| **Playback Queue** | An ordered list of songs scheduled for continuous sequential playback in the multitrack player. |
| **Multitrack Player** | The browser-based interface rendering 3 synchronized Wavesurfer.js waveforms with unified transport and individual channel controls (Mute, Solo, Volume). |
| **Solo / Mute Matrix** | The audio routing logic where Solo isolates one or more selected tracks and silences all unselected tracks, while Mute silences specific individual tracks. |

## Architectural Overview
- **Backend:** Python FastAPI with in-process asynchronous task runner.
- **Processing Engine:** `audio-separator` + `yt-dlp` + `ffmpeg`.
- **Storage:** Local filesystem persistence under `./data/jobs/{job_id}/` with in-memory library index caching.
- **Frontend:** HTML5 / TailwindCSS / ES Modules with Wavesurfer.js v7 and MultiTrack plugin.
