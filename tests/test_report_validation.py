from copy import deepcopy

import pytest
import pandas as pd

from roadsense.data import add_report, load_reports, new_report_id


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

@pytest.mark.parametrize("duplicate_id", ["RS-TEST", " rs-test ", "RS-TEST "])
def test_add_report_rejects_ids_that_duplicate_after_trimming_and_casefolding(duplicate_id):
    reports = load_reports()
    reports.loc[len(reports)] = {**_valid_report(), "report_id": "RS-TEST"}
    report = _valid_report()
    report["report_id"] = duplicate_id

    with pytest.raises(ValueError, match="Report ID already exists"):
        add_report(reports, report)


def test_add_report_trims_new_report_ids():
    report = _valid_report()
    report["report_id"] = "  RS-TRIMMED  "

    added = add_report(load_reports(), report)

    assert added.iloc[0]["report_id"] == "RS-TRIMMED"


@pytest.mark.parametrize("field", ["issue_type", "road_name", "description"])
@pytest.mark.parametrize("value", ["", "   ", None])
def test_add_report_rejects_blank_or_non_text_descriptions(field, value):
    report = _valid_report()
    report[field] = value

    with pytest.raises(ValueError, match=field):
        add_report(load_reports(), report)


def test_add_report_trims_descriptive_text_and_rejects_overlong_description():
    report = _valid_report()
    report["issue_type"] = "  Pothole  "
    report["road_name"] = "  Test Road  "
    report["description"] = "  Uneven surface  "

    added = add_report(load_reports(), report)

    assert added.iloc[0]["issue_type"] == "Pothole"
    assert added.iloc[0]["road_name"] == "Test Road"
    assert added.iloc[0]["description"] == "Uneven surface"

    report["description"] = "x" * 301
    with pytest.raises(ValueError, match="300 characters or fewer"):
        add_report(load_reports(), report)


@pytest.mark.parametrize("reported_at", ["not-a-date", "", None, float("nan")])
def test_add_report_rejects_invalid_reported_at(reported_at):
    report = _valid_report()
    report["reported_at"] = reported_at

    with pytest.raises(ValueError, match="reported_at"):
        add_report(load_reports(), report)


def test_add_report_normalizes_reported_at_to_timestamp():
    report = _valid_report()

    added = add_report(load_reports(), report)

    assert added.iloc[0]["reported_at"] == pd.Timestamp("2026-11-24")


def test_new_report_ids_are_unique_and_keep_the_demo_prefix():
    identifiers = {new_report_id() for _ in range(100)}

    assert len(identifiers) == 100
    assert all(identifier.startswith("RS-") for identifier in identifiers)
