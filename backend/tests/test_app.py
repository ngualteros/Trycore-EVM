from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_swagger_and_openapi():
    response = client.get("/api-docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "/openapi.json" in response.text
    schema = client.get("/openapi.json")
    assert schema.status_code == 200
    assert "/health" in schema.json()["paths"]
    assert client.get("/docs").status_code == 404
