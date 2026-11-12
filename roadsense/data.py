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
        int(row.severity), int(row.traffic), int(row.safety_risk), int(row.age_days),
        bool(row.vulnerable_users),
    ).score


def add_report(reports: pd.DataFrame, report: dict) -> pd.DataFrame:
    """Append an in-session report; production persistence needs a backend."""
    new_row = pd.DataFrame([report])
    new_row["priority"] = new_row.apply(_score_row, axis=1)
    return pd.concat([new_row, reports], ignore_index=True)
