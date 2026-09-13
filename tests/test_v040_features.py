import io
import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from src.main import app
from src.models import SourceType, JobStatus
from src.services.job_manager import JobManager
from src.services.queue_manager import QueueManager
from src.services.video_manager import VideoManager

client = TestClient(app)

@pytest.fixture
def v040_environment(monkeypatch, tmp_path):
    job_dir = tmp_path / "jobs"
    video_dir = tmp_path / "videos"
    job_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    jm = JobManager(data_dir=job_dir, max_workers=1)
    vm = VideoManager(data_dir=video_dir)
    qm = QueueManager()

    # Seed default background video
    vm.save_video("bg001.mp4", b"0123456789abcdef" * 128) # 2048 bytes
    vm.save_video("stage_lights.webm", b"fedcba9876543210" * 128)

    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", jm)
    monkeypatch.setattr(routes, "video_manager", vm)
    monkeypatch.setattr(routes, "queue_manager", qm)

    return jm, vm, qm

def test_v040_end_to_end_video_and_metadata_flow(v040_environment):
    """Verify video upload, discovery, song metadata assignment, and streaming."""
    jm, vm, qm = v040_environment

    # 1. Video Discovery
    resp = client.get("/api/videos")
    assert resp.status_code == 200
    videos = resp.json()["videos"]
    assert len(videos) == 2
    filenames = [v["filename"] for v in videos]
    assert "bg001.mp4" in filenames
    assert "stage_lights.webm" in filenames

    # 2. Video Upload
    new_video = b"custom_bg_content_bytes" * 50
    upload_resp = client.post(
        "/api/videos/upload",
        files={"file": ("neon_pulse.mp4", io.BytesIO(new_video), "video/mp4")}
    )
    assert upload_resp.status_code == 201
    assert upload_resp.json()["filename"] == "neon_pulse.mp4"

    # 3. Create song and verify default video fallback
    job = jm.create_job(SourceType.UPLOAD, "sample.mp3", "Sample Track", "Sample Artist")
    assert job.video_id == "bg001.mp4"
    assert job.video_offset_seconds == 0.0

    # 4. Assign custom video and offset
    patch_resp = client.patch(
        f"/api/jobs/{job.job_id}",
        json={"video_id": "neon_pulse.mp4", "video_offset_seconds": 14.2}
    )
    assert patch_resp.status_code == 200
    updated_job = patch_resp.json()
    assert updated_job["video_id"] == "neon_pulse.mp4"
    assert updated_job["video_offset_seconds"] == 14.2

    # 5. Stream Video Range
    stream_resp = client.get("/api/videos/neon_pulse.mp4", headers={"Range": "bytes=0-99"})
    assert stream_resp.status_code == 206
    assert stream_resp.headers.get("content-range") == f"bytes 0-99/{len(new_video)}"

def test_v040_end_to_end_side_ab_lifecycle_and_queue(v040_environment):
    """Verify Side A/B upload, Side A attachment, queue propagation, and playback metadata."""
    jm, vm, qm = v040_environment

    fake_b = b"\xFF\xFB\x90\x44" + b"\x00" * 512
    fake_a = b"\xFF\xFB\x90\x44" + b"\x01" * 512

    # 1. Ingest Side B only
    resp = client.post(
        "/api/jobs/upload-side-ab",
        files={"file_side_b": ("side_b_instrumental.mp3", io.BytesIO(fake_b), "audio/mpeg")},
        data={"title": "Dual Mode Track", "artist": "Duo Stars"}
    )
    assert resp.status_code == 200
    job = resp.json()
    assert job["source_type"] == "side_ab"
    assert job["status"] == "completed"
    assert job["progress"] == 100
    assert "instrumental" in job["stems"]
    assert "lead_vocals" not in job["stems"]
    job_id = job["job_id"]

    # 2. Attach Side A
    attach_resp = client.post(
        f"/api/jobs/{job_id}/attach-side-a",
        files={"file": ("side_a_vocal.mp3", io.BytesIO(fake_a), "audio/mpeg")}
    )
    assert attach_resp.status_code == 200
    attached_job = attach_resp.json()
    assert "lead_vocals" in attached_job["stems"]

    # 3. Add to Queue and Play Now
    q_resp = client.post("/api/queue/play-now", json={"job_id": job_id})
    assert q_resp.status_code == 200
    current = q_resp.json()["current_track"]
    assert current["job_id"] == job_id
    assert current["source_type"] == "side_ab"
    assert "instrumental" in current["stems"]
    assert "lead_vocals" in current["stems"]

def test_v040_dom_and_css_contract():
    """Verify all DOM elements and CSS variables required for Version 0.4.0 exist in frontend assets."""
    # HTML checks
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Video DOM
    assert 'id="karaoke-bg-video"' in html
    assert 'id="lyrics-modal-video-select"' in html
    assert 'id="lyrics-modal-video-offset"' in html

    # Stage Geometry DOM
    assert 'id="settings-fullscreen-width"' in html
    assert 'id="settings-fullscreen-height"' in html
    assert 'id="settings-fullscreen-v-offset"' in html

    # Side A/B Upload DOM
    assert 'id="tab-side-ab-btn"' in html
    assert 'id="tab-side-ab-content"' in html
    assert 'id="side-b-file-input"' in html
    assert 'id="side-a-file-input"' in html
    assert 'id="submit-side-ab-btn"' in html

    # CSS checks
    css_resp = client.get("/static/styles.css")
    assert css_resp.status_code == 200
    css = css_resp.text

    assert "--karaoke-fullscreen-stage-width" in css
    assert "--karaoke-fullscreen-stage-max-height" in css
    assert "--karaoke-fullscreen-stage-v-offset" in css
    assert "#karaoke-bg-video" in css
