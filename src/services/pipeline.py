import logging
import shutil
from pathlib import Path
from typing import Optional

from src.models import JobStatus
from src.services.job_manager import job_manager
from src.services import separator

logger = logging.getLogger("flexioke.pipeline")

VALID_STEM_TYPES = {"instrumental", "lead_vocals", "backing_vocals"}

def run_separation_pipeline(job_id: str):
    """
    Orchestrates the full 2-stage audio stem separation pipeline:
    1. Mel-Band RoFormer (Stage 1) -> Instrumental & Vocals
    2. UVR MDX-Net Karaoke (Stage 2) -> Lead & Backing Vocals
    3. MP3 encoding and final stem registration
    """
    job = job_manager.get_job(job_id)
    if not job:
        logger.error(f"Job {job_id} not found when starting pipeline.")
        return
    if job.status == JobStatus.CANCELLED:
        logger.info(f"Job {job_id} was cancelled before starting.")
        return

    job_dir = job_manager.get_job_dir(job_id)

    # Locate input audio file in job directory
    input_files = list(job_dir.glob("input.*"))
    if not input_files:
        error_msg = "No input audio file found in job directory."
        logger.error(f"[{job_id}] {error_msg}")
        job_manager.update_job(
            job_id,
            status=JobStatus.FAILED,
            error=error_msg,
            current_stage="Failed: Input file missing"
        )
        return

    input_file = input_files[0]

    try:
        if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
            return

        # Stage 1: Mel-Band RoFormer
        job_manager.update_job(
            job_id,
            status=JobStatus.SEPARATING_STAGE_1,
            progress=25,
            current_stage="Stage 1: Separating Music & Vocals (Mel-Band RoFormer)..."
        )
        stage1_out = job_dir / "stage1_temp"
        stage1_res = separator.separate_stage_1(input_file, stage1_out)

        if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
            shutil.rmtree(stage1_out, ignore_errors=True)
            return

        # Stage 2: UVR MDX-Net Karaoke
        job_manager.update_job(
            job_id,
            status=JobStatus.SEPARATING_STAGE_2,
            progress=65,
            current_stage="Stage 2: Separating Lead & Backing Vocals (Karaoke Model)..."
        )
        stage2_out = job_dir / "stage2_temp"
        stage2_res = separator.separate_stage_2(stage1_res.vocals_path, stage2_out)

        if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
            shutil.rmtree(stage1_out, ignore_errors=True)
            shutil.rmtree(stage2_out, ignore_errors=True)
            return

        # MP3 Encoding & Normalization
        job_manager.update_job(
            job_id,
            progress=90,
            current_stage="Encoding & standardizing MP3 audio stems..."
        )
        separator.encode_final_stems(stage1_res, stage2_res, job_dir)

        # Cleanup intermediate WAV directories to save disk space
        shutil.rmtree(stage1_out, ignore_errors=True)
        shutil.rmtree(stage2_out, ignore_errors=True)

        if job_manager.get_job(job_id).status == JobStatus.CANCELLED:
            return

        # Register final stem streaming URLs
        stems_map = {
            "instrumental": f"/api/jobs/{job_id}/stems/instrumental",
            "lead_vocals": f"/api/jobs/{job_id}/stems/lead_vocals",
            "backing_vocals": f"/api/jobs/{job_id}/stems/backing_vocals",
        }

        # Post-separation archiving: Move raw input audio to ./data/archive/{job_id}_{clean_source_name}
        try:
            archive_dir = job_manager.data_dir.parent / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            clean_source = (job.source_name or "audio").replace(" ", "_")
            dest_archive_path = archive_dir / f"{job_id}_{clean_source}"
            if input_file.exists():
                shutil.move(str(input_file), str(dest_archive_path))
                logger.info(f"[{job_id}] Archived raw input audio to {dest_archive_path}")
        except Exception as archive_err:
            logger.warning(f"[{job_id}] Failed to archive input audio: {archive_err}")

        job_manager.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            current_stage="Ready for playback",
            stems=stems_map
        )
        logger.info(f"[{job_id}] Separation pipeline completed successfully.")

    except Exception as e:
        logger.exception(f"[{job_id}] Separation pipeline failed: {str(e)}")
        job_manager.update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e),
            current_stage="Separation failed"
        )
