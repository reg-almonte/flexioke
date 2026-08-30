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

def test_search_clear_button_and_queue_count_badges():
    resp_html = client.get("/")
    assert resp_html.status_code == 200
    assert "library-search-clear-btn" in resp_html.text
    assert "queue-count-badge" in resp_html.text

    resp_js = client.get("/static/library_queue.js")
    assert resp_js.status_code == 200
    assert "searchClearBtns" in resp_js.text or "library-search-clear-btn" in resp_js.text
    assert "queueCountBadges" in resp_js.text or "queue-count-badge" in resp_js.text

def test_sidebar_fixed_heights_and_badge_cleanup():
    resp_html = client.get("/")
    assert resp_html.status_code == 200
    assert "h-[196px]" in resp_html.text
    assert "h-[210px]" in resp_html.text

    resp_js = client.get("/static/library_queue.js")
    assert resp_js.status_code == 200
    assert "Stems ready" not in resp_js.text

def test_scoped_edit_lyrics_button_visibility():
    resp_js = client.get("/static/library_queue.js")
    assert resp_js.status_code == 200
    assert "isStudio" in resp_js.text or "view-studio" in resp_js.text or "studio-library-list" in resp_js.text

def test_expanded_song_catalog_modal():
    resp_html = client.get("/")
    assert resp_html.status_code == 200
    assert 'id="song-catalog-modal"' in resp_html.text
    assert 'id="open-catalog-modal-btn"' in resp_html.text
    assert 'id="catalog-search-input"' in resp_html.text
    assert 'id="catalog-sort-select"' in resp_html.text
    assert 'id="catalog-songs-list"' in resp_html.text

    resp_js = client.get("/static/library_queue.js")
    assert resp_js.status_code == 200
    assert "renderCatalog" in resp_js.text
    assert "openCatalogModal" in resp_js.text or "catalogModal" in resp_js.text





