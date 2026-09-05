import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1. LOAD DATASET
# ==============================

file_path = "data/raw/synthetic_soc_cases.csv"

df = pd.read_csv(file_path)

print("\n" + "=" * 60)
print("SOC PLAYBOOK ASSISTANT - EDA")
print("=" * 60)


# ==============================
# 2. BASIC DATASET INFORMATION
# ==============================

print("\n--- DATASET SHAPE ---")

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


print("\n--- COLUMN NAMES ---")

for column in df.columns:
    print(column)


# ==============================
# 3. FIRST 5 RECORDS
# ==============================

print("\n--- FIRST 5 RECORDS ---")

print(df.head())


# ==============================
# 4. DATA TYPES
# ==============================

print("\n--- DATA TYPES ---")

print(df.dtypes)


# ==============================
# 5. MISSING VALUES
# ==============================

print("\n--- MISSING VALUES ---")

missing_values = df.isnull().sum()

print(missing_values)


# ==============================
# 6. DUPLICATE RECORDS
# ==============================

print("\n--- DUPLICATES ---")

duplicates = df.duplicated().sum()

print("Duplicate rows:", duplicates)


# ==============================
# 7. RISK DISTRIBUTION
# ==============================

print("\n--- RISK LEVEL DISTRIBUTION ---")

risk_distribution = df["risk_level"].value_counts()

print(risk_distribution)


# ==============================
# 8. ALERT TYPE DISTRIBUTION
# ==============================

print("\n--- ALERT TYPE DISTRIBUTION ---")

alert_distribution = df["alert_type"].value_counts()

print(alert_distribution)


# ==============================
# 9. INVESTIGATION STATUS
# ==============================

print("\n--- INVESTIGATION STATUS ---")

status_distribution = df["investigation_status"].value_counts()

print(status_distribution)


# ==============================
# 10. CASE OUTCOME
# ==============================

print("\n--- CASE OUTCOME ---")

outcome_distribution = df["case_outcome"].value_counts()

print(outcome_distribution)


# ==============================
# 11. CONTAINMENT DECISIONS
# ==============================

print("\n--- CONTAINMENT DECISIONS ---")

containment_distribution = df["containment_decision"].value_counts()

print(containment_distribution)


# ==============================
# 12. FAILURE CASES
# ==============================

print("\n--- FAILURE CASE ANALYSIS ---")

print(
    "Missing Evidence Cases:",
    df["evidence_missing"].sum()
)

print(
    "Conflicting Evidence Cases:",
    df["evidence_conflict"].sum()
)


# ==============================
# 13. RISK SCORE STATISTICS
# ==============================

print("\n--- RISK SCORE STATISTICS ---")

print(df["risk_score"].describe())


# ==============================
# 14. SECURITY INDICATORS
# ==============================

security_features = [
    "successful_login",
    "new_ip",
    "location_change",
    "endpoint_anomaly",
    "email_anomaly",
    "cloud_anomaly",
    "previous_incident"
]

print("\n--- SECURITY INDICATOR COUNTS ---")

for feature in security_features:

    count = df[feature].sum()

    print(f"{feature}: {count}")


# ==============================
# 15. RISK LEVEL vs SECURITY FEATURES
# ==============================

print("\n--- AVERAGE FEATURES BY RISK LEVEL ---")

risk_analysis = df.groupby("risk_level")[
    [
        "failed_login_count",
        "successful_login",
        "new_ip",
        "location_change",
        "endpoint_anomaly",
        "email_anomaly",
        "cloud_anomaly"
    ]
].mean()

print(risk_analysis)


# ==============================
# 16. GRAPH - RISK DISTRIBUTION
# ==============================

plt.figure(figsize=(7, 5))

risk_distribution.plot(kind="bar")

plt.title("SOC Risk Level Distribution")

plt.xlabel("Risk Level")

plt.ylabel("Number of Cases")

plt.tight_layout()

plt.show()


# ==============================
# 17. GRAPH - ALERT TYPES
# ==============================

plt.figure(figsize=(8, 5))

alert_distribution.plot(kind="bar")

plt.title("Alert Type Distribution")

plt.xlabel("Alert Type")

plt.ylabel("Number of Cases")

plt.xticks(rotation=30)

plt.tight_layout()

plt.show()


# ==============================
# 18. GRAPH - RISK SCORE
# ==============================

plt.figure(figsize=(8, 5))

df["risk_score"].plot(
    kind="hist",
    bins=20
)

plt.title("Risk Score Distribution")

plt.xlabel("Risk Score")

plt.ylabel("Number of Cases")

plt.tight_layout()

plt.show()


# ==============================
# 19. FINAL SUMMARY
# ==============================

print("\n" + "=" * 60)
print("EDA COMPLETED")
print("=" * 60)

print("\nDataset is ready for:")
print("1. Data Cleaning")
print("2. Feature Engineering")
print("3. ML Model Training")
print("4. Playbook Recommendation Engine")