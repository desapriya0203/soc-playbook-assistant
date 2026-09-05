import pandas as pd
from playbook_rules import generate_playbook


DATA_FILE = "data/processed/clean_soc_cases.csv"


def test_missing_evidence(df):
    print("\n" + "=" * 70)
    print("TEST 1: MISSING EVIDENCE")
    print("=" * 70)

    case = df[df["evidence_missing"] == 1].iloc[0]
    result = generate_playbook(case)

    failure_detected = any(
        "Missing Evidence" in str(item)
        for item in result["playbook_steps"]
    )

    containment_blocked = "DO NOT CONTAIN" in result["containment"]["action"]

    if failure_detected and containment_blocked:
        status = "PASS"
    else:
        status = "FAIL"

    print(f"Case ID              : {case['case_id']}")
    print(f"Risk Level           : {case['risk_level']}")
    print(f"Failure Detected     : {failure_detected}")
    print(f"Containment Blocked  : {containment_blocked}")
    print(f"Result               : {status}")

    return {
        "test_case": "Missing Evidence",
        "case_id": case["case_id"],
        "expected_behavior": "Stop investigation and block containment",
        "result": status
    }


def test_conflicting_evidence(df):
    print("\n" + "=" * 70)
    print("TEST 2: CONFLICTING EVIDENCE")
    print("=" * 70)

    case = df[df["evidence_conflict"] == 1].iloc[0]
    result = generate_playbook(case)

    conflict_detected = any(
        "Conflicting Evidence" in str(item)
        for item in result["playbook_steps"]
    )

    manual_review = any(
        "manual" in str(item).lower()
        for item in result["recommendations"]
    )

    if conflict_detected and manual_review:
        status = "PASS"
    else:
        status = "FAIL"

    print(f"Case ID              : {case['case_id']}")
    print(f"Risk Level           : {case['risk_level']}")
    print(f"Conflict Detected    : {conflict_detected}")
    print(f"Manual Review        : {manual_review}")
    print(f"Result               : {status}")

    return {
        "test_case": "Conflicting Evidence",
        "case_id": case["case_id"],
        "expected_behavior": "Stop and require manual review",
        "result": status
    }


def test_high_risk_human_confirmation(df):
    print("\n" + "=" * 70)
    print("TEST 3: HIGH RISK + HUMAN CONFIRMATION")
    print("=" * 70)

    case = df[
        (df["risk_level"] == "HIGH") &
        (df["evidence_missing"] == 0) &
        (df["evidence_conflict"] == 0)
    ].iloc[0]

    result = generate_playbook(case)

    human_confirmation = result["containment"].get(
    "human_confirmation",
    result["containment"].get("requires_human_confirmation", False)
)
    high_impact_exists = len(result["high_impact_actions"]) > 0

    if human_confirmation and high_impact_exists:
        status = "PASS"
    else:
        status = "FAIL"

    print(f"Case ID              : {case['case_id']}")
    print(f"Risk Level           : {case['risk_level']}")
    print(f"High Impact Action   : {high_impact_exists}")
    print(f"Human Confirmation   : {human_confirmation}")
    print(f"Result               : {status}")

    return {
        "test_case": "High Risk Human Confirmation",
        "case_id": case["case_id"],
        "expected_behavior": "Recommend containment but require human confirmation",
        "result": status
    }


def test_low_risk_monitoring(df):
    print("\n" + "=" * 70)
    print("TEST 4: LOW RISK MONITORING")
    print("=" * 70)

    case = df[
        (df["risk_level"] == "LOW") &
        (df["evidence_missing"] == 0) &
        (df["evidence_conflict"] == 0)
    ].iloc[0]

    result = generate_playbook(case)

    action = result["containment"]["action"]

    monitoring_recommended = (
        "monitor" in action.lower()
    )

    human_confirmation = result["containment"].get(
    "human_confirmation",
    result["containment"].get("requires_human_confirmation", False)
)

    if monitoring_recommended and not human_confirmation:
        status = "PASS"
    else:
        status = "FAIL"

    print(f"Case ID              : {case['case_id']}")
    print(f"Risk Level           : {case['risk_level']}")
    print(f"Containment Action   : {action}")
    print(f"Human Confirmation   : {human_confirmation}")
    print(f"Result               : {status}")

    return {
        "test_case": "Low Risk Monitoring",
        "case_id": case["case_id"],
        "expected_behavior": "Continue monitoring without high-impact confirmation",
        "result": status
    }


def main():

    print("\n")
    print("=" * 70)
    print("SOC PLAYBOOK ASSISTANT - EDGE CASE TESTING")
    print("=" * 70)

    df = pd.read_csv(DATA_FILE)

    results = []

    results.append(test_missing_evidence(df))
    results.append(test_conflicting_evidence(df))
    results.append(test_high_risk_human_confirmation(df))
    results.append(test_low_risk_monitoring(df))

    results_df = pd.DataFrame(results)

    output_file = "data/processed/edge_case_results.csv"
    results_df.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print("EDGE CASE TEST SUMMARY")
    print("=" * 70)

    print(results_df.to_string(index=False))

    passed = (results_df["result"] == "PASS").sum()
    total = len(results_df)

    print("\n" + "-" * 70)
    print(f"Tests Passed : {passed}/{total}")
    print(f"Tests Failed : {total - passed}/{total}")

    if passed == total:
        print("STATUS       : ALL EDGE CASE TESTS PASSED")
    else:
        print("STATUS       : SOME EDGE CASE TESTS FAILED")

    print("-" * 70)
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()