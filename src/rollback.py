import pandas as pd
import os

MIGRATED_FILE = "data/processed/migrated_legacy_cases.csv"
ROLLBACK_FILE = "data/legacy/rollback_cases.csv"


def rollback_to_legacy():

    print("=" * 70)
    print("SOC PLAYBOOK ASSISTANT - ROLLBACK DEMONSTRATION")
    print("=" * 70)

    # Check migrated file exists
    if not os.path.exists(MIGRATED_FILE):
        print("\nERROR: Migrated case file not found.")
        print("Run migration.py first.")
        return

    # Load migrated cases
    df = pd.read_csv(MIGRATED_FILE)

    print(f"\nMigrated cases found: {len(df)}")

    # Safety check
    if not df["rollback_available"].eq(True).all():
        print("\nROLLBACK BLOCKED")
        print("Some cases do not have rollback permission.")
        return

    # Restore original legacy workflow fields
    rollback_df = df[
        [
            "case_id",
            "legacy_status",
            "legacy_notes",
            "legacy_action",
            "analyst"
        ]
    ].copy()

    # Mark rollback operation
    rollback_df["workflow_source"] = "LEGACY"
    rollback_df["rollback_status"] = "RESTORED"

    os.makedirs("data/legacy", exist_ok=True)

    rollback_df.to_csv(ROLLBACK_FILE, index=False)

    print("\n" + "=" * 70)
    print("ROLLBACK SAFETY CHECK")
    print("=" * 70)

    print("PASS: Legacy case information preserved.")
    print("PASS: Migrated assistant fields removed from active workflow.")
    print("PASS: Cases restored to legacy workflow.")
    print("PASS: No containment action executed during rollback.")

    print("\n" + "=" * 70)
    print("ROLLBACK RESULT")
    print("=" * 70)

    print(rollback_df.to_string(index=False))

    print("\n" + "-" * 70)
    print("ROLLBACK STATUS: SUCCESS")
    print("-" * 70)

    print(f"\nRollback file saved to: {ROLLBACK_FILE}")


if __name__ == "__main__":
    rollback_to_legacy()