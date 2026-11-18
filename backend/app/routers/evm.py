from fastapi import APIRouter

from app.routers.common import ERROR_RESPONSES, DatabaseSession, ResourceId
from app.schemas.evm import EVMRead
from app.services import evm

router = APIRouter(prefix="/api/projects", tags=["evm"], responses=ERROR_RESPONSES)


@router.get("/{project_id}/evm", response_model=EVMRead)
def project_evm(project_id: ResourceId, session: DatabaseSession):
    return evm.project_evm(session, project_id)


@router.get("/{project_id}/activities/{activity_id}/evm", response_model=EVMRead)
def activity_evm(
    project_id: ResourceId, activity_id: ResourceId, session: DatabaseSession
):
    return evm.activity_evm(session, project_id, activity_id)
