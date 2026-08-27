from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.services.job_manager import job_manager
from src.services.audio_validator import validate_audio_file, clean_song_title
from src.models import JobRecord, SourceType, JobStatus

router = APIRouter(prefix="/api", tags=["api"])

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
