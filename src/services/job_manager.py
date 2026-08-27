import json
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

from src.models import JobRecord, JobStatus, SourceType

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
                    json_path = job_dir / "job.json"
                    if json_path.exists():
                        try:
                            with open(json_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                record = JobRecord.model_validate(data)
                                self._cache[record.job_id] = record
                        except Exception:
                            # Skip corrupted job folders
                            pass

    def get_job_dir(self, job_id: str) -> Path:
        """Returns the isolated directory for a specific job."""
        return self.data_dir / job_id

    def create_job(self, source_type: SourceType, source_name: str, title: str) -> JobRecord:
        """Creates a new job directory and saves the initial JobRecord."""
        job_id = str(uuid.uuid4())
        job_dir = self.get_job_dir(job_id)
        job_dir.mkdir(parents=True, exist_ok=True)

        record = JobRecord(
            job_id=job_id,
            source_type=source_type,
            source_name=source_name,
            title=title,
            status=JobStatus.QUEUED,
            progress=0,
            current_stage="Queued",
        )

        self._save_job(record)
        return record

    def _save_job(self, record: JobRecord):
        """Serializes the JobRecord to disk and updates in-memory cache."""
        with self._lock:
            record.updated_at = datetime.now(timezone.utc).isoformat()
            self._cache[record.job_id] = record

            job_dir = self.get_job_dir(record.job_id)
            job_dir.mkdir(parents=True, exist_ok=True)
            json_path = job_dir / "job.json"
            temp_path = job_dir / "job.json.tmp"

            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(record.model_dump(), f, indent=2)
            temp_path.replace(json_path)

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        """Retrieves a job by ID from memory cache or disk."""
        with self._lock:
            if job_id in self._cache:
                return self._cache[job_id]

        # Check disk if not in cache
        json_path = self.get_job_dir(job_id) / "job.json"
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    record = JobRecord.model_validate(data)
                    with self._lock:
                        self._cache[job_id] = record
                    return record
            except Exception:
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
            jobs = [j for j in jobs if q in j.title.lower() or q in j.source_name.lower()]

        jobs.sort(key=lambda j: j.created_at, reverse=True)
        return jobs

    def submit_task(self, fn: Callable, *args: Any, **kwargs: Any) -> Future:
        """Submits a background job to the bounded executor."""
        return self.executor.submit(fn, *args, **kwargs)

# Global JobManager singleton instance
job_manager = JobManager()
