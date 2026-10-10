# Cellular Validation & Intelligent Test Automation

A Python-based prototype for automated cellular test-result analysis, failure triage, and ML-driven anomaly detection. The project simulates cellular performance measurements to explore how automation and machine learning can assist engineering validation workflows.

> **Note:** This project uses synthetic data and simulated failure scenarios. It has not been validated against real cellular hardware, modem logs, or RF test equipment.

## Overview

Analyzing large volumes of engineering test results manually can be time-consuming. This project combines rule-based diagnostics with unsupervised anomaly detection to identify failed tests, flag unusual performance measurements, and generate consolidated reports.

### Key Features

- **Synthetic Test Data Generation:** Generates reproducible test records containing signal quality (SINR), throughput, latency, test status, and diagnostic logs.
- **Automated Failure Triage:** Categorizes known failure patterns, assigns severity levels, and recommends diagnostic actions using transparent rules.
- **ML-Based Anomaly Detection:** Uses Isolation Forest from scikit-learn to identify unusual KPI measurements without using failure labels during prediction.
- **Hybrid Anomaly Detection:** Combines Isolation Forest predictions with a configurable SINR threshold rule to help identify additional low-signal anomalies.
- **Model Evaluation:** Measures precision, recall, F1 score, and confusion-matrix counts against known injected anomalies.
- **Multi-Seed Evaluation:** Compares Isolation Forest and hybrid detection across five independently generated synthetic datasets.
- **Automated Reporting:** Exports detailed test results to CSV and produces a human-readable summary.
- **Automated Testing:** Uses pytest to validate data generation, triage logic, anomaly detection, hybrid detection, and report generation.
- **CI Integration:** GitHub Actions runs the automated tests on pushes and pull requests.

## Tech Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** scikit-learn, Isolation Forest
- **Testing:** pytest
- **CI/CD:** GitHub Actions
- **Version Control:** Git, GitHub

## Architecture

```text
Synthetic Test Data
        |
        v
Data Processing
        |
        +-------------------------+
        |                         |
        v                         v
Rule-Based Triage         Isolation Forest
        |                 Anomaly Detection
        |                         |
        |                 Hybrid Detection
        |                         |
        +------------+------------+
                     |
                     v
            Consolidated Results
                     |
                     v
           CSV + Summary Reports
                     |
                     v
             Automated Tests
```

## Project Structure

```text
cellular-validation-automation/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   └── synthetic_cellular_tests.csv
├── reports/
│   ├── triage_report.csv
│   ├── summary.txt
│   └── generalization_results.csv
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── triage.py
│   ├── anomaly_detector.py
│   └── report.py
├── tests/
│   └── test_pipeline.py
├── main.py
├── evaluate_generalization.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- Git

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd cellular-validation-automation
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Generate the synthetic dataset

```bash
python -m src.generate_data
```

This generates 200 reproducible test records, including 20 deliberately injected anomalies.

### 5. Run the pipeline

```bash
python main.py
```

The pipeline loads the data, performs rule-based triage, detects KPI anomalies, evaluates the detectors, and generates reports.

### 6. Run automated tests

```bash
python -m pytest -v
```

The test suite covers data generation, triage, anomaly detection, hybrid detection, and report generation.

### 7. Evaluate generalization across synthetic datasets

```bash
python evaluate_generalization.py
```

This compares Isolation Forest and hybrid detection across five generated datasets using random seeds 100–104. Results are saved to `reports/generalization_results.csv`.

## Sample Results

### Initial Synthetic Dataset

On the initial synthetic dataset of 200 records, Isolation Forest produced the following results:

| Metric | Result |
|---|---:|
| Total records | 200 |
| Injected anomalies | 20 |
| True positives | 18 |
| False positives | 2 |
| True negatives | 178 |
| False negatives | 2 |
| Precision | 0.90 |
| Recall | 0.90 |
| F1 score | 0.90 |
| Overall accuracy | 98% |

### Multi-Seed Evaluation

Mean metrics across five independently generated synthetic datasets:

| Metric | Isolation Forest | Hybrid |
|---|---:|---:|
| Mean precision | 0.910 | 0.916 |
| Mean recall | 0.910 | 0.960 |
| Mean F1 score | 0.910 | 0.937 |

The hybrid detector achieved higher mean recall and F1 score in this experiment. Its performance varied across seeds, and it did not outperform Isolation Forest on every dataset.

These results are based exclusively on synthetic data. They do not establish performance on real-world cellular networks or prove that the detector can identify actual RF faults.

## Output Files

### `reports/triage_report.csv`

Contains test measurements, failure categories, severity levels, diagnostic hypotheses, recommended actions, anomaly scores, and ML anomaly predictions. Hybrid predictions are included when generated by the pipeline.

### `reports/summary.txt`

Contains a concise overview of test counts, failed tests, flagged anomalies, and failure-category statistics.

### `reports/generalization_results.csv`

Contains the precision, recall, F1 score, and false-positive and false-negative counts for both detection methods across the five evaluation seeds.

## Design Decisions

- **Rule-based triage and ML are separate:** Explicit diagnostic rules provide interpretable categories, while Isolation Forest identifies unusual KPI combinations.
- **Hybrid detection:** A configurable SINR threshold is combined with ML predictions to investigate whether a simple engineering rule can improve anomaly recall.
- **Reproducibility:** Fixed random seeds make synthetic data generation and model experiments repeatable.
- **Evaluation against known anomalies:** Injected-anomaly labels are retained for evaluation but excluded from the model's input features.
- **Multi-seed evaluation:** Multiple synthetic datasets provide a more informative comparison than a single run, although they do not represent real-world validation.
- **Automated validation:** pytest checks core functionality and report generation.
- **Lightweight implementation:** The pipeline uses a CLI instead of a web dashboard to keep the prototype focused on test automation and ML.

## Limitations and Future Work

### Current Limitations

- All measurements and failure scenarios are synthetic.
- Diagnostic thresholds and recommendations are illustrative, not validated RF engineering criteria.
- The five-seed experiment is limited in size and scope.
- The hybrid detector has not been validated against real cellular measurements or independent real-world datasets.
- The prototype has not been integrated with cellular test equipment or real validation infrastructure.
- The system identifies statistical anomalies and potential failure patterns; it does not independently establish root cause.

### Potential Extensions

- Parse real, appropriately anonymized engineering logs into structured failure categories.
- Evaluate against larger datasets and more varied failure scenarios.
- Investigate false positives and false negatives.
- Add time-series analysis and risk-based test selection.
- Explore test-log classification using NLP.
- Integrate with real test execution systems and reporting workflows.
- Extend CI to include data-quality checks and model-regression tests.

## Motivation

This project explores the application of Python automation, statistical analysis, and machine learning to engineering test validation. It is a learning prototype demonstrating failure triage, anomaly detection, reproducible experimentation, and automated software testing.