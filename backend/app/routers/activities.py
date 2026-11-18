from fastapi import APIRouter, Response, status

from app.routers.common import ERROR_RESPONSES, DatabaseSession, ResourceId
from app.schemas.activities import ActivityRead, ActivityWrite
from app.services import activities

router = APIRouter(
    prefix="/api/projects/{project_id}/activities",
    tags=["activities"],
    responses=ERROR_RESPONSES,
)


@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(
    project_id: ResourceId, data: ActivityWrite, session: DatabaseSession
):
    return activities.create_activity(session, project_id, data)


@router.get("", response_model=list[ActivityRead])
def list_activities(project_id: ResourceId, session: DatabaseSession):
    return activities.list_activities(session, project_id)


@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(
    project_id: ResourceId, activity_id: ResourceId, session: DatabaseSession
):
    return activities.get_activity(session, project_id, activity_id)


@router.put("/{activity_id}", response_model=ActivityRead)
def update_activity(
    project_id: ResourceId,
    activity_id: ResourceId,
    data: ActivityWrite,
    session: DatabaseSession,
):
    return activities.update_activity(session, project_id, activity_id, data)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    project_id: ResourceId, activity_id: ResourceId, session: DatabaseSession
) -> Response:
    activities.delete_activity(session, project_id, activity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
