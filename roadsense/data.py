"""Synthetic report data and local report-store helpers."""

from __future__ import annotations

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
    report_id = report["report_id"]
    if not isinstance(report_id, str) or not report_id.strip():
        raise ValueError("Report ID must be a non-empty string.")
    if "report_id" in reports.columns and reports["report_id"].eq(report_id).any():
        raise ValueError(f"Report ID already exists: {report_id}")

    new_row = pd.DataFrame([report])
    new_row["priority"] = new_row.apply(_score_row, axis=1)
    return pd.concat([new_row, reports], ignore_index=True)
