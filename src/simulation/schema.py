"""
Schema definition for synthetic hospital access logs.
This defines the structure of each access event in the simulation.
"""

from dataclasses import dataclass


@dataclass
class AccessEvent:
    event_id: int
    timestamp: str
    user_id: str
    role: str
    department: str
    patient_id: str
    action: str
    access_location: str
    is_anomaly: bool = False
    anomaly_type: str = "none"