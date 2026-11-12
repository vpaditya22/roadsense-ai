# RoadSense AI · Product requirements

## Product summary

RoadSense AI is a portfolio prototype for a two-sided road maintenance workflow: residents report visible street damage and municipal teams review a transparent triage queue. The demo uses synthetic Indore-area reports and an explainable heuristic score. It is not connected to a municipality and does not create real service requests.

## Problem framing

Road issues can be difficult for residents to route and hard for operations teams to compare consistently. A focused product opportunity is to improve report quality and make the first review decision easier, while preserving engineering judgment and public accountability.

## Users and jobs to be done

- **Resident / commuter:** “When I spot a road hazard, help me send a useful report quickly and know what happened next.”
- **Municipal triage coordinator:** “When reports arrive from different places, help me see where they are, what might be urgent, and what needs follow-up.”
- **Road engineer / field inspector:** “When a queue suggests urgency, give me the underlying evidence so I can inspect the site and make a safe technical decision.”

These are product-design personas, not findings from user research.

## MVP scope

1. Submit an issue type, street or landmark, approximate coordinates, severity, description, and optional photo.
2. See synthetic and in-session reports on a map and in a sortable priority queue.
3. Filter by issue and workflow status; update status and resident feedback.
4. Explain the score components and let a reviewer explore the assumptions.
5. Clearly disclose prototype data, session-only storage, and lack of live model inference.

## Out of scope

Production intake, authentication, city GIS integration, dispatch/work orders, guaranteed service-level commitments, public user accounts, persistent database, automated image classification, and an engineering condition assessment.

## Product assumptions and trade-offs

- A rule-based score is legible and testable for an MVP; a learned ranker would require representative labeled history and fairness review.
- The demo map is centered on Indore to connect the portfolio project to civil engineering field experience; points are illustrative, not verified locations.
- Session state makes the reporting loop demonstrable without collecting personal data. It also means reports disappear when the session ends.
- Photos are received by the active Streamlit server in session memory for the reporting flow but are not persisted or analyzed. Avoiding a heavyweight model keeps setup simple and avoids implying unsupported accuracy.
- Severity, traffic, safety, age and vulnerable-user weights are product hypotheses. A municipal engineer and policy owner would need to calibrate them.

## Success metrics

No user research or live product performance is claimed. Proposed targets should be validated in usability studies and a controlled pilot:

| Metric | Definition | Illustrative target |
|---|---|---:|
| Report completion rate | Submitted reports / report starts | ≥ 80% |
| Median report time | Start to successful submission | < 60 sec |
| Report completeness | Reports with actionable location and issue detail | ≥ 90% |
| Triage usefulness | Share of reviewed reports where staff say score supports first-pass ordering | ≥ 80% |
| Status freshness | Open reports with a status update within the agreed service window | Baseline first, then improve |
| Equity check | Differences in completion and triage outcomes by neighborhood / access mode | No unexplained material gap |

The dashboard numbers in the app are synthetic and must not be presented as achieved results.

## Risks and mitigations

- **Incorrect location or duplicated reports:** add geospatial duplicate suggestions and staff confirmation in a later phase.
- **Score bias or misplaced trust:** display factors, thresholds and uncertainty; permit human override with reason; audit by neighborhood and road-user group.
- **Unsafe exposure of personal information:** avoid names and phone numbers in the demo; production should minimize collection, restrict access, define retention and redact image metadata.
- **Accessibility barriers:** support keyboard operation, visible labels, non-color status cues, plain language, high contrast and a text alternative to map-only navigation.
- **False expectation of municipal action:** label the prototype persistently and use explicit confirmation language.

## Release acceptance

- A resident can submit a valid in-session report and receive a clear acknowledgement.
- A municipal reviewer can filter a queue, understand score factors, update status, and record feedback.
- Invalid score inputs are rejected; score output is bounded and deterministic.
- Synthetic data and unsupported capabilities are explicitly labeled.
- Automated tests and CI run on pushes and pull requests.
