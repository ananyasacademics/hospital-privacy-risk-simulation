"""
Rule engine execution logic.
"""

from __future__ import annotations

import pandas as pd

from src.detection.rules import (
    apply_r1_excessive_access_frequency,
    apply_r2_after_hours_activity,
    apply_r3_cross_department_access,
    apply_r4_role_action_mismatch,
)


def run_rule_engine(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all detection rules and add detection columns.
    """
    result = df.copy()

    result["rule_r1"] = apply_r1_excessive_access_frequency(result)
    result["rule_r2"] = apply_r2_after_hours_activity(result)
    result["rule_r3"] = apply_r3_cross_department_access(result)
    result["rule_r4"] = apply_r4_role_action_mismatch(result)

    result["predicted_anomaly"] = (
        result["rule_r1"] |
        result["rule_r2"] |
        result["rule_r3"] |
        result["rule_r4"]
    )

    return result