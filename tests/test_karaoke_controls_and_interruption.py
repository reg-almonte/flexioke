import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_karaoke_controls_markup_in_html():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "karaoke-toggle-lead-btn" in html
    assert "karaoke-toggle-backing-btn" in html
    assert "play-confirm-modal" in html
    assert "confirm-play-btn" in html
    assert "confirm-cancel-btn" in html

def test_karaoke_script_contains_vocal_toggle_logic():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "karaoke-toggle-lead-btn" in resp.text or "toggleLead" in resp.text or "toggleMute" in resp.text

def test_compact_vocal_buttons_and_fullscreen_style():
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200
    assert "karaoke-toggle-lead-btn" in resp.text
    assert "karaoke-lead-status-text" in resp.text

