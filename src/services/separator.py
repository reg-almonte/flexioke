import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except ImportError:
    pass

from audio_separator.separator import Separator

logger = logging.getLogger("flexioke.separator")

# Default model checkpoints
MEL_BAND_ROFORMER_MODEL = "model_mel_band_roformer_ep_3005_sdr_11.4360.ckpt"
UVR_KARAOKE_MODEL = "UVR_MDXNET_KARA_2.onnx"

@dataclass
class Stage1Result:
    instrumental_path: Path
    vocals_path: Path

@dataclass
class Stage2Result:
    lead_vocals_path: Path
    backing_vocals_path: Path

@dataclass
class FinalStems:
    instrumental: Path
    lead_vocals: Path
    backing_vocals: Path

def convert_to_mp3(input_audio: Path, output_mp3: Path, bitrate: str = "320k") -> Path:
    """Converts any audio file to standardized MP3 using ffmpeg."""
    input_audio = Path(input_audio)
    output_mp3 = Path(output_mp3)
    output_mp3.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_audio),
        "-codec:a", "libmp3lame",
        "-b:a", bitrate,
        "-qscale:a", "0",
        str(output_mp3)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg MP3 conversion failed: {e.stderr.decode('utf-8', errors='ignore')}")
        raise RuntimeError(f"FFmpeg MP3 conversion failed for {input_audio}") from e

    return output_mp3

def _run_audio_separator(audio_file_path: Path, output_dir: Path, model_filename: str) -> List[str]:
    """Instantiates audio-separator, loads model, and separates audio."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    separator = Separator(
        output_dir=str(output_dir),
        output_format="WAV",
        log_level=logging.INFO
    )
    separator.load_model(model_filename=model_filename)
    output_files = separator.separate(str(audio_file_path))
    return output_files

def separate_stage_1(
    input_audio: Path,
    output_dir: Path,
    model_name: str = MEL_BAND_ROFORMER_MODEL
) -> Stage1Result:
    """
    Executes Stage 1 separation using Mel-Band RoFormer to separate
    input audio into Instrumental and Combined Vocals stems.
    """
    input_audio = Path(input_audio)
    output_dir = Path(output_dir)

    if not input_audio.exists():
        raise FileNotFoundError(f"Input audio file not found: {input_audio}")

    output_files = _run_audio_separator(input_audio, output_dir, model_name)

    inst_path: Optional[Path] = None
    voc_path: Optional[Path] = None

    for fname in output_files:
        full_path = output_dir / fname
        lower_name = fname.lower()
        if "instrumental" in lower_name:
            inst_path = full_path
        elif "vocals" in lower_name or "vocal" in lower_name:
            voc_path = full_path

    if not inst_path or not voc_path:
        if len(output_files) >= 2:
            inst_path = output_dir / output_files[0]
            voc_path = output_dir / output_files[1]
        else:
            raise RuntimeError(f"Stage 1 separation did not produce expected stem files: {output_files}")

    return Stage1Result(
        instrumental_path=inst_path,
        vocals_path=voc_path
    )

def separate_stage_2(
    vocals_audio: Path,
    output_dir: Path,
    model_name: str = UVR_KARAOKE_MODEL
) -> Stage2Result:
    """
    Executes Stage 2 separation using UVR MDX-Net Karaoke to separate
    Combined Vocals into Lead Vocals and Backing Vocals.
    """
    vocals_audio = Path(vocals_audio)
    output_dir = Path(output_dir)

    if not vocals_audio.exists():
        raise FileNotFoundError(f"Vocals audio file not found: {vocals_audio}")

    output_files = _run_audio_separator(vocals_audio, output_dir, model_name)

    lead_path: Optional[Path] = None
    backing_path: Optional[Path] = None

    for fname in output_files:
        full_path = output_dir / fname
        lower_name = fname.lower()
        if "vocals" in lower_name and "instrumental" not in lower_name:
            # In Karaoke model, (Vocals) is the Lead Vocals
            lead_path = full_path
        elif "instrumental" in lower_name or "karaoke" in lower_name or "backing" in lower_name:
            # In Karaoke model, (Instrumental) corresponds to Backing Vocals
            backing_path = full_path

    if not lead_path or not backing_path:
        if len(output_files) >= 2:
            lead_path = output_dir / output_files[0]
            backing_path = output_dir / output_files[1]
        else:
            raise RuntimeError(f"Stage 2 separation did not produce expected stem files: {output_files}")

    return Stage2Result(
        lead_vocals_path=lead_path,
        backing_vocals_path=backing_path
    )

def encode_final_stems(
    stage1_result: Stage1Result,
    stage2_result: Stage2Result,
    job_dir: Path
) -> FinalStems:
    """
    Converts and standardizes all 3 stems to 320kbps MP3 inside the job directory.
    """
    job_dir = Path(job_dir)
    inst_mp3 = job_dir / "instrumental.mp3"
    lead_mp3 = job_dir / "lead_vocals.mp3"
    backing_mp3 = job_dir / "backing_vocals.mp3"

    convert_to_mp3(stage1_result.instrumental_path, inst_mp3)
    convert_to_mp3(stage2_result.lead_vocals_path, lead_mp3)
    convert_to_mp3(stage2_result.backing_vocals_path, backing_mp3)

    return FinalStems(
        instrumental=inst_mp3,
        lead_vocals=lead_mp3,
        backing_vocals=backing_mp3
    )
