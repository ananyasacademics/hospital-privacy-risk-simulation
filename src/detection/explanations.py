"""
Human-readable explanation output for flagged events.
"""

from __future__ import annotations

import pandas as pd


def build_rule_explanations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a plain-English explanation column based on triggered rules.
    """
    result = df.copy()
    explanations = []

    for _, row in result.iterrows():
        reasons = []
        if row.get("rule_r1", False):
            reasons.append("R1: unusually frequent access by same user")
        if row.get("rule_r2", False):
            reasons.append("R2: access during after-hours period")
        if row.get("rule_r3", False):
            reasons.append("R3: cross-department access pattern")
        if row.get("rule_r4", False):
            reasons.append("R4: role-action mismatch pattern")

        explanations.append("; ".join(reasons) if reasons else "No rule triggered")

    result["rule_explanation"] = explanations
    return result