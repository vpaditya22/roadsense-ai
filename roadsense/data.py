"""Synthetic report data and local report-store helpers."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_reports.csv"


def load_reports(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the clearly labeled synthetic dataset used by the demo."""
    frame = pd.read_csv(path, parse_dates=["reported_at"])
    frame["priority"] = frame.apply(
        lambda row: _score_row(row), axis=1
    )
    return frame


def _score_row(row: pd.Series) -> int:
    from roadsense.scoring import score_priority

    return score_priority(
        row.severity, row.traffic, row.safety_risk, row.age_days, row.vulnerable_users,
    ).score


def add_report(reports: pd.DataFrame, report: dict) -> pd.DataFrame:
    """Append an in-session report; production persistence needs a backend."""
    required_fields = {
        "report_id", "issue_type", "road_name", "latitude", "longitude", "severity",
        "traffic", "safety_risk", "age_days", "vulnerable_users", "status", "feedback",
        "reported_at", "description",
    }
    if not isinstance(report, dict):
        raise ValueError("Report must be provided as a dictionary.")
    missing = required_fields - set(report)
    if missing:
        raise ValueError(f"Report is missing required fields: {', '.join(sorted(missing))}")

    normalized_report = dict(report)
    for field in ("issue_type", "road_name", "description"):
        value = report[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string.")
        normalized_report[field] = value.strip()
    if len(normalized_report["description"]) > 300:
        raise ValueError("description must be 300 characters or fewer.")

    report_id = report["report_id"]
    if not isinstance(report_id, str) or not report_id.strip():
        raise ValueError("Report ID must be a non-empty string.")
    normalized_id = report_id.strip()
    existing_ids = (
        reports["report_id"].dropna().astype(str).str.strip().str.casefold()
        if "report_id" in reports.columns
        else pd.Series(dtype="object")
    )
    if existing_ids.eq(normalized_id.casefold()).any():
        raise ValueError(f"Report ID already exists: {report_id}")

    normalized_report["report_id"] = normalized_id
    for field, lower, upper in (
        ("latitude", -90.0, 90.0),
        ("longitude", -180.0, 180.0),
    ):
        value = report[field]
        if isinstance(value, bool):
            raise ValueError(f"{field} must be finite and between {lower:g} and {upper:g}.")
        try:
            coordinate = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"{field} must be finite and between {lower:g} and {upper:g}."
            ) from exc
        if not math.isfinite(coordinate) or not lower <= coordinate <= upper:
            raise ValueError(f"{field} must be finite and between {lower:g} and {upper:g}.")
        normalized_report[field] = coordinate

    new_row = pd.DataFrame([normalized_report])
    new_row["priority"] = new_row.apply(_score_row, axis=1)
    return pd.concat([new_row, reports], ignore_index=True)
