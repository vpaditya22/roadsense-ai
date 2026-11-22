"""Explainable, deterministic repair-priority scoring for demonstration use."""

from __future__ import annotations

from dataclasses import dataclass
import math


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
    normalized_inputs = {}
    for name, value in values.items():
        if isinstance(value, bool):
            raise ValueError("Severity, traffic, and safety risk must be whole numbers between 1 and 5.")
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Severity, traffic, and safety risk must be whole numbers between 1 and 5.") from exc
        if not math.isfinite(numeric_value) or not numeric_value.is_integer() or not 1 <= numeric_value <= 5:
            raise ValueError("Severity, traffic, and safety risk must be whole numbers between 1 and 5.")
        normalized_inputs[name] = int(numeric_value)

    if isinstance(age_days, bool):
        raise ValueError("age_days must be a non-negative whole number.")
    try:
        numeric_age = float(age_days)
    except (TypeError, ValueError) as exc:
        raise ValueError("age_days must be a non-negative whole number.") from exc
    if not math.isfinite(numeric_age) or not numeric_age.is_integer() or numeric_age < 0:
        raise ValueError("age_days must be a non-negative whole number.")
    if not isinstance(vulnerable_users, bool):
        raise ValueError("vulnerable_users must be a boolean.")

    normalized = {
        "severity": round((normalized_inputs["severity"] - 1) / 4 * 35),
        "traffic": round((normalized_inputs["traffic"] - 1) / 4 * 20),
        "safety_risk": round((normalized_inputs["safety_risk"] - 1) / 4 * 25),
        "report_age": round(min(int(numeric_age), 30) / 30 * 10),
        "vulnerable_users": 10 if vulnerable_users else 0,
    }
    score = min(100, sum(normalized.values()))
    tier = "Urgent" if score >= 70 else "High" if score >= 50 else "Standard"
    return PriorityResult(score=score, tier=tier, factors=normalized)
