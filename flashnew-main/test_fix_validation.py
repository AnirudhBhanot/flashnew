#!/usr/bin/env python3
"""
Test script to verify the /predict endpoint validation fix
"""

import sys
sys.path.insert(0, '.')

from api_server_unified import StartupData, StartupDataStrict
from pydantic import ValidationError
import json

print("=== Testing StartupData Validation Fix ===\n")

# Test data scenarios
test_scenarios = [
    {
        "name": "User data only (should be caught)",
        "data": {
            "user_id": "test_user",
            "username": "testuser",
            "email": "test@example.com"
        }
    },
    {
        "name": "Valid startup data",
        "data": {
            "total_capital_raised_usd": 1000000,
            "funding_stage": "seed",
            "sector": "saas",
            "team_size_full_time": 10
        }
    },
    {
        "name": "Mixed user + startup data",
        "data": {
            "user_id": "test_user",
            "username": "testuser",
            "total_capital_raised_usd": 1000000,
            "funding_stage": "seed"
        }
    },
    {
        "name": "Data with 'id' field",
        "data": {
            "id": "startup_123",
            "total_capital_raised_usd": 1000000,
            "funding_stage": "seed"
        }
    }
]

# Test with regular StartupData (allows extra fields)
print("1. Testing with StartupData (extra='allow'):")
print("-" * 50)
for scenario in test_scenarios:
    print(f"\n{scenario['name']}:")
    try:
        startup = StartupData(**scenario['data'])
        print("  ✓ Validation passed")
        # Check for user fields
        data_dict = startup.model_dump()
        user_fields = {'user_id', 'username', 'id'}
        found_user_fields = [f for f in user_fields if f in data_dict and data_dict[f] is not None]
        if found_user_fields:
            print(f"  ⚠️  Warning: Found user fields: {found_user_fields}")
    except ValidationError as e:
        print("  ✗ Validation failed:")
        for error in e.errors():
            print(f"    - {error['loc']}: {error['msg']}")

# Test with strict version
print("\n\n2. Testing with StartupDataStrict (extra='forbid'):")
print("-" * 50)
for scenario in test_scenarios:
    print(f"\n{scenario['name']}:")
    try:
        startup = StartupDataStrict(**scenario['data'])
        print("  ✓ Validation passed")
    except ValidationError as e:
        print("  ✗ Validation failed:")
        for error in e.errors():
            print(f"    - {error['loc']}: {error['msg']}")

# Test the validation logic from the predict endpoint
print("\n\n3. Testing endpoint validation logic:")
print("-" * 50)

def check_for_user_data(data_dict):
    """Replicate the validation logic from the predict endpoint"""
    user_fields = {'user_id', 'username', 'id'}
    if any(field in data_dict for field in user_fields):
        # Check if this looks like user auth data
        if 'user_id' in data_dict and 'username' in data_dict and len(data_dict) < 10:
            return True, f"Detected user auth data: {list(data_dict.keys())}"
    return False, None

for scenario in test_scenarios:
    print(f"\n{scenario['name']}:")
    is_user_data, message = check_for_user_data(scenario['data'])
    if is_user_data:
        print(f"  ✗ Would be rejected: {message}")
    else:
        print("  ✓ Would be accepted")