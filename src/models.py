from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    SEPARATING_STAGE_1 = "separating_stage_1"
    SEPARATING_STAGE_2 = "separating_stage_2"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SourceType(str, Enum):
    UPLOAD = "upload"
    YOUTUBE = "youtube"
    URL = "url"

class JobRecord(BaseModel):
    job_id: str
    source_type: SourceType
    source_name: str
    title: str
    artist: Optional[str] = None
    status: JobStatus = JobStatus.QUEUED
    progress: int = Field(default=0, ge=0, le=100)
    current_stage: str = "Queued"
    error: Optional[str] = None
    duration_seconds: Optional[float] = None
    stems: Dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class JobListResponse(BaseModel):
    total: int
    jobs: List[JobRecord]

class QueueItem(BaseModel):
    queue_id: str
    job_id: str
    title: str
    artist: Optional[str] = None
    duration_seconds: Optional[float] = None
    stems: Dict[str, str] = Field(default_factory=dict)
    added_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class QueueResponse(BaseModel):
    current_track: Optional[QueueItem] = None
    queue: List[QueueItem]
    total_queued: int

class LyricsUpdateRequest(BaseModel):
    lyrics: str

class LyricsResponse(BaseModel):
    job_id: str
    lyrics: str = ""
    has_lyrics: bool = False
    has_timestamps: bool = False

class JobUpdateMetadataRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    artist: Optional[str] = Field(default=None, max_length=200)

class QueueReorderRequest(BaseModel):
    queue_id: str
    direction: str = Field(..., description="'up' or 'down'")

class AudioUrlRequest(BaseModel):
    url: str = Field(..., description="Direct HTTP or HTTPS URL to audio file")


