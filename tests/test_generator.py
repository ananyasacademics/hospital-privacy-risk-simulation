"""Tests for the synthetic access log generator."""

from src.simulation.generator import generate_access_events, events_to_dataframe


def test_generate_access_events_count():
    events = generate_access_events(num_events=10, seed=42)
    assert len(events) == 10


def test_events_to_dataframe_shape():
    events = generate_access_events(num_events=5, seed=42)
    df = events_to_dataframe(events)

    assert df.shape[0] == 5
    assert "event_id" in df.columns
    assert "timestamp" in df.columns
    assert "user_id" in df.columns
    assert "role" in df.columns
    assert "department" in df.columns
    assert "patient_id" in df.columns
    assert "action" in df.columns
    assert "access_location" in df.columns