import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_playlists_script_served():
    resp = client.get("/static/playlists.js")
    assert resp.status_code == 200
    assert "flexiokeFavorites" in resp.text or "FavoritesManager" in resp.text
    assert "toggleFavorite" in resp.text
    assert "flexioke:favorites-toggled" in resp.text

def test_index_includes_playlists_script():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "/static/playlists.js" in resp.text

def test_heart_toggle_buttons_rendered_in_library_and_catalog():
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    assert "favorite-toggle-btn" in resp.text or "fav-btn" in resp.text
    assert "toggleFavorite" in resp.text or "flexiokeFavorites" in resp.text
    assert "flexioke:favorites-toggled" in resp.text

def test_heart_button_styles_and_attributes():
    resp = client.get("/static/playlists.js")
    assert resp.status_code == 200
    # Should handle both favorited ♥ and unfavorited ♡
    assert "♥" in resp.text
    assert "♡" in resp.text
    assert "isFavorite" in resp.text
