"""Lazy synchronous database resources; transactions belong to callers."""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings


@lru_cache
def get_engine() -> Engine:
    """Read configuration on first use, without connecting during import."""
    return create_engine(
        Settings().database_url,
        pool_pre_ping=True,
        hide_parameters=True,
        connect_args={"connect_timeout": 5},
    )


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_session() -> Iterator[Session]:
    """Yield a session and always close it; callers explicitly commit or rollback."""
    with get_session_factory()() as session:
        yield session
