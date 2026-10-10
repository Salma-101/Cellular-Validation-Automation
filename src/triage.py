import pandas as pd


def classify_failure(row):
    """Classify a cellular test result using transparent diagnostic rules."""

    error_log = str(row.get("error_log", "")).upper()

    if "TIMEOUT" in error_log:
        return pd.Series({
            "failure_category": "CONNECTION_TIMEOUT",
            "severity": "HIGH",
            "likely_cause": "Connection establishment or protocol response delay",
            "recommended_action": "Inspect connection and protocol logs",
        })

    if "THROUGHPUT_DEGRADATION" in error_log:
        return pd.Series({
            "failure_category": "THROUGHPUT_DEGRADATION",
            "severity": "HIGH",
            "likely_cause": "Reduced data throughput",
            "recommended_action": "Investigate signal quality and network conditions",
        })

    if "LATENCY_SPIKE" in error_log:
        return pd.Series({
            "failure_category": "LATENCY_SPIKE",
            "severity": "MEDIUM",
            "likely_cause": "Unusually high response latency",
            "recommended_action": "Inspect latency measurements and connection stability",
        })

    if "LOW_SIGNAL_QUALITY" in error_log:
        return pd.Series({
            "failure_category": "LOW_SIGNAL_QUALITY",
            "severity": "HIGH",
            "likely_cause": "Low measured signal quality",
            "recommended_action": "Review signal measurements and test conditions",
        })

    # Fallback rules for failures without recognized error logs
    if row.get("status") == "FAIL":
        if row.get("throughput_mbps", float("inf")) < 10:
            category = "THROUGHPUT_DEGRADATION"
            cause = "Low measured throughput"
            action = "Investigate throughput and network conditions"
        elif row.get("latency_ms", 0) > 100:
            category = "LATENCY_SPIKE"
            cause = "High measured latency"
            action = "Inspect latency measurements and connection stability"
        elif row.get("sinr_db", float("inf")) < 5:
            category = "LOW_SIGNAL_QUALITY"
            cause = "Low measured SINR"
            action = "Review signal measurements and test conditions"
        else:
            category = "UNCLASSIFIED_FAILURE"
            cause = "Failure detected but evidence is insufficient"
            action = "Inspect the full test log and configuration"

        return pd.Series({
            "failure_category": category,
            "severity": "HIGH" if category != "UNCLASSIFIED_FAILURE" else "MEDIUM",
            "likely_cause": cause,
            "recommended_action": action,
        })

    return pd.Series({
        "failure_category": "NONE",
        "severity": "NONE",
        "likely_cause": "No failure reported",
        "recommended_action": "No action required",
    })


def triage_tests(data):
    """Enrich test records with diagnostic classifications."""

    result = data.copy()

    diagnostics = result.apply(classify_failure, axis=1)
    result = pd.concat([result, diagnostics], axis=1)

    return result