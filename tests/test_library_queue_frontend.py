import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_library_queue_script_served():
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    assert "SongLibraryManager" in resp.text
    assert "Unknown Artist" in resp.text or "artist" in resp.text.lower()

def test_index_includes_library_queue_script():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "/static/library_queue.js" in resp.text
    assert "Search by song title or artist" in resp.text

