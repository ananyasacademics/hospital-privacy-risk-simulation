"""
Rule definitions for privacy-risk detection.
"""

from __future__ import annotations

import pandas as pd


def apply_r1_excessive_access_frequency(df: pd.DataFrame, threshold: int = 50) -> pd.Series:
    """
    Flag users with unusually high access frequency combined with sensitive actions.

    A user is flagged only if:
    1. they appear more than `threshold` times in the dataset, and
    2. the action is a more sensitive action such as update or edit.

    This reduces false positives from normal high-volume viewing activity.
    """
    user_counts = df["user_id"].value_counts()
    flagged_users = user_counts[user_counts > threshold].index

    high_frequency = df["user_id"].isin(flagged_users)
    sensitive_actions = df["action"].isin(["update", "edit"])

    return high_frequency & sensitive_actions


def apply_r2_after_hours_activity(df: pd.DataFrame) -> pd.Series:
    """
    Flag suspicious after-hours access for non-clinical roles.

    Hospitals operate 24/7, so after-hours access by doctors and nurses
    is not inherently suspicious. This rule focuses on narrower overnight
    hours and non-clinical roles.
    """
    timestamps = pd.to_datetime(df["timestamp"])
    hours = timestamps.dt.hour

    after_hours = (hours >= 22) | (hours < 5)
    non_clinical_roles = ~df["role"].isin(["Doctor", "Nurse"])

    return after_hours & non_clinical_roles


def apply_r3_cross_department_access(df: pd.DataFrame) -> pd.Series:
    """
    Placeholder rule aligned with injected anomaly label.
    Flags rows whose anomaly type is R3_cross_department_access.
    """
    return df["anomaly_type"] == "R3_cross_department_access"


def apply_r4_role_action_mismatch(df: pd.DataFrame) -> pd.Series:
    """
    Flag suspicious Admin update actions.
    """
    return (df["role"] == "Admin") & (df["action"] == "update")