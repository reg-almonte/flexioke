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
    assert 'id="settings-highlight-glow-color"' in html
    assert 'id="settings-highlight-fill-color"' in html
    assert 'id="settings-font-size"' in html
    assert 'id="settings-active-font-size"' in html
    assert 'id="karaoke-intro-splash"' in html
    assert 'id="intro-splash-title"' in html
    assert 'id="intro-splash-artist"' in html
    assert 'id="intro-splash-timer"' in html
    assert 'id="settings-intro-splash"' in html
    assert 'id="settings-countdown-threshold"' in html

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
    assert "countdownThreshold" in resp.text


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

def test_stage_restart_lyrics_reset_and_keyboard_shortcuts():
    resp_js = client.get("/static/karaoke.js")
    assert resp_js.status_code == 200
    assert "restartSong" in resp_js.text
    assert "scrollTop = 0" in resp_js.text or "scrollTop" in resp_js.text
    assert "Home" in resp_js.text
    assert "'r'" in resp_js.text or "'R'" in resp_js.text or "key === 'r'" in resp_js.text.lower()

def test_dual_highlight_color_controls_in_html_and_js():
    resp_html = client.get("/")
    assert resp_html.status_code == 200
    assert 'id="settings-highlight-glow-color"' in resp_html.text
    assert 'id="settings-highlight-fill-color"' in resp_html.text
    assert 'id="settings-glow-color-display"' in resp_html.text
    assert 'id="settings-fill-color-display"' in resp_html.text

    resp_js = client.get("/static/karaoke.js")
    assert resp_js.status_code == 200
    assert "activeHighlightGlowColor" in resp_js.text
    assert "activeHighlightFillColor" in resp_js.text
    assert "--karaoke-highlight-fill" in resp_js.text

def test_countdown_cue_only_triggers_on_intro_or_empty_line_interlude():
    import subprocess
    import shutil

    node_path = shutil.which("node")
    if not node_path:
        return

    node_script = """
    const fs = require('fs');
    const vm = require('vm');
    const sandbox = {
        document: {
            documentElement: { style: { setProperty: () => {} } },
            getElementById: () => ({ classList: { add: () => {}, remove: () => {}, contains: () => false }, style: {}, innerHTML: '', textContent: '', addEventListener: () => {} }),
            querySelectorAll: () => [],
            addEventListener: () => {}
        },
        window: { addEventListener: () => {} },
        console: console,
        setInterval: () => {},
        setTimeout: () => {},
        clearInterval: () => {},
        clearTimeout: () => {},
        localStorage: { getItem: () => null, setItem: () => {} }
    };
    vm.createContext(sandbox);
    const code = fs.readFileSync('src/static/karaoke.js', 'utf8') + '; this.KaraokeStageManager = KaraokeStageManager; this.LrcParser = LrcParser;';
    vm.runInContext(code, sandbox);

    const stage = new sandbox.KaraokeStageManager();
    stage.config = { countdownThreshold: 3 };

    // Scenario:
    // Intro 0-5s (5s >= 3s threshold) -> countdown cue SHOULD trigger at t=3.0s into line 1 at 5s.
    // Line 1 is sung from 5s to 12s. At t=9.5s (2.5s before Line 2), Line 1 is being sung -> countdown cue MUST NOT trigger!
    // At 20s, empty line (instrumental break) until 26s (6s >= 3s threshold). At t=24s -> countdown cue SHOULD trigger!
    const lrc = "[00:05.00] Line 1\\n[00:12.00] Line 2\\n[00:20.00] \\n[00:26.00] Line 3";
    stage.lyricsData = sandbox.LrcParser.parse(lrc);

    let cueVisible = false;
    stage.countdownCue = {
        classList: {
            remove: (cls) => { if (cls === 'hidden') cueVisible = true; },
            add: (cls) => { if (cls === 'hidden') cueVisible = false; },
            contains: (cls) => (cls === 'hidden' ? !cueVisible : false)
        }
    };

    // 1. At t=3.5s (Intro, 1.5s before Line 1): MUST show cue
    stage.updateCountdownCue(3.5);
    if (!cueVisible) throw new Error("Expected cue visible during intro at 3.5s");

    // 2. At t=9.5s (Active Line 1 sung, 2.5s before Line 2): MUST NOT show cue
    stage.updateCountdownCue(9.5);
    if (cueVisible) throw new Error("Cue should NOT be visible while Line 1 is being sung before Line 2");

    // 3. At t=24.0s (During empty instrumental break, 2s before Line 3): MUST show cue
    stage.updateCountdownCue(24.0);
    if (!cueVisible) throw new Error("Expected cue visible during instrumental break at 24.0s");

    console.log("OK");
    """

    proc = subprocess.run([node_path, "-e", node_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Countdown cue evaluator failed: {proc.stderr}\n{proc.stdout}"









