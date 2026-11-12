import pytest

from roadsense.scoring import score_priority


def test_score_is_bounded_and_has_explainable_components():
    result = score_priority(5, 5, 5, 30, True)
    assert result.score == 100
    assert result.tier == "Urgent"
    assert sum(result.factors.values()) == result.score


def test_priority_increases_with_severity_and_wait_time():
    base = score_priority(2, 3, 2, 0)
    more_severe = score_priority(5, 3, 2, 0)
    older = score_priority(2, 3, 2, 30)
    assert more_severe.score > base.score
    assert older.score > base.score


def test_vulnerable_user_context_adds_ten_points():
    without = score_priority(3, 3, 3, 10)
    with_context = score_priority(3, 3, 3, 10, True)
    assert with_context.score - without.score == 10


@pytest.mark.parametrize("kwargs", [
    {"severity": 0, "traffic": 3, "safety_risk": 3, "age_days": 1},
    {"severity": 3, "traffic": 6, "safety_risk": 3, "age_days": 1},
    {"severity": 3, "traffic": 3, "safety_risk": 3, "age_days": -1},
])
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError):
        score_priority(**kwargs)
