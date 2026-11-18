from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, StringConstraints

from app.models.validation import validate_name

Name = Annotated[
    str,
    StringConstraints(strict=True, min_length=1, max_length=150),
    AfterValidator(validate_name),
]


class ProjectWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Name
    description: str | None = None


class ProjectRead(ProjectWrite):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
