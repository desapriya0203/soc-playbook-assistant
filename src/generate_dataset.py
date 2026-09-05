import pandas as pd
import numpy as np
import random
import os

# Reproducibility
random.seed(42)
np.random.seed(42)

# Number of cases
N = 2000

records = []

alert_types = [
    "Suspicious Login",
    "Endpoint Malware",
    "Phishing Email",
    "Cloud Account Anomaly"
]

locations = [
    "Chennai",
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Unknown"
]

for i in range(1, N + 1):

    # -----------------------------
    # Generate security indicators
    # -----------------------------

    alert_type = random.choice(alert_types)

    failed_logins = np.random.poisson(2)

    successful_login = random.choice([0, 1])

    new_ip = random.choice([0, 1])

    location_change = random.choice([0, 1])

    endpoint_anomaly = random.choice([0, 1])

    email_anomaly = random.choice([0, 1])

    cloud_anomaly = random.choice([0, 1])

    previous_incident = random.choice([0, 1])

    evidence_missing = random.choice([0, 0, 0, 1])

    evidence_conflict = random.choice([0, 0, 1])


    # -----------------------------
    # Calculate risk score
    # -----------------------------

    risk_score = 0

    if failed_logins >= 5:
        risk_score += 20

    if successful_login == 1:
        risk_score += 10

    if new_ip == 1:
        risk_score += 15

    if location_change == 1:
        risk_score += 15

    if endpoint_anomaly == 1:
        risk_score += 15

    if email_anomaly == 1:
        risk_score += 10

    if cloud_anomaly == 1:
        risk_score += 10

    if previous_incident == 1:
        risk_score += 5

    # Missing evidence reduces confidence
    if evidence_missing == 1:
        risk_score -= 5

    risk_score = max(0, min(100, risk_score))


    # -----------------------------
    # Risk classification
    # -----------------------------

    if risk_score >= 60:
        risk_level = "HIGH"

    elif risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    # -----------------------------
    # Investigation steps
    # -----------------------------

    investigation_steps = [
        "Validate Alert",
        "Check Authentication History"
    ]

    if new_ip == 1 or location_change == 1:
        investigation_steps.append(
            "Investigate IP and Location"
        )

    if endpoint_anomaly == 1:
        investigation_steps.append(
            "Review Endpoint Activity"
        )

    if email_anomaly == 1:
        investigation_steps.append(
            "Review Email Activity"
        )

    if cloud_anomaly == 1:
        investigation_steps.append(
            "Review Cloud Activity"
        )

    investigation_steps.extend([
        "Collect Evidence",
        "Assess Risk",
        "Determine Containment"
    ])


    # -----------------------------
    # Containment decision
    # -----------------------------

    if risk_level == "HIGH":

        containment_decision = random.choice([
            "Isolate Endpoint",
            "Disable Account",
            "Escalate to Senior Analyst"
        ])

    elif risk_level == "MEDIUM":

        containment_decision = "Escalate for Review"

    else:

        containment_decision = "Continue Monitoring"


    # -----------------------------
    # Failure-state handling
    # -----------------------------

    if evidence_missing == 1:

        investigation_status = (
            "BLOCKED - Missing Evidence"
        )

    elif evidence_conflict == 1:

        investigation_status = (
            "MANUAL REVIEW - Conflicting Evidence"
        )

    else:

        investigation_status = (
            "Normal Investigation"
        )


    # -----------------------------
    # Case outcome
    # -----------------------------

    if risk_level == "HIGH":

        case_outcome = random.choice([
            "Confirmed Incident",
            "Escalated Incident"
        ])

    elif risk_level == "MEDIUM":

        case_outcome = random.choice([
            "Needs Further Investigation",
            "Benign Activity"
        ])

    else:

        case_outcome = "Benign Activity"


    # -----------------------------
    # Store case
    # -----------------------------

    records.append({

        "case_id":
            f"CASE-{i:04d}",

        "alert_type":
            alert_type,

        "failed_login_count":
            failed_logins,

        "successful_login":
            successful_login,

        "new_ip":
            new_ip,

        "location_change":
            location_change,

        "login_location":
            random.choice(locations),

        "endpoint_anomaly":
            endpoint_anomaly,

        "email_anomaly":
            email_anomaly,

        "cloud_anomaly":
            cloud_anomaly,

        "previous_incident":
            previous_incident,

        "evidence_missing":
            evidence_missing,

        "evidence_conflict":
            evidence_conflict,

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "investigation_steps":
            " → ".join(investigation_steps),

        "containment_decision":
            containment_decision,

        "investigation_status":
            investigation_status,

        "case_outcome":
            case_outcome
    })


# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(records)


# -----------------------------
# Create output directory
# -----------------------------

os.makedirs("data/raw", exist_ok=True)


# -----------------------------
# Save dataset
# -----------------------------

output_path = "data/raw/synthetic_soc_cases.csv"

df.to_csv(
    output_path,
    index=False
)


# -----------------------------
# Display results
# -----------------------------

print("\n" + "=" * 60)
print("SOC PLAYBOOK ASSISTANT")
print("SYNTHETIC DATASET CREATED")
print("=" * 60)

print(f"\nTotal Cases    : {len(df)}")
print(f"Total Features : {len(df.columns)}")

print("\nRisk Distribution:")
print(df["risk_level"].value_counts())

print("\nInvestigation Status:")
print(df["investigation_status"].value_counts())

print("\nDataset saved at:")
print(output_path)

print("\nFirst 5 cases:")
print(df.head())