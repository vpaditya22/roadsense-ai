"""Streamlit views for citizen reporting and municipal triage."""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from roadsense.data import add_report
from roadsense.scoring import score_priority

STATUS_ORDER = ["New", "Assigned", "In progress", "Resolved"]


def render_app(reports: pd.DataFrame) -> None:
    if "reports" not in st.session_state:
        st.session_state.reports = reports
    st.markdown("<div class='eyebrow'>CITY OPERATIONS • PROTOTYPE</div>", unsafe_allow_html=True)
    st.title("RoadSense AI")
    st.caption("A shared view of street issues, repair urgency, and community feedback.")
    st.info("Demo workspace · all dashboard reports and performance figures are synthetic. Reports you submit stay in this browser session.", icon="🧪")

    page = st.radio("Choose a workspace", ["City dashboard", "Report an issue", "How prioritization works"], horizontal=True, label_visibility="collapsed")
    if page == "Report an issue":
        render_report_form()
    elif page == "How prioritization works":
        render_scoring_guide()
    else:
        render_dashboard(st.session_state.reports)


def render_dashboard(reports: pd.DataFrame) -> None:
    with st.sidebar:
        st.header("Explore reports")
        status_filter = st.multiselect("Status", STATUS_ORDER, default=STATUS_ORDER)
        issue_filter = st.multiselect("Issue type", sorted(reports.issue_type.unique()), default=sorted(reports.issue_type.unique()))
        st.divider()
        st.caption("Prototype boundary")
        st.caption("No live city feeds, dispatch, or model inference are connected.")

    filtered = reports[reports.status.isin(status_filter) & reports.issue_type.isin(issue_filter)].copy()
    st.subheader("Operations at a glance")
    open_count = int((reports.status != "Resolved").sum())
    urgent_count = int(((reports.priority >= 70) & (reports.status != "Resolved")).sum())
    resolved_count = int((reports.status == "Resolved").sum())
    avg_age = round(float(reports.loc[reports.status != "Resolved", "age_days"].mean() or 0)) if open_count else 0
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Open reports", open_count, help="Synthetic sample plus reports submitted in this session")
    k2.metric("Urgent triage", urgent_count, help="Rule-based score of 70 or higher")
    k3.metric("Resolved", resolved_count)
    k4.metric("Average open age", f"{avg_age} days", help="Mean age for this demo; synthetic data")

    left, right = st.columns([1.55, 1])
    with left:
        st.subheader("Report map")
        st.caption("Markers show approximate demo locations in Indore; locations are illustrative.")
        st.map(filtered.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]], color="#e05a47", size=100)
    with right:
        st.subheader("Backlog by status")
        counts = filtered.groupby("status", as_index=False).size().rename(columns={"size": "reports"})
        chart = px.bar(counts, x="reports", y="status", orientation="h", color="status",
                       color_discrete_map={"New": "#e5a34d", "Assigned": "#4d82b8", "In progress": "#8b78c8", "Resolved": "#40a784"})
        chart.update_layout(showlegend=False, height=250, margin=dict(l=0, r=10, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(chart, use_container_width=True)

    st.subheader("Triage queue")
    queue = filtered.sort_values(["priority", "reported_at"], ascending=[False, True])
    display = queue[["report_id", "issue_type", "road_name", "severity", "priority", "status", "age_days", "feedback"]].rename(columns={
        "report_id": "Report", "issue_type": "Issue", "road_name": "Street", "severity": "Severity / 5", "priority": "Priority / 100", "status": "Status", "age_days": "Age (days)", "feedback": "Community feedback",
    })
    st.dataframe(display, hide_index=True, use_container_width=True, column_config={"Priority / 100": st.column_config.ProgressColumn("Priority / 100", min_value=0, max_value=100, format="%d")})
    if not queue.empty:
        render_status_feedback(queue)


def render_status_feedback(queue: pd.DataFrame) -> None:
    st.subheader("Update a report")
    options = {f"{row.report_id} · {row.issue_type} · {row.road_name}": row.report_id for row in queue.itertuples()}
    with st.form("status_update"):
        selected = st.selectbox("Report", list(options))
        report_id = options[selected]
        row = queue.loc[queue.report_id == report_id].iloc[0]
        c1, c2 = st.columns(2)
        new_status = c1.selectbox("Status", STATUS_ORDER, index=STATUS_ORDER.index(row.status))
        feedback = c2.selectbox("Community feedback", ["Awaiting confirmation", "Confirmed resolved", "Still present", "Needs follow-up"], index=["Awaiting confirmation", "Confirmed resolved", "Still present", "Needs follow-up"].index(row.feedback))
        submitted = st.form_submit_button("Save update", type="primary")
    if submitted:
        st.session_state.reports.loc[st.session_state.reports.report_id == report_id, "status"] = new_status
        st.session_state.reports.loc[st.session_state.reports.report_id == report_id, "feedback"] = feedback
        st.success(f"Updated {report_id}. This change is held in the current browser session.")
        st.rerun()


def render_report_form() -> None:
    st.subheader("Tell the city what you found")
    st.write("A clear location and a short description help the right team review an issue.")
    with st.form("citizen_report", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        issue = col_a.selectbox("Issue type", ["Pothole", "Cracking", "Waterlogging", "Broken surface", "Other"])
        severity_label = col_b.select_slider("How serious does it look?", options=["Minor", "Moderate", "Severe"], value="Moderate")
        location = st.text_input("Street or landmark", placeholder="e.g., near the public library")
        c1, c2 = st.columns(2)
        lat = c1.number_input("Latitude (demo area)", min_value=22.60, max_value=22.85, value=22.7196, format="%.5f", help="Approximate Indore coordinates for the prototype")
        lon = c2.number_input("Longitude (demo area)", min_value=75.75, max_value=75.95, value=75.8577, format="%.5f")
        description = st.text_area("What should the repair team know?", max_chars=300, placeholder="Describe the damage or any immediate safety concern.")
        photo = st.file_uploader("Add a photo (optional)", type=["jpg", "jpeg", "png"], help="The active Streamlit server receives the image in session memory. This prototype does not save or analyze it.")
        consent = st.checkbox("I understand this portfolio prototype stores my report only in this browser session.")
        submit = st.form_submit_button("Submit report", type="primary")
    if submit:
        if not location.strip() or not description.strip():
            st.error("Add a street or landmark and a short description.")
            return
        if not consent:
            st.error("Please confirm how this prototype handles your report.")
            return
        severity = {"Minor": 2, "Moderate": 3, "Severe": 5}[severity_label]
        report_id = f"RS-{datetime.now().strftime('%y%m%d%H%M%S')}"
        report = {"report_id": report_id, "issue_type": issue, "road_name": location.strip(), "latitude": lat, "longitude": lon,
                  "severity": severity, "traffic": 3, "safety_risk": 4 if severity == 5 else 2, "age_days": 0,
                  "vulnerable_users": False, "status": "New", "feedback": "Awaiting confirmation",
                  "reported_at": pd.Timestamp(date.today()), "description": description.strip(), "image_attached": photo is not None}
        st.session_state.reports = add_report(st.session_state.reports, report)
        st.success(f"Report {report_id} added to the in-session demo queue. Thank you for helping improve street safety.")
        st.caption("A production service would confirm receipt, protect contact and image data, and provide a real municipal follow-up channel.")


def render_scoring_guide() -> None:
    st.subheader("A transparent starting point for triage")
    st.write("RoadSense ranks reports for human review using five configurable signals. A score can focus attention; it cannot replace an engineer’s inspection or local policy.")
    factors = pd.DataFrame({"Signal": ["Observed severity", "Traffic exposure", "Safety risk", "Time waiting", "Vulnerable road users"],
                            "Weight": ["35%", "20%", "25%", "10%", "10%"],
                            "Why it matters": ["Larger defects may need faster attention.", "More road users can be exposed.", "Potential harm influences urgency.", "Older reports should not disappear in the queue.", "Nearby schools, crossings, or high-footfall areas may need additional care."]})
    st.dataframe(factors, hide_index=True, use_container_width=True)
    severity = st.slider("Try the score · severity", 1, 5, 4)
    traffic = st.slider("Traffic exposure", 1, 5, 3)
    safety = st.slider("Safety risk", 1, 5, 4)
    age = st.slider("Days waiting", 0, 30, 7)
    vulnerable = st.checkbox("Near a school, crossing, or other vulnerable road-user location")
    result = score_priority(severity, traffic, safety, age, vulnerable)
    st.metric("Illustrative triage score", f"{result.score} / 100 · {result.tier}")
    st.caption("Weights and thresholds are product assumptions for demonstration, not empirically validated or approved by a municipality.")

