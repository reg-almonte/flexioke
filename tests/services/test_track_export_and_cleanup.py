import io
import zipfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.job_manager import JobManager
from src.services.queue_manager import QueueManager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture
def test_setup(monkeypatch, tmp_path):
    data_dir = tmp_path / "data" / "jobs"
    archive_dir = tmp_path / "data" / "archive"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    jm = JobManager(data_dir=data_dir, max_workers=1)
    qm = QueueManager()

    from src.api import routes
    from src.services import pipeline

    monkeypatch.setattr(routes, "job_manager", jm)
    monkeypatch.setattr(routes, "queue_manager", qm)
    monkeypatch.setattr(pipeline, "job_manager", jm)

    return {"jm": jm, "qm": qm, "data_dir": data_dir, "archive_dir": archive_dir}

def test_export_stems_zip_success(test_setup):
    jm = test_setup["jm"]
    job = jm.create_job(SourceType.UPLOAD, "test.mp3", "Awesome Track", "Great Artist")
    job_dir = jm.get_job_dir(job.job_id)

    # Create mock stem files
    (job_dir / "instrumental.mp3").write_bytes(b"dummy instrumental mp3 data")
    (job_dir / "lead_vocals.mp3").write_bytes(b"dummy lead vocals mp3 data")
    (job_dir / "backing_vocals.mp3").write_bytes(b"dummy backing vocals mp3 data")
    (job_dir / "lyrics.lrc").write_text("[00:01.00]Hello world\n[00:05.00]Singing karaoke", encoding="utf-8")

    jm.update_job(job.job_id, status=JobStatus.COMPLETED, progress=100)

    # Call ZIP export endpoint
    resp = client.get(f"/api/jobs/{job.job_id}/export/zip")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/zip"
    assert "Awesome_Track_stems.zip" in resp.headers.get("content-disposition", "")

    # Unpack and verify zip contents
    zip_bytes = io.BytesIO(resp.content)
    with zipfile.ZipFile(zip_bytes, "r") as zf:
        namelist = zf.namelist()
        assert "instrumental.mp3" in namelist
        assert "lead_vocals.mp3" in namelist
        assert "backing_vocals.mp3" in namelist
        assert "lyrics.lrc" in namelist
        assert zf.read("instrumental.mp3") == b"dummy instrumental mp3 data"
        assert "[00:01.00]Hello world" in zf.read("lyrics.lrc").decode("utf-8")

def test_export_stems_zip_alias(test_setup):
    jm = test_setup["jm"]
    job = jm.create_job(SourceType.UPLOAD, "test2.mp3", "Second Song")
    job_dir = jm.get_job_dir(job.job_id)

    (job_dir / "instrumental.mp3").write_bytes(b"mp3 1")
    (job_dir / "lead_vocals.mp3").write_bytes(b"mp3 2")
    (job_dir / "backing_vocals.mp3").write_bytes(b"mp3 3")
    jm.update_job(job.job_id, status=JobStatus.COMPLETED)

    resp = client.get(f"/api/jobs/{job.job_id}/download-all.zip")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/zip"

def test_export_stems_zip_not_completed(test_setup):
    jm = test_setup["jm"]
    job = jm.create_job(SourceType.UPLOAD, "test3.mp3", "Incomplete Song")

    resp = client.get(f"/api/jobs/{job.job_id}/export/zip")
    assert resp.status_code == 400
    assert "not completed" in resp.json()["detail"]

def test_export_stems_zip_not_found(test_setup):
    resp = client.get("/api/jobs/non-existent-id/export/zip")
    assert resp.status_code == 404

def test_delete_job_and_cascade_cleanup(test_setup):
    jm = test_setup["jm"]
    qm = test_setup["qm"]
    archive_dir = test_setup["archive_dir"]

    job = jm.create_job(SourceType.UPLOAD, "song_to_delete.mp3", "Delete Me Song")
    job_dir = jm.get_job_dir(job.job_id)
    (job_dir / "instrumental.mp3").write_bytes(b"data")

    # Put in queue
    qm.add_to_queue(job.job_id, "Delete Me Song")
    assert len(qm.queue) == 1

    # Place mock archive file
    archive_file = archive_dir / f"{job.job_id}_song_to_delete.mp3"
    archive_file.write_bytes(b"archived raw audio")
    assert archive_file.exists()

    # Call DELETE /api/jobs/{job_id}
    resp = client.delete(f"/api/jobs/{job.job_id}")
    assert resp.status_code == 200
    assert resp.json()["job_id"] == job.job_id

    # Verify job record removed
    assert jm.get_job(job.job_id) is None
    # Verify disk folder removed
    assert not job_dir.exists()
    # Verify queue cleared
    assert len(qm.queue) == 0
    # Verify archive file cleaned up
    assert not archive_file.exists()

def test_delete_job_not_found(test_setup):
    resp = client.delete("/api/jobs/non-existent-id")
    assert resp.status_code == 404
