from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, OperationalError

from app.db import get_session
from app.main import app
from app.services import projects


def test_openapi_documents_all_endpoints():
    with TestClient(app) as client:
        assert client.get("/api-docs").status_code == 200
        schema = client.get("/openapi.json").json()
    paths = {
        "/api/projects": {"get", "post"},
        "/api/projects/{project_id}": {"get", "put", "delete"},
        "/api/projects/{project_id}/activities": {"get", "post"},
        "/api/projects/{project_id}/activities/{activity_id}": {"get", "put", "delete"},
        "/api/projects/{project_id}/evm": {"get"},
        "/api/projects/{project_id}/activities/{activity_id}/evm": {"get"},
    }
    for path, methods in paths.items():
        assert set(schema["paths"][path]) == methods
        for method in methods:
            operation = schema["paths"][path][method]
            assert operation["tags"][0] in ("projects", "activities", "evm")
            success = (
                "201" if method == "post" else "204" if method == "delete" else "200"
            )
            assert success in operation["responses"]
            assert "422" in operation["responses"]
    activity = schema["components"]["schemas"]["ActivityWrite"]
    assert activity["properties"]["bac"]["type"] == "string"


def test_database_failures_do_not_expose_internal_details(monkeypatch):
    def failure(*args):
        raise OperationalError(
            "SECRET SQL", {"password": "secret"}, Exception("private")
        )

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = lambda: None
    monkeypatch.setattr(projects, "list_projects", failure)
    try:
        with TestClient(app) as client:
            response = client.get("/api/projects")
        assert response.status_code == 503
        assert response.json() == {"detail": "Database temporarily unavailable"}
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)


def test_integrity_errors_have_safe_response(monkeypatch):
    def failure(*args):
        raise IntegrityError("SECRET SQL", {}, Exception("private"))

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = lambda: None
    monkeypatch.setattr(projects, "create_project", failure)
    try:
        with TestClient(app) as client:
            response = client.post("/api/projects", json={"name": "Project"})
        assert response.status_code == 422
        assert response.json() == {"detail": "Data violates storage constraints"}
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
