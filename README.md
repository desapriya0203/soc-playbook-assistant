# 🛡️ SOC Investigation Playbook Assistant

A rule-based SOC investigation assistant designed to help junior security analysts follow approved investigation procedures, review evidence, learn from past investigations, and make safer containment decisions.

## 🎯 Problem

In a Security Operations Center (SOC), junior analysts may struggle to follow organization-specific investigation procedures consistently.

This can lead to:

- Missing investigation steps
- Incomplete evidence collection
- Inconsistent decisions
- Incorrect containment actions
- Longer investigation time

## 💡 Solution

The SOC Investigation Playbook Assistant provides step-by-step investigation guidance based on:

- Approved SOC procedures
- Current case evidence
- Previous investigation records
- Risk level
- Failure-state conditions

The assistant focuses on explainable recommendations and keeps human analysts responsible for high-impact actions.

## ✨ Key Features

### 1. Investigation Playbook

Provides investigation steps based on the selected SOC case.

### 2. Evidence Guidance

Shows evidence required for investigation and allows analysts to record evidence.

### 3. Approved Procedures

Uses organization-specific approved procedures to guide the investigation.

### 4. Past Investigations

Shows similar previous investigations and lessons learned.

### 5. Explainable Recommendations

Each recommendation is connected to investigation rules and supporting evidence.

### 6. Failure-State Handling

The assistant safely handles:

- Missing evidence
- Conflicting evidence
- High-risk cases
- High-risk cases with missing evidence
- High-risk cases with conflicting evidence

### 7. Human Confirmation

High-impact containment actions require human confirmation.

Examples:

- Endpoint isolation
- Account disablement

The assistant does not automatically execute these actions.

### 8. Override Tracking

Analysts can override recommendations, but an override reason is required for accountability.

### 9. Investigation History

Investigation evidence, confirmations, and overrides can be recorded for later review.

### 10. Usability Validation

The dashboard contains a feedback form for collecting actual analyst or stakeholder feedback.

## 🏗️ Project Structure

```text
soc-playbook-assistant/
│
├── data/
│   ├── raw/
│   │   └── synthetic_soc_cases.csv
│   │
│   └── processed/
│       ├── approved_procedures.csv
│       ├── clean_soc_cases.csv
│       ├── edge_case_results.csv
│       ├── evaluation_results.csv
│       ├── past_investigations.csv
│       └── performance_results.csv
│
├── docs/
│   ├── 70_percent_phase_review.md
│   ├── deployment_checklist.md
│   └── ethics_note.md
│
├── src/
│   ├── app.py
│   ├── clean_data.py
│   ├── edge_case_tests.py
│   ├── eda.py
│   ├── evaluation.py
│   ├── evidence_manager.py
│   ├── generate_dataset.py
│   ├── migration.py
│   ├── past_investigation_loader.py
│   ├── performance_test.py
│   ├── playbook_rules.py
│   ├── procedure_loader.py
│   └── rollback.py
│
├── .gitignore
└── README.md
