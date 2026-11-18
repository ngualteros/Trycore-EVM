from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

Interpretation = Literal["favorable", "desfavorable", "según lo previsto"]


@dataclass(frozen=True)
class ActivityInput:
    bac: Decimal
    planned_progress: Decimal
    actual_progress: Decimal
    ac: Decimal

    def __post_init__(self) -> None:
        for name in ("bac", "planned_progress", "actual_progress", "ac"):
            value = getattr(self, name)
            if not isinstance(value, Decimal):
                raise TypeError(f"{name} must be a Decimal")
            if not value.is_finite() or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        for name in ("planned_progress", "actual_progress"):
            if getattr(self, name) > 100:
                raise ValueError(f"{name} must be between 0 and 100")


@dataclass(frozen=True)
class EVMResult:
    bac: Decimal
    pv: Decimal
    ev: Decimal
    ac: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    cpi_interpretation: Interpretation | None
    spi_interpretation: Interpretation | None
