"""
Safe Math Operations
Provides division by zero protection and numerical stability
"""

import numpy as np
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)

# Numerical constants
EPSILON = 1e-10
LARGE_NUMBER = 1e10


def safe_divide(
    numerator: Union[float, np.ndarray],
    denominator: Union[float, np.ndarray],
    default: Union[float, np.ndarray] = 0.0,
    epsilon: float = EPSILON
) -> Union[float, np.ndarray]:
    """
    Safely divide two numbers, handling division by zero
    
    Args:
        numerator: The numerator
        denominator: The denominator
        default: Value to return if division fails
        epsilon: Small value to prevent exact division by zero
        
    Returns:
        Result of division or default value
    """
    try:
        # Handle scalar division
        if np.isscalar(numerator) and np.isscalar(denominator):
            if abs(denominator) < epsilon:
                logger.warning(f"Division by near-zero: {numerator} / {denominator}")
                return default
            return numerator / denominator
        
        # Handle array division
        denominator = np.asarray(denominator)
        numerator = np.asarray(numerator)
        
        # Create mask for safe denominators
        safe_mask = np.abs(denominator) >= epsilon
        
        # Initialize result with default values
        result = np.full_like(numerator, default, dtype=np.float64)
        
        # Perform division only where safe
        if np.any(safe_mask):
            result[safe_mask] = numerator[safe_mask] / denominator[safe_mask]
        
        return result
        
    except Exception as e:
        logger.error(f"Division error: {e}")
        return default


def safe_log(
    x: Union[float, np.ndarray],
    base: Optional[float] = None,
    epsilon: float = EPSILON
) -> Union[float, np.ndarray]:
    """
    Safely compute logarithm, handling zero and negative values
    
    Args:
        x: Input value(s)
        base: Logarithm base (None for natural log)
        epsilon: Small value to prevent log(0)
        
    Returns:
        Logarithm result
    """
    # Ensure positive values
    x_safe = np.maximum(x, epsilon)
    
    if base is None:
        return np.log(x_safe)
    else:
        return np.log(x_safe) / np.log(base)


def safe_sqrt(
    x: Union[float, np.ndarray],
    epsilon: float = 0.0
) -> Union[float, np.ndarray]:
    """
    Safely compute square root, handling negative values
    
    Args:
        x: Input value(s)
        epsilon: Minimum value before sqrt
        
    Returns:
        Square root result
    """
    return np.sqrt(np.maximum(x, epsilon))


def safe_exp(
    x: Union[float, np.ndarray],
    max_value: float = 100.0
) -> Union[float, np.ndarray]:
    """
    Safely compute exponential, preventing overflow
    
    Args:
        x: Input value(s)
        max_value: Maximum input value to prevent overflow
        
    Returns:
        Exponential result
    """
    x_clipped = np.clip(x, -max_value, max_value)
    return np.exp(x_clipped)


def safe_sigmoid(
    x: Union[float, np.ndarray],
    epsilon: float = EPSILON
) -> Union[float, np.ndarray]:
    """
    Safely compute sigmoid function
    
    Args:
        x: Input value(s)
        epsilon: Small value for numerical stability
        
    Returns:
        Sigmoid result bounded in (epsilon, 1-epsilon)
    """
    # Prevent overflow in exp
    x_clipped = np.clip(x, -500, 500)
    sigmoid = 1 / (1 + np.exp(-x_clipped))
    
    # Ensure bounds
    return np.clip(sigmoid, epsilon, 1 - epsilon)


def safe_ratio(
    value1: float,
    value2: float,
    max_ratio: float = 1000.0,
    min_ratio: float = 0.001
) -> float:
    """
    Compute ratio with bounds to prevent extreme values
    
    Args:
        value1: Numerator
        value2: Denominator
        max_ratio: Maximum allowed ratio
        min_ratio: Minimum allowed ratio
        
    Returns:
        Bounded ratio
    """
    ratio = safe_divide(value1, value2, default=1.0)
    return np.clip(ratio, min_ratio, max_ratio)


def safe_percentage(
    part: float,
    whole: float,
    default: float = 0.0
) -> float:
    """
    Calculate percentage safely
    
    Args:
        part: The part value
        whole: The whole value
        default: Default percentage if calculation fails
        
    Returns:
        Percentage (0-100)
    """
    if whole == 0:
        return default
    
    percentage = safe_divide(part * 100, whole, default=default)
    return np.clip(percentage, 0, 100)


def safe_mean(
    values: Union[list, np.ndarray],
    default: float = 0.0,
    ignore_nan: bool = True
) -> float:
    """
    Calculate mean safely, handling empty arrays and NaN values
    
    Args:
        values: Array of values
        default: Default value if mean cannot be calculated
        ignore_nan: Whether to ignore NaN values
        
    Returns:
        Mean value or default
    """
    if len(values) == 0:
        return default
    
    values = np.asarray(values)
    
    if ignore_nan:
        valid_values = values[~np.isnan(values)]
        if len(valid_values) == 0:
            return default
        return np.mean(valid_values)
    else:
        if np.any(np.isnan(values)):
            return default
        return np.mean(values)


def safe_weighted_average(
    values: Union[list, np.ndarray],
    weights: Union[list, np.ndarray],
    default: float = 0.0
) -> float:
    """
    Calculate weighted average safely
    
    Args:
        values: Array of values
        weights: Array of weights
        default: Default value if calculation fails
        
    Returns:
        Weighted average or default
    """
    if len(values) == 0 or len(weights) == 0:
        return default
    
    if len(values) != len(weights):
        logger.error(f"Values and weights length mismatch: {len(values)} vs {len(weights)}")
        return default
    
    values = np.asarray(values)
    weights = np.asarray(weights)
    
    # Remove NaN values
    valid_mask = ~(np.isnan(values) | np.isnan(weights))
    if not np.any(valid_mask):
        return default
    
    valid_values = values[valid_mask]
    valid_weights = weights[valid_mask]
    
    # Normalize weights
    weight_sum = np.sum(valid_weights)
    if weight_sum == 0:
        return default
    
    return np.sum(valid_values * valid_weights) / weight_sum


def clip_value(
    value: Union[float, np.ndarray],
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> Union[float, np.ndarray]:
    """
    Clip value to specified bounds
    
    Args:
        value: Value to clip
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Clipped value
    """
    if min_value is not None and max_value is not None:
        return np.clip(value, min_value, max_value)
    elif min_value is not None:
        return np.maximum(value, min_value)
    elif max_value is not None:
        return np.minimum(value, max_value)
    else:
        return value