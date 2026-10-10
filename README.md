# 🖨️ Printing Press ML Challenge

> **Interactive Machine Learning Regression Challenge**, integrated into a locally runnable web-based coding workspace with Python execution, automated evaluation, and visualization support.

[![Challenge Repository](https://img.shields.io/badge/Challenge_Repo-Printing__Press__ML-blue?logo=github)](https://github.com/aaditya-hamirani07/Printing_Press_ML)
[![Platform Repository](https://img.shields.io/badge/Platform_Repo-Online__IDE-10b981?logo=github)](https://github.com/aaditya-hamirani07/Online_IDE)
[![Python Version](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python)](https://www.python.org/)
[![Next.js Framework](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)

---

## 📖 Table of Contents

- [🎯 Overview](#overview)
- [✨ Challenge Highlights](#challenge-highlights)
- [⚙️ How the Challenge Works](#how-the-challenge-works)
- [📊 Dataset Specifications](#dataset-specifications)
- [📐 Scoring System & Evaluation Metric](#scoring-system--evaluation-metric)
- [📈 Benchmark Results](#benchmark-results)
- [🏗️ Platform Architecture & Integration](#platform-architecture--integration)
- [🛠️ Tech Stack](#tech-stack)
- [📁 Repository Structure](#repository-structure)
- [🚀 Getting Started & Local Setup](#getting-started--local-setup)
- [🧪 Running Unit Tests & Benchmarks](#running-unit-tests--benchmarks)
- [🔒 Security & Answer-Key Privacy](#security--answer-key-privacy)
- [🔗 Links & References](#links--references)

---

## 🎯 Overview

The **Printing Press ML Challenge** is an machine learning regression challenge built around a synthetic printing-press dataset. The objective is to predict the total production volume (**`amount_printed`**) from machine-related, material, operational, and environmental features.

The challenge can be run through **[Online_IDE](https://github.com/aaditya-hamirani07/Online_IDE)**, a web-based coding workspace with Monaco editing, Python execution, automated evaluation, and Matplotlib plot rendering. It is locally runnable and is not presented here as a publicly hosted service.

The core dataset generation engine, physics simulation design, and scoring modules are also available as a standalone repository at **[Printing_Press_ML](https://github.com/aaditya-hamirani07/Printing_Press_ML)**.

---

## ✨ Challenge Highlights

- 🎯 **Regression Prediction Challenge**: Predict the continuous target (`amount_printed`) from structured tabular features.
- 📦 **8,500 Total Samples**: Partitioned into a public training set (7,000 samples) and a withheld evaluation test set (1,500 samples).
- 🔬 **15 Input Features**: 8 numerical metrics and 7 categorical features modeling machinery, environmental sensors, materials, and shifts.
- ⚙️ **Synthetic Physical Simulation**: Generated using a synthetic domain-inspired model ([`generator.py`](challenges/printing-press/generator.py)) with nonlinear feature relationships and 3 noise features.
- ⚡ **Automated In-IDE Grading**: Real-time evaluation pipeline via `POST /api/printing-press/run` that inspects the participant's `predictions` variable, validates schema and value bounds, and computes official score points.
- 📊 **Telemetry Visualizer**: Automatic server-side capture of Matplotlib and Seaborn plots rendered directly in the web UI.

---

## ⚙️ How the Challenge Works

Contestants participate directly in the browser via the challenge workspace at `/printing-press`:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CONTESTANT WORKSPACE                            │
│                                                                        │
│   1. Explore Datasets         2. Engineer Features & Model             │
│   ┌─────────────────────┐     ┌────────────────────────────────────┐   │
│   │ train.csv (7,000)   │ ──► │ • Impute missing sensor values     │   │
│   │ test.csv  (1,500)   │     │ • One-hot encode categoricals      │   │
│   └─────────────────────┘     │ • Train ML regressor (Trees/GBDT)  │   │
│                               └─────────────────┬──────────────────┘   │
│                                                 ▼                      │
│   3. Generate Predictions     4. Execute & Score ("Run Operation")     │
│   ┌─────────────────────┐     ┌────────────────────────────────────┐   │
│   │ predictions = [...] │ ──► │ POST /api/printing-press/run       │   │
│   │ (len == 1,500)      │     │ • Sandboxed runner execution       │   │
│   └─────────────────────┘     │ • Graded against private targets   │   │
│                               └─────────────────┬──────────────────┘   │
└─────────────────────────────────────────────────┼──────────────────────┘
                                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     AUTOMATED EVALUATION FEEDBACK                      │
│   • Checklist: Exit Code 0, Prediction Variable, Length, No NaN/Inf    │
│   • Official Metric: Relative Absolute Error % & Score (out of 10)     │
│   • Visual Telemetry: Matplotlib / Seaborn plots automatically rendered │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Explore the Datasets**: `train.csv` (features and target) and `test.csv` (features only) are automatically pre-seeded in the workspace.
2. **Preprocess & Feature Engineer**: Handle missing sensor values (`NaN`), encode categorical features, and extract interaction signals.
3. **Train Regression Models**: Train regression models (e.g. Ridge, Random Forest, HistGradientBoosting, XGBoost, or LightGBM).
4. **Generate Test Predictions**: Run model inference on `test.csv` and assign the 1,500 predictions to the global variable `predictions`.
5. **Submit & Review Diagnostics**: Click **"Run Operation"** to execute the script in the isolated runner. The server validates execution integrity, grades predictions against the private answer key, and displays the score breakdown.

---

## 📊 Dataset Specifications

The synthetic dataset is designed to represent printing-press operations using nonlinear relationships and feature interactions; it is not real industrial production data:

| Dataset | Rows | Columns | Target (`amount_printed`) | Status |
|---|---:|---:|---|---|
| [`data/train.csv`](challenges/printing-press/data/train.csv) | 7,000 | 17 (ID + 15 features + target) | Included | Public training set |
| [`data/test.csv`](challenges/printing-press/data/test.csv) | 1,500 | 16 (ID + 15 features) | Withheld | Public evaluation features |
| `data/answer_key.csv` | 1,500 | 2 (ID + target) | Server-side only | Private evaluation ground truth; not copied into contestant workspaces |

### Feature Summary

- **Numerical Features (8)**: `printing_speed` (prints/min), `machine_age` (years), `operating_hours` (hours), `temperature` (°C), `humidity` (%), `power_stability` (0–100 index), `setup_time` (minutes), `last_calibration_day` (days, noise).
- **Categorical Features (7)**: `paper_type` (Standard, Glossy, Matte, Cardstock), `shift` (Morning, Afternoon, Night), `maintenance_status` (Good, Average, Poor), `machine_type` (Type_A–D), `paper_quality` (Low, Medium, High), `operator_id` (Op01–Op10, noise), `ink_batch_id` (B01–B20, noise).

*For the complete mathematical physics formulation, see [`DESIGN.md`](challenges/printing-press/DESIGN.md).*

---

## 📐 Scoring System & Evaluation Metric

Submissions are evaluated on the 1,500 test samples using the **Relative Absolute Percentage Error** metric:

$$\text{Overall Error \%} = \frac{\sum_{i=1}^{N} |\text{predicted}_i - \text{actual}_i|}{\sum_{i=1}^{N} \text{actual}_i} \times 100$$

### Official 10-Point Scoring Scale

Points are awarded based on the overall percentage error on the withheld test set:

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

## 📈 Benchmark Results

Challenge difficulty is benchmarked across four standard machine learning models evaluated under reproducible conditions (see [`BENCHMARK.md`](challenges/printing-press/BENCHMARK.md)):

| Model | Validation R² (20% Holdout) | Test Error % (Ground Truth) | Official Points |
|:---|:---:|:---:|:---:|
| **Mean Baseline** (`DummyRegressor`) | −0.0000 | 39.81% | **2 / 10** |
| **Ridge Regression** (`Ridge(alpha=10.0)`) | 0.8284 | 15.54% | **6 / 10** |
| **Random Forest** (`n_estimators=150, max_depth=16`) | 0.9410 | 8.68% | **8 / 10** |
| **Gradient Boosting** (`HistGradientBoostingRegressor`) | 0.9790 | 4.76% | **9 / 10** |

> 💡 **Note**: Validation R² is measured on a held-out 20% split of `train.csv`. The private evaluation ground truth is used solely for final test scoring. The $\le 2.0\%$ bracket (10 points) was not reached by standard baseline models with default hyperparameters.

---

## 🏗️ Platform Architecture & Integration

Online_IDE provides the full execution and evaluation runtime for the challenge:

- 🖥️ **Frontend (`src/app/printing-press/`)**: Monaco code editor with custom themes, interactive progress tracking, audio controls, and an output console with a visualization tab.
- ⚙️ **Grading API (`src/app/api/printing-press/run/route.ts`)**: Wraps contestant code with headless Matplotlib configuration (`MPLBACKEND=Agg`), intercepts predictions, and grades them server-side.
- 🔒 **Execution Service (`server/`)**: Modular Node.js execution backend that manages workspace directories, pre-seeds challenge data, enforces thread limits (`SANDBOX_THREAD_CAP=4`), and caps runtimes at 5 minutes.

---

## 🛠️ Tech Stack

### Machine Learning & Data Science Stack
- **Language**: Python 3.10+
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning**: [Scikit-learn](https://scikit-learn.org/), [SciPy](https://scipy.org/), [XGBoost](https://xgboost.readthedocs.io/), [LightGBM](https://lightgbm.readthedocs.io/)
- **Visualization**: [Matplotlib](https://matplotlib.org/) (Headless `Agg`), [Seaborn](https://seaborn.pydata.org/)

### IDE & Platform Stack
- **Frontend**: [Next.js 16](https://nextjs.org/) (App Router), [React 19](https://react.dev/), [Tailwind CSS v4](https://tailwindcss.com/)
- **Editor & Terminal**: [@monaco-editor/react](https://github.com/suren-atoyan/monaco-react), [@xterm/xterm](https://xtermjs.org/), [node-pty](https://github.com/microsoft/node-pty)
- **Backend & Storage**: Node.js execution runner, [Supabase](https://supabase.com/) (PostgreSQL & Storage), [Dexie.js](https://dexie.org/) (IndexedDB)

---

## 📁 Repository Structure

```
Online_IDE/
├── challenges/
│   └── printing-press/            # 🖨️ Printing Press ML Challenge Core
│       ├── data/
│       │   ├── train.csv          # 7,000 training samples (public)
│       │   └── test.csv           # 1,500 test samples (public features)
│       ├── src/
│       │   └── scorer.py          # Official scoring & validation logic
│       ├── tests/
│       │   └── test_scorer.py     # Unit tests for scoring boundaries
│       ├── generator.py           # Physical simulation dataset generator
│       ├── benchmark.py           # Difficulty benchmark runner (test & val modes)
│       ├── DESIGN.md              # Mathematical dataset physics specification
│       ├── BENCHMARK.md           # Benchmark documentation & baseline table
│       ├── README.md              # Dedicated challenge documentation
│       └── requirements.txt       # Challenge Python dependencies
├── src/
│   ├── app/
│   │   ├── printing-press/        # 🎯 Challenge workspace interface
│   │   └── api/printing-press/    # Execution, validation & key verification APIs
│   ├── components/                # Editor, OutputPanel, TerminalPanel, UI modals
│   └── lib/                       # Executor client, language map, audio utilities
├── server/                        # Sandboxed execution & terminal backend
│   ├── runner.js                  # Multi-language code execution runner
│   ├── workspace.js               # Workspace isolation & dataset seeding
│   ├── env.js                     # Environment sanitization & thread capping
│   └── terminal.js                # node-pty WebSocket terminal service
├── scripts/
│   └── test-system.js             # Automated end-to-end service verification
├── package.json                   # Platform scripts and dependencies
└── tsconfig.json                  # TypeScript compiler configuration
```

---

## 🚀 Getting Started & Local Setup

### 1. Prerequisites

- **Node.js 20+** and npm
- **Python 3.10+** with ML packages

### 2. Install Dependencies

```bash
# Install platform npm dependencies
npm install

# Install challenge Python ML dependencies
pip install -r challenges/printing-press/requirements.txt
```

### 3. Environment Configuration

Create a local environment file from the example template:

```bash
cp .env.local.example .env.local
```

Default local service configuration:

```ini
EXECUTOR_URL=http://localhost:4000
NEXT_PUBLIC_EXECUTOR_URL=http://localhost:4000
NEXT_PUBLIC_TERMINAL_WS_URL=ws://localhost:4000/terminal
```

### 4. Running the Services

Start the backend execution service (port 4000):

```bash
npm run server
```

In a separate terminal, start the Next.js development server:

```bash
npm run dev
```

Open [`http://localhost:3000/printing-press`](http://localhost:3000/printing-press) to access the challenge workspace.

---

## 🧪 Running Unit Tests & Benchmarks

Run the official scoring unit tests:

```bash
python -m unittest challenges/printing-press/tests/test_scorer.py
```

Run the model difficulty benchmark:

```bash
python challenges/printing-press/benchmark.py
```

Score a submission file via CLI:

```bash
python challenges/printing-press/src/scorer.py submission.csv --answer-key challenges/printing-press/data/answer_key.csv
```

---

## 🔒 Security & Answer-Key Privacy

- 🛡️ **Dataset Isolation**: [`server/workspace.js`](server/workspace.js) copies only `train.csv` and `test.csv` into contestant workspaces; `answer_key.csv` is used only by the server-side evaluator and is never copied into contestant workspaces or exposed to the client.
- 🔐 **Server-Side Evaluation**: Test set prediction scoring executes exclusively on the backend server or via private storage in production.
- ⏱️ **Resource Sandboxing**: Execution is bounded by a 5-minute timeout, CPU thread caps (`SANDBOX_THREAD_CAP=4`), and a 2MB output buffer limit.

---
