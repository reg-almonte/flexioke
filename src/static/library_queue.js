/**
 * Flexioke — Song Library & Playback Queue UI Controller
 */
class SongLibraryManager {
    constructor() {
        this.searchInput = document.getElementById('library-search-input');
        this.listContainer = document.getElementById('library-list-container');
        this.countBadge = document.getElementById('library-count-badge');
        this.debounceTimeout = null;

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
                </div>
            `;

            // Bind card actions
            const playBtn = card.querySelector('.play-now-btn');
            playBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.playNow(job.job_id);
                } else if (window.flexiokePlayer) {
                    window.flexiokePlayer.loadSong(job);
                    setTimeout(() => window.flexiokePlayer.play(), 200);
                }
            });

            const queueBtn = card.querySelector('.add-queue-btn');
            queueBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.addToQueue(job.job_id);
                }
            });

            this.listContainer.appendChild(card);
        });
    }
}

class PlaybackQueueManager {
    constructor() {
        this.queueContainer = document.getElementById('queue-list-container');
        this.clearBtn = document.getElementById('clear-queue-btn');
        this.playNextBtn = document.getElementById('play-next-queue-btn');

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
            console.log("Track ended, advancing queue...");
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
                    window.flexiokePlayer.loadSong(state.current_track);
                    setTimeout(() => window.flexiokePlayer.play(), 250);
                }
            }
        } catch (err) {
            console.error("Error with play now:", err);
        }
    }

    async advanceNext() {
        try {
            const resp = await fetch('/api/queue/next', { method: 'POST' });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
                if (state.current_track && window.flexiokePlayer) {
                    window.flexiokePlayer.loadSong(state.current_track);
                    setTimeout(() => window.flexiokePlayer.play(), 250);
                }
            }
        } catch (err) {
            console.error("Error advancing queue:", err);
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
