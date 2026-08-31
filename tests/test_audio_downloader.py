import pytest
from pathlib import Path
from src.services.audio_downloader import validate_audio_url, download_audio_url

def test_validate_audio_url_valid():
    is_valid, msg = validate_audio_url("https://example.com/audio/Bohemian_Rhapsody_-_Queen.mp3")
    assert is_valid is True
    assert msg == ""

    is_valid, msg = validate_audio_url("http://cdn.music.com/song.flac?token=123")
    assert is_valid is True
    assert msg == ""

def test_validate_audio_url_invalid():
    is_valid, msg = validate_audio_url("ftp://example.com/song.mp3")
    assert is_valid is False
    assert "Invalid URL protocol" in msg

    is_valid, msg = validate_audio_url("not a url")
    assert is_valid is False
    assert "Invalid URL" in msg

def test_download_audio_url_mock(monkeypatch, tmp_path):
    class MockResponse:
        status_code = 200
        headers = {"content-type": "audio/mpeg", "content-length": "100"}
        def iter_content(self, chunk_size=8192):
            yield b"ID3" + b"\x00" * 97

        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    import urllib.request
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

    dest = tmp_path / "input.mp3"
    info = download_audio_url("https://example.com/music/Bohemian_Rhapsody_-_Queen.mp3", dest)
    assert dest.exists()
    assert dest.stat().st_size == 100
    assert info["title"] == "Bohemian Rhapsody"
    assert info["artist"] == "Queen"

def test_download_audio_url_rejects_html(monkeypatch, tmp_path):
    import urllib.request
    def mock_urlopen(req, timeout=30):
        class MockUrlOpen:
            headers = {"Content-Type": "text/html; charset=utf-8", "Content-Length": "150"}
            def read(self, chunk_size=8192):
                return b"<html><body>Not Found</body></html>"
            def __enter__(self): return self
            def __exit__(self, *args): pass
        return MockUrlOpen()

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    dest = tmp_path / "invalid.mp3"
    with pytest.raises(ValueError, match="does not point to an audio file"):
        download_audio_url("https://example.com/page.html", dest)
    assert not dest.exists()
