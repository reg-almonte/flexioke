import re
import json
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

from src.models import JobRecord, JobStatus, SourceType, LyricsResponse

class JobManager:
    def __init__(self, data_dir: Optional[Path] = None, max_workers: int = 1):
        if data_dir is None:
            self.data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "jobs"
        else:
            self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="separator-worker")
        self._lock = threading.Lock()
        self._cache: Dict[str, JobRecord] = {}
        self._load_existing_jobs()

    def _load_existing_jobs(self):
        """Loads all existing job records from disk into memory cache."""
        with self._lock:
            if not self.data_dir.exists():
                return
            for job_dir in self.data_dir.iterdir():
                if job_dir.is_dir():
                    meta_file = job_dir / "job.json"
                    if meta_file.exists():
                        try:
                            data = json.loads(meta_file.read_text(encoding="utf-8"))
                            record = JobRecord.model_validate(data)
                            self._cache[record.job_id] = record
                        except Exception as e:
                            # Log and skip corrupted job files
                            print(f"[JobManager] Failed to load job metadata from {meta_file}: {e}")

    def _save_job(self, record: JobRecord):
        """Persists a job record to disk and updates in-memory cache."""
        job_dir = self.data_dir / record.job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        meta_file = job_dir / "job.json"
        
        # Atomic write via temporary file
        tmp_file = job_dir / f"job.json.tmp.{uuid.uuid4().hex}"
        record.updated_at = datetime.now(timezone.utc).isoformat()
        tmp_file.write_text(record.model_dump_json(indent=2), encoding="utf-8")
        tmp_file.replace(meta_file)

        with self._lock:
            self._cache[record.job_id] = record

    def get_job_dir(self, job_id: str) -> Path:
        """Returns the base directory Path for a specific job."""
        job_dir = self.data_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        return job_dir

    def create_job(self, source_type: SourceType, source_name: str, title: str, artist: Optional[str] = None) -> JobRecord:
        """Creates a new job record, persists it to disk, and tracks it in cache."""
        job_id = str(uuid.uuid4())
        record = JobRecord(
            job_id=job_id,
            source_type=source_type,
            source_name=source_name,
            title=title,
            artist=artist,
            status=JobStatus.QUEUED,
            progress=0,
            current_stage="Job created, queued for processing"
        )
        self._save_job(record)
        return record

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        """Retrieves a job record from cache, falling back to disk read if necessary."""
        with self._lock:
            if job_id in self._cache:
                return self._cache[job_id]

        meta_file = self.data_dir / job_id / "job.json"
        if meta_file.exists():
            try:
                data = json.loads(meta_file.read_text(encoding="utf-8"))
                record = JobRecord.model_validate(data)
                with self._lock:
                    self._cache[job_id] = record
                return record
            except Exception as e:
                print(f"[JobManager] Failed to read job {job_id}: {e}")
                return None
        return None

    def update_job(self, job_id: str, **kwargs) -> Optional[JobRecord]:
        """Updates specific fields of an existing job and persists to disk."""
        record = self.get_job(job_id)
        if not record:
            return None

        update_data = record.model_dump()
        for k, v in kwargs.items():
            if k in update_data:
                update_data[k] = v

        updated_record = JobRecord.model_validate(update_data)
        self._save_job(updated_record)
        return updated_record

    def list_jobs(self, status: Optional[JobStatus] = None, query: Optional[str] = None) -> List[JobRecord]:
        """Returns filtered list of jobs sorted by creation date descending."""
        with self._lock:
            jobs = list(self._cache.values())

        if status:
            jobs = [j for j in jobs if j.status == status]

        if query:
            q = query.lower().strip()
            jobs = [
                j for j in jobs
                if q in j.title.lower() or q in j.source_name.lower() or (j.artist and q in j.artist.lower())
            ]

        jobs.sort(key=lambda j: j.created_at, reverse=True)
        return jobs

    def get_lyrics(self, job_id: str) -> LyricsResponse:
        """Retrieves the lyrics for a specific job."""
        job_dir = self.get_job_dir(job_id)
        lyrics_file = job_dir / "lyrics.lrc"
        if not lyrics_file.exists():
            return LyricsResponse(
                job_id=job_id,
                lyrics="",
                has_lyrics=False,
                has_timestamps=False
            )

        try:
            content = lyrics_file.read_text(encoding="utf-8")
            has_timestamps = bool(re.search(r"\[\d{2}:\d{2}", content))
            return LyricsResponse(
                job_id=job_id,
                lyrics=content,
                has_lyrics=bool(content.strip()),
                has_timestamps=has_timestamps
            )
        except Exception as e:
            print(f"[JobManager] Error reading lyrics for job {job_id}: {e}")
            return LyricsResponse(
                job_id=job_id,
                lyrics="",
                has_lyrics=False,
                has_timestamps=False
            )

    def save_lyrics(self, job_id: str, lyrics_text: str) -> LyricsResponse:
        """Atomically saves lyrics content to lyrics.lrc for a job."""
        job_dir = self.get_job_dir(job_id)
        lyrics_file = job_dir / "lyrics.lrc"
        tmp_file = job_dir / f"lyrics.lrc.tmp.{uuid.uuid4().hex}"

        tmp_file.write_text(lyrics_text, encoding="utf-8")
        tmp_file.replace(lyrics_file)

        has_timestamps = bool(re.search(r"\[\d{2}:\d{2}", lyrics_text))
        return LyricsResponse(
            job_id=job_id,
            lyrics=lyrics_text,
            has_lyrics=bool(lyrics_text.strip()),
            has_timestamps=has_timestamps
        )

    def submit_task(self, fn: Callable, *args: Any, **kwargs: Any) -> Future:
        """Submits a background job to the bounded executor."""
        return self.executor.submit(fn, *args, **kwargs)

# Global JobManager singleton instance
job_manager = JobManager()
