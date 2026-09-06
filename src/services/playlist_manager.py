import json
import uuid
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from src.models import (
    Playlist,
    PlaylistSummary,
    PlaylistDetail,
    JobRecord,
)

class PlaylistManager:
    def __init__(self, data_file: Optional[Path] = None):
        if data_file is None:
            self.data_file = Path(__file__).resolve().parent.parent.parent / "data" / "playlists.json"
        else:
            self.data_file = Path(data_file)
        
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._playlists: Dict[str, Playlist] = {}
        self._load_playlists()

    def _load_playlists(self):
        """Loads playlists from disk into memory cache and ensures favorites exists."""
        with self._lock:
            if self.data_file.exists():
                try:
                    raw_data = json.loads(self.data_file.read_text(encoding="utf-8"))
                    if isinstance(raw_data, dict):
                        for p_id, p_data in raw_data.items():
                            try:
                                self._playlists[p_id] = Playlist.model_validate(p_data)
                            except Exception as e:
                                print(f"[PlaylistManager] Skipping invalid playlist record {p_id}: {e}")
                    elif isinstance(raw_data, list):
                        for p_data in raw_data:
                            try:
                                p = Playlist.model_validate(p_data)
                                self._playlists[p.id] = p
                            except Exception as e:
                                print(f"[PlaylistManager] Skipping invalid playlist record: {e}")
                except Exception as e:
                    print(f"[PlaylistManager] Failed to read {self.data_file}: {e}")

            # Bootstrap Favorites system playlist if not present
            if "favorites" not in self._playlists:
                now_iso = datetime.now(timezone.utc).isoformat()
                self._playlists["favorites"] = Playlist(
                    id="favorites",
                    name="Favorites",
                    description="Your favorite songs",
                    is_system=True,
                    song_ids=[],
                    created_at=now_iso,
                    updated_at=now_iso,
                )
                self._save_playlists()

    def _save_playlists(self):
        """Atomically persists playlists cache to disk."""
        tmp_file = self.data_file.parent / f"playlists.json.tmp.{uuid.uuid4().hex}"
        data = {p_id: p.model_dump() for p_id, p in self._playlists.items()}
        tmp_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp_file.replace(self.data_file)

    def get_all_playlists(self, job_mgr=None) -> List[PlaylistSummary]:
        """Returns summaries of all playlists sorted with system playlists first."""
        with self._lock:
            summaries: List[PlaylistSummary] = []
            for p in self._playlists.values():
                total_duration = 0.0
                if job_mgr:
                    for sid in p.song_ids:
                        job = job_mgr.get_job(sid)
                        if job and job.duration_seconds:
                            total_duration += job.duration_seconds

                summaries.append(
                    PlaylistSummary(
                        id=p.id,
                        name=p.name,
                        description=p.description,
                        is_system=p.is_system,
                        song_count=len(p.song_ids),
                        total_duration_seconds=total_duration,
                        created_at=p.created_at,
                        updated_at=p.updated_at,
                    )
                )

            # Sort: system playlist first, then created_at ascending
            summaries.sort(key=lambda s: (not s.is_system, s.created_at))
            return summaries

    def get_playlist(self, playlist_id: str) -> Optional[Playlist]:
        """Returns raw playlist record by ID."""
        with self._lock:
            return self._playlists.get(playlist_id)

    def get_playlist_detail(self, playlist_id: str, job_mgr=None) -> Optional[PlaylistDetail]:
        """Returns detailed playlist with resolved Job records, auto-pruning orphaned IDs."""
        with self._lock:
            p = self._playlists.get(playlist_id)
            if not p:
                return None

            songs: List[JobRecord] = []
            valid_song_ids: List[str] = []
            total_duration = 0.0

            if job_mgr:
                for sid in p.song_ids:
                    job = job_mgr.get_job(sid)
                    if job is not None:
                        songs.append(job)
                        valid_song_ids.append(sid)
                        if job.duration_seconds:
                            total_duration += job.duration_seconds
                
                # Auto-prune orphaned references if any were removed from disk
                if len(valid_song_ids) != len(p.song_ids):
                    p.song_ids = valid_song_ids
                    p.updated_at = datetime.now(timezone.utc).isoformat()
                    self._save_playlists()
            else:
                valid_song_ids = list(p.song_ids)

            return PlaylistDetail(
                id=p.id,
                name=p.name,
                description=p.description,
                is_system=p.is_system,
                song_count=len(valid_song_ids),
                total_duration_seconds=total_duration,
                songs=songs,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )

    def create_playlist(self, name: str, description: Optional[str] = "") -> Playlist:
        """Creates a new custom playlist."""
        name_clean = name.strip()
        if not name_clean:
            raise ValueError("Playlist name cannot be empty")
        
        with self._lock:
            now_iso = datetime.now(timezone.utc).isoformat()
            p_id = f"pl_{uuid.uuid4().hex[:10]}"
            playlist = Playlist(
                id=p_id,
                name=name_clean,
                description=(description or "").strip(),
                is_system=False,
                song_ids=[],
                created_at=now_iso,
                updated_at=now_iso,
            )
            self._playlists[p_id] = playlist
            self._save_playlists()
            return playlist

    def update_playlist(
        self, playlist_id: str, name: Optional[str] = None, description: Optional[str] = None
    ) -> Optional[Playlist]:
        """Updates metadata for a playlist. Rejects renaming system playlists."""
        with self._lock:
            p = self._playlists.get(playlist_id)
            if not p:
                return None

            if name is not None:
                name_clean = name.strip()
                if not name_clean:
                    raise ValueError("Playlist name cannot be empty")
                if p.is_system and name_clean != p.name:
                    raise ValueError("Cannot rename system playlist")
                p.name = name_clean

            if description is not None:
                p.description = description.strip()

            p.updated_at = datetime.now(timezone.utc).isoformat()
            self._save_playlists()
            return p

    def delete_playlist(self, playlist_id: str) -> bool:
        """Deletes a custom playlist. Rejects deletion of system playlists."""
        with self._lock:
            p = self._playlists.get(playlist_id)
            if not p:
                return False
            if p.is_system:
                raise ValueError("Cannot delete system playlist")

            del self._playlists[playlist_id]
            self._save_playlists()
            return True

    def add_song(self, playlist_id: str, song_id: str, job_mgr=None) -> Playlist:
        """Adds a song ID to a playlist."""
        with self._lock:
            p = self._playlists.get(playlist_id)
            if not p:
                raise KeyError(f"Playlist {playlist_id} not found")

            if job_mgr and job_mgr.get_job(song_id) is None:
                raise KeyError(f"Song not found: {song_id}")

            if song_id in p.song_ids:
                raise ValueError(f"Song {song_id} already exists in playlist")

            p.song_ids.append(song_id)
            p.updated_at = datetime.now(timezone.utc).isoformat()
            self._save_playlists()
            return p

    def remove_song(self, playlist_id: str, song_id: str) -> Playlist:
        """Removes a song ID from a playlist."""
        with self._lock:
            p = self._playlists.get(playlist_id)
            if not p:
                raise KeyError(f"Playlist {playlist_id} not found")

            if song_id not in p.song_ids:
                raise ValueError(f"Song {song_id} not in playlist")

            p.song_ids.remove(song_id)
            p.updated_at = datetime.now(timezone.utc).isoformat()
            self._save_playlists()
            return p

    def reorder_songs(self, playlist_id: str, song_ids: List[str]) -> Playlist:
        """Reorders song IDs in a playlist."""
        with self._lock:
            p = self._playlists.get(playlist_id)
            if not p:
                raise KeyError(f"Playlist {playlist_id} not found")

            if sorted(p.song_ids) != sorted(song_ids) or len(p.song_ids) != len(song_ids):
                raise ValueError("Invalid song reorder list: IDs must match existing playlist songs exactly")

            p.song_ids = list(song_ids)
            p.updated_at = datetime.now(timezone.utc).isoformat()
            self._save_playlists()
            return p

    def create_from_queue(
        self, name: str, song_ids: List[str], description: Optional[str] = "", job_mgr=None
    ) -> Playlist:
        """Creates a new custom playlist from an ordered list of song IDs, filtering duplicates and missing jobs."""
        name_clean = name.strip()
        if not name_clean:
            raise ValueError("Playlist name cannot be empty")

        unique_song_ids: List[str] = []
        seen = set()
        for sid in song_ids:
            if sid not in seen:
                if job_mgr is None or job_mgr.get_job(sid) is not None:
                    seen.add(sid)
                    unique_song_ids.append(sid)

        with self._lock:
            now_iso = datetime.now(timezone.utc).isoformat()
            p_id = f"pl_{uuid.uuid4().hex[:10]}"
            playlist = Playlist(
                id=p_id,
                name=name_clean,
                description=(description or "").strip(),
                is_system=False,
                song_ids=unique_song_ids,
                created_at=now_iso,
                updated_at=now_iso,
            )
            self._playlists[p_id] = playlist
            self._save_playlists()
            return playlist

    def prune_song_from_all_playlists(self, song_id: str) -> int:
        """Prunes a deleted song ID from all playlists."""
        with self._lock:
            pruned_count = 0
            now_iso = datetime.now(timezone.utc).isoformat()
            for p in self._playlists.values():
                if song_id in p.song_ids:
                    p.song_ids = [sid for sid in p.song_ids if sid != song_id]
                    p.updated_at = now_iso
                    pruned_count += 1

            if pruned_count > 0:
                self._save_playlists()

            return pruned_count

# Global singleton
playlist_manager = PlaylistManager()
