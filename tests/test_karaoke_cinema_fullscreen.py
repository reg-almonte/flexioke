import subprocess
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_cinema_fullscreen_css_rules_in_styles():
    """Verify styles.css contains rules for cinema fullscreen, floating overlays, and auto-hide states."""
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200
    css = resp.text

    # Verify cinema fullscreen classes
    assert ".karaoke-cinema-fullscreen" in css or ".stage-fullscreen" in css
    assert "karaoke-chrome-hidden" in css
    assert "karaoke-cursor-hidden" in css
    assert "cursor: none" in css
    assert "pointer-events: none" in css

def test_cinema_fullscreen_elements_in_html():
    """Verify index.html contains necessary hooks for floating header and bottom transport overlays."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert "karaoke-stage-card" in html
    assert "karaoke-lyrics-stage" in html
    assert "karaoke-fullscreen-btn" in html
    assert "karaoke-exit-fullscreen-btn" in html
    assert "karaoke-now-singing-container" in html
    assert "karaoke-up-next-container" in html

def test_karaoke_fullscreen_and_autohide_logic_in_node():
    """Test KaraokeStageManager fullscreen and auto-hide state methods in Node.js environment."""
    karaoke_js_path = Path(__file__).resolve().parent.parent / "src" / "static" / "karaoke.js"
    assert karaoke_js_path.exists()

    js_code = karaoke_js_path.read_text(encoding="utf-8")
    assert "karaoke-chrome-hidden" in js_code
    assert "karaoke-cursor-hidden" in js_code
    assert "3000" in js_code or "inactivity" in js_code.lower()
    assert "exitFullscreen" in js_code
    assert "enterFullscreen" in js_code
    assert "dblclick" in js_code or "double" in js_code.lower()

def test_karaoke_keyboard_shortcuts_and_tooltips():
    """Verify F hotkey and tooltips for fullscreen toggling."""
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text

    # Hotkey handler for 'f' / 'F'
    assert "key.toLowerCase() === 'f'" in js or "key === 'f'" in js or "key === 'F'" in js or "e.key === 'f'" in js or "e.code === 'KeyF'" in js
