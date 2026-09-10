import re
import mimetypes
import threading
from pathlib import Path
from typing import List, Optional

from src.models import VideoInfo

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv"}

MIME_TYPE_MAP = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".mkv": "video/x-matroska",
}

class VideoManager:
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            self.data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "videos"
        else:
            self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def sanitize_filename(self, filename: str) -> str:
        """Strips directory traversal components and unsafe characters from a filename."""
        name = Path(filename).name
        # Keep alphanumeric, dashes, underscores, dots
        clean = re.sub(r"[^\w\-\.]", "_", name)
        return clean.strip("._") or "video.mp4"

    def get_content_type(self, filename: str) -> str:
        """Determines the MIME content-type for a video filename."""
        ext = Path(filename).suffix.lower()
        if ext in MIME_TYPE_MAP:
            return MIME_TYPE_MAP[ext]
        mime, _ = mimetypes.guess_type(filename)
        return mime or "video/mp4"

    def list_videos(self) -> List[VideoInfo]:
        """Scans the video data directory and returns a sorted list of discovered videos."""
        with self._lock:
            if not self.data_dir.exists():
                return []
            videos: List[VideoInfo] = []
            for file_path in sorted(self.data_dir.iterdir(), key=lambda p: p.name.lower()):
                if file_path.is_file() and file_path.suffix.lower() in ALLOWED_VIDEO_EXTENSIONS:
                    try:
                        stat = file_path.stat()
                        videos.append(
                            VideoInfo(
                                id=file_path.name,
                                filename=file_path.name,
                                size_bytes=stat.st_size,
                                url=f"/api/videos/{file_path.name}"
                            )
                        )
                    except Exception:
                        pass
            return videos

    def save_video(self, filename: str, content: bytes) -> VideoInfo:
        """Validates and persists a video file to the video storage directory."""
        safe_name = self.sanitize_filename(filename)
        ext = Path(safe_name).suffix.lower()
        if ext not in ALLOWED_VIDEO_EXTENSIONS:
            raise ValueError(
                f"Unsupported video format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_VIDEO_EXTENSIONS))}"
            )

        with self._lock:
            dest_path = self.data_dir / safe_name
            dest_path.write_bytes(content)
            stat = dest_path.stat()
            return VideoInfo(
                id=safe_name,
                filename=safe_name,
                size_bytes=stat.st_size,
                url=f"/api/videos/{safe_name}"
            )

    def get_video_path(self, filename: str) -> Optional[Path]:
        """Resolves and validates a video path, preventing path traversal attacks."""
        safe_name = Path(filename).name
        target = (self.data_dir / safe_name).resolve()
        base = self.data_dir.resolve()

        if base in target.parents or target == base:
            if target.exists() and target.is_file() and target.suffix.lower() in ALLOWED_VIDEO_EXTENSIONS:
                return target
        return None

# Singleton instance
video_manager = VideoManager()
