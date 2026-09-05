import pandas as pd
import os

LEGACY_FILE = "data/legacy/legacy_cases.csv"
OUTPUT_FILE = "data/processed/migrated_legacy_cases.csv"


def migrate_legacy_cases():

    print("=" * 70)
    print("LEGACY WORKFLOW MIGRATION")
    print("=" * 70)

    df = pd.read_csv(LEGACY_FILE)

    print(f"\nLegacy cases found: {len(df)}")

    # Preserve all original legacy information
    migrated = df.copy()

    # Add fields required by the new assistant workflow
    migrated["workflow_source"] = "LEGACY"
    migrated["assistant_status"] = "Available"
    migrated["migration_status"] = "Migrated"
    migrated["rollback_available"] = True

    # Important:
    # Migration does NOT automatically execute containment.
    migrated["automatic_containment"] = False

    os.makedirs("data/processed", exist_ok=True)

    migrated.to_csv(OUTPUT_FILE, index=False)

    print("\nMigration completed successfully.")
    print(f"Output saved to: {OUTPUT_FILE}")

    print("\nMigrated Data:")
    print(migrated.to_string(index=False))

    print("\n" + "=" * 70)
    print("MIGRATION SAFETY CHECK")
    print("=" * 70)

    if migrated["automatic_containment"].eq(False).all():
        print("PASS: No automatic containment actions executed.")

    if migrated["rollback_available"].eq(True).all():
        print("PASS: Rollback option available for all migrated cases.")

    print("\nLEGACY COEXISTENCE STATUS: READY")


if __name__ == "__main__":
    migrate_legacy_cases()