from decimal import Decimal, localcontext

import pytest

from app.evm import (
    ActivityInput,
    calculate_activity,
    calculate_project,
    interpret_index,
)

D = Decimal


@pytest.fixture(autouse=True)
def decimal_context():
    with localcontext() as context:
        context.prec = 28
        yield


def activity(bac="100", planned="50", actual="40", ac="50"):
    return ActivityInput(D(bac), D(planned), D(actual), D(ac))


@pytest.mark.parametrize(
    ("inputs", "pv", "ev", "cv", "sv", "cpi", "spi", "eac", "vac"),
    [
        (("10", "80", "100", "9"), "8", "10", "1", "2", (10, 9), (5, 4), "9", "1"),
        (
            ("20", "60", "40", "12"),
            "12",
            "8",
            "-4",
            "-4",
            (2, 3),
            (2, 3),
            "30",
            "-10",
        ),
        (
            ("30", "50", "50", "16"),
            "15",
            "15",
            "-1",
            "0",
            (15, 16),
            (1, 1),
            "32",
            "-2",
        ),
    ],
)
def test_individual_formulas(inputs, pv, ev, cv, sv, cpi, spi, eac, vac):
    result = calculate_activity(activity(*inputs))

    assert result.bac == D(inputs[0])
    assert result.ac == D(inputs[3])
    assert (result.pv, result.ev, result.cv, result.sv) == tuple(
        map(D, (pv, ev, cv, sv))
    )
    assert result.cpi == D(cpi[0]) / D(cpi[1])
    assert result.spi == D(spi[0]) / D(spi[1])
    assert result.eac == pytest.approx(D(eac), rel=D("0"), abs=D("1e-24"))
    assert result.vac == pytest.approx(D(vac), rel=D("0"), abs=D("1e-24"))


def test_required_project_case():
    result = calculate_project(
        [
            activity("10", "80", "100", "9"),
            activity("20", "60", "40", "12"),
            activity("30", "50", "50", "16"),
        ]
    )

    assert (result.bac, result.pv, result.ev, result.ac) == tuple(
        map(D, ("60", "35", "33", "37"))
    )
    assert (result.cv, result.sv) == (D("-4"), D("-2"))
    assert result.cpi == D(33) / D(37)
    assert result.spi == D(33) / D(35)
    assert result.eac == pytest.approx(D(740) / D(11), rel=D(0), abs=D("1e-24"))
    assert result.vac == pytest.approx(D(-80) / D(11), rel=D(0), abs=D("1e-24"))
    assert result.cpi_interpretation == "desfavorable"
    assert result.spi_interpretation == "desfavorable"


def test_project_uses_totals_not_average_indices_and_accepts_generators():
    activities = [activity("100", "10", "20", "10"), activity("100", "90", "90", "90")]
    first, second = map(calculate_activity, activities)
    result = calculate_project(item for item in activities)

    assert result.cpi == result.spi == D("1.1")
    assert result.cpi != (first.cpi + second.cpi) / D(2)
    assert result.spi != (first.spi + second.spi) / D(2)
    assert result.cpi_interpretation == result.spi_interpretation == "favorable"


def test_project_includes_values_from_activities_with_undefined_indices():
    result = calculate_project(
        [activity("100", "0", "50", "0"), activity("100", "100", "50", "100")]
    )

    assert (result.bac, result.pv, result.ev, result.ac) == tuple(
        map(D, ("200", "100", "100", "100"))
    )
    assert result.cpi == result.spi == D(1)
    assert result.eac == D(200)
    assert result.vac == D(0)
    assert result.cpi_interpretation == result.spi_interpretation == "según lo previsto"


@pytest.mark.parametrize("activities", [[], iter(())])
def test_empty_project(activities):
    result = calculate_project(activities)

    for name in ("bac", "pv", "ev", "ac", "cv", "sv"):
        assert getattr(result, name) == D(0)
        assert isinstance(getattr(result, name), Decimal)
    for name in (
        "cpi",
        "spi",
        "eac",
        "vac",
        "cpi_interpretation",
        "spi_interpretation",
    ):
        assert getattr(result, name) is None


@pytest.mark.parametrize(
    "calculate", [calculate_activity, lambda a: calculate_project([a])]
)
@pytest.mark.parametrize(
    ("inputs", "cpi", "spi", "eac", "vac"),
    [
        (("100", "50", "50", "0"), None, "1", None, None),
        (("100", "0", "50", "25"), "2", None, "50", "50"),
        (("100", "50", "0", "25"), "0", "0", None, None),
        (("100", "0", "0", "0"), None, None, None, None),
        (("0", "100", "100", "25"), "0", None, None, None),
        (("0", "0", "0", "0"), None, None, None, None),
    ],
)
def test_zero_denominators_and_zero_budget(calculate, inputs, cpi, spi, eac, vac):
    result = calculate(activity(*inputs))

    for name, expected in (("cpi", cpi), ("spi", spi), ("eac", eac), ("vac", vac)):
        if expected is None:
            assert getattr(result, name) is None
        else:
            assert getattr(result, name) == D(expected)
    assert result.cpi_interpretation == interpret_index(result.cpi)
    assert result.spi_interpretation == interpret_index(result.spi)


@pytest.mark.parametrize(
    ("index", "expected"),
    [
        (None, None),
        (D("0"), "desfavorable"),
        (D("0.9999999999999999999999999999"), "desfavorable"),
        (D("1"), "según lo previsto"),
        (D("1.000000000000000000000000001"), "favorable"),
    ],
)
def test_interpretation(index, expected):
    assert interpret_index(index) == expected


def test_fractional_values_are_not_quantized():
    result = calculate_activity(activity("123.4567", "12.345", "67.891", "43.2109"))

    assert result.pv == D("15.240729615")
    assert result.ev == D("83.815988197")
    assert result.cv == D("40.605088197")
    assert result.sv == D("68.575258582")
    assert result.cpi == result.ev / D("43.2109")
    assert result.spi == result.ev / result.pv
    assert result.eac == result.bac / result.cpi
    assert result.vac == result.bac - result.eac


def test_repeating_fractions_respect_callers_precision():
    with localcontext() as context:
        context.prec = 50
        result = calculate_activity(activity("1", "100", "100", "3"))
        assert result.cpi == D(1) / D(3)
        assert len(result.cpi.as_tuple().digits) == 50
        assert result.eac == pytest.approx(D(3), rel=D(0), abs=D("1e-48"))


@pytest.mark.parametrize("field", ["bac", "planned_progress", "actual_progress", "ac"])
@pytest.mark.parametrize(
    "value", [D("-0.01"), D("NaN"), D("sNaN"), D("Infinity"), D("-Infinity")]
)
def test_reject_negative_and_nonfinite_inputs(field, value):
    values = dict(bac=D(100), planned_progress=D(50), actual_progress=D(50), ac=D(50))
    values[field] = value
    with pytest.raises(ValueError, match=field):
        ActivityInput(**values)


@pytest.mark.parametrize("field", ["planned_progress", "actual_progress"])
def test_reject_progress_above_one_hundred(field):
    values = dict(bac=D(100), planned_progress=D(50), actual_progress=D(50), ac=D(50))
    values[field] = D("100.0001")
    with pytest.raises(ValueError, match=field):
        ActivityInput(**values)


@pytest.mark.parametrize("field", ["bac", "planned_progress", "actual_progress", "ac"])
@pytest.mark.parametrize("value", [0.1, 1, "1", True, None])
def test_reject_non_decimal_inputs(field, value):
    values = dict(bac=D(100), planned_progress=D(50), actual_progress=D(50), ac=D(50))
    values[field] = value
    with pytest.raises(TypeError, match=field):
        ActivityInput(**values)


@pytest.mark.parametrize("value", [D("NaN"), D("sNaN"), D("Infinity"), D("-Infinity")])
def test_reject_nonfinite_index(value):
    with pytest.raises(ValueError, match="finite"):
        interpret_index(value)


def test_reject_float_index():
    with pytest.raises(TypeError, match="Decimal"):
        interpret_index(1.0)
