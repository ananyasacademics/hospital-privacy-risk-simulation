"""
Main entry point for Hospital Privacy Risk Simulation.

Pipeline steps:
1. Generate synthetic hospital access events
2. Inject controlled anomalies
3. Convert events to DataFrame
4. Validate dataset
5. Save dataset to CSV
"""

from src.simulation.generator import (
    generate_access_events,
    events_to_dataframe,
    save_events_csv,
)

from src.simulation.anomaly_injector import inject_anomalies
from src.simulation.validator import validate_access_log


def main() -> None:
    """Run the synthetic data pipeline."""

    output_path = "data/generated/report_run/sample_events.csv"

    # Step 1 — generate baseline events
    events = generate_access_events(num_events=100, seed=42)

    # Step 2 — inject anomalies
    events = inject_anomalies(events, anomaly_count=10, seed=42)

    # Step 3 — convert to DataFrame
    df = events_to_dataframe(events)

    # Step 4 — validate dataset
    validation_result = validate_access_log(df)
    print("Validation result:", validation_result)

    # Step 5 — report anomaly count
    anomaly_total = int(df["is_anomaly"].sum())
    print("Injected anomalies:", anomaly_total)

    # Stop pipeline if validation fails
    if not validation_result["is_valid"]:
        raise ValueError("Generated access log failed validation.")

    # Step 6 — export CSV
    save_events_csv(events, output_path)

    print(f"Saved {len(events)} events to {output_path}")


if __name__ == "__main__":
    main()