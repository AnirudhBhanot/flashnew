#!/usr/bin/env python3
"""
Test if pattern system is properly enabled and working
"""
import os
import subprocess
import time
import requests
import json

print("🧪 Testing Pattern System")
print("=" * 50)

# Start server with environment
process = subprocess.Popen(
    ["python3", "api_server_unified.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env={
        "DB_PASSWORD": "test_password",
        "ENVIRONMENT": "development",
        "API_KEYS": "",
        **dict(os.environ)
    }
)

# Wait for startup
time.sleep(5)

if process.poll() is not None:
    print("❌ API server failed to start")
    stdout, stderr = process.communicate()
    print("Error:", stderr[:500])
    exit(1)

print("✅ API server started")

# Test patterns endpoint
print("\n1️⃣ Testing /patterns endpoint...")
try:
    response = requests.get("http://localhost:8001/patterns", timeout=5)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['total_patterns']} patterns")
        if result['total_patterns'] > 0:
            print("Sample patterns:")
            for pattern in result['patterns'][:5]:
                print(f"  - {pattern}")
    else:
        print(f"❌ Patterns endpoint failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test system info to check weights
print("\n2️⃣ Testing /system_info endpoint...")
try:
    response = requests.get("http://localhost:8001/system_info", timeout=5)
    if response.status_code == 200:
        result = response.json()
        weights = result.get('weights', {})
        print("Model weights:")
        for model, weight in weights.items():
            print(f"  - {model}: {weight}")
        
        pattern_weight = weights.get('pattern_analysis', 0)
        if pattern_weight > 0:
            print(f"\n✅ Pattern system is ENABLED with {pattern_weight*100:.0f}% weight")
        else:
            print(f"\n❌ Pattern system is DISABLED (weight: {pattern_weight})")
    else:
        print(f"❌ System info failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test prediction with pattern analysis
print("\n3️⃣ Testing prediction with patterns...")
test_data = {
    "funding_stage": "series_a",
    "total_capital_raised_usd": 5000000,
    "sector": "b2b_saas",
    "product_stage": "growth",
    "tech_differentiation_score": 4,
    "scalability_score": 4,
    "team_size_full_time": 25,
    "founders_count": 2,
    "market_growth_rate_percent": 30,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "years_experience_avg": 10,
    "ltv_cac_ratio": 3.5,
    "annual_revenue_run_rate": 2000000,
    "user_growth_rate_percent": 100,
    "burn_multiple": 2.0
}

try:
    response = requests.post(
        "http://localhost:8001/predict_enhanced",
        json=test_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Enhanced prediction successful")
        
        # Check for pattern analysis
        if 'pattern_analysis' in result:
            patterns = result['pattern_analysis']
            print("\n📊 Pattern Analysis:")
            print(f"  Pattern Score: {patterns.get('pattern_score', 'N/A')}")
            print(f"  Primary Patterns: {patterns.get('primary_patterns', [])}")
            if patterns.get('pattern_insights'):
                print("  Insights:")
                for insight in patterns['pattern_insights'][:3]:
                    print(f"    - {insight}")
        else:
            print("\n⚠️  No pattern analysis in response")
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(response.text[:200])
except Exception as e:
    print(f"❌ Error: {e}")

# Cleanup
process.terminate()
process.wait()
print("\n✅ Test completed")