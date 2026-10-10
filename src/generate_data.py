import numpy as np
import pandas as pd
from pathlib import Path


def generate_test_data(n_samples=200, random_state=42):
    """Generate reproducible synthetic cellular validation results."""

    rng = np.random.default_rng(random_state)

    # Simulated baseline measurements, not real RF measurements
    data = pd.DataFrame({
        "test_id": [f"TC-{i:04d}" for i in range(1, n_samples + 1)],
        "sinr_db": rng.normal(18, 4, n_samples).clip(-5, 35),
        "throughput_mbps": rng.normal(85, 15, n_samples).clip(1, 150),
        "latency_ms": rng.normal(35, 8, n_samples).clip(5, 200),
        "error_log": [""] * n_samples,
        "status": ["PASS"] * n_samples,
        "is_injected_anomaly": [False] * n_samples,
    })

    # Inject known abnormal measurements into 10% of the records
    anomaly_count = max(1, n_samples // 10)
    anomaly_indices = rng.choice(
        n_samples, size=anomaly_count, replace=False
    )

    for idx in anomaly_indices:
        data.loc[idx, "is_injected_anomaly"] = True

        # Alternate between different synthetic failure patterns
        if idx % 3 == 0:
            data.loc[idx, "throughput_mbps"] = rng.uniform(1, 8)
            data.loc[idx, "error_log"] = "THROUGHPUT_DEGRADATION"
        elif idx % 3 == 1:
            data.loc[idx, "latency_ms"] = rng.uniform(150, 250)
            data.loc[idx, "error_log"] = "LATENCY_SPIKE"
        else:
            data.loc[idx, "sinr_db"] = rng.uniform(-5, 2)
            data.loc[idx, "error_log"] = "LOW_SIGNAL_QUALITY"

        data.loc[idx, "status"] = "FAIL"

    return data


if __name__ == "__main__":
    output_path = Path("data/synthetic_cellular_tests.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_test_data()
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} test records.")
    print(f"Injected anomalies: {df['is_injected_anomaly'].sum()}")
    print(f"Failed tests: {(df['status'] == 'FAIL').sum()}")
    print(f"Saved to: {output_path}")