/**
 * Flexioke — Karaoke Synchronized Stage & LRC Engine
 */
class LrcParser {
    static parse(lrcText) {
        if (!lrcText || typeof lrcText !== 'string') {
            return { lines: [], hasTimestamps: false, raw: "" };
        }

        const rawLines = lrcText.split(/\r?\n/);
        const parsedLines = [];
        const timestampRegex = /\[(\d{1,2}):(\d{1,2}(?:\.\d{1,3})?)\](.*)/;

        rawLines.forEach(line => {
            const match = line.match(timestampRegex);
            if (match) {
                const mins = parseInt(match[1], 10);
                const secs = parseFloat(match[2]);
                const time = mins * 60 + secs;
                const text = match[3].trim();
                parsedLines.push({ time, text });
            }
        });

        if (parsedLines.length > 0) {
            parsedLines.sort((a, b) => a.time - b.time);
            return {
                lines: parsedLines,
                hasTimestamps: true,
                raw: lrcText
            };
        }

        // Fallback to plain text
        const plainLines = rawLines.map(l => l.trim()).filter(l => l.length > 0);
        return {
            lines: plainLines.map(text => ({ time: null, text })),
            hasTimestamps: false,
            raw: lrcText
        };
    }
}

class KaraokeStageManager {
    constructor() {
        this.stageContainer = document.getElementById('karaoke-lyrics-stage');
        this.songTitleEl = document.getElementById('karaoke-song-title');
        this.timecodeEl = document.getElementById('karaoke-timecode');

        // Karaoke Transport Elements
        this.playBtn = document.getElementById('karaoke-play-btn');
        this.skipBtn = document.getElementById('karaoke-skip-btn');
        this.toggleLeadBtn = document.getElementById('karaoke-toggle-lead-btn');
        this.leadStatusText = document.getElementById('karaoke-lead-status-text');
        this.toggleBackingBtn = document.getElementById('karaoke-toggle-backing-btn');
        this.backingStatusText = document.getElementById('karaoke-backing-status-text');
        this.volumeSlider = document.getElementById('karaoke-volume-slider');

        this.currentJobId = null;
        this.lyricsData = null;
        this.activeLineIndex = -1;
        this.lineElements = [];

        this.init();
    }

    init() {
        // Bind Karaoke Transport Controls
        if (this.playBtn) {
            this.playBtn.addEventListener('click', () => {
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.togglePlay();
                    this.updatePlayBtnUI();
                }
            });
        }

        if (this.skipBtn) {
            this.skipBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.advanceNext();
                }
            });
        }

        if (this.volumeSlider) {
            this.volumeSlider.addEventListener('input', (e) => {
                const val = parseFloat(e.target.value);
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.masterVolume = val;
                    window.flexiokePlayer.applyGainMatrix();
                }
                const masterSlider = document.getElementById('master-volume-slider');
                if (masterSlider) masterSlider.value = val;
            });
        }

        // Quick Vocal Toggles
        if (this.toggleLeadBtn) {
            this.toggleLeadBtn.addEventListener('click', () => {
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.toggleMute('lead_vocals');
                    this.syncVocalButtons();
                }
            });
        }

        if (this.toggleBackingBtn) {
            this.toggleBackingBtn.addEventListener('click', () => {
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.toggleMute('backing_vocals');
                    this.syncVocalButtons();
                }
            });
        }

        // Listen for lyrics updates from editor
        window.addEventListener('flexioke:lyrics-updated', (e) => {
            if (e.detail && e.detail.job_id === this.currentJobId) {
                this.loadLyricsForJob(this.currentJobId);
            }
        });

        // Hook into FlexiokePlayer loadSong
        const originalLoadSong = window.flexiokePlayer ? window.flexiokePlayer.loadSong.bind(window.flexiokePlayer) : null;
        if (window.flexiokePlayer && originalLoadSong) {
            window.flexiokePlayer.loadSong = (job, autoPlay = false) => {
                originalLoadSong(job, autoPlay);
                if (job) {
                    this.onSongLoaded(job);
                }
            };
        }

        // Time & Transport state check
        setInterval(() => this.onTimeCheck(), 100);
    }

    onSongLoaded(job) {
        this.currentJobId = job.job_id;
        if (this.songTitleEl) {
            this.songTitleEl.textContent = job.title || "Untitled Song";
        }
        this.syncVocalButtons();
        this.loadLyricsForJob(job.job_id);
    }

    syncVocalButtons() {
        if (!window.flexiokePlayer) return;
        const leadTrack = window.flexiokePlayer.tracks.lead_vocals;
        const backingTrack = window.flexiokePlayer.tracks.backing_vocals;

        if (this.toggleLeadBtn && this.leadStatusText && leadTrack) {
            if (leadTrack.muted) {
                this.toggleLeadBtn.className = "px-3.5 py-1.5 rounded-xl bg-rose-600/30 border border-rose-500/50 text-rose-300 text-xs font-semibold transition flex items-center gap-1.5";
                this.leadStatusText.textContent = "Lead Vocals: MUTED";
            } else {
                this.toggleLeadBtn.className = "px-3.5 py-1.5 rounded-xl bg-brand-600/30 border border-brand-500/50 text-brand-300 text-xs font-semibold transition flex items-center gap-1.5";
                this.leadStatusText.textContent = "Lead Vocals: ON";
            }
        }

        if (this.toggleBackingBtn && this.backingStatusText && backingTrack) {
            if (backingTrack.muted) {
                this.toggleBackingBtn.className = "px-3.5 py-1.5 rounded-xl bg-rose-600/30 border border-rose-500/50 text-rose-300 text-xs font-semibold transition flex items-center gap-1.5";
                this.backingStatusText.textContent = "Backing: MUTED";
            } else {
                this.toggleBackingBtn.className = "px-3.5 py-1.5 rounded-xl bg-violet-600/30 border border-violet-500/50 text-violet-300 text-xs font-semibold transition flex items-center gap-1.5";
                this.backingStatusText.textContent = "Backing: ON";
            }
        }
    }

    updatePlayBtnUI() {
        if (!this.playBtn || !window.flexiokePlayer) return;
        this.playBtn.innerHTML = window.flexiokePlayer.isPlaying ? '⏸' : '▶';
    }

    async loadLyricsForJob(jobId) {
        if (!jobId) return;
        this.activeLineIndex = -1;

        try {
            const resp = await fetch(`/api/jobs/${jobId}/lyrics`);
            if (resp.ok) {
                const data = await resp.json();
                this.lyricsData = LrcParser.parse(data.lyrics || "");
                this.renderStage();
            } else {
                this.renderEmptyState();
            }
        } catch (err) {
            console.error("Error loading karaoke lyrics:", err);
            this.renderEmptyState();
        }
    }

    renderStage() {
        if (!this.stageContainer) return;
        this.stageContainer.innerHTML = '';
        this.lineElements = [];

        if (!this.lyricsData || this.lyricsData.lines.length === 0) {
            this.renderEmptyState();
            return;
        }

        // If plain text (no timestamps)
        if (!this.lyricsData.hasTimestamps) {
            const wrapper = document.createElement('div');
            wrapper.className = "space-y-3 py-6 text-slate-300 text-sm leading-relaxed max-w-md mx-auto";
            this.lyricsData.lines.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line.text;
                wrapper.appendChild(p);
            });
            this.stageContainer.appendChild(wrapper);
            return;
        }

        // Timestamped LRC mode
        const wrapper = document.createElement('div');
        wrapper.className = "space-y-5 py-24 max-w-xl mx-auto w-full transition-all";

        this.lyricsData.lines.forEach((line, index) => {
            const lineEl = document.createElement('div');
            lineEl.className = "karaoke-line text-slate-500 font-semibold text-base sm:text-lg transition-all duration-300 py-1.5 cursor-pointer hover:text-slate-300";
            lineEl.textContent = line.text || "♪ ♪ ♪";
            lineEl.dataset.index = index;

            // Click to seek to line
            lineEl.addEventListener('click', () => {
                if (window.flexiokePlayer && line.time !== null) {
                    window.flexiokePlayer.syncSeek(line.time, 'none');
                    const primary = Object.values(window.flexiokePlayer.tracks).find(t => t.ws && t.isReady);
                    if (primary) {
                        primary.ws.setTime(line.time);
                    }
                }
            });

            wrapper.appendChild(lineEl);
            this.lineElements.push(lineEl);
        });

        this.stageContainer.appendChild(wrapper);
    }

    renderEmptyState() {
        if (!this.stageContainer) return;
        this.stageContainer.innerHTML = `
            <div class="text-center py-16 space-y-2">
                <span class="text-3xl">🎤</span>
                <p class="text-slate-400 text-sm font-medium">No lyrics added yet for this song</p>
                <p class="text-slate-500 text-xs">Click the "📝" button on the song card in the library to add timestamped lyrics!</p>
            </div>
        `;
    }

    onTimeCheck() {
        if (!window.flexiokePlayer) return;

        this.updatePlayBtnUI();

        if (!this.lyricsData || !this.lyricsData.hasTimestamps) {
            return;
        }

        // Get current timestamp
        let currentTime = 0;
        const firstReady = Object.values(window.flexiokePlayer.tracks).find(t => t.ws && t.isReady);
        if (firstReady) {
            currentTime = firstReady.ws.getCurrentTime();
            if (this.timecodeEl) {
                const dur = window.flexiokePlayer.duration || firstReady.ws.getDuration();
                const fmt = (s) => {
                    const m = Math.floor(s / 60);
                    const sc = Math.floor(s % 60);
                    return `${String(m).padStart(2, '0')}:${String(sc).padStart(2, '0')}`;
                };
                this.timecodeEl.textContent = `${fmt(currentTime)} / ${fmt(dur || 0)}`;
            }
        }

        // Find active line
        let newIndex = -1;
        for (let i = 0; i < this.lyricsData.lines.length; i++) {
            if (this.lyricsData.lines[i].time <= currentTime) {
                newIndex = i;
            } else {
                break;
            }
        }

        if (newIndex !== this.activeLineIndex && newIndex >= 0) {
            this.highlightLine(newIndex);
        }
    }

    highlightLine(index) {
        if (this.activeLineIndex >= 0 && this.lineElements[this.activeLineIndex]) {
            this.lineElements[this.activeLineIndex].className = "karaoke-line text-slate-500 font-semibold text-base sm:text-lg transition-all duration-300 py-1.5 cursor-pointer hover:text-slate-300";
        }

        this.activeLineIndex = index;
        const activeEl = this.lineElements[index];
        if (activeEl) {
            activeEl.className = "karaoke-line text-xl sm:text-2xl font-black text-white scale-110 drop-shadow-[0_0_15px_rgba(99,102,241,0.6)] py-2 transition-all duration-300 cursor-pointer bg-gradient-to-r from-brand-400 to-violet-400 bg-clip-text text-transparent";
            activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.flexiokeKaraoke = new KaraokeStageManager();
});
