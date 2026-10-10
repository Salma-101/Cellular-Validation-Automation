from pathlib import Path
import pandas as pd


def generate_report(results, output_dir="reports"):
    """Export detailed test results and an engineering summary."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    detailed_path = output_path / "triage_report.csv"
    summary_path = output_path / "summary.txt"

    results.to_csv(detailed_path, index=False)

    total = len(results)
    failed = int((results["status"] == "FAIL").sum())
    flagged = int(results["ml_anomaly"].sum())

    categories = results["failure_category"].value_counts()

    lines = [
        "CELLULAR VALIDATION SUMMARY",
        "=" * 30,
        f"Total tests: {total}",
        f"Failed tests: {failed}",
        f"ML anomalies flagged: {flagged}",
        "",
        "Failure categories:",
    ]

    for category, count in categories.items():
        if category != "NONE":
            lines.append(f"- {category}: {count}")

    lines.extend([
        "",
        "Note: Measurements are synthetic.",
        "Anomaly flags indicate unusual KPIs, not confirmed root causes.",
    ])

    summary_path.write_text("\n".join(lines), encoding="utf-8")

    return detailed_path, summary_path