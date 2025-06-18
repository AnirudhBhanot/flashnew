#!/usr/bin/env python3
"""
Test script to verify authentication bypass is working correctly
"""
import os
import requests
import json
from datetime import datetime

# Set test environment
os.environ['ENVIRONMENT'] = 'development'
os.environ['DISABLE_AUTH'] = 'true'

# Test configuration
BASE_URL = "http://localhost:8001"
TEST_ENDPOINTS = [
    ("/", "GET", None),
    ("/health", "GET", None),
    ("/features", "GET", None),
    ("/system_info", "GET", None),
    ("/metrics/summary", "GET", None),
    ("/predict", "POST", {
        "total_capital_raised_usd": 1000000,
        "monthly_burn_usd": 50000,
        "runway_months": 20,
        "team_size_full_time": 10,
        "funding_stage": "seed",
        "sector": "saas",
        "product_stage": "mvp"
    })
]

def test_auth_bypass():
    """Test that endpoints work without authentication"""
    print(f"\n{'='*60}")
    print(f"Testing Authentication Bypass - {datetime.now()}")
    print(f"{'='*60}\n")
    
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'not set')}")
    print(f"DISABLE_AUTH: {os.environ.get('DISABLE_AUTH', 'not set')}")
    print(f"Base URL: {BASE_URL}\n")
    
    results = []
    
    for endpoint, method, data in TEST_ENDPOINTS:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTesting {method} {endpoint}...")
        
        try:
            # Make request WITHOUT any authentication headers
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(
                    url, 
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
            
            # Check response
            success = response.status_code < 400
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "success": success,
                "message": "OK" if success else response.text[:100]
            }
            
            if success:
                print(f"  ✅ Success: {response.status_code}")
                if endpoint == "/predict" and method == "POST":
                    try:
                        data = response.json()
                        print(f"  Success Probability: {data.get('success_probability', 'N/A')}")
                        print(f"  Verdict: {data.get('verdict', 'N/A')}")
                    except:
                        pass
            else:
                print(f"  ❌ Failed: {response.status_code}")
                print(f"  Error: {response.text[:200]}")
            
            results.append(result)
            
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Connection Error - Is the server running on {BASE_URL}?")
            results.append({
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "success": False,
                "message": "Connection refused"
            })
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append({
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "success": False,
                "message": str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    
    print(f"\nTotal endpoints tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    
    if successful == total:
        print("\n✅ All endpoints accessible without authentication!")
        print("Authentication bypass is working correctly.")
    else:
        print("\n❌ Some endpoints failed!")
        print("Authentication bypass may not be working correctly.")
        print("\nFailed endpoints:")
        for r in results:
            if not r["success"]:
                print(f"  - {r['method']} {r['endpoint']}: {r['message']}")
    
    return successful == total

def test_with_auth_enabled():
    """Test that authentication is enforced when DISABLE_AUTH is false"""
    print(f"\n\n{'='*60}")
    print("Testing With Authentication Enabled")
    print(f"{'='*60}\n")
    
    # Temporarily disable the bypass
    os.environ['DISABLE_AUTH'] = 'false'
    
    url = f"{BASE_URL}/system_info"
    print(f"Testing {url} without auth headers (should fail)...")
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 401:
            print("✅ Correctly rejected: 401 Unauthorized")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
    except:
        print("❌ Connection error")
        return False

if __name__ == "__main__":
    print("FLASH API Authentication Bypass Test")
    print("Make sure the API server is running on http://localhost:8001")
    print("with ENVIRONMENT=development and DISABLE_AUTH=true\n")
    
    input("Press Enter to start tests...")
    
    # Test bypass
    bypass_works = test_auth_bypass()
    
    # Note: Don't test with auth enabled as it would require restarting the server
    print("\n\nNote: To test with authentication enabled, restart the server")
    print("with DISABLE_AUTH=false and run this script again.")