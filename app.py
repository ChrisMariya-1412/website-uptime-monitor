import os
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import streamlit as st

from monitor import check_website


DATA_FILE = "monitoring_history.csv"

st.set_page_config(
    page_title="Website Uptime Monitor",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Website Uptime & Latency Monitor")
st.write("Check website availability and track response times.")

# Load previous monitoring results
if os.path.exists(DATA_FILE):
    history = pd.read_csv(DATA_FILE)
else:
    history = pd.DataFrame(
        columns=[
            "url",
            "timestamp",
            "status_code",
            "latency_ms",
            "is_up",
            "error",
        ]
    )

# Website input
url = st.text_input(
    "Enter a website URL",
    placeholder="https://www.google.com",
)

if st.button("Check Website"):
    if not url.startswith(("http://", "https://")):
        st.error("Enter a URL starting with http:// or https://")
    else:
        with st.spinner("Checking website..."):
            result = check_website(url)

        new_row = pd.DataFrame([result])
        history = pd.concat(
            [history, new_row],
            ignore_index=True,
        )
        history.to_csv(DATA_FILE, index=False)

        if result["is_up"]:
            st.success("Website responded successfully!")
        else:
            st.error("Website may be down or experiencing errors.")

        st.json(result)

# Display monitoring history
st.subheader("Monitoring History")

if not history.empty:
    history["is_up"] = history["is_up"].astype(str).str.lower().eq("true")

    total_checks = len(history)
    uptime = history["is_up"].mean() * 100
    latest_latency = history.iloc[-1]["latency_ms"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Checks", total_checks)
    col2.metric("Recorded Uptime", f"{uptime:.1f}%")
    col3.metric(
        "Latest Response Time",
        f"{latest_latency:.2f} ms"
        if pd.notna(latest_latency)
        else "Unavailable",
    )

    st.dataframe(history, width="stretch")

    # Response-time chart
    chart_data = history.dropna(subset=["latency_ms"]).copy()

    if not chart_data.empty:
        chart_data["timestamp"] = pd.to_datetime(
            chart_data["timestamp"], errors="coerce"
        )

        fig = px.line(
            chart_data,
            x="timestamp",
            y="latency_ms",
            color="url",
            markers=True,
            title="Website Response Time Over Time",
            labels={
                "timestamp": "Time",
                "latency_ms": "Response Time (ms)",
                "url": "Website",
            },
        )
        st.plotly_chart(fig, width="stretch")
else:
    st.info("No checks yet. Enter a URL above to begin.")