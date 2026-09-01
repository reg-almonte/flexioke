import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from src.main import app
from src.services.job_manager import JobManager
from src.models import SourceType, JobStatus

client = TestClient(app)

@pytest.fixture
def mock_job_environment(monkeypatch, tmp_path):
    manager = JobManager(data_dir=tmp_path / "jobs", max_workers=1)
    from src.api import routes
    monkeypatch.setattr(routes, "job_manager", manager)
    
    from src.services import pipeline
    monkeypatch.setattr(pipeline, "job_manager", manager)
    return manager

def test_pipeline_execution_and_stem_streaming(mock_job_environment, monkeypatch, tmp_path):
    job = mock_job_environment.create_job(
        source_type=SourceType.UPLOAD,
        source_name="test_song.mp3",
        title="Test Song"
    )
    job_dir = mock_job_environment.get_job_dir(job.job_id)
    input_file = job_dir / "input.mp3"
    input_file.write_bytes(b"dummy input audio")

    # Mock stage 1 and stage 2 separators and encoder
    from src.services import separator
    from src.services.separator import Stage1Result, Stage2Result, FinalStems

    def fake_stage1(input_audio, output_dir, **kwargs):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        inst = output_dir / "inst.wav"
        voc = output_dir / "voc.wav"
        inst.write_bytes(b"inst")
        voc.write_bytes(b"voc")
        return Stage1Result(instrumental_path=inst, vocals_path=voc)

    def fake_stage2(vocals_audio, output_dir, **kwargs):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        lead = output_dir / "lead.wav"
        backing = output_dir / "backing.wav"
        lead.write_bytes(b"lead")
        backing.write_bytes(b"backing")
        return Stage2Result(lead_vocals_path=lead, backing_vocals_path=backing)

    def fake_encode(s1, s2, j_dir):
        inst = j_dir / "instrumental.mp3"
        lead = j_dir / "lead_vocals.mp3"
        backing = j_dir / "backing_vocals.mp3"
        inst.write_bytes(b"instrumental mp3 data")
        lead.write_bytes(b"lead vocals mp3 data")
        backing.write_bytes(b"backing vocals mp3 data")
        return FinalStems(instrumental=inst, lead_vocals=lead, backing_vocals=backing)

    from src.services import pipeline
    monkeypatch.setattr(pipeline.separator, "separate_stage_1", fake_stage1)
    monkeypatch.setattr(pipeline.separator, "separate_stage_2", fake_stage2)
    monkeypatch.setattr(pipeline.separator, "encode_final_stems", fake_encode)

    # Run the pipeline
    pipeline.run_separation_pipeline(job.job_id)

    # Verify job status updated to COMPLETED
    updated_job = mock_job_environment.get_job(job.job_id)
    assert updated_job.status == JobStatus.COMPLETED
    assert updated_job.progress == 100
    assert len(updated_job.stems) == 3

    # Verify input audio was moved to data/archive
    archive_dir = mock_job_environment.data_dir.parent / "archive"
    archived_file = archive_dir / f"{job.job_id}_test_song.mp3"
    assert archived_file.exists()
    assert not input_file.exists()

    # Test stem streaming endpoint
    for stem_type in ["instrumental", "lead_vocals", "backing_vocals"]:
        resp = client.get(f"/api/jobs/{job.job_id}/stems/{stem_type}")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "audio/mpeg"
        assert len(resp.content) > 0

def test_stem_streaming_invalid_stem(mock_job_environment):
    job = mock_job_environment.create_job(
        source_type=SourceType.UPLOAD,
        source_name="song.mp3",
        title="Song"
    )
    resp = client.get(f"/api/jobs/{job.job_id}/stems/invalid_stem")
    assert resp.status_code == 400
    assert "invalid stem type" in resp.json()["detail"].lower()

def test_pipeline_auto_sync_lyrics(mock_job_environment, monkeypatch):
    job = mock_job_environment.create_job(
        source_type=SourceType.UPLOAD,
        source_name="valley_last_birthday.mp3",
        title="Last Birthday",
        artist="Valley"
    )
    job_dir = mock_job_environment.get_job_dir(job.job_id)
    input_file = job_dir / "input.mp3"
    input_file.write_bytes(b"dummy audio")

    from src.services import pipeline
    from src.services.separator import Stage1Result, Stage2Result, FinalStems

    monkeypatch.setattr(pipeline.separator, "separate_stage_1", lambda inp, out: Stage1Result(instrumental_path=out/"i.wav", vocals_path=out/"v.wav"))
    monkeypatch.setattr(pipeline.separator, "separate_stage_2", lambda voc, out: Stage2Result(lead_vocals_path=out/"l.wav", backing_vocals_path=out/"b.wav"))
    monkeypatch.setattr(pipeline.separator, "encode_final_stems", lambda s1, s2, jd: FinalStems(instrumental=jd/"i.mp3", lead_vocals=jd/"l.mp3", backing_vocals=jd/"b.mp3"))

    mock_lyrics = {
        "found": True,
        "lyrics": "[00:08.02] I wanted to talk\n[00:12.03] You wanted to sleep",
        "has_timestamps": True
    }
    monkeypatch.setattr(pipeline.lrclib_client, "get_lyrics", lambda track_name, artist_name: mock_lyrics)

    pipeline.run_separation_pipeline(job.job_id)

    # Verify lyrics.lrc was created automatically
    lyrics_file = job_dir / "lyrics.lrc"
    assert lyrics_file.exists()
    assert "[00:08.02] I wanted to talk" in lyrics_file.read_text(encoding="utf-8")

