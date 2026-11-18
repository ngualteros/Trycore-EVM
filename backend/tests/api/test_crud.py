from decimal import Decimal

import pytest
from sqlalchemy import func, select

from app.models import Activity, Project

pytestmark = pytest.mark.integration


def create_project(client, name="Project"):
    response = client.post(
        "/api/projects", json={"name": name, "description": "Description"}
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def activity_body(**changes):
    return {
        "name": "Analysis",
        "bac": "10.00",
        "planned_progress_pct": "80.00",
        "actual_progress_pct": "100.00",
        "actual_cost": "9.00",
    } | changes


def test_project_crud(client, database):
    assert client.get("/api/projects").json() == []
    project_id = create_project(client)
    path = f"/api/projects/{project_id}"
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {
        "id": project_id,
        "name": "Project",
        "description": "Description",
    }
    assert client.get("/api/projects").json() == [response.json()]
    assert (
        database[0].scalar(select(Project.name).where(Project.id == project_id))
        == "Project"
    )
    response = client.put(path, json={"name": "Updated"})
    assert response.status_code == 200
    assert response.json()["description"] is None
    assert (
        database[0].scalar(select(Project.name).where(Project.id == project_id))
        == "Updated"
    )
    response = client.delete(path)
    assert response.status_code == 204 and response.content == b""
    assert client.get(path).status_code == 404
    assert database[0].scalar(select(func.count()).select_from(Project)) == 0


def test_activity_crud_and_decimal_persistence(client, database):
    project_id = create_project(client)
    collection = f"/api/projects/{project_id}/activities"
    assert client.get(collection).json() == []
    data = activity_body(bac="99999999999999.99", actual_cost="0.01")
    response = client.post(collection, json=data)
    assert response.status_code == 201, response.text
    activity_id = response.json()["id"]
    path = f"{collection}/{activity_id}"
    assert response.json()["project_id"] == project_id
    assert response.json()["bac"] == "99999999999999.99"
    assert client.get(path).json() == response.json()
    assert client.get(collection).json() == [response.json()]
    assert database[0].scalar(select(Activity.bac)) == Decimal("99999999999999.99")
    data = activity_body(name="Updated activity", bac="123.45", actual_cost="12.34")
    response = client.put(path, json=data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated activity"
    assert response.json()["bac"] == "123.45"
    assert client.get(path).json() == response.json()
    assert database[0].scalar(select(Activity.actual_cost)) == Decimal("12.34")
    response = client.delete(path)
    assert response.status_code == 204 and response.content == b""
    assert client.get(path).status_code == 404
    assert client.get(collection).json() == []
    assert database[0].scalar(select(func.count()).select_from(Activity)) == 0


def test_project_delete_cascades_and_preserves_other_project(client, database):
    first, second = create_project(client, "First"), create_project(client, "Second")
    for project_id in (first, second):
        assert (
            client.post(
                f"/api/projects/{project_id}/activities", json=activity_body()
            ).status_code
            == 201
        )
    assert client.delete(f"/api/projects/{first}").status_code == 204
    assert client.get(f"/api/projects/{first}/activities").status_code == 404
    assert len(client.get(f"/api/projects/{second}/activities").json()) == 1
    assert database[0].scalar(select(func.count()).select_from(Activity)) == 1


def test_activity_cannot_be_accessed_through_another_project(client, database):
    owner, other = create_project(client, "Owner"), create_project(client, "Other")
    created = client.post(
        f"/api/projects/{owner}/activities", json=activity_body()
    ).json()
    path = f"/api/projects/{other}/activities/{created['id']}"
    assert client.get(path).status_code == 404
    assert client.get(path + "/evm").status_code == 404
    assert (
        client.put(path, json=activity_body(name="Forbidden update")).status_code == 404
    )
    assert client.delete(path).status_code == 404
    assert client.get(f"/api/projects/{other}/activities").json() == []
    assert database[0].scalar(select(Activity.name)) == "Analysis"


@pytest.mark.parametrize(
    "method,suffix",
    [
        ("get", ""),
        ("put", ""),
        ("delete", ""),
        ("get", "/evm"),
        ("post", "/activities"),
        ("get", "/activities"),
        ("get", "/activities/1"),
        ("put", "/activities/1"),
        ("delete", "/activities/1"),
        ("get", "/activities/1/evm"),
    ],
)
def test_missing_project_returns_404(client, method, suffix):
    kwargs = {}
    if method in ("post", "put"):
        kwargs["json"] = (
            activity_body() if "activities" in suffix else {"name": "Missing"}
        )
    assert (
        client.request(
            method, "/api/projects/2147483647" + suffix, **kwargs
        ).status_code
        == 404
    )


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_activity_returns_404(client, method):
    project_id = create_project(client)
    kwargs = {"json": activity_body()} if method == "put" else {}
    assert (
        client.request(
            method, f"/api/projects/{project_id}/activities/2147483647", **kwargs
        ).status_code
        == 404
    )


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"name": ""},
        {"name": " \t\n"},
        {"name": "x" * 151},
        {"name": None},
        {"name": 12},
        {"name": "Project", "extra": True},
    ],
)
def test_invalid_projects_do_not_persist(client, database, body):
    assert client.post("/api/projects", json=body).status_code == 422
    assert database[0].scalar(select(func.count()).select_from(Project)) == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("bac", "-0.001"),
        ("bac", "100000000000000.00"),
        ("bac", "0.001"),
        ("bac", "NaN"),
        ("bac", "Infinity"),
        ("bac", 0.1),
        ("actual_cost", "-0.01"),
        ("actual_cost", "100000000000000"),
        ("actual_cost", "1.001"),
        ("actual_cost", None),
        ("planned_progress_pct", "100.001"),
        ("planned_progress_pct", "-0.01"),
        ("actual_progress_pct", "100.01"),
        ("actual_progress_pct", "-0.001"),
        ("actual_progress_pct", True),
        ("name", ""),
        ("name", "x" * 151),
    ],
)
def test_invalid_activities_do_not_persist(client, database, field, value):
    project_id = create_project(client)
    response = client.post(
        f"/api/projects/{project_id}/activities", json=activity_body(**{field: value})
    )
    assert response.status_code == 422, response.text
    assert database[0].scalar(select(func.count()).select_from(Activity)) == 0


def test_invalid_updates_leave_existing_values_unchanged(client, database):
    project_id = create_project(client)
    base = f"/api/projects/{project_id}"
    created = client.post(base + "/activities", json=activity_body()).json()
    assert client.put(base, json={"name": ""}).status_code == 422
    path = base + f"/activities/{created['id']}"
    assert client.put(path, json=activity_body(bac="-1")).status_code == 422
    assert client.put(path, json={"name": "Incomplete"}).status_code == 422
    assert client.put(path, json=activity_body(project_id=999)).status_code == 422
    assert database[0].scalar(select(Project.name)) == "Project"
    assert database[0].scalar(select(Activity.bac)) == Decimal("10.00")


@pytest.mark.parametrize("identifier", ["0", "-1", "text", "2147483648"])
def test_invalid_path_id_returns_422(client, identifier):
    assert client.get(f"/api/projects/{identifier}").status_code == 422


def test_database_error_is_sanitized_and_rolled_back(client, database):
    response = client.post("/api/projects", json={"name": "invalid\u0000name"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Data violates storage constraints"}
    assert database[0].scalar(select(func.count()).select_from(Project)) == 0
    assert (
        client.post("/api/projects", json={"name": "Valid after error"}).status_code
        == 201
    )
