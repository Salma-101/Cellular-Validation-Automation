import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


FEATURES = ["sinr_db", "throughput_mbps", "latency_ms"]


def detect_anomalies(data, contamination=0.10, random_state=42):
    """Detect unusual KPI combinations without using failure labels."""

    result = data.copy()

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state,
    )

    # Fit and predict using numeric KPI measurements only
    predictions = model.fit_predict(result[FEATURES])

    result["anomaly_score"] = model.decision_function(result[FEATURES])
    result["ml_anomaly"] = predictions == -1

    return result, model


def evaluate_detector(results):
    """Evaluate predictions against known injected anomalies."""

    y_true = results["is_injected_anomaly"].astype(bool)
    y_pred = results["ml_anomaly"].astype(bool)

    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[False, True]
    ).ravel()

    return {
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "f1_score": round(f1_score(y_true, y_pred, zero_division=0), 3),
    }