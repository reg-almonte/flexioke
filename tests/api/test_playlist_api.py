import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from unittest.mock import patch

from src.main import app
from src.services.job_manager import job_manager
from src.services.playlist_manager import playlist_manager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_data(tmp_path):
    orig_job_dir = job_manager.data_dir
    orig_pl_file = playlist_manager.data_file

    # Reconfigure job_manager and playlist_manager data dirs
    jobs_dir = tmp_path / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    job_manager.data_dir = jobs_dir
    job_manager._cache.clear()

    playlist_file = tmp_path / "playlists.json"
    playlist_manager.data_file = playlist_file
    playlist_manager._playlists.clear()
    playlist_manager._load_playlists()

    # Create two test jobs
    j1 = job_manager.create_job(SourceType.UPLOAD, "test1.mp3", "Song One", "Artist A")
    job_manager.update_job(j1.job_id, status=JobStatus.COMPLETED, duration_seconds=120.0)

    j2 = job_manager.create_job(SourceType.UPLOAD, "test2.mp3", "Song Two", "Artist B")
    job_manager.update_job(j2.job_id, status=JobStatus.COMPLETED, duration_seconds=180.0)

    yield {"job1_id": j1.job_id, "job2_id": j2.job_id}

    # Teardown: restore original dirs
    job_manager.data_dir = orig_job_dir
    job_manager._cache.clear()
    playlist_manager.data_file = orig_pl_file
    playlist_manager._playlists.clear()
    playlist_manager._load_playlists()


def test_get_playlists_initial(setup_test_data):
    response = client.get("/api/playlists")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "favorites"
    assert data[0]["is_system"] is True
    assert data[0]["song_count"] == 0
    assert data[0]["total_duration_seconds"] == 0.0

def test_create_custom_playlist(setup_test_data):
    # Valid creation
    payload = {"name": "My Acoustic Set", "description": "Chill songs"}
    response = client.post("/api/playlists", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Acoustic Set"
    assert data["description"] == "Chill songs"
    assert data["is_system"] is False
    assert data["song_ids"] == []
    playlist_id = data["id"]

    # Retrieve all playlists
    res_all = client.get("/api/playlists")
    assert res_all.status_code == 200
    summaries = res_all.json()
    assert len(summaries) == 2
    assert summaries[0]["id"] == "favorites"
    assert summaries[1]["id"] == playlist_id

    # Invalid creation: empty name
    res_empty = client.post("/api/playlists", json={"name": "   "})
    assert res_empty.status_code == 422 or res_empty.status_code == 400

def test_get_playlist_detail_and_404(setup_test_data):
    # Non-existent
    res_404 = client.get("/api/playlists/nonexistent_pl")
    assert res_404.status_code == 404

    # Existing favorites
    res_fav = client.get("/api/playlists/favorites")
    assert res_fav.status_code == 200
    fav_data = res_fav.json()
    assert fav_data["id"] == "favorites"
    assert fav_data["songs"] == []

def test_update_playlist(setup_test_data):
    res_create = client.post("/api/playlists", json={"name": "Original Name", "description": "Original Desc"})
    pl_id = res_create.json()["id"]

    # Valid update
    res_update = client.put(f"/api/playlists/{pl_id}", json={"name": "Updated Name", "description": "Updated Desc"})
    assert res_update.status_code == 200
    data = res_update.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Desc"

    # Attempt to rename favorites -> 400
    res_fav_rename = client.put("/api/playlists/favorites", json={"name": "Hacked Favorites"})
    assert res_fav_rename.status_code == 400

    # Updating favorites description -> 200
    res_fav_desc = client.put("/api/playlists/favorites", json={"description": "My curated favorites"})
    assert res_fav_desc.status_code == 200
    assert res_fav_desc.json()["description"] == "My curated favorites"

def test_delete_playlist(setup_test_data):
    res_create = client.post("/api/playlists", json={"name": "To Delete"})
    pl_id = res_create.json()["id"]

    # Delete custom playlist -> 200
    res_del = client.delete(f"/api/playlists/{pl_id}")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "deleted"

    # Verify gone
    assert client.get(f"/api/playlists/{pl_id}").status_code == 404

    # Delete non-existent -> 404
    assert client.delete(f"/api/playlists/{pl_id}").status_code == 404

    # Delete favorites -> 400
    res_del_fav = client.delete("/api/playlists/favorites")
    assert res_del_fav.status_code == 400

def test_add_and_remove_playlist_songs(setup_test_data):
    job1_id = setup_test_data["job1_id"]
    job2_id = setup_test_data["job2_id"]

    # Add to favorites
    res_add1 = client.post("/api/playlists/favorites/songs", json={"song_id": job1_id})
    assert res_add1.status_code == 200
    data = res_add1.json()
    assert data["song_count"] == 1
    assert data["total_duration_seconds"] == 120.0
    assert len(data["songs"]) == 1
    assert data["songs"][0]["job_id"] == job1_id

    # Duplicate add -> 409 Conflict
    res_dup = client.post("/api/playlists/favorites/songs", json={"song_id": job1_id})
    assert res_dup.status_code == 409

    # Add non-existent song -> 404
    res_missing_song = client.post("/api/playlists/favorites/songs", json={"song_id": "ghost_id"})
    assert res_missing_song.status_code == 404

    # Add second song
    res_add2 = client.post("/api/playlists/favorites/songs", json={"song_id": job2_id})
    assert res_add2.status_code == 200
    assert res_add2.json()["song_count"] == 2
    assert res_add2.json()["total_duration_seconds"] == 300.0

    # Remove song 1
    res_rem = client.delete(f"/api/playlists/favorites/songs/{job1_id}")
    assert res_rem.status_code == 200
    rem_data = res_rem.json()
    assert rem_data["song_count"] == 1
    assert rem_data["songs"][0]["job_id"] == job2_id

    # Remove already removed song -> 400 or 404
    assert client.delete(f"/api/playlists/favorites/songs/{job1_id}").status_code in (400, 404)

def test_reorder_playlist_songs(setup_test_data):
    job1_id = setup_test_data["job1_id"]
    job2_id = setup_test_data["job2_id"]

    res_create = client.post("/api/playlists", json={"name": "Reorder Test"})
    pl_id = res_create.json()["id"]

    client.post(f"/api/playlists/{pl_id}/songs", json={"song_id": job1_id})
    client.post(f"/api/playlists/{pl_id}/songs", json={"song_id": job2_id})

    # Reorder
    res_reorder = client.put(f"/api/playlists/{pl_id}/reorder", json={"song_ids": [job2_id, job1_id]})
    assert res_reorder.status_code == 200
    data = res_reorder.json()
    assert [s["job_id"] for s in data["songs"]] == [job2_id, job1_id]

    # Invalid reorder list -> 400
    res_invalid = client.put(f"/api/playlists/{pl_id}/reorder", json={"song_ids": [job2_id]})
    assert res_invalid.status_code == 400

def test_create_from_queue_endpoint(setup_test_data):
    job1_id = setup_test_data["job1_id"]
    job2_id = setup_test_data["job2_id"]

    payload = {
        "name": "Live Set from Queue",
        "description": "Exported queue",
        "song_ids": [job2_id, job1_id, job2_id] # Contains duplicate
    }
    response = client.post("/api/playlists/from-queue", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Live Set from Queue"
    assert data["song_count"] == 2
    assert [s["job_id"] for s in data["songs"]] == [job2_id, job1_id]

def test_cascading_song_deletion_endpoint(setup_test_data):
    job1_id = setup_test_data["job1_id"]
    job2_id = setup_test_data["job2_id"]

    # Add job1 to favorites and custom playlist
    client.post("/api/playlists/favorites/songs", json={"song_id": job1_id})
    res_pl = client.post("/api/playlists", json={"name": "Cleanup Test"})
    pl_id = res_pl.json()["id"]
    client.post(f"/api/playlists/{pl_id}/songs", json={"song_id": job1_id})
    client.post(f"/api/playlists/{pl_id}/songs", json={"song_id": job2_id})

    # Delete job1 via DELETE /api/jobs/{id}
    res_del_job = client.delete(f"/api/jobs/{job1_id}")
    assert res_del_job.status_code == 200

    # Verify job1 was pruned from favorites
    fav_detail = client.get("/api/playlists/favorites").json()
    assert fav_detail["song_count"] == 0

    # Verify job1 was pruned from custom playlist
    custom_detail = client.get(f"/api/playlists/{pl_id}").json()
    assert custom_detail["song_count"] == 1
    assert custom_detail["songs"][0]["job_id"] == job2_id
