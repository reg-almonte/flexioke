from pathlib import Path
from pydantic import BaseModel, Field
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.services.job_manager import job_manager
from src.services.audio_validator import validate_audio_file, clean_song_title
from src.services.youtube_downloader import validate_youtube_url, download_youtube_audio
from src.models import JobRecord, SourceType, JobStatus

router = APIRouter(prefix="/api", tags=["api"])

class YouTubeRequest(BaseModel):
    url: str = Field(..., description="YouTube video or music link")

def _handle_youtube_download(job_id: str, url: str):
    """Background task handler for downloading YouTube audio."""
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
            current_stage="Audio downloaded, queued for separation"
        )
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

    # Dispatch background download
    job_manager.submit_task(_handle_youtube_download, job.job_id, req.url.strip())

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
