# RoadSense AI

**A road issue reporting and repair triage prototype for a Google APM portfolio.** Built with Python, Streamlit, pandas, and Plotly.

Residents can submit an in-session road issue report; a municipal-style dashboard maps sample reports, displays workflow KPIs, sorts a repair queue with an explainable priority score, and captures status and community feedback.

> **Portfolio demo only.** All provided reports and dashboard metrics are synthetic. Map points are illustrative Indore locations. This app is not connected to a municipality, does not dispatch repairs, and does not run an image-classification model. Submitted reports and workflow edits live only in the active browser session.

## Product preview

The first run opens with a synthetic operations dashboard. Use the workspace switcher to try the citizen report flow and the interactive priority explanation. No account or API key is required.

## Run locally

Python 3.10 or newer is required.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Run tests and checks

```bash
pytest
python -m compileall -q app.py roadsense tests
```

GitHub Actions runs the test suite, compile check and Streamlit health check on pushes and pull requests to `main`.

## What is implemented

- **Citizen intake:** issue type, location, severity, description, optional photo selection, consent notice and clear in-session acknowledgement.
- **Interactive map:** filterable report locations in the Indore demo area.
- **Explainable priority:** weighted score from severity (35%), traffic exposure (20%), safety risk (25%), time waiting (10%) and vulnerable road-user context (10%). Review the factors and thresholds in the app.
- **Municipal dashboard:** open/urgent/resolved counts, backlog by status, triage queue and issue/status filters.
- **Workflow:** update report status and community feedback; changes are in-session only.
- **Prototype image boundary:** image upload is available to demonstrate report capture. The active Streamlit server receives the image in session memory; this prototype does not write it to disk or a database and does not classify it. No model accuracy is claimed.

## Architecture

```text
app.py (Streamlit entrypoint)
  └── roadsense/ui.py       views, report capture, dashboard, workflow
      ├── roadsense/data.py CSV loading and in-session report updates
      └── roadsense/scoring.py deterministic, explainable score
data/sample_reports.csv     synthetic demo records
tests/                      scoring and data behavior
docs/                        PRD, case study and product decisions
```

The app separates scoring and data operations from the Streamlit UI so the decision logic can be tested independently. A production architecture would add an authenticated API, persistent database, object storage with retention policy, municipal GIS integration, observability, and role-based access.

## Product and domain context

This project draws on Aditya Vikram Pandey's CV: civil engineering education, PCC road-construction support at Maa Construction, rural bridge survey/documentation exposure with the Madhya Pradesh Rural Road Development Authority, and current MSDSM studies at IIT Indore and IIM Indore. It complements his existing portfolio analytics work with a civic infrastructure problem and an explicit product workflow. It makes no claim of user research, municipal partnership, or measured impact.

See [Product requirements](docs/PRD.md) and [Product case study](docs/CASE_STUDY.md) for personas, assumptions, proposed success metrics, trade-offs, privacy/accessibility considerations and roadmap.

## Privacy and accessibility

- The form does not ask for a name, phone number or account.
- Report details remain in session state. An optional photo is received by the active Streamlit server in session memory, but is not saved to disk or a database; both are lost when the session ends. Do not submit sensitive photos or real personal information.
- Production would need informed consent, data minimization, secure image handling, location precision controls, retention/deletion rules and role-based access.
- Controls use labels and text status in addition to color. A production map should have a fully equivalent searchable list, keyboard-accessible map interactions, screen-reader descriptions, localization and field testing with people with disabilities.

## Limitations and next steps

- No CV model, duplicate detection, authentication, database, city connection or actual work order integration.
- Scoring factors and thresholds are unvalidated product assumptions, not engineering standards.
- Sample records, locations and operational KPIs are simulated for demonstration.
- Prioritize stakeholder discovery and usability/accessibility validation before collecting real reports or training a classifier.

## License

MIT. See [LICENSE](LICENSE).
