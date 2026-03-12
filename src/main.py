"""
Main entry point for Hospital Privacy Risk Simulation.
"""

import os
import pandas as pd

from src.simulation.generator import generate_access_events, events_to_dataframe
from src.simulation.validator import validate_access_log
from src.simulation.anomaly_injector import inject_anomalies

from src.detection.detector import run_rule_engine
from src.detection.explanations import build_rule_explanations

from src.evaluation.metrics import compute_metrics
from src.evaluation.baseline import random_baseline_metrics
from src.evaluation.missed_cases import extract_missed_cases
from src.evaluation.sensitivity_experiment import run_sensitivity_experiment

from src.reporting.report_generator import (
    generate_confusion_matrix,
    generate_metrics_table,
    save_tables,
)

from src.reporting.reproducibility import (
    generate_run_id,
    compute_file_hash,
    write_run_manifest,
    write_execution_log,
    write_judge_summary,
)

from src.reporting.execution_trace import (
    generate_execution_trace,
    generate_rule_trigger_counts,
    generate_board_summary,
)


def main() -> None:
    # -----------------------------
    # Output paths
    # -----------------------------
    dataset_output_dir = "data/generated/report_run"
    tables_output_dir = "outputs/report_run/tables"
    report_output_dir = "outputs/report_run"
    logs_output_dir = "logs"
    judge_packet_dir = "docs/judge_packet"

    os.makedirs(dataset_output_dir, exist_ok=True)
    os.makedirs(tables_output_dir, exist_ok=True)
    os.makedirs(report_output_dir, exist_ok=True)
    os.makedirs(logs_output_dir, exist_ok=True)
    os.makedirs(judge_packet_dir, exist_ok=True)

    dataset_path = os.path.join(dataset_output_dir, "sample_events.csv")
    fp_output_path = os.path.join(report_output_dir, "false_positive_examples.csv")
    fn_output_path = os.path.join(report_output_dir, "false_negative_examples.csv")
    baseline_output_path = os.path.join(report_output_dir, "baseline_comparison.csv")
    sensitivity_output_path = os.path.join(report_output_dir, "sensitivity_experiment.csv")
    execution_trace_path = os.path.join(report_output_dir, "execution_trace.csv")
    rule_trigger_counts_path = os.path.join(report_output_dir, "rule_trigger_counts.csv")
    board_summary_path = os.path.join(report_output_dir, "board_summary.csv")

    # -----------------------------
    # Step 1 — Generate events
    # -----------------------------
    events = generate_access_events(num_events=100, seed=42)
    events = inject_anomalies(events, anomaly_count=10, seed=42)
    df = events_to_dataframe(events)

    # -----------------------------
    # Step 2 — Validate dataset
    # -----------------------------
    validation_result = validate_access_log(df)
    print("Validation result:", validation_result)

    if not validation_result["is_valid"]:
        raise ValueError("Generated access log failed validation.")

    injected_total = int(df["is_anomaly"].sum())
    print("Injected anomalies:", injected_total)

    # -----------------------------
    # Step 3 — Run rule detection
    # -----------------------------
    detected_df = run_rule_engine(df)
    detected_df = build_rule_explanations(detected_df)

    predicted_total = int(detected_df["predicted_anomaly"].sum())
    print("Predicted anomalies:", predicted_total)

    # -----------------------------
    # Step 4 — Compute rule-engine metrics
    # -----------------------------
    metrics = compute_metrics(detected_df)
    print("Rule engine metrics:", metrics)

    # -----------------------------
    # Step 5 — Compute baseline metrics
    # -----------------------------
    baseline_metrics = random_baseline_metrics(detected_df, positive_rate=0.1)
    print("Baseline metrics:", baseline_metrics)

    baseline_df = pd.DataFrame(
        [
            {
                "method": "rule_engine",
                "tp": metrics["tp"],
                "tn": metrics["tn"],
                "fp": metrics["fp"],
                "fn": metrics["fn"],
                "precision": round(metrics["precision"], 3),
                "recall": round(metrics["recall"], 3),
                "f1": round(metrics["f1"], 3),
                "false_positive_rate": round(metrics["false_positive_rate"], 3),
            },
            {
                "method": "baseline",
                "tp": baseline_metrics["tp"],
                "tn": baseline_metrics["tn"],
                "fp": baseline_metrics["fp"],
                "fn": baseline_metrics["fn"],
                "precision": round(baseline_metrics["precision"], 3),
                "recall": round(baseline_metrics["recall"], 3),
                "f1": round(baseline_metrics["f1"], 3),
                "false_positive_rate": round(baseline_metrics["false_positive_rate"], 3),
            },
        ]
    )
    baseline_df.to_csv(baseline_output_path, index=False)

    # -----------------------------
    # Step 6 — Extract missed cases
    # -----------------------------
    fp_df, fn_df = extract_missed_cases(detected_df, limit=5)
    fp_df.to_csv(fp_output_path, index=False)
    fn_df.to_csv(fn_output_path, index=False)

    # -----------------------------
    # Step 7 — Save full dataset
    # -----------------------------
    detected_df.to_csv(dataset_path, index=False)
    print(f"Saved {len(detected_df)} events to {dataset_path}")

    # -----------------------------
    # Step 8 — Save reporting tables
    # -----------------------------
    confusion_df = generate_confusion_matrix(metrics)
    metrics_df = generate_metrics_table(metrics)
    save_tables(confusion_df, metrics_df, tables_output_dir)

    print(f"Saved baseline comparison to {baseline_output_path}")
    print(f"Saved false positives to {fp_output_path}")
    print(f"Saved false negatives to {fn_output_path}")

    # -----------------------------
    # Step 9 — Sensitivity experiment
    # -----------------------------
    sensitivity_df = run_sensitivity_experiment(
        total_events=1000,
        anomaly_rates=[0.05, 0.02, 0.01],
        seed=42,
    )
    sensitivity_df.to_csv(sensitivity_output_path, index=False)
    print(f"Saved sensitivity experiment to {sensitivity_output_path}")

    # -----------------------------
    # Step 10 — Execution trace artifacts
    # -----------------------------
    execution_trace_df = generate_execution_trace(detected_df, limit=10)
    execution_trace_df.to_csv(execution_trace_path, index=False)

    rule_trigger_counts_df = generate_rule_trigger_counts(detected_df)
    rule_trigger_counts_df.to_csv(rule_trigger_counts_path, index=False)

    board_summary_df = generate_board_summary(metrics, baseline_metrics)
    board_summary_df.to_csv(board_summary_path, index=False)

    print(f"Saved execution trace to {execution_trace_path}")
    print(f"Saved rule trigger counts to {rule_trigger_counts_path}")
    print(f"Saved board summary to {board_summary_path}")

    # -----------------------------
    # Step 11 — Reproducibility artifacts
    # -----------------------------
    run_id = generate_run_id()
    manifest_path = os.path.join(report_output_dir, f"run_manifest_{run_id}.json")
    execution_log_path = os.path.join(logs_output_dir, f"run_{run_id}.log")
    judge_summary_path = os.path.join(report_output_dir, "judge_summary.txt")
    judge_packet_summary_path = os.path.join(judge_packet_dir, "judge_summary.txt")

    dataset_hash = compute_file_hash(dataset_path)

    manifest = {
        "run_id": run_id,
        "seed": 42,
        "dataset_path": dataset_path,
        "dataset_hash": dataset_hash,
        "row_count": len(detected_df),
        "injected_anomalies": injected_total,
        "predicted_anomalies": predicted_total,
        "metrics": metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": {
            "baseline_comparison": baseline_output_path,
            "false_positives": fp_output_path,
            "false_negatives": fn_output_path,
            "sensitivity_experiment": sensitivity_output_path,
            "execution_trace": execution_trace_path,
            "rule_trigger_counts": rule_trigger_counts_path,
            "board_summary": board_summary_path,
            "confusion_matrix": os.path.join(tables_output_dir, "confusion_matrix.csv"),
            "metrics_summary": os.path.join(tables_output_dir, "metrics_summary.csv"),
        },
    }
    write_run_manifest(manifest, manifest_path)

    log_lines = [
        f"run_id: {run_id}",
        f"seed: 42",
        f"dataset_path: {dataset_path}",
        f"dataset_hash: {dataset_hash}",
        f"row_count: {len(detected_df)}",
        f"injected_anomalies: {injected_total}",
        f"predicted_anomalies: {predicted_total}",
        f"metrics: {metrics}",
        f"baseline_metrics: {baseline_metrics}",
    ]
    write_execution_log(log_lines, execution_log_path)

    judge_summary = f"""Hospital Privacy Risk Simulation — Judge Summary

Run ID: {run_id}
Seed: 42
Rows Generated: {len(detected_df)}
Injected Anomalies: {injected_total}
Predicted Anomalies: {predicted_total}

Rule Engine Metrics
TP: {metrics['tp']}
TN: {metrics['tn']}
FP: {metrics['fp']}
FN: {metrics['fn']}
Precision: {round(metrics['precision'], 3)}
Recall: {round(metrics['recall'], 3)}
F1: {round(metrics['f1'], 3)}
False Positive Rate: {round(metrics['false_positive_rate'], 3)}

Baseline F1: {round(baseline_metrics['f1'], 3)}
Dataset Hash: {dataset_hash}
"""
    write_judge_summary(judge_summary, judge_summary_path)
    write_judge_summary(judge_summary, judge_packet_summary_path)

    print(f"Saved run manifest to {manifest_path}")
    print(f"Saved execution log to {execution_log_path}")
    print(f"Saved judge summary to {judge_summary_path}")
    print(f"Saved judge packet summary to {judge_packet_summary_path}")


if __name__ == "__main__":
    main()