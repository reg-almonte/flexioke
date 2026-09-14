import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_index_includes_studio_playlists_accordion():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "studio-card-playlists" in html
    assert "accordion-header-studio-playlists" in html
    assert "accordion-body-studio-playlists" in html
    assert "studio-playlists-count-badge" in html
    assert "studio-create-playlist-btn" in html
    assert "studio-playlists-directory-view" in html
    assert "studio-playlist-detail-view" in html

def test_lyrics_modal_includes_playlists_assignment_section():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "lyrics-modal-playlists-container" in html
    assert "lyrics-modal-playlist-feedback" in html

def test_playlists_js_implements_studio_and_modal_features():
    resp = client.get("/static/playlists.js")
    assert resp.status_code == 200
    js = resp.text
    assert "PlaylistsManager" in js or "flexiokePlaylists" in js
    assert "fetchPlaylists" in js
    assert "createPlaylist" in js
    assert "deletePlaylist" in js
    assert "reorderPlaylistSongs" in js or "reorder" in js
    assert "renderLyricsModalPlaylists" in js or "lyrics-modal-playlists" in js
