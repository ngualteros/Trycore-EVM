from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Identity, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.models.base import Base
from app.models.validation import validate_name

if TYPE_CHECKING:
    from app.models.activity import Activity


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("name ~ '[^[:space:]]'", name="ck_projects_name_not_blank"),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    activities: Mapped[list[Activity]] = relationship(
        back_populates="project", cascade="all, delete-orphan", passive_deletes=True
    )

    @validates("name")
    def validate_project_name(self, key: str, value: str) -> str:
        return validate_name(value)
