# Printing Press ML 

A machine learning regression challenge developed for a college technical event, designed to evaluate feature engineering, tabular preprocessing, and regression modeling on simulated industrial telemetry data.

This challenge is hosted on [Online_IDE](https://github.com/aaditya-hamirani07/Online_IDE), a browser-based development environment with integrated code execution and automated grading.

---

## Problem Statement

Given the operating parameters of an industrial printing press session, build a regression model to predict the total production volume (**`amount_printed`**).

- **Task**: Supervised Tabular Regression
- **Target Variable**: `amount_printed` (continuous, non-negative)
- **Evaluation Metric**: Relative Absolute Percentage Error
- **Repositories**:
  - Challenge Core: [Printing_Press_ML](https://github.com/aaditya-hamirani07/Printing_Press_ML)
  - Deployment Platform: [Online_IDE](https://github.com/aaditya-hamirani07/Online_IDE)

---

## Dataset Overview

The dataset consists of 8,500 industrial printing sessions split into public training and private evaluation partitions:

| File | Rows | Columns | Target Column |
|---|---|---|---|
| `data/train.csv` | 7,000 | 17 (ID + 15 features + `amount_printed`) | Included |
| `data/test.csv` | 1,500 | 16 (ID + 15 features) | Withheld |

### Features Summary

The 15 input features capture mechanical, environmental, operational, and material conditions:

- **Numerical Features**: `printing_speed` (prints/min), `machine_age` (years), `operating_hours` (hours), `temperature` (°C), `humidity` (%), `power_stability` (0–100 score), `setup_time` (minutes), `last_calibration_day` (days).
- **Categorical Features**: `paper_type` (Standard, Glossy, Matte, Cardstock), `shift` (Morning, Afternoon, Night), `maintenance_status` (Good, Average, Poor), `machine_type` (Type_A–D), `paper_quality` (Low, Medium, High), `operator_id` (Op01–Op10), `ink_batch_id` (B01–B20).

**Data Characteristics**:
- Sensor features (`temperature`, `humidity`, `power_stability`) contain ~4% to 10% condition-dependent missing values (`NaN`).
- Three features (`last_calibration_day`, `operator_id`, `ink_batch_id`) are noise features with no underlying relationship to the target.

---

## Synthetic Generation & Nonlinear Interactions

The dataset is synthesized using a domain-driven physical simulation ([`generator.py`](generator.py)) incorporating nonlinear constraints and compound interaction effects:

- **Effective Run Time**: Setup time directly reduces active production hours.
- **Speed Efficiency Curve**: Production efficiency peaks in an optimal range (120–150 prints/min) and degrades at extreme speeds due to mechanical vibration and paper handling faults.
- **Compound Interactions**:
  - High speed combined with high humidity creates additional moisture resistance.
  - High speed paired with low paper quality increases print defect and tear rates.
  - Older machinery under poor maintenance status incurs compounding efficiency losses.
  - Extended operating sessions (>16 hours) introduce progressive machine fatigue.
  - Low power stability causes intermittent micro-stoppages.

---

## Scoring System

### Evaluation Metric

Submissions are evaluated using the **overall percentage error** across all test samples:

$$\text{Overall Error \%} = \frac{\sum_{i=1}^{N} |\text{predicted}_i - \text{actual}_i|}{\sum_{i=1}^{N} \text{actual}_i} \times 100$$

### Points Scale (10 Points Maximum)

Points are mapped from the overall error percentage:

| Overall Error Bracket | Points |
|---|:---:|
| $\le 2.0\%$ | **10** |
| $> 2.0\%$ and $\le 5.0\%$ | **9** |
| $> 5.0\%$ and $\le 10.0\%$ | **8** |
| $> 10.0\%$ and $\le 15.0\%$ | **7** |
| $> 15.0\%$ and $\le 20.0\%$ | **6** |
| $> 20.0\%$ and $\le 30.0\%$ | **4** |
| $> 30.0\%$ and $\le 50.0\%$ | **2** |
| $> 50.0\%$ | **0** |

---

## Dependencies & Supported Libraries

The challenge environment provides standard Python scientific and machine learning libraries for data exploration, feature engineering, and model training:

- **Python 3** (3.8+) — Runtime environment
- **NumPy** (`numpy`) — Numerical array computations, vectorization, and data simulation
- **pandas** (`pandas`) — Tabular data manipulation, schema validation, and CSV I/O
- **scikit-learn** (`scikit-learn`) — Preprocessing pipelines, feature transformations, baseline regressors, and validation metrics
- **SciPy** (`scipy`) — Statistical distributions and scientific computing utilities
- **XGBoost** (`xgboost`) — Gradient boosted decision tree modeling for tabular regression
- **LightGBM** (`lightgbm`) — High-performance gradient boosting for tabular feature sets
- **Matplotlib** (`matplotlib`) — Plotting, distribution checks, and residual visualization
- **Seaborn** (`seaborn`) — Statistical data visualization and feature correlation analysis

---

## Repository Structure

```
challenges/printing-press/
├── data/
│   ├── train.csv         # 7,000 training sessions with features and target
│   ├── test.csv          # 1,500 test sessions with features only
│   └── answer_key.csv    # 1,500 private evaluation ground-truth (server-side only)
├── src/
│   └── scorer.py         # Official submission evaluation and scoring logic
├── tests/
│   └── test_scorer.py    # Unit tests for scoring logic and boundary checks
├── generator.py          # Synthetic dataset generation engine
├── benchmark.py          # Model benchmark runner (supports validation-only mode)
├── DESIGN.md             # Dataset physics and interaction specification
├── BENCHMARK.md          # Benchmark methodology notes
└── requirements.txt      # Python dependencies
```

---

## Getting Started

### 1. Running Unit Tests

Run the test suite to verify scoring logic and boundary transitions:

```bash
python -m unittest challenges/printing-press/tests/test_scorer.py
```

### 2. Running Benchmarks

```bash
python challenges/printing-press/benchmark.py
```

- **Validation-Only Mode**: When `data/answer_key.csv` is excluded (e.g. contestant sandbox), `benchmark.py` automatically evaluates baseline models on an 80/20 train/validation split.
- **Full Test Evaluation**: When `data/answer_key.csv` is present locally, `benchmark.py` automatically evaluates predictions across the full 1,500 test rows.

### 3. Scoring a Submission File

```bash
python challenges/printing-press/src/scorer.py submission.csv --answer-key challenges/printing-press/data/answer_key.csv
```
