import pytest
from pathlib import Path
from src.services.separator import (
    separate_stage_1,
    separate_stage_2,
    encode_final_stems,
    Stage1Result,
    Stage2Result,
    FinalStems,
    convert_to_mp3,
)

def test_stage2_separation_mock(monkeypatch, tmp_path):
    vocals_file = tmp_path / "vocals.wav"
    vocals_file.write_bytes(b"dummy vocals wav")
    out_dir = tmp_path / "output_stage2"
    out_dir.mkdir()

    # Mock the internal _run_audio_separator
    def fake_run_separator(audio_path, output_dir, model_name):
        lead = output_dir / "vocals_(Vocals)_UVR_MDXNET_KARA_2.wav"
        backing = output_dir / "vocals_(Instrumental)_UVR_MDXNET_KARA_2.wav"
        lead.write_bytes(b"lead vocals wav")
        backing.write_bytes(b"backing vocals wav")
        return [lead.name, backing.name]

    from src.services import separator
    monkeypatch.setattr(separator, "_run_audio_separator", fake_run_separator)

    result = separate_stage_2(vocals_file, out_dir)
    assert isinstance(result, Stage2Result)
    assert result.lead_vocals_path.exists()
    assert result.backing_vocals_path.exists()

def test_convert_and_encode_final_stems(monkeypatch, tmp_path):
    job_dir = tmp_path / "job_123"
    job_dir.mkdir()

    s1 = Stage1Result(
        instrumental_path=tmp_path / "inst.wav",
        vocals_path=tmp_path / "voc.wav"
    )
    s2 = Stage2Result(
        lead_vocals_path=tmp_path / "lead.wav",
        backing_vocals_path=tmp_path / "backing.wav"
    )
    s1.instrumental_path.write_bytes(b"inst")
    s2.lead_vocals_path.write_bytes(b"lead")
    s2.backing_vocals_path.write_bytes(b"backing")

    # Mock ffmpeg convert function to avoid running subprocess in mock test
    def fake_convert(input_path, output_path, bitrate="320k"):
        output_path.write_bytes(b"dummy mp3 content")
        return output_path

    from src.services import separator
    monkeypatch.setattr(separator, "convert_to_mp3", fake_convert)

    stems = encode_final_stems(s1, s2, job_dir)
    assert isinstance(stems, FinalStems)
    assert stems.instrumental == job_dir / "instrumental.mp3"
    assert stems.lead_vocals == job_dir / "lead_vocals.mp3"
    assert stems.backing_vocals == job_dir / "backing_vocals.mp3"
    assert stems.instrumental.exists()
    assert stems.lead_vocals.exists()
    assert stems.backing_vocals.exists()
