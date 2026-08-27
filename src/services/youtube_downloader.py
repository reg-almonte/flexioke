import re
from pathlib import Path
from typing import Tuple, Dict, Any
import yt_dlp

YOUTUBE_REGEX = re.compile(
    r"^(https?://)?(www\.|m\.|music\.)?(youtube\.com/(watch\?.*v=|v/|embed/)|youtu\.be/)([\w\-]+)"
)
MAX_YOUTUBE_DURATION_SECONDS = 900  # 15 minutes

def validate_youtube_url(url: str) -> Tuple[bool, str]:
    """Validates whether a given URL matches a valid YouTube link format."""
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string."
    
    url = url.strip()
    if not YOUTUBE_REGEX.match(url):
        return False, "Invalid YouTube URL format. Must be a valid youtube.com or youtu.be link."
    
    return True, ""

def download_youtube_audio(url: str, output_path: Path) -> Dict[str, Any]:
    """
    Downloads audio stream from YouTube using yt-dlp.
    Saves the output audio file to output_path and returns metadata dictionary.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # yt-dlp template without extension because postprocessor adds .mp3
    output_stem = output_path.with_suffix("")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_stem) + ".%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info first without full download to check duration
        info = ydl.extract_info(url, download=False)
        if not info:
            raise ValueError("Could not extract video metadata from YouTube URL.")

        duration = info.get("duration") or 0
        if duration > MAX_YOUTUBE_DURATION_SECONDS:
            raise ValueError(
                f"Video duration ({duration / 60:.1f} minutes) exceeds the maximum allowed limit of {MAX_YOUTUBE_DURATION_SECONDS / 60:.0f} minutes."
            )

        # Download audio
        info = ydl.extract_info(url, download=True)
        title = info.get("title") or "YouTube Audio Track"
        duration = float(info.get("duration") or 0.0)

        # Confirm the output file exists
        expected_mp3 = output_stem.with_suffix(".mp3")
        if not expected_mp3.exists():
            # If ffmpeg wasn't available for postprocessing, check whatever audio file was written
            candidates = list(output_path.parent.glob(f"{output_stem.name}.*"))
            if candidates:
                expected_mp3 = candidates[0]

        return {
            "title": title,
            "duration": duration,
            "file_path": str(expected_mp3),
            "filename": expected_mp3.name
        }
