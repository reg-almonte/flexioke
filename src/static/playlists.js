/**
 * Flexioke — Playlists & Favorites Client State Machine
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
        const icon = isFav ? '♥' : '♡';
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
            btn.textContent = isFav ? '♥' : '♡';

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
            if (songId) {
                const isFav = this.isFavorite(songId);
                this.updateHeartButtonsForSong(songId, isFav);
            }
        });
    }
}

// Global Singletons
window.flexiokeFavorites = new FavoritesManager();
window.flexiokeFavoritesSet = window.flexiokeFavorites.favoritesSet;
