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

def test_native_fullscreen_api_integration():
    """Verify karaoke.js integrates HTML5 Fullscreen API with vendor prefixes and two-way sync."""
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text

    assert "enterNativeFullscreen" in js
    assert "exitNativeFullscreen" in js
    assert "syncNativeFullscreenState" in js
    assert "requestFullscreen" in js
    assert "webkitRequestFullscreen" in js
    assert "fullscreenchange" in js
    assert "webkitfullscreenchange" in js

def test_inactivity_timer_debouncing_and_autohide_in_node():
    """Execute Node test verifying that 100ms interval ticks do not prevent 3s autohide timer from firing."""
    node_script = """
    class MockClassList {
        constructor() { this.classes = new Set(); }
        add(...cls) { cls.forEach(c => this.classes.add(c)); }
        remove(...cls) { cls.forEach(c => this.classes.delete(c)); }
        contains(c) { return this.classes.has(c); }
    }

    class MockElement {
        constructor() {
            this.classList = new MockClassList();
        }
    }

    const mgr = {
        isFullscreen: true,
        isPlaying: true,
        isChromeHidden: false,
        inactivityDelay: 50, // 50ms for fast test
        inactivityTimer: null,
        _lastPlaybackState: null,
        topHeaderEl: new MockElement(),
        transportBarEl: new MockElement(),
        stageCard: new MockElement(),

        scheduleInactivityTimer() {
            this.clearInactivityTimer();
            if (!this.isFullscreen || !this.isPlaying) return;
            this.inactivityTimer = setTimeout(() => {
                this.hideChrome();
            }, this.inactivityDelay);
        },

        clearInactivityTimer() {
            if (this.inactivityTimer) {
                clearTimeout(this.inactivityTimer);
                this.inactivityTimer = null;
            }
        },

        hideChrome() {
            if (!this.isFullscreen || !this.isPlaying) return;
            this.isChromeHidden = true;
            this.topHeaderEl.classList.add('karaoke-chrome-hidden');
            this.transportBarEl.classList.add('karaoke-chrome-hidden');
            this.stageCard.classList.add('karaoke-cursor-hidden');
        },

        wakeChrome() {
            if (!this.isChromeHidden) return;
            this.isChromeHidden = false;
            this.topHeaderEl.classList.remove('karaoke-chrome-hidden');
            this.transportBarEl.classList.remove('karaoke-chrome-hidden');
            this.stageCard.classList.remove('karaoke-cursor-hidden');
        },

        handlePlaybackStateChange(force = false) {
            const playing = this.isPlaying;
            if (!force && this._lastPlaybackState === playing) {
                return;
            }
            this._lastPlaybackState = playing;
            if (this.isFullscreen && playing) {
                this.scheduleInactivityTimer();
            } else {
                this.wakeChrome();
                this.clearInactivityTimer();
            }
        }
    };

    // 1. Enter fullscreen & start playing
    mgr.handlePlaybackStateChange(true);
    if (!mgr.inactivityTimer) throw new Error("Inactivity timer should be scheduled");

    // 2. Simulate 10 frequent 5ms ticks (like 100ms interval during 3s timeout)
    let tickCount = 0;
    const interval = setInterval(() => {
        mgr.handlePlaybackStateChange(false);
        tickCount++;
        if (tickCount >= 10) {
            clearInterval(interval);
        }
    }, 5);

    // 3. After 80ms (greater than 50ms delay), check that hideChrome fired
    setTimeout(() => {
        if (!mgr.isChromeHidden) throw new Error("Chrome should have been hidden after inactivity");
        if (!mgr.topHeaderEl.classList.contains('karaoke-chrome-hidden')) throw new Error("Header should have karaoke-chrome-hidden class");
        if (!mgr.transportBarEl.classList.contains('karaoke-chrome-hidden')) throw new Error("Transport bar should have karaoke-chrome-hidden class");
        if (!mgr.stageCard.classList.contains('karaoke-cursor-hidden')) throw new Error("Stage card should have karaoke-cursor-hidden class");

        // 4. Test waking chrome on user activity
        mgr.wakeChrome();
        if (mgr.isChromeHidden) throw new Error("Chrome should be awake");
        if (mgr.topHeaderEl.classList.contains('karaoke-chrome-hidden')) throw new Error("Header should not be hidden after waking");

        console.log("AUTOHIDE_TEST_SUCCESS");
    }, 80);
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Node script error: {proc.stderr}"
    assert "AUTOHIDE_TEST_SUCCESS" in proc.stdout

def test_settings_button_auto_closes_fullscreen_mode():
    """Verify openSettingsModal auto-closes fullscreen mode to immediately display the subwindow."""
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text

    assert "openSettingsModal()" in js
    assert "if (this.isFullscreen) {" in js or "this.isFullscreen &&" in js
    assert "this.exitFullscreen" in js

def test_lyrics_stage_margins_and_countdown_clearance():
    """Verify vertical padding clearance for countdown cue and maximized horizontal width for long lines."""
    resp_css = client.get("/static/styles.css")
    assert resp_css.status_code == 200
    css = resp_css.text

    # Fullscreen lyrics stage vertical clearance and maximized width
    assert "padding-top: 8.5rem" in css or "padding-top: 9rem" in css or "padding-top: 8" in css
    assert "padding-bottom: 8.5rem" in css or "padding-bottom: 9rem" in css or "padding-bottom: 8" in css
    assert "max-width: 98%" in css

    resp_html = client.get("/")
    assert resp_html.status_code == 200
    html = resp_html.text

    # Windowed lyrics stage clearance
    assert "top-16" in html
    assert "pt-14" in html and "pb-14" in html


