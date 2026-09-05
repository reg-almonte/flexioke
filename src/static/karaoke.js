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
                const rawText = trimmed.replace(timestampRegex, '').trim();
                let text = rawText;
                let isInstrumental = false;
                if (!text) {
                    text = "♪ ♪ ♪ (Instrumental)";
                    isInstrumental = true;
                }

                matches.forEach(m => {
                    const mins = parseInt(m[1], 10);
                    const secs = parseFloat(m[2]);
                    const time = mins * 60 + secs;
                    parsedLines.push({ time, text, rawText, isInstrumental });
                });
            }
        });

        if (parsedLines.length > 0) {
            parsedLines.sort((a, b) => a.time - b.time);

            // If the final line is an empty timestamp or instrumental placeholder, label it as "End"
            const lastLine = parsedLines[parsedLines.length - 1];
            if (lastLine.isInstrumental || lastLine.text === "♪ ♪ ♪ (Instrumental)" || !lastLine.rawText) {
                lastLine.text = "♪  End  ♪";
                lastLine.isInstrumental = true;
            }

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
        this.nowSingingTextEl = document.getElementById('karaoke-now-singing-text');
        this.upNextTextEl = document.getElementById('karaoke-up-next-text');
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
        this.settingGlowColorInput = document.getElementById('settings-highlight-glow-color');
        this.settingGlowColorDisplay = document.getElementById('settings-glow-color-display');
        this.settingFillColorInput = document.getElementById('settings-highlight-fill-color');
        this.settingFillColorDisplay = document.getElementById('settings-fill-color-display');
        this.settingFontSizeInput = document.getElementById('settings-font-size');
        this.settingFontSizeDisplay = document.getElementById('settings-font-size-display');
        this.settingActiveFontSizeInput = document.getElementById('settings-active-font-size');
        this.settingActiveFontSizeDisplay = document.getElementById('settings-active-font-size-display');

        // Intro Splash Screen Elements
        this.introSplash = document.getElementById('karaoke-intro-splash');
        this.introSplashTitle = document.getElementById('intro-splash-title');
        this.introSplashArtist = document.getElementById('intro-splash-artist');
        this.introSplashTimer = document.getElementById('intro-splash-timer');
        this.settingIntroSplashInput = document.getElementById('settings-intro-splash');
        this.settingIntroSplashDisplay = document.getElementById('settings-intro-splash-display');
        this.introSplashInterval = null;

        // Countdown Threshold Setting Elements
        this.settingCountdownThresholdInput = document.getElementById('settings-countdown-threshold');
        this.settingCountdownThresholdDisplay = document.getElementById('settings-countdown-threshold-display');

        // Default Config & State
        this.defaultConfig = {
            introSplashDuration: 3,
            countdownThreshold: 3,
            activeHighlightGlowColor: '#06b6d4',
            activeHighlightFillColor: '#0891b2',
            baseFontSizePx: 20,
            activeFontSizePx: 24
        };
        this.config = { ...this.defaultConfig };

        // Fullscreen elements
        this.fullscreenBtn = document.getElementById('karaoke-fullscreen-btn');
        this.fullscreenIcon = document.getElementById('fullscreen-icon');
        this.fullscreenBtnText = document.getElementById('fullscreen-btn-text');
        this.isFullscreen = false;

        // Karaoke Transport Elements
        this.playBtn = document.getElementById('karaoke-play-btn');
        this.restartBtn = document.getElementById('karaoke-restart-btn');
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

        this.timecodeMode = localStorage.getItem('flexioke_timecode_mode') || 'elapsed';

        this.loadSettings();
        this.init();
    }

    init() {
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
        if (this.settingGlowColorInput) {
            this.settingGlowColorInput.addEventListener('input', (e) => {
                const val = e.target.value;
                if (this.settingGlowColorDisplay) this.settingGlowColorDisplay.textContent = val;
                this.saveSettings({ activeHighlightGlowColor: val, activeHighlightColor: val });
            });
        }
        if (this.settingFillColorInput) {
            this.settingFillColorInput.addEventListener('input', (e) => {
                const val = e.target.value;
                if (this.settingFillColorDisplay) this.settingFillColorDisplay.textContent = val;
                this.saveSettings({ activeHighlightFillColor: val });
            });
        }
        if (this.settingFontSizeInput) {
            this.settingFontSizeInput.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10) || 20;
                if (this.settingFontSizeDisplay) this.settingFontSizeDisplay.textContent = `${val}px`;
                this.saveSettings({ baseFontSizePx: val });
            });
        }
        if (this.settingActiveFontSizeInput) {
            this.settingActiveFontSizeInput.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10) || 24;
                if (this.settingActiveFontSizeDisplay) this.settingActiveFontSizeDisplay.textContent = `${val}px`;
                this.saveSettings({ activeFontSizePx: val });
            });
        }
        if (this.settingIntroSplashInput) {
            this.settingIntroSplashInput.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10);
                const safeVal = isNaN(val) ? 3 : Math.max(0, Math.min(5, val));
                if (this.settingIntroSplashDisplay) this.settingIntroSplashDisplay.textContent = `${safeVal}s`;
                this.saveSettings({ introSplashDuration: safeVal });
            });
        }
        if (this.settingCountdownThresholdInput) {
            this.settingCountdownThresholdInput.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10);
                const safeVal = isNaN(val) ? 3 : Math.max(3, Math.min(5, val));
                if (this.settingCountdownThresholdDisplay) this.settingCountdownThresholdDisplay.textContent = `${safeVal}s`;
                this.saveSettings({ countdownThreshold: safeVal });
            });
        }

        // Stage Background Click-to-Play/Pause
        if (this.stageContainer) {
            this.stageContainer.style.cursor = 'pointer';
            this.stageContainer.addEventListener('click', (e) => {
                if (!e.target.closest('.karaoke-line')) {
                    this.togglePlayPause();
                }
            });
        }

        // Fullscreen Toggle
        if (this.fullscreenBtn) {
            this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }

        document.addEventListener('keydown', (e) => {
            // Dismiss Modals and Fullscreen on Escape
            if (e.key === 'Escape') {
                if (this.isFullscreen) {
                    this.exitFullscreen();
                }
                this.closeSettingsModal();
                const catalogModal = document.getElementById('song-catalog-modal');
                if (catalogModal && !catalogModal.classList.contains('hidden')) {
                    catalogModal.classList.add('hidden');
                }
            }

            // Keyboard Shortcut: 'R' or 'Home' to restart song in Karaoke Mode
            const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
            const isTyping = activeTag === 'input' || activeTag === 'textarea' || (document.activeElement && document.activeElement.isContentEditable);
            if (!isTyping) {
                if (e.key === 'r' || e.key === 'R' || e.key === 'Home') {
                    const karaokeView = document.getElementById('view-karaoke');
                    if (karaokeView && !karaokeView.classList.contains('hidden')) {
                        e.preventDefault();
                        this.restartSong();
                    }
                }
            }
        });

        // Bind Karaoke Transport Controls
        if (this.playBtn) {
            this.playBtn.addEventListener('click', () => {
                this.togglePlayPause();
            });
        }

        if (this.restartBtn) {
            this.restartBtn.addEventListener('click', () => {
                this.restartSong();
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
            const savedVol = parseFloat(localStorage.getItem('flexioke_master_volume') || '0.8');
            this.volumeSlider.value = savedVol;
            if (window.flexiokePlayer) {
                window.flexiokePlayer.masterVolume = savedVol;
            }

            this.volumeSlider.addEventListener('input', (e) => {
                const val = parseFloat(e.target.value);
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.masterVolume = val;
                    window.flexiokePlayer.applyGainMatrix();
                }
                try {
                    localStorage.setItem('flexioke_master_volume', String(val));
                } catch(err) {}
                const masterSlider = document.getElementById('master-volume-slider');
                if (masterSlider) masterSlider.value = val;
            });
        }

        // Timecode Click-to-Toggle Mode
        if (this.timecodeEl) {
            this.timecodeEl.addEventListener('click', () => {
                this.toggleTimecodeMode();
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
                this.updateStageHeader();
            }
        });

        // Listen for queue updates to dynamically update Up Next header
        window.addEventListener('flexioke:queue-updated', (e) => {
            this.updateStageHeader();
        });

        // Listen for player reset (when queue finishes or stop clicked without queue)
        window.addEventListener('flexioke:player-reset', () => {
            this.clearIntroSplash();
            this.hideIntroSplash();
            this.currentJob = null;
            this.currentJobId = null;
            this.lyricsData = null;
            this.activeLineIndex = -1;
            this.updateStageHeader();
            if (this.timecodeEl) {
                this.timecodeEl.textContent = (this.timecodeMode === 'remaining') ? "-00:00 / 00:00" : "00:00 / 00:00";
            }
            this.renderDefaultState();
            this.updatePlayBtnUI();
        });

        // Listen for song loaded event from FlexiokePlayer
        window.addEventListener('flexioke:song-loaded', (e) => {
            if (e.detail && e.detail.job) {
                this.onSongLoaded(e.detail.job, e.detail.autoPlay);
            }
        });

        // Hook into FlexiokePlayer loadSong as fallback
        const originalLoadSong = window.flexiokePlayer ? window.flexiokePlayer.loadSong.bind(window.flexiokePlayer) : null;
        if (window.flexiokePlayer && originalLoadSong) {
            window.flexiokePlayer.loadSong = (job, autoPlay = false) => {
                originalLoadSong(job, autoPlay);
                if (job) {
                    this.onSongLoaded(job, autoPlay);
                }
            };
        }

        // If player already has a job loaded on initialization
        if (window.flexiokePlayer && window.flexiokePlayer.currentJob) {
            this.onSongLoaded(window.flexiokePlayer.currentJob);
        }

        // Setup dynamic observer for Stage Header Marquee
        if (window.ResizeObserver && this.stageCard) {
            const resizeObs = new ResizeObserver(() => {
                this.updateStageHeader();
            });
            resizeObs.observe(this.stageCard);
        }

        // Time & Transport state check
        setInterval(() => this.onTimeCheck(), 100);

        // Initialize Karaoke Sidebar Accordions
        this.initKaraokeAccordions();
    }

    initKaraokeAccordions() {
        const ACCORDION_STORAGE_KEY = 'flexioke_karaoke_accordions';
        const defaultAccordionState = { 'karaoke-queue': true, 'karaoke-library': true };
        let accordionState = { ...defaultAccordionState };

        try {
            const saved = localStorage.getItem(ACCORDION_STORAGE_KEY);
            if (saved) {
                accordionState = { ...defaultAccordionState, ...JSON.parse(saved) };
            }
        } catch (e) {
            console.error("Failed to load karaoke accordion state:", e);
        }

        const updateKaraokeAccordionUI = (section, isExpanded) => {
            const body = document.getElementById(`accordion-body-${section}`);
            const chevron = document.getElementById(`accordion-chevron-${section}`);
            if (body) {
                if (isExpanded) {
                    body.classList.remove('hidden');
                } else {
                    body.classList.add('hidden');
                }
            }
            if (chevron) {
                chevron.textContent = isExpanded ? '▾' : '▸';
            }
        };

        ['karaoke-queue', 'karaoke-library'].forEach(section => {
            const header = document.getElementById(`accordion-header-${section}`);
            if (header) {
                // Initial render from state
                updateKaraokeAccordionUI(section, !!accordionState[section]);

                header.addEventListener('click', (e) => {
                    // Prevent clicks on action buttons inside header (e.g. clear queue, open catalog) from toggling
                    if (e.target.closest('button:not(.accordion-toggle)')) return;
                    accordionState[section] = !accordionState[section];
                    try {
                        localStorage.setItem(ACCORDION_STORAGE_KEY, JSON.stringify(accordionState));
                    } catch (err) {}
                    updateKaraokeAccordionUI(section, accordionState[section]);
                });
            }
        });
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
        const basePx = parseInt(this.config.baseFontSizePx, 10) || 20;
        const activePx = parseInt(this.config.activeFontSizePx, 10) || 24;
        const glowColor = this.config.activeHighlightGlowColor || this.config.activeHighlightColor || '#06b6d4';
        const fillColor = this.config.activeHighlightFillColor || '#0891b2';

        document.documentElement.style.setProperty('--karaoke-font-size', `${basePx}px`);
        document.documentElement.style.setProperty('--karaoke-active-font-size', `${activePx}px`);
        document.documentElement.style.setProperty('--karaoke-highlight-color', glowColor);
        document.documentElement.style.setProperty('--karaoke-highlight-fill', fillColor);

        if (this.settingGlowColorInput) this.settingGlowColorInput.value = glowColor;
        if (this.settingGlowColorDisplay) this.settingGlowColorDisplay.textContent = glowColor;
        if (this.settingFillColorInput) this.settingFillColorInput.value = fillColor;
        if (this.settingFillColorDisplay) this.settingFillColorDisplay.textContent = fillColor;
        if (this.settingFontSizeInput) this.settingFontSizeInput.value = basePx;
        if (this.settingFontSizeDisplay) this.settingFontSizeDisplay.textContent = `${basePx}px`;
        if (this.settingActiveFontSizeInput) this.settingActiveFontSizeInput.value = activePx;
        if (this.settingActiveFontSizeDisplay) this.settingActiveFontSizeDisplay.textContent = `${activePx}px`;

        const introSplashSec = (typeof this.config.introSplashDuration !== 'undefined') ? parseInt(this.config.introSplashDuration, 10) : 3;
        if (this.settingIntroSplashInput) this.settingIntroSplashInput.value = introSplashSec;
        if (this.settingIntroSplashDisplay) this.settingIntroSplashDisplay.textContent = `${introSplashSec}s`;

        const countdownThresh = (typeof this.config.countdownThreshold !== 'undefined') ? parseInt(this.config.countdownThreshold, 10) : 3;
        if (this.settingCountdownThresholdInput) this.settingCountdownThresholdInput.value = countdownThresh;
        if (this.settingCountdownThresholdDisplay) this.settingCountdownThresholdDisplay.textContent = `${countdownThresh}s`;

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

    updateStageHeader() {
        if (this.nowSingingTextEl) {
            if (this.currentJob) {
                const title = this.currentJob.title || "Untitled Song";
                const artist = this.currentJob.artist ? ` - ${this.currentJob.artist}` : "";
                this.nowSingingTextEl.textContent = `${title}${artist}`;
            } else {
                this.nowSingingTextEl.textContent = "No Track Selected";
            }
            this.checkMarquee(this.nowSingingTextEl);
        }

        if (this.upNextTextEl) {
            const queue = (window.flexiokeQueue && window.flexiokeQueue.queue) ? window.flexiokeQueue.queue : [];
            if (queue.length > 0) {
                const next = queue[0];
                const title = next.title || "Untitled Song";
                const artist = next.artist ? ` - ${next.artist}` : "";
                this.upNextTextEl.textContent = `${title}${artist}`;
                this.upNextTextEl.className = "text-xs sm:text-sm font-semibold text-violet-200 tracking-tight inline-block whitespace-nowrap";
            } else {
                this.upNextTextEl.textContent = "— (Queue Empty)";
                this.upNextTextEl.className = "text-xs sm:text-sm font-medium text-slate-500 italic tracking-tight inline-block whitespace-nowrap";
            }
            this.checkMarquee(this.upNextTextEl);
        }
    }

    checkMarquee(el) {
        if (!el || !el.parentElement) return;
        const parent = el.parentElement;
        const evaluate = () => {
            if (!el || !el.parentElement) return;
            const wasScrolling = el.classList.contains('marquee-scroll');
            if (wasScrolling) {
                el.classList.remove('marquee-scroll');
            }
            const isOverflowing = el.scrollWidth > parent.clientWidth + 4;
            if (isOverflowing) {
                el.classList.add('marquee-scroll');
            } else {
                el.classList.remove('marquee-scroll');
            }
        };

        evaluate();
        setTimeout(evaluate, 60);
        setTimeout(evaluate, 350);
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
        // Fullscreen Active: button toggles to Collapse View
        // NOTE: Customize collapse icon here (e.g. '⤡', '🗕', '↙', '✕', '⛶')
        if (this.fullscreenIcon) this.fullscreenIcon.textContent = '↙';
        if (this.fullscreenBtnText) this.fullscreenBtnText.textContent = 'Collapse';
        if (this.fullscreenBtn) this.fullscreenBtn.title = "Exit Fullscreen Stage (Esc)";
        this.updateStageHeader();
        setTimeout(() => this.updateStageHeader(), 350);
    }

    exitFullscreen() {
        this.isFullscreen = false;
        if (this.stageCard) {
            this.stageCard.classList.remove('stage-fullscreen');
        }
        // Default View: button toggles to Expand View
        // NOTE: Customize expand icon here (e.g. '⛶', '⤢', '⤧', '↗')
        if (this.fullscreenIcon) this.fullscreenIcon.textContent = '⛶';
        if (this.fullscreenBtnText) this.fullscreenBtnText.textContent = 'Expand';
        if (this.fullscreenBtn) this.fullscreenBtn.title = "Toggle Fullscreen Stage";
        this.updateStageHeader();
        setTimeout(() => this.updateStageHeader(), 350);
    }

    onSongLoaded(job, autoPlay = true) {
        this.currentJob = job;
        this.currentJobId = job.job_id;
        this.updateStageHeader();
        if (this.stageContainer) {
            this.stageContainer.scrollTop = 0;
        }
        this.syncVocalButtons();
        this.loadLyricsForJob(job.job_id);
        this.triggerIntroSplash(job, autoPlay);
    }

    triggerIntroSplash(job, autoPlay = true) {
        this.clearIntroSplash();
        if (!job || !this.introSplash) return;

        const duration = (typeof this.config.introSplashDuration !== 'undefined') ? parseInt(this.config.introSplashDuration, 10) : 3;
        if (duration <= 0 || !autoPlay) {
            this.hideIntroSplash();
            return;
        }

        // Delay audio playback while intro splash is active
        if (window.flexiokePlayer) {
            window.flexiokePlayer.autoPlayPending = false;
            window.flexiokePlayer.pause();
        }

        if (this.introSplashTitle) this.introSplashTitle.textContent = job.title || "Unknown Title";
        if (this.introSplashArtist) this.introSplashArtist.textContent = job.artist || "Unknown Artist";
        if (this.introSplashTimer) this.introSplashTimer.textContent = duration;

        this.introSplash.classList.remove('hidden');

        let remaining = duration;
        this.introSplashInterval = setInterval(() => {
            remaining--;
            if (remaining > 0) {
                if (this.introSplashTimer) this.introSplashTimer.textContent = remaining;
            } else {
                this.clearIntroSplash();
                this.hideIntroSplash();
                if (window.flexiokePlayer && autoPlay) {
                    window.flexiokePlayer.play();
                }
            }
        }, 1000);
    }

    clearIntroSplash() {
        if (this.introSplashInterval) {
            clearInterval(this.introSplashInterval);
            this.introSplashInterval = null;
        }
    }

    hideIntroSplash() {
        this.clearIntroSplash();
        if (this.introSplash) {
            this.introSplash.classList.add('hidden');
        }
    }

    syncVocalButtons() {
        if (!window.flexiokePlayer) return;
        const leadTrack = window.flexiokePlayer.tracks.lead_vocals;
        const backingTrack = window.flexiokePlayer.tracks.backing_vocals;

        if (this.toggleLeadBtn && this.leadStatusText && leadTrack) {
            if (leadTrack.muted) {
                this.toggleLeadBtn.className = "karaoke-vocal-toggle rounded-xl bg-rose-600/30 border border-rose-500/50 text-rose-300 text-sm font-semibold transition flex items-center justify-center gap-1.5 hover:bg-rose-600/50 hover:text-white";
                this.leadStatusText.textContent = "Lead Vocals: MUTED";
                this.toggleLeadBtn.title = "Lead Vocals: MUTED (Click to Unmute)";
            } else {
                this.toggleLeadBtn.className = "karaoke-vocal-toggle rounded-xl bg-brand-600/30 border border-brand-500/50 text-brand-300 text-sm font-semibold transition flex items-center justify-center gap-1.5 hover:bg-brand-600/50 hover:text-white";
                this.leadStatusText.textContent = "Lead Vocals: ON";
                this.toggleLeadBtn.title = "Lead Vocals: ON (Click to Mute)";
            }
        }

        if (this.toggleBackingBtn && this.backingStatusText && backingTrack) {
            if (backingTrack.muted) {
                this.toggleBackingBtn.className = "karaoke-vocal-toggle rounded-xl bg-rose-600/30 border border-rose-500/50 text-rose-300 text-sm font-semibold transition flex items-center justify-center gap-1.5 hover:bg-rose-600/50 hover:text-white";
                this.backingStatusText.textContent = "Backing: MUTED";
                this.toggleBackingBtn.title = "Backing Vocals: MUTED (Click to Unmute)";
            } else {
                this.toggleBackingBtn.className = "karaoke-vocal-toggle rounded-xl bg-violet-600/30 border border-violet-500/50 text-violet-300 text-sm font-semibold transition flex items-center justify-center gap-1.5 hover:bg-violet-600/50 hover:text-white";
                this.backingStatusText.textContent = "Backing: ON";
                this.toggleBackingBtn.title = "Backing Vocals: ON (Click to Mute)";
            }
        }
    }

    togglePlayPause() {
        if (window.flexiokePlayer && this.currentJob) {
            window.flexiokePlayer.togglePlay();
            this.updatePlayBtnUI();
        } else if (!this.currentJob) {
            // Smart Idle Play Dispatch
            if (window.flexiokeQueue && Array.isArray(window.flexiokeQueue.queue) && window.flexiokeQueue.queue.length > 0) {
                window.flexiokeQueue.playNext();
            } else if (window.flexiokeSongLibrary) {
                window.flexiokeSongLibrary.openCatalogModal();
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
        wrapper.className = "space-y-3 py-32 max-w-3xl mx-auto w-full text-center";

        this.lyricsData.lines.forEach((line, index) => {
            const rowWrapper = document.createElement('div');
            rowWrapper.className = "karaoke-line-row py-1 text-center";

            const lineEl = document.createElement('span');
            lineEl.className = "karaoke-line inline-block text-slate-400 font-semibold transition-all duration-300 py-1.5 px-5 rounded-full cursor-pointer hover:text-white hover:bg-slate-800/60";
            lineEl.style.fontSize = "var(--karaoke-font-size, 20px)";
            lineEl.textContent = line.text;
            lineEl.dataset.index = index;

            // Click to seek directly to line with stopPropagation
            lineEl.addEventListener('click', (e) => {
                e.stopPropagation();
                if (window.flexiokePlayer && line.time !== null) {
                    window.flexiokePlayer.seekTo(line.time);
                }
            });

            rowWrapper.appendChild(lineEl);
            wrapper.appendChild(rowWrapper);
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

    toggleTimecodeMode() {
        this.timecodeMode = (this.timecodeMode === 'elapsed') ? 'remaining' : 'elapsed';
        try {
            localStorage.setItem('flexioke_timecode_mode', this.timecodeMode);
        } catch(err) {}
        this.onTimeCheck();
    }

    onTimeCheck() {
        if (!window.flexiokePlayer) return;

        this.updatePlayBtnUI();

        if (!this.currentJobId) {
            if (this.timecodeEl) {
                this.timecodeEl.textContent = (this.timecodeMode === 'remaining') ? "-00:00 / 00:00" : "00:00 / 00:00";
            }
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
                if (this.timecodeMode === 'remaining') {
                    this.timecodeEl.textContent = `-${fmt(remaining)} / ${fmt(dur || 0)}`;
                } else {
                    this.timecodeEl.textContent = `${fmt(currentTime)} / ${fmt(dur || 0)}`;
                }
            }
        }

        if (!this.lyricsData || !this.lyricsData.hasTimestamps) {
            return;
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

        // Find next upcoming sung lyric line (non-instrumental with text)
        let targetIndex = -1;
        for (let i = 0; i < this.lyricsData.lines.length; i++) {
            const line = this.lyricsData.lines[i];
            if (line.time > currentTime && !line.isInstrumental && line.rawText && line.rawText.length > 0) {
                targetIndex = i;
                break;
            }
        }

        if (targetIndex === -1) {
            this.hideCountdownCue();
            return;
        }

        const targetLine = this.lyricsData.lines[targetIndex];
        const delta = targetLine.time - currentTime;
        const threshold = (typeof this.config.countdownThreshold !== 'undefined') ? parseFloat(this.config.countdownThreshold) : 3.0;

        // Check if all lines before targetIndex are non-lyric / intro
        const hasPrevSungLine = this.lyricsData.lines.slice(0, targetIndex).some(l => !l.isInstrumental && l.rawText && l.rawText.length > 0);
        const isIntro = !hasPrevSungLine && (targetLine.time >= threshold);

        // Check if there is an explicit empty line / instrumental break preceding targetLine
        const prevLine = targetIndex > 0 ? this.lyricsData.lines[targetIndex - 1] : null;
        const isPrevInstrumental = prevLine && (prevLine.isInstrumental || !prevLine.rawText || prevLine.rawText.length === 0);
        const isInterlude = hasPrevSungLine && isPrevInstrumental && ((targetLine.time - prevLine.time) >= threshold) && (currentTime >= prevLine.time);

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
            prevEl.className = "karaoke-line inline-block text-slate-400 font-semibold transition-all duration-300 py-1.5 px-5 rounded-full cursor-pointer hover:text-white hover:bg-slate-800/60";
            prevEl.style.fontSize = `var(--karaoke-font-size, ${this.config.baseFontSizePx || 20}px)`;
            prevEl.style.borderColor = "transparent";
            prevEl.style.backgroundColor = "transparent";
            prevEl.style.boxShadow = "none";
        }

        this.activeLineIndex = index;
        const activeEl = this.lineElements[index];
        if (activeEl) {
            const glowColor = this.config.activeHighlightGlowColor || this.config.activeHighlightColor || '#06b6d4';
            const fillColor = this.config.activeHighlightFillColor || '#0891b2';
            activeEl.className = "karaoke-line inline-block text-white font-extrabold rounded-full py-2.5 px-7 scale-105 transition-all duration-300 cursor-pointer border";
            activeEl.style.fontSize = `var(--karaoke-active-font-size, ${this.config.activeFontSizePx || 24}px)`;
            activeEl.style.borderColor = `var(--karaoke-highlight-color, ${glowColor})`;
            activeEl.style.backgroundColor = `${fillColor}33`;
            activeEl.style.boxShadow = `0 10px 25px -5px ${glowColor}40`;
            activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    restartSong() {
        if (!this.currentJob) return;

        // 1. Reset stage lyrics scroll position immediately to the top
        if (this.stageContainer) {
            this.stageContainer.scrollTop = 0;
        }

        // 2. Reset active line index and clear active highlighted styling on all lines
        this.activeLineIndex = -1;
        if (this.lineElements && this.lineElements.length > 0) {
            const basePx = parseInt(this.config.baseFontSizePx, 10) || 20;
            this.lineElements.forEach((el) => {
                el.className = "karaoke-line inline-block text-slate-400 font-semibold transition-all duration-300 py-1.5 px-5 rounded-full cursor-pointer hover:text-white hover:bg-slate-800/60";
                el.style.fontSize = `var(--karaoke-font-size, ${basePx}px)`;
                el.style.borderColor = "transparent";
                el.style.backgroundColor = "transparent";
                el.style.boxShadow = "none";
            });
        }

        // 3. Clear and hide countdown cue
        this.hideCountdownCue();

        // 4. Trigger Intro Splash if duration > 0, otherwise restart audio playback immediately
        const duration = (typeof this.config.introSplashDuration !== 'undefined') ? parseInt(this.config.introSplashDuration, 10) : 3;
        if (duration > 0) {
            if (window.flexiokePlayer) {
                window.flexiokePlayer.restart(false);
            }
            this.triggerIntroSplash(this.currentJob, true);
        } else {
            if (window.flexiokePlayer) {
                window.flexiokePlayer.restart(true);
            }
        }
        this.updatePlayBtnUI();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.flexiokeKaraoke = new KaraokeStageManager();
});
