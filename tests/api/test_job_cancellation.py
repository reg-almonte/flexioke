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

def test_cancel_queued_job(tmp_path):
    jm = JobManager(data_dir=tmp_path)
    job = jm.create_job(SourceType.UPLOAD, "test.mp3", "Test Song")
    assert job.status == JobStatus.QUEUED

    cancelled = jm.cancel_job(job.job_id)
    assert cancelled is not None
    assert cancelled.status == JobStatus.CANCELLED
    assert cancelled.current_stage == "Cancelled by user"

def test_cancel_job_endpoint(mock_job_manager):
    job = mock_job_manager.create_job(SourceType.UPLOAD, "test2.mp3", "Test Song 2")
    
    resp = client.post(f"/api/jobs/{job.job_id}/cancel")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "cancelled"
    assert data["job_id"] == job.job_id
