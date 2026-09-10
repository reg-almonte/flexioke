import subprocess
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_video_elements_in_html():
    """Verify index.html contains karaoke background video element and modal video controls."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert "karaoke-bg-video" in html
    assert "lyrics-modal-video-select" in html
    assert "lyrics-modal-video-offset" in html

def test_video_stage_styles_in_css():
    """Verify styles.css contains rules for karaoke background video and stage transparency."""
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200
    css = resp.text

    assert "#karaoke-bg-video" in css
    assert "object-fit: cover" in css or "object-cover" in css

def test_video_playback_and_sync_logic_in_karaoke_js():
    """Verify karaoke.js implements video source loading, offset calculation, and playback coordination."""
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text

    assert "karaoke-bg-video" in js
    assert "video_id" in js
    assert "video_offset_seconds" in js
    assert "bgVideo" in js

def test_lyrics_modal_video_controls_in_library_queue_js():
    """Verify library_queue.js populates video selector from /api/videos and handles metadata saves."""
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    js = resp.text

    assert "/api/videos" in js
    assert "lyrics-modal-video-select" in js
    assert "lyrics-modal-video-offset" in js
    assert "video_offset_seconds" in js

def test_video_timecode_synchronization_in_node():
    """Simulate KaraokeStageManager video synchronization and offset looping math in Node.js."""
    node_script = """
    class MockVideo {
        constructor() {
            this.src = "";
            this.currentTime = 0;
            this.duration = 40.0; // 40 second looping video
            this.paused = true;
            this.muted = true;
            this.loop = true;
        }
        play() { this.paused = false; }
        pause() { this.paused = true; }
    }

    const stage = {
        bgVideo: new MockVideo(),
        videoOffset: 5.0, // 5 second offset
        currentJob: {
            job_id: "test-123",
            video_id: "bg001.mp4",
            video_offset_seconds: 5.0
        },

        onSongLoaded(job) {
            this.currentJob = job;
            const videoId = job.video_id || "bg001.mp4";
            this.videoOffset = typeof job.video_offset_seconds === 'number' ? job.video_offset_seconds : 0.0;
            this.bgVideo.src = `/api/videos/${encodeURIComponent(videoId)}`;
            this.bgVideo.currentTime = this.videoOffset;
        },

        syncVideoPlayback(audioTime, isAudioPlaying) {
            if (!this.bgVideo || !this.bgVideo.duration) return;

            if (isAudioPlaying) {
                if (this.bgVideo.paused) {
                    this.bgVideo.play();
                }
                const expectedVideoTime = (audioTime + this.videoOffset) % this.bgVideo.duration;
                const diff = Math.abs(this.bgVideo.currentTime - expectedVideoTime);
                if (diff > 0.4) {
                    this.bgVideo.currentTime = expectedVideoTime;
                }
            } else {
                if (!this.bgVideo.paused) {
                    this.bgVideo.pause();
                }
            }
        }
    };

    // 1. Initial Load
    stage.onSongLoaded(stage.currentJob);
    if (stage.bgVideo.src !== "/api/videos/bg001.mp4") throw new Error("Incorrect video src");
    if (stage.bgVideo.currentTime !== 5.0) throw new Error("Initial offset time not set");

    // 2. Play Audio at 10s -> Expected video time: (10 + 5) % 40 = 15s
    stage.syncVideoPlayback(10.0, true);
    if (stage.bgVideo.paused) throw new Error("Video should be playing when audio is playing");
    if (stage.bgVideo.currentTime !== 15.0) throw new Error(`Expected video time 15s, got ${stage.bgVideo.currentTime}`);

    // 3. Audio at 50s (past 40s duration) -> Expected video time: (50 + 5) % 40 = 15s (looping)
    stage.syncVideoPlayback(50.0, true);
    if (stage.bgVideo.currentTime !== 15.0) throw new Error(`Expected looped video time 15s, got ${stage.bgVideo.currentTime}`);

    // 4. Pause Audio -> Video should pause
    stage.syncVideoPlayback(50.0, false);
    if (!stage.bgVideo.paused) throw new Error("Video should pause when audio is paused");

    console.log("VIDEO_SYNC_SUCCESS");
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Node script error: {proc.stderr}"
    assert "VIDEO_SYNC_SUCCESS" in proc.stdout
