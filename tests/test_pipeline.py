import pandas as pd

from src.generate_data import generate_test_data
from src.triage import triage_tests
from src.anomaly_detector import detect_anomalies
from src.report import generate_report


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