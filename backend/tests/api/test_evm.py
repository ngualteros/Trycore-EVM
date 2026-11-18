from decimal import Decimal

import pytest

from .test_crud import activity_body, create_project

pytestmark = pytest.mark.integration
D = Decimal


def test_required_evm_case(client):
    project_id = create_project(client)
    base = f"/api/projects/{project_id}"
    values = [
        ("Analysis", "10", "80", "100", "9", "8", "10", "1", "2", "9", "1"),
        ("Development", "20", "60", "40", "12", "12", "8", "-4", "-4", "30", "-10"),
        ("Testing", "30", "50", "50", "16", "15", "15", "-1", "0", "32", "-2"),
    ]
    for name, bac, planned, actual, ac, pv, ev, cv, sv, eac, vac in values:
        response = client.post(
            base + "/activities",
            json=activity_body(
                name=name,
                bac=bac,
                planned_progress_pct=planned,
                actual_progress_pct=actual,
                actual_cost=ac,
            ),
        )
        assert response.status_code == 201
        metrics_response = client.get(base + f"/activities/{response.json()['id']}/evm")
        assert metrics_response.status_code == 200
        metrics = metrics_response.json()
        expected = dict(bac=bac, pv=pv, ev=ev, ac=ac, cv=cv, sv=sv, eac=eac, vac=vac)
        for field, number in expected.items():
            assert isinstance(metrics[field], str)
            assert D(metrics[field]) == pytest.approx(
                D(number), rel=D(0), abs=D("1e-24")
            )
        assert D(metrics["cpi"]) == D(ev) / D(ac)
        assert D(metrics["spi"]) == D(ev) / D(pv)
    response = client.get(base + "/evm")
    assert response.status_code == 200
    result = response.json()
    expected = dict(bac="60", pv="35", ev="33", ac="37", cv="-4", sv="-2")
    for field, value in expected.items():
        assert isinstance(result[field], str)
        assert D(result[field]) == D(value)
    assert D(result["cpi"]) == D(33) / D(37)
    assert D(result["spi"]) == D(33) / D(35)
    assert D(result["eac"]) == pytest.approx(D(740) / D(11), rel=D(0), abs=D("1e-24"))
    assert D(result["vac"]) == pytest.approx(D(-80) / D(11), rel=D(0), abs=D("1e-24"))
    assert (
        result["cpi_interpretation"] == result["spi_interpretation"] == "desfavorable"
    )


def test_empty_project_evm(client):
    project_id = create_project(client)
    response = client.get(f"/api/projects/{project_id}/evm")
    assert response.status_code == 200
    result = response.json()
    for field in ("bac", "pv", "ev", "ac", "cv", "sv"):
        assert result[field] == "0"
    for field in (
        "cpi",
        "spi",
        "eac",
        "vac",
        "cpi_interpretation",
        "spi_interpretation",
    ):
        assert field in result and result[field] is None


@pytest.mark.parametrize(
    "planned,actual,cost,cpi,spi,interpretation",
    [
        ("0", "0", "0", None, None, None),
        ("50", "0", "1", "0", "0", "desfavorable"),
        ("50", "50", "0", None, "1", None),
        ("0", "50", "5", "1", None, "según lo previsto"),
        ("50", "100", "5", "2", "2", "favorable"),
    ],
)
def test_evm_zero_and_interpretation_contract(
    client, planned, actual, cost, cpi, spi, interpretation
):
    project_id = create_project(client)
    base = f"/api/projects/{project_id}"
    response = client.post(
        base + "/activities",
        json=activity_body(
            planned_progress_pct=planned, actual_progress_pct=actual, actual_cost=cost
        ),
    )
    activity_id = response.json()["id"]
    for path in (base + "/evm", base + f"/activities/{activity_id}/evm"):
        result = client.get(path).json()
        for field, expected in (("cpi", cpi), ("spi", spi)):
            if expected is None:
                assert result[field] is None
            else:
                assert isinstance(result[field], str) and D(result[field]) == D(
                    expected
                )
        assert result["cpi_interpretation"] == interpretation
        if cpi is None or cpi == "0":
            assert result["eac"] is None and result["vac"] is None
