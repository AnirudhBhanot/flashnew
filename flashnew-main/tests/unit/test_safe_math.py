"""
Unit tests for safe math operations
"""

import pytest
import numpy as np
from utils.safe_math import (
    safe_divide,
    safe_log,
    safe_sqrt,
    safe_exp,
    safe_sigmoid,
    safe_ratio,
    safe_percentage,
    safe_mean,
    safe_weighted_average,
    clip_value
)


class TestSafeDivide:
    """Test safe division operations"""
    
    def test_normal_division(self):
        """Test normal division"""
        assert safe_divide(10, 2) == 5
        assert safe_divide(1, 3) == pytest.approx(0.333, rel=0.01)
    
    def test_division_by_zero(self):
        """Test division by zero"""
        assert safe_divide(10, 0) == 0  # Default
        assert safe_divide(10, 0, default=999) == 999
    
    def test_array_division(self):
        """Test array division"""
        numerator = np.array([10, 20, 30])
        denominator = np.array([2, 0, 5])
        
        result = safe_divide(numerator, denominator, default=-1)
        expected = np.array([5, -1, 6])
        
        assert np.allclose(result, expected)
    
    def test_near_zero_division(self):
        """Test division by very small numbers"""
        result = safe_divide(1, 1e-15, epsilon=1e-10)
        assert result == 0  # Should use default


class TestSafeLog:
    """Test safe logarithm operations"""
    
    def test_normal_log(self):
        """Test normal logarithm"""
        assert safe_log(10) == pytest.approx(np.log(10))
        assert safe_log(100, base=10) == pytest.approx(2)
    
    def test_log_zero(self):
        """Test log of zero"""
        result = safe_log(0)
        assert result == np.log(1e-10)  # Should use epsilon
    
    def test_log_negative(self):
        """Test log of negative"""
        result = safe_log(-5)
        assert result == np.log(1e-10)  # Should use epsilon
    
    def test_array_log(self):
        """Test array logarithm"""
        values = np.array([1, 0, 10, -5])
        result = safe_log(values)
        
        assert result[0] == pytest.approx(0)  # log(1) = 0
        assert result[1] > -25  # log(epsilon)
        assert result[2] == pytest.approx(np.log(10))
        assert result[3] > -25  # log(epsilon)


class TestSafeSqrt:
    """Test safe square root operations"""
    
    def test_normal_sqrt(self):
        """Test normal square root"""
        assert safe_sqrt(4) == 2
        assert safe_sqrt(9) == 3
    
    def test_sqrt_negative(self):
        """Test sqrt of negative"""
        assert safe_sqrt(-4) == 0  # Should use epsilon default
        assert safe_sqrt(-4, epsilon=1) == 1
    
    def test_array_sqrt(self):
        """Test array square root"""
        values = np.array([4, -1, 9, 0])
        result = safe_sqrt(values)
        
        assert np.allclose(result, [2, 0, 3, 0])


class TestSafeExp:
    """Test safe exponential operations"""
    
    def test_normal_exp(self):
        """Test normal exponential"""
        assert safe_exp(0) == 1
        assert safe_exp(1) == pytest.approx(np.e)
    
    def test_exp_overflow(self):
        """Test exponential overflow protection"""
        result = safe_exp(1000)  # Would overflow
        assert result == np.exp(100)  # Clipped to max
    
    def test_array_exp(self):
        """Test array exponential"""
        values = np.array([-1000, 0, 1, 1000])
        result = safe_exp(values)
        
        assert result[0] == pytest.approx(0, abs=1e-10)  # Very small
        assert result[1] == 1
        assert result[2] == pytest.approx(np.e)
        assert np.isfinite(result[3])  # Not infinity


class TestSafeSigmoid:
    """Test safe sigmoid operations"""
    
    def test_normal_sigmoid(self):
        """Test normal sigmoid"""
        assert safe_sigmoid(0) == pytest.approx(0.5)
        assert safe_sigmoid(100) > 0.99
        assert safe_sigmoid(-100) < 0.01
    
    def test_sigmoid_bounds(self):
        """Test sigmoid bounds"""
        # Should never be exactly 0 or 1
        assert safe_sigmoid(-1000) > 0
        assert safe_sigmoid(1000) < 1
    
    def test_array_sigmoid(self):
        """Test array sigmoid"""
        values = np.array([-10, 0, 10])
        result = safe_sigmoid(values)
        
        assert all(0 < r < 1 for r in result)
        assert result[1] == pytest.approx(0.5)


class TestSafeRatio:
    """Test safe ratio operations"""
    
    def test_normal_ratio(self):
        """Test normal ratio"""
        assert safe_ratio(10, 5) == 2
        assert safe_ratio(5, 10) == 0.5
    
    def test_extreme_ratios(self):
        """Test extreme ratios"""
        # Very large ratio
        assert safe_ratio(10000, 1) == 1000  # Max ratio
        
        # Very small ratio
        assert safe_ratio(1, 10000) == 0.001  # Min ratio
    
    def test_zero_denominator(self):
        """Test zero denominator"""
        assert safe_ratio(10, 0) == 1  # Default


class TestSafePercentage:
    """Test safe percentage operations"""
    
    def test_normal_percentage(self):
        """Test normal percentage"""
        assert safe_percentage(25, 100) == 25
        assert safe_percentage(1, 2) == 50
    
    def test_zero_whole(self):
        """Test zero whole"""
        assert safe_percentage(10, 0) == 0  # Default
        assert safe_percentage(10, 0, default=100) == 100
    
    def test_bounds(self):
        """Test percentage bounds"""
        assert safe_percentage(150, 100) == 100  # Clipped
        assert safe_percentage(-10, 100) == 0  # Clipped


class TestSafeMean:
    """Test safe mean operations"""
    
    def test_normal_mean(self):
        """Test normal mean"""
        assert safe_mean([1, 2, 3, 4, 5]) == 3
        assert safe_mean(np.array([10, 20, 30])) == 20
    
    def test_empty_array(self):
        """Test empty array"""
        assert safe_mean([]) == 0  # Default
        assert safe_mean([], default=999) == 999
    
    def test_nan_handling(self):
        """Test NaN handling"""
        values = [1, 2, np.nan, 4, 5]
        
        # With ignore_nan=True (default)
        assert safe_mean(values) == 3  # Mean of [1,2,4,5]
        
        # With ignore_nan=False
        assert safe_mean(values, ignore_nan=False) == 0  # Default
    
    def test_all_nan(self):
        """Test all NaN values"""
        values = [np.nan, np.nan, np.nan]
        assert safe_mean(values) == 0  # Default


class TestSafeWeightedAverage:
    """Test safe weighted average operations"""
    
    def test_normal_weighted_average(self):
        """Test normal weighted average"""
        values = [10, 20, 30]
        weights = [1, 2, 1]
        
        result = safe_weighted_average(values, weights)
        expected = (10*1 + 20*2 + 30*1) / 4
        assert result == expected
    
    def test_zero_weights(self):
        """Test all zero weights"""
        values = [10, 20, 30]
        weights = [0, 0, 0]
        
        assert safe_weighted_average(values, weights) == 0  # Default
    
    def test_length_mismatch(self):
        """Test mismatched lengths"""
        values = [10, 20, 30]
        weights = [1, 2]  # Too short
        
        assert safe_weighted_average(values, weights) == 0  # Default
    
    def test_nan_handling(self):
        """Test NaN handling"""
        values = [10, np.nan, 30]
        weights = [1, 2, 1]
        
        result = safe_weighted_average(values, weights)
        expected = (10*1 + 30*1) / 2
        assert result == expected


class TestClipValue:
    """Test value clipping"""
    
    def test_both_bounds(self):
        """Test clipping with both bounds"""
        assert clip_value(5, 0, 10) == 5
        assert clip_value(-5, 0, 10) == 0
        assert clip_value(15, 0, 10) == 10
    
    def test_min_only(self):
        """Test clipping with min only"""
        assert clip_value(5, min_value=0) == 5
        assert clip_value(-5, min_value=0) == 0
    
    def test_max_only(self):
        """Test clipping with max only"""
        assert clip_value(5, max_value=10) == 5
        assert clip_value(15, max_value=10) == 10
    
    def test_no_bounds(self):
        """Test no clipping"""
        assert clip_value(999) == 999
        assert clip_value(-999) == -999
    
    def test_array_clipping(self):
        """Test array clipping"""
        values = np.array([-5, 0, 5, 10, 15])
        result = clip_value(values, 0, 10)
        
        assert np.allclose(result, [0, 0, 5, 10, 10])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])