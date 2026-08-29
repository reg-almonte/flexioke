import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_library_queue_script_served():
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    assert "SongLibraryManager" in resp.text
    assert "Unknown Artist" in resp.text or "artist" in resp.text.lower()
    assert "localeCompare" in resp.text or "sort" in resp.text

def test_index_includes_library_queue_script():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "/static/library_queue.js" in resp.text
    assert "Search by song title or artist" in resp.text

def test_karaoke_sidebar_layout_order():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    # In karaoke-page sidebar, Playback Queue should appear before Song Library
    karaoke_idx = html.find('id="view-karaoke"')
    assert karaoke_idx != -1
    queue_idx = html.find('Playback Queue', karaoke_idx)
    lib_idx = html.find('Song Library', karaoke_idx)
    assert queue_idx != -1 and lib_idx != -1
    assert queue_idx < lib_idx

def test_queue_reordering_frontend_logic():
    resp = client.get("/static/library_queue.js")
    assert resp.status_code == 200
    assert "reorderItem" in resp.text or "reorder" in resp.text
    assert "/api/queue/reorder" in resp.text



