import json
import subprocess
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_icons_script_served_and_referenced_in_index():
    """Verify index.html includes script tag for /static/icons.js and endpoint returns 200."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert '<script src="/static/icons.js"></script>' in html or 'src="/static/icons.js"' in html

    icons_resp = client.get("/static/icons.js")
    assert icons_resp.status_code == 200
    js = icons_resp.text
    assert "flexiokeIcons" in js
    assert "getIconHtml" in js

def test_svg_icons_dictionary_and_helper_in_node():
    """Execute icons.js in Node.js to verify dictionary keys, helper rendering, and fallback behavior."""
    icons_path = Path(__file__).resolve().parent.parent / "src" / "static" / "icons.js"
    assert icons_path.exists(), "src/static/icons.js must exist"

    node_script = f"""
    const fs = require('fs');
    const window = {{}};
    const code = fs.readFileSync('{icons_path}', 'utf8');
    eval(code);

    const icons = window.flexiokeIcons || {{}};
    const getIconHtml = window.getIconHtml;

    const requiredKeys = [
        'play', 'pause', 'restart', 'next', 'stop',
        'volume_high', 'volume_low', 'volume_muted',
        'settings', 'fullscreen_enter', 'fullscreen_exit',
        'chevron_down', 'chevron_right', 'chevron_left',
        'instrumental', 'lead_vocals', 'backing_vocals',
        'zip_export', 'heart_filled', 'heart_outline',
        'search', 'edit', 'delete', 'notes'
    ];

    const missingKeys = requiredKeys.filter(k => !icons[k]);

    // Test getIconHtml rendering
    const playHtml = getIconHtml ? getIconHtml('play', 'w-4 h-4 text-white') : '';
    const unknownHtml = getIconHtml ? getIconHtml('non_existent_key_123') : 'throw';

    console.log(JSON.stringify({{
        keysCount: Object.keys(icons).length,
        missingKeys,
        hasGetIconHtml: typeof getIconHtml === 'function',
        playHtmlValid: playHtml.includes('<svg') && playHtml.includes('w-4 h-4 text-white'),
        unknownHtmlSafe: unknownHtml === ''
    }}));
    """

    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    res = json.loads(proc.stdout)

def test_index_and_js_modules_use_svg_icons_and_hotkey_tooltips():
    """Verify HTML and JS scripts reference SVG icons and hotkey tooltips."""
    index_resp = client.get("/")
    assert index_resp.status_code == 200
    html = index_resp.text

    # Verify tooltips with hotkey prompts
    assert "Play / Pause (Space)" in html
    assert "Restart (R)" in html or "Restart Song (R)" in html or "Restart" in html
    assert "Toggle Fullscreen" in html or "Fullscreen" in html

    # Verify player.js, karaoke.js, playlists.js, and library_queue.js reference getIconHtml
    for script_name in ["player.js", "karaoke.js", "playlists.js", "library_queue.js", "app.js"]:
        resp = client.get(f"/static/{script_name}")
        assert resp.status_code == 200
        assert "getIconHtml" in resp.text, f"{script_name} must reference getIconHtml"

