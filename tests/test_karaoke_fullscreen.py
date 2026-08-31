import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_fullscreen_button_in_html():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "karaoke-fullscreen-btn" in html

def test_karaoke_js_contains_fullscreen_logic():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "fullscreen" in resp.text.lower()

def test_fullscreen_css_rules():
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200
    assert "stage-fullscreen" in resp.text
    assert "var(--karaoke-font-size" in resp.text

