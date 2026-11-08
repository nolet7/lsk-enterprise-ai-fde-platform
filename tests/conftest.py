import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setenv("DEMO_API_KEY", "local-demo-only-change-me")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as c:
        yield c

@pytest.fixture
def headers():
    def make(tenant="meridian-demo", actor="alice", role="analyst"):
        return {"X-API-Key": "local-demo-only-change-me", "X-Tenant": tenant,
                "X-Actor": actor, "X-Role": role}
    return make
