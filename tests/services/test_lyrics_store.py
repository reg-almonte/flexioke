import pytest
from src.services.job_manager import JobManager
from src.models import SourceType, LyricsResponse, LyricsUpdateRequest

@pytest.fixture
def temp_job_manager(tmp_path):
    return JobManager(data_dir=tmp_path / "jobs", max_workers=1)

def test_lyrics_models():
    req = LyricsUpdateRequest(lyrics="[00:01.00] Hello World")
    assert req.lyrics == "[00:01.00] Hello World"

    res = LyricsResponse(
        job_id="test-123",
        lyrics="[00:01.00] Hello World",
        has_lyrics=True,
        has_timestamps=True
    )
    assert res.has_timestamps is True

def test_get_lyrics_empty(temp_job_manager):
    job = temp_job_manager.create_job(SourceType.UPLOAD, "test.mp3", "Test Song")
    lyrics_res = temp_job_manager.get_lyrics(job.job_id)
    assert lyrics_res.job_id == job.job_id
    assert lyrics_res.has_lyrics is False
    assert lyrics_res.lyrics == ""
    assert lyrics_res.has_timestamps is False

def test_save_and_get_timestamped_lyrics(temp_job_manager):
    job = temp_job_manager.create_job(SourceType.UPLOAD, "test.mp3", "Test Song")
    lrc_content = "[00:00.18] If I could be anybody, I would be you\n[00:05.17] Maybe I'd understand the things that you do"
    
    saved = temp_job_manager.save_lyrics(job.job_id, lrc_content)
    assert saved.has_lyrics is True
    assert saved.has_timestamps is True
    assert saved.lyrics == lrc_content

    # Re-read
    loaded = temp_job_manager.get_lyrics(job.job_id)
    assert loaded.has_lyrics is True
    assert loaded.has_timestamps is True
    assert loaded.lyrics == lrc_content

def test_save_plain_text_lyrics(temp_job_manager):
    job = temp_job_manager.create_job(SourceType.UPLOAD, "test.mp3", "Test Song")
    plain_content = "Just plain lyrics without timestamps\nLine two of the song"
    
    saved = temp_job_manager.save_lyrics(job.job_id, plain_content)
    assert saved.has_lyrics is True
    assert saved.has_timestamps is False
    assert saved.lyrics == plain_content
