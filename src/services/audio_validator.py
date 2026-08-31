import re
from pathlib import Path
from typing import Tuple

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

def parse_song_and_artist(filename: str) -> Tuple[str, str]:
    """
    Parses a filename into (title, artist).
    Handles '<Song Title> - <Artist>.<ext>', stripping leading track numbers
    and normalizing underscores to spaces.
    """
    stem = Path(filename).stem
    # Strip leading track numbers like '01. ', '01 - ', '01 '
    stem_cleaned = re.sub(r"^\d{1,3}[\.\-_\s]+", "", stem).strip()
    if not stem_cleaned:
        stem_cleaned = stem

    # Normalize space/underscore hyphen delimiters like ' - ', '_-_', ' _- ', etc.
    stem_normalized = re.sub(r"[_\s]+-[_\s]+", " - ", stem_cleaned)

    if " - " in stem_normalized:
        parts = stem_normalized.split(" - ", 1)
        title = re.sub(r"_+", " ", parts[0]).strip()
        artist = re.sub(r"_+", " ", parts[1]).strip()
        return (title or "Untitled Track", artist or "Unknown Artist")
    
    title = re.sub(r"[_\-]+", " ", stem_cleaned).strip()
    return (title or "Untitled Track", "Unknown Artist")

def clean_song_title(filename: str) -> str:
    """Derives a clean, readable song display title from a filename."""
    title, _ = parse_song_and_artist(filename)
    return title

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
