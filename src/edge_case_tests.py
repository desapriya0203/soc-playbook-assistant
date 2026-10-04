import pandas as pd
from playbook_rules import generate_playbook


DATA_FILE = "data/processed/clean_soc_cases.csv"


# ============================================================
# HELPER
# ============================================================

def get_human_confirmation(containment):

    """
    Support both possible field names used by the
    Playbook Assistant.
    """

    return containment.get(
        "human_confirmation",
        containment.get(
            "requires_human_confirmation",
            False
        )
    )


# ============================================================
# TEST 1 - MISSING EVIDENCE
# ============================================================

def test_missing_evidence(df):

    print("\n" + "=" * 70)
    print("TEST 1: MISSING EVIDENCE")
    print("=" * 70)

    matching_cases = df[
        df["evidence_missing"] == 1
    ]

    if matching_cases.empty:

        print("No missing-evidence case found.")

        return {
            "test_case": "Missing Evidence",
            "case_id": "N/A",
            "expected_behavior":
                "Stop investigation and block containment",
            "result": "FAIL"
        }

    case = matching_cases.iloc[0]

    result = generate_playbook(case)

    # Check failure-state detection
    failure_detected = any(
        "Missing Evidence"
        in str(item)
        for item in result.get(
            "playbook_steps",
            []
        )
    )

    # Check containment protection
    containment = result.get(
        "containment",
        {}
    )

    containment_action = str(
        containment.get(
            "action",
            ""
        )
    )

    containment_blocked = (
        "DO NOT CONTAIN"
        in containment_action.upper()
    )

    human_confirmation = get_human_confirmation(
        containment
    )

    # Both blocking and human control should exist
    safe_handling = (
        failure_detected
        and containment_blocked
        and human_confirmation
    )

    status = (
        "PASS"
        if safe_handling
        else "FAIL"
    )

    print(
        f"Case ID              : "
        f"{case['case_id']}"
    )

    print(
        f"Risk Level           : "
        f"{case['risk_level']}"
    )

    print(
        f"Failure Detected     : "
        f"{failure_detected}"
    )

    print(
        f"Containment Blocked  : "
        f"{containment_blocked}"
    )

    print(
        f"Human Confirmation   : "
        f"{human_confirmation}"
    )

    print(
        f"Result               : "
        f"{status}"
    )

    return {
        "test_case":
            "Missing Evidence",

        "case_id":
            case["case_id"],

        "expected_behavior":
            "Stop investigation and block containment",

        "failure_detected":
            failure_detected,

        "containment_blocked":
            containment_blocked,

        "human_confirmation":
            human_confirmation,

        "result":
            status
    }


# ============================================================
# TEST 2 - CONFLICTING EVIDENCE
# ============================================================

def test_conflicting_evidence(df):

    print("\n" + "=" * 70)
    print("TEST 2: CONFLICTING EVIDENCE")
    print("=" * 70)

    matching_cases = df[
        df["evidence_conflict"] == 1
    ]

    if matching_cases.empty:

        print("No conflicting-evidence case found.")

        return {
            "test_case": "Conflicting Evidence",
            "case_id": "N/A",
            "expected_behavior":
                "Stop and require manual review",
            "result": "FAIL"
        }

    case = matching_cases.iloc[0]

    result = generate_playbook(case)

    # Detect conflict
    conflict_detected = any(
        "Conflicting Evidence"
        in str(item)
        for item in result.get(
            "playbook_steps",
            []
        )
    )

    # Check manual review recommendation
    manual_review = any(
        "manual"
        in str(item).lower()
        for item in result.get(
            "recommendations",
            []
        )
    )

    # Check containment protection
    containment = result.get(
        "containment",
        {}
    )

    containment_action = str(
        containment.get(
            "action",
            ""
        )
    )

    containment_blocked = (
        "DO NOT CONTAIN"
        in containment_action.upper()
    )

    safe_handling = (
        conflict_detected
        and manual_review
        and containment_blocked
    )

    status = (
        "PASS"
        if safe_handling
        else "FAIL"
    )

    print(
        f"Case ID              : "
        f"{case['case_id']}"
    )

    print(
        f"Risk Level           : "
        f"{case['risk_level']}"
    )

    print(
        f"Conflict Detected    : "
        f"{conflict_detected}"
    )

    print(
        f"Manual Review        : "
        f"{manual_review}"
    )

    print(
        f"Containment Blocked  : "
        f"{containment_blocked}"
    )

    print(
        f"Result               : "
        f"{status}"
    )

    return {
        "test_case":
            "Conflicting Evidence",

        "case_id":
            case["case_id"],

        "expected_behavior":
            "Stop and require manual review",

        "conflict_detected":
            conflict_detected,

        "manual_review":
            manual_review,

        "containment_blocked":
            containment_blocked,

        "result":
            status
    }


# ============================================================
# TEST 3 - HIGH RISK + HUMAN CONFIRMATION
# ============================================================

def test_high_risk_human_confirmation(df):

    print("\n" + "=" * 70)
    print("TEST 3: HIGH RISK + HUMAN CONFIRMATION")
    print("=" * 70)

    matching_cases = df[
        (df["risk_level"] == "HIGH")
        &
        (df["evidence_missing"] == 0)
        &
        (df["evidence_conflict"] == 0)
    ]

    if matching_cases.empty:

        print("No suitable high-risk case found.")

        return {
            "test_case":
                "High Risk Human Confirmation",

            "case_id":
                "N/A",

            "expected_behavior":
                "Recommend containment but require human confirmation",

            "result":
                "FAIL"
        }

    case = matching_cases.iloc[0]

    result = generate_playbook(case)

    containment = result.get(
        "containment",
        {}
    )

    human_confirmation = get_human_confirmation(
        containment
    )

    high_impact_actions = result.get(
        "high_impact_actions",
        []
    )

    high_impact_exists = (
        len(high_impact_actions) > 0
    )

    # High-risk containment should be protected
    safe_high_risk_handling = (
        human_confirmation
        and high_impact_exists
    )

    status = (
        "PASS"
        if safe_high_risk_handling
        else "FAIL"
    )

    print(
        f"Case ID              : "
        f"{case['case_id']}"
    )

    print(
        f"Risk Level           : "
        f"{case['risk_level']}"
    )

    print(
        f"High Impact Action   : "
        f"{high_impact_exists}"
    )

    print(
        f"Human Confirmation   : "
        f"{human_confirmation}"
    )

    print(
        f"Result               : "
        f"{status}"
    )

    return {
        "test_case":
            "High Risk Human Confirmation",

        "case_id":
            case["case_id"],

        "expected_behavior":
            "Recommend containment but require human confirmation",

        "high_impact_action":
            high_impact_exists,

        "human_confirmation":
            human_confirmation,

        "result":
            status
    }


# ============================================================
# TEST 4 - LOW RISK MONITORING
# ============================================================

def test_low_risk_monitoring(df):

    print("\n" + "=" * 70)
    print("TEST 4: LOW RISK MONITORING")
    print("=" * 70)

    matching_cases = df[
        (df["risk_level"] == "LOW")
        &
        (df["evidence_missing"] == 0)
        &
        (df["evidence_conflict"] == 0)
    ]

    if matching_cases.empty:

        print("No suitable low-risk case found.")

        return {
            "test_case":
                "Low Risk Monitoring",

            "case_id":
                "N/A",

            "expected_behavior":
                "Continue monitoring without high-impact confirmation",

            "result":
                "FAIL"
        }

    case = matching_cases.iloc[0]

    result = generate_playbook(case)

    containment = result.get(
        "containment",
        {}
    )

    action = str(
        containment.get(
            "action",
            ""
        )
    )

    monitoring_recommended = (
        "monitor"
        in action.lower()
    )

    human_confirmation = get_human_confirmation(
        containment
    )

    safe_low_risk_handling = (
        monitoring_recommended
        and not human_confirmation
    )

    status = (
        "PASS"
        if safe_low_risk_handling
        else "FAIL"
    )

    print(
        f"Case ID              : "
        f"{case['case_id']}"
    )

    print(
        f"Risk Level           : "
        f"{case['risk_level']}"
    )

    print(
        f"Containment Action   : "
        f"{action}"
    )

    print(
        f"Monitoring           : "
        f"{monitoring_recommended}"
    )

    print(
        f"Human Confirmation   : "
        f"{human_confirmation}"
    )

    print(
        f"Result               : "
        f"{status}"
    )

    return {
        "test_case":
            "Low Risk Monitoring",

        "case_id":
            case["case_id"],

        "expected_behavior":
            "Continue monitoring without high-impact confirmation",

        "monitoring_recommended":
            monitoring_recommended,

        "human_confirmation":
            human_confirmation,

        "result":
            status
    }


# ============================================================
# TEST 5 - HIGH RISK + MISSING EVIDENCE
# ============================================================

def test_high_risk_missing_evidence(df):

    print("\n" + "=" * 70)
    print("TEST 5: HIGH RISK + MISSING EVIDENCE")
    print("=" * 70)

    matching_cases = df[
        (df["risk_level"] == "HIGH")
        &
        (df["evidence_missing"] == 1)
    ]

    if matching_cases.empty:

        print(
            "No high-risk missing-evidence case found."
        )

        return {
            "test_case":
                "High Risk Missing Evidence",

            "case_id":
                "N/A",

            "expected_behavior":
                "Block containment despite high risk",

            "result":
                "FAIL"
        }

    case = matching_cases.iloc[0]

    result = generate_playbook(case)

    containment = result.get(
        "containment",
        {}
    )

    action = str(
        containment.get(
            "action",
            ""
        )
    )

    failure_detected = any(
        "Missing Evidence"
        in str(item)
        for item in result.get(
            "playbook_steps",
            []
        )
    )

    containment_blocked = (
        "DO NOT CONTAIN"
        in action.upper()
    )

    # Failure state must override high-risk containment.
    safe_handling = (
        failure_detected
        and containment_blocked
    )

    status = (
        "PASS"
        if safe_handling
        else "FAIL"
    )

    print(
        f"Case ID              : "
        f"{case['case_id']}"
    )

    print(
        f"Risk Level           : "
        f"{case['risk_level']}"
    )

    print(
        f"Failure Detected     : "
        f"{failure_detected}"
    )

    print(
        f"Containment Blocked  : "
        f"{containment_blocked}"
    )

    print(
        f"Result               : "
        f"{status}"
    )

    return {
        "test_case":
            "High Risk Missing Evidence",

        "case_id":
            case["case_id"],

        "expected_behavior":
            "Block containment despite high risk",

        "failure_detected":
            failure_detected,

        "containment_blocked":
            containment_blocked,

        "result":
            status
    }


# ============================================================
# TEST 6 - HIGH RISK + CONFLICTING EVIDENCE
# ============================================================

def test_high_risk_conflicting_evidence(df):

    print("\n" + "=" * 70)
    print("TEST 6: HIGH RISK + CONFLICTING EVIDENCE")
    print("=" * 70)

    matching_cases = df[
        (df["risk_level"] == "HIGH")
        &
        (df["evidence_conflict"] == 1)
    ]

    if matching_cases.empty:

        print(
            "No high-risk conflicting-evidence case found."
        )

        return {
            "test_case":
                "High Risk Conflicting Evidence",

            "case_id":
                "N/A",

            "expected_behavior":
                "Block automated containment and require review",

            "result":
                "FAIL"
        }

    case = matching_cases.iloc[0]

    result = generate_playbook(case)

    containment = result.get(
        "containment",
        {}
    )

    action = str(
        containment.get(
            "action",
            ""
        )
    )

    conflict_detected = any(
        "Conflicting Evidence"
        in str(item)
        for item in result.get(
            "playbook_steps",
            []
        )
    )

    manual_review = any(
        "manual"
        in str(item).lower()
        for item in result.get(
            "recommendations",
            []
        )
    )

    containment_blocked = (
        "DO NOT CONTAIN"
        in action.upper()
    )

    safe_handling = (
        conflict_detected
        and manual_review
        and containment_blocked
    )

    status = (
        "PASS"
        if safe_handling
        else "FAIL"
    )

    print(
        f"Case ID              : "
        f"{case['case_id']}"
    )

    print(
        f"Risk Level           : "
        f"{case['risk_level']}"
    )

    print(
        f"Conflict Detected    : "
        f"{conflict_detected}"
    )

    print(
        f"Manual Review        : "
        f"{manual_review}"
    )

    print(
        f"Containment Blocked  : "
        f"{containment_blocked}"
    )

    print(
        f"Result               : "
        f"{status}"
    )

    return {
        "test_case":
            "High Risk Conflicting Evidence",

        "case_id":
            case["case_id"],

        "expected_behavior":
            "Block automated containment and require review",

        "conflict_detected":
            conflict_detected,

        "manual_review":
            manual_review,

        "containment_blocked":
            containment_blocked,

        "result":
            status
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")

    print("=" * 70)
    print(
        "SOC PLAYBOOK ASSISTANT - EDGE CASE TESTING"
    )
    print("=" * 70)

    df = pd.read_csv(
        DATA_FILE
    )

    results = []

    # Core failure-state tests
    results.append(
        test_missing_evidence(df)
    )

    results.append(
        test_conflicting_evidence(df)
    )

    # Human-in-the-loop test
    results.append(
        test_high_risk_human_confirmation(df)
    )

    # Normal low-risk behaviour
    results.append(
        test_low_risk_monitoring(df)
    )

    # Combined failure-state tests
    results.append(
        test_high_risk_missing_evidence(df)
    )

    results.append(
        test_high_risk_conflicting_evidence(df)
    )

    # --------------------------------------------------------
    # Results DataFrame
    # --------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    output_file = (
        "data/processed/"
        "edge_case_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("EDGE CASE TEST SUMMARY")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    passed = (
        results_df["result"] == "PASS"
    ).sum()

    total = len(
        results_df
    )

    failed = (
        total - passed
    )

    print(
        "\n" + "-" * 70
    )

    print(
        f"Tests Passed : "
        f"{passed}/{total}"
    )

    print(
        f"Tests Failed : "
        f"{failed}/{total}"
    )

    if passed == total:

        print(
            "STATUS       : "
            "ALL EDGE CASE TESTS PASSED"
        )

    else:

        print(
            "STATUS       : "
            "SOME EDGE CASE TESTS FAILED"
        )

    print(
        "-" * 70
    )

    print(
        f"\nResults saved to: "
        f"{output_file}"
    )


if __name__ == "__main__":
    main()
