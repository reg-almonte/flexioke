import re
from pathlib import Path
from typing import Tuple

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

def clean_song_title(filename: str) -> str:
    """Derives a clean, readable song display title from a filename."""
    stem = Path(filename).stem
    # Replace underscores, hyphens with spaces, collapse multiple spaces
    cleaned = re.sub(r"[_\-]+", " ", stem).strip()
    return cleaned if cleaned else "Untitled Track"

def validate_audio_file(filename: str, file_size: int) -> Tuple[bool, str]:
    """
    Validates audio file extension and size.
    Returns (is_valid, error_message).
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file format '{ext}'. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
    
    if file_size > MAX_FILE_SIZE_BYTES:
        max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
        return False, f"File size ({file_size / (1024 * 1024):.1f}MB) exceeds maximum allowed size of {max_mb:.0f}MB."

    return True, ""
