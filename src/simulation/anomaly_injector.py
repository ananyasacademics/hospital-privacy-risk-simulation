"""
Controlled anomaly injection for hospital privacy risk simulation.
"""

from __future__ import annotations

from dataclasses import replace
import random
from typing import List

from src.simulation.schema import AccessEvent


ANOMALY_TYPES = [
    "R1_excessive_access_frequency",
    "R2_after_hours_activity",
    "R3_cross_department_access",
    "R4_role_action_mismatch",
]


def inject_anomalies(
    events: List[AccessEvent],
    anomaly_count: int,
    seed: int = 42,
) -> List[AccessEvent]:
    """
    Inject labeled anomalies into a copy of the event list.
    """
    random.seed(seed)

    if anomaly_count > len(events):
        raise ValueError("anomaly_count cannot exceed number of events")

    selected_indices = random.sample(range(len(events)), anomaly_count)
    updated_events = events.copy()

    for i, idx in enumerate(selected_indices):
        anomaly_type = ANOMALY_TYPES[i % len(ANOMALY_TYPES)]
        original = updated_events[idx]

        if anomaly_type == "R1_excessive_access_frequency":
            updated = replace(
                original,
                user_id="U1999",
                is_anomaly=True,
                anomaly_type=anomaly_type,
            )
        elif anomaly_type == "R2_after_hours_activity":
            updated = replace(
                original,
                timestamp=original.timestamp[:11] + "23:45:00",
                is_anomaly=True,
                anomaly_type=anomaly_type,
            )
        elif anomaly_type == "R3_cross_department_access":
            updated = replace(
                original,
                department="Radiology" if original.department != "Radiology" else "Oncology",
                is_anomaly=True,
                anomaly_type=anomaly_type,
            )
        else:  # R4_role_action_mismatch
            updated = replace(
                original,
                role="Admin",
                action="update",
                is_anomaly=True,
                anomaly_type=anomaly_type,
            )

        updated_events[idx] = updated

    return updated_events