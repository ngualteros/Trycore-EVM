from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Activity
from app.schemas.activities import ActivityWrite
from app.services.common import ResourceNotFound, commit_changes
from app.services.projects import get_project


def get_activity(session: Session, project_id: int, activity_id: int) -> Activity:
    get_project(session, project_id)
    activity = session.scalar(
        select(Activity).where(
            Activity.id == activity_id, Activity.project_id == project_id
        )
    )
    if activity is None:
        raise ResourceNotFound("Activity not found")
    return activity


def list_activities(session: Session, project_id: int) -> list[Activity]:
    get_project(session, project_id)
    return list(
        session.scalars(
            select(Activity)
            .where(Activity.project_id == project_id)
            .order_by(Activity.id)
        )
    )


def create_activity(session: Session, project_id: int, data: ActivityWrite) -> Activity:
    get_project(session, project_id)
    activity = Activity(project_id=project_id, **data.model_dump())
    session.add(activity)
    commit_changes(session)
    return activity


def update_activity(
    session: Session, project_id: int, activity_id: int, data: ActivityWrite
) -> Activity:
    activity = get_activity(session, project_id, activity_id)
    for field, value in data.model_dump().items():
        setattr(activity, field, value)
    commit_changes(session)
    return activity


def delete_activity(session: Session, project_id: int, activity_id: int) -> None:
    session.delete(get_activity(session, project_id, activity_id))
    commit_changes(session)
