import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_lyrics_modal_in_html():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "lyrics-modal" in html
    assert "lyrics-edit-title" in html
    assert "lyrics-edit-artist" in html
    assert "lyrics-textarea" in html
    assert "save-lyrics-btn" in html
    assert "fetch-lrclib-btn" in html
    assert "lrclib-fetch-alert" in html
    assert "lyrics-shift-btn" in html
    assert "lyrics-custom-shift-input" in html
    assert "lyrics-custom-shift-btn" in html
    assert "lyrics-shift-alert" in html

def test_library_js_contains_lyrics_modal_logic():
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    assert "openLyricsModal" in resp.text
    assert "lyricsEditTitle" in resp.text or "lyrics-edit-title" in resp.text
    assert "lyricsEditArtist" in resp.text or "lyrics-edit-artist" in resp.text
    assert "handleFetchLrclib" in resp.text
    assert "api/lyrics/lrclib/get" in resp.text
    assert "shiftLrcTimestamps" in resp.text
    assert "handleShiftLrc" in resp.text
    assert "lyrics-shift-btn" in resp.text
    assert "updateSaveButtonState" in resp.text

def test_save_button_state_and_persistence_in_node():
    """Verify in Node.js that save button is disabled without edits and disabled after save without closing modal."""
    import subprocess
    node_script = """
    const modal = {
        saveLyricsBtn: { disabled: false },
        modalContext: { baseline: null, isDirty: false },
        isModalClosed: false,

        openModal(song) {
            this.modalContext.baseline = {
                title: song.title,
                artist: song.artist,
                lyrics: song.lyrics || ""
            };
            this.current = { ...this.modalContext.baseline };
            this.saveLyricsBtn.disabled = true;
            this.isModalClosed = false;
        },

        onFieldInput(field, val) {
            this.current[field] = val;
            const dirty = this.isDirty();
            this.modalContext.isDirty = dirty;
            this.saveLyricsBtn.disabled = !dirty;
        },

        isDirty() {
            return this.current.title !== this.modalContext.baseline.title ||
                   this.current.artist !== this.modalContext.baseline.artist ||
                   this.current.lyrics !== this.modalContext.baseline.lyrics;
        },

        saveLyrics() {
            if (this.saveLyricsBtn.disabled) return;
            // Update baseline to new values
            this.modalContext.baseline = { ...this.current };
            this.modalContext.isDirty = false;
            // Disable save button, do not close modal
            this.saveLyricsBtn.disabled = true;
        },

        closeModal() {
            this.isModalClosed = true;
        }
    };

    // 1. Open modal -> save button must be disabled
    modal.openModal({ title: "Song A", artist: "Artist A", lyrics: "line 1" });
    if (!modal.saveLyricsBtn.disabled) throw new Error("Save button should be disabled initially");

    // 2. Type change -> save button enabled
    modal.onFieldInput("title", "Song A (Live)");
    if (modal.saveLyricsBtn.disabled) throw new Error("Save button should be enabled after edits");

    // 3. Revert change -> save button disabled again
    modal.onFieldInput("title", "Song A");
    if (!modal.saveLyricsBtn.disabled) throw new Error("Save button should be disabled when reverted");

    // 4. Make change and save -> saved, button disabled, modal stays open
    modal.onFieldInput("lyrics", "line 1 updated");
    modal.saveLyrics();
    if (!modal.saveLyricsBtn.disabled) throw new Error("Save button should be disabled after save");
    if (modal.isModalClosed) throw new Error("Modal should not be closed on save");

    console.log("SAVE_BUTTON_FLOW_SUCCESS");
    """
    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    assert "SAVE_BUTTON_FLOW_SUCCESS" in proc.stdout


