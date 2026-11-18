from collections.abc import Iterable
from decimal import Decimal

from app.evm.types import ActivityInput, EVMResult, Interpretation

ZERO = Decimal("0")
HUNDRED = Decimal("100")


def interpret_index(index: Decimal | None) -> Interpretation | None:
    """Interpret CPI or SPI relative to one; undefined remains None."""
    if index is None:
        return None
    if not isinstance(index, Decimal):
        raise TypeError("index must be a Decimal or None")
    if not index.is_finite():
        raise ValueError("index must be finite")
    if index > 1:
        return "favorable"
    if index < 1:
        return "desfavorable"
    return "según lo previsto"


def _value_at_progress(bac: Decimal, progress: Decimal) -> Decimal:
    return bac * progress / HUNDRED


def _ratio(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    return None if denominator == ZERO else numerator / denominator


def _calculate_metrics(
    bac: Decimal, pv: Decimal, ev: Decimal, ac: Decimal
) -> EVMResult:
    cpi = _ratio(ev, ac)
    spi = _ratio(ev, pv)
    eac = None if cpi is None or cpi == ZERO else bac / cpi
    vac = None if eac is None else bac - eac
    return EVMResult(
        bac=bac,
        pv=pv,
        ev=ev,
        ac=ac,
        cv=ev - ac,
        sv=ev - pv,
        cpi=cpi,
        spi=spi,
        eac=eac,
        vac=vac,
        cpi_interpretation=interpret_index(cpi),
        spi_interpretation=interpret_index(spi),
    )


def calculate_activity(activity: ActivityInput) -> EVMResult:
    """Calculate all EVM metrics for one validated activity."""
    return _calculate_metrics(
        bac=activity.bac,
        pv=_value_at_progress(activity.bac, activity.planned_progress),
        ev=_value_at_progress(activity.bac, activity.actual_progress),
        ac=activity.ac,
    )


def calculate_project(activities: Iterable[ActivityInput]) -> EVMResult:
    """Aggregate amounts first, then calculate indices (never average them).

    Accepts single-pass iterables. An empty collection has zero totals and
    undefined indices, estimates and interpretations.
    """
    bac = pv = ev = ac = ZERO
    for activity in activities:
        bac += activity.bac
        pv += _value_at_progress(activity.bac, activity.planned_progress)
        ev += _value_at_progress(activity.bac, activity.actual_progress)
        ac += activity.ac
    return _calculate_metrics(bac, pv, ev, ac)
