"""Tests for missed-case extraction."""

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.anomaly_injector import inject_anomalies
from src.detection.detector import run_rule_engine
from src.detection.explanations import build_rule_explanations
from src.evaluation.missed_cases import extract_missed_cases


def test_extract_missed_cases_returns_two_tables():
    events = generate_access_events(num_events=20, seed=42)
    events = inject_anomalies(events, anomaly_count=4, seed=42)
    df = events_to_dataframe(events)
    df = run_rule_engine(df)
    df = build_rule_explanations(df)

    fp_df, fn_df = extract_missed_cases(df, limit=3)

    assert fp_df is not None
    assert fn_df is not None