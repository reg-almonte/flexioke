import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_top_navigation_tabs_in_html():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "nav-tab-studio" in html
    assert "nav-tab-karaoke" in html
    assert "view-stem-studio" in html
    assert "view-karaoke" in html

def test_dual_independent_library_and_queue_panels():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    # Check that both Studio and Karaoke pages have their own library & queue components
    assert "Studio Song Library" in html
    assert "Song Library" in html
    assert "Studio Queue" in html
    assert "Playback Queue" in html

def test_auto_hiding_header_and_sensor():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert 'id="app-header"' in html
    assert 'id="top-nav-sensor"' in html

    resp_css = client.get("/static/styles.css")
    assert resp_css.status_code == 200
    assert "karaoke-active" in resp_css.text
    assert "top-nav-sensor" in resp_css.text

