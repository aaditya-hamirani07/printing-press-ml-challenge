"""Printing Press ML — Difficulty Benchmark

Evaluates challenge difficulty across four standard machine learning approaches:
1. Mean Baseline
2. Ridge Regression
3. Random Forest Regressor
4. Gradient Boosting Regressor

Validation metrics (RMSE, MAE, R²) are computed on a 20% validation split
derived solely from train.csv. If data/answer_key.csv is present locally,
post-hoc evaluation of test set predictions is performed using the official
scoring metric. If data/answer_key.csv is missing (such as on a fresh public clone),
the script safely falls back to a train/validation evaluation mode without crashing.
"""

from __future__ import annotations

import os
import sys
from typing import Optional, Tuple
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Import official scoring module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    import scorer
except ImportError:
    from src import scorer

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data") if os.path.exists(os.path.join(BASE_DIR, "data")) else "data"
TRAIN_PATH = os.path.join(DATA_DIR, "train.csv")
TEST_PATH = os.path.join(DATA_DIR, "test.csv")
ANSWER_KEY_PATH = os.path.join(DATA_DIR, "answer_key.csv")


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]:
    """Load train, test, and optional private answer key datasets."""
    if not os.path.exists(TRAIN_PATH):
        raise FileNotFoundError(f"Training dataset not found at '{TRAIN_PATH}'")
    if not os.path.exists(TEST_PATH):
        raise FileNotFoundError(f"Test dataset not found at '{TEST_PATH}'")

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    answer_key_df = None
    if os.path.exists(ANSWER_KEY_PATH):
        try:
            answer_key_df = pd.read_csv(ANSWER_KEY_PATH)
        except Exception as err:
            print(f"[Warning] Could not read '{ANSWER_KEY_PATH}': {err}. Falling back to validation-only mode.")
            answer_key_df = None

    return train_df, test_df, answer_key_df


def build_preprocessors(num_cols, cat_cols):
    """Build standard scikit-learn preprocessing pipelines."""
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, num_cols),
            ("cat", cat_transformer, cat_cols),
        ]
    )
    return preprocessor


def main():
    print("Loading competition datasets...")
    train_df, test_df, answer_key_df = load_datasets()
    has_answer_key = answer_key_df is not None

    target_col = "amount_printed"
    id_col = "id"

    # Separate features and target from train
    X = train_df.drop(columns=[id_col, target_col])
    y = train_df[target_col]

    # Test features without id
    X_test = test_df.drop(columns=[id_col])
    actual_test_targets = None
    if has_answer_key:
        try:
            actual_test_targets = (
                answer_key_df.set_index(id_col)[target_col]
                .loc[test_df[id_col]]
                .to_numpy()
            )
        except Exception as err:
            print(f"[Warning] Failed to align answer key with test IDs: {err}. Falling back to validation-only mode.")
            has_answer_key = False

    # Identify numerical and categorical columns
    num_cols = [
        "printing_speed", "machine_age", "operating_hours",
        "temperature", "humidity", "power_stability",
        "setup_time", "last_calibration_day"
    ]
    cat_cols = [
        "paper_type", "shift", "maintenance_status",
        "machine_type", "paper_quality", "operator_id", "ink_batch_id"
    ]

    # Split train.csv ONLY (80% train / 20% validation)
    X_tr, X_val, y_tr, y_val = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    y_val_arr = y_val.to_numpy()

    preprocessor = build_preprocessors(num_cols, cat_cols)

    # Models to benchmark
    models = {
        "Mean Baseline": DummyRegressor(strategy="mean"),
        "Ridge Regression": Ridge(alpha=10.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=150,
            max_depth=16,
            min_samples_leaf=3,
            random_state=42,
            n_jobs=-1
        ),
        "Gradient Boosting": HistGradientBoostingRegressor(
            max_iter=200,
            max_depth=8,
            learning_rate=0.08,
            random_state=42
        ),
    }

    results = []

    for name, model in models.items():
        pipe = Pipeline([
            ("prep", preprocessor),
            ("reg", model)
        ])

        # 1. Fit on training split
        pipe.fit(X_tr, y_tr)

        # 2. Evaluate on validation split (derived strictly from train.csv)
        val_preds = np.maximum(0.0, pipe.predict(X_val))
        val_rmse = np.sqrt(mean_squared_error(y_val, val_preds))
        val_mae = mean_absolute_error(y_val, val_preds)
        val_r2 = r2_score(y_val, val_preds)
        val_err_pct = scorer.calculate_overall_error(val_preds, y_val_arr)
        val_points = scorer.calculate_points(val_err_pct)

        test_err_pct = None
        test_points = None

        # 3. If answer key is available, fit on FULL train.csv and evaluate on test.csv
        if has_answer_key and actual_test_targets is not None:
            pipe.fit(X, y)
            test_preds = np.maximum(0.0, pipe.predict(X_test))
            test_err_pct = scorer.calculate_overall_error(test_preds, actual_test_targets)
            test_points = scorer.calculate_points(test_err_pct)

        results.append({
            "Model": name,
            "Val RMSE": val_rmse,
            "Val MAE": val_mae,
            "Val R²": val_r2,
            "Val Error %": val_err_pct,
            "Val Points": val_points,
            "Test Error %": test_err_pct,
            "Test Points": test_points,
        })

    # Print results summary table
    print("\n" + "=" * 68)
    if has_answer_key:
        print("PRINTING PRESS ML — DIFFICULTY BENCHMARK (FULL TEST EVALUATION)")
        print("=" * 68)
        header = f"{'Model':<25}{'Validation R²':<17}{'Test Error %':<16}{'Test Points'}"
        print(header)
        print("-" * 68)
        for r in results:
            val_r2_str = f"{r['Val R²']:.4f}"
            test_err_str = f"{r['Test Error %']:.2f}%"
            print(f"{r['Model']:<25}{val_r2_str:<17}{test_err_str:<16}{r['Test Points']}/10")
    else:
        print("PRINTING PRESS ML — DIFFICULTY BENCHMARK (VALIDATION ONLY)")
        print("Notice: 'data/answer_key.csv' not found. Showing 20% holdout validation.")
        print("=" * 68)
        header = f"{'Model':<25}{'Validation R²':<17}{'Val Error %':<16}{'Val Points'}"
        print(header)
        print("-" * 68)
        for r in results:
            val_r2_str = f"{r['Val R²']:.4f}"
            val_err_str = f"{r['Val Error %']:.2f}%"
            print(f"{r['Model']:<25}{val_r2_str:<17}{val_err_str:<16}{r['Val Points']}/10")
    print("=" * 68 + "\n")

    # Detailed diagnostic breakdown
    print("Detailed Model Breakdown:")
    print("-" * 68)
    for r in results:
        print(f"{r['Model']}:")
        print(f"  [Validation Split (20%)] RMSE: {r['Val RMSE']:,.2f} | MAE: {r['Val MAE']:,.2f} | R²: {r['Val R²']:.4f} | Error: {r['Val Error %']:.2f}% ({r['Val Points']}/10 pts)")
        if has_answer_key and r["Test Error %"] is not None:
            print(f"  [Test Ground Truth]    Overall Error: {r['Test Error %']:.2f}% -> Official Points: {r['Test Points']}/10")

    # Benchmark summary range
    if has_answer_key:
        min_err_model = min(results, key=lambda x: x["Test Error %"])
        max_err_model = max(results, key=lambda x: x["Test Error %"])
        print("\nTest Benchmark Range:")
        print(f"  Lowest Test Error : {min_err_model['Test Error %']:.2f}% ({min_err_model['Model']}) -> {min_err_model['Test Points']}/10 pts")
        print(f"  Highest Test Error: {max_err_model['Test Error %']:.2f}% ({max_err_model['Model']}) -> {max_err_model['Test Points']}/10 pts")
    else:
        min_val_model = min(results, key=lambda x: x["Val Error %"])
        max_val_model = max(results, key=lambda x: x["Val Error %"])
        print("\nValidation Benchmark Range:")
        print(f"  Lowest Val Error : {min_val_model['Val Error %']:.2f}% ({min_val_model['Model']}) -> {min_val_model['Val Points']}/10 pts")
        print(f"  Highest Val Error: {max_val_model['Val Error %']:.2f}% ({max_val_model['Model']}) -> {max_val_model['Val Points']}/10 pts")
        print("\n[Tip] To run test-set scoring, provide 'data/answer_key.csv' in the data directory.")


if __name__ == "__main__":
    main()
