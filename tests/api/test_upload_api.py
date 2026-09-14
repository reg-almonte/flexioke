import io
import pytest
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

def test_valid_mp3_upload(mock_job_manager):
    file_content = b"ID3\x03\x00\x00\x00\x00\x00#dummy mp3 audio content"
    files = {"file": ("Bohemian_Rhapsody.mp3", io.BytesIO(file_content), "audio/mpeg")}
    
    response = client.post("/api/jobs/upload", files=files)
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"
    assert data["title"] == "Bohemian Rhapsody"
    
    job = mock_job_manager.get_job(data["job_id"])
    assert job is not None
    assert job.source_type == SourceType.UPLOAD
    assert job.source_name == "Bohemian_Rhapsody.mp3"
    
    # Ensure input file was saved
    job_dir = mock_job_manager.get_job_dir(data["job_id"])
    input_files = list(job_dir.glob("input.*"))
    assert len(input_files) == 1
    assert input_files[0].name == "input.mp3"
    assert input_files[0].read_bytes() == file_content

def test_valid_wav_upload(mock_job_manager):
    file_content = b"RIFF....WAVEfmt dummy wav content"
    files = {"file": ("test_track.wav", io.BytesIO(file_content), "audio/wav")}
    
    response = client.post("/api/jobs/upload", files=files)
    assert response.status_code == 202
    data = response.json()
    assert data["title"] == "test track"

def test_invalid_extension_upload(mock_job_manager):
    file_content = b"malicious or unsupported text data"
    files = {"file": ("script.sh", io.BytesIO(file_content), "text/plain")}
    
    response = client.post("/api/jobs/upload", files=files)
    assert response.status_code == 400
    assert "unsupported file format" in response.json()["detail"].lower()

def test_file_size_exceeded(mock_job_manager, monkeypatch):
    # Mock max file size to 1KB for test efficiency
    from src.services import audio_validator
    monkeypatch.setattr(audio_validator, "MAX_FILE_SIZE_BYTES", 1024)
    
    large_content = b"0" * 2048
    files = {"file": ("large_song.mp3", io.BytesIO(large_content), "audio/mpeg")}
    
    response = client.post("/api/jobs/upload", files=files)
    assert response.status_code == 400
    assert "exceeds maximum allowed size" in response.json()["detail"].lower()
