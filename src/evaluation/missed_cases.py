"""
False positive and false negative example extraction.
"""

from __future__ import annotations

import pandas as pd


def extract_missed_cases(df: pd.DataFrame, limit: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return small false-positive and false-negative tables.
    """
    false_positives = df[(df["is_anomaly"] == False) & (df["predicted_anomaly"] == True)].copy()
    false_negatives = df[(df["is_anomaly"] == True) & (df["predicted_anomaly"] == False)].copy()

    fp_cols = [
        "event_id",
        "timestamp",
        "user_id",
        "role",
        "department",
        "action",
        "rule_explanation",
    ]

    fn_cols = [
        "event_id",
        "timestamp",
        "user_id",
        "role",
        "department",
        "action",
        "anomaly_type",
    ]

    return false_positives[fp_cols].head(limit), false_negatives[fn_cols].head(limit)