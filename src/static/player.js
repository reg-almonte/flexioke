/**
 * Flexioke — Multitrack Synchronized Audio Player & Mixer
 */
class FlexiokePlayer {
    constructor() {
        this.tracks = {
            instrumental: {
                id: 'instrumental',
                container: '#waveform-instrumental',
                waveColor: '#059669',
                progressColor: '#34d399',
                ws: null,
                muted: false,
                soloed: false,
                volume: 1.0,
                isReady: false,
            },
            lead_vocals: {
                id: 'lead_vocals',
                container: '#waveform-lead_vocals',
                waveColor: '#4f46e5',
                progressColor: '#818cf8',
                ws: null,
                muted: false,
                soloed: false,
                volume: 1.0,
                isReady: false,
            },
            backing_vocals: {
                id: 'backing_vocals',
                container: '#waveform-backing_vocals',
                waveColor: '#7c3aed',
                progressColor: '#a78bfa',
                ws: null,
                muted: false,
                soloed: false,
                volume: 1.0,
                isReady: false,
            }
        };

        this.isPlaying = false;
        this.masterVolume = 0.8;
        this.currentJob = null;
        this.duration = 0;
        this.isSyncingSeek = false;
        this.autoPlayPending = false;
        this.finishedFired = false;

        this.initDOM();
    }

    initDOM() {
        this.playBtn = document.getElementById('transport-play-btn');
        this.stopBtn = document.getElementById('transport-stop-btn');
        this.masterVolSlider = document.getElementById('master-volume-slider');
        this.songTitleEl = document.getElementById('player-song-title');
        this.timecodeEl = document.getElementById('player-timecode');

        if (this.playBtn) {
            this.playBtn.addEventListener('click', () => this.togglePlay());
        }
        if (this.stopBtn) {
            this.stopBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.stopAndCueNext();
                } else {
                    this.stop();
                }
            });
        }
        if (this.masterVolSlider) {
            this.masterVolSlider.addEventListener('input', (e) => {
                this.masterVolume = parseFloat(e.target.value);
                this.applyGainMatrix();
                const karaokeVol = document.getElementById('karaoke-volume-slider');
                if (karaokeVol) karaokeVol.value = this.masterVolume;
            });
        }

        // Bind per-track buttons
        Object.keys(this.tracks).forEach((trackKey) => {
            const muteBtn = document.getElementById(`mute-btn-${trackKey}`);
            const soloBtn = document.getElementById(`solo-btn-${trackKey}`);
            const volSlider = document.getElementById(`vol-slider-${trackKey}`);

            if (muteBtn) {
                muteBtn.addEventListener('click', () => this.toggleMute(trackKey));
            }
            if (soloBtn) {
                soloBtn.addEventListener('click', () => this.toggleSolo(trackKey));
            }
            if (volSlider) {
                volSlider.addEventListener('input', (e) => {
                    this.tracks[trackKey].volume = parseFloat(e.target.value);
                    this.applyGainMatrix();
                });
            }
        });

        // Listen for completed job events
        window.addEventListener('flexioke:job-completed', (e) => {
            if (e.detail && e.detail.stems) {
                this.loadSong(e.detail, true);
            }
        });
    }

    loadSong(job, autoPlay = false) {
        if (!job || !job.stems) {
            this.resetToDefault();
            return;
        }
        this.currentJob = job;
        this.autoPlayPending = autoPlay;
        this.finishedFired = false;
        if (this.songTitleEl) {
            this.songTitleEl.textContent = job.title || "Untitled Song";
        }
        this.isPlaying = false;
        this.updatePlayBtnUI();

        window.dispatchEvent(new CustomEvent('flexioke:song-loaded', { detail: { job, autoPlay } }));

        // Track how many stems need to load
        const expectedStems = Object.keys(this.tracks).filter(key => !!job.stems[key]);
        let readyCount = 0;

        // Destroy prior wavesurfer instances
        Object.keys(this.tracks).forEach((trackKey) => {
            const track = this.tracks[trackKey];
            if (track.ws) {
                try {
                    track.ws.unAll();
                    track.ws.destroy();
                } catch (err) {
                    console.error("Error destroying wavesurfer:", err);
                }
                track.ws = null;
            }
            track.isReady = false;
            const container = document.querySelector(track.container);
            if (container) {
                container.innerHTML = '';
            }
        });

        // Initialize Wavesurfer instances for each stem
        Object.keys(this.tracks).forEach((trackKey) => {
            const track = this.tracks[trackKey];
            const stemUrl = job.stems[trackKey];

            if (!stemUrl) {
                const container = document.querySelector(track.container);
                if (container) {
                    container.innerHTML = '<div class="absolute inset-0 flex items-center justify-center text-slate-600 text-[11px]">Stem not found</div>';
                }
                return;
            }

            if (typeof WaveSurfer === 'undefined') {
                console.warn("WaveSurfer library is not loaded.");
                return;
            }

            const ws = WaveSurfer.create({
                container: track.container,
                waveColor: track.waveColor,
                progressColor: track.progressColor,
                cursorColor: '#f43f5e',
                cursorWidth: 2,
                height: 64,
                barWidth: 2,
                barGap: 1,
                barRadius: 2,
                normalize: true,
                url: stemUrl
            });

            track.ws = ws;

            ws.on('ready', () => {
                track.isReady = true;
                readyCount++;
                this.duration = ws.getDuration();
                this.updateTimecode(0, this.duration);
                this.applyGainMatrix();

                // If all stems are decoded and ready, trigger autoplay if requested
                if (readyCount >= expectedStems.length && this.autoPlayPending) {
                    this.autoPlayPending = false;
                    this.play();
                }
            });

            ws.on('timeupdate', (currentTime) => {
                if (trackKey === 'instrumental' || (!this.tracks.instrumental.ws && track.isReady)) {
                    this.updateTimecode(currentTime, this.duration || ws.getDuration());
                }
            });

            ws.on('seeking', (currentTime) => {
                if (this.isSyncingSeek) return;
                this.isSyncingSeek = true;
                this.syncSeek(currentTime, trackKey);
                setTimeout(() => { this.isSyncingSeek = false; }, 50);
            });

            ws.on('finish', () => {
                // Only trigger finish once per song from the primary track
                if (trackKey === 'instrumental' || !this.tracks.instrumental.ws) {
                    this.onSongFinished();
                }
            });
        });
    }

    resetToDefault() {
        this.pause();
        this.currentJob = null;
        this.duration = 0;
        this.autoPlayPending = false;
        this.finishedFired = false;

        // Destroy prior wavesurfer instances
        Object.keys(this.tracks).forEach((trackKey) => {
            const track = this.tracks[trackKey];
            if (track.ws) {
                try {
                    track.ws.unAll();
                    track.ws.destroy();
                } catch (err) {
                    console.error("Error destroying wavesurfer:", err);
                }
                track.ws = null;
            }
            track.isReady = false;
            const container = document.querySelector(track.container);
            if (container) {
                container.innerHTML = '<div class="waveform-placeholder absolute inset-0 flex items-center justify-center text-slate-600 text-[11px]">No audio loaded</div>';
            }
        });

        if (this.songTitleEl) {
            this.songTitleEl.textContent = "No Track Loaded";
        }
        this.updateTimecode(0, 0);
        this.updatePlayBtnUI();

        // Dispatch reset event so Karaoke and other components reset too
        window.dispatchEvent(new CustomEvent('flexioke:player-reset'));
    }

    syncSeek(time, sourceTrackKey) {
        Object.keys(this.tracks).forEach((key) => {
            if (key !== sourceTrackKey && this.tracks[key].ws && this.tracks[key].isReady) {
                this.tracks[key].ws.setTime(time);
            }
        });
    }

    togglePlay() {
        if (!this.currentJob) return;

        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        this.isPlaying = true;
        this.updatePlayBtnUI();

        // Find primary timestamp
        let primaryTime = 0;
        const firstReady = Object.values(this.tracks).find(t => t.ws && t.isReady);
        if (firstReady) {
            primaryTime = firstReady.ws.getCurrentTime();
        }

        Object.values(this.tracks).forEach(track => {
            if (track.ws && track.isReady) {
                track.ws.setTime(primaryTime);
                track.ws.play().catch(err => console.warn(`Autoplay restriction or error on ${track.id}:`, err));
            }
        });
    }

    pause() {
        this.isPlaying = false;
        this.updatePlayBtnUI();

        Object.values(this.tracks).forEach(track => {
            if (track.ws) {
                track.ws.pause();
            }
        });
    }

    stop() {
        this.pause();
        this.finishedFired = false;
        Object.values(this.tracks).forEach(track => {
            if (track.ws && track.isReady) {
                track.ws.setTime(0);
            }
        });
        this.updateTimecode(0, this.duration);
    }

    toggleMute(trackKey) {
        const track = this.tracks[trackKey];
        if (!track) return;
        track.muted = !track.muted;

        const btn = document.getElementById(`mute-btn-${trackKey}`);
        if (btn) {
            btn.classList.toggle('btn-active-mute', track.muted);
        }

        this.applyGainMatrix();
    }

    toggleSolo(trackKey) {
        const track = this.tracks[trackKey];
        if (!track) return;
        track.soloed = !track.soloed;

        const btn = document.getElementById(`solo-btn-${trackKey}`);
        if (btn) {
            btn.classList.toggle('btn-active-solo', track.soloed);
        }

        this.applyGainMatrix();
    }

    applyGainMatrix() {
        const hasSolo = Object.values(this.tracks).some(t => t.soloed);

        Object.values(this.tracks).forEach(track => {
            if (!track.ws) return;

            let effectiveGain = 0;

            if (hasSolo) {
                effectiveGain = track.soloed ? track.volume * this.masterVolume : 0;
            } else {
                effectiveGain = track.muted ? 0 : track.volume * this.masterVolume;
            }

            try {
                track.ws.setVolume(effectiveGain);
            } catch (err) {
                console.error(`Error setting volume for ${track.id}:`, err);
            }
        });
    }

    onSongFinished() {
        if (this.finishedFired) return;
        this.finishedFired = true;

        this.isPlaying = false;
        this.updatePlayBtnUI();
        console.log("Song finished, dispatching flexioke:track-ended");
        window.dispatchEvent(new CustomEvent('flexioke:track-ended', { detail: this.currentJob }));
    }

    updatePlayBtnUI() {
        if (!this.playBtn) return;
        this.playBtn.innerHTML = this.isPlaying ? '⏸' : '▶';
    }

    updateTimecode(current, total) {
        if (!this.timecodeEl) return;
        const fmt = (s) => {
            const mins = Math.floor(s / 60);
            const secs = Math.floor(s % 60);
            return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        };
        this.timecodeEl.textContent = `${fmt(current || 0)} / ${fmt(total || 0)}`;
    }
}

// Instantiate global player
document.addEventListener('DOMContentLoaded', () => {
    window.flexiokePlayer = new FlexiokePlayer();
});
