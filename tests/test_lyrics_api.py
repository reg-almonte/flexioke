import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.job_manager import JobManager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture
def mock_lyrics_env(monkeypatch, tmp_path):
    manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", manager)

    job = manager.create_job(SourceType.UPLOAD, "song.mp3", "Sample Track")
    manager.update_job(job.job_id, status=JobStatus.COMPLETED, progress=100)

    return manager, job

def test_get_lyrics_initial_empty(mock_lyrics_env):
    manager, job = mock_lyrics_env
    resp = client.get(f"/api/jobs/{job.job_id}/lyrics")
    assert resp.status_code == 200
    data = resp.json()
    assert data["job_id"] == job.job_id
    assert data["has_lyrics"] is False
    assert data["lyrics"] == ""

def test_post_and_get_lyrics(mock_lyrics_env):
    manager, job = mock_lyrics_env
    lrc_text = "[00:01.00] Line one\n[00:04.50] Line two"

    post_resp = client.post(
        f"/api/jobs/{job.job_id}/lyrics",
        json={"lyrics": lrc_text}
    )
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["has_lyrics"] is True
    assert data["has_timestamps"] is True
    assert data["lyrics"] == lrc_text

    # Verify GET
    get_resp = client.get(f"/api/jobs/{job.job_id}/lyrics")
    assert get_resp.status_code == 200
    assert get_resp.json()["lyrics"] == lrc_text

def test_lyrics_endpoints_404_invalid_job():
    get_resp = client.get("/api/jobs/invalid-job-id/lyrics")
    assert get_resp.status_code == 404

    post_resp = client.post(
        "/api/jobs/invalid-job-id/lyrics",
        json={"lyrics": "Sample"}
    )
    assert post_resp.status_code == 404
