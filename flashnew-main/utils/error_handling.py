"""
Comprehensive error handling for FLASH platform
Provides centralized error management and recovery
"""
import logging
import traceback
import sys
from typing import Any, Dict, Optional, Union
from datetime import datetime
from functools import wraps
import asyncio

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import numpy as np

logger = logging.getLogger(__name__)


class FlashError(Exception):
    """Base exception class for FLASH platform"""
    def __init__(self, message: str, code: str = None, details: Dict = None):
        super().__init__(message)
        self.code = code or "FLASH_ERROR"
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()


class DataValidationError(FlashError):
    """Raised when input data validation fails"""
    def __init__(self, message: str, field: str = None, details: Dict = None):
        super().__init__(message, "DATA_VALIDATION_ERROR", details)
        self.field = field


class ModelError(FlashError):
    """Raised when model prediction fails"""
    def __init__(self, message: str, model_name: str = None, details: Dict = None):
        super().__init__(message, "MODEL_ERROR", details)
        self.model_name = model_name


class FeatureError(FlashError):
    """Raised when feature processing fails"""
    def __init__(self, message: str, feature_name: str = None, details: Dict = None):
        super().__init__(message, "FEATURE_ERROR", details)
        self.feature_name = feature_name


class DatabaseError(FlashError):
    """Raised when database operations fail"""
    def __init__(self, message: str, operation: str = None, details: Dict = None):
        super().__init__(message, "DATABASE_ERROR", details)
        self.operation = operation


class SecurityError(FlashError):
    """Raised when security checks fail"""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, "SECURITY_ERROR", details)


def handle_prediction_errors(func):
    """Decorator to handle errors in prediction functions"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return handle_error(e)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handle_error(e)
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def handle_error(error: Exception) -> Dict[str, Any]:
    """Convert exception to error response"""
    # Log the full error
    logger.error(f"Error occurred: {type(error).__name__}: {str(error)}")
    logger.debug(traceback.format_exc())
    
    # Determine error type and response
    if isinstance(error, ValidationError):
        return {
            "success": False,
            "error": "Validation Error",
            "message": "Invalid input data format",
            "details": error.errors(),
            "code": "VALIDATION_ERROR"
        }
    elif isinstance(error, FlashError):
        return {
            "success": False,
            "error": error.__class__.__name__,
            "message": str(error),
            "code": error.code,
            "details": error.details,
            "timestamp": error.timestamp
        }
    elif isinstance(error, ValueError):
        return {
            "success": False,
            "error": "Value Error",
            "message": str(error),
            "code": "VALUE_ERROR"
        }
    elif isinstance(error, KeyError):
        return {
            "success": False,
            "error": "Missing Required Field",
            "message": f"Required field not found: {str(error)}",
            "code": "MISSING_FIELD"
        }
    elif isinstance(error, TypeError):
        return {
            "success": False,
            "error": "Type Error",
            "message": "Invalid data type provided",
            "code": "TYPE_ERROR",
            "details": {"error": str(error)}
        }
    else:
        # Generic error
        return {
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "code": "INTERNAL_ERROR",
            "details": {"type": type(error).__name__}
        }


async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler for FastAPI"""
    error_response = handle_error(exc)
    
    # Determine status code
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, ValidationError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(exc, DataValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, SecurityError):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, HTTPException):
        status_code = exc.status_code
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


def validate_numeric_value(
    value: Any,
    min_val: float = None,
    max_val: float = None,
    field_name: str = "value"
) -> float:
    """Validate and convert numeric value with bounds checking"""
    try:
        num_value = float(value)
        
        # Check for NaN or infinity
        if np.isnan(num_value) or np.isinf(num_value):
            raise DataValidationError(
                f"{field_name} contains invalid numeric value (NaN or Inf)",
                field=field_name
            )
        
        # Check bounds
        if min_val is not None and num_value < min_val:
            raise DataValidationError(
                f"{field_name} value {num_value} is below minimum {min_val}",
                field=field_name
            )
        
        if max_val is not None and num_value > max_val:
            raise DataValidationError(
                f"{field_name} value {num_value} is above maximum {max_val}",
                field=field_name
            )
        
        return num_value
        
    except (ValueError, TypeError) as e:
        raise DataValidationError(
            f"{field_name} must be a valid number",
            field=field_name,
            details={"value": str(value), "error": str(e)}
        )


def validate_probability(value: Any, field_name: str = "probability") -> float:
    """Validate probability value (0-1 range)"""
    return validate_numeric_value(value, min_val=0.0, max_val=1.0, field_name=field_name)


def validate_percentage(value: Any, field_name: str = "percentage") -> float:
    """Validate percentage value (-100 to unlimited)"""
    return validate_numeric_value(value, min_val=-100.0, field_name=field_name)


def validate_score(value: Any, field_name: str = "score") -> int:
    """Validate score value (1-5 range)"""
    num_value = validate_numeric_value(value, min_val=1.0, max_val=5.0, field_name=field_name)
    return int(round(num_value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers"""
    try:
        if abs(denominator) < 1e-10:
            logger.warning(f"Division by near-zero: {numerator} / {denominator}")
            return default
        return numerator / denominator
    except Exception as e:
        logger.error(f"Division error: {e}")
        return default


def safe_log(value: float, base: float = None, default: float = 0.0) -> float:
    """Safely compute logarithm"""
    try:
        if value <= 0:
            logger.warning(f"Log of non-positive value: {value}")
            return default
        
        if base is None:
            return np.log(value)
        else:
            return np.log(value) / np.log(base)
    except Exception as e:
        logger.error(f"Log error: {e}")
        return default


def safe_sqrt(value: float, default: float = 0.0) -> float:
    """Safely compute square root"""
    try:
        if value < 0:
            logger.warning(f"Square root of negative value: {value}")
            return default
        return np.sqrt(value)
    except Exception as e:
        logger.error(f"Square root error: {e}")
        return default


class ErrorRecovery:
    """Context manager for error recovery"""
    
    def __init__(self, 
                 operation_name: str,
                 fallback_value: Any = None,
                 max_retries: int = 3,
                 retry_delay: float = 0.1):
        self.operation_name = operation_name
        self.fallback_value = fallback_value
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.attempt = 0
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
            
        self.attempt += 1
        logger.warning(
            f"Error in {self.operation_name} (attempt {self.attempt}/{self.max_retries}): "
            f"{exc_type.__name__}: {exc_val}"
        )
        
        if self.attempt < self.max_retries:
            # Retry with exponential backoff
            await asyncio.sleep(self.retry_delay * (2 ** (self.attempt - 1)))
            return True  # Suppress exception and retry
        else:
            # Max retries exceeded
            logger.error(f"Max retries exceeded for {self.operation_name}")
            return False  # Re-raise exception
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
            
        self.attempt += 1
        logger.warning(
            f"Error in {self.operation_name} (attempt {self.attempt}/{self.max_retries}): "
            f"{exc_type.__name__}: {exc_val}"
        )
        
        if self.attempt < self.max_retries:
            # For sync version, we can't retry automatically
            return False
        else:
            logger.error(f"Max retries exceeded for {self.operation_name}")
            return False


def create_error_response(
    error: Union[str, Exception],
    status_code: int = 500,
    request_id: str = None
) -> Dict[str, Any]:
    """Create standardized error response"""
    if isinstance(error, str):
        message = error
        error_type = "Error"
    else:
        message = str(error)
        error_type = type(error).__name__
    
    response = {
        "success": False,
        "error": {
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    if request_id:
        response["request_id"] = request_id
    
    return response


# Circuit breaker implementation
class CircuitBreaker:
    """Simple circuit breaker pattern implementation"""
    
    def __init__(self, 
                 name: str,
                 failure_threshold: int = 5,
                 recovery_timeout: float = 60.0,
                 expected_exception: type = Exception):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise FlashError(
                    f"Circuit breaker {self.name} is open",
                    code="CIRCUIT_BREAKER_OPEN"
                )
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        return (
            self.last_failure_time and
            (datetime.utcnow() - self.last_failure_time).total_seconds() >= self.recovery_timeout
        )
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = "closed"
        
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.error(f"Circuit breaker {self.name} opened after {self.failure_count} failures")