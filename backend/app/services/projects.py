from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project
from app.schemas.projects import ProjectWrite
from app.services.common import ResourceNotFound, commit_changes


def get_project(session: Session, project_id: int) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise ResourceNotFound("Project not found")
    return project


def list_projects(session: Session) -> list[Project]:
    return list(session.scalars(select(Project).order_by(Project.id)))


def create_project(session: Session, data: ProjectWrite) -> Project:
    project = Project(**data.model_dump())
    session.add(project)
    commit_changes(session)
    return project


def update_project(session: Session, project_id: int, data: ProjectWrite) -> Project:
    project = get_project(session, project_id)
    project.name = data.name
    project.description = data.description
    commit_changes(session)
    return project


def delete_project(session: Session, project_id: int) -> None:
    session.delete(get_project(session, project_id))
    commit_changes(session)
