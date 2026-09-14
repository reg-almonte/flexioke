import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_lrclib_get_endpoint_success():
    mock_result = {
        "found": True,
        "id": 12345,
        "track_name": "Last Birthday",
        "artist_name": "Valley",
        "duration": 237.0,
        "synced_lyrics": "[00:08.02] Line 1",
        "plain_lyrics": "Line 1",
        "lyrics": "[00:08.02] Line 1",
        "has_timestamps": True
    }

    with patch("src.services.lrclib_client.lrclib_client.get_lyrics", return_value=mock_result):
        resp = client.get("/api/lyrics/lrclib/get?title=Last%20Birthday&artist=Valley")
        assert resp.status_code == 200
        data = resp.json()
        assert data["found"] is True
        assert data["track_name"] == "Last Birthday"
        assert data["has_timestamps"] is True
        assert "[00:08.02] Line 1" in data["lyrics"]

def test_lrclib_get_endpoint_missing_title():
    resp = client.get("/api/lyrics/lrclib/get")
    assert resp.status_code == 422  # validation error for required title query param

def test_lrclib_search_endpoint_success():
    mock_results = [
        {
            "id": 111,
            "track_name": "Last Birthday",
            "artist_name": "Valley",
            "album_name": "Last Birthday",
            "duration": 237.0,
            "has_synced_lyrics": True,
            "synced_lyrics": "[00:08.02] Line 1",
            "plain_lyrics": "Line 1",
            "lyrics": "[00:08.02] Line 1"
        }
    ]

    with patch("src.services.lrclib_client.lrclib_client.search_lyrics", return_value=mock_results):
        resp = client.get("/api/lyrics/lrclib/search?q=valley%20last%20birthday")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["track_name"] == "Last Birthday"
        assert data["results"][0]["has_synced_lyrics"] is True
