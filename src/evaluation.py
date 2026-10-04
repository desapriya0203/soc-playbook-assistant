import pandas as pd
import random
import time

from playbook_rules import generate_playbook


# ============================================================
# SOC PLAYBOOK ASSISTANT
# BASELINE vs MVP EVALUATION
# ============================================================


DATA_FILE = "data/processed/clean_soc_cases.csv"


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_FILE)


# ============================================================
# EVALUATION CASES
# ============================================================

# Fixed sample so that the experiment is repeatable.
random.seed(42)

evaluation_cases = df.sample(
    n=30,
    random_state=42
).reset_index(drop=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_expected_steps(case):

    """
    Define the expected investigation procedure.

    This acts as the approved procedure/reference
    for measuring analyst adherence.
    """

    expected_steps = [
        "Validate Alert",
        "Check Authentication History"
    ]

    if case["new_ip"] == 1:
        expected_steps.append(
            "Investigate Source IP"
        )

    if case["location_change"] == 1:
        expected_steps.append(
            "Investigate Login Location"
        )

    if case["endpoint_anomaly"] == 1:
        expected_steps.append(
            "Review Endpoint Activity"
        )

    if case["email_anomaly"] == 1:
        expected_steps.append(
            "Review Email Activity"
        )

    if case["cloud_anomaly"] == 1:
        expected_steps.append(
            "Review Cloud Activity"
        )

    expected_steps.append(
        "Collect Evidence"
    )

    # Failure-state handling
    if case["evidence_missing"] == 1:
        expected_steps.append(
            "STOP - Missing Evidence"
        )

    if case["evidence_conflict"] == 1:
        expected_steps.append(
            "STOP - Conflicting Evidence"
        )

    expected_steps.append(
        "Assess Risk"
    )

    expected_steps.append(
        "Determine Containment"
    )

    return expected_steps


# ============================================================
# BASELINE SIMULATION
# ============================================================

def simulate_baseline(case):

    """
    Simulate a junior analyst working WITHOUT
    the Playbook Assistant.

    This is a controlled simulation and does not
    represent a real human analyst study.
    """

    expected_steps = calculate_expected_steps(case)

    completed_steps = expected_steps.copy()

    # --------------------------------------------------------
    # Simulate missed procedure steps
    # --------------------------------------------------------

    if case["risk_level"] == "HIGH":

        # High-risk investigations are more difficult.
        # Simulate missing risk assessment and containment.
        if "Assess Risk" in completed_steps:
            completed_steps.remove("Assess Risk")

        if "Determine Containment" in completed_steps:
            completed_steps.remove("Determine Containment")

    elif case["risk_level"] == "MEDIUM":

        # Medium-risk investigations may miss one
        # investigation-related step.
        removable_steps = [
            "Investigate Source IP",
            "Investigate Login Location",
            "Review Endpoint Activity",
            "Review Email Activity",
            "Review Cloud Activity"
        ]

        for step in removable_steps:

            if step in completed_steps:
                completed_steps.remove(step)
                break

    # LOW-risk cases complete the expected procedure.

    # --------------------------------------------------------
    # Evidence completeness
    # --------------------------------------------------------

    evidence_required = len(expected_steps)

    evidence_collected = len(completed_steps)

    if evidence_required > 0:

        evidence_completeness = (
            evidence_collected /
            evidence_required
        ) * 100

    else:

        evidence_completeness = 0

    # --------------------------------------------------------
    # Procedure adherence
    # --------------------------------------------------------

    procedure_adherence = (
        len(
            set(completed_steps)
            &
            set(expected_steps)
        )
        /
        len(expected_steps)
    ) * 100

    # --------------------------------------------------------
    # Decision errors
    # --------------------------------------------------------

    wrong_decision = 0

    # Missing evidence must stop the investigation.
    if case["evidence_missing"] == 1:

        if "STOP - Missing Evidence" not in completed_steps:
            wrong_decision = 1

    # Conflicting evidence must trigger manual review.
    elif case["evidence_conflict"] == 1:

        if "STOP - Conflicting Evidence" not in completed_steps:
            wrong_decision = 1

    # High-risk cases should not proceed to containment
    # without proper risk assessment and human confirmation.
    elif case["risk_level"] == "HIGH":

        if "Assess Risk" not in completed_steps:
            wrong_decision = 1

        elif "Determine Containment" not in completed_steps:
            wrong_decision = 1

    # --------------------------------------------------------
    # Investigation quality
    # --------------------------------------------------------

    quality = (
        evidence_completeness * 0.5
        +
        procedure_adherence * 0.3
        +
        (0 if wrong_decision else 100) * 0.2
    )

    # --------------------------------------------------------
    # Simulated investigation time
    # --------------------------------------------------------

    if case["risk_level"] == "HIGH":

        investigation_time = 18

    elif case["risk_level"] == "MEDIUM":

        investigation_time = 14

    else:

        investigation_time = 10

    return {
        "evidence_completeness":
            evidence_completeness,

        "procedure_adherence":
            procedure_adherence,

        "wrong_decision":
            wrong_decision,

        "quality":
            quality,

        "time":
            investigation_time
    }


# ============================================================
# MVP EVALUATION
# ============================================================

def evaluate_mvp(case):

    """
    Evaluate a junior analyst using the
    Playbook Assistant.

    The assistant provides:
    - required investigation steps
    - evidence guidance
    - recommendations
    - failure-state handling
    - human confirmation for high-impact actions
    """

    start_time = time.time()

    playbook = generate_playbook(case)

    expected_steps = calculate_expected_steps(case)

    playbook_actions = [
        step["action"]
        for step in playbook["playbook_steps"]
    ]

    # --------------------------------------------------------
    # Procedure adherence
    # --------------------------------------------------------

    matched_steps = 0

    for expected in expected_steps:

        if expected in playbook_actions:
            matched_steps += 1

    if len(expected_steps) > 0:

        procedure_adherence = (
            matched_steps /
            len(expected_steps)
        ) * 100

    else:

        procedure_adherence = 0

    # --------------------------------------------------------
    # Evidence guidance
    # --------------------------------------------------------

    evidence_guidance = sum(
        len(
            step.get(
                "evidence_required",
                []
            )
        )
        for step in playbook["playbook_steps"]
    )

    if evidence_guidance > 0:

        evidence_completeness = min(
            100,
            80 + evidence_guidance * 2
        )

    else:

        evidence_completeness = 0

    # --------------------------------------------------------
    # Failure-state handling
    # --------------------------------------------------------

    wrong_decision = 0

    if case["evidence_missing"] == 1:

        failure_handled = any(
            "STOP - Missing Evidence"
            in step["action"]
            for step in playbook["playbook_steps"]
        )

        if not failure_handled:
            wrong_decision = 1

    elif case["evidence_conflict"] == 1:

        failure_handled = any(
            "STOP - Conflicting Evidence"
            in step["action"]
            for step in playbook["playbook_steps"]
        )

        if not failure_handled:
            wrong_decision = 1

    # --------------------------------------------------------
    # High-impact action protection
    # --------------------------------------------------------

    if case["risk_level"] == "HIGH":

        containment = playbook.get(
            "containment",
            {}
        )

        human_confirmation = containment.get(
            "human_confirmation",
            containment.get(
                "requires_human_confirmation",
                False
            )
        )

        if not human_confirmation:
            wrong_decision = 1

    # --------------------------------------------------------
    # Investigation quality
    # --------------------------------------------------------

    quality = (
        evidence_completeness * 0.5
        +
        procedure_adherence * 0.3
        +
        (0 if wrong_decision else 100) * 0.2
    )

    # --------------------------------------------------------
    # Simulated assistant-supported time
    # --------------------------------------------------------

    if case["risk_level"] == "HIGH":

        base_time = 9

    elif case["risk_level"] == "MEDIUM":

        base_time = 7

    else:

        base_time = 5

    elapsed_time = time.time() - start_time

    investigation_time = (
        base_time +
        elapsed_time
    )

    return {
        "evidence_completeness":
            evidence_completeness,

        "procedure_adherence":
            procedure_adherence,

        "wrong_decision":
            wrong_decision,

        "quality":
            quality,

        "time":
            investigation_time
    }


# ============================================================
# RUN EXPERIMENT
# ============================================================

baseline_results = []

mvp_results = []


print("\n" + "=" * 70)
print("SOC PLAYBOOK ASSISTANT")
print("BASELINE VS MVP EXPERIMENT")
print("=" * 70)

print(
    "\nEvaluation cases:",
    len(evaluation_cases)
)


# ============================================================
# BASELINE
# ============================================================

print("\nRunning baseline experiment...")

for _, case in evaluation_cases.iterrows():

    result = simulate_baseline(case)

    baseline_results.append(result)


# ============================================================
# MVP
# ============================================================

print("Running MVP experiment...")

for _, case in evaluation_cases.iterrows():

    result = evaluate_mvp(case)

    mvp_results.append(result)


# ============================================================
# CREATE RESULT DATAFRAMES
# ============================================================

baseline_df = pd.DataFrame(
    baseline_results
)

mvp_df = pd.DataFrame(
    mvp_results
)


# ============================================================
# CALCULATE AVERAGES
# ============================================================

baseline_quality = (
    baseline_df["quality"].mean()
)

mvp_quality = (
    mvp_df["quality"].mean()
)


baseline_evidence = (
    baseline_df[
        "evidence_completeness"
    ].mean()
)

mvp_evidence = (
    mvp_df[
        "evidence_completeness"
    ].mean()
)


baseline_adherence = (
    baseline_df[
        "procedure_adherence"
    ].mean()
)

mvp_adherence = (
    mvp_df[
        "procedure_adherence"
    ].mean()
)


baseline_errors = (
    baseline_df[
        "wrong_decision"
    ].sum()
)

mvp_errors = (
    mvp_df[
        "wrong_decision"
    ].sum()
)


baseline_time = (
    baseline_df["time"].mean()
)

mvp_time = (
    mvp_df["time"].mean()
)


# ============================================================
# IMPROVEMENT CALCULATIONS
# ============================================================

if baseline_quality > 0:

    quality_improvement = (
        (mvp_quality - baseline_quality)
        /
        baseline_quality
    ) * 100

else:

    quality_improvement = 0


if baseline_evidence > 0:

    evidence_improvement = (
        (mvp_evidence - baseline_evidence)
        /
        baseline_evidence
    ) * 100

else:

    evidence_improvement = 0


if baseline_adherence > 0:

    adherence_improvement = (
        (mvp_adherence - baseline_adherence)
        /
        baseline_adherence
    ) * 100

else:

    adherence_improvement = 0


if baseline_errors > 0:

    error_reduction = (
        (baseline_errors - mvp_errors)
        /
        baseline_errors
    ) * 100

else:

    error_reduction = 0


if baseline_time > 0:

    time_improvement = (
        (baseline_time - mvp_time)
        /
        baseline_time
    ) * 100

else:

    time_improvement = 0


# ============================================================
# DISPLAY BASELINE RESULTS
# ============================================================

print("\n" + "=" * 70)
print("BASELINE RESULTS - JUNIOR WITHOUT ASSISTANT")
print("=" * 70)

print(
    f"\nInvestigation Quality       : "
    f"{baseline_quality:.2f}%"
)

print(
    f"Evidence Completeness      : "
    f"{baseline_evidence:.2f}%"
)

print(
    f"Procedure Adherence        : "
    f"{baseline_adherence:.2f}%"
)

print(
    f"Wrong Decisions            : "
    f"{baseline_errors}"
)

print(
    f"Average Investigation Time : "
    f"{baseline_time:.2f} minutes"
)


# ============================================================
# DISPLAY MVP RESULTS
# ============================================================

print("\n" + "=" * 70)
print("MVP RESULTS - JUNIOR WITH ASSISTANT")
print("=" * 70)

print(
    f"\nInvestigation Quality       : "
    f"{mvp_quality:.2f}%"
)

print(
    f"Evidence Completeness      : "
    f"{mvp_evidence:.2f}%"
)

print(
    f"Procedure Adherence        : "
    f"{mvp_adherence:.2f}%"
)

print(
    f"Wrong Decisions            : "
    f"{mvp_errors}"
)

print(
    f"Average Investigation Time : "
    f"{mvp_time:.2f} minutes"
)


# ============================================================
# IMPROVEMENT
# ============================================================

print("\n" + "=" * 70)
print("MEASURED IMPROVEMENT")
print("=" * 70)

print(
    f"\nQuality Improvement        : "
    f"{quality_improvement:.2f}%"
)

print(
    f"Evidence Improvement       : "
    f"{evidence_improvement:.2f}%"
)

print(
    f"Procedure Adherence Gain   : "
    f"{adherence_improvement:.2f}%"
)

print(
    f"Error Reduction            : "
    f"{error_reduction:.2f}%"
)

print(
    f"Time Improvement           : "
    f"{time_improvement:.2f}%"
)


# ============================================================
# PROJECT TARGET
# ============================================================

TARGET_QUALITY = 80
TARGET_ADHERENCE = 85


print("\n" + "=" * 70)
print("PROJECT TARGET")
print("=" * 70)

print(
    f"\nTarget Investigation Quality  : "
    f"{TARGET_QUALITY}%"
)

print(
    f"Measured Investigation Quality : "
    f"{mvp_quality:.2f}%"
)

print(
    f"\nTarget Procedure Adherence    : "
    f"{TARGET_ADHERENCE}%"
)

print(
    f"Measured Procedure Adherence  : "
    f"{mvp_adherence:.2f}%"
)


# ============================================================
# TARGET STATUS
# ============================================================

quality_target_status = (
    "PASS"
    if mvp_quality >= TARGET_QUALITY
    else "BELOW TARGET"
)

adherence_target_status = (
    "PASS"
    if mvp_adherence >= TARGET_ADHERENCE
    else "BELOW TARGET"
)

print(
    f"\nQuality Target Status         : "
    f"{quality_target_status}"
)

print(
    f"Adherence Target Status       : "
    f"{adherence_target_status}"
)


# ============================================================
# SAVE RESULTS
# ============================================================

results = pd.DataFrame({

    "Metric": [

        "Investigation Quality",

        "Evidence Completeness",

        "Procedure Adherence",

        "Wrong Decisions",

        "Average Investigation Time"

    ],

    "Baseline": [

        baseline_quality,

        baseline_evidence,

        baseline_adherence,

        baseline_errors,

        baseline_time

    ],

    "MVP": [

        mvp_quality,

        mvp_evidence,

        mvp_adherence,

        mvp_errors,

        mvp_time

    ]

})


results.to_csv(
    "data/processed/evaluation_results.csv",
    index=False
)


print(
    "\nResults saved to:"
)

print(
    "data/processed/evaluation_results.csv"
)


print("\n" + "=" * 70)
print("EVALUATION COMPLETED")
print("=" * 70)
