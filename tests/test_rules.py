"""Tests for rule-based detection."""

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.anomaly_injector import inject_anomalies
from src.detection.detector import run_rule_engine


def test_rule_engine_adds_prediction_columns():
    events = generate_access_events(num_events=20, seed=42)
    events = inject_anomalies(events, anomaly_count=4, seed=42)
    df = events_to_dataframe(events)

    result = run_rule_engine(df)

    assert "rule_r1" in result.columns
    assert "rule_r2" in result.columns
    assert "rule_r3" in result.columns
    assert "rule_r4" in result.columns
    assert "predicted_anomaly" in result.columns


def test_rule_engine_flags_some_rows():
    events = generate_access_events(num_events=20, seed=42)
    events = inject_anomalies(events, anomaly_count=4, seed=42)
    df = events_to_dataframe(events)

    result = run_rule_engine(df)

    assert result["predicted_anomaly"].sum() >= 1