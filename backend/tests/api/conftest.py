import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db import get_session
from app.main import app


@pytest.fixture
def client(database):
    def override_session():
        with Session(
            bind=database[0], join_transaction_mode="create_savepoint"
        ) as session:
            yield session

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = override_session
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
