# SOC Investigation Playbook Assistant --- 70% Phase Review

## 1. Project Objective

The MVP helps junior SOC analysts follow organization-specific
investigation procedures, collect evidence, understand recommendation
rules, and keep human control over high-impact containment decisions.

## 2. Current Implementation

The current prototype contains:

-   Synthetic SOC dataset generation and cleaning.
-   Exploratory data analysis.
-   Rule-based investigation playbook generation.
-   Evidence recording.
-   Human confirmation for high-impact actions.
-   Mandatory override reasons.
-   Approved SOC procedure retrieval.
-   Similar past investigation retrieval.
-   Past investigation lessons.
-   Investigation history.
-   Legacy workflow coexistence.
-   Migration and rollback scripts.
-   Baseline-versus-MVP evaluation.
-   Six edge/failure-state tests.
-   Actual playbook performance testing.
-   Usability validation form.

## 3. Evaluation

The baseline-versus-MVP experiment uses a fixed sample of 30 cases. The
current experiment is a simulated evaluation intended to demonstrate the
measurement framework.

Previously observed run:

  Metric                          Baseline        MVP
  ---------------------------- ----------- ----------
  Investigation Quality             88.87%     97.33%
  Evidence Completeness             88.58%    100.00%
  Procedure Adherence               88.58%    100.00%
  Wrong Decisions                        3          4
  Average Investigation Time     13.87 min   6.93 min

Observed quality improvement was 9.53% and average investigation time
improvement was approximately 50%.

The wrong-decision result should be reported honestly and not hidden.
The experiment is simulated and therefore should not be interpreted as
proof of real-world analyst effectiveness.

## 4. Edge-Case Coverage

The edge-case suite covers:

1.  Missing evidence.
2.  Conflicting evidence.
3.  High risk requiring human confirmation.
4.  Low risk monitoring.
5.  High risk with missing evidence.
6.  High risk with conflicting evidence.

The intended milestone is 6/6 passing after the human-confirmation
compatibility fix.

## 5. Performance

A separate performance test measures actual playbook-generation response
time over 100 cases. This is different from the simulated analyst
investigation-time metric used in the baseline-versus-MVP experiment.

The performance result should be taken from:

`data/processed/performance_results.csv`

## 6. Usability Validation

The Streamlit dashboard now provides a usability feedback form covering:

-   Ease of use.
-   Recommendation clarity.
-   Procedure and past-investigation usefulness.
-   Confidence in following the playbook.
-   Additional comments.

The form stores responses in:

`data/processed/usability_feedback.csv`

At the current stage, the mechanism is implemented but actual
analyst/stakeholder responses still need to be collected.

## 7. Safety and Ethics

The assistant is advisory rather than autonomous. High-impact actions
require human confirmation. Missing or conflicting evidence blocks
containment. Overrides require a reason and are recorded.

The current prototype uses synthetic data and should not be described as
production-ready without security, privacy, access-control, retention,
and operational reviews.

## 8. 70% Milestone Status

### Completed

-   [x] Scenario definition
-   [x] Synthetic baseline dataset
-   [x] Data cleaning
-   [x] EDA
-   [x] Playbook implementation
-   [x] Explainable recommendations
-   [x] Evidence recording
-   [x] Human confirmation
-   [x] Override reason capture
-   [x] Approved procedures
-   [x] Past investigations
-   [x] Failure-state handling
-   [x] Edge-case test framework
-   [x] Baseline/MVP experiment
-   [x] Performance test
-   [x] Usability validation mechanism
-   [x] Ethics note
-   [x] Deployment checklist

### Still Needed for a Stronger Final Milestone

-   [ ] Collect actual stakeholder/analyst usability responses.
-   [ ] Confirm the final 6/6 edge-case test result.
-   [ ] Add final performance numbers to the report.
-   [ ] Add final GitHub repository files.
-   [ ] Conduct final end-to-end walkthrough.
-   [ ] Demonstrate migration and rollback when required.
-   [ ] Prepare final presentation/report evidence.

## 9. Final Limitation Statement

This is an MVP prototype using synthetic data and simulated baseline
evaluation. Results demonstrate the designed workflow and measurement
approach, but they do not establish production-level effectiveness or
safety. Human review remains required for high-impact decisions.
