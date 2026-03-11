"""
Evaluation metrics for detection results.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


def compute_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute confusion-matrix-based metrics from actual vs predicted anomaly labels.
    """
    actual = df["is_anomaly"].astype(bool)
    predicted = df["predicted_anomaly"].astype(bool)

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