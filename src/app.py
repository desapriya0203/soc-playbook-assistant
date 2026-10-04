import os
import sys
from datetime import datetime

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from playbook_rules import generate_playbook
from evidence_manager import (
    record_evidence,
    record_confirmation,
    record_override,
    get_case_history,
)

DATA_FILE = os.path.join(
    PROJECT_ROOT, "data", "processed", "clean_soc_cases.csv"
)
FEEDBACK_FILE = os.path.join(
    PROJECT_ROOT, "data", "processed", "usability_feedback.csv"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SOC Playbook Assistant",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# HELPERS
# ============================================================

def save_usability_feedback(
    case_id,
    analyst,
    ease_of_use,
    recommendation_clarity,
    procedure_usefulness,
    confidence,
    comments,
):
    """Save actual analyst/stakeholder usability feedback."""
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

    record = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "case_id": case_id,
        "analyst": analyst,
        "ease_of_use": ease_of_use,
        "recommendation_clarity": recommendation_clarity,
        "procedure_usefulness": procedure_usefulness,
        "confidence_after_using_assistant": confidence,
        "comments": comments,
    }])

    if os.path.exists(FEEDBACK_FILE):
        record.to_csv(FEEDBACK_FILE, mode="a", header=False, index=False)
    else:
        record.to_csv(FEEDBACK_FILE, index=False)


def human_confirmation_required(containment):
    """Support both current and older containment field names."""
    return containment.get(
        "human_confirmation",
        containment.get(
            "human_confirmation_required",
            containment.get("requires_human_confirmation", False),
        ),
    )


# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists(DATA_FILE):
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

df = pd.read_csv(DATA_FILE)

if df.empty:
    st.error("The cleaned SOC dataset is empty.")
    st.stop()


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
    df["case_id"].tolist(),
)

analyst_name = st.sidebar.text_input(
    "Analyst Name",
    value="Junior Analyst",
)


# ============================================================
# GET SELECTED CASE
# ============================================================

selected_case = df[df["case_id"] == case_id].iloc[0]
playbook = generate_playbook(selected_case)


# ============================================================
# APPROVED SOC PROCEDURES
# ============================================================

st.subheader("📋 Approved SOC Procedures")
approved_procedures = playbook.get("approved_procedures", [])

if approved_procedures:
    for procedure in approved_procedures:
        st.markdown(
            f"**{procedure['procedure_id']} - "
            f"{procedure['investigation_step']}**"
        )
        st.write(
            f"**Evidence Required:** {procedure['evidence_required']}"
        )
        st.write(
            f"**Expected Action:** {procedure['expected_action']}"
        )
        st.caption(f"Source: {procedure['source']}")
        st.divider()
else:
    st.info("No approved procedure found for this alert type.")


# ============================================================
# SIMILAR PAST INVESTIGATIONS
# ============================================================

st.subheader("📚 Similar Past Investigations")
similar_investigations = playbook.get("similar_investigations", [])

if similar_investigations:
    for investigation in similar_investigations:
        st.markdown(
            f"**{investigation['case_id']} — "
            f"{investigation['investigation_summary']}**"
        )
        st.write(f"**Evidence Found:** {investigation['evidence_found']}")
        st.write(
            f"**Analyst Decision:** {investigation['analyst_decision']}"
        )
        st.write(
            f"**Containment Decision:** "
            f"{investigation['containment_decision']}"
        )
        st.write(f"**Case Outcome:** {investigation['case_outcome']}")
        st.info(
            f"💡 Lesson Learned: {investigation['lesson_learned']}"
        )
        st.caption(f"Source: {investigation['source']}")
        st.divider()
else:
    st.info("No similar past investigations found for this alert type.")


# ============================================================
# PAST INVESTIGATION INSIGHTS
# ============================================================

st.subheader("💡 Past Investigation Insights")
past_investigation_insights = playbook.get(
    "past_investigation_insights", []
)

if past_investigation_insights:
    for insight in past_investigation_insights:
        st.info(
            f"💡 **{insight['case_id']} - Lesson Learned:** "
            f"{insight['lesson_learned']}"
        )
else:
    st.info("No past investigation insights available.")


# ============================================================
# CASE SUMMARY
# ============================================================

st.subheader("📋 Case Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Case ID", playbook["case_id"])
with col2:
    st.metric("Risk Level", playbook["risk_level"])
with col3:
    st.metric("Risk Score", playbook["risk_score"])
with col4:
    st.metric("Analyst", analyst_name)


# ============================================================
# CASE DETAILS
# ============================================================

st.subheader("🔎 Alert Details")
detail_col1, detail_col2 = st.columns(2)

with detail_col1:
    st.write(
        "**Alert Type:**",
        selected_case.get("alert_type", "Not Available"),
    )
    st.write(
        "**Location:**",
        selected_case.get(
            "login_location",
            selected_case.get("location", "Not Available"),
        ),
    )
    st.write(
        "**Failed Login Count:**",
        selected_case.get("failed_login_count", 0),
    )
    st.write(
        "**Successful Login:**",
        selected_case.get("successful_login", 0),
    )

with detail_col2:
    st.write("**New IP:**", selected_case.get("new_ip", 0))
    st.write(
        "**Location Change:**",
        selected_case.get("location_change", 0),
    )
    st.write(
        "**Endpoint Anomaly:**",
        selected_case.get("endpoint_anomaly", 0),
    )
    st.write(
        "**Email Anomaly:**",
        selected_case.get("email_anomaly", 0),
    )

st.divider()


# ============================================================
# EVIDENCE DETECTED
# ============================================================

st.subheader("🔍 Evidence Detected")

if playbook["evidence"]:
    for evidence in playbook["evidence"]:
        st.info("Evidence: " + evidence)
else:
    st.success("No significant evidence indicators detected.")


# ============================================================
# INVESTIGATION PLAYBOOK
# ============================================================

st.subheader("📖 Investigation Playbook")

for step in playbook["playbook_steps"]:
    with st.expander(
        f"Step {step['step']} — {step['action']}"
    ):
        st.write("**Why this step?**")
        st.write(step["reason"])
        st.write("**Evidence to collect:**")
        for item in step["evidence_required"]:
            st.write("• " + item)

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
            st.info(f"Action: {recommendation['action']}")

        st.write("**Rule:**", recommendation["reason"])
        st.write("**Evidence:**", recommendation["evidence"])
else:
    st.success("No additional recommendations.")

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
        "Other",
    ],
)

evidence_description = st.text_area(
    "Evidence Description",
    placeholder="Enter what you observed during investigation...",
)

if st.button("💾 Save Evidence", type="secondary"):
    if evidence_description.strip() == "":
        st.warning("Please enter an evidence description.")
    else:
        record_evidence(
            case_id=case_id,
            evidence_type=evidence_type,
            evidence_description=evidence_description,
            analyst=analyst_name,
        )
        st.success("Evidence recorded successfully.")

st.divider()


# ============================================================
# CONTAINMENT DECISION
# ============================================================

st.subheader("🚨 Containment Decision")
containment = playbook["containment"]

requires_confirmation = human_confirmation_required(containment)

if requires_confirmation:
    st.warning("⚠️ HUMAN CONFIRMATION REQUIRED")
else:
    st.info("Human confirmation is not mandatory for this action.")

st.write("**Recommended Action:**", containment["action"])
st.write("**Reason:**", containment["reason"])


# ============================================================
# APPROVE / OVERRIDE
# ============================================================

decision = st.radio(
    "Analyst Decision",
    [
        "Approve Recommendation",
        "Override Recommendation",
    ],
)

if decision == "Approve Recommendation":
    if st.button("✅ Confirm Action"):
        record_confirmation(
            case_id=case_id,
            action=containment["action"],
            decision="APPROVED",
            analyst=analyst_name,
        )
        st.success("Decision approved and recorded.")
else:
    override_reason = st.text_area(
        "Override Reason",
        placeholder=(
            "Explain why you are overriding the assistant recommendation..."
        ),
    )

    if st.button("⚠️ Submit Override"):
        if override_reason.strip() == "":
            st.error("Override reason is mandatory.")
        else:
            record_override(
                case_id=case_id,
                recommended_action=containment["action"],
                override_reason=override_reason,
                analyst=analyst_name,
            )
            st.success("Override recorded successfully.")

st.divider()


# ============================================================
# INVESTIGATION HISTORY
# ============================================================

st.subheader("📚 Investigation History")
history = get_case_history(case_id)

if history:
    history_df = pd.DataFrame(history)
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No previous investigation records for this case.")


# ============================================================
# USABILITY VALIDATION
# ============================================================

st.divider()
st.subheader("🧑‍💻 Usability Validation")
st.write(
    "Use this form after reviewing the case and playbook. "
    "Enter feedback from an actual analyst or stakeholder."
)

with st.form("usability_feedback_form"):
    ease_of_use = st.slider(
        "1. How easy was the assistant to use?",
        1,
        5,
        4,
        help="1 = Very difficult, 5 = Very easy",
    )
    recommendation_clarity = st.slider(
        "2. How clear were the assistant recommendations?",
        1,
        5,
        4,
        help="1 = Very unclear, 5 = Very clear",
    )
    procedure_usefulness = st.slider(
        "3. How useful were the approved procedures and past investigations?",
        1,
        5,
        4,
        help="1 = Not useful, 5 = Very useful",
    )
    confidence = st.slider(
        "4. How confident would you feel following this playbook?",
        1,
        5,
        4,
        help="1 = Not confident, 5 = Very confident",
    )
    comments = st.text_area(
        "5. Additional feedback",
        placeholder="What was useful? What should be improved?",
    )

    submitted = st.form_submit_button("📊 Submit Usability Feedback")

if submitted:
    save_usability_feedback(
        case_id=case_id,
        analyst=analyst_name,
        ease_of_use=ease_of_use,
        recommendation_clarity=recommendation_clarity,
        procedure_usefulness=procedure_usefulness,
        confidence=confidence,
        comments=comments.strip(),
    )
    st.success("Usability feedback recorded successfully.")
    st.caption("Saved to data/processed/usability_feedback.csv")

if os.path.exists(FEEDBACK_FILE):
    feedback_df = pd.read_csv(FEEDBACK_FILE)

    if not feedback_df.empty:
        st.markdown("### 📈 Collected Usability Feedback")

        rating_columns = [
            "ease_of_use",
            "recommendation_clarity",
            "procedure_usefulness",
            "confidence_after_using_assistant",
        ]
        average_ratings = feedback_df[rating_columns].mean()

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(
                "Ease of Use",
                f"{average_ratings['ease_of_use']:.2f}/5",
            )
        with c2:
            st.metric(
                "Recommendation Clarity",
                f"{average_ratings['recommendation_clarity']:.2f}/5",
            )
        with c3:
            st.metric(
                "Procedure Usefulness",
                f"{average_ratings['procedure_usefulness']:.2f}/5",
            )
        with c4:
            st.metric(
                "Confidence",
                f"{average_ratings['confidence_after_using_assistant']:.2f}/5",
            )

        st.caption(
            f"Validation responses collected: {len(feedback_df)}"
        )
        st.dataframe(feedback_df, use_container_width=True)
else:
    st.info(
        "No usability validation responses collected yet. "
        "Complete the form above with actual analyst/stakeholder feedback."
    )


# ============================================================
# LEGACY WORKFLOW COEXISTENCE
# ============================================================

st.divider()
st.subheader("🔄 Legacy Workflow Coexistence")
st.info(
    "This MVP operates alongside the existing SOC workflow. "
    "The assistant provides investigation guidance and records "
    "decisions without automatically executing containment."
)
st.caption("High-impact actions remain under human control.")
