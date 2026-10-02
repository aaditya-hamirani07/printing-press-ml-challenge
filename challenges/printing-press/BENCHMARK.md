# Printing Press ML — Difficulty Benchmark

## Official Scoring Metric

```
overall_error_percentage =
    (SUM(abs(predicted_amount - actual_amount)) / SUM(actual_amount)) × 100
```

## Points Scale

| Overall Error | Points |
|---|---:|
| ≤ 2% | 10 |
| > 2% and ≤ 5% | 9 |
| > 5% and ≤ 10% | 8 |
| > 10% and ≤ 15% | 7 |
| > 15% and ≤ 20% | 6 |
| > 20% and ≤ 30% | 4 |
| > 30% and ≤ 50% | 2 |
| > 50% | 0 |

---

## Benchmark Results

Evaluated on the official 1,500-row test set.
Validation R² is measured on a held-out 20% split of `train.csv` only.
The private `answer_key.csv` was used solely for final test evaluation.

| Model | Validation R² | Test Error % | Points |
|---|---:|---:|---:|
| Mean Baseline | −0.0000 | 39.81% | 2/10 |
| Ridge Regression | 0.8262 | 15.54% | 6/10 |
| Random Forest | 0.9410 | 8.68% | 8/10 |
| Gradient Boosting | 0.9790 | 4.76% | 9/10 |

---

## Notes

- All models used default or conservative hyperparameters with no extensive tuning.
- Categorical features were one-hot encoded; numerical missing values imputed with the median.
- The `10`-point bracket (≤ 2% error) was not achieved by any of the baselines above.
- Dataset: 7,000 training rows, 1,500 test rows, 15 features, seed 2026.
