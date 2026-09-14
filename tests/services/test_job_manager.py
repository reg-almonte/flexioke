import json
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

def test_job_record_with_artist(temp_job_manager):
    job = temp_job_manager.create_job(
        source_type=SourceType.UPLOAD,
        source_name="artist_song.mp3",
        title="Come Alive",
        artist="Rachel Taylor"
    )
    assert job.title == "Come Alive"
    assert job.artist == "Rachel Taylor"

    retrieved = temp_job_manager.get_job(job.job_id)
    assert retrieved is not None
    assert retrieved.artist == "Rachel Taylor"

def test_legacy_job_json_without_artist_loads_gracefully(tmp_path):
    # Simulate a legacy v0.1.0/v0.2.0 job.json file without an artist field
    legacy_job_dir = tmp_path / "jobs" / "legacy-uuid-1234"
    legacy_job_dir.mkdir(parents=True)
    legacy_json = {
        "job_id": "legacy-uuid-1234",
        "source_type": "upload",
        "source_name": "legacy_track.mp3",
        "title": "Legacy Track",
        "status": "completed",
        "progress": 100,
        "current_stage": "Ready for playback",
        "error": None,
        "duration_seconds": 120.0,
        "stems": {},
        "created_at": "2026-08-27T00:00:00Z",
        "updated_at": "2026-08-27T00:00:00Z"
    }
    import json
    (legacy_job_dir / "job.json").write_text(json.dumps(legacy_json), encoding="utf-8")

    manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    job = manager.get_job("legacy-uuid-1234")
    assert job is not None
    assert job.title == "Legacy Track"
    assert job.artist is None

    # Updating artist on legacy job
    updated = manager.update_job("legacy-uuid-1234", artist="Legacy Artist")
    assert updated.artist == "Legacy Artist"
    
    # Verify persisted to disk
    reloaded = json.loads((legacy_job_dir / "job.json").read_text(encoding="utf-8"))
    assert reloaded["artist"] == "Legacy Artist"

def test_startup_prunes_leftover_queued_and_in_progress_jobs(tmp_path):
    """Verify that restarting the server / initializing JobManager automatically cleans up uncompleted queued/in-flight jobs."""
    jobs_dir = tmp_path / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = tmp_path / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # 1. Completed job (should be kept)
    comp_dir = jobs_dir / "comp-job-1"
    comp_dir.mkdir(parents=True)
    (comp_dir / "job.json").write_text(json.dumps({
        "job_id": "comp-job-1",
        "source_type": "upload",
        "source_name": "comp.mp3",
        "title": "Completed Song",
        "status": "completed",
        "progress": 100,
        "current_stage": "Ready",
        "stems": {"instrumental": "/stems/inst.mp3"},
        "created_at": "2026-09-01T00:00:00Z",
        "updated_at": "2026-09-01T00:00:00Z"
    }), encoding="utf-8")

    # 2. Queued job from previous session (should be pruned)
    queued_dir = jobs_dir / "queued-job-2"
    queued_dir.mkdir(parents=True)
    (queued_dir / "job.json").write_text(json.dumps({
        "job_id": "queued-job-2",
        "source_type": "upload",
        "source_name": "queued.mp3",
        "title": "Queued Song",
        "status": "queued",
        "progress": 0,
        "current_stage": "Queued",
        "stems": {},
        "created_at": "2026-09-01T00:01:00Z",
        "updated_at": "2026-09-01T00:01:00Z"
    }), encoding="utf-8")
    queued_archive = archive_dir / "queued-job-2_audio.mp3"
    queued_archive.write_text("dummy", encoding="utf-8")

    # 3. In-flight Stage 1 job from previous session (should be pruned)
    stage1_dir = jobs_dir / "stage1-job-3"
    stage1_dir.mkdir(parents=True)
    (stage1_dir / "job.json").write_text(json.dumps({
        "job_id": "stage1-job-3",
        "source_type": "youtube",
        "source_name": "https://youtube.com/watch?v=xyz",
        "title": "In Flight Song",
        "status": "separating_stage_1",
        "progress": 45,
        "current_stage": "Stage 1",
        "stems": {},
        "created_at": "2026-09-01T00:02:00Z",
        "updated_at": "2026-09-01T00:02:00Z"
    }), encoding="utf-8")

    # Initialize JobManager (simulating server restart)
    manager = JobManager(data_dir=jobs_dir, max_workers=1)

    # Verify completed job is preserved
    assert manager.get_job("comp-job-1") is not None
    assert comp_dir.exists()

    # Verify queued and in-flight jobs are pruned from cache and disk
    assert manager.get_job("queued-job-2") is None
    assert not queued_dir.exists()
    assert not queued_archive.exists()

    assert manager.get_job("stage1-job-3") is None
    assert not stage1_dir.exists()

    # Verify list_jobs returns only completed job
    all_jobs = manager.list_jobs(status=None)
    assert len(all_jobs) == 1
    assert all_jobs[0].job_id == "comp-job-1"


