import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.job_manager import JobManager
from src.services.queue_manager import QueueManager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture
def mock_queue_environment(monkeypatch, tmp_path):
    job_mgr = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    queue_mgr = QueueManager()

    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", job_mgr)
    monkeypatch.setattr(routes, "queue_manager", queue_mgr)

    # Seed a completed job
    j1 = job_mgr.create_job(SourceType.UPLOAD, "track1.mp3", "Track One")
    job_mgr.update_job(j1.job_id, status=JobStatus.COMPLETED, progress=100, duration_seconds=180.0, stems={"instrumental": "url1"})

    j2 = job_mgr.create_job(SourceType.UPLOAD, "track2.mp3", "Track Two")
    job_mgr.update_job(j2.job_id, status=JobStatus.COMPLETED, progress=100, duration_seconds=200.0, stems={"instrumental": "url2"})

    return job_mgr, queue_mgr, j1, j2

def test_queue_operations(mock_queue_environment):
    job_mgr, queue_mgr, j1, j2 = mock_queue_environment

    # Initially empty
    resp = client.get("/api/queue")
    assert resp.status_code == 200
    assert resp.json()["total_queued"] == 0
    assert resp.json()["current_track"] is None

    # Add j1 to queue
    resp = client.post("/api/queue/add", json={"job_id": j1.job_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_queued"] == 1
    assert data["queue"][0]["title"] == "Track One"

    # Add j2 to queue
    resp = client.post("/api/queue/add", json={"job_id": j2.job_id})
    assert resp.status_code == 200
    assert resp.json()["total_queued"] == 2

    # Play now / Advance next
    resp = client.post("/api/queue/next")
    assert resp.status_code == 200
    data = resp.json()
    assert data["current_track"]["title"] == "Track One"
    assert data["total_queued"] == 1
    assert data["queue"][0]["title"] == "Track Two"

    # Remove item from queue
    item_to_remove = data["queue"][0]["queue_id"]
    resp = client.delete(f"/api/queue/{item_to_remove}")
    assert resp.status_code == 200
    assert resp.json()["total_queued"] == 0

def test_queue_play_now(mock_queue_environment):
    job_mgr, queue_mgr, j1, j2 = mock_queue_environment

    resp = client.post("/api/queue/play-now", json={"job_id": j2.job_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["current_track"]["title"] == "Track Two"

def test_add_nonexistent_or_incomplete_job(mock_queue_environment):
    job_mgr, queue_mgr, j1, j2 = mock_queue_environment

    # Incomplete job
    j_pending = job_mgr.create_job(SourceType.UPLOAD, "pending.mp3", "Pending")
    resp = client.post("/api/queue/add", json={"job_id": j_pending.job_id})
    assert resp.status_code == 400
    assert "not ready" in resp.json()["detail"].lower()

def test_queue_reorder_operations(mock_queue_environment):
    job_mgr, queue_mgr, j1, j2 = mock_queue_environment

    # Seed a third job
    j3 = job_mgr.create_job(SourceType.UPLOAD, "track3.mp3", "Track Three")
    job_mgr.update_job(j3.job_id, status=JobStatus.COMPLETED, progress=100, duration_seconds=150.0, stems={"instrumental": "url3"})

    # Add 3 jobs to queue
    client.post("/api/queue/add", json={"job_id": j1.job_id})
    client.post("/api/queue/add", json={"job_id": j2.job_id})
    resp = client.post("/api/queue/add", json={"job_id": j3.job_id})
    queue_data = resp.json()["queue"]
    assert [item["title"] for item in queue_data] == ["Track One", "Track Two", "Track Three"]

    id1 = queue_data[0]["queue_id"]
    id2 = queue_data[1]["queue_id"]
    id3 = queue_data[2]["queue_id"]

    # Reorder middle item up (Track Two moves to index 0)
    resp = client.post("/api/queue/reorder", json={"queue_id": id2, "direction": "up"})
    assert resp.status_code == 200
    assert [item["title"] for item in resp.json()["queue"]] == ["Track Two", "Track One", "Track Three"]

    # Reorder first item down (Track Two moves back to index 1)
    resp = client.post("/api/queue/reorder", json={"queue_id": id2, "direction": "down"})
    assert resp.status_code == 200
    assert [item["title"] for item in resp.json()["queue"]] == ["Track One", "Track Two", "Track Three"]

    # Boundary edge cases: moving top item up -> 400
    resp = client.post("/api/queue/reorder", json={"queue_id": id1, "direction": "up"})
    assert resp.status_code == 400

    # Boundary edge cases: moving bottom item down -> 400
    resp = client.post("/api/queue/reorder", json={"queue_id": id3, "direction": "down"})
    assert resp.status_code == 400

    # Invalid queue_id -> 404 or 400
    resp = client.post("/api/queue/reorder", json={"queue_id": "non-existent-id", "direction": "up"})
    assert resp.status_code in (400, 404)

    # Invalid direction -> 400
    resp = client.post("/api/queue/reorder", json={"queue_id": id2, "direction": "sideways"})
    assert resp.status_code == 400

