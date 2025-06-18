"""
Unit tests for probability utilities
"""

import pytest
import numpy as np
from utils.probability_utils import (
    normalize_probabilities,
    ensure_probability_bounds,
    normalize_binary_probabilities,
    weighted_probability_combination,
    ensemble_probabilities,
    calibrate_probability,
    confidence_interval_from_probability,
    safe_probability_division
)


class TestNormalizeProbabilities:
    """Test probability normalization functions"""
    
    def test_normalize_basic(self):
        """Test basic normalization"""
        probs = [0.2, 0.3, 0.1]
        normalized = normalize_probabilities(probs)
        
        assert np.allclose(np.sum(normalized), 1.0)
        assert all(0 <= p <= 1 for p in normalized)
    
    def test_normalize_zeros(self):
        """Test normalization of all zeros"""
        probs = [0, 0, 0]
        normalized = normalize_probabilities(probs)
        
        # Should return uniform distribution
        assert np.allclose(normalized, [1/3, 1/3, 1/3])
    
    def test_normalize_negative(self):
        """Test normalization with negative values"""
        probs = [-0.1, 0.5, 0.3]
        normalized = normalize_probabilities(probs)
        
        # Negatives should be set to 0
        assert normalized[0] >= 0
        assert np.allclose(np.sum(normalized), 1.0)
    
    def test_normalize_empty(self):
        """Test normalization of empty array"""
        probs = []
        normalized = normalize_probabilities(probs)
        
        assert len(normalized) == 0


class TestEnsureProbabilityBounds:
    """Test probability bounding"""
    
    def test_valid_probability(self):
        """Test valid probability remains unchanged"""
        assert ensure_probability_bounds(0.5) == 0.5
    
    def test_below_zero(self):
        """Test negative probability is bounded"""
        result = ensure_probability_bounds(-0.1)
        assert result > 0
        assert result < 0.01  # epsilon
    
    def test_above_one(self):
        """Test probability > 1 is bounded"""
        result = ensure_probability_bounds(1.5)
        assert result < 1
        assert result > 0.99  # 1 - epsilon
    
    def test_exact_bounds(self):
        """Test exact 0 and 1 are adjusted"""
        assert ensure_probability_bounds(0) > 0
        assert ensure_probability_bounds(1) < 1


class TestBinaryProbabilities:
    """Test binary probability normalization"""
    
    def test_valid_probability(self):
        """Test valid success probability"""
        fail_prob, success_prob = normalize_binary_probabilities(0.7)
        
        assert np.allclose(fail_prob + success_prob, 1.0)
        assert np.allclose(success_prob, 0.7, atol=0.01)
    
    def test_extreme_values(self):
        """Test extreme probabilities"""
        # Very low
        fail_prob, success_prob = normalize_binary_probabilities(0.001)
        assert fail_prob + success_prob == 1.0
        
        # Very high
        fail_prob, success_prob = normalize_binary_probabilities(0.999)
        assert fail_prob + success_prob == 1.0


class TestWeightedCombination:
    """Test weighted probability combination"""
    
    def test_equal_weights(self):
        """Test combination with equal weights"""
        probs = [0.2, 0.4, 0.6]
        weights = [1, 1, 1]
        
        result = weighted_probability_combination(probs, weights)
        assert np.allclose(result, 0.4)  # Average
    
    def test_different_weights(self):
        """Test combination with different weights"""
        probs = [0.2, 0.8]
        weights = [0.3, 0.7]
        
        result = weighted_probability_combination(probs, weights)
        expected = 0.2 * 0.3 + 0.8 * 0.7  # 0.62
        assert np.allclose(result, expected)
    
    def test_zero_weights(self):
        """Test with zero weights"""
        probs = [0.2, 0.8, 0.5]
        weights = [0, 1, 0]
        
        result = weighted_probability_combination(probs, weights)
        assert np.allclose(result, 0.8)
    
    def test_empty_inputs(self):
        """Test empty inputs"""
        result = weighted_probability_combination([], [])
        assert result == 0.5  # Default


class TestEnsembleProbabilities:
    """Test ensemble probability methods"""
    
    def test_weighted_average(self):
        """Test weighted average ensemble"""
        model_probs = {
            'model1': 0.3,
            'model2': 0.6,
            'model3': 0.9
        }
        model_weights = {
            'model1': 1,
            'model2': 2,
            'model3': 1
        }
        
        result = ensemble_probabilities(model_probs, model_weights, method='weighted_average')
        expected = (0.3 * 1 + 0.6 * 2 + 0.9 * 1) / 4
        assert np.allclose(result, expected)
    
    def test_geometric_mean(self):
        """Test geometric mean ensemble"""
        model_probs = {
            'model1': 0.4,
            'model2': 0.6
        }
        
        result = ensemble_probabilities(model_probs, method='geometric_mean')
        expected = np.sqrt(0.4 * 0.6)
        assert np.allclose(result, expected, atol=0.01)
    
    def test_harmonic_mean(self):
        """Test harmonic mean ensemble"""
        model_probs = {
            'model1': 0.4,
            'model2': 0.6
        }
        
        result = ensemble_probabilities(model_probs, method='harmonic_mean')
        expected = 2 / (1/0.4 + 1/0.6)
        assert np.allclose(result, expected, atol=0.01)


class TestCalibration:
    """Test probability calibration"""
    
    def test_platt_calibration(self):
        """Test Platt scaling calibration"""
        # Neutral calibration
        assert np.allclose(calibrate_probability(0.5, 1.0, 'platt'), 0.5)
        
        # Stronger calibration
        result = calibrate_probability(0.7, 2.0, 'platt')
        assert result > 0.7  # Should push away from 0.5
    
    def test_beta_calibration(self):
        """Test beta calibration"""
        # Power < 1 flattens
        result = calibrate_probability(0.8, 0.5, 'beta')
        assert result < 0.8
        
        # Power > 1 sharpens
        result = calibrate_probability(0.8, 2.0, 'beta')
        assert result < 0.8  # 0.8^2 = 0.64


class TestConfidenceInterval:
    """Test confidence interval calculation"""
    
    def test_basic_interval(self):
        """Test basic confidence interval"""
        lower, upper = confidence_interval_from_probability(0.7, n_samples=100)
        
        assert lower < 0.7
        assert upper > 0.7
        assert lower < upper
    
    def test_sample_size_effect(self):
        """Test effect of sample size"""
        # Smaller sample = wider interval
        lower1, upper1 = confidence_interval_from_probability(0.5, n_samples=10)
        lower2, upper2 = confidence_interval_from_probability(0.5, n_samples=1000)
        
        interval1 = upper1 - lower1
        interval2 = upper2 - lower2
        
        assert interval1 > interval2


class TestSafeDivision:
    """Test safe probability division"""
    
    def test_normal_division(self):
        """Test normal division"""
        result = safe_probability_division(0.3, 0.6)
        assert np.allclose(result, 0.5)
    
    def test_division_by_zero(self):
        """Test division by zero"""
        result = safe_probability_division(0.3, 0.0, default=0.7)
        assert result == 0.7
    
    def test_nan_handling(self):
        """Test NaN handling"""
        result = safe_probability_division(np.nan, 0.5)
        assert result == 0.5  # Default
        
        result = safe_probability_division(0.5, np.nan)
        assert result == 0.5  # Default
    
    def test_infinity_handling(self):
        """Test infinity handling"""
        result = safe_probability_division(np.inf, 1.0)
        assert 0 <= result <= 1  # Should be bounded


if __name__ == "__main__":
    pytest.main([__file__, "-v"])