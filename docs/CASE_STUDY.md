# RoadSense AI · Product case study

## Why this problem

Aditya's civil engineering training and field exposure make road maintenance a grounded domain for a product case study. During an engineering trainee placement at Maa Construction, he supported PCC road activities, material planning and quality checks. Earlier, as a diploma trainee with the Madhya Pradesh Rural Road Development Authority, he assisted with site surveys and documentation for a rural bridge project. His MS in Data Science & Management at IIT Indore and IIM Indore (expected 2028) adds a route to explore data-informed decisions.

This project complements his existing portfolio-risk dashboard by showing a different product problem and a public-service workflow. It does not imply municipal partnership or user research.

## Product thesis

If a road issue report captures a useful location and evidence, and a triage view makes urgency understandable, then residents may have a clearer way to report problems and staff may have a more consistent first-pass queue. This hypothesis needs validation with residents, municipal operations staff, and road engineers.

## Personas

1. **Asha, daily commuter:** Notices a pothole on her route; needs a fast report and a visible status.
2. **Ravi, municipal coordinator:** Receives reports from multiple channels; needs a manageable queue and clear escalation cues.
3. **Meera, field engineer:** Inspects conditions on site; needs evidence and context, while retaining final technical authority.

These illustrative personas are design tools, not interview findings.

## MVP experience

- Citizen flow captures issue type, location, severity, description and optional image.
- Operations view presents map, backlog metrics, workflow status, feedback and triage ranking.
- Priority score is a transparent heuristic with configurable weights; the app displays its rationale and limitations.
- Sample reports are synthetic. New reports and workflow updates exist only in Streamlit session state.

## Decisions and trade-offs

| Decision | Rationale | Cost / risk |
|---|---|---|
| Rule-based priority score | Explainable, deterministic, easy to test with no historical labels | Weights may not match local policy; human review is required |
| No live image model | Avoids unsupported accuracy claims, large downloads and unvalidated automation | Photos are not classified in this prototype |
| Session-only storage | Demonstrates an end-to-end flow without retaining personal data | No persistence or multi-user workflow |
| Synthetic Indore examples | Makes the map and dashboard useful on first launch | No operational conclusions can be drawn from the data |
| Streamlit single app | Low-friction portfolio demo and simple deployment | Not a production-scale citizen service |

## Success measurement plan

First test comprehension and completion with 5–8 residents and 3–5 staff/engineering reviewers, subject to access and consent. Do not treat this proposed sample as completed research. Observe report completion, time, location quality, score comprehension, override reasons, and map accessibility. Then run a small supervised pilot only with a municipal partner and an agreed service process.

Proposed initial targets: at least 80% report completion, under 60 seconds median reporting time, and at least 80% reviewer agreement that the score helps with first-pass sorting. These are targets for validation, not outcomes.

## Roadmap

1. **Prototype:** synthetic data, report form, map, transparent score, status/feedback loop.
2. **Discovery:** interview residents, coordinators and engineers; test accessibility and score explanations.
3. **Pilot foundation:** co-design taxonomy and service levels; add authentication, persistent database, audit logs, image retention controls and GIS validation.
4. **Operational pilot:** duplicate detection, staff override/reason codes, neighborhood fairness review, and outcome tracking.
5. **Model evaluation:** only if labeled representative images and governance exist; compare a model with the human baseline and publish precision/recall by relevant conditions before any operational use.

## Portfolio reflection

The central product decision is to show explainability and workflow value before adding AI. In infrastructure, an impressive prediction is not useful if a report cannot be located, reviewed, assigned, and confirmed. A next iteration should begin with stakeholder discovery and operational constraints rather than expanding model complexity.
