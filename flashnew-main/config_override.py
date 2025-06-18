"""
Configuration override for testing without database
"""
import os

# Override database password requirement for testing
os.environ["DB_PASSWORD"] = "test_password_123"
os.environ["ENVIRONMENT"] = "development"
os.environ["API_KEYS"] = ""  # Empty for development