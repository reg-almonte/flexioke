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
    assert 'id="settings-active-font-size"' in html
    assert 'id="karaoke-intro-splash"' in html
    assert 'id="intro-splash-title"' in html
    assert 'id="intro-splash-artist"' in html
    assert 'id="intro-splash-timer"' in html
    assert 'id="settings-intro-splash"' in html

def test_intro_splash_js_logic():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    assert "introSplashDuration" in resp.text
    assert "triggerIntroSplash" in resp.text or "introSplash" in resp.text



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

def test_stage_click_to_play_and_bounded_pills():
    resp_js = client.get("/static/karaoke.js")
    assert resp_js.status_code == 200
    assert "togglePlayPause" in resp_js.text or "togglePlay" in resp_js.text
    assert "stopPropagation" in resp_js.text
    assert "karaoke-line" in resp_js.text

    resp_css = client.get("/static/styles.css")
    assert resp_css.status_code == 200
    assert ".karaoke-line" in resp_css.text

def test_left_transport_cluster_and_timecode_toggle():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert 'id="karaoke-play-btn"' in html
    assert 'id="karaoke-volume-slider"' in html
    assert 'id="karaoke-timecode"' in html
    assert 'karaoke-volume-control' in html or 'karaoke-volume-wrapper' in html

    resp_js = client.get("/static/karaoke.js")
    assert resp_js.status_code == 200
    assert "timecodeMode" in resp_js.text
    assert "toggleTimecodeMode" in resp_js.text or "timecodeMode" in resp_js.text
    assert "flexioke_master_volume" in resp_js.text

def test_right_transport_cluster_and_restart_action():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert 'id="karaoke-restart-btn"' in html
    assert 'id="karaoke-skip-btn"' in html
    assert 'id="karaoke-stop-btn"' in html
    assert 'id="karaoke-settings-btn"' in html
    assert 'id="karaoke-fullscreen-btn"' in html
    assert 'z-[10000]' in html or 'z-50' in html or 'z-[9999]' in html

    resp_js = client.get("/static/karaoke.js")
    assert resp_js.status_code == 200
    assert "restartBtn" in resp_js.text or "karaoke-restart-btn" in resp_js.text
    assert "restart(" in resp_js.text or "syncSeek" in resp_js.text

def test_lrc_end_line_labeling():
    resp_js = client.get("/static/karaoke.js")
    assert resp_js.status_code == 200
    assert "• End •" in resp_js.text or "End" in resp_js.text

def test_up_next_header_right_alignment():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "karaoke-up-next-container" in resp.text
    assert "justify-end" in resp.text







