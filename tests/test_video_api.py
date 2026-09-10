import io
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from src.main import app
from src.services.video_manager import VideoManager
from src.services.job_manager import JobManager
from src.models import SourceType

client = TestClient(app)

@pytest.fixture
def mock_video_env(monkeypatch, tmp_path):
    video_dir = tmp_path / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    vm = VideoManager(data_dir=video_dir)

    job_dir = tmp_path / "jobs"
    job_dir.mkdir(parents=True, exist_ok=True)
    jm = JobManager(data_dir=job_dir)

    from src.api import routes
    monkeypatch.setattr(routes, "video_manager", vm)
    monkeypatch.setattr(routes, "job_manager", jm)

    # Seed an initial video
    vm.save_video("bg001.mp4", b"0123456789abcdef" * 64) # 1024 bytes
    return vm, jm

def test_get_videos_list(mock_video_env):
    vm, _ = mock_video_env
    resp = client.get("/api/videos")
    assert resp.status_code == 200
    data = resp.json()
    assert "videos" in data
    assert data["total"] == 1
    assert data["videos"][0]["filename"] == "bg001.mp4"
    assert data["videos"][0]["url"] == "/api/videos/bg001.mp4"

def test_upload_video(mock_video_env):
    vm, _ = mock_video_env
    video_content = b"fake video bytes for testing"
    files = {"file": ("party_lights.webm", io.BytesIO(video_content), "video/webm")}

    resp = client.post("/api/videos/upload", files=files)
    assert resp.status_code == 201
    data = resp.json()
    assert data["filename"] == "party_lights.webm"
    assert data["size_bytes"] == len(video_content)

    # Verify listed in GET /api/videos
    list_resp = client.get("/api/videos")
    assert list_resp.status_code == 200
    filenames = [v["filename"] for v in list_resp.json()["videos"]]
    assert "party_lights.webm" in filenames
    assert "bg001.mp4" in filenames

def test_upload_invalid_video_format(mock_video_env):
    files = {"file": ("script.py", io.BytesIO(b"print(1)"), "text/plain")}
    resp = client.post("/api/videos/upload", files=files)
    assert resp.status_code == 400
    assert "unsupported video format" in resp.json()["detail"].lower()

def test_stream_video_full_and_range(mock_video_env):
    vm, _ = mock_video_env
    # 1. Full GET
    resp = client.get("/api/videos/bg001.mp4")
    assert resp.status_code == 200
    assert resp.headers.get("accept-ranges") == "bytes"
    assert len(resp.content) == 1024

    # 2. Partial Content GET (Range: bytes=0-99)
    range_resp = client.get("/api/videos/bg001.mp4", headers={"Range": "bytes=0-99"})
    assert range_resp.status_code == 206
    assert range_resp.headers.get("content-range") == "bytes 0-99/1024"
    assert len(range_resp.content) == 100

    # 3. Partial Content GET (Range: bytes=500-)
    range_resp2 = client.get("/api/videos/bg001.mp4", headers={"Range": "bytes=500-"})
    assert range_resp2.status_code == 206
    assert range_resp2.headers.get("content-range") == "bytes 500-1023/1024"
    assert len(range_resp2.content) == 524

    # 4. Non-existent video 404
    not_found = client.get("/api/videos/missing.mp4")
    assert not_found.status_code == 404

def test_job_metadata_video_assignment_and_offset(mock_video_env):
    vm, jm = mock_video_env
    job = jm.create_job(SourceType.UPLOAD, "test_song.mp3", "Test Song", "Test Artist")
    assert job.video_id == "bg001.mp4"
    assert job.video_offset_seconds == 0.0

    # Update video assignment and start offset
    patch_resp = client.patch(
        f"/api/jobs/{job.job_id}",
        json={"video_id": "concert_stage.mp4", "video_offset_seconds": 15.5}
    )
    assert patch_resp.status_code == 200
    updated = patch_resp.json()
    assert updated["video_id"] == "concert_stage.mp4"
    assert updated["video_offset_seconds"] == 15.5

    # Verify persisted in job manager
    persisted = jm.get_job(job.job_id)
    assert persisted.video_id == "concert_stage.mp4"
    assert persisted.video_offset_seconds == 15.5
