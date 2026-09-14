import subprocess
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_stage_geometry_elements_in_html():
    """Verify index.html contains stage geometry range sliders and live value displays."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert 'id="settings-fullscreen-width"' in html
    assert 'id="settings-fullscreen-width-display"' in html
    assert 'id="settings-fullscreen-height"' in html
    assert 'id="settings-fullscreen-height-display"' in html
    assert 'id="settings-fullscreen-v-offset"' in html
    assert 'id="settings-fullscreen-v-offset-display"' in html

def test_stage_geometry_css_variables_in_styles_css():
    """Verify styles.css defines root geometry variables and scopes them to fullscreen lyrics stage."""
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200
    css = resp.text

    assert "--karaoke-fullscreen-stage-width" in css
    assert "--karaoke-fullscreen-stage-max-height" in css
    assert "--karaoke-fullscreen-stage-v-offset" in css
    assert "calc(50% + var(--karaoke-fullscreen-stage-v-offset" in css

def test_stage_geometry_logic_in_karaoke_js():
    """Verify karaoke.js defines geometry default configs, bindings, and CSS variable updates."""
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text

    assert "fullscreenStageWidth" in js
    assert "fullscreenStageHeight" in js
    assert "fullscreenStageVOffset" in js
    assert "--karaoke-fullscreen-stage-width" in js
    assert "--karaoke-fullscreen-stage-max-height" in js
    assert "--karaoke-fullscreen-stage-v-offset" in js
    assert "settingFullscreenWidthInput" in js

def test_stage_geometry_simulation_in_node():
    """Simulate stage geometry configuration, live CSS variable binding, and persistence in Node.js."""
    node_script = """
    class MockStorage {
        constructor() { this.store = {}; }
        getItem(key) { return this.store[key] || null; }
        setItem(key, val) { this.store[key] = String(val); }
    }

    const mockLocalStorage = new MockStorage();
    const mockDocumentStyle = {
        properties: {},
        setProperty(name, val) { this.properties[name] = val; },
        getProperty(name) { return this.properties[name]; }
    };

    const defaultConfig = {
        introSplashDuration: 3,
        countdownThreshold: 3,
        activeHighlightGlowColor: '#06b6d4',
        activeHighlightFillColor: '#0891b2',
        baseFontSizePx: 20,
        activeFontSizePx: 24,
        fullscreenStageWidth: 98,
        fullscreenStageHeight: 56,
        fullscreenStageVOffset: 0
    };

    class MockKaraokeStageManager {
        constructor() {
            this.defaultConfig = { ...defaultConfig };
            this.config = { ...this.defaultConfig };
            this.loadSettings();
        }

        loadSettings() {
            const raw = mockLocalStorage.getItem('flexioke_stage_config');
            if (raw) {
                this.config = { ...this.defaultConfig, ...JSON.parse(raw) };
            } else {
                this.config = { ...this.defaultConfig };
            }
            this.applySettings();
        }

        applySettings() {
            const widthPct = parseInt(this.config.fullscreenStageWidth, 10) || 98;
            const heightVh = parseInt(this.config.fullscreenStageHeight, 10) || 56;
            const vOffsetPct = (typeof this.config.fullscreenStageVOffset !== 'undefined') ? parseInt(this.config.fullscreenStageVOffset, 10) : 0;

            mockDocumentStyle.setProperty('--karaoke-fullscreen-stage-width', `${widthPct}%`);
            mockDocumentStyle.setProperty('--karaoke-fullscreen-stage-max-height', `${heightVh}vh`);
            mockDocumentStyle.setProperty('--karaoke-fullscreen-stage-v-offset', `${vOffsetPct}%`);
        }

        saveSettings(newConfig) {
            this.config = { ...this.config, ...newConfig };
            mockLocalStorage.setItem('flexioke_stage_config', JSON.stringify(this.config));
            this.applySettings();
        }
    }

    // 1. Initial State Check
    const manager = new MockKaraokeStageManager();
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-width') !== '98%') throw new Error("Default width not 98%");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-max-height') !== '56vh') throw new Error("Default height not 56vh");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-v-offset') !== '0%') throw new Error("Default offset not 0%");

    // 2. Adjust Geometry Settings
    manager.saveSettings({
        fullscreenStageWidth: 85,
        fullscreenStageHeight: 48,
        fullscreenStageVOffset: -10
    });

    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-width') !== '85%') throw new Error("Updated width failed");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-max-height') !== '48vh') throw new Error("Updated height failed");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-v-offset') !== '-10%') throw new Error("Updated vOffset failed");

    // 3. Persistence Check on Reload
    const reloadedManager = new MockKaraokeStageManager();
    if (reloadedManager.config.fullscreenStageWidth !== 85) throw new Error("Persisted width mismatch");
    if (reloadedManager.config.fullscreenStageHeight !== 48) throw new Error("Persisted height mismatch");
    if (reloadedManager.config.fullscreenStageVOffset !== -10) throw new Error("Persisted vOffset mismatch");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-width') !== '85%') throw new Error("Reloaded style property width failed");

    // 4. Reset Defaults
    reloadedManager.saveSettings(reloadedManager.defaultConfig);
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-width') !== '98%') throw new Error("Reset width failed");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-max-height') !== '56vh') throw new Error("Reset height failed");
    if (mockDocumentStyle.getProperty('--karaoke-fullscreen-stage-v-offset') !== '0%') throw new Error("Reset vOffset failed");

    console.log("STAGE_GEOMETRY_SUCCESS");
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    assert proc.returncode == 0, f"Node script error: {proc.stderr}"
    assert "STAGE_GEOMETRY_SUCCESS" in proc.stdout
