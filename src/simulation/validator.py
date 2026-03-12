"""
Validation layer for synthetic hospital access logs.
Checks schema completeness and basic data quality rules.
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd

REQUIRED_COLUMNS = [
    "event_id",
    "timestamp",
    "user_id",
    "role",
    "department",
    "patient_id",
    "action",
    "access_location",
    "is_anomaly",
    "anomaly_type",
]

VALID_ROLES = {"Doctor", "Nurse", "Admin", "Technician"}
VALID_DEPARTMENTS = {"Cardiology", "Oncology", "Emergency", "Radiology", "Pediatrics"}
VALID_ACTIONS = {"view", "edit", "update"}
VALID_ANOMALY_TYPES = {
    "none",
    "R1_excessive_access_frequency",
    "R2_after_hours_activity",
    "R3_cross_department_access",
    "R4_role_action_mismatch",
}


def validate_access_log(df: pd.DataFrame) -> Dict[str, object]:
    """
    Validate synthetic hospital access log data and return a summary dictionary.
    """
    errors: List[str] = []

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")

    if not missing_columns:
        for col in REQUIRED_COLUMNS:
            if df[col].isnull().any():
                errors.append(f"Null values found in column: {col}")

        invalid_roles = sorted(set(df["role"]) - VALID_ROLES)
        if invalid_roles:
            errors.append(f"Invalid role values: {invalid_roles}")

        invalid_departments = sorted(set(df["department"]) - VALID_DEPARTMENTS)
        if invalid_departments:
            errors.append(f"Invalid department values: {invalid_departments}")

        invalid_actions = sorted(set(df["action"]) - VALID_ACTIONS)
        if invalid_actions:
            errors.append(f"Invalid action values: {invalid_actions}")

        invalid_anomaly_types = sorted(set(df["anomaly_type"]) - VALID_ANOMALY_TYPES)
        if invalid_anomaly_types:
            errors.append(f"Invalid anomaly_type values: {invalid_anomaly_types}")

    return {
        "is_valid": len(errors) == 0,
        "row_count": len(df),
        "column_count": len(df.columns),
        "errors": errors,
    }