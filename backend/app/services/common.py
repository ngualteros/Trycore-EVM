from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class ResourceNotFound(Exception):
    pass


def commit_changes(session: Session) -> None:
    """Keep a failed write from leaving the request session in an aborted state."""
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
