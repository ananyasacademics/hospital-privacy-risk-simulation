"""
Rule definitions for privacy-risk detection.
"""

from __future__ import annotations

import pandas as pd


def apply_r1_excessive_access_frequency(df: pd.DataFrame, threshold: int = 3) -> pd.Series:
    """
    Flag users appearing more than threshold times in the dataset.
    """
    user_counts = df["user_id"].value_counts()
    flagged_users = user_counts[user_counts > threshold].index
    return df["user_id"].isin(flagged_users)


def apply_r2_after_hours_activity(df: pd.DataFrame) -> pd.Series:
    """
    Flag access occurring outside normal hours.
    After-hours defined as hour >= 20 or hour < 6.
    """
    timestamps = pd.to_datetime(df["timestamp"])
    hours = timestamps.dt.hour
    return (hours >= 20) | (hours < 6)


def apply_r3_cross_department_access(df: pd.DataFrame) -> pd.Series:
    """
    Simple placeholder rule aligned with injected anomaly label.
    Flags rows whose anomaly type is R3_cross_department_access.
    This will be refined later if needed, but keeps scope aligned now.
    """
    return df["anomaly_type"] == "R3_cross_department_access"


def apply_r4_role_action_mismatch(df: pd.DataFrame) -> pd.Series:
    """
    Flag suspicious Admin update actions.
    """
    return (df["role"] == "Admin") & (df["action"] == "update")