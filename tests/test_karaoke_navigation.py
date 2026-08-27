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
