import json
import pytest
from unittest.mock import patch, MagicMock
from src.services.lrclib_client import LRCLIBClient

@pytest.fixture
def client():
    return LRCLIBClient()

def test_get_lyrics_exact_match(client):
    mock_response_data = {
        "id": 12345,
        "trackName": "Last Birthday",
        "artistName": "Valley",
        "duration": 237.0,
        "syncedLyrics": "[00:08.02] Line 1\n[00:12.03] Line 2",
        "plainLyrics": "Line 1\nLine 2"
    }

    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = json.dumps(mock_response_data).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = client.get_lyrics(track_name="Last Birthday", artist_name="Valley")

        assert res["found"] is True
        assert res["id"] == 12345
        assert res["track_name"] == "Last Birthday"
        assert res["artist_name"] == "Valley"
        assert res["has_timestamps"] is True
        assert "[00:08.02] Line 1" in res["lyrics"]

def test_get_lyrics_fallback_to_search(client):
    mock_search_data = [
        {
            "id": 67890,
            "trackName": "Last Birthday",
            "artistName": "Valley",
            "duration": 237.0,
            "syncedLyrics": "[00:08.02] Synced fallback line",
            "plainLyrics": "Synced fallback line"
        }
    ]

    mock_search_resp = MagicMock()
    mock_search_resp.status = 200
    mock_search_resp.read.return_value = json.dumps(mock_search_data).encode("utf-8")
    mock_search_resp.__enter__.return_value = mock_search_resp

    import urllib.error
    http_err = urllib.error.HTTPError("https://lrclib.net/api/get", 404, "Not Found", {}, None)

    with patch("urllib.request.urlopen", side_effect=[http_err, mock_search_resp]):
        res = client.get_lyrics(track_name="Last Birthday", artist_name="Valley")

        assert res["found"] is True
        assert res["id"] == 67890
        assert res["has_timestamps"] is True
        assert "Synced fallback line" in res["lyrics"]

def test_get_lyrics_not_found(client):
    import urllib.error
    http_err = urllib.error.HTTPError("https://lrclib.net/api/get", 404, "Not Found", {}, None)

    mock_empty_search = MagicMock()
    mock_empty_search.status = 200
    mock_empty_search.read.return_value = json.dumps([]).encode("utf-8")
    mock_empty_search.__enter__.return_value = mock_empty_search

    with patch("urllib.request.urlopen", side_effect=[http_err, mock_empty_search]):
        res = client.get_lyrics(track_name="Unknown Song", artist_name="Unknown Artist")

        assert res["found"] is False
        assert res["lyrics"] == ""
        assert res["has_timestamps"] is False

def test_search_lyrics_success(client):
    mock_search_data = [
        {
            "id": 111,
            "trackName": "Song A",
            "artistName": "Artist A",
            "duration": 180.0,
            "syncedLyrics": "[00:01.00] Test",
            "plainLyrics": "Test"
        }
    ]

    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = json.dumps(mock_search_data).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        results = client.search_lyrics("Song A")
        assert len(results) == 1
        assert results[0]["id"] == 111
        assert results[0]["track_name"] == "Song A"
        assert results[0]["has_synced_lyrics"] is True
