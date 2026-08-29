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
    assert 'id="karaoke-now-singing-text"' in html
    assert 'id="karaoke-up-next-text"' in html
    assert 'id="karaoke-countdown-cue"' in html
    assert 'id="karaoke-settings-modal"' in html
    assert 'id="settings-highlight-color"' in html
    assert 'id="settings-font-size"' in html

def test_karaoke_js_dual_header_marquee_logic():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "updateStageHeader" in resp.text
    assert "marquee" in resp.text.lower()

def test_marquee_css_rules():
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200
    assert "marquee" in resp.text



def test_karaoke_countdown_cue_logic():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "countdownCue" in resp.text or "countdown-cue" in resp.text
    assert "updateCountdownCue" in resp.text or "countdown" in resp.text.lower()

def test_karaoke_settings_and_font_scaling():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "flexioke_stage_config" in resp.text
    assert "applySettings" in resp.text or "baseFontSize" in resp.text



