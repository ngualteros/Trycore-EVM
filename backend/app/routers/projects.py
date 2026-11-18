from fastapi import APIRouter, Response, status

from app.routers.common import ERROR_RESPONSES, DatabaseSession, ResourceId
from app.schemas.projects import ProjectRead, ProjectWrite
from app.services import projects

router = APIRouter(prefix="/api/projects", tags=["projects"], responses=ERROR_RESPONSES)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectWrite, session: DatabaseSession):
    return projects.create_project(session, data)


@router.get("", response_model=list[ProjectRead])
def list_projects(session: DatabaseSession):
    return projects.list_projects(session)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: ResourceId, session: DatabaseSession):
    return projects.get_project(session, project_id)


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: ResourceId, data: ProjectWrite, session: DatabaseSession
):
    return projects.update_project(session, project_id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: ResourceId, session: DatabaseSession) -> Response:
    projects.delete_project(session, project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
