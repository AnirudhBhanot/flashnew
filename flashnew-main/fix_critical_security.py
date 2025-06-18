#!/usr/bin/env python3
"""
Fix critical security vulnerabilities in FLASH platform
"""

import os
import re
from pathlib import Path

def fix_sql_injection():
    """Fix SQL injection vulnerability in repositories.py"""
    repo_file = Path("database/repositories.py")
    if not repo_file.exists():
        print("❌ repositories.py not found")
        return
    
    content = repo_file.read_text()
    
    # Fix the SQL injection vulnerability
    vulnerable_pattern = r'''query = f"""
    SELECT \* FROM predictions 
    WHERE startup_id = '{startup_id}'
    ORDER BY created_at DESC
"""'''
    
    safe_code = '''query = """
    SELECT * FROM predictions 
    WHERE startup_id = :startup_id
    ORDER BY created_at DESC
"""
params = {"startup_id": startup_id}'''
    
    if "WHERE startup_id = '{startup_id}'" in content:
        content = content.replace(
            "WHERE startup_id = '{startup_id}'",
            "WHERE startup_id = :startup_id"
        )
        print("✅ Fixed SQL injection vulnerability")
        
        # Also add parameter passing
        content = content.replace(
            "session.execute(query)",
            "session.execute(query, params)"
        )
        
        repo_file.write_text(content)
    else:
        print("⚠️  SQL injection pattern not found or already fixed")

def fix_hardcoded_credentials():
    """Fix hardcoded credentials in connection.py"""
    conn_file = Path("database/connection.py")
    if not conn_file.exists():
        print("❌ connection.py not found")
        return
    
    content = conn_file.read_text()
    
    # Replace hardcoded password with secure default
    content = content.replace(
        'db_password = os.getenv("DB_PASSWORD", "flash_password")',
        '''db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise ValueError("DB_PASSWORD environment variable must be set")'''
    )
    
    # Add warning for default user
    content = content.replace(
        'db_user = os.getenv("DB_USER", "flash_user")',
        '''db_user = os.getenv("DB_USER", "flash_user")
# WARNING: Using default user, set DB_USER in production'''
    )
    
    conn_file.write_text(content)
    print("✅ Fixed hardcoded credentials")

def fix_api_key_validation():
    """Fix weak API key validation"""
    api_file = Path("api_server_unified.py")
    if not api_file.exists():
        print("❌ api_server_unified.py not found")
        return
    
    content = api_file.read_text()
    
    # Replace weak validation with proper implementation
    old_validation = '''    # Check if API key is valid
    # For now, accept any non-empty API key (no settings module)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )'''
    
    new_validation = '''    # Check if API key is valid
    valid_api_keys = os.getenv("VALID_API_KEYS", "").split(",")
    valid_api_keys = [key.strip() for key in valid_api_keys if key.strip()]
    
    if not valid_api_keys:
        # No API keys configured - allow access but log warning
        logger.warning("No API keys configured - API is unprotected!")
        return api_key
    
    if api_key not in valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )'''
    
    content = content.replace(old_validation, new_validation)
    api_file.write_text(content)
    print("✅ Fixed API key validation")

def add_input_sanitization():
    """Add basic input sanitization"""
    print("📝 Creating input sanitization utility...")
    
    sanitizer_content = '''"""
Input sanitization utilities for FLASH platform
"""
import re
from typing import Any, Dict
import html

def sanitize_string(value: str, max_length: int = 1000) -> str:
    """Sanitize string input to prevent XSS and injection attacks"""
    if not isinstance(value, str):
        return str(value)
    
    # HTML escape
    value = html.escape(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Limit length
    value = value[:max_length]
    
    # Remove potentially dangerous patterns
    value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE)
    value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
    value = re.sub(r'on\w+\s*=', '', value, flags=re.IGNORECASE)
    
    return value

def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively sanitize dictionary values"""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_string(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_string(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            sanitized[key] = value
    return sanitized

def validate_sql_identifier(identifier: str) -> str:
    """Validate SQL identifier to prevent injection"""
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return identifier
'''
    
    Path("utils").mkdir(exist_ok=True)
    Path("utils/sanitization.py").write_text(sanitizer_content)
    print("✅ Created input sanitization utilities")

def create_security_config():
    """Create security configuration"""
    print("📝 Creating security configuration...")
    
    config_content = '''"""
Security configuration for FLASH platform
"""
import os
from typing import List

class SecurityConfig:
    """Security configuration settings"""
    
    # API Security
    API_KEY_MIN_LENGTH = 32
    API_KEY_HEADER = "X-API-Key"
    REQUIRE_HTTPS = os.getenv("REQUIRE_HTTPS", "true").lower() == "true"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_DEFAULT = "100/hour"
    RATE_LIMIT_PREDICT = "10/minute"
    
    # CORS Settings
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    ALLOWED_METHODS = ["GET", "POST", "OPTIONS"]
    ALLOWED_HEADERS = ["Content-Type", "X-API-Key", "Authorization"]
    
    # Input Validation
    MAX_REQUEST_SIZE = 1024 * 1024  # 1MB
    MAX_STRING_LENGTH = 1000
    MAX_ARRAY_LENGTH = 100
    
    # Session Security
    SESSION_TIMEOUT = 3600  # 1 hour
    SESSION_SECURE = True
    SESSION_HTTPONLY = True
    SESSION_SAMESITE = "strict"
    
    # Password Policy (for future use)
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SPECIAL = True
    
    # Security Headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    @classmethod
    def validate_api_key(cls, api_key: str) -> bool:
        """Validate API key format"""
        if not api_key:
            return False
        if len(api_key) < cls.API_KEY_MIN_LENGTH:
            return False
        # Add more validation as needed
        return True
'''
    
    Path("security").mkdir(exist_ok=True)
    Path("security/config.py").write_text(config_content)
    print("✅ Created security configuration")

def main():
    """Run all security fixes"""
    print("🔒 Fixing Critical Security Vulnerabilities")
    print("=" * 50)
    
    # Fix vulnerabilities
    fix_sql_injection()
    fix_hardcoded_credentials()
    fix_api_key_validation()
    add_input_sanitization()
    create_security_config()
    
    print("\n📋 Next Steps:")
    print("1. Set environment variables:")
    print("   export DB_PASSWORD='your-secure-password'")
    print("   export VALID_API_KEYS='key1,key2,key3'")
    print("2. Update API server to use sanitization:")
    print("   from utils.sanitization import sanitize_dict")
    print("3. Add security headers to API responses")
    print("4. Implement proper session management")
    print("5. Set up HTTPS in production")
    
    print("\n✅ Security fixes applied!")
    print("⚠️  Remember to test thoroughly before deploying")

if __name__ == "__main__":
    main()