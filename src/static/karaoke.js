/**
 * Flexioke — Karaoke Synchronized Stage & LRC Engine (Overhauled with Fullscreen & Auto-Scroll Reset)
 */
class LrcParser {
    static parse(lrcText) {
        if (!lrcText || typeof lrcText !== 'string') {
            return { lines: [], hasTimestamps: false, raw: "" };
        }

        const rawLines = lrcText.split(/\r?\n/);
        const parsedLines = [];
        const timestampRegex = /\[(\d{1,2}):(\d{1,2}(?:\.\d{1,3})?)\]/g;

        rawLines.forEach(line => {
            const trimmed = line.trim();
            if (!trimmed) return;

            // Find all timestamp tags on this line
            const matches = [...trimmed.matchAll(timestampRegex)];
            if (matches.length > 0) {
                // Extract lyric text after removing all [mm:ss.xx] tags
                let text = trimmed.replace(timestampRegex, '').trim();
                if (!text) {
                    text = "♪ ♪ ♪ (Instrumental)";
                }

                matches.forEach(m => {
                    const mins = parseInt(m[1], 10);
                    const secs = parseFloat(m[2]);
                    const time = mins * 60 + secs;
                    parsedLines.push({ time, text });
                });
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
        this.stageCard = document.getElementById('karaoke-stage-card');
        this.headerBanner = document.getElementById('karaoke-header-banner');
        this.bannerLabel = document.getElementById('karaoke-banner-label');
        this.songTitleEl = document.getElementById('karaoke-song-title');
        this.songArtistEl = document.getElementById('karaoke-song-artist');
        this.timecodeEl = document.getElementById('karaoke-timecode');

        // Countdown cue elements
        this.countdownCue = document.getElementById('karaoke-countdown-cue');
        this.countdownDots = document.getElementById('countdown-dots');
        this.countdownNumber = document.getElementById('countdown-number');

        // Stage Toolbar Controls
        this.fontDecBtn = document.getElementById('karaoke-font-dec-btn');
        this.fontIncBtn = document.getElementById('karaoke-font-inc-btn');
        this.settingsBtn = document.getElementById('karaoke-settings-btn');

        // Stage Settings Modal Elements
        this.settingsModal = document.getElementById('karaoke-settings-modal');
        this.closeSettingsModalBtn = document.getElementById('close-settings-modal-btn');
        this.saveSettingsBtn = document.getElementById('save-settings-btn');
        this.resetSettingsBtn = document.getElementById('settings-reset-btn');
        this.settingIntervalInput = document.getElementById('settings-transition-interval');
        this.settingIntervalDisplay = document.getElementById('settings-interval-display');
        this.settingColorInput = document.getElementById('settings-highlight-color');
        this.settingColorDisplay = document.getElementById('settings-color-display');
        this.settingFontSizeInput = document.getElementById('settings-font-size');
        this.settingFontSizeDisplay = document.getElementById('settings-font-size-display');

        // Default Config & State
        this.defaultConfig = {
            headerTransitionInterval: 6,
            activeHighlightColor: '#06b6d4',
            baseFontSizePx: 20
        };
        this.config = { ...this.defaultConfig };

        // Fullscreen elements
        this.fullscreenBtn = document.getElementById('karaoke-fullscreen-btn');
        this.fullscreenIcon = document.getElementById('fullscreen-icon');
        this.fullscreenBtnText = document.getElementById('fullscreen-btn-text');
        this.isFullscreen = false;

        // Karaoke Transport Elements
        this.playBtn = document.getElementById('karaoke-play-btn');
        this.skipBtn = document.getElementById('karaoke-skip-btn');
        this.stopBtn = document.getElementById('karaoke-stop-btn');
        this.toggleLeadBtn = document.getElementById('karaoke-toggle-lead-btn');
        this.leadStatusText = document.getElementById('karaoke-lead-status-text');
        this.toggleBackingBtn = document.getElementById('karaoke-toggle-backing-btn');
        this.backingStatusText = document.getElementById('karaoke-backing-status-text');
        this.volumeSlider = document.getElementById('karaoke-volume-slider');

        this.currentJob = null;
        this.currentJobId = null;
        this.lyricsData = null;
        this.activeLineIndex = -1;
        this.lineElements = [];

        // Alternating Header Banner state
        this.bannerState = 'now_singing'; // 'now_singing' | 'up_next'
        this.bannerIntervalTimer = null;
        this.headerTransitionInterval = 6000;

        this.loadSettings();
        this.init();
    }

    init() {
        // Stage Toolbar Resizing (A- / A+)
        if (this.fontDecBtn) {
            this.fontDecBtn.addEventListener('click', () => this.adjustFontSize(-2));
        }
        if (this.fontIncBtn) {
            this.fontIncBtn.addEventListener('click', () => this.adjustFontSize(2));
        }

        // Settings Modal Bindings
        if (this.settingsBtn) {
            this.settingsBtn.addEventListener('click', () => this.openSettingsModal());
        }
        if (this.closeSettingsModalBtn) {
            this.closeSettingsModalBtn.addEventListener('click', () => this.closeSettingsModal());
        }
        if (this.saveSettingsBtn) {
            this.saveSettingsBtn.addEventListener('click', () => this.closeSettingsModal());
        }
        if (this.resetSettingsBtn) {
            this.resetSettingsBtn.addEventListener('click', () => {
                this.saveSettings(this.defaultConfig);
            });
        }

        // Real-time Settings Input Handlers
        if (this.settingIntervalInput) {
            this.settingIntervalInput.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10) || 6;
                if (this.settingIntervalDisplay) this.settingIntervalDisplay.textContent = `${val}s`;
                this.saveSettings({ headerTransitionInterval: val });
            });
        }
        if (this.settingColorInput) {
            this.settingColorInput.addEventListener('input', (e) => {
                const val = e.target.value;
                if (this.settingColorDisplay) this.settingColorDisplay.textContent = val;
                this.saveSettings({ activeHighlightColor: val });
            });
        }
        if (this.settingFontSizeInput) {
            this.settingFontSizeInput.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10) || 20;
                if (this.settingFontSizeDisplay) this.settingFontSizeDisplay.textContent = `${val}px`;
                this.saveSettings({ baseFontSizePx: val });
            });
        }

        // Fullscreen Toggle
        if (this.fullscreenBtn) {
            this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isFullscreen) {
                this.exitFullscreen();
            }
        });

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
                    window.flexiokeQueue.advanceNext(true);
                }
            });
        }

        if (this.stopBtn) {
            this.stopBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.stopAndCueNext();
                } else if (window.flexiokePlayer) {
                    window.flexiokePlayer.resetToDefault();
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

        // Listen for metadata updates from editor
        window.addEventListener('flexioke:metadata-updated', (e) => {
            if (e.detail && this.currentJob && e.detail.job_id === this.currentJob.job_id) {
                this.currentJob = e.detail;
                if (this.bannerState === 'now_singing') {
                    if (this.songTitleEl) this.songTitleEl.textContent = this.currentJob.title || "Untitled Song";
                    if (this.songArtistEl) this.songArtistEl.textContent = this.currentJob.artist || "Unknown Artist";
                }
            }
        });

        // Listen for queue updates to dynamically start or reset alternating banner
        window.addEventListener('flexioke:queue-updated', (e) => {
            const queue = (e.detail && e.detail.queue) ? e.detail.queue : [];
            if (queue.length === 0 && this.bannerState === 'up_next') {
                this.setBannerContent('now_singing');
            } else if (queue.length > 0 && this.currentJob && !this.bannerIntervalTimer) {
                this.startAlternatingBannerCycle();
            }
        });

        // Listen for player reset (when queue finishes or stop clicked without queue)
        window.addEventListener('flexioke:player-reset', () => {
            this.currentJob = null;
            this.currentJobId = null;
            this.lyricsData = null;
            this.activeLineIndex = -1;
            this.stopAlternatingBannerCycle();
            if (this.bannerLabel) {
                this.bannerLabel.textContent = "Now Singing";
                this.bannerLabel.className = "text-[10px] uppercase font-bold tracking-widest text-brand-400";
            }
            if (this.songTitleEl) {
                this.songTitleEl.textContent = "No Track Selected";
            }
            if (this.songArtistEl) {
                this.songArtistEl.textContent = "";
            }
            if (this.timecodeEl) {
                this.timecodeEl.textContent = "00:00 / 00:00 (-00:00)";
            }
            this.renderDefaultState();
            this.updatePlayBtnUI();
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

    loadSettings() {
        try {
            const raw = localStorage.getItem('flexioke_stage_config');
            if (raw) {
                const parsed = JSON.parse(raw);
                this.config = { ...this.defaultConfig, ...parsed };
            }
        } catch (err) {
            console.error("Error loading stage settings:", err);
            this.config = { ...this.defaultConfig };
        }
        this.applySettings();
    }

    applySettings() {
        this.headerTransitionInterval = (this.config.headerTransitionInterval || 6) * 1000;

        const basePx = this.config.baseFontSizePx || 20;
        const activePx = Math.round(basePx * 1.35);
        const color = this.config.activeHighlightColor || '#06b6d4';

        document.documentElement.style.setProperty('--karaoke-font-size', `${basePx}px`);
        document.documentElement.style.setProperty('--karaoke-active-font-size', `${activePx}px`);
        document.documentElement.style.setProperty('--karaoke-highlight-color', color);

        if (this.settingIntervalInput) this.settingIntervalInput.value = this.config.headerTransitionInterval;
        if (this.settingIntervalDisplay) this.settingIntervalDisplay.textContent = `${this.config.headerTransitionInterval}s`;
        if (this.settingColorInput) this.settingColorInput.value = color;
        if (this.settingColorDisplay) this.settingColorDisplay.textContent = color;
        if (this.settingFontSizeInput) this.settingFontSizeInput.value = basePx;
        if (this.settingFontSizeDisplay) this.settingFontSizeDisplay.textContent = `${basePx}px`;

        if (this.lineElements && this.lineElements.length > 0) {
            this.lineElements.forEach((el, idx) => {
                if (idx !== this.activeLineIndex) {
                    el.style.fontSize = `var(--karaoke-font-size, ${basePx}px)`;
                }
            });
        }

        if (this.activeLineIndex >= 0) {
            this.highlightLine(this.activeLineIndex);
        }

        // Dynamically restart alternating cycle with updated interval
        if (this.currentJob) {
            const queue = (window.flexiokeQueue && window.flexiokeQueue.queue) ? window.flexiokeQueue.queue : [];
            if (queue.length > 0) {
                this.startAlternatingBannerCycle();
            }
        }
    }

    saveSettings(newConfig) {
        this.config = { ...this.config, ...newConfig };
        try {
            localStorage.setItem('flexioke_stage_config', JSON.stringify(this.config));
        } catch (err) {
            console.error("Error persisting stage settings:", err);
        }
        this.applySettings();
    }

    adjustFontSize(delta) {
        let newSize = (this.config.baseFontSizePx || 20) + delta;
        newSize = Math.max(14, Math.min(36, newSize));
        this.saveSettings({ baseFontSizePx: newSize });
    }

    openSettingsModal() {
        if (this.settingsModal) {
            this.applySettings();
            this.settingsModal.classList.remove('hidden');
        }
    }

    closeSettingsModal() {
        if (this.settingsModal) {
            this.settingsModal.classList.add('hidden');
        }
    }

    startAlternatingBannerCycle() {
        if (this.bannerIntervalTimer) {
            clearInterval(this.bannerIntervalTimer);
            this.bannerIntervalTimer = null;
        }

        const intervalSec = this.config.headerTransitionInterval || 6;
        this.headerTransitionInterval = intervalSec * 1000;

        this.bannerIntervalTimer = setInterval(() => {
            this.toggleAlternatingBanner();
        }, this.headerTransitionInterval);
    }

    stopAlternatingBannerCycle() {
        if (this.bannerIntervalTimer) {
            clearInterval(this.bannerIntervalTimer);
            this.bannerIntervalTimer = null;
        }
        this.setBannerContent('now_singing');
    }

    toggleAlternatingBanner() {
        const queue = (window.flexiokeQueue && window.flexiokeQueue.queue) ? window.flexiokeQueue.queue : [];
        const nextTrack = queue.length > 0 ? queue[0] : null;

        if (!nextTrack || !this.currentJob) {
            if (this.bannerState !== 'now_singing') {
                this.setBannerContent('now_singing');
            }
            return;
        }

        const targetState = (this.bannerState === 'now_singing') ? 'up_next' : 'now_singing';
        this.setBannerContent(targetState, nextTrack);
    }

    setBannerContent(state, nextTrack = null) {
        this.bannerState = state;
        if (!this.headerBanner) return;

        this.headerBanner.classList.add('opacity-0');
        setTimeout(() => {
            if (state === 'up_next' && nextTrack) {
                if (this.bannerLabel) {
                    this.bannerLabel.textContent = "Up Next";
                    this.bannerLabel.className = "text-[10px] uppercase font-bold tracking-widest text-violet-400";
                }
                if (this.songTitleEl) {
                    this.songTitleEl.textContent = nextTrack.title || "Untitled Song";
                }
                if (this.songArtistEl) {
                    this.songArtistEl.textContent = nextTrack.artist || "Unknown Artist";
                }
            } else {
                if (this.bannerLabel) {
                    this.bannerLabel.textContent = "Now Singing";
                    this.bannerLabel.className = "text-[10px] uppercase font-bold tracking-widest text-brand-400";
                }
                if (this.songTitleEl) {
                    this.songTitleEl.textContent = this.currentJob ? (this.currentJob.title || "Untitled Song") : "No Track Selected";
                }
                if (this.songArtistEl) {
                    this.songArtistEl.textContent = this.currentJob ? (this.currentJob.artist || "Unknown Artist") : "";
                }
            }
            this.headerBanner.classList.remove('opacity-0');
        }, 250);
    }

    toggleFullscreen() {
        if (this.isFullscreen) {
            this.exitFullscreen();
        } else {
            this.enterFullscreen();
        }
    }

    enterFullscreen() {
        this.isFullscreen = true;
        if (this.stageCard) {
            this.stageCard.classList.add('stage-fullscreen');
        }
        if (this.fullscreenIcon) this.fullscreenIcon.textContent = '🗗';
        if (this.fullscreenBtnText) this.fullscreenBtnText.textContent = 'Collapse';
        if (this.fullscreenBtn) this.fullscreenBtn.title = "Exit Fullscreen Stage (Esc)";
    }

    exitFullscreen() {
        this.isFullscreen = false;
        if (this.stageCard) {
            this.stageCard.classList.remove('stage-fullscreen');
        }
        if (this.fullscreenIcon) this.fullscreenIcon.textContent = '⛶';
        if (this.fullscreenBtnText) this.fullscreenBtnText.textContent = 'Expand';
        if (this.fullscreenBtn) this.fullscreenBtn.title = "Toggle Fullscreen Stage";
    }

    onSongLoaded(job) {
        this.currentJob = job;
        this.currentJobId = job.job_id;
        this.setBannerContent('now_singing');
        this.startAlternatingBannerCycle();
        if (this.stageContainer) {
            this.stageContainer.scrollTop = 0;
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
        if (!jobId) {
            this.renderDefaultState();
            return;
        }
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
        this.stageContainer.scrollTop = 0;
        this.lineElements = [];

        if (!this.currentJobId) {
            this.renderDefaultState();
            return;
        }

        if (!this.lyricsData || this.lyricsData.lines.length === 0) {
            this.renderEmptyState();
            return;
        }

        // If plain text (no timestamps)
        if (!this.lyricsData.hasTimestamps) {
            const wrapper = document.createElement('div');
            wrapper.className = "space-y-3 py-6 text-slate-200 text-base sm:text-lg leading-relaxed max-w-lg mx-auto text-center";
            this.lyricsData.lines.forEach(line => {
                const p = document.createElement('p');
                p.className = "py-1";
                p.textContent = line.text;
                wrapper.appendChild(p);
            });
            this.stageContainer.appendChild(wrapper);
            return;
        }

        // Timestamped LRC mode
        const wrapper = document.createElement('div');
        wrapper.className = "space-y-4 py-32 max-w-3xl mx-auto w-full text-center";

        this.lyricsData.lines.forEach((line, index) => {
            const lineEl = document.createElement('div');
            lineEl.className = "karaoke-line text-slate-400 font-semibold transition-all duration-300 py-2.5 px-4 rounded-xl cursor-pointer hover:text-white hover:bg-slate-800/40";
            lineEl.style.fontSize = "var(--karaoke-font-size, 20px)";
            lineEl.textContent = line.text;
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
        this.stageContainer.scrollTop = 0;
    }

    renderDefaultState() {
        if (!this.stageContainer) return;
        this.stageContainer.innerHTML = `
            <div id="karaoke-empty-state" class="text-center py-20 text-slate-500 text-sm italic">
                Select a song from the library to start karaoke!
            </div>
        `;
        this.stageContainer.scrollTop = 0;
    }

    renderEmptyState() {
        if (!this.stageContainer) return;
        this.stageContainer.innerHTML = `
            <div class="text-center py-20 space-y-2">
                <span class="text-3xl">🎤</span>
                <p class="text-slate-300 text-base font-semibold">No lyrics added yet for this song</p>
                <p class="text-slate-500 text-xs">Click the "📝" button on the song card in the library to add timestamped lyrics!</p>
            </div>
        `;
        this.stageContainer.scrollTop = 0;
    }

    onTimeCheck() {
        if (!window.flexiokePlayer) return;

        this.updatePlayBtnUI();

        if (!this.currentJobId || !this.lyricsData || !this.lyricsData.hasTimestamps) {
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
                const remaining = Math.max(0, (dur || 0) - currentTime);
                this.timecodeEl.textContent = `${fmt(currentTime)} / ${fmt(dur || 0)} (-${fmt(remaining)})`;
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

        // Update 3-beat countdown cue
        this.updateCountdownCue(currentTime);
    }

    updateCountdownCue(currentTime) {
        if (!this.countdownCue || !this.lyricsData || !this.lyricsData.hasTimestamps || !this.lyricsData.lines.length) {
            this.hideCountdownCue();
            return;
        }

        // Find next upcoming lyric line
        let nextIndex = -1;
        for (let i = 0; i < this.lyricsData.lines.length; i++) {
            if (this.lyricsData.lines[i].time > currentTime) {
                nextIndex = i;
                break;
            }
        }

        if (nextIndex === -1) {
            this.hideCountdownCue();
            return;
        }

        const nextLine = this.lyricsData.lines[nextIndex];
        const delta = nextLine.time - currentTime;

        // Check if intro (first line with >= 2.5s intro) or musical interlude (> 8.0s gap between lines)
        const isIntro = (nextIndex === 0 && nextLine.time >= 2.5);
        const prevLineTime = nextIndex > 0 ? this.lyricsData.lines[nextIndex - 1].time : 0;
        const isInterlude = !isIntro && (nextLine.time - prevLineTime > 8.0);

        if ((isIntro || isInterlude) && delta > 0.05 && delta <= 3.0) {
            this.countdownCue.classList.remove('hidden');
            let num = Math.ceil(delta);
            if (num > 3) num = 3;
            if (num < 1) num = 1;

            if (this.countdownNumber) {
                this.countdownNumber.textContent = String(num);
            }

            if (this.countdownDots) {
                if (num === 3) {
                    this.countdownDots.innerHTML = `<span>●</span><span>○</span><span>○</span>`;
                } else if (num === 2) {
                    this.countdownDots.innerHTML = `<span>●</span><span>●</span><span>○</span>`;
                } else {
                    this.countdownDots.innerHTML = `<span>●</span><span>●</span><span>●</span>`;
                }
            }
        } else {
            this.hideCountdownCue();
        }
    }

    hideCountdownCue() {
        if (this.countdownCue && !this.countdownCue.classList.contains('hidden')) {
            this.countdownCue.classList.add('hidden');
        }
    }

    highlightLine(index) {
        if (this.activeLineIndex >= 0 && this.lineElements[this.activeLineIndex]) {
            const prevEl = this.lineElements[this.activeLineIndex];
            prevEl.className = "karaoke-line text-slate-400 font-semibold transition-all duration-300 py-2.5 px-4 rounded-xl cursor-pointer hover:text-white hover:bg-slate-800/40";
            prevEl.style.fontSize = "var(--karaoke-font-size, 20px)";
            prevEl.style.borderColor = "transparent";
            prevEl.style.backgroundColor = "transparent";
            prevEl.style.boxShadow = "none";
        }

        this.activeLineIndex = index;
        const activeEl = this.lineElements[index];
        if (activeEl) {
            const highlightColor = this.config.activeHighlightColor || '#06b6d4';
            activeEl.className = "karaoke-line text-white font-extrabold rounded-2xl py-3.5 px-6 scale-105 transition-all duration-300 cursor-pointer border";
            activeEl.style.fontSize = "var(--karaoke-active-font-size, 27px)";
            activeEl.style.borderColor = "var(--karaoke-highlight-color, " + highlightColor + ")";
            activeEl.style.backgroundColor = "rgba(6, 182, 212, 0.15)";
            activeEl.style.boxShadow = `0 10px 25px -5px ${highlightColor}40`;
            activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.flexiokeKaraoke = new KaraokeStageManager();
});
