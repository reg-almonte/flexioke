I am building a web application that extracts stems from uploaded audio files, splits them into separate tracks (Music, Lead Vocals, Backing Vocals), and plays them in an interactive multitrack web player with real-time mute/solo controls.

Here are the functional and technical specifications:

1. Core Architecture & Tech Stack:
- Backend: Python (FastAPI)
- Audio Processing: `audio-separator` (using Mel-Band RoFormer for main stems and UVR_MDXNET_KARA_2 for backing/lead vocal isolation)
- YouTube Ingestion: `yt-dlp` for extracting raw audio from submitted URLs
- Frontend: HTML5, TailwindCSS, and JavaScript (Wavesurfer.js with MultiTrack plugin)

2. Pipeline & Workflow:
- Input: User uploads an audio file (.mp3, .wav) OR submits a valid YouTube link.
- Processing Pipeline:
  * Stage 1: Separate audio into Instrumental (Music) and Combined Vocals.
  * Stage 2: Pass Combined Vocals through the karaoke model to extract Lead Vocals and Backing Vocals.
- Output: Three distinct stems (Instrumental, Lead Vocals, Backing Vocals) saved in a job-specific folder.

3. Frontend & Player Requirements:
- Visual display of 3 stacked waveforms rendered via Wavesurfer.js.
- Global transport: Play/Pause all, Seek bar, Master volume.
- Per-track controls: Mute/Unmute toggle, Solo toggle, individual volume slider.
- Export options: Download individual stems or download all stems in a single .zip file.

4. How We Will Work:
- Do not dump all the code at once.
- Break the implementation into sequential, testable milestones starting with project setup and backend API scaffolding.
- Ask any clarifying questions before writing code for Milestone 1.