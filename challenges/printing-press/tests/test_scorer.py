"""Unit and integration tests for competition scorer."""

import os
import sys
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    import scorer
except ImportError:
    from src import scorer


class TestScorer(unittest.TestCase):
    """Test suite for scorer.py functions and boundary conditions."""

    def test_calculate_points_boundaries(self):
        """Verify all exact boundary conditions specified for competition scoring."""
        boundaries = [
            (0.00, 10),
            (1.50, 10),
            (2.00, 10),         # <= 2.0% -> 10
            (2.0001, 9),        # > 2.0% and <= 5.0% -> 9
            (4.25, 9),          # 4.25% -> 9
            (4.99, 9),
            (5.00, 9),          # <= 5.0% -> 9
            (5.0001, 8),        # > 5.0% and <= 10.0% -> 8
            (7.43, 8),
            (8.19, 8),          # 8.19% -> 8
            (9.99, 8),
            (10.00, 8),         # <= 10.0% -> 8
            (10.0001, 7),       # > 10.0% and <= 15.0% -> 7
            (14.99, 7),
            (15.00, 7),         # <= 15.0% -> 7
            (15.0001, 6),       # > 15.0% and <= 20.0% -> 6
            (19.99, 6),
            (20.00, 6),         # <= 20.0% -> 6
            (20.0001, 4),       # > 20.0% and <= 30.0% -> 4
            (29.99, 4),
            (30.00, 4),         # <= 30.0% -> 4
            (30.0001, 2),       # > 30.0% and <= 50.0% -> 2
            (49.99, 2),
            (50.00, 2),         # <= 50.0% -> 2
            (50.0001, 0),       # > 50.0% -> 0
            (75.00, 0),
            (120.0, 0)
        ]
        for err_pct, expected_pts in boundaries:
            with self.subTest(err_pct=err_pct):
                self.assertEqual(scorer.calculate_points(err_pct), expected_pts)

    def test_overall_error_calculation(self):
        """Verify the overall percentage error formula."""
        actuals = np.array([100.0, 200.0, 300.0])
        # Total actual = 600.0
        # Absolute errors = |110 - 100| + |190 - 200| + |300 - 300| = 10 + 10 + 0 = 20
        # Error % = (20 / 600) * 100 = 3.3333...
        preds = np.array([110.0, 190.0, 300.0])
        err = scorer.calculate_overall_error(preds, actuals)
        self.assertAlmostEqual(err, (20.0 / 600.0) * 100.0, places=4)

    def test_validation_missing_columns(self):
        """Verify rejection when required columns are missing."""
        key_df = pd.DataFrame({"id": ["PP0001", "PP0002"], "amount_printed": [10.0, 20.0]})
        bad_sub = pd.DataFrame({"id": ["PP0001", "PP0002"], "wrong_column": [10.0, 20.0]})
        with self.assertRaises(scorer.SubmissionValidationError):
            scorer.validate_submission(bad_sub, key_df)

    def test_validation_duplicate_ids(self):
        """Verify rejection when submission contains duplicate IDs."""
        key_df = pd.DataFrame({"id": ["PP0001", "PP0002"], "amount_printed": [10.0, 20.0]})
        bad_sub = pd.DataFrame({"id": ["PP0001", "PP0001"], "predicted_amount": [10.0, 20.0]})
        with self.assertRaises(scorer.SubmissionValidationError):
            scorer.validate_submission(bad_sub, key_df)

    def test_validation_missing_ids(self):
        """Verify rejection when submission omits test IDs."""
        key_df = pd.DataFrame({"id": ["PP0001", "PP0002", "PP0003"], "amount_printed": [10.0, 20.0, 30.0]})
        bad_sub = pd.DataFrame({"id": ["PP0001", "PP0002"], "predicted_amount": [10.0, 20.0]})
        with self.assertRaises(scorer.SubmissionValidationError):
            scorer.validate_submission(bad_sub, key_df)

    def test_validation_extra_ids(self):
        """Verify rejection when submission contains invalid/extra IDs."""
        key_df = pd.DataFrame({"id": ["PP0001", "PP0002"], "amount_printed": [10.0, 20.0]})
        bad_sub = pd.DataFrame({"id": ["PP0001", "PP0002", "PP9999"], "predicted_amount": [10.0, 20.0, 30.0]})
        with self.assertRaises(scorer.SubmissionValidationError):
            scorer.validate_submission(bad_sub, key_df)

    def test_validation_nan_predictions(self):
        """Verify rejection when predictions contain NaNs."""
        key_df = pd.DataFrame({"id": ["PP0001", "PP0002"], "amount_printed": [10.0, 20.0]})
        bad_sub = pd.DataFrame({"id": ["PP0001", "PP0002"], "predicted_amount": [10.0, np.nan]})
        with self.assertRaises(scorer.SubmissionValidationError):
            scorer.validate_submission(bad_sub, key_df)

    def test_validation_non_numeric_predictions(self):
        """Verify rejection when predictions contain strings."""
        key_df = pd.DataFrame({"id": ["PP0001", "PP0002"], "amount_printed": [10.0, 20.0]})
        bad_sub = pd.DataFrame({"id": ["PP0001", "PP0002"], "predicted_amount": [10.0, "text"]})
        with self.assertRaises(scorer.SubmissionValidationError):
            scorer.validate_submission(bad_sub, key_df)


if __name__ == "__main__":
    unittest.main()
