"""Explainable, deterministic repair-priority scoring for demonstration use."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorityResult:
    score: int
    tier: str
    factors: dict[str, int]


def score_priority(
    severity: int,
    traffic: int,
    safety_risk: int,
    age_days: int,
    vulnerable_users: bool = False,
) -> PriorityResult:
    """Return a transparent 0–100 score from normalized product assumptions.

    Severity, traffic, safety risk, report age, and vulnerable road-user exposure
    are weighted 35/20/25/10/10. The score supports triage; it is not an
    engineering assessment or an automated work order.
    """
    values = {"severity": severity, "traffic": traffic, "safety_risk": safety_risk}
    if any(not 1 <= value <= 5 for value in values.values()):
        raise ValueError("Severity, traffic, and safety risk must be between 1 and 5.")
    if age_days < 0:
        raise ValueError("age_days cannot be negative.")

    normalized = {
        "severity": round((severity - 1) / 4 * 35),
        "traffic": round((traffic - 1) / 4 * 20),
        "safety_risk": round((safety_risk - 1) / 4 * 25),
        "report_age": round(min(age_days, 30) / 30 * 10),
        "vulnerable_users": 10 if vulnerable_users else 0,
    }
    score = min(100, sum(normalized.values()))
    tier = "Urgent" if score >= 70 else "High" if score >= 50 else "Standard"
    return PriorityResult(score=score, tier=tier, factors=normalized)
