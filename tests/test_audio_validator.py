import pytest
from src.services.audio_validator import clean_song_title, parse_song_and_artist, validate_audio_file

def test_parse_song_and_artist_with_hyphen():
    title, artist = parse_song_and_artist("Queen - Bohemian Rhapsody.mp3")
    assert title == "Bohemian Rhapsody"
    assert artist == "Queen"

def test_parse_song_and_artist_with_track_number_prefix():
    title, artist = parse_song_and_artist("01. Eagles - Hotel California.flac")
    assert title == "Hotel California"
    assert artist == "Eagles"

    title2, artist2 = parse_song_and_artist("02 - Guns_N_Roses - Sweet_Child_O_Mine.mp3")
    assert title2 == "Sweet Child O Mine"
    assert artist2 == "Guns N Roses"

def test_parse_song_and_artist_without_delimiter():
    title, artist = parse_song_and_artist("Imagine_Track.wav")
    assert title == "Imagine Track"
    assert artist == "Unknown Artist"

    title2, artist2 = parse_song_and_artist("03. Imagine.wav")
    assert title2 == "Imagine"
    assert artist2 == "Unknown Artist"

def test_validate_audio_file_supported():
    is_valid, msg = validate_audio_file("song.mp3", 1024 * 1024)
    assert is_valid is True
    assert msg == ""

def test_validate_audio_file_unsupported_extension():
    is_valid, msg = validate_audio_file("video.mp4", 1024)
    assert is_valid is False
    assert "Unsupported file format" in msg
