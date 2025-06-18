"""
Input sanitization utilities for FLASH platform
Prevents XSS, SQL injection, and other security vulnerabilities
"""
import re
import html
from typing import Any, Dict, List, Union
import logging

logger = logging.getLogger(__name__)

# Maximum lengths for different field types
MAX_LENGTHS = {
    "default": 1000,
    "name": 200,
    "email": 254,
    "url": 2048,
    "description": 5000,
    "short_text": 100,
}

# Dangerous patterns to remove
DANGEROUS_PATTERNS = [
    (r'<script[^>]*>.*?</script>', ''),  # Script tags
    (r'javascript:', ''),                 # JavaScript protocol
    (r'on\w+\s*=', ''),                  # Event handlers
    (r'<iframe[^>]*>.*?</iframe>', ''),  # Iframes
    (r'<object[^>]*>.*?</object>', ''),  # Objects
    (r'<embed[^>]*>', ''),               # Embeds
    (r'<!--.*?-->', ''),                 # HTML comments
]


def sanitize_string(
    value: str, 
    field_type: str = "default",
    max_length: int = None,
    allow_html: bool = False
) -> str:
    """
    Sanitize string input to prevent XSS and injection attacks
    
    Args:
        value: String to sanitize
        field_type: Type of field for specific rules
        max_length: Maximum allowed length (overrides field_type default)
        allow_html: Whether to allow safe HTML tags
    
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return str(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Trim whitespace
    value = value.strip()
    
    # Apply HTML escaping unless HTML is allowed
    if not allow_html:
        value = html.escape(value)
    
    # Remove dangerous patterns
    for pattern, replacement in DANGEROUS_PATTERNS:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE | re.DOTALL)
    
    # Apply length limit
    if max_length is None:
        max_length = MAX_LENGTHS.get(field_type, MAX_LENGTHS["default"])
    value = value[:max_length]
    
    # Field-specific sanitization
    if field_type == "email":
        # Basic email sanitization
        value = value.lower()
        value = re.sub(r'[^a-z0-9@._+-]', '', value)
    elif field_type == "url":
        # URL sanitization
        if not value.startswith(('http://', 'https://')):
            value = ''  # Reject non-HTTP(S) URLs
    elif field_type == "name":
        # Name sanitization - allow letters, spaces, hyphens, apostrophes
        value = re.sub(r'[^a-zA-Z0-9\s\-\']', '', value)
    
    return value


def sanitize_number(value: Any, min_val: float = None, max_val: float = None) -> float:
    """
    Sanitize numeric input
    
    Args:
        value: Value to sanitize
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Sanitized float value
    """
    try:
        num = float(value)
        
        # Check for special values
        if not (-1e308 < num < 1e308):  # Avoid infinity
            raise ValueError("Number out of range")
        
        # Apply bounds
        if min_val is not None:
            num = max(num, min_val)
        if max_val is not None:
            num = min(num, max_val)
        
        return num
    except (ValueError, TypeError):
        logger.warning(f"Invalid numeric value: {value}")
        return 0.0


def sanitize_boolean(value: Any) -> bool:
    """Sanitize boolean input"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return bool(value)


def sanitize_list(
    values: List[Any], 
    max_items: int = 100,
    sanitizer_func: callable = sanitize_string
) -> List[Any]:
    """
    Sanitize list input
    
    Args:
        values: List to sanitize
        max_items: Maximum number of items allowed
        sanitizer_func: Function to sanitize each item
    
    Returns:
        Sanitized list
    """
    if not isinstance(values, list):
        return []
    
    # Limit number of items
    values = values[:max_items]
    
    # Sanitize each item
    return [sanitizer_func(item) for item in values]


def sanitize_dict(
    data: Dict[str, Any],
    schema: Dict[str, Dict] = None,
    recursive: bool = True
) -> Dict[str, Any]:
    """
    Recursively sanitize dictionary values
    
    Args:
        data: Dictionary to sanitize
        schema: Schema defining field types and rules
        recursive: Whether to sanitize nested dictionaries
    
    Returns:
        Sanitized dictionary
    """
    if not isinstance(data, dict):
        return {}
    
    sanitized = {}
    
    for key, value in data.items():
        # Sanitize key
        clean_key = sanitize_string(key, field_type="short_text")
        
        # Get field schema if available
        field_schema = schema.get(clean_key, {}) if schema else {}
        field_type = field_schema.get("type", "default")
        
        # Sanitize value based on type
        if value is None:
            sanitized[clean_key] = None
        elif isinstance(value, str):
            sanitized[clean_key] = sanitize_string(
                value, 
                field_type=field_type,
                max_length=field_schema.get("max_length")
            )
        elif isinstance(value, (int, float)):
            sanitized[clean_key] = sanitize_number(
                value,
                min_val=field_schema.get("min"),
                max_val=field_schema.get("max")
            )
        elif isinstance(value, bool):
            sanitized[clean_key] = sanitize_boolean(value)
        elif isinstance(value, list):
            sanitized[clean_key] = sanitize_list(
                value,
                max_items=field_schema.get("max_items", 100)
            )
        elif isinstance(value, dict) and recursive:
            sanitized[clean_key] = sanitize_dict(
                value,
                schema=field_schema.get("properties") if schema else None,
                recursive=recursive
            )
        else:
            # For other types, convert to string and sanitize
            sanitized[clean_key] = sanitize_string(str(value))
    
    return sanitized


def validate_sql_identifier(identifier: str) -> str:
    """
    Validate SQL identifier to prevent injection
    Only allows alphanumeric characters and underscores
    """
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return identifier


def sanitize_startup_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize startup data specifically for FLASH platform
    """
    schema = {
        "startup_name": {"type": "name", "max_length": 200},
        "funding_stage": {"type": "short_text", "max_length": 50},
        "sector": {"type": "short_text", "max_length": 100},
        "product_stage": {"type": "short_text", "max_length": 50},
        "investor_tier_primary": {"type": "short_text", "max_length": 50},
        "hq_location": {"type": "short_text", "max_length": 100},
        
        # Numeric fields with bounds
        "total_capital_raised_usd": {"type": "number", "min": 0, "max": 1e12},
        "monthly_burn_usd": {"type": "number", "min": 0, "max": 1e9},
        "runway_months": {"type": "number", "min": 0, "max": 1000},
        "team_size_full_time": {"type": "number", "min": 0, "max": 100000},
        "founders_count": {"type": "number", "min": 0, "max": 100},
        
        # Score fields (1-5 range)
        "tech_differentiation_score": {"type": "number", "min": 1, "max": 5},
        "switching_cost_score": {"type": "number", "min": 1, "max": 5},
        "brand_strength_score": {"type": "number", "min": 1, "max": 5},
        "scalability_score": {"type": "number", "min": 1, "max": 5},
        "board_advisor_experience_score": {"type": "number", "min": 1, "max": 5},
        "competition_intensity": {"type": "number", "min": 1, "max": 5},
        
        # Percentage fields (0-100 range)
        "market_growth_rate_percent": {"type": "number", "min": -100, "max": 1000},
        "revenue_growth_rate_percent": {"type": "number", "min": -100, "max": 10000},
        "gross_margin_percent": {"type": "number", "min": -100, "max": 100},
        "team_diversity_percent": {"type": "number", "min": 0, "max": 100},
        
        # Ratio fields (0-1 range)
        "product_retention_30d": {"type": "number", "min": 0, "max": 1},
        "product_retention_90d": {"type": "number", "min": 0, "max": 1},
        "dau_mau_ratio": {"type": "number", "min": 0, "max": 1},
    }
    
    return sanitize_dict(data, schema=schema)


# Middleware function for FastAPI
async def sanitize_request_data(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Middleware function to sanitize incoming request data
    """
    try:
        # Log original data size
        original_size = len(str(request_data))
        
        # Sanitize the data
        sanitized_data = sanitize_startup_data(request_data)
        
        # Log if data was modified
        sanitized_size = len(str(sanitized_data))
        if original_size != sanitized_size:
            logger.info(f"Sanitized request data: {original_size} -> {sanitized_size} bytes")
        
        return sanitized_data
    except Exception as e:
        logger.error(f"Error sanitizing request data: {e}")
        raise ValueError("Invalid request data format")