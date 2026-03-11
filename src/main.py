"""
Main entry point for Hospital Privacy Risk Simulation.
"""

from src.simulation.anomaly_injector import inject_anomalies
from src.simulation.generator import (
    events_to_dataframe,
    generate_access_events,
)
from src.simulation.validator import validate_access_log
from src.detection.detector import run_rule_engine
from src.detection.explanations import build_rule_explanations
from src.evaluation.metrics import compute_metrics


def main() -> None:
    output_path = "data/generated/report_run/sample_events.csv"

    events = generate_access_events(num_events=100, seed=42)
    events = inject_anomalies(events, anomaly_count=10, seed=42)

    df = events_to_dataframe(events)

    validation_result = validate_access_log(df)
    print("Validation result:", validation_result)

    if not validation_result["is_valid"]:
        raise ValueError("Generated access log failed validation.")

    anomaly_total = int(df["is_anomaly"].sum())
    print("Injected anomalies:", anomaly_total)

    detected_df = run_rule_engine(df)
    detected_df = build_rule_explanations(detected_df)

    predicted_total = int(detected_df["predicted_anomaly"].sum())
    print("Predicted anomalies:", predicted_total)

    metrics = compute_metrics(detected_df)
    print("Metrics:", metrics)

    detected_df.to_csv(output_path, index=False)
    print(f"Saved {len(detected_df)} events to {output_path}")


if __name__ == "__main__":
    main()