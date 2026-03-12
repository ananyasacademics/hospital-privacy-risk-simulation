"""
Execution trace and board export helpers.
"""

from __future__ import annotations

import pandas as pd


def generate_execution_trace(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """
    Create a compact execution trace table showing how events moved through the pipeline.
    """
    cols = [
        "event_id",
        "timestamp",
        "user_id",
        "role",
        "department",
        "action",
        "is_anomaly",
        "anomaly_type",
        "rule_r1",
        "rule_r2",
        "rule_r3",
        "rule_r4",
        "predicted_anomaly",
        "rule_explanation",
    ]

    available_cols = [c for c in cols if c in df.columns]
    return df[available_cols].head(limit).copy()


def generate_rule_trigger_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count how many times each rule triggered.
    """
    counts = {
        "rule": ["R1", "R2", "R3", "R4"],
        "trigger_count": [
            int(df["rule_r1"].sum()) if "rule_r1" in df.columns else 0,
            int(df["rule_r2"].sum()) if "rule_r2" in df.columns else 0,
            int(df["rule_r3"].sum()) if "rule_r3" in df.columns else 0,
            int(df["rule_r4"].sum()) if "rule_r4" in df.columns else 0,
        ],
    }
    return pd.DataFrame(counts)


def generate_board_summary(metrics: dict, baseline_metrics: dict) -> pd.DataFrame:
    """
    Create a compact board summary table.
    """
    return pd.DataFrame(
        [
            {
                "section": "Rule Engine",
                "precision": round(metrics["precision"], 3),
                "recall": round(metrics["recall"], 3),
                "f1": round(metrics["f1"], 3),
                "false_positive_rate": round(metrics["false_positive_rate"], 3),
            },
            {
                "section": "Baseline",
                "precision": round(baseline_metrics["precision"], 3),
                "recall": round(baseline_metrics["recall"], 3),
                "f1": round(baseline_metrics["f1"], 3),
                "false_positive_rate": round(baseline_metrics["false_positive_rate"], 3),
            },
        ]
    )