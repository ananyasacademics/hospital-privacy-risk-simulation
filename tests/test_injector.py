"""Tests for anomaly injection."""

from src.simulation.generator import generate_access_events
from src.simulation.anomaly_injector import inject_anomalies


def test_inject_anomalies_count():
    events = generate_access_events(num_events=20, seed=42)
    updated_events = inject_anomalies(events, anomaly_count=4, seed=42)

    anomaly_count = sum(event.is_anomaly for event in updated_events)
    assert anomaly_count == 4


def test_inject_anomalies_labels_present():
    events = generate_access_events(num_events=20, seed=42)
    updated_events = inject_anomalies(events, anomaly_count=4, seed=42)

    anomaly_types = [event.anomaly_type for event in updated_events if event.is_anomaly]
    assert len(anomaly_types) == 4
    assert all(a != "none" for a in anomaly_types)