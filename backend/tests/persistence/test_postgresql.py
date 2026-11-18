from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import delete, func, insert, select, text
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.models import Activity, Base, Project

from .conftest import INIT_SQL
from .support import schema_signature

pytestmark = pytest.mark.integration


def activity_values(**overrides):
    values = {
        "name": "Analysis",
        "bac": Decimal("99999999999999.99"),
        "planned_progress_pct": Decimal("80.12"),
        "actual_progress_pct": Decimal("100.00"),
        "actual_cost": Decimal("123.45"),
    }
    return values | overrides


def test_create_and_reload_project_and_activity(session):
    project = Project(name="Project", description="Optional description")
    project.activities.append(Activity(**activity_values()))
    session.add(project)
    session.commit()
    project_id = project.id
    session.expunge_all()
    loaded = session.get(Project, project_id)
    assert loaded.name == "Project"
    assert loaded.description == "Optional description"
    assert len(loaded.activities) == 1
    item = loaded.activities[0]
    assert item.project_id == project_id
    assert item.project is loaded
    for field, expected in activity_values().items():
        assert getattr(item, field) == expected
        if field != "name":
            assert isinstance(getattr(item, field), Decimal)


@pytest.mark.parametrize("name", [None, "", " \t\n", "a" * 151])
@pytest.mark.parametrize("table", [Project.__table__, Activity.__table__])
def test_database_rejects_invalid_names(session, table, name):
    values = {"name": name}
    if table.name == "activities":
        parent = Project(name="Parent")
        session.add(parent)
        session.flush()
        values = activity_values(name=name, project_id=parent.id)
    with pytest.raises((IntegrityError, DataError)):
        session.execute(insert(table).values(**values))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("bac", "-0.01"),
        ("actual_cost", "-0.01"),
        ("bac", "100000000000000"),
        ("actual_cost", "100000000000000"),
        ("planned_progress_pct", "-0.01"),
        ("actual_progress_pct", "-0.01"),
        ("planned_progress_pct", "100.01"),
        ("actual_progress_pct", "100.01"),
        ("bac", "NaN"),
        ("actual_cost", "NaN"),
        ("planned_progress_pct", "NaN"),
        ("actual_progress_pct", "NaN"),
    ],
)
def test_database_numeric_constraints(session, field, value):
    project = Project(name="Parent")
    session.add(project)
    session.flush()
    values = activity_values(project_id=project.id, **{field: Decimal(value)})
    with pytest.raises((IntegrityError, DataError)):
        session.execute(insert(Activity.__table__).values(**values))


@pytest.mark.parametrize(
    "field", ["bac", "actual_cost", "planned_progress_pct", "actual_progress_pct"]
)
def test_database_numeric_not_null(session, field):
    project = Project(name="Parent")
    session.add(project)
    session.flush()
    with pytest.raises(IntegrityError):
        session.execute(
            insert(Activity.__table__).values(
                **activity_values(project_id=project.id, **{field: None})
            )
        )


@pytest.mark.parametrize("project_id", [None, -1])
def test_foreign_key_requires_existing_project(session, project_id):
    with pytest.raises(IntegrityError):
        session.execute(
            insert(Activity.__table__).values(**activity_values(project_id=project_id))
        )


@pytest.mark.parametrize("mode", ["loaded", "unloaded", "sql"])
def test_delete_cascade(session, mode):
    project = Project(name="Parent", activities=[Activity(**activity_values())])
    session.add(project)
    session.commit()
    project_id = project.id
    session.expunge_all()
    if mode == "sql":
        session.execute(delete(Project).where(Project.id == project_id))
    else:
        project = session.get(Project, project_id)
        if mode == "loaded":
            assert len(project.activities) == 1
        session.delete(project)
    session.commit()
    assert session.scalar(select(func.count()).select_from(Activity)) == 0
    assert session.scalar(select(func.count()).select_from(Project)) == 0


def test_removing_activity_from_collection_deletes_orphan(session):
    project = Project(name="Parent", activities=[Activity(**activity_values())])
    session.add(project)
    session.commit()
    project.activities.clear()
    session.commit()
    assert session.scalar(select(func.count()).select_from(Activity)) == 0
    assert session.get(Project, project.id) is project


def test_zero_values_and_nullable_description(session):
    values = {
        field: Decimal("0")
        for field in (
            "bac",
            "actual_cost",
            "planned_progress_pct",
            "actual_progress_pct",
        )
    }
    project = Project(name="Zero", activities=[Activity(name="Zero", **values)])
    session.add(project)
    session.commit()
    session.expire_all()
    assert project.description is None
    assert project.activities[0].bac == Decimal("0.00")


def test_sql_is_idempotent_and_matches_orm(database):
    connection, schema = database
    with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
        session.add(Project(name="Preserved"))
        session.commit()
    connection.exec_driver_sql(INIT_SQL)
    connection.exec_driver_sql(INIT_SQL)
    assert (
        connection.scalar(
            text("SELECT count(*) FROM projects WHERE name = 'Preserved'")
        )
        == 1
    )
    actual = schema_signature(connection, schema)
    comparison = f"evm_compare_{uuid4().hex}"
    connection.exec_driver_sql(f'CREATE SCHEMA "{comparison}"')
    connection.exec_driver_sql(f'SET LOCAL search_path TO "{comparison}"')
    Base.metadata.create_all(connection)
    assert actual == schema_signature(connection, comparison)


def test_every_test_starts_with_empty_tables(session):
    assert session.scalar(select(func.count()).select_from(Project)) == 0
    assert session.scalar(select(func.count()).select_from(Activity)) == 0
