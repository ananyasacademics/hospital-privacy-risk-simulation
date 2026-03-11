import os
import pandas as pd


def generate_confusion_matrix(metrics):
    data = {
        "Actual Anomaly": [metrics["tp"], metrics["fn"]],
        "Actual Normal": [metrics["fp"], metrics["tn"]],
    }

    df = pd.DataFrame(data, index=["Predicted Anomaly", "Predicted Normal"])
    return df


def generate_metrics_table(metrics):
    table = pd.DataFrame(
        {
            "Metric": [
                "True Positives",
                "False Positives",
                "True Negatives",
                "False Negatives",
                "Precision",
                "Recall",
                "F1 Score",
                "False Positive Rate",
            ],
            "Value": [
                metrics["tp"],
                metrics["fp"],
                metrics["tn"],
                metrics["fn"],
                round(metrics["precision"], 3),
                round(metrics["recall"], 3),
                round(metrics["f1"], 3),
                round(metrics["false_positive_rate"], 3),
            ],
        }
    )

    return table


def save_tables(confusion_df, metrics_df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    confusion_path = os.path.join(output_dir, "confusion_matrix.csv")
    metrics_path = os.path.join(output_dir, "metrics_summary.csv")

    confusion_df.to_csv(confusion_path)
    metrics_df.to_csv(metrics_path)

    print("Saved tables:")
    print(confusion_path)
    print(metrics_path)
