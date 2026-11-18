from types import SimpleNamespace
from unittest.mock import MagicMock

from sqlalchemy.engine import Engine

from app import db


def test_engine_and_factory_are_lazy_and_cached(monkeypatch):
    monkeypatch.setattr(
        db,
        "Settings",
        lambda: SimpleNamespace(
            database_url="postgresql+psycopg://unused:unused@127.0.0.1:1/unused"
        ),
    )
    db.get_engine.cache_clear()
    db.get_session_factory.cache_clear()
    engine = None
    try:
        engine = db.get_engine()
        assert isinstance(engine, Engine)
        assert db.get_engine() is engine
        factory = db.get_session_factory()
        assert db.get_session_factory() is factory
        with factory() as session:
            assert session.bind is engine
            assert not session.in_transaction()
    finally:
        if engine is not None:
            engine.dispose()
        db.get_engine.cache_clear()
        db.get_session_factory.cache_clear()


def test_session_dependency_closes_without_implicit_commit(monkeypatch):
    session = MagicMock()
    session.__enter__.return_value = session
    monkeypatch.setattr(db, "get_session_factory", lambda: lambda: session)
    dependency = db.get_session()
    assert next(dependency) is session
    dependency.close()
    session.__exit__.assert_called_once()
    session.commit.assert_not_called()
