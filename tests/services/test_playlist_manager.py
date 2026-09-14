import pytest
import os
import json
from pathlib import Path
from src.models import (
    Playlist,
    PlaylistSummary,
    PlaylistDetail,
    PlaylistCreate,
    PlaylistUpdate,
    PlaylistSongAdd,
    PlaylistReorderRequest,
    PlaylistFromQueueRequest,
    JobRecord,
    SourceType,
    JobStatus,
)
from src.services.playlist_manager import PlaylistManager
from src.services.job_manager import JobManager

@pytest.fixture
def temp_env(tmp_path):
    jobs_dir = tmp_path / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    job_mgr = JobManager(data_dir=jobs_dir)
    
    playlist_file = tmp_path / "playlists.json"
    playlist_mgr = PlaylistManager(data_file=playlist_file)
    
    # Create sample jobs
    job1 = job_mgr.create_job(SourceType.UPLOAD, "song1.mp3", "Bohemian Rhapsody", "Queen")
    job_mgr.update_job(job1.job_id, status=JobStatus.COMPLETED, duration_seconds=354.0)
    
    job2 = job_mgr.create_job(SourceType.UPLOAD, "song2.mp3", "Hotel California", "Eagles")
    job_mgr.update_job(job2.job_id, status=JobStatus.COMPLETED, duration_seconds=390.0)

    return {
        "tmp_path": tmp_path,
        "job_mgr": job_mgr,
        "playlist_mgr": playlist_mgr,
        "playlist_file": playlist_file,
        "job1": job_mgr.get_job(job1.job_id),
        "job2": job_mgr.get_job(job2.job_id),
    }

def test_playlist_manager_bootstrap(temp_env):
    mgr = temp_env["playlist_mgr"]
    playlists = mgr.get_all_playlists()
    assert len(playlists) == 1
    fav = playlists[0]
    assert fav.id == "favorites"
    assert fav.name == "Favorites"
    assert fav.is_system is True
    assert fav.song_count == 0
    assert fav.total_duration_seconds == 0.0

def test_create_and_get_custom_playlist(temp_env):
    mgr = temp_env["playlist_mgr"]
    job_mgr = temp_env["job_mgr"]
    
    pl = mgr.create_playlist(name="Rock Classics", description="My favorite rock hits")
    assert pl.id.startswith("pl_")
    assert pl.name == "Rock Classics"
    assert pl.description == "My favorite rock hits"
    assert pl.is_system is False
    assert pl.song_ids == []
    
    # Retrieve it
    fetched = mgr.get_playlist(pl.id)
    assert fetched is not None
    assert fetched.name == "Rock Classics"

    # Summaries check
    summaries = mgr.get_all_playlists(job_mgr=job_mgr)
    assert len(summaries) == 2
    # System playlist is first
    assert summaries[0].id == "favorites"
    assert summaries[1].id == pl.id

def test_add_and_remove_songs(temp_env):
    mgr = temp_env["playlist_mgr"]
    job_mgr = temp_env["job_mgr"]
    job1 = temp_env["job1"]
    job2 = temp_env["job2"]
    
    pl = mgr.create_playlist(name="Party Vibes")
    
    # Add song 1
    updated = mgr.add_song(pl.id, job1.job_id, job_mgr=job_mgr)
    assert updated.song_ids == [job1.job_id]
    
    # Add duplicate song should raise ValueError
    with pytest.raises(ValueError, match="already exists"):
        mgr.add_song(pl.id, job1.job_id, job_mgr=job_mgr)

    # Add non-existent song should raise KeyError
    with pytest.raises(KeyError, match="Song not found"):
        mgr.add_song(pl.id, "non_existent_job", job_mgr=job_mgr)
        
    # Add song 2
    updated = mgr.add_song(pl.id, job2.job_id, job_mgr=job_mgr)
    assert updated.song_ids == [job1.job_id, job2.job_id]
    
    # Detail with resolved songs and duration
    detail = mgr.get_playlist_detail(pl.id, job_mgr=job_mgr)
    assert detail is not None
    assert detail.song_count == 2
    assert detail.total_duration_seconds == 744.0
    assert len(detail.songs) == 2
    assert detail.songs[0].job_id == job1.job_id
    assert detail.songs[1].job_id == job2.job_id
    
    # Remove song 1
    updated = mgr.remove_song(pl.id, job1.job_id)
    assert updated.song_ids == [job2.job_id]
    
    # Removing non-present song raises ValueError
    with pytest.raises(ValueError, match="not in playlist"):
        mgr.remove_song(pl.id, job1.job_id)

def test_reorder_songs(temp_env):
    mgr = temp_env["playlist_mgr"]
    job_mgr = temp_env["job_mgr"]
    job1 = temp_env["job1"]
    job2 = temp_env["job2"]
    
    pl = mgr.create_playlist(name="Setlist")
    mgr.add_song(pl.id, job1.job_id, job_mgr=job_mgr)
    mgr.add_song(pl.id, job2.job_id, job_mgr=job_mgr)
    
    # Reorder
    updated = mgr.reorder_songs(pl.id, [job2.job_id, job1.job_id])
    assert updated.song_ids == [job2.job_id, job1.job_id]
    
    # Invalid reorder (missing item) raises ValueError
    with pytest.raises(ValueError, match="Invalid song reorder list"):
        mgr.reorder_songs(pl.id, [job2.job_id])

def test_system_playlist_protection(temp_env):
    mgr = temp_env["playlist_mgr"]
    
    # Renaming favorites raises ValueError
    with pytest.raises(ValueError, match="Cannot rename system playlist"):
        mgr.update_playlist("favorites", name="New Name")
        
    # Updating description is allowed
    fav = mgr.update_playlist("favorites", description="Updated description")
    assert fav.description == "Updated description"
    assert fav.name == "Favorites"
    
    # Deleting favorites raises ValueError
    with pytest.raises(ValueError, match="Cannot delete system playlist"):
        mgr.delete_playlist("favorites")

def test_create_from_queue(temp_env):
    mgr = temp_env["playlist_mgr"]
    job_mgr = temp_env["job_mgr"]
    job1 = temp_env["job1"]
    job2 = temp_env["job2"]
    
    pl = mgr.create_from_queue(
        name="Queue Export",
        song_ids=[job1.job_id, job2.job_id, job1.job_id], # Contains duplicate
        description="Saved from active queue",
        job_mgr=job_mgr
    )
    assert pl.name == "Queue Export"
    assert pl.description == "Saved from active queue"
    # Duplicates pruned while preserving order
    assert pl.song_ids == [job1.job_id, job2.job_id]

def test_cascading_prune_on_song_deletion(temp_env):
    mgr = temp_env["playlist_mgr"]
    job_mgr = temp_env["job_mgr"]
    job1 = temp_env["job1"]
    job2 = temp_env["job2"]
    
    # Add to favorites and custom playlist
    mgr.add_song("favorites", job1.job_id, job_mgr=job_mgr)
    mgr.add_song("favorites", job2.job_id, job_mgr=job_mgr)
    
    pl = mgr.create_playlist(name="Custom List")
    mgr.add_song(pl.id, job1.job_id, job_mgr=job_mgr)
    
    # Prune job1
    pruned_count = mgr.prune_song_from_all_playlists(job1.job_id)
    assert pruned_count == 2
    
    assert mgr.get_playlist("favorites").song_ids == [job2.job_id]
    assert mgr.get_playlist(pl.id).song_ids == []

def test_orphan_pruning_on_detail_load(temp_env):
    mgr = temp_env["playlist_mgr"]
    job_mgr = temp_env["job_mgr"]
    job1 = temp_env["job1"]
    
    pl = mgr.create_playlist(name="Orphan Test")
    # Manually inject invalid ID
    pl.song_ids = [job1.job_id, "deleted_job_id_xyz"]
    mgr._save_playlists()
    
    detail = mgr.get_playlist_detail(pl.id, job_mgr=job_mgr)
    assert detail.song_count == 1
    assert detail.songs[0].job_id == job1.job_id
    assert mgr.get_playlist(pl.id).song_ids == [job1.job_id]
