import io
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from src.main import app
from src.models import SourceType, JobStatus
from src.services.job_manager import JobManager

client = TestClient(app)

@pytest.fixture
def temp_job_environment(monkeypatch, tmp_path):
    job_mgr = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", job_mgr)
    return job_mgr

def test_source_type_side_ab_enum():
    """Verify SourceType enum includes SIDE_AB."""
    assert SourceType.SIDE_AB == "side_ab"
    assert SourceType.SIDE_AB.value == "side_ab"

def test_upload_side_b_only(temp_job_environment):
    """Verify POST /api/jobs/upload-side-ab with Side B creates instant completed job."""
    fake_audio = b"\xFF\xFB\x90\x44" + b"\x00" * 1024  # minimal fake MP3 bytes
    
    files = {
        "file_side_b": ("test_track_instrumental.mp3", io.BytesIO(fake_audio), "audio/mpeg")
    }
    data = {
        "title": "Dual Track Song",
        "artist": "The Duo"
    }

    resp = client.post("/api/jobs/upload-side-ab", files=files, data=data)
    assert resp.status_code == 200
    job = resp.json()

    assert job["source_type"] == "side_ab"
    assert job["title"] == "Dual Track Song"
    assert job["artist"] == "The Duo"
    assert job["status"] == "completed"
    assert job["progress"] == 100
    assert "instrumental" in job["stems"]
    assert "lead_vocals" not in job["stems"]

    # Verify stem retrieval
    job_id = job["job_id"]
    stem_resp = client.get(f"/api/jobs/{job_id}/stems/instrumental")
    assert stem_resp.status_code == 200
    assert len(stem_resp.content) > 0

def test_upload_side_a_and_side_b(temp_job_environment):
    """Verify POST /api/jobs/upload-side-ab with both Side A and Side B."""
    fake_audio_b = b"\xFF\xFB\x90\x44" + b"\x00" * 512
    fake_audio_a = b"\xFF\xFB\x90\x44" + b"\x01" * 512

    files = {
        "file_side_b": ("instrumental_part.mp3", io.BytesIO(fake_audio_b), "audio/mpeg"),
        "file_side_a": ("vocal_part.mp3", io.BytesIO(fake_audio_a), "audio/mpeg")
    }
    data = {
        "title": "Complete Side AB Song",
        "artist": "Star Artist"
    }

    resp = client.post("/api/jobs/upload-side-ab", files=files, data=data)
    assert resp.status_code == 200
    job = resp.json()

    assert job["source_type"] == "side_ab"
    assert job["status"] == "completed"
    assert "instrumental" in job["stems"]
    assert "lead_vocals" in job["stems"]

    job_id = job["job_id"]
    stem_b_resp = client.get(f"/api/jobs/{job_id}/stems/instrumental")
    assert stem_b_resp.status_code == 200
    stem_a_resp = client.get(f"/api/jobs/{job_id}/stems/lead_vocals")
    assert stem_a_resp.status_code == 200

def test_attach_side_a_to_existing_job(temp_job_environment):
    """Verify POST /api/jobs/{job_id}/attach-side-a attaches vocal track to existing track."""
    fake_audio_b = b"\xFF\xFB\x90\x44" + b"\x00" * 512
    files = {
        "file_side_b": ("solo_instrumental.mp3", io.BytesIO(fake_audio_b), "audio/mpeg")
    }
    resp = client.post("/api/jobs/upload-side-ab", files=files)
    assert resp.status_code == 200
    job = resp.json()
    job_id = job["job_id"]
    assert "lead_vocals" not in job["stems"]

    # Attach Side A
    fake_audio_a = b"\xFF\xFB\x90\x44" + b"\x02" * 512
    attach_files = {
        "file": ("new_vocal.mp3", io.BytesIO(fake_audio_a), "audio/mpeg")
    }
    attach_resp = client.post(f"/api/jobs/{job_id}/attach-side-a", files=attach_files)
    assert attach_resp.status_code == 200
    updated_job = attach_resp.json()

    assert "lead_vocals" in updated_job["stems"]

    # Check that lead_vocals stem is now accessible
    stem_a_resp = client.get(f"/api/jobs/{job_id}/stems/lead_vocals")
    assert stem_a_resp.status_code == 200

def test_upload_side_ab_invalid_files(temp_job_environment):
    """Verify invalid file types are rejected."""
    bad_files = {
        "file_side_b": ("corrupted.txt", io.BytesIO(b"not an audio file"), "text/plain")
    }
    resp = client.post("/api/jobs/upload-side-ab", files=bad_files)
    assert resp.status_code == 400
    assert "unsupported" in resp.json()["detail"].lower() or "invalid" in resp.json()["detail"].lower()

def test_side_ab_ui_elements_in_html():
    """Verify index.html contains the Side A/B upload tab and dual file upload dropzones."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert "tab-side-ab-btn" in html
    assert "tab-side-ab-content" in html
    assert "side-b-file-input" in html
    assert "side-a-file-input" in html
    assert "submit-side-ab-btn" in html
