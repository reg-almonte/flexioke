import logging
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
        # Fallback if names don't explicitly contain keywords
        if len(output_files) >= 2:
            inst_path = output_dir / output_files[0]
            voc_path = output_dir / output_files[1]
        else:
            raise RuntimeError(f"Stage 1 separation did not produce expected stem files: {output_files}")

    return Stage1Result(
        instrumental_path=inst_path,
        vocals_path=voc_path
    )
