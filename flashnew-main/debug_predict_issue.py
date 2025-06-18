#!/usr/bin/env python3
"""
Debug script to identify the /predict endpoint validation issue
"""

import json
from pydantic import ValidationError
from api_server_unified import StartupData
from auth.jwt_auth import CurrentUser

# Test case 1: Check if StartupData expects an 'id' field
print("=== Testing StartupData Model ===")
print("Required fields:", StartupData.__fields__.keys())
print("\nChecking for 'id' field:")
if 'id' in StartupData.__fields__:
    print("  - 'id' field found in StartupData")
    print("  - Field info:", StartupData.__fields__['id'])
else:
    print("  - 'id' field NOT found in StartupData")

# Test case 2: Try to create StartupData with user data
print("\n=== Testing with User Data ===")
user_data = {
    "user_id": "test_user",
    "username": "testuser",
    "email": "test@example.com"
}

try:
    startup = StartupData(**user_data)
    print("StartupData created successfully with user data (unexpected!)")
except ValidationError as e:
    print("Validation error (expected):")
    print(json.dumps(e.errors(), indent=2))

# Test case 3: Check CurrentUser model
print("\n=== CurrentUser Model Fields ===")
print("Fields:", CurrentUser.__fields__.keys())

# Test case 4: Create valid StartupData
print("\n=== Testing Valid StartupData ===")
valid_data = {
    "total_capital_raised_usd": 1000000,
    "funding_stage": "seed",
    "sector": "saas"
}

try:
    startup = StartupData(**valid_data)
    print("Valid StartupData created successfully")
    print("Non-null fields:", sum(1 for v in startup.dict().values() if v is not None))
except ValidationError as e:
    print("Validation error:")
    print(json.dumps(e.errors(), indent=2))

# Test case 5: Check if there's field name collision
print("\n=== Checking for Field Collisions ===")
startup_fields = set(StartupData.__fields__.keys())
user_fields = set(CurrentUser.__fields__.keys())
common_fields = startup_fields.intersection(user_fields)
if common_fields:
    print(f"Common fields found: {common_fields}")
else:
    print("No common fields between StartupData and CurrentUser")