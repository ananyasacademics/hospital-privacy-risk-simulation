"""Tests for baseline comparison."""

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.anomaly_injector import inject_anomalies
from src.evaluation.baseline import random_baseline_metrics


def test_random_baseline_metrics_keys_present():
    events = generate_access_events(num_events=20, seed=42)
    events = inject_anomalies(events, anomaly_count=4, seed=42)
    df = events_to_dataframe(events)

    metrics = random_baseline_metrics(df, positive_rate=0.2)

    assert "tp" in metrics
    assert "tn" in metrics
    assert "fp" in metrics
    assert "fn" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert "false_positive_rate" in metrics