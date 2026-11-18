from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class ResourceNotFound(Exception):
    pass


def commit_changes(session: Session) -> None:
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
