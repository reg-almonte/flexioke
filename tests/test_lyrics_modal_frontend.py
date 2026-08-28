import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_lyrics_modal_in_html():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "lyrics-modal" in html
    assert "lyrics-edit-title" in html
    assert "lyrics-edit-artist" in html
    assert "lyrics-textarea" in html
    assert "save-lyrics-btn" in html

def test_library_js_contains_lyrics_modal_logic():
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    assert "openLyricsModal" in resp.text
    assert "lyricsEditTitle" in resp.text or "lyrics-edit-title" in resp.text
    assert "lyricsEditArtist" in resp.text or "lyrics-edit-artist" in resp.text

