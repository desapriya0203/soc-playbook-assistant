import pandas as pd
import os

# ==========================================
# 1. LOAD RAW DATA
# ==========================================

input_path = "data/raw/synthetic_soc_cases.csv"

df = pd.read_csv(input_path)

print("\n" + "=" * 60)
print("SOC PLAYBOOK ASSISTANT - DATA CLEANING")
print("=" * 60)

print("\nOriginal dataset shape:")
print(df.shape)


# ==========================================
# 2. CHECK DUPLICATES
# ==========================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")
else:
    print("No duplicate rows found.")


# ==========================================
# 3. CHECK MISSING VALUES
# ==========================================

print("\nMissing values before cleaning:")

print(df.isnull().sum())


# ==========================================
# 4. HANDLE MISSING VALUES
# ==========================================

# Numeric columns
numeric_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns

for column in numeric_columns:
    if df[column].isnull().sum() > 0:
        df[column] = df[column].fillna(
            df[column].median()
        )


# Text columns
text_columns = df.select_dtypes(
    include=["object"]
).columns

for column in text_columns:
    if df[column].isnull().sum() > 0:
        df[column] = df[column].fillna("Unknown")


print("\nMissing values after cleaning:")

print(df.isnull().sum())


# ==========================================
# 5. VALIDATE RISK SCORE
# ==========================================

invalid_scores = (
    (df["risk_score"] < 0) |
    (df["risk_score"] > 100)
).sum()

print("\nInvalid risk scores:", invalid_scores)

if invalid_scores > 0:

    df["risk_score"] = df["risk_score"].clip(
        lower=0,
        upper=100
    )

    print("Risk scores corrected to 0-100 range.")

else:

    print("All risk scores are valid.")


# ==========================================
# 6. VALIDATE RISK LEVEL
# ==========================================

valid_risk_levels = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

invalid_risk_levels = (
    ~df["risk_level"].isin(valid_risk_levels)
).sum()

print("\nInvalid risk levels:", invalid_risk_levels)

if invalid_risk_levels > 0:

    # Recalculate invalid values from risk score
    def assign_risk(score):

        if score >= 60:
            return "HIGH"

        elif score >= 30:
            return "MEDIUM"

        else:
            return "LOW"

    mask = ~df["risk_level"].isin(
        valid_risk_levels
    )

    df.loc[mask, "risk_level"] = (
        df.loc[mask, "risk_score"]
        .apply(assign_risk)
    )

    print("Invalid risk levels corrected.")

else:

    print("All risk levels are valid.")


# ==========================================
# 7. VALIDATE BINARY SECURITY FEATURES
# ==========================================

binary_columns = [
    "successful_login",
    "new_ip",
    "location_change",
    "endpoint_anomaly",
    "email_anomaly",
    "cloud_anomaly",
    "previous_incident",
    "evidence_missing",
    "evidence_conflict"
]

print("\nBinary feature validation:")

for column in binary_columns:

    invalid_values = (
        ~df[column].isin([0, 1])
    ).sum()

    print(
        f"{column}: {invalid_values} invalid values"
    )


# ==========================================
# 8. VALIDATE FAILURE STATES
# ==========================================

print("\nFailure-state validation:")

missing_evidence_cases = df[
    df["evidence_missing"] == 1
]

conflicting_evidence_cases = df[
    df["evidence_conflict"] == 1
]

print(
    "Missing evidence cases:",
    len(missing_evidence_cases)
)

print(
    "Conflicting evidence cases:",
    len(conflicting_evidence_cases)
)


# ==========================================
# 9. CHECK CASE IDs
# ==========================================

duplicate_case_ids = df["case_id"].duplicated().sum()

print("\nDuplicate case IDs:", duplicate_case_ids)


# ==========================================
# 10. CREATE CLEAN DATA DIRECTORY
# ==========================================

os.makedirs(
    "data/processed",
    exist_ok=True
)


# ==========================================
# 11. SAVE CLEAN DATA
# ==========================================

output_path = (
    "data/processed/clean_soc_cases.csv"
)

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 12. FINAL REPORT
# ==========================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print("\nFinal dataset shape:")
print(df.shape)

print("\nFinal risk distribution:")
print(df["risk_level"].value_counts())

print("\nFinal dataset saved at:")
print(output_path)

print("\nDataset is ready for the next stage.")