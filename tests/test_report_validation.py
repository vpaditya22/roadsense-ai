from copy import deepcopy

import pytest

from roadsense.data import add_report, load_reports


def _valid_report():
    return {
        "report_id": "RS-VALIDATION",
        "issue_type": "Pothole",
        "road_name": "Test Road",
        "latitude": 22.72,
        "longitude": 75.85,
        "severity": 5,
        "traffic": 3,
        "safety_risk": 4,
        "age_days": 0,
        "vulnerable_users": False,
        "status": "New",
        "feedback": "Awaiting confirmation",
        "reported_at": "2026-11-24",
        "description": "Test report",
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("latitude", 90.01),
        ("latitude", -90.01),
        ("latitude", float("nan")),
        ("latitude", True),
        ("longitude", 180.01),
        ("longitude", -180.01),
        ("longitude", float("inf")),
        ("longitude", False),
    ],
)
def test_add_report_rejects_invalid_coordinates(field, value):
    report = _valid_report()
    report[field] = value

    with pytest.raises(ValueError, match=field):
        add_report(load_reports(), report)


def test_add_report_accepts_and_normalizes_numeric_coordinate_strings():
    report = _valid_report()
    report["latitude"] = "22.72"
    report["longitude"] = "75.85"

    added = add_report(load_reports(), report)

    assert added.iloc[0]["latitude"] == 22.72
    assert added.iloc[0]["longitude"] == 75.85
