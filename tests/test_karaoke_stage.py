import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_karaoke_script_served():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "LrcParser" in resp.text
    assert "KaraokeStageManager" in resp.text

def test_index_includes_karaoke_script():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "/static/karaoke.js" in resp.text

def test_karaoke_stage_markup_structure():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert 'id="karaoke-lyrics-stage"' in html
    assert 'id="karaoke-song-title"' in html
    assert 'id="karaoke-timecode"' in html
