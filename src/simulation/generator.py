"""
Synthetic hospital access log generator.
Generates normal baseline access events for the simulation.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
import random
from typing import List

import pandas as pd

from src.simulation.schema import AccessEvent


ROLES = ["Doctor", "Nurse", "Admin", "Technician"]
DEPARTMENTS = ["Cardiology", "Oncology", "Emergency", "Radiology", "Pediatrics"]
ACTIONS = ["view", "edit", "update"]
LOCATIONS = ["Terminal-A", "Terminal-B", "Terminal-C", "Nurse-Station-1", "ER-Desk-2"]


def generate_timestamp(base_time: datetime, offset_minutes: int) -> str:
    """Return ISO-like timestamp string shifted by offset minutes."""
    event_time = base_time + timedelta(minutes=offset_minutes)
    return event_time.strftime("%Y-%m-%d %H:%M:%S")


def generate_access_events(num_events: int, seed: int = 42) -> List[AccessEvent]:
    """
    Generate a list of normal synthetic hospital access events.
    """
    random.seed(seed)

    base_time = datetime(2025, 1, 15, 8, 0, 0)
    events: List[AccessEvent] = []

    for event_id in range(1, num_events + 1):
        role = random.choice(ROLES)
        department = random.choice(DEPARTMENTS)
        action = random.choice(ACTIONS)
        location = random.choice(LOCATIONS)

        user_id = f"U{random.randint(1000, 1999)}"
        patient_id = f"P{random.randint(10000, 19999)}"
        timestamp = generate_timestamp(base_time, event_id)

        event = AccessEvent(
            event_id=event_id,
            timestamp=timestamp,
            user_id=user_id,
            role=role,
            department=department,
            patient_id=patient_id,
            action=action,
            access_location=location,
        )
        events.append(event)

    return events


def events_to_dataframe(events: List[AccessEvent]) -> pd.DataFrame:
    """Convert AccessEvent objects to a pandas DataFrame."""
    return pd.DataFrame([asdict(event) for event in events])


def save_events_csv(events: List[AccessEvent], output_path: str) -> None:
    """Save generated events to CSV."""
    df = events_to_dataframe(events)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    events = generate_access_events(num_events=100)
    df = events_to_dataframe(events)
    print(df.head())