import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "flexioke"

def test_static_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Flexioke" in response.text
