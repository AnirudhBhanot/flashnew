#!/usr/bin/env python3
"""Verify the fixed API server is running correctly"""

import requests
import json

print("Verifying FLASH Fixed API Server...\n")

# 1. Check health
try:
    health = requests.get("http://localhost:8001/health", timeout=5)
    if health.ok:
        print("✅ Server is healthy")
        print(f"   Response: {health.json()}")
    else:
        print("❌ Health check failed")
except Exception as e:
    print(f"❌ Could not connect to server: {e}")
    exit(1)

# 2. Test prediction with pre-seed case
print("\n2. Testing pre-seed prediction (should get < 50% and FAIL)...")

test_data = {
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 150000,
    "runway_months": 10,
    "burn_multiple": 3,
    "gross_margin_percent": 45,
    "revenue_growth_rate_percent": 80,
    "patent_count": 1,
    "network_effects_present": False,
    "tech_differentiation_score": 2,
    "scalability_score": 3,
    "tam_size_usd": 500000000,
    "market_growth_rate_percent": 15,
    "competitive_intensity_score": 4,
    "ltv_to_cac_ratio": 2.0,
    "team_size_full_time": 4,
    "founders_experience_score": 2,
    "previous_startup_experience": 0,
    "team_completeness_score": 2,
    "product_stage": "mvp",
    "mrr_usd": 2000,
    "product_market_fit_score": 2,
}

try:
    response = requests.post(
        "http://localhost:8001/predict_enhanced",
        json=test_data,
        timeout=10
    )
    
    if response.ok:
        result = response.json()
        print(f"\n✅ Prediction successful!")
        print(f"   Success Probability: {result['success_probability']:.1%}")
        print(f"   Verdict: {result['verdict']}")
        print(f"   Risk Level: {result.get('risk_level', 'N/A')}")
        
        print(f"\n   CAMP Scores:")
        for pillar, score in result['pillar_scores'].items():
            print(f"     {pillar}: {score:.1%}")
            
        # Verify it's working correctly
        if result['success_probability'] < 0.5 and result['verdict'] == 'FAIL':
            print(f"\n✅ SYSTEM WORKING CORRECTLY!")
            print(f"   Pre-seed with mediocre metrics correctly gets FAIL verdict")
        else:
            print(f"\n⚠️  Unexpected result - check system")
            
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(f"   Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error making prediction: {e}")

print("\n" + "="*60)
print("Server Status: RUNNING on http://localhost:8001")
print("="*60)
print("\nAvailable endpoints:")
print("- POST /predict_enhanced - Main prediction endpoint")
print("- GET  /health - Health check")
print("- GET  /config/stage-weights - Stage-specific weights")
print("- GET  /config/company-examples - Example companies")
print("- GET  /validate - List required features")
print("\nTo stop the server, use: pkill -f 'api_server_fixed'")