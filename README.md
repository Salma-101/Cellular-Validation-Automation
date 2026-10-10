# Cellular Validation & Intelligent Test Automation

A Python-based prototype for automated cellular test-result analysis, failure triage, and ML-driven anomaly detection. The project simulates cellular performance measurements to explore how automation and machine learning can assist engineering validation workflows.

> **Note:** This project uses synthetic data and simulated failure scenarios. It has not been validated against real cellular hardware, modem logs, or RF test equipment.

## Overview

Analyzing large volumes of engineering test results manually can be time-consuming. This project combines rule-based diagnostics with unsupervised anomaly detection to identify failed tests, flag unusual performance measurements, and generate consolidated reports.

### Key Features

- **Synthetic Test Data Generation:** Generates reproducible test records containing signal quality (SINR), throughput, latency, test status, and diagnostic logs.
- **Automated Failure Triage:** Categorizes known failure patterns, assigns severity levels, and recommends diagnostic actions using transparent rules.
- **ML-Based Anomaly Detection:** Uses Isolation Forest from scikit-learn to identify unusual KPI measurements without using failure labels during prediction.
- **Model Evaluation:** Measures precision, recall, F1 score, and confusion-matrix counts against known injected anomalies.
- **Automated Reporting:** Exports detailed test results to CSV and produces a human-readable summary.
- **Automated Testing:** Uses pytest to validate data generation, triage logic, anomaly detection, and report generation.
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
        +---------------------+
        |                     |
        v                     v
Rule-Based Triage      KPI Anomaly Detection
        |                     |
        +----------+----------+
                   |
                   v
          Consolidated Results
                   |
                   v
          CSV + Summary Report
                   |
                   v
         Automated Test Suite
```

## Project Structure

```text
cellular-test-intelligence/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   └── synthetic_cellular_tests.csv
├── reports/
│   ├── triage_report.csv
│   └── summary.txt
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── triage.py
│   ├── anomaly_detector.py
│   └── report.py
├── tests/
│   └── test_pipeline.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- Git (optional, for version control)

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd cellular-test-intelligence
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

The pipeline loads the data, performs rule-based triage, detects KPI anomalies, evaluates the detector, and generates reports.

### 6. Run automated tests

```bash
python -m pytest -v
```

## Sample Results

On the initial synthetic dataset of 200 records, the Isolation Forest detector produced the following results:

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
| Automated tests passed | 4/4 |

These are results from a single controlled synthetic dataset, not a benchmark of real-world cellular performance. The model flags statistical outliers; it does not independently establish the root cause of a failure.

## Output Files

### `reports/triage_report.csv`

Contains the original test measurements, failure categories, severity levels, diagnostic hypotheses, recommended actions, anomaly scores, and ML anomaly predictions.

### `reports/summary.txt`

Contains a concise overview of test counts, failed tests, flagged anomalies, and failure-category statistics.

## Design Decisions

- **Rule-based triage and ML are separate:** Explicit diagnostic rules provide interpretable categories, while Isolation Forest independently identifies unusual KPI combinations.
- **Reproducibility:** A fixed random seed makes synthetic data generation repeatable.
- **Evaluation against known anomalies:** Injected-anomaly labels are retained for evaluation but excluded from the model's input features.
- **Automated validation:** pytest checks core functionality and report generation.
- **Lightweight implementation:** The pipeline uses a CLI instead of a web dashboard to keep the prototype focused on test automation and ML.

## Limitations and Future Work

Current limitations:

- All measurements and failure scenarios are synthetic.
- Diagnostic thresholds and recommendations are illustrative rather than validated engineering criteria.
- The anomaly detector has only been evaluated on the generated dataset.
- The prototype has not been integrated with cellular test equipment or real validation infrastructure.

Potential extensions:

- Parse real, appropriately anonymized engineering logs.
- Evaluate against larger datasets and more varied failure scenarios.
- Investigate false positives and false negatives.
- Add time-series analysis and risk-based test selection.
- Integrate with real test execution systems and reporting workflows.
- Extend CI to include data-quality checks and model-regression tests.

## Motivation

This project explores the application of Python automation, statistical analysis, and machine learning to engineering test validation. It is intended as a learning prototype demonstrating failure triage, anomaly detection, reproducible experimentation, and automated software testing.