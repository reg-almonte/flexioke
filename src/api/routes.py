from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, status
from fastapi.responses import FileResponse

from src.services.job_manager import job_manager
from src.services.queue_manager import queue_manager
from src.services.audio_validator import validate_audio_file, clean_song_title
from src.services.youtube_downloader import validate_youtube_url, download_youtube_audio
from src.services.pipeline import run_separation_pipeline, VALID_STEM_TYPES
from src.models import (
    JobRecord,
    JobListResponse,
    QueueItem,
    QueueResponse,
    LyricsResponse,
    LyricsUpdateRequest,
    SourceType,
    JobStatus,
)

router = APIRouter(prefix="/api", tags=["api"])

class YouTubeRequest(BaseModel):
    url: str = Field(..., description="YouTube video or music link")

class QueueActionRequest(BaseModel):
    job_id: str = Field(..., description="Target Job ID to add or play")

def _handle_youtube_download_and_pipeline(job_id: str, url: str):
    """Background task handler for downloading YouTube audio and triggering separation."""
    job_dir = job_manager.get_job_dir(job_id)
    output_path = job_dir / "input.mp3"
    try:
        job_manager.update_job(
            job_id,
            status=JobStatus.DOWNLOADING,
            progress=5,
            current_stage="Downloading audio from YouTube..."
        )
        info = download_youtube_audio(url, output_path)
        job_manager.update_job(
            job_id,
            title=info["title"],
            duration_seconds=info["duration"],
            status=JobStatus.QUEUED,
            progress=15,
            current_stage="Audio downloaded, starting separation..."
        )
        # Proceed straight to 2-stage separation pipeline
        run_separation_pipeline(job_id)
    except Exception as e:
        job_manager.update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e),
            current_stage="YouTube download failed"
        )

@router.get("/health")
def health_check():
    """Health check endpoint verifying API availability."""
    return {
        "status": "ok",
        "app": "flexioke",
        "version": "0.1.0",
    }

@router.get("/jobs", response_model=JobListResponse)
def list_jobs(
    status: Optional[JobStatus] = Query(default=JobStatus.COMPLETED, description="Filter by job status"),
    q: Optional[str] = Query(default=None, description="Search query for title or source")
):
    """List and search songs in the processed library."""
    jobs = job_manager.list_jobs(status=status, query=q)
    return JobListResponse(total=len(jobs), jobs=jobs)

@router.post("/jobs/upload", status_code=status.HTTP_202_ACCEPTED, response_model=JobRecord)
async def upload_audio(file: UploadFile = File(...)):
    """Upload an audio file to initiate stem separation."""
    filename = file.filename or "uploaded_audio.mp3"
    
    # Read file content into memory/spool
    content = await file.read()
    file_size = len(content)

    is_valid, error_msg = validate_audio_file(filename, file_size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    title = clean_song_title(filename)
    job = job_manager.create_job(
        source_type=SourceType.UPLOAD,
        source_name=filename,
        title=title
    )

    # Save uploaded audio file into job directory
    ext = Path(filename).suffix.lower()
    job_dir = job_manager.get_job_dir(job.job_id)
    input_path = job_dir / f"input{ext}"
    input_path.write_bytes(content)

    # Enqueue separation pipeline in worker pool
    job_manager.submit_task(run_separation_pipeline, job.job_id)

    return job

@router.post("/jobs/youtube", status_code=status.HTTP_202_ACCEPTED, response_model=JobRecord)
def submit_youtube(req: YouTubeRequest):
    """Submit a YouTube URL for audio extraction and stem separation."""
    is_valid, error_msg = validate_youtube_url(req.url)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    job = job_manager.create_job(
        source_type=SourceType.YOUTUBE,
        source_name=req.url.strip(),
        title="YouTube Audio Track"
    )

    # Dispatch background download and separation pipeline
    job_manager.submit_task(_handle_youtube_download_and_pipeline, job.job_id, req.url.strip())

    return job

@router.get("/jobs/{job_id}", response_model=JobRecord)
def get_job_status(job_id: str):
    """Retrieve current processing status and metadata for a given job."""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )
    return job

@router.get("/jobs/{job_id}/stems/{stem_type}")
def get_stem_audio(job_id: str, stem_type: str):
    """Streams an isolated MP3 stem track (instrumental, lead_vocals, backing_vocals)."""
    stem_type_clean = stem_type.lower().strip()
    if stem_type_clean not in VALID_STEM_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stem type '{stem_type}'. Allowed: {', '.join(sorted(VALID_STEM_TYPES))}."
        )

    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )

    job_dir = job_manager.get_job_dir(job_id)
    stem_file = job_dir / f"{stem_type_clean}.mp3"
    if not stem_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stem '{stem_type_clean}' is not yet available for job '{job_id}'."
        )

    return FileResponse(
        path=str(stem_file),
        media_type="audio/mpeg",
        filename=f"{stem_type_clean}.mp3"
    )

# --- Lyrics Endpoints ---

@router.get("/jobs/{job_id}/lyrics", response_model=LyricsResponse)
def get_song_lyrics(job_id: str):
    """Retrieve lyrics text and timestamp metadata for a song."""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )
    return job_manager.get_lyrics(job_id)

@router.post("/jobs/{job_id}/lyrics", response_model=LyricsResponse)
def save_song_lyrics(job_id: str, req: LyricsUpdateRequest):
    """Save or update lyrics (.lrc or plain text) for a song."""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )
    return job_manager.save_lyrics(job_id, req.lyrics)

# --- Playback Queue Endpoints ---

@router.get("/queue", response_model=QueueResponse)
def get_queue():
    """Retrieve current playback queue state."""
    return queue_manager.get_state()

@router.post("/queue/add", response_model=QueueResponse)
def add_to_queue(req: QueueActionRequest):
    """Add a completed song to the playback queue."""
    job = job_manager.get_job(req.job_id)
    if not job or job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job '{req.job_id}' is not ready for playback."
        )
    queue_manager.add_to_queue(job.job_id, job.title, job.duration_seconds, job.stems)
    return queue_manager.get_state()

@router.post("/queue/play-now", response_model=QueueResponse)
def play_now(req: QueueActionRequest):
    """Set a completed song as the active track immediately."""
    job = job_manager.get_job(req.job_id)
    if not job or job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job '{req.job_id}' is not ready for playback."
        )
    queue_manager.play_now(job.job_id, job.title, job.duration_seconds, job.stems)
    return queue_manager.get_state()

@router.post("/queue/next", response_model=QueueResponse)
def advance_queue_next():
    """Advance to the next track in the queue."""
    queue_manager.advance_next()
    return queue_manager.get_state()

@router.delete("/queue/{queue_id}", response_model=QueueResponse)
def remove_queue_item(queue_id: str):
    """Remove a track from the queue by queue ID."""
    queue_manager.remove_from_queue(queue_id)
    return queue_manager.get_state()

@router.delete("/queue", response_model=QueueResponse)
def clear_queue():
    """Clear all songs from the playback queue."""
    queue_manager.clear_queue()
    return queue_manager.get_state()
