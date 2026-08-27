# 🎤 Flexioke

> **AI-Powered 2-Stage Stem Studio & Synchronized Karaoke Web Player**  
> Isolate vocals, lead melodies, and backing harmonies with state-of-the-art deep learning, and sing along to synchronized timestamped lyrics in an immersive karaoke stage.

---

## ✨ Features

### 1. ⚡ 2-Stage AI Audio Stem Separation
Flexioke uses a cascading deep learning pipeline to extract clean, studio-grade individual stems from any song:
- **Stage 1 (Mel-Band RoFormer):** Isolates the master vocal track from the instrumental background music with extreme clarity.
- **Stage 2 (UVR MDX-Net Kara 2):** Takes the isolated vocal track and separates it into **Lead Vocals** and **Backing Vocals & Harmonies**.

### 2. 🎛️ Stem Studio Page (Multitrack Mixer)
- **3-Track WaveSurfer.js Visualizer:** Stacked waveform visualizers synchronized to a unified playback timeline.
- **Independent Channel Strips:** Dedicated **Mute**, **Solo**, and **Volume sliders** for Instrumental, Lead Vocals, and Backing Vocals.
- **Audio Ingestion:** Upload local audio files (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`) or paste a YouTube video URL for automated audio extraction and stem processing.

### 3. 🎤 Dedicated Karaoke Mode & Synchronized Stage
- **Real-Time LRC Lyrics Synchronization:** Center-stage lyrics display that illuminates and magnifies the active singing line with smooth vertical auto-scroll.
- **Click-to-Seek:** Click any lyric line on screen to instantly seek playback to that exact moment in the song.
- **Quick Vocal Mutes for Singers:**
  - `[ 🎤 Lead Vocals: ON/OFF ]` — Mute the original artist's voice to sing solo over the instrumental and harmonies.
  - `[ 👥 Backing: ON/OFF ]` — Toggle backing vocals and harmonies on or off.
- **Dedicated Cue-Stop (`⏹`):** Stop the current song and cue the next queued track in pause mode.
- **Fullscreen Expand Mode (`⛶ Expand` / `Escape`):** Immersive, edge-to-edge dark stage view designed for live performances and TV/monitor displays.

### 4. 📚 Synchronized Library & Playback Queue
- **Song Library:** Persistent catalog of processed stems with instant real-time search.
- **Playback Queue:** Shared queue across both Studio and Karaoke pages with drag/drop order, auto-advance, and smart play interruption alerts.
- **Built-In Lyrics Editor (`📝`):** Paste timestamped `.lrc` lyrics (`[00:05.20] Lyric text`) or plain-text transcripts directly from the Song Library.

---

## 🛠️ Architecture & Tech Stack

```
   ┌─────────────────────────────────────────────────────────┐
   │             FastAPI Backend (src/main.py)               │
   │  ┌─────────────────────────┬─────────────────────────┐  │
   │  │   Audio Ingestion &     │  2-Stage AI Separator   │  │
   │  │   YouTube Extractor     │  • Mel-Band RoFormer    │  │
   │  │   (Upload / yt-dlp)     │  • UVR MDX-Net Kara 2   │  │
   │  └─────────────────────────┴─────────────────────────┘  │
   │  ┌─────────────────────────┬─────────────────────────┐  │
   │  │   Song Library &        │   LRC Lyrics Storage    │  │
   │  │   Queue Service         │   & REST API            │  │
   │  └─────────────────────────┴─────────────────────────┘  │
   └─────────────────────────────────────────────────────────┘
                                ▲
                                │ REST & Stem Streaming
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │            Modern SPA Client (src/static/)              │
   │  ┌─────────────────────────┬─────────────────────────┐  │
   │  │   🎛️ Stem Studio View    │  🎤 Dedicated Karaoke   │  │
   │  │   • 3-Track WaveSurfer  │  • Synced LRC Engine    │  │
   │  │   • Mute / Solo / Vol   │  • Fullscreen Stage     │  │
   │  └─────────────────────────┴─────────────────────────┘  │
   └─────────────────────────────────────────────────────────┘
```

- **Backend:** Python 3.9+, FastAPI, PyTorch (Apple Silicon GPU `mps` / `cuda` acceleration), `audio-separator`, `yt-dlp`, Uvicorn.
- **Frontend:** Vanilla JavaScript (ES6+ Modules), WaveSurfer.js v7 + Multitrack Plugin, TailwindCSS.
- **Testing:** Comprehensive test suite (51 unit and integration tests with Pytest and FastAPI TestClient).

---

## 🚀 Quick Start

### Prerequisites
1. **Python 3.9+**
2. **`ffmpeg`** installed on your system:
   ```bash
   # macOS (Homebrew)
   brew install ffmpeg

   # Ubuntu / Debian
   sudo apt update && sudo apt install ffmpeg
   ```

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/reg-almonte/flexioke.git
cd flexioke

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
PYTHONPATH=. uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 3. Open in Browser
- **Web App:** [http://localhost:8000](http://localhost:8000)
- **Interactive API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Tests

```bash
source .venv/bin/activate
PYTHONPATH=. pytest -v
```

---

## 📖 How to Use

1. **Add a Song:**
   - Go to **Stem Studio**, drag and drop an audio file (`.mp3`, `.wav`, etc.) or paste a YouTube URL.
   - Click **Separate Stems** and watch the live progress bar as Mel-Band RoFormer and UVR Kara 2 process the audio.
2. **Add Lyrics:**
   - Click the **`📝`** button on your song card in the Song Library.
   - Paste timestamped `.lrc` lyrics (e.g. from Spotify, Genius, or Megalobiz) and click **Save Lyrics**.
3. **Sing in Karaoke Mode:**
   - Switch to **`[ 🎤 Karaoke Mode ]`** in the top navigation bar.
   - Press **Play** or click **`⛶ Expand`** for a full-screen stage experience!
   - Toggle **`Lead Vocals: OFF`** to sing solo with the original backing band and harmonies.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
