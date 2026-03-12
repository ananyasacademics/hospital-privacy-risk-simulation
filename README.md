## Science Day Artifacts

Key experiment outputs used for the science fair board are available in the `science_day_artifacts` folder, including:

- confusion matrix
- detection metrics
- baseline comparison
- example false positives
- example false negatives
- judge summary

# Hospital Privacy Risk Simulation

Rule-based hospital privacy risk simulation developed for Regional Science Day (SOFT category).

This project implements a reproducible software system that generates synthetic hospital access logs and evaluates rule-based detection of suspicious privacy-risk events. The system simulates electronic health record access activity, injects controlled anomalies, applies detection rules, and evaluates detection performance using standard classification metrics.

Because real hospital audit logs contain protected health information, the project uses fully synthetic data to safely study privacy-risk detection behavior.

---

## Project Overview

Hospitals generate large volumes of electronic access logs as staff interact with patient records. Unusual access patterns may indicate potential privacy risks such as unauthorized viewing, excessive record access, or activity outside expected workflows.

This project builds a reproducible simulation pipeline that:

1. Generates synthetic hospital access log events  
2. Validates the generated data structure  
3. Injects controlled anomalies for evaluation  
4. Applies rule-based detection methods  
5. Measures detection performance using standard metrics  

---

## Detection Rules

The rule-based detection engine evaluates events using four privacy-risk rules:

- **R1 — Excessive Access Frequency**
- **R2 — After-Hours Activity**
- **R3 — Cross-Department Access**
- **R4 — Role–Action Mismatch**

These rules are designed to identify suspicious access behavior in a transparent and explainable way.

---

## System Components

The implemented system includes:

- Synthetic hospital access log generator  
- Validation layer for generated events  
- Controlled anomaly injection engine  
- Rule-based detection engine  
- Evaluation and metrics pipeline  
- Sensitivity experiment framework  
- Reproducibility artifacts and experiment logs  

---

## Baseline Experiment

The baseline experiment was executed using a synthetic dataset containing:

- **Total events:** 10,000  
- **Injected anomalies:** 500  

### Confusion Matrix

|                     | Actual Anomaly | Actual Normal |
|---------------------|---------------|---------------|
| Predicted Anomaly   | 399 (True Positive) | 1952 (False Positive) |
| Predicted Normal    | 101 (False Negative) | 7548 (True Negative) |

### Detection Metrics

| Metric | Value |
|------|------|
| Precision | 0.17 |
| Recall | 0.80 |
| F1 Score | 0.28 |
| False Positive Rate | 0.205 |

**Key Result:**  
The system detected **399 of 500 injected anomalies**, achieving **80% recall** in the baseline experiment.

---

## Sensitivity Analysis

To evaluate how detection performance changes under different conditions, the simulator was executed with varying anomaly prevalence levels.

Anomaly prevalence tested:

- **5% anomalies** — baseline experiment  
- **2% anomalies** — reduced anomaly frequency  
- **1% anomalies** — rare anomaly scenario  

Detection performance remained relatively consistent as anomaly prevalence decreased from **5% to 1%**, suggesting that the rule-based detection approach behaves consistently even when suspicious events are rare.

---

## Synthetic Dataset

The simulator generates structured hospital access log events representing interactions between healthcare staff and patient records.

Each event includes fields such as:

- event_id  
- user_id  
- role  
- department  
- patient_id  
- action  
- timestamp  
- anomaly_type  

The dataset is fully synthetic and designed to mimic realistic hospital access patterns without using real patient data.

---

## Reproducibility

This project was designed so that experiments can be repeated and verified.

Reproducibility artifacts include:

- Random seed: **42**  
- Run manifest  
- Dataset hash verification  
- Execution logs  
- Experiment summaries  

These artifacts help ensure consistent experiment execution and verifiable results.

---

## Error Analysis

Example missed-case patterns include:

- **False Positive:** administrator updating multiple records during legitimate maintenance  
- **False Positive:** authorized after-hours access in a 24/7 hospital environment  
- **False Negative:** slow browsing behavior that remains below rule thresholds  

These cases illustrate the trade-off between detecting suspicious patterns and minimizing unnecessary alerts.

---

## Limitations

- The dataset is synthetic and approximates real hospital workflows.  
- Rule-based detection relies on fixed thresholds and may generate false positives.  
- Contextual information such as staff schedules or patient assignments is not modeled.  
- The system is a research prototype and not intended for operational hospital deployment.

---

## Repository Structure

Example structure of the repository:

Key outputs include:

- confusion_matrix.csv  
- metrics_summary.csv  
- baseline_comparison.csv  
- false_positive_examples.csv  
- false_negative_examples.csv  
- judge_summary.txt  

---

## Future Work

Possible future extensions include:

- modeling hospital shift schedules and contextual access patterns  
- incorporating behavioral baselines for user activity  
- comparing rule-based detection with machine learning methods  

---

## Author

**Ananya Desai**  
William Mason High School  
Regional Science Day – SOFT Category