import pytest
from pathlib import Path
from src.services.separator import separate_stage_1, Stage1Result

def test_stage1_separation_mock(monkeypatch, tmp_path):
    input_file = tmp_path / "input.mp3"
    input_file.write_bytes(b"dummy audio")
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    # Mock the internal _run_audio_separator to avoid downloading multi-gigabyte models in unit test
    def fake_run_separator(audio_path, output_dir, model_name):
        inst = output_dir / "input_(Instrumental)_model_mel_band_roformer.wav"
        voc = output_dir / "input_(Vocals)_model_mel_band_roformer.wav"
        inst.write_bytes(b"instrumental wav")
        voc.write_bytes(b"vocals wav")
        return [inst.name, voc.name]

    from src.services import separator
    monkeypatch.setattr(separator, "_run_audio_separator", fake_run_separator)

    result = separate_stage_1(input_file, out_dir)
    assert isinstance(result, Stage1Result)
    assert result.instrumental_path.exists()
    assert result.vocals_path.exists()
    assert "Instrumental" in result.instrumental_path.name
    assert "Vocals" in result.vocals_path.name

def test_stage1_input_not_found(tmp_path):
    missing_file = tmp_path / "non_existent.mp3"
    out_dir = tmp_path / "output"
    with pytest.raises(FileNotFoundError):
        separate_stage_1(missing_file, out_dir)
