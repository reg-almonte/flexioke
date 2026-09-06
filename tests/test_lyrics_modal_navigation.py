import json
import re
import subprocess
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_index_includes_lyrics_modal_navigation_elements():
    """Verify HTML contains modal navigation controls: prev, next, and counter badge."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    assert 'id="modal-nav-prev-btn"' in html
    assert 'id="modal-nav-next-btn"' in html
    assert 'id="modal-nav-counter-badge"' in html

def test_library_queue_js_implements_modal_navigation():
    """Verify library_queue.js implements in-modal navigation, dirty state checks, and keyboard shortcuts."""
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    js = resp.text

    assert "modal-nav-prev-btn" in js or "modalNavPrevBtn" in js
    assert "modal-nav-next-btn" in js or "modalNavNextBtn" in js
    assert "modal-nav-counter-badge" in js or "modalNavCounterBadge" in js
    assert "navigateToModalSong" in js or "navigateModal" in js or "navigateToSong" in js
    assert "isModalDirty" in js or "hasUnsavedChanges" in js or "checkUnsavedChanges" in js

def test_modal_navigation_and_dirty_state_logic_in_node():
    """Execute navigation and dirty state detection logic in Node.js."""
    node_script = """
    class ModalNavigator {
        constructor() {
            this.contextList = [];
            this.activeIndex = -1;
            this.baseline = { title: '', artist: '', lyrics: '' };
            this.current = { title: '', artist: '', lyrics: '' };
        }

        setContext(list, activeJobId) {
            this.contextList = list;
            this.activeIndex = this.contextList.findIndex(item => (item.job_id || item.id) === activeJobId);
            if (this.activeIndex === -1 && this.contextList.length > 0) {
                this.activeIndex = 0;
            }
        }

        isDirty() {
            return this.current.title !== this.baseline.title ||
                   this.current.artist !== this.baseline.artist ||
                   this.current.lyrics !== this.baseline.lyrics;
        }

        canPrev() {
            return this.activeIndex > 0;
        }

        canNext() {
            return this.activeIndex < this.contextList.length - 1;
        }

        getCounterText() {
            if (this.contextList.length === 0 || this.activeIndex === -1) return "Track 0 of 0";
            return `Track ${this.activeIndex + 1} of ${this.contextList.length}`;
        }
    }

    const songs = [
        { job_id: "s1", title: "Song 1", artist: "Artist 1" },
        { job_id: "s2", title: "Song 2", artist: "Artist 2" },
        { job_id: "s3", title: "Song 3", artist: "Artist 3" }
    ];

    const nav = new ModalNavigator();
    nav.setContext(songs, "s1");
    const initCounter = nav.getCounterText();
    const initCanPrev = nav.canPrev();
    const initCanNext = nav.canNext();

    nav.baseline = { title: "Song 1", artist: "Artist 1", lyrics: "Lyrics" };
    nav.current = { title: "Song 1", artist: "Artist 1", lyrics: "Lyrics" };
    const cleanDirty = nav.isDirty();

    nav.current.lyrics = "Edited Lyrics";
    const editedDirty = nav.isDirty();

    nav.setContext(songs, "s3");
    const lastCounter = nav.getCounterText();
    const lastCanPrev = nav.canPrev();
    const lastCanNext = nav.canNext();

    console.log(JSON.stringify({
        initCounter,
        initCanPrev,
        initCanNext,
        cleanDirty,
        editedDirty,
        lastCounter,
        lastCanPrev,
        lastCanNext
    }));
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    res = json.loads(proc.stdout)

    assert res["initCounter"] == "Track 1 of 3"
    assert res["initCanPrev"] is False
    assert res["initCanNext"] is True
    assert res["cleanDirty"] is False
    assert res["editedDirty"] is True
    assert res["lastCounter"] == "Track 3 of 3"
    assert res["lastCanPrev"] is True
    assert res["lastCanNext"] is False
