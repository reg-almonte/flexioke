import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_player_script_served():
    resp = client.get("/static/player.js")
    assert resp.status_code == 200
    assert "MultitrackPlayer" in resp.text or "FlexiokePlayer" in resp.text or "loadSong" in resp.text

def test_index_includes_player_script():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "/static/player.js" in resp.text

def test_player_seek_to_method():
    resp = client.get("/static/player.js")
    assert resp.status_code == 200
    assert "seekTo(" in resp.text

