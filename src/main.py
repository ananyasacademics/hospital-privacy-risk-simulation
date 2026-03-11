"""
Main entry point for Hospital Privacy Risk Simulation.
"""

import os

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.validator import validate_access_log
from src.simulation.anomaly_injector import inject_anomalies

from src.detection.detector import run_rule_engine
from src.detection.explanations import build_rule_explanations

from src.evaluation.metrics import compute_metrics

from src.reporting.report_generator import (
    generate_confusion_matrix,
    generate_metrics_table,
    save_tables,
)


def main() -> None:
    # Step 1 — Generate events
    events = generate_access_events(num_events=100, seed=42)
    df = events_to_dataframe(events)

    # Step 2 — Inject anomalies
    events = inject_anomalies(events, anomaly_count=10, seed=42)
    df = events_to_dataframe(events)

    # Step 3 — Validate dataset
    validation_result = validate_access_log(df)
    print("Validation result:", validation_result)

    if not validation_result["is_valid"]:
        raise ValueError("Generated access log failed validation.")

    # Step 4 — Count injected anomalies
    injected_total = int(df["is_anomaly"].sum())
    print("Injected anomalies:", injected_total)

    # Step 5 — Run rule detection
    detected_df = run_rule_engine(df)
    detected_df = build_rule_explanations(detected_df)

    predicted_total = int(detected_df["predicted_anomaly"].sum())
    print("Predicted anomalies:", predicted_total)

    # Step 6 — Compute metrics
    metrics = compute_metrics(detected_df)
    print("Metrics:", metrics)

    # Step 7 — Save dataset
    dataset_output_dir = "data/generated/report_run"
    os.makedirs(dataset_output_dir, exist_ok=True)

    dataset_path = os.path.join(dataset_output_dir, "sample_events.csv")
    detected_df.to_csv(dataset_path, index=False)
    print(f"Saved {len(detected_df)} events to {dataset_path}")

    # Step 8 — Generate reporting tables
    tables_output_dir = "outputs/report_run/tables"
    confusion_df = generate_confusion_matrix(metrics)
    metrics_df = generate_metrics_table(metrics)

    save_tables(confusion_df, metrics_df, tables_output_dir)


if __name__ == "__main__":
    main()