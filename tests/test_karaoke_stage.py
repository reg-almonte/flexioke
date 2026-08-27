import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_karaoke_script_served():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "LrcParser" in resp.text or "KaraokeStageManager" in resp.text

def test_index_includes_karaoke_script():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "/static/karaoke.js" in resp.text
