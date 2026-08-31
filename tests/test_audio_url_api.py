import pytest
from fastapi.testclient import TestClient
from src.main import app
import urllib.request

client = TestClient(app)

def test_download_url_endpoint_invalid_url():
    resp = client.post("/api/jobs/download-url", json={"url": "invalid://not-http"})
    assert resp.status_code == 400
    assert "Invalid URL protocol" in resp.json()["detail"]

def test_download_url_endpoint_success(monkeypatch, tmp_path):
    def mock_urlopen(req, timeout=30):
        class MockUrlOpen:
            headers = {"Content-Type": "audio/mpeg", "Content-Length": "100"}
            def read(self, chunk_size=8192):
                if not hasattr(self, "_read"):
                    self._read = True
                    return b"ID3" + b"\x00" * 97
                return b""
            def __enter__(self): return self
            def __exit__(self, *args): pass
        return MockUrlOpen()

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)
    from src.services.job_manager import job_manager
    monkeypatch.setattr(job_manager, "submit_task", lambda fn, *args, **kwargs: None)

    resp = client.post(
        "/api/jobs/download-url",
        json={"url": "https://example.com/audio/01._Bohemian_Rhapsody_-_Queen.mp3"}
    )
    assert resp.status_code == 202
    data = resp.json()
    assert data["source_type"] == "url"
    assert data["title"] == "Bohemian Rhapsody"
    assert data["artist"] == "Queen"
    assert data["status"] == "queued"
