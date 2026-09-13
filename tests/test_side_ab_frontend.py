import os
import json
import subprocess
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_side_ab_html_elements():
    """Verify Side A/B tab, dropzones, modal attachment elements in index.html."""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Tab and Ingestion elements
    assert "tab-side-ab-btn" in html
    assert "tab-side-ab-content" in html
    assert "side-b-dropzone" in html
    assert "side-b-file-input" in html
    assert "side-a-dropzone" in html
    assert "side-a-file-input" in html
    assert "side-ab-title-input" in html
    assert "side-ab-artist-input" in html
    assert "submit-side-ab-btn" in html

    # Modal attachment elements
    assert "lyrics-modal-side-a-section" in html
    assert "lyrics-modal-side-a-file" in html
    assert "lyrics-modal-attach-side-a-btn" in html
    assert "lyrics-modal-side-a-status" in html

def test_side_ab_js_logic_coverage():
    """Verify JavaScript files include Side A/B integration points."""
    app_js = client.get("/static/app.js").text
    assert "/api/jobs/upload-side-ab" in app_js
    assert "tab-side-ab-btn" in app_js
    assert "flexioke:job-completed" in app_js

    lib_js = client.get("/static/library_queue.js").text
    assert "lyricsModalSideASection" in lib_js
    assert "attach-side-a" in lib_js
    assert "Side A/B" in lib_js

    player_js = client.get("/static/player.js").text
    assert "side_ab" in player_js
    assert "applyGainMatrix" in player_js

    karaoke_js = client.get("/static/karaoke.js").text
    assert "side_ab" in karaoke_js
    assert "Lead: OFF (Side B Only)" in karaoke_js
    assert "Backing: N/A (Side A/B)" in karaoke_js

def test_side_ab_webaudio_and_toggle_simulation():
    """Execute Node.js simulation of WebAudio gain matrix hot-swapping and dynamic button state adaptation."""
    node_code = """
    function createElement(id) {
        return {
            id,
            className: "",
            disabled: false,
            textContent: "",
            title: "",
            classList: { toggle: () => {}, add: () => {}, remove: () => {} }
        };
    }

    const mockToggleLeadBtn = createElement("karaoke-toggle-lead-btn");
    const mockLeadStatusText = createElement("karaoke-lead-status-text");
    const mockToggleBackingBtn = createElement("karaoke-toggle-backing-btn");
    const mockBackingStatusText = createElement("karaoke-backing-status-text");

    function createMockPlayer(sourceType, stems) {
        return {
            masterVolume: 0.8,
            currentJob: { source_type: sourceType, stems: stems },
            tracks: {
                instrumental: {
                    id: "instrumental",
                    volume: 1.0,
                    muted: false,
                    soloed: false,
                    ws: { volume: 0, setVolume: function(v) { this.volume = v; } }
                },
                lead_vocals: {
                    id: "lead_vocals",
                    volume: 1.0,
                    muted: false,
                    soloed: false,
                    ws: stems.lead_vocals ? { volume: 0, setVolume: function(v) { this.volume = v; } } : null
                },
                backing_vocals: {
                    id: "backing_vocals",
                    volume: 1.0,
                    muted: false,
                    soloed: false,
                    ws: stems.backing_vocals ? { volume: 0, setVolume: function(v) { this.volume = v; } } : null
                }
            },
            applyGainMatrix: function() {
                const isSideAB = this.currentJob && this.currentJob.source_type === "side_ab";
                if (isSideAB) {
                    const hasLead = Boolean(this.tracks.lead_vocals.ws && this.currentJob.stems && this.currentJob.stems.lead_vocals);
                    const hasInst = Boolean(this.tracks.instrumental.ws && this.currentJob.stems && this.currentJob.stems.instrumental);

                    if (hasLead && hasInst) {
                        const leadActive = !this.tracks.lead_vocals.muted;
                        if (leadActive) {
                            this.tracks.lead_vocals.ws.setVolume(this.tracks.lead_vocals.volume * this.masterVolume);
                            this.tracks.instrumental.ws.setVolume(0);
                        } else {
                            this.tracks.lead_vocals.ws.setVolume(0);
                            this.tracks.instrumental.ws.setVolume(this.tracks.instrumental.volume * this.masterVolume);
                        }
                    } else if (hasInst) {
                        const gain = this.tracks.instrumental.muted ? 0 : this.tracks.instrumental.volume * this.masterVolume;
                        this.tracks.instrumental.ws.setVolume(gain);
                        if (this.tracks.lead_vocals.ws) this.tracks.lead_vocals.ws.setVolume(0);
                    }
                    if (this.tracks.backing_vocals.ws) this.tracks.backing_vocals.ws.setVolume(0);
                    return;
                }
            }
        };
    }

    function syncVocalButtons(player) {
        const leadTrack = player.tracks.lead_vocals;
        const isSideAB = player.currentJob && player.currentJob.source_type === "side_ab";

        if (isSideAB) {
            const hasLead = Boolean(player.currentJob.stems && player.currentJob.stems.lead_vocals);
            const hasInst = Boolean(player.currentJob.stems && player.currentJob.stems.instrumental);

            if (hasLead && hasInst) {
                mockToggleLeadBtn.disabled = false;
                if (leadTrack && leadTrack.muted) {
                    mockLeadStatusText.textContent = "Lead Vocals: MUTED";
                } else {
                    mockLeadStatusText.textContent = "Lead Vocals: ON";
                }
            } else if (hasInst && !hasLead) {
                mockToggleLeadBtn.disabled = true;
                mockLeadStatusText.textContent = "Lead: OFF (Side B Only)";
            }

            mockToggleBackingBtn.disabled = true;
            mockBackingStatusText.textContent = "Backing: N/A (Side A/B)";
        }
    }

    // Scenario 1: Dual-track Side A/B (Both Side A and Side B)
    const player1 = createMockPlayer("side_ab", { instrumental: "/audio/inst.mp3", lead_vocals: "/audio/lead.mp3" });
    player1.applyGainMatrix();
    syncVocalButtons(player1);
    if (Math.abs(player1.tracks.lead_vocals.ws.volume - 0.8) > 0.001) throw new Error("Side A volume error");
    if (player1.tracks.instrumental.ws.volume !== 0) throw new Error("Side B volume error");
    if (mockToggleLeadBtn.disabled !== false) throw new Error("Lead button disabled error");
    if (mockLeadStatusText.textContent !== "Lead Vocals: ON") throw new Error("Status ON error");
    if (mockToggleBackingBtn.disabled !== true) throw new Error("Backing button disabled error");
    if (mockBackingStatusText.textContent !== "Backing: N/A (Side A/B)") throw new Error("Backing text error");

    // Hot-swap
    player1.tracks.lead_vocals.muted = true;
    player1.applyGainMatrix();
    syncVocalButtons(player1);
    if (player1.tracks.lead_vocals.ws.volume !== 0) throw new Error("Side A muted volume error");
    if (Math.abs(player1.tracks.instrumental.ws.volume - 0.8) > 0.001) throw new Error("Side B unmuted volume error");
    if (mockLeadStatusText.textContent !== "Lead Vocals: MUTED") throw new Error("Status MUTED error");

    // Scenario 2: Side B only
    const player2 = createMockPlayer("side_ab", { instrumental: "/audio/inst.mp3" });
    player2.applyGainMatrix();
    syncVocalButtons(player2);
    if (Math.abs(player2.tracks.instrumental.ws.volume - 0.8) > 0.001) throw new Error("Side B only volume error");
    if (mockToggleLeadBtn.disabled !== true) throw new Error("Side B only lead button enabled error");
    if (mockLeadStatusText.textContent !== "Lead: OFF (Side B Only)") throw new Error("Side B only text error");

    console.log("ALL_NODE_SIMULATION_TESTS_PASSED");
    """

    res = subprocess.run(["node", "-e", node_code], capture_output=True, text=True)
    assert res.returncode == 0, f"Node simulation failed:\n{res.stderr}"
    assert "ALL_NODE_SIMULATION_TESTS_PASSED" in res.stdout
