"""RoadSense AI: a portfolio prototype for citizen road issue reporting."""

import streamlit as st

from roadsense.data import load_reports
from roadsense.ui import render_app


st.set_page_config(
    page_title="RoadSense AI | Safer streets, smarter repairs",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1440px;}
    .eyebrow {color:#b85d43; font-size:.72rem; font-weight:750; letter-spacing:.16em; margin-bottom:.35rem;}
    h1 {letter-spacing:-.045em; color:#172b28;}
    h2, h3 {letter-spacing:-.025em; color:#203a35;}
    [data-testid="stMetric"] {background:#fff; border:1px solid #e4eae7; padding:1rem 1.1rem; border-radius:14px;}
    [data-testid="stMetricValue"] {font-weight:750; color:#1d3933;}
    [data-testid="stAlert"] {border-radius:12px;}
    div[data-testid="stRadio"] > div {gap:.5rem;}
</style>
""", unsafe_allow_html=True)

render_app(load_reports())
