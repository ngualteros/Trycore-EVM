from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator

from app.models.validation import MAX_MONEY, MAX_PROGRESS, validate_amount
from app.schemas.projects import Name


def require_decimal_string(value: object) -> object:
    """JSON numbers may already have lost precision before validation."""
    if not isinstance(value, (str, Decimal)):
        raise ValueError("Decimal values must be supplied as strings")
    return value


DecimalInput = Annotated[
    Decimal, BeforeValidator(require_decimal_string, json_schema_input_type=str)
]
Money = Annotated[
    DecimalInput, Field(ge=0, le=MAX_MONEY, max_digits=16, decimal_places=2)
]
Progress = Annotated[
    DecimalInput, Field(ge=0, le=MAX_PROGRESS, max_digits=5, decimal_places=2)
]


class ActivityWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Name
    bac: Money
    planned_progress_pct: Progress
    actual_progress_pct: Progress
    actual_cost: Money

    @field_validator(
        "bac", "actual_cost", "planned_progress_pct", "actual_progress_pct"
    )
    @classmethod
    def validate_numeric_fields(cls, value: Decimal, info) -> Decimal:
        maximum = (
            MAX_MONEY if info.field_name in ("bac", "actual_cost") else MAX_PROGRESS
        )
        return validate_amount(info.field_name, value, maximum)


class ActivityRead(ActivityWrite):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    project_id: int
