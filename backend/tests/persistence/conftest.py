import os
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import dotenv_values
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.models import Base

from .support import validate_test_url

BACKEND = Path(__file__).resolve().parents[2]
INIT_SQL = (BACKEND.parent / "database" / "init_db.sql").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def test_engine():
    test_settings = dotenv_values(BACKEND / ".env.test")
    value = os.getenv("TEST_DATABASE_URL") or test_settings.get("TEST_DATABASE_URL")
    if not value:
        pytest.skip("Set TEST_DATABASE_URL or backend/.env.test for PostgreSQL tests")
    development = os.getenv("DATABASE_URL") or dotenv_values(BACKEND / ".env").get(
        "DATABASE_URL"
    )
    url = validate_test_url(value, development)
    engine = create_engine(
        url, hide_parameters=True, connect_args={"connect_timeout": 5}
    )
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT current_database()")) == url.database
            version = int(connection.scalar(text("SHOW server_version_num")))
            assert 170000 <= version < 180000, "Persistence tests require PostgreSQL 17"
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(params=["sql", "orm"])
def database(request, test_engine):
    """Every test owns a fresh schema inside an outer, rolled-back transaction."""
    schema = f"evm_test_{uuid4().hex}"
    with test_engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.exec_driver_sql(f'CREATE SCHEMA "{schema}"')
            connection.exec_driver_sql(f'SET LOCAL search_path TO "{schema}"')
            if request.param == "sql":
                connection.exec_driver_sql(INIT_SQL)
            else:
                Base.metadata.create_all(connection)
            yield connection, schema
        finally:
            transaction.rollback()
    with test_engine.connect() as connection:
        assert (
            connection.scalar(
                text("SELECT count(*) FROM pg_namespace WHERE nspname = :schema"),
                {"schema": schema},
            )
            == 0
        )


@pytest.fixture
def session(database):
    with Session(bind=database[0], join_transaction_mode="create_savepoint") as session:
        yield session
