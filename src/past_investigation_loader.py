import pandas as pd
import os


# ============================================================
# PAST INVESTIGATION LOADER
# ============================================================

DATA_FILE = "data/processed/past_investigations.csv"


def load_past_investigations():
    """
    Load previous SOC investigation records.
    """

    if not os.path.exists(DATA_FILE):
        return []

    df = pd.read_csv(DATA_FILE)

    return df.to_dict(orient="records")


def get_similar_investigations(alert_type, max_results=5):
    """
    Return previous investigations matching the alert type.
    """

    investigations = load_past_investigations()

    if not investigations:
        return []

    matching_investigations = []

    for investigation in investigations:
        investigation_alert = str(
            investigation.get("alert_type", "")
        ).strip()

        if investigation_alert.lower() == str(
            alert_type
        ).strip().lower():
            matching_investigations.append(
                investigation
            )

    return matching_investigations[:max_results]
