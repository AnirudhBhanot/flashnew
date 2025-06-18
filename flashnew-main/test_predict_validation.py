#!/usr/bin/env python3
"""
Test the /predict endpoint validation issue
"""

import requests
import json

# Test data that looks like user data
user_like_data = {
    "user_id": "test_user",
    "username": "testuser", 
    "email": "test@example.com"
}

# Valid startup data
valid_startup_data = {
    "total_capital_raised_usd": 1000000,
    "funding_stage": "seed",
    "sector": "saas",
    "team_size_full_time": 10,
    "runway_months": 18
}

# Mixed data (user data + startup data)
mixed_data = {
    **user_like_data,
    **valid_startup_data
}

print("=== Testing /predict endpoint locally ===")

# Test 1: Send user data only
print("\n1. Sending user data only:")
try:
    response = requests.post(
        "http://localhost:8001/predict",
        json=user_like_data,
        headers={"X-API-Key": "test-key"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Send valid startup data
print("\n2. Sending valid startup data:")
try:
    response = requests.post(
        "http://localhost:8001/predict",
        json=valid_startup_data,
        headers={"X-API-Key": "test-key"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
    else:
        print(f"Response: {response.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Send mixed data
print("\n3. Sending mixed data:")
try:
    response = requests.post(
        "http://localhost:8001/predict",
        json=mixed_data,
        headers={"X-API-Key": "test-key"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
    else:
        print(f"Response: {response.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")

# Test direct Pydantic validation
print("\n=== Direct Pydantic Validation ===")
from api_server_unified import StartupData
from pydantic import ValidationError

for test_name, test_data in [
    ("User data", user_like_data),
    ("Valid startup data", valid_startup_data),
    ("Mixed data", mixed_data)
]:
    print(f"\nTesting {test_name}:")
    try:
        startup = StartupData(**test_data)
        print(f"  ✓ Validation passed")
        non_null = sum(1 for v in startup.model_dump().values() if v is not None)
        print(f"  ✓ Non-null fields: {non_null}")
    except ValidationError as e:
        print(f"  ✗ Validation failed:")
        for error in e.errors():
            print(f"    - {error['loc']}: {error['msg']}")