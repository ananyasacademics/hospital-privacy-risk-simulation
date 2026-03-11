"""
Sensitivity experiment: evaluate detection performance under different anomaly prevalence levels.
"""

from __future__ import annotations

import pandas as pd

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.anomaly_injector import inject_anomalies
from src.detection.detector import run_rule_engine
from src.detection.explanations import build_rule_explanations
from src.evaluation.metrics import compute_metrics


def run_sensitivity_experiment(
    total_events: int = 1000,
    anomaly_rates: list[float] | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Run experiments for different anomaly prevalence levels.
    Returns a dataframe summarizing the metrics.
    """
    if anomaly_rates is None:
        anomaly_rates = [0.05, 0.02, 0.01]

    results = []

    for rate in anomaly_rates:
        anomaly_count = int(total_events * rate)

        events = generate_access_events(num_events=total_events, seed=seed)
        events = inject_anomalies(events, anomaly_count=anomaly_count, seed=seed)

        df = events_to_dataframe(events)

        df = run_rule_engine(df)
        df = build_rule_explanations(df)

        metrics = compute_metrics(df)

        results.append(
            {
                "anomaly_rate": rate,
                "anomaly_count": anomaly_count,
                "precision": round(metrics["precision"], 3),
                "recall": round(metrics["recall"], 3),
                "f1": round(metrics["f1"], 3),
                "false_positive_rate": round(metrics["false_positive_rate"], 3),
            }
        )

    return pd.DataFrame(results)