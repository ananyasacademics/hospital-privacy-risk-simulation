"""Main entry point for Hospital Privacy Risk Simulation."""

from src.simulation.generator import (
    events_to_dataframe,
    generate_access_events,
    save_events_csv,
)
from src.simulation.validator import validate_access_log


def main() -> None:
    output_path = "data/generated/report_run/sample_events.csv"

    events = generate_access_events(num_events=100, seed=42)
    df = events_to_dataframe(events)

    validation_result = validate_access_log(df)
    print("Validation result:", validation_result)

    if not validation_result["is_valid"]:
        raise ValueError("Generated access log failed validation.")

    save_events_csv(events, output_path)
    print(f"Saved {len(events)} events to {output_path}")


if __name__ == "__main__":
    main()