# Deployment Checklist

## Application

-   [ ] Verify Python environment and required packages.
-   [ ] Verify `data/processed/clean_soc_cases.csv` is available.
-   [ ] Verify `src/app.py` starts successfully with Streamlit.
-   [ ] Verify the selected case generates a playbook.
-   [ ] Verify approved procedures are displayed.
-   [ ] Verify similar past investigations are displayed.
-   [ ] Verify past investigation insights are displayed.

## Safety Controls

-   [ ] Verify missing-evidence cases block containment.
-   [ ] Verify conflicting-evidence cases block containment.
-   [ ] Verify HIGH-risk containment requires human confirmation.
-   [ ] Verify MEDIUM-risk actions require appropriate review.
-   [ ] Verify LOW-risk cases remain monitoring-oriented.
-   [ ] Verify override reason is mandatory.
-   [ ] Verify evidence and decisions are recorded.

## Testing

-   [ ] Run `python src/edge_case_tests.py`.
-   [ ] Confirm all six edge cases pass.
-   [ ] Run `python src/performance_test.py`.
-   [ ] Review `data/processed/performance_results.csv`.
-   [ ] Run the baseline-versus-MVP evaluation.
-   [ ] Review `data/processed/evaluation_results.csv`.

## Usability

-   [ ] Conduct usability walkthrough with an actual analyst or
    stakeholder.
-   [ ] Collect ratings using the dashboard usability form.
-   [ ] Review `data/processed/usability_feedback.csv`.
-   [ ] Record improvement suggestions.

## Deployment / Rollback

-   [ ] Keep the legacy workflow available during migration.
-   [ ] Verify migration output before changing operational workflow.
-   [ ] Verify rollback procedure before production adoption.
-   [ ] Define an owner for deployment approval.
-   [ ] Define an owner for incident rollback.

## Security and Operations

-   [ ] Do not commit secrets or API keys.
-   [ ] Review repository access permissions.
-   [ ] Protect investigation records from unauthorized modification.
-   [ ] Define log retention and backup policy.
-   [ ] Monitor application errors after deployment.
