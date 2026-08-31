/**
 * Flexioke — Song Library & Playback Queue UI Controller (Dual-Page Sync)
 */
class SongLibraryManager {
    constructor() {
        this.searchInputs = document.querySelectorAll('.library-search-input');
        this.searchClearBtns = document.querySelectorAll('.library-search-clear-btn');
        this.listContainers = document.querySelectorAll('.library-list-container');
        this.countBadges = document.querySelectorAll('.library-count-badge');
        this.debounceTimeout = null;
        this.jobs = [];

        // Lyrics modal elements
        this.lyricsModal = document.getElementById('lyrics-modal');
        this.lyricsModalTitle = document.getElementById('lyrics-modal-title');
        this.lyricsEditTitle = document.getElementById('lyrics-edit-title');
        this.lyricsEditArtist = document.getElementById('lyrics-edit-artist');
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
        this.confirmQueueBtn = document.getElementById('confirm-queue-btn');
        this.confirmCancelBtn = document.getElementById('confirm-cancel-btn');
        this.pendingPlayJob = null;

        // Expanded Song Catalog Modal elements
        this.catalogModal = document.getElementById('song-catalog-modal');
        this.openCatalogModalBtn = document.getElementById('open-catalog-modal-btn');
        this.closeCatalogModalBtn = document.getElementById('close-catalog-modal-btn');
        this.catalogSearchInput = document.getElementById('catalog-search-input');
        this.catalogSearchClearBtn = document.getElementById('catalog-search-clear-btn');
        this.catalogSortSelect = document.getElementById('catalog-sort-select');
        this.catalogSongsList = document.getElementById('catalog-songs-list');
        this.catalogTotalCount = document.getElementById('catalog-total-count');

        this.init();
    }

    init() {
        // Expanded catalog modal listeners
        const catalogTriggers = document.querySelectorAll('.open-catalog-btn, #open-catalog-modal-btn, #open-studio-catalog-btn');
        catalogTriggers.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.openCatalogModal();
            });
        });
        if (this.closeCatalogModalBtn) {
            this.closeCatalogModalBtn.addEventListener('click', () => this.closeCatalogModal());
        }
        if (this.catalogModal) {
            this.catalogModal.addEventListener('click', (e) => {
                if (e.target === this.catalogModal) this.closeCatalogModal();
            });
        }
        if (this.catalogSearchInput) {
            this.catalogSearchInput.addEventListener('input', (e) => {
                const query = e.target.value;
                if (this.catalogSearchClearBtn) {
                    if (query.trim().length > 0) {
                        this.catalogSearchClearBtn.classList.remove('hidden');
                    } else {
                        this.catalogSearchClearBtn.classList.add('hidden');
                    }
                }
                clearTimeout(this.debounceTimeout);
                this.debounceTimeout = setTimeout(() => {
                    this.renderCatalog();
                }, 150);
            });
        }
        if (this.catalogSearchClearBtn) {
            this.catalogSearchClearBtn.addEventListener('click', () => {
                if (this.catalogSearchInput) {
                    this.catalogSearchInput.value = '';
                    this.catalogSearchInput.focus();
                }
                this.catalogSearchClearBtn.classList.add('hidden');
                this.renderCatalog();
            });
        }
        if (this.catalogSortSelect) {
            this.catalogSortSelect.addEventListener('change', () => {
                this.renderCatalog();
            });
        }
        this.searchInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const query = e.target.value;
                // Sync all search inputs
                this.searchInputs.forEach(other => {
                    if (other !== e.target) other.value = query;
                });
                // Toggle clear buttons
                this.searchClearBtns.forEach(btn => {
                    if (query.trim().length > 0) {
                        btn.classList.remove('hidden');
                    } else {
                        btn.classList.add('hidden');
                    }
                });
                clearTimeout(this.debounceTimeout);
                this.debounceTimeout = setTimeout(() => {
                    this.fetchLibrary(query.trim());
                }, 250);
            });
        });

        this.searchClearBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                this.searchInputs.forEach(input => {
                    input.value = '';
                });
                this.searchClearBtns.forEach(b => b.classList.add('hidden'));
                this.fetchLibrary('');
            });
        });

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

        if (this.confirmQueueBtn) {
            this.confirmQueueBtn.addEventListener('click', () => {
                if (this.playConfirmModal) this.playConfirmModal.classList.add('hidden');
                if (this.pendingPlayJob && window.flexiokeQueue) {
                    window.flexiokeQueue.addToQueue(this.pendingPlayJob.job_id);
                }
                this.pendingPlayJob = null;
                // Resume previous music
                if (window.flexiokePlayer) {
                    window.flexiokePlayer.play();
                }
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
            this.jobs = data.jobs || [];
            this.render(this.jobs);
        } catch (err) {
            console.error("Error fetching library:", err);
        }
    }

    render(jobs = null) {
        if (jobs !== null) {
            this.jobs = jobs;
        }
        const currentJobs = this.jobs || [];

        this.countBadges.forEach(badge => {
            badge.textContent = `${currentJobs.length} ${currentJobs.length === 1 ? 'song' : 'songs'}`;
        });

        this.listContainers.forEach(container => {
            if (currentJobs.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-8 text-slate-500 text-xs">
                        No matching songs found.<br>Upload or extract audio in Stem Studio!
                    </div>
                `;
                return;
            }

            container.innerHTML = '';
            const isStudio = container.closest('#view-stem-studio') !== null || container.id === 'studio-library-list';
            const displayJobs = [...currentJobs];

            if (isStudio) {
                // Stem Studio: default to Recently Added (descending created_at)
                displayJobs.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
            } else {
                // Karaoke Mode: default to Alphabetical (Title A-Z)
                displayJobs.sort((a, b) => (a.title || "").toLowerCase().localeCompare((b.title || "").toLowerCase()));
            }

            displayJobs.forEach(job => {
                const card = document.createElement('div');
                card.className = "p-3 bg-surface-950/80 hover:bg-slate-800/80 border border-slate-800/80 hover:border-brand-500/40 rounded-xl transition flex items-center justify-between gap-3 group";

                const sourceIcon = job.source_type === 'youtube' ? '▶️' : '📁';
                const durationFmt = job.duration_seconds ? `${Math.floor(job.duration_seconds / 60)}:${String(Math.floor(job.duration_seconds % 60)).padStart(2, '0')}` : '';
                const durationSnippet = durationFmt ? `<span>${durationFmt}</span><span>•</span>` : '';
                const artistHtml = job.artist ? escapeHtml(job.artist) : '<span class="text-slate-500 italic">Unknown Artist</span>';

                let buttonsHtml = `
                    <button class="play-now-btn px-2.5 py-1 rounded-lg bg-brand-600/90 hover:bg-brand-500 text-white text-[10px] font-semibold transition flex items-center gap-1 shadow-sm" data-job-id="${job.job_id}">
                        <span>▶</span> Play
                    </button>
                    <button class="add-queue-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-[10px] font-medium transition" data-job-id="${job.job_id}">
                        + Queue
                    </button>
                `;
                if (isStudio) {
                    buttonsHtml += `
                        <button class="lyrics-btn edit-lyrics-btn px-2 py-1 rounded-lg bg-slate-800/70 hover:bg-slate-700 text-slate-400 hover:text-brand-300 text-[10px] font-medium transition" title="Edit Song Details & Lyrics" data-job-id="${job.job_id}">
                            📝
                        </button>
                    `;
                }

                card.innerHTML = `
                    <div class="flex items-center gap-2.5 min-w-0 flex-1">
                        <span class="text-base">${sourceIcon}</span>
                        <div class="truncate">
                            <h4 class="text-xs font-semibold text-slate-200 truncate group-hover:text-brand-300 transition">${escapeHtml(job.title)}</h4>
                            <div class="text-[11px] text-slate-400 truncate">${artistHtml}</div>
                            <div class="flex items-center gap-2 text-[10px] text-slate-500">
                                ${durationSnippet}
                                <span class="truncate">${escapeHtml(job.source_name)}</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-1.5 shrink-0">
                        ${buttonsHtml}
                    </div>
                `;

                // Bind card actions
                const playBtn = card.querySelector('.play-now-btn');
                playBtn.addEventListener('click', () => this.handlePlay(job));

                const queueBtn = card.querySelector('.add-queue-btn');
                queueBtn.addEventListener('click', () => {
                    if (window.flexiokeQueue) {
                        window.flexiokeQueue.addToQueue(job.job_id);
                    }
                });

                const lyricsBtn = card.querySelector('.lyrics-btn');
                if (lyricsBtn) {
                    lyricsBtn.addEventListener('click', () => {
                        this.openLyricsModal(job);
                    });
                }

                container.appendChild(card);
            });
        });

        this.renderCatalog();
    }

    handlePlay(job) {
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
    }

    openCatalogModal() {
        if (!this.catalogModal) return;
        this.catalogModal.classList.remove('hidden');
        if (this.catalogSearchInput) {
            this.catalogSearchInput.focus();
        }
        this.renderCatalog();
    }

    closeCatalogModal() {
        if (!this.catalogModal) return;
        this.catalogModal.classList.add('hidden');
    }

    renderCatalog() {
        if (!this.catalogSongsList) return;
        const rawJobs = [...(this.jobs || [])];
        const query = this.catalogSearchInput ? this.catalogSearchInput.value.trim().toLowerCase() : '';
        const sortOrder = this.catalogSortSelect ? this.catalogSortSelect.value : 'title_asc';

        let filtered = rawJobs;
        if (query) {
            filtered = filtered.filter(j => {
                const t = (j.title || '').toLowerCase();
                const a = (j.artist || '').toLowerCase();
                return t.includes(query) || a.includes(query);
            });
        }

        // Sort catalog jobs
        if (sortOrder === 'title_asc') {
            filtered.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
        } else if (sortOrder === 'title_desc') {
            filtered.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
        } else if (sortOrder === 'artist_asc') {
            filtered.sort((a, b) => (a.artist || '').localeCompare(b.artist || ''));
        } else if (sortOrder === 'recent') {
            filtered.sort((a, b) => (b.created_at || '').localeCompare(a.created_at || ''));
        }

        if (this.catalogTotalCount) {
            this.catalogTotalCount.textContent = `${filtered.length} ${filtered.length === 1 ? 'song' : 'songs'}`;
        }

        if (filtered.length === 0) {
            this.catalogSongsList.innerHTML = `
                <div class="text-center py-12 text-slate-500 text-xs">
                    No songs found matching "${escapeHtml(query)}".
                </div>
            `;
            return;
        }

        this.catalogSongsList.innerHTML = '';
        filtered.forEach(job => {
            const row = document.createElement('div');
            row.className = "p-3 bg-surface-950/90 hover:bg-slate-800/80 border border-slate-800/90 hover:border-brand-500/40 rounded-xl transition flex items-center justify-between gap-3 group";

            const sourceIcon = job.source_type === 'youtube' ? '▶️' : '📁';
            const durationFmt = job.duration_seconds ? `${Math.floor(job.duration_seconds / 60)}:${String(Math.floor(job.duration_seconds % 60)).padStart(2, '0')}` : '';
            const durationSnippet = durationFmt ? `<span>${durationFmt}</span><span>•</span>` : '';
            const artistHtml = job.artist ? escapeHtml(job.artist) : '<span class="text-slate-500 italic">Unknown Artist</span>';

            row.innerHTML = `
                <div class="flex items-center gap-3 min-w-0 flex-1">
                    <span class="text-lg">${sourceIcon}</span>
                    <div class="truncate">
                        <h4 class="text-xs sm:text-sm font-semibold text-slate-100 truncate group-hover:text-brand-300 transition">${escapeHtml(job.title)}</h4>
                        <div class="text-xs text-slate-400 truncate">${artistHtml}</div>
                        <div class="flex items-center gap-2 text-[10px] text-slate-500 mt-0.5">
                            ${durationSnippet}
                            <span class="truncate">${escapeHtml(job.source_name)}</span>
                        </div>
                    </div>
                </div>
                <div class="flex items-center gap-2 shrink-0">
                    <button class="catalog-play-btn px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition flex items-center gap-1.5 shadow-sm" data-job-id="${job.job_id}">
                        <span>▶</span> Play Now
                    </button>
                    <button class="catalog-queue-btn px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-medium transition" data-job-id="${job.job_id}">
                        + Add to Queue
                    </button>
                    <button class="catalog-edit-btn px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-brand-300 text-xs font-medium transition flex items-center gap-1" title="Edit Song Details & Lyrics" data-job-id="${job.job_id}">
                        <span>📝</span> Edit
                    </button>
                </div>
            `;

            const playBtn = row.querySelector('.catalog-play-btn');
            playBtn.addEventListener('click', () => {
                this.closeCatalogModal();
                this.handlePlay(job);
            });

            const queueBtn = row.querySelector('.catalog-queue-btn');
            queueBtn.addEventListener('click', () => {
                if (window.flexiokeQueue) {
                    window.flexiokeQueue.addToQueue(job.job_id);
                    queueBtn.textContent = '✓ Queued';
                    queueBtn.classList.add('text-brand-400');
                    setTimeout(() => {
                        queueBtn.textContent = '+ Add to Queue';
                        queueBtn.classList.remove('text-brand-400');
                    }, 1200);
                }
            });

            const editBtn = row.querySelector('.catalog-edit-btn');
            if (editBtn) {
                editBtn.addEventListener('click', () => {
                    this.openLyricsModal(job);
                });
            }

            this.catalogSongsList.appendChild(row);
        });
    }

    async openLyricsModal(job) {
        this.activeLyricsJobId = job.job_id;
        if (this.lyricsModalTitle) {
            this.lyricsModalTitle.textContent = job.title || "Untitled Song";
        }
        if (this.lyricsEditTitle) {
            this.lyricsEditTitle.value = job.title || "";
        }
        if (this.lyricsEditArtist) {
            this.lyricsEditArtist.value = job.artist || "";
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
        const newTitle = this.lyricsEditTitle ? this.lyricsEditTitle.value.trim() : "";
        const newArtist = this.lyricsEditArtist ? this.lyricsEditArtist.value.trim() : "";

        if (this.saveLyricsBtn) this.saveLyricsBtn.disabled = true;
        if (this.lyricsSaveStatus) this.lyricsSaveStatus.textContent = "Saving...";

        try {
            // Save metadata (title & artist) if title is provided
            let updatedJob = null;
            if (newTitle) {
                const metaResp = await fetch(`/api/jobs/${this.activeLyricsJobId}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: newTitle,
                        artist: newArtist || null
                    })
                });
                if (metaResp.ok) {
                    updatedJob = await metaResp.json();
                    if (this.jobs && Array.isArray(this.jobs)) {
                        const idx = this.jobs.findIndex(j => j.job_id === this.activeLyricsJobId);
                        if (idx !== -1 && updatedJob) {
                            this.jobs[idx] = updatedJob;
                            this.render(this.jobs);
                        }
                    }
                    window.dispatchEvent(new CustomEvent('flexioke:metadata-updated', {
                        detail: updatedJob
                    }));
                }
            }

            const resp = await fetch(`/api/jobs/${this.activeLyricsJobId}/lyrics`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lyrics: text })
            });

            if (resp.ok) {
                const data = await resp.json();
                if (this.lyricsSaveStatus) this.lyricsSaveStatus.textContent = "Saved!";
                window.dispatchEvent(new CustomEvent('flexioke:lyrics-updated', {
                    detail: {
                        job_id: this.activeLyricsJobId,
                        lyrics: text,
                        has_timestamps: data.has_timestamps,
                        title: newTitle,
                        artist: newArtist
                    }
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
        this.queueContainers = document.querySelectorAll('.queue-list-container');
        this.queueCountBadges = document.querySelectorAll('.queue-count-badge');
        this.clearBtns = document.querySelectorAll('.clear-queue-btn');
        this.playNextBtns = document.querySelectorAll('.play-next-queue-btn');
        this.isAdvancing = false;
        this.queue = [];
        this.state = { queue: [], current_track: null, history: [] };

        this.init();
    }

    init() {
        this.clearBtns.forEach(btn => {
            btn.addEventListener('click', () => this.clearQueue());
        });

        this.playNextBtns.forEach(btn => {
            btn.addEventListener('click', () => this.advanceNext(true));
        });

        // Handle auto-advance when a track finishes
        window.addEventListener('flexioke:track-ended', () => {
            console.log("Track ended event received, triggering auto-advance...");
            this.advanceNext(true);
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

    async stopAndCueNext() {
        if (window.flexiokePlayer) {
            window.flexiokePlayer.pause();
        }
        // Advance queue with autoPlay = false
        await this.advanceNext(false);
    }

    async advanceNext(autoPlay = true) {
        if (this.isAdvancing) return;
        this.isAdvancing = true;

        try {
            const resp = await fetch('/api/queue/next', { method: 'POST' });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
                if (state.current_track && window.flexiokePlayer) {
                    window.flexiokePlayer.loadSong(state.current_track, autoPlay);
                } else if (!state.current_track && window.flexiokePlayer) {
                    // No more queued songs: display No Track Selected / default view
                    window.flexiokePlayer.resetToDefault();
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

    async reorderItem(queueId, direction) {
        try {
            const resp = await fetch('/api/queue/reorder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ queue_id: queueId, direction })
            });
            if (resp.ok) {
                const state = await resp.json();
                this.render(state);
            }
        } catch (err) {
            console.error("Error reordering queue:", err);
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
        this.state = state || { queue: [], current_track: null, history: [] };
        this.queue = this.state.queue || [];
        const queue = this.queue;

        window.dispatchEvent(new CustomEvent('flexioke:queue-updated', { detail: this.state }));

        const count = queue.length;
        this.queueCountBadges.forEach(badge => {
            badge.textContent = `${count} ${count === 1 ? 'song' : 'songs'}`;
        });

        this.queueContainers.forEach(container => {
            if (queue.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-6 text-slate-500 text-xs">
                        Playback queue is empty.<br>Add songs from the library!
                    </div>
                `;
                return;
            }

            container.innerHTML = '';
            queue.forEach((item, index) => {
                const row = document.createElement('div');
                row.className = "p-2.5 bg-surface-950/70 border border-slate-800/80 rounded-xl flex items-center justify-between gap-3 text-xs";

                const isFirst = index === 0;
                const isLast = index === queue.length - 1;

                row.innerHTML = `
                    <div class="flex items-center gap-2.5 truncate min-w-0 flex-1">
                        <span class="w-5 h-5 rounded-full bg-slate-800 text-[10px] text-slate-400 font-bold flex items-center justify-center shrink-0">
                            ${index + 1}
                        </span>
                        <span class="font-medium text-slate-200 truncate">${escapeHtml(item.title)}</span>
                    </div>
                    <div class="flex items-center gap-1 shrink-0">
                        <button class="reorder-up-btn p-1 text-[10px] rounded hover:bg-slate-800 ${isFirst ? 'text-slate-700 cursor-not-allowed' : 'text-slate-400 hover:text-white transition'}" title="Move Up" ${isFirst ? 'disabled' : ''}>
                            ▲
                        </button>
                        <button class="reorder-down-btn p-1 text-[10px] rounded hover:bg-slate-800 ${isLast ? 'text-slate-700 cursor-not-allowed' : 'text-slate-400 hover:text-white transition'}" title="Move Down" ${isLast ? 'disabled' : ''}>
                            ▼
                        </button>
                        <button class="remove-queue-btn text-slate-500 hover:text-rose-400 p-1 text-xs transition" title="Remove from Queue" data-queue-id="${item.queue_id}">
                            ✕
                        </button>
                    </div>
                `;

                const upBtn = row.querySelector('.reorder-up-btn');
                if (!isFirst && upBtn) {
                    upBtn.addEventListener('click', () => this.reorderItem(item.queue_id, 'up'));
                }

                const downBtn = row.querySelector('.reorder-down-btn');
                if (!isLast && downBtn) {
                    downBtn.addEventListener('click', () => this.reorderItem(item.queue_id, 'down'));
                }

                const removeBtn = row.querySelector('.remove-queue-btn');
                removeBtn.addEventListener('click', () => this.removeFromQueue(item.queue_id));

                container.appendChild(row);
            });
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
