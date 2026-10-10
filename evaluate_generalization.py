import pandas as pd

from src.generate_data import generate_test_data
from src.anomaly_detector import (
    detect_anomalies,
    apply_hybrid_detection,
    evaluate_detector,
)


def main():
    rows = []

    for seed in range(100, 105):
        data = generate_test_data(random_state=seed)

        ml_results, _ = detect_anomalies(data)
        ml_metrics = evaluate_detector(ml_results)

        hybrid_results = apply_hybrid_detection(ml_results)
        hybrid_for_eval = hybrid_results.copy()

        # Evaluate hybrid predictions using a temporary column.
        hybrid_for_eval["ml_anomaly"] = hybrid_for_eval["hybrid_anomaly"]

        hybrid_metrics = evaluate_detector(
            hybrid_results,
            prediction_column="hybrid_anomaly",
        )

        for method, metrics in [
            ("Isolation Forest", ml_metrics),
            ("Hybrid", hybrid_metrics),
        ]:
            rows.append({
                "seed": seed,
                "method": method,
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "false_positives": metrics["false_positives"],
                "false_negatives": metrics["false_negatives"],
            })

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))

    print("\nMean metrics across five fresh datasets:")
    print(
        results.groupby("method")[
            ["precision", "recall", "f1_score"]
        ].mean().round(3)
    )

    results.to_csv(
        "reports/generalization_results.csv",
        index=False,
    )
    print("\nSaved reports/generalization_results.csv")


if __name__ == "__main__":
    main()