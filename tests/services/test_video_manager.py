import pytest
from pathlib import Path
from src.services.video_manager import VideoManager

@pytest.fixture
def temp_video_manager(tmp_path):
    video_dir = tmp_path / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    return VideoManager(data_dir=video_dir)

def test_list_videos_empty_and_auto_discover(temp_video_manager, tmp_path):
    # Initial empty list
    videos = temp_video_manager.list_videos()
    assert len(videos) == 0

    # Add dummy video files directly to folder
    v1 = temp_video_manager.data_dir / "bg001.mp4"
    v1.write_bytes(b"dummy mp4 content")
    v2 = temp_video_manager.data_dir / "anime_bg.webm"
    v2.write_bytes(b"dummy webm content")
    v3 = temp_video_manager.data_dir / "ignored.txt"
    v3.write_bytes(b"not a video")

    videos = temp_video_manager.list_videos()
    assert len(videos) == 2
    filenames = [v.filename for v in videos]
    assert "anime_bg.webm" in filenames
    assert "bg001.mp4" in filenames
    assert "ignored.txt" not in filenames

def test_save_video_valid_and_invalid(temp_video_manager):
    # Valid save
    info = temp_video_manager.save_video("stage_lights.mp4", b"00000000")
    assert info.filename == "stage_lights.mp4"
    assert info.size_bytes == 8
    assert info.url == "/api/videos/stage_lights.mp4"
    assert (temp_video_manager.data_dir / "stage_lights.mp4").exists()

    # Invalid extension
    with pytest.raises(ValueError, match="Unsupported video format"):
        temp_video_manager.save_video("malicious.exe", b"malicious data")

    # Filename sanitization / path traversal prevention
    info2 = temp_video_manager.save_video("../../etc/evil.mp4", b"evil data")
    assert info2.filename == "evil.mp4"
    assert (temp_video_manager.data_dir / "evil.mp4").exists()

def test_get_video_path(temp_video_manager):
    temp_video_manager.save_video("loop.mp4", b"loop data")
    path = temp_video_manager.get_video_path("loop.mp4")
    assert path is not None
    assert path.name == "loop.mp4"

    # Non-existent
    assert temp_video_manager.get_video_path("non_existent.mp4") is None

    # Path traversal attempt
    assert temp_video_manager.get_video_path("../../../etc/passwd") is None
