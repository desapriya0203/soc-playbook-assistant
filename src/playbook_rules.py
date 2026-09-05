import pandas as pd


# ============================================================
# SOC INVESTIGATION PLAYBOOK RULES
# ============================================================

def generate_playbook(case):
    """
    Generate an investigation playbook for a single SOC case.

    The assistant does NOT automatically perform containment.
    It only recommends actions and explains the evidence/rule.
    High-impact actions require human confirmation.
    """

    steps = []
    evidence = []
    recommendations = []
    high_impact_actions = []

    # --------------------------------------------------------
    # Extract case information
    # --------------------------------------------------------

    failed_logins = int(case["failed_login_count"])
    successful_login = int(case["successful_login"])
    new_ip = int(case["new_ip"])
    location_change = int(case["location_change"])
    endpoint_anomaly = int(case["endpoint_anomaly"])
    email_anomaly = int(case["email_anomaly"])
    cloud_anomaly = int(case["cloud_anomaly"])

    evidence_missing = int(case["evidence_missing"])
    evidence_conflict = int(case["evidence_conflict"])

    risk_level = case["risk_level"]

    # --------------------------------------------------------
    # STEP 1 - Validate Alert
    # --------------------------------------------------------

    steps.append({
        "step": 1,
        "action": "Validate Alert",
        "reason": "Every investigation must begin by validating the original alert.",
        "evidence_required": [
            "Alert source",
            "Alert timestamp",
            "Affected user or endpoint"
        ]
    })

    # --------------------------------------------------------
    # STEP 2 - Authentication Investigation
    # --------------------------------------------------------

    if failed_logins >= 5:

        evidence.append(
            f"{failed_logins} failed login attempts detected."
        )

        steps.append({
            "step": 2,
            "action": "Check Authentication History",
            "reason": (
                "Repeated failed login attempts may indicate "
                "credential attack or suspicious authentication activity."
            ),
            "evidence_required": [
                "Authentication logs",
                "Failed login timestamps",
                "Source IP addresses"
            ]
        })

        recommendations.append({
            "action": "Investigate repeated authentication failures",
            "priority": "HIGH",
            "reason": f"Rule triggered: failed_login_count >= 5",
            "evidence": f"failed_login_count = {failed_logins}"
        })

    else:

        steps.append({
            "step": 2,
            "action": "Check Authentication History",
            "reason": "Authentication history must still be verified.",
            "evidence_required": [
                "Recent login events",
                "Source IP"
            ]
        })

    # --------------------------------------------------------
    # STEP 3 - New IP Investigation
    # --------------------------------------------------------

    if new_ip == 1:

        evidence.append(
            "Login from a new or previously unseen IP detected."
        )

        steps.append({
            "step": 3,
            "action": "Investigate Source IP",
            "reason": (
                "A new IP can indicate account compromise "
                "or unusual user activity."
            ),
            "evidence_required": [
                "Source IP",
                "IP reputation",
                "Previous login locations"
            ]
        })

        recommendations.append({
            "action": "Investigate new source IP",
            "priority": "HIGH",
            "reason": "Rule triggered: new_ip == 1",
            "evidence": "new_ip = 1"
        })

    # --------------------------------------------------------
    # STEP 4 - Location Change
    # --------------------------------------------------------

    if location_change == 1:

        evidence.append(
            "Unusual location change detected."
        )

        steps.append({
            "step": 4,
            "action": "Investigate Login Location",
            "reason": (
                "A sudden location change may indicate "
                "impossible travel or account misuse."
            ),
            "evidence_required": [
                "Current login location",
                "Previous login location",
                "Login timestamps"
            ]
        })

        recommendations.append({
            "action": "Verify unusual login location",
            "priority": "MEDIUM",
            "reason": "Rule triggered: location_change == 1",
            "evidence": "location_change = 1"
        })

    # --------------------------------------------------------
    # STEP 5 - Endpoint Investigation
    # --------------------------------------------------------

    if endpoint_anomaly == 1:

        evidence.append(
            "Endpoint anomaly detected."
        )

        steps.append({
            "step": 5,
            "action": "Review Endpoint Activity",
            "reason": (
                "Endpoint anomalies require process, network "
                "and system activity review."
            ),
            "evidence_required": [
                "Running processes",
                "Network connections",
                "Recent files",
                "Endpoint security alerts"
            ]
        })

        recommendations.append({
            "action": "Review endpoint activity",
            "priority": "HIGH",
            "reason": "Rule triggered: endpoint_anomaly == 1",
            "evidence": "endpoint_anomaly = 1"
        })

    # --------------------------------------------------------
    # STEP 6 - Email Investigation
    # --------------------------------------------------------

    if email_anomaly == 1:

        evidence.append(
            "Suspicious email activity detected."
        )

        steps.append({
            "step": 6,
            "action": "Review Email Activity",
            "reason": (
                "Email anomalies may indicate phishing, "
                "malicious attachments or account compromise."
            ),
            "evidence_required": [
                "Sender",
                "Recipient",
                "Email subject",
                "Attachments",
                "URLs"
            ]
        })

        recommendations.append({
            "action": "Investigate suspicious email",
            "priority": "HIGH",
            "reason": "Rule triggered: email_anomaly == 1",
            "evidence": "email_anomaly = 1"
        })

    # --------------------------------------------------------
    # STEP 7 - Cloud Investigation
    # --------------------------------------------------------

    if cloud_anomaly == 1:

        evidence.append(
            "Cloud account anomaly detected."
        )

        steps.append({
            "step": 7,
            "action": "Review Cloud Activity",
            "reason": (
                "Cloud anomalies may indicate unauthorized "
                "access or unusual account activity."
            ),
            "evidence_required": [
                "Cloud login history",
                "API activity",
                "Permission changes",
                "Resource access"
            ]
        })

        recommendations.append({
            "action": "Investigate cloud account activity",
            "priority": "HIGH",
            "reason": "Rule triggered: cloud_anomaly == 1",
            "evidence": "cloud_anomaly = 1"
        })

    # --------------------------------------------------------
    # STEP 8 - Evidence Collection
    # --------------------------------------------------------

    steps.append({
        "step": 8,
        "action": "Collect Evidence",
        "reason": (
            "Investigation decisions must be supported "
            "by recorded evidence."
        ),
        "evidence_required": [
            "Relevant logs",
            "Alert details",
            "Screenshots or event references",
            "Analyst notes"
        ]
    })

    # --------------------------------------------------------
    # FAILURE STATE 1 - Missing Evidence
    # --------------------------------------------------------

    if evidence_missing == 1:

        steps.append({
            "step": 9,
            "action": "STOP - Missing Evidence",
            "reason": (
                "Required evidence is unavailable. "
                "Do not make a final containment decision."
            ),
            "evidence_required": [
                "Missing log source",
                "Missing event details",
                "Missing analyst evidence"
            ]
        })

        recommendations.append({
            "action": "Request missing evidence",
            "priority": "BLOCKED",
            "reason": "Rule triggered: evidence_missing == 1",
            "evidence": "Required evidence is unavailable",
            "human_confirmation_required": True
        })

    # --------------------------------------------------------
    # FAILURE STATE 2 - Conflicting Evidence
    # --------------------------------------------------------

    if evidence_conflict == 1:

        steps.append({
            "step": 10,
            "action": "STOP - Conflicting Evidence",
            "reason": (
                "Evidence sources disagree. "
                "Escalate for manual review."
            ),
            "evidence_required": [
                "Conflicting log entries",
                "Timeline comparison",
                "Analyst explanation"
            ]
        })

        recommendations.append({
            "action": "Escalate conflicting evidence for manual review",
            "priority": "BLOCKED",
            "reason": "Rule triggered: evidence_conflict == 1",
            "evidence": "Evidence sources contain conflicting information",
            "human_confirmation_required": True
        })

    # --------------------------------------------------------
    # STEP 9 - Risk Assessment
    # --------------------------------------------------------

    steps.append({
        "step": 11,
        "action": "Assess Risk",
        "reason": (
            "Risk level is determined from the available "
            "security indicators and evidence."
        ),
        "evidence_required": [
            "Risk score",
            "Security indicators",
            "Investigation findings"
        ]
    })

    # --------------------------------------------------------
    # CONTAINMENT RECOMMENDATION
    # --------------------------------------------------------

    if evidence_missing == 1 or evidence_conflict == 1:

        containment = {
            "action": "DO NOT CONTAIN YET",
            "reason": (
                "Containment is blocked until evidence "
                "is complete and consistent."
            ),
            "human_confirmation_required": True
        }

    elif risk_level == "HIGH":

        containment = {
            "action": "Recommend Endpoint Isolation / Account Disablement",
            "reason": (
                "HIGH risk case with multiple correlated "
                "security indicators."
            ),
            "human_confirmation_required": True
        }

        high_impact_actions.append(
            "Endpoint isolation or account disablement"
        )

    elif risk_level == "MEDIUM":

        containment = {
            "action": "Escalate for Senior Analyst Review",
            "reason": (
                "MEDIUM risk requires additional review "
                "before containment."
            ),
            "human_confirmation_required": True
        }

    else:

        containment = {
            "action": "Continue Monitoring",
            "reason": (
                "LOW risk indicators do not currently "
                "justify containment."
            ),
            "human_confirmation_required": False
        }

    # --------------------------------------------------------
    # FINAL STEP
    # --------------------------------------------------------

    steps.append({
        "step": 12,
        "action": "Determine Containment",
        "reason": containment["reason"],
        "evidence_required": [
            "Investigation findings",
            "Risk assessment",
            "Senior analyst approval where required"
        ]
    })

    # --------------------------------------------------------
    # RETURN PLAYBOOK
    # --------------------------------------------------------

    return {
        "case_id": case["case_id"],
        "risk_level": risk_level,
        "risk_score": case["risk_score"],
        "evidence": evidence,
        "playbook_steps": steps,
        "recommendations": recommendations,
        "containment": containment,
        "high_impact_actions": high_impact_actions
    }


# ============================================================
# TEST THE PLAYBOOK
# ============================================================

if __name__ == "__main__":

    # Load cleaned dataset
    file_path = "data/processed/clean_soc_cases.csv"

    df = pd.read_csv(file_path)

    # Select one case
    test_case = df.iloc[0]

    # Generate investigation playbook
    result = generate_playbook(test_case)

    print("\n" + "=" * 70)
    print("SOC INVESTIGATION PLAYBOOK")
    print("=" * 70)

    print("\nCase ID:")
    print(result["case_id"])

    print("\nRisk:")
    print(
        result["risk_level"],
        f"(Score: {result['risk_score']})"
    )

    print("\nEvidence:")
    for item in result["evidence"]:
        print("  ✓", item)

    print("\nRecommendations:")

    for recommendation in result["recommendations"]:

        print(
            f"\n  Action: {recommendation['action']}"
        )

        print(
            f"  Priority: {recommendation['priority']}"
        )

        print(
            f"  Reason: {recommendation['reason']}"
        )

        print(
            f"  Evidence: {recommendation['evidence']}"
        )

    print("\nContainment Decision:")

    print(
        result["containment"]["action"]
    )

    print(
        "Reason:",
        result["containment"]["reason"]
    )

    print(
        "Human confirmation required:",
        result["containment"]["human_confirmation_required"]
    )

    print("\nInvestigation Steps:")

    for step in result["playbook_steps"]:

        print(
            f"{step['step']}. {step['action']}"
        )