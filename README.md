# 🖨️ Printing Press ML Challenge

> **Industrial Yield Regression Challenge for CodeVerse 2.0**, integrated into a browser-based development environment with live Python execution, automated scoring, and real-time telemetry visualizer.

[![Challenge Repository](https://img.shields.io/badge/Challenge_Repo-Printing__Press__ML-blue?logo=github)](https://github.com/aaditya-hamirani07/Printing_Press_ML)
[![Platform Repository](https://img.shields.io/badge/Platform_Repo-Online__IDE-10b981?logo=github)](https://github.com/aaditya-hamirani07/Online_IDE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python)](https://www.python.org/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Challenge Highlights](#-challenge-highlights)
- [How the Challenge Works](#-how-the-challenge-works)
- [Dataset Specifications](#-dataset-specifications)
- [Scoring System & Evaluation Metric](#-scoring-system--evaluation-metric)
- [Benchmark Results](#-benchmark-results)
- [Platform Architecture & Integration](#-platform-architecture--integration)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Getting Started & Local Setup](#-getting-started--local-setup)
- [Running Unit Tests & Benchmarks](#-running-unit-tests--benchmarks)
- [Security & Answer-Key Privacy](#-security--answer-key-privacy)
- [Links & References](#-links--references)

---

## 🎯 Overview

The **Printing Press ML Challenge** is a competitive machine learning regression task developed for the **CodeVerse 2.0** technical competition. Contestants analyze simulated industrial manufacturing telemetry to predict total production output (**`amount_printed`**) under varying mechanical, operational, and environmental conditions.

To provide an accessible competition experience, the challenge is hosted on **[Online_IDE](https://github.com/aaditya-hamirani07/Online_IDE)** — a full-stack, browser-based development platform featuring Monaco code editing, isolated Python runtime execution, automated validation, and visual regression telemetry.

The core challenge logic and dataset generation engine are also maintained as a standalone open-source repository at **[Printing_Press_ML](https://github.com/aaditya-hamirani07/Printing_Press_ML)**.

---

## ✨ Challenge Highlights

- **Supervised Industrial Regression**: Predict continuous production volume (`amount_printed`) from multi-dimensional telemetry data.
- **8,500 Total Samples**: Partitioned into a public training set (7,000 samples) and a withheld evaluation test set (1,500 samples).
- **15 Heterogeneous Features**: 8 numerical metrics and 7 categorical features spanning machine specifications, sensor readings, and shift logs.
- **Physical Non-Linear Dynamics**: Synthesized using a domain-driven simulation engine ([`generator.py`](challenges/printing-press/generator.py)) with realistic mechanical vibration, thermal degradation, humidity moisture resistance, and machine fatigue.
- **Automated In-IDE Grading**: Real-time evaluation pipeline with automated schema validation, relative absolute percentage error scoring, and a 10-point scale.
- **Telemetry Visualizer**: Automatic capture and rendering of Matplotlib / Seaborn residual plots directly in the web UI.

---

## 🕹️ How the Challenge Works

Contestants interact with the challenge through the dedicated workspace route at `/printing-press`:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│  1. Explore     │  ──►  │  2. Preprocess  │  ──►  │   3. Train      │  ──►  │  4. Evaluate     │
│  train.csv      │       │  & Engineer     │       │   ML Regressor  │       │  test.csv (1500) │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────┬────────┘
                                                                                        │
                                                                                        ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│  5. Automated Grading via Online_IDE Execution Service                                            │
│  • Compares 'predictions' against private answer key server-side                                 │
│  • Computes relative error percentage and maps to 10-point score                                 │
│  • Renders diagnostics checklist, error breakdown, and telemetry plots in IDE                    │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Explore the Data**: `train.csv` (features + ground-truth targets) and `test.csv` (features only) are automatically pre-seeded into the contestant's workspace.
2. **Feature Engineering & Preprocessing**: Handle sensor missing values (`NaN`), encode categorical identifiers (machine types, shifts, paper grades), and scale numerical features.
3. **Train Regression Models**: Train machine learning models using Scikit-learn, XGBoost, LightGBM, or custom ensembles.
4. **Generate Test Predictions**: Run inference on `test.csv` and assign the 1,500-element output array to the global `predictions` variable.
5. **Instant In-Browser Evaluation**: Click **"Run Operation"** to execute the script in the isolated backend runner. The server validates output format, scores predictions against the private ground truth, and displays points and visual diagnostics.

---

## 📊 Dataset Specifications

The dataset models realistic industrial printing press operations with complex feature interactions:

| Partition | Rows | Columns | Target Column | Access |
|---|---:|---:|---|---|
| [`data/train.csv`](challenges/printing-press/data/train.csv) | 7,000 | 17 (ID + 15 features + target) | `amount_printed` | Public in workspace |
| [`data/test.csv`](challenges/printing-press/data/test.csv) | 1,500 | 16 (ID + 15 features) | Withheld | Public in workspace |
| `data/answer_key.csv` | 1,500 | 2 (ID + `amount_printed`) | `amount_printed` | Private (server-side only) |

### Feature Summary

- **Numerical Features (8)**: `printing_speed` (prints/min), `machine_age` (years), `operating_hours` (hours), `temperature` (°C), `humidity` (%), `power_stability` (0–100 index), `setup_time` (mins), `last_calibration_day` (days).
- **Categorical Features (7)**: `paper_type` (Standard, Glossy, Matte, Cardstock), `shift` (Morning, Afternoon, Night), `maintenance_status` (Good, Average, Poor), `machine_type` (Type_A–D), `paper_quality` (Low, Medium, High), `operator_id` (Op01–Op10), `ink_batch_id` (B01–B20).

*For the complete mathematical physics specification, see [`DESIGN.md`](challenges/printing-press/DESIGN.md).*

---

## 📐 Scoring System & Evaluation Metric

Submissions are evaluated on the test set using the **Relative Absolute Percentage Error** metric:

$$\text{Overall Error \%} = \frac{\sum_{i=1}^{N} |\text{predicted}_i - \text{actual}_i|}{\sum_{i=1}^{N} \text{actual}_i} \times 100$$

### Official 10-Point Scoring Scale

Points are awarded based on the overall percentage error on the held-out 1,500 test samples:

| Overall Error Bracket | Official Score | Performance Tier |
|---|:---:|:---|
| $\le 2.0\%$ | **10 / 10** | 🏆 Grandmaster Tier (Exceptional precision & interaction modeling) |
| $> 2.0\%$ and $\le 5.0\%$ | **9 / 10** | 🥇 Top Benchmark (Tuned Gradient Boosting / Ensemble) |
| $> 5.0\%$ and $\le 10.0\%$ | **8 / 10** | 🥈 High Performance (Random Forest / Advanced Trees) |
| $> 10.0\%$ and $\le 15.0\%$ | **7 / 10** | 🥉 Solid Generalization (Ridge Regression / Linear Baselines) |
| $> 15.0\%$ and $\le 20.0\%$ | **6 / 10** | Baseline ML Regressor |
| $> 20.0\%$ and $\le 30.0\%$ | **4 / 10** | Underfitted / Basic Linear Model |
| $> 30.0\%$ and $\le 50.0\%$ | **2 / 10** | Mean Baseline / Minimal Feature Extraction |
| $> 50.0\%$ | **0 / 10** | Untrained / Invalid Outputs |

---

## 📈 Benchmark Results

The challenge difficulty has been validated using four reproducible baseline models evaluated on the official 1,500-sample test set (see [`BENCHMARK.md`](challenges/printing-press/BENCHMARK.md)):

| Model | Validation R² (20% Holdout) | Test Error % (Ground Truth) | Official Points |
|:---|:---:|:---:|:---:|
| **Mean Baseline** (`DummyRegressor`) | −0.0000 | 39.81% | **2 / 10** |
| **Ridge Regression** (`Ridge(alpha=10.0)`) | 0.8284 | 15.54% | **6 / 10** |
| **Random Forest** (`n_estimators=150, max_depth=16`) | 0.9410 | 8.68% | **8 / 10** |
| **Gradient Boosting** (`HistGradientBoostingRegressor`) | 0.9790 | 4.76% | **9 / 10** |

> **Note**: The $\le 2.0\%$ error threshold (10/10 points) requires advanced feature engineering, nonlinear interaction terms, or tuned gradient boosting algorithms.

---

## 🏗️ Platform Architecture & Integration

Online_IDE provides the full execution and evaluation harness for the challenge:

```
┌────────────────────────────────────────────────────────────────────────┐
│                              BROWSER                                   │
│                                                                        │
│  ┌───────────────────────┐   ┌─────────────────┐   ┌────────────────┐  │
│  │ Challenge File Tree   │   │ Monaco Editor   │   │ Telemetry &    │  │
│  │ (main.py, train, test)│   │ (Python Source) │   │ Output Panel   │  │
│  └───────────┬───────────┘   └────────┬────────┘   └───────▲────────┘  │
│              │                        │                    │           │
│              └────────────────────────┼────────────────────┘           │
│                                       ▼                                │
│                   POST /api/printing-press/run                         │
└───────────────────────────────────────┬────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Next.js 16 App Router Backend                        │
│   • Injects execution wrapper & telemetry extraction hooks             │
│   • Validates prediction array format (shape, numeric, NaN/Inf checks) │
│   • Computes error against server-side answer key                      │
│   • Maps error to 10-point scale & contextual feedback hints           │
└───────────────────────────────────────┬────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│              Modular Execution Backend Service (:4000)                 │
│   • Sandboxed workspace directory isolation                            │
│   • Pre-seeds train.csv & test.csv into execution workspace            │
│   • Thread limits (SANDBOX_THREAD_CAP=4) & 5-minute timeout caps       │
│   • Captures Matplotlib / Seaborn plots in headless mode               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Machine Learning & Data Science Stack
- **Runtime**: Python 3.10+
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning**: [Scikit-learn](https://scikit-learn.org/), [SciPy](https://scipy.org/), [XGBoost](https://xgboost.readthedocs.io/), [LightGBM](https://lightgbm.readthedocs.io/)
- **Data Visualization**: [Matplotlib](https://matplotlib.org/) (Headless `Agg`), [Seaborn](https://seaborn.pydata.org/)

### IDE & Platform Infrastructure
- **Frontend Framework**: [Next.js 16](https://nextjs.org/) (App Router) + [React 19](https://react.dev/)
- **Code Editor**: [@monaco-editor/react](https://github.com/suren-atoyan/monaco-react)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Terminal Emulator**: [@xterm/xterm](https://xtermjs.org/) + [node-pty](https://github.com/microsoft/node-pty)
- **Storage & State**: [Supabase](https://supabase.com/) (PostgreSQL & Storage) + [Dexie.js](https://dexie.org/) (IndexedDB)
- **Backend Execution Service**: Node.js HTTP/WebSocket server with process tree management

---

## 📁 Repository Structure

```
Online_IDE/
├── challenges/
│   └── printing-press/            # 🖨️ Printing Press ML Challenge Core
│       ├── data/
│       │   ├── train.csv          # 7,000 training samples (public)
│       │   ├── test.csv           # 1,500 test samples (public features)
│       │   └── answer_key.csv     # 1,500 private test targets (server-only)
│       ├── src/
│       │   └── scorer.py          # Official scoring module & validation logic
│       ├── tests/
│       │   └── test_scorer.py     # Unit tests for scoring boundaries
│       ├── generator.py           # Synthetic physical simulation dataset generator
│       ├── benchmark.py           # Difficulty benchmark runner (test & val modes)
│       ├── DESIGN.md              # Domain physics & feature interaction design
│       ├── BENCHMARK.md           # Benchmark documentation & model baseline table
│       ├── README.md              # Dedicated challenge documentation
│       └── requirements.txt       # Python ML dependencies
├── src/
│   ├── app/
│   │   ├── printing-press/        # 🎯 Challenge workspace & heist-themed UI
│   │   ├── project/[id]/          # Cloud project workspace
│   │   ├── local/                 # Local folder workspace (FS Access API)
│   │   └── api/
│   │       └── printing-press/
│   │           ├── run/           # Code execution, validation & scoring API
│   │           └── verify/        # Event game key verification API
│   ├── components/                # Monaco Editor, OutputPanel, TerminalPanel, etc.
│   └── lib/                       # Language map, audio synthesizer, executor client
├── server/                        # Modular Node.js execution & terminal runner
│   ├── runner.js                  # Multi-language sandboxed execution runner
│   ├── workspace.js               # Workspace isolation & challenge dataset seeding
│   ├── env.js                     # Environment sanitization & thread capping
│   └── terminal.js                # node-pty WebSocket PTY session management
├── scripts/
│   └── test-system.js             # Automated end-to-end service verification
├── package.json                   # Project scripts and dependencies
└── tsconfig.json                  # TypeScript configuration
```

---

## 🚀 Getting Started & Local Setup

### 1. Prerequisites

- **Node.js 20+** and npm
- **Python 3.10+** with scientific and ML packages

### 2. Install Dependencies

```bash
# Install platform npm dependencies
npm install

# Install challenge Python ML dependencies
pip install -r challenges/printing-press/requirements.txt
```

### 3. Environment Configuration

Create a local environment file:

```bash
cp .env.local.example .env.local
```

Default local environment values:

```ini
EXECUTOR_URL=http://localhost:4000
NEXT_PUBLIC_EXECUTOR_URL=http://localhost:4000
NEXT_PUBLIC_TERMINAL_WS_URL=ws://localhost:4000/terminal
```

### 4. Running the Platform Services

Start the execution service (runs on port 4000):

```bash
npm run server
```

In a separate terminal, start the Next.js development server:

```bash
npm run dev
```

Visit [`http://localhost:3000/printing-press`](http://localhost:3000/printing-press) to open the challenge interface.

---

## 🧪 Running Unit Tests & Benchmarks

### 1. Scorer Unit Tests

Run the official unit test suite to verify scoring boundaries and validation constraints:

```bash
python -m unittest challenges/printing-press/tests/test_scorer.py
```

### 2. Model Benchmark Suite

Run the reproducible benchmark suite:

```bash
python challenges/printing-press/benchmark.py
```

- **With Answer Key**: Computes both 20% holdout validation metrics and official ground-truth test scores.
- **Without Answer Key (Validation Mode)**: Automatically falls back to 80/20 train/validation evaluation.

### 3. Submission CLI Scorer

To score a submission CSV file against the answer key via CLI:

```bash
python challenges/printing-press/src/scorer.py submission.csv --answer-key challenges/printing-press/data/answer_key.csv
```

---

## 🔒 Security & Answer-Key Privacy

- **Strict Dataset Isolation**: [`server/workspace.js`](server/workspace.js) seeds only `train.csv` and `test.csv` to contestant workspaces. `answer_key.csv` is never copied to user directories.
- **Server-Side Grading**: Prediction evaluation occurs in the backend API ([`src/app/api/printing-press/run/route.ts`](src/app/api/printing-press/run/route.ts)) or from private cloud storage in production.
- **Resource Limits**: The execution runner enforces execution timeouts (5 minutes), CPU thread caps (`SANDBOX_THREAD_CAP=4`), and sanitized environment variables.

---

## 🔗 Links & References

- **Standalone Challenge Repo**: [github.com/aaditya-hamirani07/Printing_Press_ML](https://github.com/aaditya-hamirani07/Printing_Press_ML)
- **Deployment Platform Repo**: [github.com/aaditya-hamirani07/Online_IDE](https://github.com/aaditya-hamirani07/Online_IDE)
- **Dataset Generation Engine**: [`challenges/printing-press/generator.py`](challenges/printing-press/generator.py)
- **Official Scorer**: [`challenges/printing-press/src/scorer.py`](challenges/printing-press/src/scorer.py)
- **Difficulty Benchmark**: [`challenges/printing-press/BENCHMARK.md`](challenges/printing-press/BENCHMARK.md)
- **Physics & Design Specification**: [`challenges/printing-press/DESIGN.md`](challenges/printing-press/DESIGN.md)
