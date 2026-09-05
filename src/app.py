import streamlit as st
import pandas as pd
import sys
import os

# Allow importing files from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playbook_rules import generate_playbook
from evidence_manager import (
    record_evidence,
    record_confirmation,
    record_override,
    get_case_history
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SOC Playbook Assistant",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = "data/processed/clean_soc_cases.csv"

df = pd.read_csv(DATA_FILE)


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ SOC Investigation Playbook Assistant")

st.write(
    "Guides junior analysts through organisation-specific "
    "investigation procedures with evidence-based recommendations."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Case Selection")

case_id = st.sidebar.selectbox(
    "Select Investigation Case",
    df["case_id"].tolist()
)

analyst_name = st.sidebar.text_input(
    "Analyst Name",
    value="Junior Analyst"
)


# ============================================================
# GET SELECTED CASE
# ============================================================

selected_case = df[
    df["case_id"] == case_id
].iloc[0]

playbook = generate_playbook(selected_case)


# ============================================================
# CASE SUMMARY
# ============================================================

st.subheader("📋 Case Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Case ID",
        playbook["case_id"]
    )

with col2:
    st.metric(
        "Risk Level",
        playbook["risk_level"]
    )

with col3:
    st.metric(
        "Risk Score",
        playbook["risk_score"]
    )

with col4:
    st.metric(
        "Analyst",
        analyst_name
    )


# ============================================================
# CASE DETAILS
# ============================================================

st.subheader("🔎 Alert Details")

detail_col1, detail_col2 = st.columns(2)

with detail_col1:

    st.write(
        "**Alert Type:**",
        selected_case.get("alert_type", "Not Available")
    )

    st.write(
        "**Location:**",
        selected_case.get("location", "Not Available")
    )

    st.write(
        "**Failed Login Count:**",
        selected_case.get("failed_login_count", 0)
    )

    st.write(
        "**Successful Login:**",
        selected_case.get("successful_login", 0)
    )

with detail_col2:

    st.write(
        "**New IP:**",
        selected_case.get("new_ip", 0)
    )

    st.write(
        "**Location Change:**",
        selected_case.get("location_change", 0)
    )

    st.write(
        "**Endpoint Anomaly:**",
        selected_case.get("endpoint_anomaly", 0)
    )

    st.write(
        "**Email Anomaly:**",
        selected_case.get("email_anomaly", 0)
    )

st.divider()


# ============================================================
# EVIDENCE
# ============================================================

st.subheader("🔍 Evidence Detected")

if playbook["evidence"]:

    for evidence in playbook["evidence"]:

        st.info(
            "Evidence: " + evidence
        )

else:

    st.success(
        "No significant evidence indicators detected."
    )


# ============================================================
# INVESTIGATION PLAYBOOK
# ============================================================

st.subheader("📖 Investigation Playbook")

for step in playbook["playbook_steps"]:

    with st.expander(
        f"Step {step['step']} — {step['action']}"
    ):

        st.write(
            "**Why this step?**"
        )

        st.write(
            step["reason"]
        )

        st.write(
            "**Evidence to collect:**"
        )

        for item in step["evidence_required"]:

            st.write(
                "• " + item
            )


st.divider()


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.subheader("🤖 Assistant Recommendations")

if playbook["recommendations"]:

    for recommendation in playbook["recommendations"]:

        priority = recommendation["priority"]

        if priority == "HIGH":

            st.error(
                f"🔴 HIGH PRIORITY\n\n"
                f"Action: {recommendation['action']}"
            )

        elif priority == "MEDIUM":

            st.warning(
                f"🟠 MEDIUM PRIORITY\n\n"
                f"Action: {recommendation['action']}"
            )

        elif priority == "BLOCKED":

            st.error(
                f"⛔ BLOCKED\n\n"
                f"Action: {recommendation['action']}"
            )

        else:

            st.info(
                f"Action: {recommendation['action']}"
            )

        st.write(
            "**Rule:**",
            recommendation["reason"]
        )

        st.write(
            "**Evidence:**",
            recommendation["evidence"]
        )

else:

    st.success(
        "No additional recommendations."
    )


st.divider()


# ============================================================
# EVIDENCE RECORDING
# ============================================================

st.subheader("📝 Record Investigation Evidence")

evidence_type = st.selectbox(
    "Evidence Type",
    [
        "Authentication Log",
        "Source IP",
        "Endpoint Activity",
        "Email Investigation",
        "Cloud Activity",
        "Analyst Observation",
        "Other"
    ]
)

evidence_description = st.text_area(
    "Evidence Description",
    placeholder="Enter what you observed during investigation..."
)

if st.button(
    "💾 Save Evidence",
    type="secondary"
):

    if evidence_description.strip() == "":

        st.warning(
            "Please enter an evidence description."
        )

    else:

        record_evidence(

            case_id=case_id,

            evidence_type=evidence_type,

            evidence_description=evidence_description,

            analyst=analyst_name
        )

        st.success(
            "Evidence recorded successfully."
        )


st.divider()


# ============================================================
# CONTAINMENT DECISION
# ============================================================

st.subheader("🚨 Containment Decision")

containment = playbook["containment"]

if containment["human_confirmation_required"]:

    st.warning(
        "⚠️ HUMAN CONFIRMATION REQUIRED"
    )

else:

    st.info(
        "Human confirmation is not mandatory for this action."
    )


st.write(
    "**Recommended Action:**",
    containment["action"]
)

st.write(
    "**Reason:**",
    containment["reason"]
)


# ============================================================
# APPROVE / OVERRIDE
# ============================================================

decision = st.radio(
    "Analyst Decision",
    [
        "Approve Recommendation",
        "Override Recommendation"
    ]
)


if decision == "Approve Recommendation":

    if st.button(
        "✅ Confirm Action"
    ):

        record_confirmation(

            case_id=case_id,

            action=containment["action"],

            decision="APPROVED",

            analyst=analyst_name
        )

        st.success(
            "Decision approved and recorded."
        )


else:

    override_reason = st.text_area(
        "Override Reason",
        placeholder=(
            "Explain why you are overriding "
            "the assistant recommendation..."
        )
    )

    if st.button(
        "⚠️ Submit Override"
    ):

        if override_reason.strip() == "":

            st.error(
                "Override reason is mandatory."
            )

        else:

            record_override(

                case_id=case_id,

                recommended_action=containment["action"],

                override_reason=override_reason,

                analyst=analyst_name
            )

            st.success(
                "Override recorded successfully."
            )


st.divider()


# ============================================================
# INVESTIGATION HISTORY
# ============================================================

st.subheader("📚 Investigation History")

history = get_case_history(case_id)

if history:

    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "No previous investigation records for this case."
    )


# ============================================================
# LEGACY WORKFLOW NOTICE
# ============================================================

st.divider()

st.subheader("🔄 Legacy Workflow Coexistence")

st.info(
    "This MVP operates alongside the existing SOC workflow. "
    "The assistant provides investigation guidance and records "
    "decisions without automatically executing containment."
)

st.caption(
    "High-impact actions remain under human control."
)