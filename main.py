import pandas as pd

from src.triage import triage_tests
from src.anomaly_detector import detect_anomalies, evaluate_detector
from src.report import generate_report


def main():
    input_path = "data/synthetic_cellular_tests.csv"

    print("Loading cellular test data...")
    data = pd.read_csv(input_path)

    print(f"Loaded {len(data)} test records.")

    print("\nRunning failure triage...")
    results = triage_tests(data)

    print("Running ML anomaly detection...")
    results, _ = detect_anomalies(results)

    print("\nEvaluating anomaly detector...")
    metrics = evaluate_detector(results)

    for name, value in metrics.items():
        print(f"{name}: {value}")

    print("\nGenerating reports...")
    detailed_path, summary_path = generate_report(results)

    print(f"Detailed report: {detailed_path}")
    print(f"Summary report: {summary_path}")

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()