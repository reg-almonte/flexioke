import pytest
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

from src.models import JobStatus, SourceType, JobRecord
from src.services.job_manager import JobManager
from src.main import app

@pytest.fixture
def temp_job_manager(tmp_path):
    manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    return manager

def test_create_and_get_job(temp_job_manager):
    job = temp_job_manager.create_job(
        source_type=SourceType.UPLOAD,
        source_name="test_song.mp3",
        title="Test Song"
    )
    assert job.job_id is not None
    assert job.status == JobStatus.QUEUED
    assert job.progress == 0
    assert job.title == "Test Song"
    
    # Check directory and JSON file created
    job_dir = temp_job_manager.get_job_dir(job.job_id)
    assert job_dir.exists()
    assert (job_dir / "job.json").exists()
    
    # Retrieve job
    retrieved = temp_job_manager.get_job(job.job_id)
    assert retrieved is not None
    assert retrieved.job_id == job.job_id
    assert retrieved.source_name == "test_song.mp3"

def test_update_job_status_and_stems(temp_job_manager):
    job = temp_job_manager.create_job(
        source_type=SourceType.YOUTUBE,
        source_name="https://youtube.com/watch?v=123",
        title="YT Track"
    )
    
    updated = temp_job_manager.update_job(
        job.job_id,
        status=JobStatus.SEPARATING_STAGE_1,
        progress=30,
        current_stage="Running Stage 1 (Mel-Band RoFormer)"
    )
    assert updated.status == JobStatus.SEPARATING_STAGE_1
    assert updated.progress == 30
    assert updated.current_stage == "Running Stage 1 (Mel-Band RoFormer)"
    
    # Complete job with stems
    completed = temp_job_manager.update_job(
        job.job_id,
        status=JobStatus.COMPLETED,
        progress=100,
        current_stage="Completed",
        stems={
            "instrumental": f"/api/jobs/{job.job_id}/stems/instrumental",
            "lead_vocals": f"/api/jobs/{job.job_id}/stems/lead_vocals",
            "backing_vocals": f"/api/jobs/{job.job_id}/stems/backing_vocals"
        }
    )
    assert completed.status == JobStatus.COMPLETED
    assert len(completed.stems) == 3

def test_job_not_found(temp_job_manager):
    assert temp_job_manager.get_job("non-existent-uuid") is None

def test_api_get_job_status(monkeypatch, tmp_path):
    test_manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    job = test_manager.create_job(
        source_type=SourceType.UPLOAD,
        source_name="sample.wav",
        title="Sample Audio"
    )
    
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", test_manager)
    
    client = TestClient(app)
    resp = client.get(f"/api/jobs/{job.job_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["job_id"] == job.job_id
    assert data["status"] == "queued"
    assert data["title"] == "Sample Audio"

def test_api_get_job_status_404(monkeypatch, tmp_path):
    test_manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", test_manager)
    
    client = TestClient(app)
    resp = client.get("/api/jobs/invalid-job-id")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
