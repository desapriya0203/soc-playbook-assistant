import json
import os
from datetime import datetime


# ============================================================
# EVIDENCE MANAGER
# ============================================================

EVIDENCE_FILE = "data/processed/investigation_records.json"


# ------------------------------------------------------------
# Create storage file if it does not exist
# ------------------------------------------------------------

def initialize_storage():

    os.makedirs("data/processed", exist_ok=True)

    if not os.path.exists(EVIDENCE_FILE):

        with open(EVIDENCE_FILE, "w") as file:
            json.dump([], file, indent=4)


# ------------------------------------------------------------
# Load investigation records
# ------------------------------------------------------------

def load_records():

    initialize_storage()

    with open(EVIDENCE_FILE, "r") as file:
        return json.load(file)


# ------------------------------------------------------------
# Save investigation records
# ------------------------------------------------------------

def save_records(records):

    initialize_storage()

    with open(EVIDENCE_FILE, "w") as file:
        json.dump(records, file, indent=4)


# ============================================================
# RECORD EVIDENCE
# ============================================================

def record_evidence(
    case_id,
    evidence_type,
    evidence_description,
    analyst
):

    records = load_records()

    evidence_record = {

        "record_type": "EVIDENCE",

        "case_id": case_id,

        "evidence_type": evidence_type,

        "description": evidence_description,

        "analyst": analyst,

        "timestamp":
            datetime.now().isoformat(),

    }

    records.append(evidence_record)

    save_records(records)

    return evidence_record


# ============================================================
# HUMAN CONFIRMATION
# ============================================================

def record_confirmation(
    case_id,
    action,
    decision,
    analyst
):

    records = load_records()

    confirmation_record = {

        "record_type": "CONFIRMATION",

        "case_id": case_id,

        "action": action,

        "decision": decision,

        "analyst": analyst,

        "timestamp":
            datetime.now().isoformat(),

    }

    records.append(confirmation_record)

    save_records(records)

    return confirmation_record


# ============================================================
# OVERRIDE ACTION
# ============================================================

def record_override(
    case_id,
    recommended_action,
    override_reason,
    analyst
):

    records = load_records()

    override_record = {

        "record_type": "OVERRIDE",

        "case_id": case_id,

        "recommended_action":
            recommended_action,

        "decision":
            "OVERRIDDEN",

        "override_reason":
            override_reason,

        "analyst":
            analyst,

        "timestamp":
            datetime.now().isoformat(),

    }

    records.append(override_record)

    save_records(records)

    return override_record


# ============================================================
# GET CASE HISTORY
# ============================================================

def get_case_history(case_id):

    records = load_records()

    case_records = [

        record
        for record in records
        if record["case_id"] == case_id

    ]

    return case_records


# ============================================================
# DISPLAY CASE HISTORY
# ============================================================

def display_case_history(case_id):

    history = get_case_history(case_id)

    print("\n" + "=" * 70)
    print("CASE INVESTIGATION HISTORY")
    print("=" * 70)

    print("\nCase ID:", case_id)

    if not history:

        print("\nNo investigation records found.")

        return

    for index, record in enumerate(history, start=1):

        print(f"\nRecord {index}")
        print("-" * 50)

        print(
            "Type:",
            record["record_type"]
        )

        print(
            "Analyst:",
            record["analyst"]
        )

        print(
            "Timestamp:",
            record["timestamp"]
        )

        if record["record_type"] == "EVIDENCE":

            print(
                "Evidence Type:",
                record["evidence_type"]
            )

            print(
                "Description:",
                record["description"]
            )

        elif record["record_type"] == "CONFIRMATION":

            print(
                "Action:",
                record["action"]
            )

            print(
                "Decision:",
                record["decision"]
            )

        elif record["record_type"] == "OVERRIDE":

            print(
                "Recommended Action:",
                record["recommended_action"]
            )

            print(
                "Decision:",
                record["decision"]
            )

            print(
                "Override Reason:",
                record["override_reason"]
            )


# ============================================================
# TEST THE EVIDENCE MANAGER
# ============================================================

if __name__ == "__main__":

    test_case_id = "CASE-0001"

    analyst_name = "Junior Analyst"

    print("\n" + "=" * 70)
    print("SOC EVIDENCE MANAGER TEST")
    print("=" * 70)


    # --------------------------------------------------------
    # 1. Record evidence
    # --------------------------------------------------------

    evidence = record_evidence(

        case_id=test_case_id,

        evidence_type="Authentication Log",

        evidence_description=(
            "Authentication history reviewed. "
            "Recent login events recorded."
        ),

        analyst=analyst_name
    )

    print("\nEvidence recorded successfully.")


    # --------------------------------------------------------
    # 2. Record human confirmation
    # --------------------------------------------------------

    confirmation = record_confirmation(

        case_id=test_case_id,

        action="Continue Investigation",

        decision="APPROVED",

        analyst=analyst_name
    )

    print("Human confirmation recorded.")


    # --------------------------------------------------------
    # 3. Record override
    # --------------------------------------------------------

    override = record_override(

        case_id=test_case_id,

        recommended_action="Isolate Endpoint",

        override_reason=(
            "Endpoint activity was verified "
            "as legitimate business activity."
        ),

        analyst=analyst_name
    )

    print("Override reason recorded.")


    # --------------------------------------------------------
    # 4. Display history
    # --------------------------------------------------------

    display_case_history(test_case_id)

    print("\n" + "=" * 70)
    print("EVIDENCE MANAGER TEST COMPLETED")
    print("=" * 70)

    print(
        "\nRecords saved at:",
        EVIDENCE_FILE
    )