import io
import re
import zipfile
import urllib.parse
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query, Request, status
from fastapi.responses import FileResponse, Response, StreamingResponse

from src.services.job_manager import job_manager
from src.services.video_manager import video_manager
from src.services.queue_manager import queue_manager
from src.services.audio_validator import validate_audio_file, clean_song_title, parse_song_and_artist
from src.services.audio_downloader import validate_audio_url, download_audio_url
from src.services.youtube_downloader import validate_youtube_url, download_youtube_audio
from src.services.pipeline import run_separation_pipeline, VALID_STEM_TYPES
from src.services.lrclib_client import lrclib_client
from src.services.playlist_manager import playlist_manager
from src.models import (
    JobRecord,
    JobListResponse,
    JobUpdateMetadataRequest,
    QueueItem,
    QueueResponse,
    QueueReorderRequest,
    LyricsResponse,
    LyricsUpdateRequest,
    AudioUrlRequest,
    SourceType,
    JobStatus,
    Playlist,
    PlaylistSummary,
    PlaylistDetail,
    PlaylistCreate,
    PlaylistUpdate,
    PlaylistSongAdd,
    PlaylistReorderRequest,
    PlaylistFromQueueRequest,
    VideoInfo,
    VideoListResponse,
)

router = APIRouter(prefix="/api", tags=["api"])

class YouTubeRequest(BaseModel):
    url: str = Field(..., description="YouTube video or music link")

class QueueActionRequest(BaseModel):
    job_id: str = Field(..., description="Target Job ID to add or play")

def _handle_audio_url_download_and_pipeline(job_id: str, url: str):
    """Background task handler for downloading audio from URL and triggering separation."""
    job_dir = job_manager.get_job_dir(job_id)
    parsed = urllib.parse.urlparse(url)
    raw_filename = urllib.parse.unquote(Path(parsed.path).name)
    ext = Path(raw_filename).suffix.lower() if ("." in raw_filename) else ".mp3"
    if ext not in (".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac"):
        ext = ".mp3"
    output_path = job_dir / f"input{ext}"
    try:
        def on_progress(pct: int, msg: str):
            job_manager.update_job(
                job_id,
                status=JobStatus.DOWNLOADING,
                progress=pct,
                current_stage=msg
            )
        info = download_audio_url(url, output_path, progress_callback=on_progress)
        if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
            return

        job_manager.update_job(
            job_id,
            title=info["title"],
            artist=info.get("artist"),
            duration_seconds=info.get("duration"),
            status=JobStatus.QUEUED,
            progress=15,
            current_stage="Audio downloaded, starting separation..."
        )
        # Proceed straight to 2-stage separation pipeline
        run_separation_pipeline(job_id)
    except Exception as e:
        current_j = job_manager.get_job(job_id)
        if current_j and current_j.status == JobStatus.CANCELLED:
            return
        job_manager.update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e),
            current_stage="Audio download failed"
        )

def _handle_youtube_download_and_pipeline(job_id: str, url: str):
    """Background task handler for downloading YouTube audio and triggering separation."""
    job_dir = job_manager.get_job_dir(job_id)
    output_path = job_dir / "input.mp3"
    try:
        job_manager.update_job(
            job_id,
            status=JobStatus.DOWNLOADING,
            progress=5,
            current_stage="Connecting to YouTube..."
        )
        def on_progress(pct: int, msg: str):
            if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
                return
            job_manager.update_job(
                job_id,
                status=JobStatus.DOWNLOADING,
                progress=pct,
                current_stage=msg
            )
        info = download_youtube_audio(url, output_path, progress_callback=on_progress)
        if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
            return

        job_manager.update_job(
            job_id,
            title=info["title"],
            artist=info.get("artist"),
            duration_seconds=info["duration"],
            status=JobStatus.QUEUED,
            progress=15,
            current_stage="Audio downloaded, starting separation..."
        )
        # Proceed straight to 2-stage separation pipeline
        run_separation_pipeline(job_id)
    except Exception as e:
        current_j = job_manager.get_job(job_id)
        if current_j and current_j.status == JobStatus.CANCELLED:
            return
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
        "version": "0.3.1",
    }

@router.get("/jobs", response_model=JobListResponse)
def list_jobs(
    status: Optional[str] = Query(default=JobStatus.COMPLETED.value, description="Filter by job status ('all' for all jobs)"),
    q: Optional[str] = Query(default=None, description="Search query for title or source")
):
    """List and search songs in the library or queue."""
    filter_status = None if status in ("all", None, "") else JobStatus(status)
    jobs = job_manager.list_jobs(status=filter_status, query=q)
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

    title, artist = parse_song_and_artist(filename)
    job = job_manager.create_job(
        source_type=SourceType.UPLOAD,
        source_name=filename,
        title=title,
        artist=artist
    )

    # Save uploaded audio file into job directory
    ext = Path(filename).suffix.lower()
    job_dir = job_manager.get_job_dir(job.job_id)
    input_path = job_dir / f"input{ext}"
    input_path.write_bytes(content)

    # Enqueue separation pipeline in worker pool
    job_manager.submit_task(run_separation_pipeline, job.job_id)

    return job

@router.post("/jobs/download-url", status_code=status.HTTP_202_ACCEPTED, response_model=JobRecord)
def submit_audio_url(req: AudioUrlRequest):
    """Submit a direct HTTP/HTTPS audio URL for downloading and stem separation."""
    is_valid, error_msg = validate_audio_url(req.url)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    parsed = urllib.parse.urlparse(req.url.strip())
    raw_filename = urllib.parse.unquote(Path(parsed.path).name) or "downloaded_audio.mp3"
    title, artist = parse_song_and_artist(raw_filename)

    job = job_manager.create_job(
        source_type=SourceType.URL,
        source_name=req.url.strip(),
        title=title,
        artist=artist
    )

    # Dispatch background download and separation pipeline
    job_manager.submit_task(_handle_audio_url_download_and_pipeline, job.job_id, req.url.strip())

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

@router.post("/jobs/upload-side-ab", response_model=JobRecord)
async def upload_side_ab_audio(
    file_side_b: UploadFile = File(...),
    file_side_a: Optional[UploadFile] = File(None),
    title: Optional[str] = Form(None),
    artist: Optional[str] = Form(None)
):
    """Direct dual-track upload for Side B (Instrumental) and optional Side A (Vocal)."""
    # 1. Validate Side B (Instrumental - Required)
    b_filename = file_side_b.filename or "instrumental.mp3"
    b_content = await file_side_b.read()
    is_b_valid, b_err = validate_audio_file(b_filename, len(b_content))
    if not is_b_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Side B (Instrumental) error: {b_err}"
        )

    # 2. Validate Side A (Vocal - Optional) if provided
    a_content = None
    if file_side_a is not None and file_side_a.filename:
        a_filename = file_side_a.filename
        a_content = await file_side_a.read()
        if len(a_content) > 0:
            is_a_valid, a_err = validate_audio_file(a_filename, len(a_content))
            if not is_a_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Side A (Vocal) error: {a_err}"
                )

    # 3. Determine Title & Artist
    parsed_title, parsed_artist = parse_song_and_artist(b_filename)
    final_title = title.strip() if (title and title.strip()) else parsed_title
    final_artist = artist.strip() if (artist and artist.strip()) else parsed_artist

    # 4. Create JobRecord
    job = job_manager.create_job(
        source_type=SourceType.SIDE_AB,
        source_name=b_filename,
        title=final_title,
        artist=final_artist
    )

    # 5. Write Files & Map Stems
    job_dir = job_manager.get_job_dir(job.job_id)
    (job_dir / "instrumental.mp3").write_bytes(b_content)
    stems_map = {
        "instrumental": f"/api/jobs/{job.job_id}/stems/instrumental"
    }

    if a_content and len(a_content) > 0:
        (job_dir / "lead_vocals.mp3").write_bytes(a_content)
        stems_map["lead_vocals"] = f"/api/jobs/{job.job_id}/stems/lead_vocals"

    # 6. Auto-Fetch Synced Lyrics (LRCLIB Integration)
    try:
        lrc_match = lrclib_client.fetch_best_synced_lyrics(
            track_name=final_title,
            artist_name=final_artist or ""
        )
        if lrc_match and lrc_match.get("synced_lyrics"):
            lyrics_text = lrc_match["synced_lyrics"]
            job_manager.save_lyrics(job.job_id, lyrics_text)
    except Exception as e:
        print(f"[Side A/B Upload] LRCLIB auto-sync notice for {job.job_id}: {e}")

    # 7. Complete Job Immediately (Bypassing Separation Pipeline)
    updated_job = job_manager.update_job(
        job.job_id,
        status=JobStatus.COMPLETED,
        progress=100,
        current_stage="Direct Side A/B Ready",
        stems=stems_map
    )

    return updated_job

@router.post("/jobs/{job_id}/attach-side-a", response_model=JobRecord)
async def attach_side_a(
    job_id: str,
    file: Optional[UploadFile] = File(None),
    file_side_a: Optional[UploadFile] = File(None)
):
    """Attaches a Side A (Lead Vocal) audio track to an existing completed Side A/B job."""
    upload = file or file_side_a
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio file for Side A is required (field 'file' or 'file_side_a')."
        )

    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )

    filename = upload.filename or "lead_vocals.mp3"
    content = await upload.read()
    is_valid, err_msg = validate_audio_file(filename, len(content))
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )

    job_dir = job_manager.get_job_dir(job_id)
    (job_dir / "lead_vocals.mp3").write_bytes(content)

    updated_stems = dict(job.stems)
    updated_stems["lead_vocals"] = f"/api/jobs/{job_id}/stems/lead_vocals"

    updated_job = job_manager.update_job(
        job_id,
        stems=updated_stems
    )
    return updated_job

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

@router.post("/jobs/{job_id}/cancel", response_model=JobRecord)
def cancel_job(job_id: str):
    """Cancel a queued or in-progress separation job."""
    job = job_manager.cancel_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )
    return job

@router.patch("/jobs/{job_id}", response_model=JobRecord)
def update_job_metadata(job_id: str, req: JobUpdateMetadataRequest):
    """Update song title and artist metadata for a job."""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )

    updates = {}
    if req.title is not None:
        updates["title"] = req.title.strip()
    if req.artist is not None:
        updates["artist"] = req.artist.strip() if req.artist.strip() else None
    if req.video_id is not None:
        updates["video_id"] = req.video_id.strip() if req.video_id.strip() else "bg001.mp4"
    if req.video_offset_seconds is not None:
        updates["video_offset_seconds"] = max(0.0, float(req.video_offset_seconds))

    updated_job = job_manager.update_job(job_id, **updates)
    queue_manager.update_job_metadata(
        job_id,
        title=updated_job.title,
        artist=updated_job.artist,
        video_id=updated_job.video_id,
        video_offset_seconds=updated_job.video_offset_seconds
    )
    return updated_job



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

@router.get("/jobs/{job_id}/export/zip")
@router.get("/jobs/{job_id}/download-all.zip")
def export_job_stems_zip(job_id: str):
    """Packages the 3 isolated stems and lyrics.lrc (if present) into a single downloadable .zip archive."""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job '{job_id}' is not completed yet (current status: {job.status})."
        )

    job_dir = job_manager.get_job_dir(job_id)
    stem_names = ["instrumental.mp3", "lead_vocals.mp3", "backing_vocals.mp3"]
    found_any = False

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in stem_names:
            path = job_dir / name
            if path.exists():
                zf.write(path, arcname=name)
                found_any = True
        lyrics_file = job_dir / "lyrics.lrc"
        if lyrics_file.exists() and lyrics_file.stat().st_size > 0:
            zf.write(lyrics_file, arcname="lyrics.lrc")

    if not found_any:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stems available on disk for job '{job_id}'."
        )

    zip_buffer.seek(0)
    clean_title = re.sub(r'[^\w\-_.]', '_', job.title or "flexioke")
    zip_filename = f"{clean_title}_stems.zip"

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{zip_filename}"'
        }
    )

@router.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    """Permanently deletes a song, its stems, archives, and removes it from playback queues and playlists."""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found."
        )

    # Purge from playback queue
    queue_manager.remove_jobs_from_queue(job_id)

    # Prune from all playlists
    playlist_manager.prune_song_from_all_playlists(job_id)

    # Delete storage and metadata
    job_manager.delete_job(job_id)

    return {"message": "Job deleted successfully", "job_id": job_id}

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

@router.get("/lyrics/lrclib/get")
def get_lrclib_lyrics(
    title: str = Query(..., description="Song track name"),
    artist: Optional[str] = Query(None, description="Artist name"),
    duration: Optional[float] = Query(None, description="Track duration in seconds")
):
    """Proxy endpoint to fetch lyrics from LRCLIB with fallback to search."""
    return lrclib_client.get_lyrics(track_name=title, artist_name=artist, duration=duration)

@router.get("/lyrics/lrclib/search")
def search_lrclib_lyrics(
    q: str = Query(..., description="Search query keywords")
):
    """Proxy endpoint to search candidate tracks on LRCLIB."""
    return {"results": lrclib_client.search_lyrics(q)}

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
    queue_manager.add_to_queue(
        job.job_id,
        job.title,
        job.artist,
        job.duration_seconds,
        job.stems,
        job.video_id,
        job.video_offset_seconds
    )
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
    queue_manager.play_now(
        job.job_id,
        job.title,
        job.artist,
        job.duration_seconds,
        job.stems,
        job.video_id,
        job.video_offset_seconds
    )
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

@router.post("/queue/reorder", response_model=QueueResponse)
def reorder_queue(req: QueueReorderRequest):
    """Reorder a queued track up or down."""
    if req.direction not in ("up", "down"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Direction must be 'up' or 'down'."
        )
    try:
        res = queue_manager.reorder_queue(req.queue_id, req.direction)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Queue item '{req.queue_id}' not found."
            )
        return res
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# --- Playlist Endpoints ---

@router.get("/playlists", response_model=list[PlaylistSummary])
def list_playlists():
    """Returns summaries of all playlists with song counts and durations."""
    return playlist_manager.get_all_playlists(job_mgr=job_manager)

@router.post("/playlists", status_code=status.HTTP_201_CREATED, response_model=Playlist)
def create_playlist(req: PlaylistCreate):
    """Creates a new custom playlist."""
    try:
        return playlist_manager.create_playlist(name=req.name, description=req.description)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/playlists/{playlist_id}", response_model=PlaylistDetail)
def get_playlist_detail(playlist_id: str):
    """Retrieves playlist details and resolved track records (with orphan pruning)."""
    detail = playlist_manager.get_playlist_detail(playlist_id, job_mgr=job_manager)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Playlist '{playlist_id}' not found."
        )
    return detail

@router.put("/playlists/{playlist_id}", response_model=Playlist)
def update_playlist(playlist_id: str, req: PlaylistUpdate):
    """Updates playlist name or description. Rejects renaming favorites."""
    try:
        updated = playlist_manager.update_playlist(
            playlist_id=playlist_id,
            name=req.name,
            description=req.description
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{playlist_id}' not found."
            )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: str):
    """Deletes a custom playlist. Rejects deletion of favorites."""
    try:
        deleted = playlist_manager.delete_playlist(playlist_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{playlist_id}' not found."
            )
        return {"status": "deleted", "playlist_id": playlist_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/playlists/{playlist_id}/songs", response_model=PlaylistDetail)
def add_song_to_playlist(playlist_id: str, req: PlaylistSongAdd):
    """Adds a track to a playlist."""
    try:
        playlist_manager.add_song(playlist_id=playlist_id, song_id=req.song_id, job_mgr=job_manager)
        return playlist_manager.get_playlist_detail(playlist_id, job_mgr=job_manager)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # Conflict: already exists
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/playlists/{playlist_id}/songs/{song_id}", response_model=PlaylistDetail)
def remove_song_from_playlist(playlist_id: str, song_id: str):
    """Removes a track from a playlist."""
    try:
        playlist_manager.remove_song(playlist_id=playlist_id, song_id=song_id)
        return playlist_manager.get_playlist_detail(playlist_id, job_mgr=job_manager)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/playlists/{playlist_id}/reorder", response_model=PlaylistDetail)
def reorder_playlist_songs(playlist_id: str, req: PlaylistReorderRequest):
    """Updates the ordering of songs in a playlist."""
    try:
        playlist_manager.reorder_songs(playlist_id=playlist_id, song_ids=req.song_ids)
        return playlist_manager.get_playlist_detail(playlist_id, job_mgr=job_manager)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/playlists/from-queue", status_code=status.HTTP_201_CREATED, response_model=PlaylistDetail)
def create_playlist_from_queue(req: PlaylistFromQueueRequest):
    """Creates a new custom playlist from active playback queue songs."""
    try:
        pl = playlist_manager.create_from_queue(
            name=req.name,
            song_ids=req.song_ids,
            description=req.description,
            job_mgr=job_manager
        )
        return playlist_manager.get_playlist_detail(pl.id, job_mgr=job_manager)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------------------------------------------------------------------------
# Background Video Endpoints
# ---------------------------------------------------------------------------

@router.get("/videos", response_model=VideoListResponse)
def list_videos():
    """Lists all available background video assets in /data/videos/."""
    videos = video_manager.list_videos()
    return VideoListResponse(total=len(videos), videos=videos)

@router.post("/videos/upload", response_model=VideoInfo, status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...)):
    """Uploads a new background video asset."""
    content = await file.read()
    try:
        info = video_manager.save_video(file.filename, content)
        return info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/videos/{filename}")
def stream_video(filename: str, request: Request):
    """Streams a background video file with HTTP Range (Partial Content) support."""
    path = video_manager.get_video_path(filename)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video '{filename}' not found."
        )

    file_size = path.stat().st_size
    content_type = video_manager.get_content_type(filename)
    range_header = request.headers.get("range")

    if range_header:
        # Range header format: bytes=START-END
        match = re.search(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1
            end = min(end, file_size - 1)
            if start > end or start >= file_size:
                raise HTTPException(
                    status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                    headers={"Content-Range": f"bytes */{file_size}"}
                )
            content_length = end - start + 1

            def chunk_generator():
                with open(path, "rb") as f:
                    f.seek(start)
                    remaining = content_length
                    while remaining > 0:
                        chunk_size = min(64 * 1024, remaining)
                        data = f.read(chunk_size)
                        if not data:
                            break
                        remaining -= len(data)
                        yield data

            return StreamingResponse(
                chunk_generator(),
                status_code=status.HTTP_206_PARTIAL_CONTENT,
                headers={
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(content_length),
                    "Content-Type": content_type,
                }
            )

    return FileResponse(
        path,
        media_type=content_type,
        headers={"Accept-Ranges": "bytes"}
    )



