import pytest
from src.services.audio_validator import clean_song_title, parse_song_and_artist, validate_audio_file

def test_parse_song_and_artist_with_hyphen():
    title, artist = parse_song_and_artist("Bohemian Rhapsody - Queen.mp3")
    assert title == "Bohemian Rhapsody"
    assert artist == "Queen"

def test_parse_song_and_artist_with_track_number_prefix():
    title, artist = parse_song_and_artist("01. Hotel California - Eagles.flac")
    assert title == "Hotel California"
    assert artist == "Eagles"

    title2, artist2 = parse_song_and_artist("02 - Sweet_Child_O_Mine - Guns_N_Roses.mp3")
    assert title2 == "Sweet Child O Mine"
    assert artist2 == "Guns N Roses"

def test_parse_song_and_artist_without_delimiter():
    title, artist = parse_song_and_artist("Imagine_Track.wav")
    assert title == "Imagine Track"
    assert artist == "Unknown Artist"

def test_validate_audio_file_supported():
    is_valid, msg = validate_audio_file("song.mp3", 1024 * 1024)
    assert is_valid is True
    assert msg == ""

def test_validate_audio_file_unsupported_extension():
    is_valid, msg = validate_audio_file("video.mp4", 1024)
    assert is_valid is False
    assert "Unsupported file format" in msg
