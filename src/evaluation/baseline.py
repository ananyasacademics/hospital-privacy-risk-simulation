"""
Simple baseline comparison methods.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


def random_baseline_metrics(df: pd.DataFrame, positive_rate: float = 0.1) -> Dict[str, float]:
    """
    Simple deterministic baseline for comparison.

    It predicts the first N rows as anomalies based on a fixed positive rate.
    This is intentionally simple and is only used as a lightweight comparison
    against the rule-based system.
    """
    baseline_df = df.copy()

    n = len(baseline_df)
    predicted_positive_count = max(1, int(n * positive_rate))

    baseline_df["baseline_predicted"] = False
    baseline_df.loc[:predicted_positive_count - 1, "baseline_predicted"] = True

    actual = baseline_df["is_anomaly"].astype(bool)
    predicted = baseline_df["baseline_predicted"].astype(bool)

    tp = int((actual & predicted).sum())
    tn = int((~actual & ~predicted).sum())
    fp = int((~actual & predicted).sum())
    fn = int((actual & ~predicted).sum())

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": false_positive_rate,
    }