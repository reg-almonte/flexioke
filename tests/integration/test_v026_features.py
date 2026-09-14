import json
import re
import subprocess
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_lrc_timestamp_shifting_algorithm():
    """Execute shiftLrcTimestamps extracted from library_queue.js in Node.js to verify exact math and edge cases."""
    js_text = Path("src/static/library_queue.js").read_text()
    match = re.search(r'(shiftLrcTimestamps\(text,\s*deltaSeconds\)\s*\{[\s\S]*?\n    \})', js_text)
    assert match is not None, "shiftLrcTimestamps method definition not found in library_queue.js"
    shift_fn = f"function {match.group(1)}"

    node_script = f"""
    {shift_fn}

    const testLrc = `[ti: Test Song]
[ar: Test Artist]
[00:00.50] Intro line
[00:59.90] Bridge before minute turn
[01:02.123] 3-decimal token line
Raw line without timestamp`;

    // 1. Shift +0.1s
    const shiftedPos = shiftLrcTimestamps(testLrc, 0.1).text;
    // 2. Shift -1.0s (testing clamping on 00:00.50 -> 00:00.00)
    const shiftedNeg = shiftLrcTimestamps(testLrc, -1.0).text;
    // 3. Shift +0.2s (testing minute rollover on 00:59.90 -> 01:00.10)
    const shiftedMin = shiftLrcTimestamps(testLrc, 0.2).text;
    // 4. Zero shift
    const shiftedZero = shiftLrcTimestamps(testLrc, 0).text;

    console.log(JSON.stringify({{
        pos_shift: shiftedPos,
        neg_clamp: shiftedNeg,
        min_roll: shiftedMin,
        zero_shift: shiftedZero
    }}));
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    res = json.loads(proc.stdout)

    # Verify +0.1s
    assert "[ti: Test Song]" in res["pos_shift"]
    assert "[ar: Test Artist]" in res["pos_shift"]
    assert "[00:00.60] Intro line" in res["pos_shift"]
    assert "[01:00.00] Bridge before minute turn" in res["pos_shift"]
    assert "[01:02.22] 3-decimal token line" in res["pos_shift"]
    assert "Raw line without timestamp" in res["pos_shift"]

    # Verify clamping at 00:00.00 on negative shift
    assert "[00:00.00] Intro line" in res["neg_clamp"]
    assert "[00:58.90] Bridge before minute turn" in res["neg_clamp"]

    # Verify minute rollover
    assert "[01:00.10] Bridge before minute turn" in res["min_roll"]

    # Verify zero shift leaves timestamps identical
    assert "[00:00.50] Intro line" in res["zero_shift"]


def test_lyrics_calibration_toolbar_dom_elements():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Toolbar container
    assert 'id="lyrics-shift-alert"' in html
    assert 'id="lyrics-custom-shift-input"' in html
    assert 'id="lyrics-custom-shift-btn"' in html

    # Preset quick-shift buttons
    assert 'data-shift="-0.5"' in html
    assert 'data-shift="-0.1"' in html
    assert 'data-shift="0.1"' in html
    assert 'data-shift="0.5"' in html


def test_karaoke_sidebar_accordions_dom_and_attributes():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Queue accordion
    assert 'id="accordion-header-karaoke-queue"' in html
    assert 'id="accordion-body-karaoke-queue"' in html
    assert 'id="accordion-chevron-karaoke-queue"' in html
    assert 'role="button"' in html
    assert 'tabindex="0"' in html

    # Library accordion
    assert 'id="accordion-header-karaoke-library"' in html
    assert 'id="accordion-body-karaoke-library"' in html
    assert 'id="accordion-chevron-karaoke-library"' in html


def test_karaoke_smart_idle_play_dispatch_wiring():
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text
    assert "togglePlayPause" in js
    assert "window.flexiokeQueue" in js
    assert "window.flexiokeQueue.playNext" in js
    assert "openCatalogModal" in js
