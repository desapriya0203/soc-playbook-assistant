import pandas as pd
import os


# ============================================================
# APPROVED PROCEDURE LOADER
# ============================================================

DATA_FILE = "data/processed/approved_procedures.csv"


def load_approved_procedures():
    """
    Load approved SOC investigation procedures.
    """

    if not os.path.exists(DATA_FILE):
        return []

    df = pd.read_csv(DATA_FILE)

    return df.to_dict(orient="records")


def get_procedures_for_alert(alert_type):
    """
    Return procedures applicable to the given alert type.

    Procedures marked as 'Any' are also included.
    """

    procedures = load_approved_procedures()

    if not procedures:
        return []

    matching_procedures = []

    for procedure in procedures:
        procedure_alert = str(
            procedure.get("alert_type", "")
        ).strip()

        if (
            procedure_alert.lower() == str(alert_type).strip().lower()
            or procedure_alert.lower() == "any"
        ):
            matching_procedures.append(procedure)

    return matching_procedures
