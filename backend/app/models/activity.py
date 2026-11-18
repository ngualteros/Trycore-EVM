from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Identity, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.models.base import Base
from app.models.validation import (
    MAX_MONEY,
    MAX_PROGRESS,
    validate_amount,
    validate_name,
)

if TYPE_CHECKING:
    from app.models.project import Project


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("name ~ '[^[:space:]]'", name="ck_activities_name_not_blank"),
        CheckConstraint(
            "bac >= 0 AND bac <= 99999999999999.99", name="ck_activities_bac_range"
        ),
        CheckConstraint(
            "actual_cost >= 0 AND actual_cost <= 99999999999999.99",
            name="ck_activities_actual_cost_range",
        ),
        CheckConstraint(
            "planned_progress_pct >= 0 AND planned_progress_pct <= 100",
            name="ck_activities_planned_progress_range",
        ),
        CheckConstraint(
            "actual_progress_pct >= 0 AND actual_progress_pct <= 100",
            name="ck_activities_actual_progress_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", name="fk_activities_project", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    bac: Mapped[Decimal] = mapped_column(Numeric(16, 2, asdecimal=True), nullable=False)
    planned_progress_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2, asdecimal=True), nullable=False
    )
    actual_progress_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2, asdecimal=True), nullable=False
    )
    actual_cost: Mapped[Decimal] = mapped_column(
        Numeric(16, 2, asdecimal=True), nullable=False
    )
    project: Mapped[Project] = relationship(back_populates="activities")

    @validates("name")
    def validate_activity_name(self, key: str, value: str) -> str:
        return validate_name(value)

    @validates("bac", "actual_cost", "planned_progress_pct", "actual_progress_pct")
    def validate_numeric_value(self, key: str, value: Decimal) -> Decimal:
        maximum = MAX_MONEY if key in ("bac", "actual_cost") else MAX_PROGRESS
        return validate_amount(key, value, maximum)
