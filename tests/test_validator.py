"""Tests for the validation layer."""

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.validator import validate_access_log


def test_validate_access_log_success():
    events = generate_access_events(num_events=10, seed=42)
    df = events_to_dataframe(events)

    result = validate_access_log(df)

    assert result["is_valid"] is True
    assert result["row_count"] == 10
    assert result["column_count"] == 8
    assert result["errors"] == []