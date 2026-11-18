from decimal import Decimal, localcontext

import pytest

from app.models import Activity, Project

from .support import validate_test_url


@pytest.mark.parametrize("model", [Project, Activity])
@pytest.mark.parametrize("name", ["", " ", "\t\n", "a" * 151])
def test_reject_invalid_names(model, name):
    with pytest.raises(ValueError):
        model(name=name)


@pytest.mark.parametrize("model", [Project, Activity])
def test_name_must_be_a_string(model):
    with pytest.raises(TypeError):
        model(name=None)
    assert model(name="a" * 150).name == "a" * 150


@pytest.mark.parametrize(
    "field", ["bac", "actual_cost", "planned_progress_pct", "actual_progress_pct"]
)
@pytest.mark.parametrize("value", ["-0.001", "NaN", "Infinity", "1.001", "0.00001"])
def test_reject_invalid_decimal_values(field, value):
    with pytest.raises(ValueError):
        Activity(**{field: Decimal(value)})


@pytest.mark.parametrize("field", ["bac", "actual_cost"])
def test_money_boundary(field):
    assert getattr(Activity(**{field: Decimal("99999999999999.99")}), field) == Decimal(
        "99999999999999.99"
    )
    with pytest.raises(ValueError):
        Activity(**{field: Decimal("100000000000000.00")})


@pytest.mark.parametrize("field", ["planned_progress_pct", "actual_progress_pct"])
def test_progress_boundary(field):
    assert getattr(Activity(**{field: Decimal("100.00")}), field) == Decimal("100")
    with pytest.raises(ValueError):
        Activity(**{field: Decimal("100.001")})


def test_reject_float_and_validate_assignments():
    item = Activity(bac=Decimal("1.2300"))
    assert item.bac == Decimal("1.23")
    with pytest.raises(TypeError):
        item.bac = 1.2
    with pytest.raises(ValueError):
        item.bac = Decimal("-1")
    with localcontext() as context:
        context.prec = 2
        item.bac = Decimal("123.45")
    assert item.bac == Decimal("123.45")


@pytest.mark.parametrize(
    "url",
    [
        "sqlite://",
        "postgresql+psycopg://localhost/trycore_evm",
        "postgresql+psycopg://localhost/",
    ],
)
def test_reject_unsafe_test_database(url):
    with pytest.raises(ValueError):
        validate_test_url(url)


def test_reject_development_database_even_if_named_test():
    with pytest.raises(ValueError):
        validate_test_url(
            "postgresql+psycopg://localhost/example_test",
            "postgresql+psycopg://localhost/example_test",
        )
