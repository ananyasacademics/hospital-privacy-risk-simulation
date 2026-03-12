# Hospital Privacy Risk Simulation
### Rule-Based Detection of Suspicious Electronic Health Record Access

A reproducible simulation framework for detecting suspicious electronic health record (EHR) access using rule-based anomaly detection.

This project generates synthetic hospital access logs, injects controlled anomalies, applies rule-based detection rules, and evaluates detection performance using standard classification metrics.

Developed for **Regional Science Day** in the **SOFT (Software Systems) category**.

---

# Key Result

Baseline experiment:

- **10,000 simulated access events**
- **500 injected anomalies**

Detection results:

| Metric | Value |
|------|------|
| True Positives | 399 |
| False Positives | 1952 |
| True Negatives | 7548 |
| False Negatives | 101 |
| Precision | 0.17 |
| Recall | 0.80 |
| F1 Score | 0.28 |
| False Positive Rate | 0.205 |

The system detected **399 of 500 injected anomalies**, achieving **80% recall** in the baseline experiment.

---

# Science Day Artifacts

Key outputs used in the science fair poster are located in:
science_day_artifacts/


This folder contains:

- confusion_matrix.csv  
- metrics_summary.csv  
- baseline_comparison.csv  
- false_positive_examples.csv  
- false_negative_examples.csv  
- judge_summary.txt  
- board_summary.csv  

These artifacts provide **evidence supporting the results presented on the poster**.

---

# System Pipeline

The system implements a complete simulation and evaluation pipeline:

Synthetic Log Generator
↓
Validation Layer
↓
Anomaly Injection
↓
Rule-Based Detection Engine
↓
Metrics & Evaluation


---

# Detection Rules

The rule-based engine evaluates events using four privacy-risk detection rules:

**R1 — Excessive Access Frequency**  
Flags unusually high numbers of patient record accesses.

**R2 — After-Hours Activity**  
Detects access outside typical hospital operating hours.

**R3 — Cross-Department Access**  
Identifies staff accessing records from unrelated departments.

**R4 — Role–Action Mismatch**  
Flags actions inconsistent with the user's role.

These rules provide **transparent and explainable detection logic**.

---

# Sensitivity Analysis

To evaluate system robustness, the simulator was executed with different anomaly prevalence levels.

Tested anomaly rates:

- **5% anomalies (baseline)**
- **2% anomalies**
- **1% anomalies**

Detection performance remained relatively stable as anomaly prevalence decreased, suggesting that the rule-based approach behaves consistently even when suspicious events are rare.

---

# Synthetic Dataset

Because real hospital audit logs contain protected patient information, this project uses a **fully synthetic dataset**.

Each simulated access event contains fields such as:

- event_id
- user_id
- role
- department
- patient_id
- action
- timestamp
- anomaly_type

The dataset is designed to **approximate realistic hospital access patterns without exposing any real patient data**.

---

# Reproducibility

This project was designed to allow experiments to be reproduced and verified.

Reproducibility artifacts include:

- **Random seed:** 42
- run manifest
- dataset hash
- execution logs
- rule trigger counts
- experiment summaries

These ensure that experiment outputs can be **consistently regenerated**.

---

# How to Run the Simulation

Clone the repository:
git clone https://github.com/ananyasacademics/hospital-privacy-risk-simulation.git


Navigate to the project folder:
cd hospital-privacy-risk-simulation


Run the simulation pipeline:
python src/run_simulation.py


This will:

- generate synthetic hospital access logs
- inject controlled anomalies
- run the rule-based detection engine
- compute evaluation metrics
- produce outputs in the `outputs/` folder

---

# Error Analysis

Example missed-case patterns include:

**False Positive**
- administrator performing legitimate bulk updates

**False Positive**
- authorized after-hours access in a 24/7 hospital environment

**False Negative**
- slow browsing behavior that stays below rule thresholds

These cases illustrate the trade-off between **detecting suspicious activity and minimizing false alerts**.

---

# Limitations

- The dataset is synthetic and approximates real hospital workflows.
- Rule-based detection relies on fixed thresholds.
- Contextual information such as staff schedules or patient assignments is not modeled.
- This system is a research prototype and is not intended for operational deployment.

---

# Repository Structure
configs/ experiment configurations
data/ synthetic dataset generation
docs/ project documentation
logs/ experiment logs
notebooks/ exploratory analysis notebooks
outputs/ experiment outputs
science_day_artifacts/ results used for science fair poster
src/ simulator and detection engine
tests/ validation tests


---

# Future Work

Possible future improvements include:

- modeling hospital staff shift schedules
- incorporating behavioral access baselines
- comparing rule-based detection with machine learning methods

---

# Author

**Ananya Desai**  
William Mason High School  
Regional Science Day Project  
Category: **SOFT**
