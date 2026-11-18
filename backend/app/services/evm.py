from sqlalchemy.orm import Session

from app.evm import ActivityInput, EVMResult, calculate_activity, calculate_project
from app.models import Activity
from app.services.activities import get_activity, list_activities


def to_evm_input(activity: Activity) -> ActivityInput:
    return ActivityInput(
        bac=activity.bac,
        planned_progress=activity.planned_progress_pct,
        actual_progress=activity.actual_progress_pct,
        ac=activity.actual_cost,
    )


def activity_evm(session: Session, project_id: int, activity_id: int) -> EVMResult:
    return calculate_activity(
        to_evm_input(get_activity(session, project_id, activity_id))
    )


def project_evm(session: Session, project_id: int) -> EVMResult:
    return calculate_project(
        to_evm_input(item) for item in list_activities(session, project_id)
    )
