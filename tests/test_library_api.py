import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.job_manager import JobManager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture
def mock_job_library(monkeypatch, tmp_path):
    manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", manager)
    
    # Create sample jobs
    j1 = manager.create_job(SourceType.UPLOAD, "bohemian_rhapsody.mp3", "Bohemian Rhapsody")
    manager.update_job(j1.job_id, status=JobStatus.COMPLETED, progress=100, stems={"instrumental": "url1"})

    j2 = manager.create_job(SourceType.YOUTUBE, "https://youtube.com/watch?v=hotel_california", "Hotel California")
    manager.update_job(j2.job_id, status=JobStatus.COMPLETED, progress=100, stems={"instrumental": "url2"})

    j3 = manager.create_job(SourceType.UPLOAD, "in_progress_track.wav", "In Progress Track")
    manager.update_job(j3.job_id, status=JobStatus.SEPARATING_STAGE_1, progress=25)

    return manager

def test_list_completed_jobs_by_default(mock_job_library):
    resp = client.get("/api/jobs")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    titles = [j["title"] for j in data["jobs"]]
    assert "Bohemian Rhapsody" in titles
    assert "Hotel California" in titles
    assert "In Progress Track" not in titles

def test_search_jobs_with_query(mock_job_library):
    resp = client.get("/api/jobs?q=bohemian")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["jobs"][0]["title"] == "Bohemian Rhapsody"

def test_search_jobs_no_match(mock_job_library):
    resp = client.get("/api/jobs?q=nonexistent")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert len(data["jobs"]) == 0

def test_list_all_jobs_explicit_status(mock_job_library):
    resp = client.get("/api/jobs?status=separating_stage_1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["jobs"][0]["title"] == "In Progress Track"
