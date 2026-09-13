/**
 * Flexioke — Playlists & Favorites Client State Machine (Dual-Page Sync)
 */

class FavoritesManager {
    constructor() {
        this.favoritesSet = new Set();
        this.isFetching = false;
        this.init();
    }

    init() {
        // Listen for favorite toggled events to update DOM elements
        window.addEventListener('flexioke:favorites-toggled', (e) => {
            const { song_id, is_favorite } = e.detail || {};
            if (song_id) {
                this.updateHeartButtonsForSong(song_id, is_favorite);
            }
        });

        // Prune deleted jobs from local state
        window.addEventListener('flexioke:job-deleted', (e) => {
            const { job_id } = e.detail || {};
            if (job_id && this.favoritesSet.has(job_id)) {
                this.favoritesSet.delete(job_id);
                window.flexiokeFavoritesSet = this.favoritesSet;
                window.dispatchEvent(new CustomEvent('flexioke:playlists-updated'));
            }
        });

        // Initial fetch
        this.fetchFavorites();
    }

    async fetchFavorites() {
        if (this.isFetching) return;
        this.isFetching = true;
        try {
            const resp = await fetch('/api/playlists/favorites');
            if (resp.ok) {
                const data = await resp.json();
                const songs = data.songs || [];
                this.favoritesSet = new Set(songs.map(s => s.job_id));
                window.flexiokeFavoritesSet = this.favoritesSet;
                this.updateAllHeartButtons();
                window.dispatchEvent(new CustomEvent('flexioke:favorites-loaded', {
                    detail: { favorites: Array.from(this.favoritesSet) }
                }));
            }
        } catch (err) {
            console.error("[FavoritesManager] Error fetching favorites:", err);
        } finally {
            this.isFetching = false;
        }
    }

    isFavorite(songId) {
        return this.favoritesSet.has(songId);
    }

    getFavoriteIds() {
        return Array.from(this.favoritesSet);
    }

    async toggleFavorite(songId) {
        if (!songId) return;
        const isFav = this.favoritesSet.has(songId);
        const nextState = !isFav;

        // 1. Optimistic Update
        if (nextState) {
            this.favoritesSet.add(songId);
        } else {
            this.favoritesSet.delete(songId);
        }
        window.flexiokeFavoritesSet = this.favoritesSet;
        window.dispatchEvent(new CustomEvent('flexioke:favorites-toggled', {
            detail: { song_id: songId, is_favorite: nextState }
        }));

        // 2. Dispatch REST API call
        try {
            let resp;
            if (nextState) {
                resp = await fetch('/api/playlists/favorites/songs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ song_id: songId })
                });
            } else {
                resp = await fetch(`/api/playlists/favorites/songs/${encodeURIComponent(songId)}`, {
                    method: 'DELETE'
                });
            }

            if (!resp.ok) {
                throw new Error(`API returned status ${resp.status}`);
            }

            window.dispatchEvent(new CustomEvent('flexioke:playlists-updated'));
        } catch (err) {
            console.error("[FavoritesManager] Failed to toggle favorite for", songId, err);
            // Rollback optimistic update
            if (isFav) {
                this.favoritesSet.add(songId);
            } else {
                this.favoritesSet.delete(songId);
            }
            window.flexiokeFavoritesSet = this.favoritesSet;
            window.dispatchEvent(new CustomEvent('flexioke:favorites-toggled', {
                detail: { song_id: songId, is_favorite: isFav }
            }));
        }
    }

    renderHeartButtonHtml(songId, extraClasses = '') {
        const isFav = this.isFavorite(songId);
        const icon = window.getIconHtml ? window.getIconHtml(isFav ? 'heart_filled' : 'heart_outline', 'w-4 h-4') : (isFav ? '♥' : '♡');
        const title = isFav ? 'Remove from Favorites' : 'Add to Favorites';
        const colorClass = isFav ? 'text-rose-500' : 'text-slate-500 hover:text-rose-400';
        return `<button type="button" class="favorite-toggle-btn p-1 text-sm ${colorClass} hover:scale-110 active:scale-95 transition-all duration-150 ${extraClasses}" title="${title}" aria-label="${title}" data-job-id="${songId}" data-favorite="${isFav ? 'true' : 'false'}">${icon}</button>`;
    }

    updateHeartButtonsForSong(songId, isFav) {
        const buttons = document.querySelectorAll(`.favorite-toggle-btn[data-job-id="${songId}"]`);
        buttons.forEach(btn => {
            btn.setAttribute('data-favorite', isFav ? 'true' : 'false');
            const title = isFav ? 'Remove from Favorites' : 'Add to Favorites';
            btn.setAttribute('title', title);
            btn.setAttribute('aria-label', title);
            if (window.getIconHtml) {
                btn.innerHTML = window.getIconHtml(isFav ? 'heart_filled' : 'heart_outline', 'w-4 h-4');
            } else {
                btn.textContent = isFav ? '♥' : '♡';
            }

            if (isFav) {
                btn.classList.remove('text-slate-500', 'hover:text-rose-400');
                btn.classList.add('text-rose-500');
            } else {
                btn.classList.remove('text-rose-500');
                btn.classList.add('text-slate-500', 'hover:text-rose-400');
            }
        });
    }

    updateAllHeartButtons() {
        const buttons = document.querySelectorAll('.favorite-toggle-btn[data-job-id]');
        buttons.forEach(btn => {
            const songId = btn.getAttribute('data-job-id');
            const isFav = this.isFavorite(songId);
            btn.setAttribute('data-favorite', isFav ? 'true' : 'false');
            const title = isFav ? 'Remove from Favorites' : 'Add to Favorites';
            btn.setAttribute('title', title);
            btn.setAttribute('aria-label', title);
            if (window.getIconHtml) {
                btn.innerHTML = window.getIconHtml(isFav ? 'heart_filled' : 'heart_outline', 'w-4 h-4');
            } else {
                btn.textContent = isFav ? '♥' : '♡';
            }

            if (isFav) {
                btn.classList.remove('text-slate-500', 'hover:text-rose-400');
                btn.classList.add('text-rose-500');
            } else {
                btn.classList.remove('text-rose-500');
                btn.classList.add('text-slate-500', 'hover:text-rose-400');
            }
        });
    }
}

class PlaylistsManager {
    constructor() {
        this.playlists = [];
        this.activePlaylistDetail = null;
        this.activePlaylistQuery = '';
        this.activeLyricsJobId = null;

        // Stem Studio Elements
        this.studioCountBadge = document.getElementById('studio-playlists-count-badge');
        this.studioCreateBtn = document.getElementById('studio-create-playlist-btn');
        this.studioListContainer = document.getElementById('studio-playlists-list');
        this.studioDirectoryView = document.getElementById('studio-playlists-directory-view');
        this.studioDetailView = document.getElementById('studio-playlist-detail-view');
        this.studioActiveName = document.getElementById('studio-active-playlist-name');
        this.studioBackBtn = document.getElementById('studio-playlist-back-btn');
        this.studioQueueAllBtn = document.getElementById('studio-playlist-queue-all-btn');
        this.studioSearchInput = document.getElementById('studio-playlist-search-input');
        this.studioSongsList = document.getElementById('studio-playlist-songs-list');

        // Karaoke Mode Elements
        this.karaokeCountBadge = document.getElementById('karaoke-playlists-count-badge');
        this.karaokeListContainer = document.getElementById('karaoke-playlists-list');

        // Queue-to-Playlist Elements
        this.saveQueueBtns = document.querySelectorAll('.save-queue-playlist-btn, #studio-save-queue-playlist-btn, #karaoke-save-queue-playlist-btn');

        // Lyrics Modal Elements
        this.lyricsModalPlaylistsContainer = document.getElementById('lyrics-modal-playlists-container');
        this.lyricsModalFeedback = document.getElementById('lyrics-modal-playlist-feedback');

        this.init();
    }

    init() {
        if (this.studioCreateBtn) {
            this.studioCreateBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.promptCreatePlaylist();
            });
        }

        if (this.studioBackBtn) {
            this.studioBackBtn.addEventListener('click', () => {
                this.closePlaylistDetail();
            });
        }

        if (this.studioQueueAllBtn) {
            this.studioQueueAllBtn.addEventListener('click', async () => {
                if (!this.activePlaylistDetail || !this.activePlaylistDetail.songs) return;
                const songIds = this.activePlaylistDetail.songs.map(s => s.job_id);
                if (songIds.length > 0 && window.flexiokeQueue) {
                    this.studioQueueAllBtn.disabled = true;
                    for (const id of songIds) {
                        await window.flexiokeQueue.addToQueue(id);
                    }
                    this.studioQueueAllBtn.textContent = '✓ Queued All';
                    setTimeout(() => {
                        if (this.studioQueueAllBtn) {
                            this.studioQueueAllBtn.textContent = '➕ Queue All';
                            this.studioQueueAllBtn.disabled = false;
                        }
                    }, 1200);
                }
            });
        }

        if (this.studioSearchInput) {
            this.studioSearchInput.addEventListener('input', (e) => {
                this.activePlaylistQuery = e.target.value.trim().toLowerCase();
                this.renderActivePlaylistSongs();
            });
        }

        // Wire Save Queue as Playlist buttons
        this.saveQueueBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.saveQueueAsPlaylist();
            });
        });

        // Listen for queue state updates to toggle Save Queue button disabled state
        window.addEventListener('flexioke:queue-updated', (e) => {
            const queue = e.detail?.queue || [];
            const hasSongs = queue.length > 0;
            this.saveQueueBtns.forEach(btn => {
                btn.disabled = !hasSongs;
            });
        });

        window.addEventListener('flexioke:playlists-updated', () => {
            this.fetchPlaylists();
        });

        window.addEventListener('flexioke:job-deleted', () => {
            this.fetchPlaylists();
        });

        // Initial fetch
        this.fetchPlaylists();
    }

    async fetchPlaylists() {
        try {
            const resp = await fetch('/api/playlists');
            if (resp.ok) {
                this.playlists = await resp.json();
                window.flexiokePlaylists = this.playlists;
                this.renderStudioDirectory();
                this.renderKaraokePlaylists();
                
                if (this.activePlaylistDetail) {
                    this.fetchPlaylistDetail(this.activePlaylistDetail.id);
                }
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error fetching playlists:", err);
        }
    }

    async fetchPlaylistDetail(playlistId) {
        try {
            const resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}`);
            if (resp.ok) {
                this.activePlaylistDetail = await resp.json();
                this.renderActivePlaylistSongs();
            } else if (resp.status === 404) {
                this.closePlaylistDetail();
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error fetching playlist detail:", err);
        }
    }

    renderStudioDirectory() {
        if (this.studioCountBadge) {
            this.studioCountBadge.textContent = String(this.playlists.length);
        }

        if (!this.studioListContainer) return;

        if (this.playlists.length === 0) {
            this.studioListContainer.innerHTML = `
                <div class="text-center py-6 text-slate-500 text-xs">
                    No playlists created yet.<br>Click "+ New" to create one!
                </div>
            `;
            return;
        }

        this.studioListContainer.innerHTML = '';
        this.playlists.forEach(pl => {
            const card = document.createElement('div');
            card.className = "p-2.5 bg-surface-950/80 hover:bg-slate-800/80 border border-slate-800/80 hover:border-brand-500/40 rounded-xl transition flex items-center justify-between gap-2.5 group cursor-pointer";
            
            const icon = pl.is_system ? '❤️' : '📁';
            const durationFmt = pl.total_duration_seconds ? `${Math.floor(pl.total_duration_seconds / 60)}:${String(Math.floor(pl.total_duration_seconds % 60)).padStart(2, '0')}` : '0:00';
            const countStr = `${pl.song_count} ${pl.song_count === 1 ? 'song' : 'songs'}`;

            let deleteBtnHtml = '';
            if (!pl.is_system) {
                deleteBtnHtml = `
                    <button class="delete-pl-btn p-1 text-slate-500 hover:text-rose-400 text-xs transition" title="Delete Playlist" data-pl-id="${pl.id}" data-pl-name="${escapeHtml(pl.name)}">
                        🗑
                    </button>
                `;
            }

            card.innerHTML = `
                <div class="flex items-center gap-2.5 min-w-0 flex-1">
                    <span class="text-base">${icon}</span>
                    <div class="truncate">
                        <div class="flex items-center gap-1.5">
                            <h4 class="text-xs font-semibold text-slate-200 truncate group-hover:text-brand-300 transition">${escapeHtml(pl.name)}</h4>
                            ${pl.is_system ? '<span class="text-[9px] px-1 rounded bg-rose-950/80 text-rose-300 border border-rose-800/50">System</span>' : ''}
                        </div>
                        <div class="text-[10px] text-slate-400 flex items-center gap-1.5">
                            <span>${countStr}</span>
                            <span>•</span>
                            <span>${durationFmt}</span>
                        </div>
                    </div>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                    <button class="view-pl-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-[10px] font-medium transition" data-pl-id="${pl.id}">
                        View
                    </button>
                    ${deleteBtnHtml}
                </div>
            `;

            card.addEventListener('click', (e) => {
                if (e.target.closest('button')) return;
                this.openPlaylistDetail(pl.id);
            });

            const viewBtn = card.querySelector('.view-pl-btn');
            if (viewBtn) {
                viewBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.openPlaylistDetail(pl.id);
                });
            }

            const deleteBtn = card.querySelector('.delete-pl-btn');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.promptDeletePlaylist(pl.id, pl.name);
                });
            }

            this.studioListContainer.appendChild(card);
        });
    }

    renderKaraokePlaylists() {
        if (this.karaokeCountBadge) {
            this.karaokeCountBadge.textContent = String(this.playlists.length);
        }

        if (!this.karaokeListContainer) return;

        if (this.playlists.length === 0) {
            this.karaokeListContainer.innerHTML = `
                <div class="text-center py-6 text-slate-500 text-xs">
                    No playlists available.<br>Create one in Stem Studio!
                </div>
            `;
            return;
        }

        this.karaokeListContainer.innerHTML = '';
        this.playlists.forEach(pl => {
            const card = document.createElement('div');
            card.className = "p-3 bg-surface-950/80 border border-slate-800/80 hover:border-brand-500/40 rounded-xl transition flex flex-col gap-2.5 group";

            const icon = pl.is_system ? '❤️' : '📁';
            const durationFmt = pl.total_duration_seconds ? `${Math.floor(pl.total_duration_seconds / 60)}:${String(Math.floor(pl.total_duration_seconds % 60)).padStart(2, '0')}` : '0:00';
            const countStr = `${pl.song_count} ${pl.song_count === 1 ? 'song' : 'songs'}`;
            const isEmpty = pl.song_count === 0;

            card.innerHTML = `
                <div class="flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2 min-w-0 flex-1">
                        <span class="text-sm">${icon}</span>
                        <div class="truncate">
                            <div class="flex items-center gap-1.5">
                                <h4 class="text-xs font-semibold text-slate-200 truncate group-hover:text-brand-300 transition">${escapeHtml(pl.name)}</h4>
                                ${pl.is_system ? '<span class="text-[9px] px-1 rounded bg-rose-950/80 text-rose-300 border border-rose-800/50">System</span>' : ''}
                            </div>
                            <div class="text-[10px] text-slate-400 flex items-center gap-1.5">
                                <span>${countStr}</span>
                                <span>•</span>
                                <span>${durationFmt}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3-Way Dispatch Toolbar -->
                <div class="grid grid-cols-3 gap-1.5 pt-1 border-t border-slate-800/60 text-[10px]">
                    <button class="karaoke-queue-order-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition flex items-center justify-center gap-1 ${isEmpty ? 'opacity-40 cursor-not-allowed' : ''}" title="Append all songs in order to queue" ${isEmpty ? 'disabled' : ''}>
                        <span>${window.getIconHtml ? window.getIconHtml('queue', 'w-3 h-3') : '➕'}</span> In Order
                    </button>
                    <button class="karaoke-queue-shuffle-btn px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition flex items-center justify-center gap-1 ${isEmpty ? 'opacity-40 cursor-not-allowed' : ''}" title="Append all songs shuffled to queue" ${isEmpty ? 'disabled' : ''}>
                        <span>${window.getIconHtml ? window.getIconHtml('refresh', 'w-3 h-3') : '🔀'}</span> Shuffle
                    </button>
                    <button class="karaoke-play-now-btn px-2 py-1 rounded-lg bg-brand-600/80 hover:bg-brand-500 text-white font-semibold transition flex items-center justify-center gap-1 ${isEmpty ? 'opacity-40 cursor-not-allowed' : ''}" title="Clear queue, play first track, and enqueue remainder" ${isEmpty ? 'disabled' : ''}>
                        <span>${window.getIconHtml ? window.getIconHtml('play', 'w-3 h-3') : '▶'}</span> Play Now
                    </button>
                </div>
            `;

            const orderBtn = card.querySelector('.karaoke-queue-order-btn');
            if (orderBtn && !isEmpty) {
                orderBtn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    await this.dispatchPlaylistQueue(pl.id, 'in_order', orderBtn);
                });
            }

            const shuffleBtn = card.querySelector('.karaoke-queue-shuffle-btn');
            if (shuffleBtn && !isEmpty) {
                shuffleBtn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    await this.dispatchPlaylistQueue(pl.id, 'shuffle', shuffleBtn);
                });
            }

            const playNowBtn = card.querySelector('.karaoke-play-now-btn');
            if (playNowBtn && !isEmpty) {
                playNowBtn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    await this.dispatchPlaylistQueue(pl.id, 'play_now', playNowBtn);
                });
            }

            this.karaokeListContainer.appendChild(card);
        });
    }

    async dispatchPlaylistQueue(playlistId, mode = 'in_order', triggerBtn = null) {
        if (!window.flexiokeQueue) return;

        let songIds = [];
        try {
            const resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}`);
            if (resp.ok) {
                const detail = await resp.json();
                const songs = detail.songs || [];
                songIds = detail.song_ids || songs.map(s => s.job_id);
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error fetching playlist details for dispatch:", err);
            return;
        }

        if (songIds.length === 0) {
            alert("This playlist has no songs.");
            return;
        }

        if (triggerBtn) {
            triggerBtn.disabled = true;
        }

        try {
            if (mode === 'in_order') {
                for (const songId of songIds) {
                    await window.flexiokeQueue.addToQueue(songId);
                }
            } else if (mode === 'shuffle') {
                const shuffled = [...songIds];
                for (let i = shuffled.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
                }
                for (const songId of shuffled) {
                    await window.flexiokeQueue.addToQueue(songId);
                }
            } else if (mode === 'play_now') {
                // Clear existing queue
                await window.flexiokeQueue.clearQueue();
                // Play first song
                await window.flexiokeQueue.playNow(songIds[0]);
                // Enqueue remaining songs
                for (const songId of songIds.slice(1)) {
                    await window.flexiokeQueue.addToQueue(songId);
                }
            }
        } finally {
            if (triggerBtn) {
                triggerBtn.disabled = false;
            }
        }
    }

    async saveQueueAsPlaylist() {
        if (!window.flexiokeQueue) return;
        const queueItems = window.flexiokeQueue.queue || [];
        const songIds = queueItems.map(item => item.job_id).filter(Boolean);

        if (songIds.length === 0) {
            alert("Playback queue is empty.");
            return;
        }

        const name = window.prompt(`Save ${songIds.length} queued song(s) as new playlist:\nEnter playlist name:`);
        if (!name || !name.trim()) return;

        const description = window.prompt("Enter playlist description (optional):") || "";

        try {
            const resp = await fetch('/api/playlists/from-queue', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: name.trim(),
                    description: description.trim(),
                    song_ids: songIds
                })
            });

            if (resp.ok) {
                const newPl = await resp.json();
                await this.fetchPlaylists();
                window.dispatchEvent(new CustomEvent('flexioke:playlists-updated'));
                alert(`✓ Playlist "${newPl.name}" created with ${songIds.length} song(s)!`);
            } else {
                const err = await resp.json();
                alert(`Failed to create playlist: ${err.detail || 'Unknown error'}`);
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error saving queue as playlist:", err);
            alert("Network error while saving playlist from queue.");
        }
    }

    openPlaylistDetail(playlistId) {
        if (this.studioDirectoryView) this.studioDirectoryView.classList.add('hidden');
        if (this.studioDetailView) this.studioDetailView.classList.remove('hidden');
        if (this.studioSearchInput) this.studioSearchInput.value = '';
        this.activePlaylistQuery = '';

        const summary = this.playlists.find(p => p.id === playlistId);
        if (summary && this.studioActiveName) {
            this.studioActiveName.textContent = summary.name;
        }

        this.fetchPlaylistDetail(playlistId);
    }

    closePlaylistDetail() {
        this.activePlaylistDetail = null;
        if (this.studioDetailView) this.studioDetailView.classList.add('hidden');
        if (this.studioDirectoryView) this.studioDirectoryView.classList.remove('hidden');
    }

    renderActivePlaylistSongs() {
        if (!this.studioSongsList || !this.activePlaylistDetail) return;

        const songs = this.activePlaylistDetail.songs || [];
        const query = this.activePlaylistQuery;

        let filtered = songs;
        if (query) {
            filtered = songs.filter(s => 
                (s.title || '').toLowerCase().includes(query) || 
                (s.artist || '').toLowerCase().includes(query)
            );
        }

        if (this.studioActiveName) {
            const countStr = `${songs.length} ${songs.length === 1 ? 'song' : 'songs'}`;
            this.studioActiveName.textContent = `${this.activePlaylistDetail.name} (${countStr})`;
        }

        if (filtered.length === 0) {
            this.studioSongsList.innerHTML = `
                <div class="text-center py-5 text-slate-500 text-xs">
                    ${query ? 'No matching songs in playlist.' : 'Playlist has no songs.<br>Add songs using the heart (♥) or song editor modal.'}
                </div>
            `;
            return;
        }

        this.studioSongsList.innerHTML = '';
        filtered.forEach((song, idx) => {
            const row = document.createElement('div');
            row.className = "p-2 bg-surface-950 border border-slate-800 rounded-lg flex items-center justify-between gap-2 text-xs hover:border-slate-700 transition";

            const isFirst = idx === 0;
            const isLast = idx === filtered.length - 1;
            const durationFmt = song.duration_seconds ? `${Math.floor(song.duration_seconds / 60)}:${String(Math.floor(song.duration_seconds % 60)).padStart(2, '0')}` : '';

            const sideAbBadge = song.source_type === 'side_ab' ? '<span class="px-1.5 py-0.5 rounded text-[8px] font-bold bg-violet-950/60 text-violet-400 border border-violet-800/60">Side A/B</span>' : '';

            row.innerHTML = `
                <div class="flex items-center gap-2 truncate min-w-0 flex-1">
                    <span class="text-[10px] text-slate-500 font-mono w-4 shrink-0 text-center">${idx + 1}</span>
                    <div class="truncate">
                        <p class="font-medium text-slate-200 truncate">${escapeHtml(song.title)}</p>
                        <p class="text-[10px] text-slate-400 truncate flex items-center gap-1.5">
                            <span>${escapeHtml(song.artist || 'Unknown Artist')} ${durationFmt ? '• ' + durationFmt : ''}</span>
                            ${sideAbBadge}
                        </p>
                    </div>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                    <button class="pl-play-btn p-1 text-[10px] rounded bg-brand-600/80 hover:bg-brand-500 text-white transition flex items-center justify-center" title="Play Now" data-job-id="${song.job_id}">
                        ${window.getIconHtml ? window.getIconHtml('play', 'w-3 h-3') : '▶'}
                    </button>
                    <button class="pl-reorder-up-btn p-1 text-[10px] rounded hover:bg-slate-800 flex items-center justify-center ${isFirst || query ? 'text-slate-700 cursor-not-allowed' : 'text-slate-400 hover:text-white transition'}" title="Move Up" ${isFirst || query ? 'disabled' : ''}>
                        ${window.getIconHtml ? window.getIconHtml('chevron_up', 'w-3 h-3') : '▲'}
                    </button>
                    <button class="pl-reorder-down-btn p-1 text-[10px] rounded hover:bg-slate-800 flex items-center justify-center ${isLast || query ? 'text-slate-700 cursor-not-allowed' : 'text-slate-400 hover:text-white transition'}" title="Move Down" ${isLast || query ? 'disabled' : ''}>
                        ${window.getIconHtml ? window.getIconHtml('chevron_down', 'w-3 h-3') : '▼'}
                    </button>
                    <button class="pl-remove-song-btn text-slate-500 hover:text-rose-400 p-1 text-xs transition flex items-center justify-center" title="Remove from playlist" data-song-id="${song.job_id}">
                        ${window.getIconHtml ? window.getIconHtml('close', 'w-3.5 h-3.5') : '✕'}
                    </button>
                </div>
            `;

            const playBtn = row.querySelector('.pl-play-btn');
            if (playBtn) {
                playBtn.addEventListener('click', () => {
                    if (window.flexiokeLibrary) {
                        window.flexiokeLibrary.handlePlay(song);
                    }
                });
            }

            const upBtn = row.querySelector('.pl-reorder-up-btn');
            if (upBtn && !isFirst && !query) {
                upBtn.addEventListener('click', () => {
                    const songIds = songs.map(s => s.job_id);
                    const originalIdx = songIds.indexOf(song.job_id);
                    if (originalIdx > 0) {
                        const temp = songIds[originalIdx - 1];
                        songIds[originalIdx - 1] = songIds[originalIdx];
                        songIds[originalIdx] = temp;
                        this.reorderPlaylistSongs(this.activePlaylistDetail.id, songIds);
                    }
                });
            }

            const downBtn = row.querySelector('.pl-reorder-down-btn');
            if (downBtn && !isLast && !query) {
                downBtn.addEventListener('click', () => {
                    const songIds = songs.map(s => s.job_id);
                    const originalIdx = songIds.indexOf(song.job_id);
                    if (originalIdx !== -1 && originalIdx < songIds.length - 1) {
                        const temp = songIds[originalIdx + 1];
                        songIds[originalIdx + 1] = songIds[originalIdx];
                        songIds[originalIdx] = temp;
                        this.reorderPlaylistSongs(this.activePlaylistDetail.id, songIds);
                    }
                });
            }

            const removeBtn = row.querySelector('.pl-remove-song-btn');
            if (removeBtn) {
                removeBtn.addEventListener('click', () => {
                    this.removeSongFromPlaylist(this.activePlaylistDetail.id, song.job_id);
                });
            }

            this.studioSongsList.appendChild(row);
        });
    }

    async promptCreatePlaylist() {
        const name = window.prompt("Enter new playlist name:");
        if (!name || !name.trim()) return;
        const desc = window.prompt("Enter playlist description (optional):") || "";
        await this.createPlaylist(name.trim(), desc.trim());
    }

    async createPlaylist(name, description = '') {
        try {
            const resp = await fetch('/api/playlists', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description })
            });
            if (resp.ok) {
                const newPl = await resp.json();
                await this.fetchPlaylists();
                this.openPlaylistDetail(newPl.id);
            } else {
                const err = await resp.json();
                alert(`Failed to create playlist: ${err.detail || 'Unknown error'}`);
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error creating playlist:", err);
            alert("Network error while creating playlist.");
        }
    }

    async promptDeletePlaylist(playlistId, playlistName) {
        const confirmed = window.confirm(`Are you sure you want to delete the playlist "${playlistName}"? This will not delete the songs from your library.`);
        if (!confirmed) return;
        await this.deletePlaylist(playlistId);
    }

    async deletePlaylist(playlistId) {
        try {
            const resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}`, {
                method: 'DELETE'
            });
            if (resp.ok) {
                if (this.activePlaylistDetail && this.activePlaylistDetail.id === playlistId) {
                    this.closePlaylistDetail();
                }
                await this.fetchPlaylists();
                window.dispatchEvent(new CustomEvent('flexioke:playlists-updated'));
            } else {
                const err = await resp.json();
                alert(`Failed to delete playlist: ${err.detail || 'Unknown error'}`);
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error deleting playlist:", err);
            alert("Network error while deleting playlist.");
        }
    }

    async removeSongFromPlaylist(playlistId, songId) {
        try {
            const resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}/songs/${encodeURIComponent(songId)}`, {
                method: 'DELETE'
            });
            if (resp.ok) {
                this.activePlaylistDetail = await resp.json();
                this.renderActivePlaylistSongs();
                this.fetchPlaylists();
                window.dispatchEvent(new CustomEvent('flexioke:playlists-updated'));
                if (playlistId === 'favorites' && window.flexiokeFavorites) {
                    window.flexiokeFavorites.favoritesSet.delete(songId);
                    window.flexiokeFavoritesSet = window.flexiokeFavorites.favoritesSet;
                    window.flexiokeFavorites.updateHeartButtonsForSong(songId, false);
                }
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error removing song from playlist:", err);
        }
    }

    async reorderPlaylistSongs(playlistId, songIds) {
        try {
            const resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}/reorder`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ song_ids: songIds })
            });
            if (resp.ok) {
                this.activePlaylistDetail = await resp.json();
                this.renderActivePlaylistSongs();
            }
        } catch (err) {
            console.error("[PlaylistsManager] Error reordering playlist:", err);
        }
    }

    async renderLyricsModalPlaylists(songId) {
        this.activeLyricsJobId = songId;
        if (!this.lyricsModalPlaylistsContainer) return;

        this.lyricsModalPlaylistsContainer.innerHTML = `
            <div class="text-slate-500 text-[11px] py-1">Loading playlists...</div>
        `;

        try {
            const resp = await fetch('/api/playlists');
            if (!resp.ok) return;
            const summaries = await resp.json();

            // Fetch details or check inclusion
            const playlistsWithDetails = await Promise.all(
                summaries.map(async (s) => {
                    try {
                        const dResp = await fetch(`/api/playlists/${encodeURIComponent(s.id)}`);
                        if (dResp.ok) return await dResp.json();
                    } catch (e) {}
                    return s;
                })
            );

            this.lyricsModalPlaylistsContainer.innerHTML = '';
            if (playlistsWithDetails.length === 0) {
                this.lyricsModalPlaylistsContainer.innerHTML = `
                    <div class="text-slate-500 text-[11px] py-1">No playlists available.</div>
                `;
                return;
            }

            playlistsWithDetails.forEach(pl => {
                const songs = pl.songs || [];
                const songIds = pl.song_ids || songs.map(s => s.job_id);
                const isMember = songIds.includes(songId);

                const item = document.createElement('label');
                item.className = "flex items-center justify-between p-1.5 rounded-lg hover:bg-slate-800/60 transition cursor-pointer select-none";

                item.innerHTML = `
                    <div class="flex items-center gap-2 truncate">
                        <input type="checkbox" class="playlist-assignment-checkbox rounded bg-surface-900 border-slate-700 text-brand-500 focus:ring-0 cursor-pointer" data-pl-id="${pl.id}" data-pl-name="${escapeHtml(pl.name)}" ${isMember ? 'checked' : ''}>
                        <span class="text-xs font-medium text-slate-200 truncate">${escapeHtml(pl.name)}</span>
                        ${pl.is_system ? '<span class="text-[9px] px-1 rounded bg-rose-950/80 text-rose-300 border border-rose-800/50">System</span>' : ''}
                    </div>
                    <span class="text-[10px] text-slate-500 shrink-0">${songIds.length} ${songIds.length === 1 ? 'song' : 'songs'}</span>
                `;

                const checkbox = item.querySelector('.playlist-assignment-checkbox');
                checkbox.addEventListener('change', async (e) => {
                    const checked = e.target.checked;
                    await this.toggleSongPlaylistMembership(pl.id, pl.name, songId, checked);
                });

                this.lyricsModalPlaylistsContainer.appendChild(item);
            });
        } catch (err) {
            console.error("[PlaylistsManager] Error rendering lyrics modal playlists:", err);
        }
    }

    async toggleSongPlaylistMembership(playlistId, playlistName, songId, add) {
        try {
            let resp;
            if (add) {
                resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}/songs`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ song_id: songId })
                });
            } else {
                resp = await fetch(`/api/playlists/${encodeURIComponent(playlistId)}/songs/${encodeURIComponent(songId)}`, {
                    method: 'DELETE'
                });
            }

            if (resp.ok) {
                this.showLyricsModalFeedback(add ? `✓ Added to "${playlistName}"` : `✓ Removed from "${playlistName}"`);
                window.dispatchEvent(new CustomEvent('flexioke:playlists-updated'));
                if (playlistId === 'favorites' && window.flexiokeFavorites) {
                    if (add) {
                        window.flexiokeFavorites.favoritesSet.add(songId);
                    } else {
                        window.flexiokeFavorites.favoritesSet.delete(songId);
                    }
                    window.flexiokeFavoritesSet = window.flexiokeFavorites.favoritesSet;
                    window.flexiokeFavorites.updateHeartButtonsForSong(songId, add);
                }
            } else {
                const err = await resp.json();
                this.showLyricsModalFeedback(`⚠️ ${err.detail || 'Action failed'}`, true);
            }
        } catch (err) {
            console.error("[PlaylistsManager] Failed to toggle playlist membership:", err);
            this.showLyricsModalFeedback("⚠️ Network error", true);
        }
    }

    showLyricsModalFeedback(msg, isError = false) {
        if (!this.lyricsModalFeedback) return;
        this.lyricsModalFeedback.textContent = msg;
        this.lyricsModalFeedback.className = isError ? "text-[10px] text-rose-400 font-medium" : "text-[10px] text-emerald-400 font-medium";
        if (this.feedbackTimeout) clearTimeout(this.feedbackTimeout);
        this.feedbackTimeout = setTimeout(() => {
            if (this.lyricsModalFeedback) this.lyricsModalFeedback.textContent = '';
        }, 2500);
    }
}

// Global Singletons
document.addEventListener('DOMContentLoaded', () => {
    window.flexiokeFavorites = new FavoritesManager();
    window.flexiokeFavoritesSet = window.flexiokeFavorites.favoritesSet;
    window.flexiokePlaylistsManager = new PlaylistsManager();
});

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

