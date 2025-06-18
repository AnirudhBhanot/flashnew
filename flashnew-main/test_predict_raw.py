#!/usr/bin/env python3
"""
Test the predict endpoint with raw HTTP request
"""

import requests
import json

# Test with minimal data first
minimal_data = {
    "total_capital_raised_usd": 5000000
}

print("Testing /predict with minimal data...")
response = requests.post(
    "http://localhost:8001/predict",
    json=minimal_data,
    headers={"Content-Type": "application/json"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}...")

if response.status_code != 200:
    # Try to understand the error
    try:
        error_data = json.loads(response.text)
        if 'details' in error_data and len(error_data['details']) > 0:
            detail = error_data['details'][0]
            print(f"\nError Detail:")
            print(f"  Type: {detail.get('type')}")
            print(f"  Location: {detail.get('loc')}")
            print(f"  Message: {detail.get('msg')}")
            print(f"  Input received: {detail.get('input')}")
    except:
        pass

# Now test the validate endpoint to see if it has the same issue
print("\n\nTesting /validate with same data...")
response = requests.post(
    "http://localhost:8001/validate",
    json=minimal_data,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}...")

# Test predict_simple
print("\n\nTesting /predict_simple with same data...")
response = requests.post(
    "http://localhost:8001/predict_simple",
    json=minimal_data,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}...")