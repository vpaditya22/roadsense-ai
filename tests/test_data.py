from roadsense.data import add_report, load_reports


def test_sample_dataset_is_synthetic_and_scored():
    reports = load_reports()
    assert len(reports) >= 8
    assert reports["priority"].between(0, 100).all()
    assert reports["report_id"].str.startswith("RS-").all()


def test_add_report_appends_one_scored_row():
    reports = load_reports()
    report = {
        "report_id": "RS-TEST", "issue_type": "Pothole", "road_name": "Test Road",
        "latitude": 22.72, "longitude": 75.85, "severity": 5, "traffic": 3,
        "safety_risk": 4, "age_days": 0, "vulnerable_users": False,
        "status": "New", "feedback": "Awaiting confirmation",
        "reported_at": "2026-11-12", "description": "Test report",
    }
    updated = add_report(reports, report)
    assert len(updated) == len(reports) + 1
    assert updated.iloc[0]["report_id"] == "RS-TEST"
    assert updated.iloc[0]["priority"] > 0
