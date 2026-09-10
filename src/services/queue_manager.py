import uuid
import threading
from typing import Dict, List, Optional
from src.models import QueueItem, QueueResponse

class QueueManager:
    def __init__(self):
        self._lock = threading.Lock()
        self.current_track: Optional[QueueItem] = None
        self.queue: List[QueueItem] = []

    def add_to_queue(
        self,
        job_id: str,
        title: str,
        artist: Optional[str] = None,
        duration_seconds: Optional[float] = None,
        stems: Optional[Dict[str, str]] = None,
        video_id: str = "bg001.mp4",
        video_offset_seconds: float = 0.0
    ) -> QueueItem:
        """Appends a song to the playback queue."""
        item = QueueItem(
            queue_id=str(uuid.uuid4()),
            job_id=job_id,
            title=title,
            artist=artist,
            duration_seconds=duration_seconds,
            stems=stems or {},
            video_id=video_id or "bg001.mp4",
            video_offset_seconds=float(video_offset_seconds or 0.0)
        )
        with self._lock:
            self.queue.append(item)
        return item

    def play_now(
        self,
        job_id: str,
        title: str,
        artist: Optional[str] = None,
        duration_seconds: Optional[float] = None,
        stems: Optional[Dict[str, str]] = None,
        video_id: str = "bg001.mp4",
        video_offset_seconds: float = 0.0
    ) -> QueueItem:
        """Sets a song as the currently playing track immediately."""
        item = QueueItem(
            queue_id=str(uuid.uuid4()),
            job_id=job_id,
            title=title,
            artist=artist,
            duration_seconds=duration_seconds,
            stems=stems or {},
            video_id=video_id or "bg001.mp4",
            video_offset_seconds=float(video_offset_seconds or 0.0)
        )
        with self._lock:
            self.current_track = item
        return item

    def update_job_metadata(
        self,
        job_id: str,
        title: Optional[str] = None,
        artist: Optional[str] = None,
        video_id: Optional[str] = None,
        video_offset_seconds: Optional[float] = None
    ):
        """Propagates updated song metadata to any queued tracks and the active track."""
        with self._lock:
            if self.current_track and self.current_track.job_id == job_id:
                if title is not None:
                    self.current_track.title = title
                if artist is not None:
                    self.current_track.artist = artist
                if video_id is not None:
                    self.current_track.video_id = video_id
                if video_offset_seconds is not None:
                    self.current_track.video_offset_seconds = float(video_offset_seconds)
            for item in self.queue:
                if item.job_id == job_id:
                    if title is not None:
                        item.title = title
                    if artist is not None:
                        item.artist = artist
                    if video_id is not None:
                        item.video_id = video_id
                    if video_offset_seconds is not None:
                        item.video_offset_seconds = float(video_offset_seconds)

    def advance_next(self) -> Optional[QueueItem]:
        """Dequeues the next item in the queue and sets it as current_track."""
        with self._lock:
            if self.queue:
                self.current_track = self.queue.pop(0)
            else:
                self.current_track = None
            return self.current_track

    def remove_from_queue(self, queue_id: str) -> bool:
        """Removes a specific queued item by its unique queue_id."""
        with self._lock:
            initial_len = len(self.queue)
            self.queue = [item for item in self.queue if item.queue_id != queue_id]
            return len(self.queue) < initial_len

    def remove_jobs_from_queue(self, job_id: str) -> int:
        """Removes all queue items referencing job_id and resets current_track if it matches."""
        with self._lock:
            initial_len = len(self.queue)
            self.queue = [item for item in self.queue if item.job_id != job_id]
            if self.current_track and self.current_track.job_id == job_id:
                self.current_track = None
            return initial_len - len(self.queue)

    def clear_queue(self):
        """Clears all queued tracks."""
        with self._lock:
            self.queue.clear()

    def reorder_queue(self, queue_id: str, direction: str) -> Optional[QueueResponse]:
        """Atomically swaps a queued track up or down."""
        with self._lock:
            idx = next((i for i, item in enumerate(self.queue) if item.queue_id == queue_id), -1)
            if idx == -1:
                return None
            if direction == "up":
                if idx == 0:
                    raise ValueError("Cannot move first item up")
                self.queue[idx], self.queue[idx - 1] = self.queue[idx - 1], self.queue[idx]
            elif direction == "down":
                if idx >= len(self.queue) - 1:
                    raise ValueError("Cannot move last item down")
                self.queue[idx], self.queue[idx + 1] = self.queue[idx + 1], self.queue[idx]
            else:
                raise ValueError(f"Invalid direction: '{direction}'. Must be 'up' or 'down'")

            return QueueResponse(
                current_track=self.current_track,
                queue=list(self.queue),
                total_queued=len(self.queue)
            )

    def get_state(self) -> QueueResponse:
        """Returns the full current queue snapshot."""
        with self._lock:
            return QueueResponse(
                current_track=self.current_track,
                queue=list(self.queue),
                total_queued=len(self.queue)
            )

queue_manager = QueueManager()


