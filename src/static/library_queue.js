/**
 * Flexioke — Song Library & Playback Queue UI Controller
 */
class SongLibraryManager {
    constructor() {
        this.searchInput = document.getElementById('library-search-input');
        this.listContainer = document.getElementById('library-list-container');
        this.countBadge = document.getElementById('library-count-badge');
        this.debounceTimeout = null;

        // Lyrics modal elements
        this.lyricsModal = document.getElementById('lyrics-modal');
        this.lyricsModalTitle = document.getElementById('lyrics-modal-title');
        this.lyricsTextarea = document.getElementById('lyrics-textarea');
        this.lyricsSaveStatus = document.getElementById('lyrics-save-status');
        this.closeLyricsModalBtn = document.getElementById('close-lyrics-modal-btn');
        this.cancelLyricsBtn = document.getElementById('cancel-lyrics-btn');
        this.saveLyricsBtn = document.getElementById('save-lyrics-btn');
        this.activeLyricsJobId = null;

        // Play interruption confirmation modal
        this.playConfirmModal = document.getElementById('play-confirm-modal');
        this.confirmSongTitle = document.getElementById('confirm-song-title');
        this.confirmPlayBtn = document.getElementById('confirm-play-btn');
        this.confirmCancelBtn = document.getElementById('confirm-cancel-btn');
        this.pendingPlayJob = null;

        this.init();
    }

    init() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => {
                clearTimeout(this.debounceTimeout);
                this.debounceTimeout = setTimeout(() => {
                    this.fetchLibrary(this.searchInput.value.trim());
                }, 250);
            });
        }

        // Lyrics modal handlers
        if (this.closeLyricsModalBtn) {
            this.closeLyricsModalBtn.addEventListener('click', () => this.closeLyricsModal());
        }
        if (this.cancelLyricsBtn) {
            this.cancelLyricsBtn.addEventListener('click', () => this.closeLyricsModal());
        }
        if (this.saveLyricsBtn) {
            this.saveLyricsBtn.addEventListener('click', () => this.saveLyrics());
        }

        // Play confirmation modal handlers
        if (this.confirmPlayBtn) {
            this.confirmPlayBtn.addEventListener('click', () => {
                if (this.playConfirmModal) this.playConfirmModal.classList.add('hidden');
                if (this.pendingPlayJob && window.flexiokeQueue) {
                    window.flexiokeQueue.playNow(this.pendingPlayJob.job_id);
                }
                this.pendingPlayJob = null;
            });
        }

        if (this.confirmCancelBtn) {
            this.confirmCancelBtn.addEventListener('click', () => {
                if (this.playConfirmModal) this.playConfirmModal.classList.add('hidden');
                this.pendingPlayJob = null;
                // Resume previous music
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.play();
                }
            });
        }

        // Auto-refresh when a job completes
        window.addEventListener('flexioke:job-completed', () => {
            this.fetchLibrary();
        });

        // Initial fetch
        this.fetchLibrary();
    }

    async fetchLibrary(query = '') {
        try {
            const url = query ? `/api/jobs?status=completed&q=${encodeURIComponent(query)}` : '/api/jobs?status=completed';
            const resp = await fetch(url);
            if (!resp.ok) return;
            const data = await resp.json();
            this.render(data.jobs || []);
        } catch (err) {
            console.error("Error fetching library:", err);
        }
    }

    render(jobs) {
        if (!this.listContainer) return;
        if (this.countBadge) {
            this.countBadge.textContent = `${jobs.length} ${jobs.length === 1 ? 'song' : 'songs'}`;
        }

        if (jobs.length === 0) {
            this.listContainer.innerHTML = `
                <div class="text-center py-8 text-slate-500 text-xs">
                    No songs found.<br>Upload or extract audio above!
                </div>
            `;
            return;
        }

        this.listContainer.innerHTML = '';
        jobs.forEach(job => {
            const card = document.createElement('div');
            card.className = "p-3 bg-surface-950/80 hover:bg-slate-800/80 border border-slate-800/80 hover:border-brand-500/40 rounded-xl transition flex items-center justify-between gap-3 group";

            const sourceIcon = job.source_type === 'youtube' ? '▶️' : '📁';
            const durationFmt = job.duration_seconds ? `${Math.floor(job.duration_seconds / 60)}:${String(Math.floor(job.duration_seconds % 60)).padStart(2, '0')}` : '';

            card.innerHTML = `
                <div class="flex items-center gap-2.5 min-w-0 flex-1">
                    <span class="text-base">${sourceIcon}</span>
                    <div class="truncate">
                        <h4 class="text-xs font-semibold text-slate-200 truncate group-hover:text-brand-300 transition">${escapeHtml(job.title)}</h4>
                        <div class="flex items-center gap-2 text-[10px] text-slate-500">
                            <span>${durationFmt || 'Stems ready'}</span>
                            <span>•</span>
                            <span class="truncate">${escapeHtml(job.source_name)}</span>
                        </div>
                    </div>
                </div>
                <div class="flex items-center gap-1.5 shrink-0">
                    <button class="play-now-btn px-2.5 py-1 rounded-lg bg-brand-600/90 hover:bg-brand-500 text-white text-[10px] font-semibold transition flex items-center gap-1 shadow-sm" data-job-id="${job.job_id}">
                        <span>▶</span> Play
                    </button>
                    <button class="add-queue-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-[10px] font-medium transition" data-job-id="${job.job_id}">
                        + Queue
                    </button>
                    <button class="lyrics-btn px-2 py-1 rounded-lg bg-slate-800/70 hover:bg-slate-700 text-slate-400 hover:text-brand-300 text-[10px] font-medium transition" title="Add / Edit Lyrics" data-job-id="${job.job_id}">
                        📝
                    </button>
                </div>
            `;

            // Bind card actions
            const playBtn = card.querySelector('.play-now-btn');
            playBtn.addEventListener('click', () => {
                // Check for active playback interruption
                if (window.flexiokePlayer && window.flexiokePlayer.isPlaying && window.flexiokePlayer.currentJob && window.flexiokePlayer.currentJob.job_id !== job.job_id) {
                    window.flexiokePlayer.pause();
                    this.pendingPlayJob = job;
                    if (this.confirmSongTitle) this.confirmSongTitle.textContent = `"${job.title}"`;
                    if (this.playConfirmModal) this.playConfirmModal.classList.remove('hidden');
                } else {
                    if (window.flexiokeQueue) {
                        window.flexiokeQueue.playNow(job.job_id);
                    } else if (window.flexiokePlayer) {
                        window.flexiokePlayer.loadSong(job, true);
                    }
                }
            });

            const queueBtn = card.querySelector('.add-queue-btn');
            queueBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.addToQueue(job.job_id);
                }
            });

            const lyricsBtn = card.querySelector('.lyrics-btn');
            lyricsBtn.addEventListener('click', () => {
                this.openLyricsModal(job);
            });

            this.listContainer.appendChild(card);
        });
    }

    async openLyricsModal(job) {
        this.activeLyricsJobId = job.job_id;
        if (this.lyricsModalTitle) {
            this.lyricsModalTitle.textContent = job.title || "Untitled Song";
        }
        if (this.lyricsTextarea) {
            this.lyricsTextarea.value = "Loading lyrics...";
        }
        if (this.lyricsSaveStatus) {
            this.lyricsSaveStatus.textContent = "";
        }
        if (this.lyricsModal) {
            this.lyricsModal.classList.remove('hidden');
        }

        try {
            const resp = await fetch(`/api/jobs/${job.job_id}/lyrics`);
            if (resp.ok) {
                const data = await resp.json();
                if (this.lyricsTextarea) {
                    this.lyricsTextarea.value = data.lyrics || "";
                }
            }
        } catch (err) {
            console.error("Error loading lyrics:", err);
            if (this.lyricsTextarea) {
                this.lyricsTextarea.value = "";
            }
        }
    }

    closeLyricsModal() {
        this.activeLyricsJobId = null;
        if (this.lyricsModal) {
            this.lyricsModal.classList.add('hidden');
        }
    }

    async saveLyrics() {
        if (!this.activeLyricsJobId || !this.lyricsTextarea) return;
        const text = this.lyricsTextarea.value;

        if (this.saveLyricsBtn) this.saveLyricsBtn.disabled = true;
        if (this.lyricsSaveStatus) this.lyricsSaveStatus.textContent = "Saving...";

        try {
            const resp = await fetch(`/api/jobs/${this.activeLyricsJobId}/lyrics`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lyrics: text })
            });

            if (resp.ok) {
                const data = await resp.json();
                if (this.lyricsSaveStatus) this.lyricsSaveStatus.textContent = "Saved!";
                window.dispatchEvent(new CustomEvent('flexioke:lyrics-updated', {
                    detail: { job_id: this.activeLyricsJobId, lyrics: text, has_timestamps: data.has_timestamps }
                }));
                setTimeout(() => this.closeLyricsModal(), 600);
            } else {
                if (this.lyricsSaveStatus) this.lyricsSaveStatus.textContent = "Save failed";
            }
        } catch (err) {
            console.error("Error saving lyrics:", err);
            if (this.lyricsSaveStatus) this.lyricsSaveStatus.textContent = "Error saving";
        } finally {
            if (this.saveLyricsBtn) this.saveLyricsBtn.disabled = false;
        }
    }
}

class PlaybackQueueManager {
    constructor() {
        this.queueContainer = document.getElementById('queue-list-container');
        this.clearBtn = document.getElementById('clear-queue-btn');
        this.playNextBtn = document.getElementById('play-next-queue-btn');
        this.isAdvancing = false;

        this.init();
    }

    init() {
        if (this.clearBtn) {
            this.clearBtn.addEventListener('click', () => this.clearQueue());
        }
        if (this.playNextBtn) {
            this.playNextBtn.addEventListener('click', () => this.advanceNext());
        }

        // Handle auto-advance when a track finishes
        window.addEventListener('flexioke:track-ended', () => {
            console.log("Track ended event received, triggering advanceNext...");
            this.advanceNext();
        });

        // Initial queue fetch
        this.fetchQueue();
    }

    async fetchQueue() {
        try {
            const resp = await fetch('/api/queue');
            if (!resp.ok) return;
            const state = await resp.json();
            this.render(state);
        } catch (err) {
            console.error("Error fetching queue:", err);
        }
    }

    async addToQueue(jobId) {
        try {
            const resp = await fetch('/api/queue/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ job_id: jobId })
            });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
            }
        } catch (err) {
            console.error("Error adding to queue:", err);
        }
    }

    async playNow(jobId) {
        try {
            const resp = await fetch('/api/queue/play-now', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ job_id: jobId })
            });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
                if (state.current_track && window.flexiokePlayer) {
                    // Autoplay set to true on load
                    window.flexiokePlayer.loadSong(state.current_track, true);
                }
            }
        } catch (err) {
            console.error("Error with play now:", err);
        }
    }

    async advanceNext() {
        if (this.isAdvancing) return;
        this.isAdvancing = true;

        try {
            const resp = await fetch('/api/queue/next', { method: 'POST' });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
                if (state.current_track && window.flexiokePlayer) {
                    // Autoplay set to true on load
                    window.flexiokePlayer.loadSong(state.current_track, true);
                }
            }
        } catch (err) {
            console.error("Error advancing queue:", err);
        } finally {
            setTimeout(() => {
                this.isAdvancing = false;
            }, 500);
        }
    }

    async removeFromQueue(queueId) {
        try {
            const resp = await fetch(`/api/queue/${queueId}`, { method: 'DELETE' });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
            }
        } catch (err) {
            console.error("Error removing from queue:", err);
        }
    }

    async clearQueue() {
        try {
            const resp = await fetch('/api/queue', { method: 'DELETE' });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
            }
        } catch (err) {
            console.error("Error clearing queue:", err);
        }
    }

    render(state) {
        if (!this.queueContainer) return;
        const queue = state.queue || [];

        if (queue.length === 0) {
            this.queueContainer.innerHTML = `
                <div class="text-center py-6 text-slate-500 text-xs">
                    Playback queue is empty.<br>Add songs from the library on the left!
                </div>
            `;
            return;
        }

        this.queueContainer.innerHTML = '';
        queue.forEach((item, index) => {
            const row = document.createElement('div');
            row.className = "p-2.5 bg-surface-950/70 border border-slate-800/80 rounded-xl flex items-center justify-between gap-3 text-xs";

            row.innerHTML = `
                <div class="flex items-center gap-2.5 truncate min-w-0">
                    <span class="w-5 h-5 rounded-full bg-slate-800 text-[10px] text-slate-400 font-bold flex items-center justify-center shrink-0">
                        ${index + 1}
                    </span>
                    <span class="font-medium text-slate-200 truncate">${escapeHtml(item.title)}</span>
                </div>
                <button class="remove-queue-btn text-slate-500 hover:text-rose-400 p-1 text-xs shrink-0 transition" data-queue-id="${item.queue_id}">
                    ✕
                </button>
            `;

            const removeBtn = row.querySelector('.remove-queue-btn');
            removeBtn.addEventListener('click', () => this.removeFromQueue(item.queue_id));

            this.queueContainer.appendChild(row);
        });
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

document.addEventListener('DOMContentLoaded', () => {
    window.flexiokeLibrary = new SongLibraryManager();
    window.flexiokeQueue = new PlaybackQueueManager();
});
