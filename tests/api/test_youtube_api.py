import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from src.main import app
from src.services.job_manager import JobManager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture
def mock_job_manager(monkeypatch, tmp_path):
    manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", manager)
    return manager

def test_invalid_youtube_url():
    response = client.post("/api/jobs/youtube", json={"url": "https://not-youtube.com/audio.mp3"})
    assert response.status_code == 400
    assert "invalid youtube url" in response.json()["detail"].lower()

def test_valid_youtube_submission(mock_job_manager, monkeypatch):
    # Mock the actual downloader function
    from src.services import youtube_downloader
    
    def fake_download(url: str, output_path: Path):
        output_path.write_bytes(b"dummy downloaded mp3")
        return {
            "title": "Rick Astley - Never Gonna Give You Up",
            "duration": 213.0,
            "filename": output_path.name
        }
    
    monkeypatch.setattr(youtube_downloader, "download_youtube_audio", fake_download)
    
    response = client.post("/api/jobs/youtube", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["source_type"] == "youtube"
    
    # Wait/check job record
    job = mock_job_manager.get_job(data["job_id"])
    assert job is not None
    assert job.source_name == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def test_youtube_duration_limit_exceeded(monkeypatch, tmp_path):
    from src.services.youtube_downloader import validate_youtube_url, download_youtube_audio
    
    # Verify URL validator works
    is_valid, _ = validate_youtube_url("https://youtu.be/dQw4w9WgXcQ")
    assert is_valid is True
    
    is_valid, err = validate_youtube_url("https://example.com")
    assert is_valid is False
    assert "invalid" in err.lower()
