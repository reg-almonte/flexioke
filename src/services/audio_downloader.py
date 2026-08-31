import re
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Tuple, Optional, Callable, Dict, Any

from src.services.audio_validator import parse_song_and_artist, MAX_FILE_SIZE_BYTES

ALLOWED_SCHEMES = {"http", "https"}

def validate_audio_url(url: str) -> Tuple[bool, str]:
    """Validates that a URL is a well-formed HTTP/HTTPS URL."""
    if not url or not isinstance(url, str):
        return False, "URL must be a non-empty string."
    
    url = url.strip()
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme.lower() not in ALLOWED_SCHEMES:
            return False, f"Invalid URL protocol '{parsed.scheme}'. Only HTTP and HTTPS URLs are supported."
        if not parsed.netloc:
            return False, "Invalid URL: missing host domain."
        return True, ""
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"

def download_audio_url(
    url: str,
    output_path: Path,
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> Dict[str, Any]:
    """
    Downloads an audio file from a direct HTTP/HTTPS URL with streaming and max size limits.
    Returns metadata dict: {'title': ..., 'artist': ..., 'filename': ..., 'duration': None}
    """
    url = url.strip()
    parsed = urllib.parse.urlparse(url)
    raw_filename = urllib.parse.unquote(Path(parsed.path).name)
    if not raw_filename or "." not in raw_filename:
        raw_filename = "downloaded_audio.mp3"
    
    title, artist = parse_song_and_artist(raw_filename)

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; Flexioke/0.2.4; +https://github.com/reg-almonte/flexioke)"}
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    total_downloaded = 0

    if progress_callback:
        progress_callback(5, "Connecting to audio URL...")

    with urllib.request.urlopen(req, timeout=30) as response:
        content_length = response.headers.get("Content-Length")
        total_size = int(content_length) if content_length and content_length.isdigit() else None

        if total_size and total_size > MAX_FILE_SIZE_BYTES:
            max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
            raise ValueError(f"File size exceeds maximum allowed limit of {max_mb:.0f}MB.")

        with open(output_path, "wb") as f_out:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                total_downloaded += len(chunk)
                if total_downloaded > MAX_FILE_SIZE_BYTES:
                    max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
                    raise ValueError(f"Downloaded stream exceeded maximum size of {max_mb:.0f}MB.")
                
                f_out.write(chunk)
                if progress_callback and total_size:
                    pct = int(5 + (total_downloaded / total_size) * 10)
                    progress_callback(min(pct, 15), f"Downloading audio ({total_downloaded // 1024} KB)...")

    if total_downloaded == 0:
        raise ValueError("Downloaded file is empty (0 bytes).")

    if progress_callback:
        progress_callback(15, "Audio download completed.")

    return {
        "title": title,
        "artist": artist,
        "filename": raw_filename,
        "duration": None
    }
