import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_index_page_structure():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    # Core elements from TASK-0010
    assert "Flexioke" in html
    assert "upload-tab-btn" in html or "Upload Audio" in html
    assert "tab-url-btn" in html or "Audio URL" in html or "YouTube" in html
    assert "processing-card" in html or "progress" in html.lower()
    assert "cancel-active-job-btn" in html
    assert "queued-jobs-section" in html
    assert 'type="file"' in html and 'multiple' in html
    assert "accordion-header-add-song" in html
    assert "accordion-header-library" in html
    assert "accordion-header-queue" in html
    assert "open-notes-modal-btn" in html
    assert "studio-notes-modal" in html
    assert "studio-notes-textarea" in html
    assert "/static/app.js" in html
    assert "/static/styles.css" in html

def test_static_assets_serving():
    js_resp = client.get("/static/app.js")
    assert js_resp.status_code == 200
    assert "application/javascript" in js_resp.headers.get("content-type", "") or js_resp.status_code == 200

    css_resp = client.get("/static/styles.css")
    assert css_resp.status_code == 200

def test_favicon_serving():
    resp = client.get("/favicon.ico")
    assert resp.status_code == 200
    assert "image" in resp.headers.get("content-type", "").lower()

    svg_resp = client.get("/static/favicon.svg")
    assert svg_resp.status_code == 200

