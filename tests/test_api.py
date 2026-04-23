from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job(monkeypatch):
    # Mock redis client methods
    class FakeRedis:
        def lpush(self, queue, job_id):
            return True

        def hset(self, key, field, value):
            return True

    monkeypatch.setattr("api.main.r", FakeRedis())

    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"


def test_get_job_not_found(monkeypatch):
    class FakeRedis:
        def hget(self, key, field):
            return None

    monkeypatch.setattr("api.main.r", FakeRedis())

    response = client.get("/jobs/fake-job-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"