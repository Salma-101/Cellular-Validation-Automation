import pandas as pd

from src.generate_data import generate_test_data
from src.triage import triage_tests
from src.anomaly_detector import detect_anomalies
from src.report import generate_report
from src.anomaly_detector import apply_hybrid_detection

def test_generator_creates_reproducible_data():
    first = generate_test_data()
    second = generate_test_data()

    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 200
    assert first["is_injected_anomaly"].sum() == 20


def test_triage_classifies_failures():
    data = generate_test_data()
    results = triage_tests(data)

    assert len(results) == len(data)
    assert "failure_category" in results.columns
    assert (results.loc[
        results["status"] == "FAIL", "failure_category"
    ] != "NONE").all()


def test_detector_returns_predictions():
    data = generate_test_data()
    results, _ = detect_anomalies(data)

    assert "ml_anomaly" in results.columns
    assert results["ml_anomaly"].dtype == bool
    assert results["ml_anomaly"].sum() > 0


def test_report_files_are_created(tmp_path):
    data = generate_test_data()
    results = triage_tests(data)
    results, _ = detect_anomalies(results)

    csv_path, summary_path = generate_report(results, tmp_path)

    assert csv_path.exists()
    assert summary_path.exists()

    exported = pd.read_csv(csv_path)
    assert len(exported) == 200

    summary = summary_path.read_text(encoding="utf-8")
    assert "CELLULAR VALIDATION SUMMARY" in summary

def test_hybrid_detection_preserves_ml_predictions():
    data = generate_test_data()
    results, _ = detect_anomalies(data)

    hybrid = apply_hybrid_detection(results)

    # Original predictions must remain unchanged.
    assert hybrid["ml_anomaly"].equals(results["ml_anomaly"])

    # Hybrid detection must not miss an anomaly already found by ML.
    assert (
        hybrid.loc[results["ml_anomaly"], "hybrid_anomaly"]
    ).all()


def test_hybrid_rule_flags_low_sinr():
    data = pd.DataFrame({
        "sinr_db": [1.0, 10.0],
        "ml_anomaly": [False, False],
    })

    results = apply_hybrid_detection(data, sinr_threshold_db=2.0)

    assert results["hybrid_anomaly"].tolist() == [True, False]
    assert results["ml_anomaly"].tolist() == [False, False]