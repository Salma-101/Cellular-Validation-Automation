import pandas as pd

from src.triage import triage_tests
from src.anomaly_detector import (
    detect_anomalies,
    evaluate_detector,
    apply_hybrid_detection,
)
from src.report import generate_report


def main():
    input_path = "data/synthetic_cellular_tests.csv"

    print("Loading cellular test data...")
    data = pd.read_csv(input_path)
    print(f"Loaded {len(data)} test records.")

    print("\nRunning failure triage...")
    results = triage_tests(data)

    print("Running Isolation Forest...")
    results, _ = detect_anomalies(results)

    print("\nOriginal ML metrics:")
    ml_metrics = evaluate_detector(results)
    for name, value in ml_metrics.items():
        print(f"{name}: {value}")

    print("\nApplying hybrid detection...")
    results = apply_hybrid_detection(results)

    # Evaluate the hybrid predictions separately.
    hybrid_results = results.rename(
        columns={"hybrid_anomaly": "ml_anomaly"}
    )
    hybrid_metrics = evaluate_detector(
        results,
        prediction_column = "hybrid_anomaly",
    )

    print("\nHybrid detector metrics:")
    for name, value in hybrid_metrics.items():
        print(f"{name}: {value}")

    print("\nGenerating reports...")
    detailed_path, summary_path = generate_report(results)

    print(f"Detailed report: {detailed_path}")
    print(f"Summary report: {summary_path}")
    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()