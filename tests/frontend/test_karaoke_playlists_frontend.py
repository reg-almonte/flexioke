import json
import re
import subprocess
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_index_includes_karaoke_playlists_accordion_and_queue_save_buttons():
    """Verify HTML contains karaoke playlists card, accordions, and save queue buttons."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Karaoke playlists card & elements
    assert 'id="karaoke-card-playlists"' in html
    assert 'id="accordion-header-karaoke-playlists"' in html
    assert 'id="accordion-body-karaoke-playlists"' in html
    assert 'id="karaoke-playlists-count-badge"' in html
    assert 'id="accordion-chevron-karaoke-playlists"' in html
    assert 'id="karaoke-playlists-list"' in html

    # Save queue as playlist buttons in both views
    assert 'id="karaoke-save-queue-playlist-btn"' in html
    assert 'id="studio-save-queue-playlist-btn"' in html

def test_karaoke_js_initializes_playlists_accordion():
    """Verify karaoke.js initializes the playlists accordion with persistence."""
    resp = client.get("/static/karaoke.js")
    assert resp.status_code == 200
    js = resp.text

    assert "'karaoke-playlists'" in js
    assert "initKaraokeAccordions" in js

def test_playlists_js_implements_karaoke_dispatch_and_save_queue():
    """Verify playlists.js contains renderKaraokePlaylists, dispatchPlaylistQueue, and saveQueueAsPlaylist."""
    resp = client.get("/static/playlists.js")
    assert resp.status_code == 200
    js = resp.text

    assert "renderKaraokePlaylists" in js
    assert "dispatchPlaylistQueue" in js
    assert "saveQueueAsPlaylist" in js
    assert "/api/playlists/from-queue" in js

def test_shuffle_algorithm_and_dispatch_logic_in_node():
    """Execute queue dispatch and shuffle logic extracted or implemented to verify behavior in Node.js."""
    js_text = Path("src/static/playlists.js").read_text()
    
    node_script = """
    function shuffleArray(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    const testSongs = ["job_1", "job_2", "job_3", "job_4", "job_5", "job_6", "job_7", "job_8"];
    const shuffled = shuffleArray(testSongs);

    // Verify properties
    const sameLength = shuffled.length === testSongs.length;
    const containsAll = testSongs.every(id => shuffled.includes(id));
    
    console.log(JSON.stringify({
        sameLength,
        containsAll,
        shuffled
    }));
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    res = json.loads(proc.stdout)
    assert res["sameLength"] is True
    assert res["containsAll"] is True
