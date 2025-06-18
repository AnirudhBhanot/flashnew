"""
Probability Utilities
Ensures all probability calculations are properly normalized and bounded
"""

import numpy as np
from typing import List, Dict, Union, Tuple
import logging

logger = logging.getLogger(__name__)


def normalize_probabilities(probs: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Normalize probabilities to sum to 1.0
    
    Args:
        probs: List or array of probabilities
        
    Returns:
        Normalized probability array
    """
    probs = np.array(probs, dtype=np.float64)
    
    # Handle edge cases
    if len(probs) == 0:
        return probs
    
    # Ensure non-negative
    probs = np.maximum(probs, 0)
    
    # Check if all zeros
    total = np.sum(probs)
    if total == 0:
        # Uniform distribution if all zeros
        return np.ones_like(probs) / len(probs)
    
    # Normalize
    normalized = probs / total
    
    # Ensure exact sum due to floating point errors
    normalized = normalized / np.sum(normalized)
    
    return normalized


def ensure_probability_bounds(prob: float, epsilon: float = 1e-7) -> float:
    """
    Ensure probability is within [0, 1] bounds with small epsilon for numerical stability
    
    Args:
        prob: Probability value
        epsilon: Small value to avoid exact 0 or 1
        
    Returns:
        Bounded probability
    """
    return np.clip(prob, epsilon, 1 - epsilon)


def normalize_binary_probabilities(prob_success: float) -> Tuple[float, float]:
    """
    Normalize binary probabilities [failure, success] to sum to 1
    
    Args:
        prob_success: Success probability
        
    Returns:
        Tuple of (prob_failure, prob_success) that sum to 1
    """
    prob_success = ensure_probability_bounds(prob_success)
    prob_failure = 1.0 - prob_success
    
    # Normalize to handle floating point errors
    probs = normalize_probabilities([prob_failure, prob_success])
    
    return float(probs[0]), float(probs[1])


def weighted_probability_combination(
    probabilities: List[float], 
    weights: List[float],
    normalize_weights: bool = True
) -> float:
    """
    Combine multiple probabilities with weights
    
    Args:
        probabilities: List of probabilities
        weights: List of weights
        normalize_weights: Whether to normalize weights to sum to 1
        
    Returns:
        Combined probability
    """
    if len(probabilities) != len(weights):
        raise ValueError("Probabilities and weights must have same length")
    
    if len(probabilities) == 0:
        return 0.5
    
    # Ensure probabilities are bounded
    probabilities = [ensure_probability_bounds(p) for p in probabilities]
    
    # Normalize weights if requested
    if normalize_weights:
        weights = normalize_probabilities(weights)
    
    # Weighted average
    combined = np.sum(np.array(probabilities) * np.array(weights))
    
    # Ensure result is bounded
    return ensure_probability_bounds(combined)


def ensemble_probabilities(
    model_probs: Dict[str, float],
    model_weights: Dict[str, float] = None,
    method: str = "weighted_average"
) -> float:
    """
    Ensemble multiple model probabilities
    
    Args:
        model_probs: Dictionary of model_name -> probability
        model_weights: Optional weights for each model
        method: Ensemble method ('weighted_average', 'geometric_mean', 'harmonic_mean')
        
    Returns:
        Ensembled probability
    """
    if not model_probs:
        return 0.5
    
    probs = list(model_probs.values())
    
    # Default equal weights
    if model_weights is None:
        weights = [1.0] * len(probs)
    else:
        # Ensure all models have weights
        weights = [model_weights.get(name, 1.0) for name in model_probs.keys()]
    
    if method == "weighted_average":
        return weighted_probability_combination(probs, weights)
    
    elif method == "geometric_mean":
        # Geometric mean with weights
        weights = normalize_probabilities(weights)
        log_probs = np.log(np.maximum(probs, 1e-10))  # Avoid log(0)
        geometric_mean = np.exp(np.sum(log_probs * weights))
        return ensure_probability_bounds(geometric_mean)
    
    elif method == "harmonic_mean":
        # Harmonic mean with weights
        weights = normalize_probabilities(weights)
        reciprocals = 1.0 / np.maximum(probs, 1e-10)  # Avoid division by 0
        harmonic_mean = 1.0 / np.sum(reciprocals * weights)
        return ensure_probability_bounds(harmonic_mean)
    
    else:
        raise ValueError(f"Unknown ensemble method: {method}")


def calibrate_probability(
    prob: float,
    calibration_factor: float = 1.0,
    method: str = "platt"
) -> float:
    """
    Calibrate probability to be more accurate
    
    Args:
        prob: Raw probability
        calibration_factor: Calibration parameter
        method: Calibration method ('platt', 'isotonic', 'beta')
        
    Returns:
        Calibrated probability
    """
    prob = ensure_probability_bounds(prob)
    
    if method == "platt":
        # Platt scaling: sigmoid(a*logit(p) + b)
        # Simplified version with single parameter
        logit = np.log(prob / (1 - prob + 1e-10))
        calibrated_logit = calibration_factor * logit
        calibrated = 1 / (1 + np.exp(-calibrated_logit))
        
    elif method == "beta":
        # Beta calibration
        # Map probability through beta CDF
        calibrated = prob ** calibration_factor
        
    else:
        calibrated = prob
    
    return ensure_probability_bounds(calibrated)


def confidence_interval_from_probability(
    prob: float,
    n_samples: int = 100,
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval for a probability estimate
    
    Args:
        prob: Probability estimate
        n_samples: Number of samples (affects interval width)
        confidence_level: Confidence level (e.g., 0.95 for 95%)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    prob = ensure_probability_bounds(prob)
    
    # Wilson score interval
    z = 1.96 if confidence_level == 0.95 else 2.58  # z-score
    
    denominator = 1 + z**2 / n_samples
    center = (prob + z**2 / (2 * n_samples)) / denominator
    
    margin = z * np.sqrt(prob * (1 - prob) / n_samples + z**2 / (4 * n_samples**2)) / denominator
    
    lower = ensure_probability_bounds(center - margin)
    upper = ensure_probability_bounds(center + margin)
    
    return lower, upper


def safe_probability_division(
    numerator: float,
    denominator: float,
    default: float = 0.5
) -> float:
    """
    Safely divide to get probability, handling division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division fails
        
    Returns:
        Probability result
    """
    if denominator == 0 or np.isnan(denominator) or np.isnan(numerator):
        logger.warning(f"Invalid division: {numerator} / {denominator}, using default {default}")
        return default
    
    result = numerator / denominator
    
    # Ensure valid probability
    if np.isnan(result) or np.isinf(result):
        return default
    
    return ensure_probability_bounds(result)