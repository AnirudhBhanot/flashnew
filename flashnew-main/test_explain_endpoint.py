#!/usr/bin/env python3
"""
Test the /explain endpoint
"""
import subprocess
import time
import requests
import json

# Start server
process = subprocess.Popen(
    ["python3", "api_server_unified.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(3)

# Test data
test_data = {
    "funding_stage": "series_a",
    "total_capital_raised_usd": 5000000,
    "sector": "enterprise_saas",
    "product_stage": "growth",
    "tech_differentiation_score": 4,
    "scalability_score": 4,
    "team_size_full_time": 25,
    "founders_count": 2,
    "market_growth_rate_percent": 30,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 70,
    "years_experience_avg": 10
}

print("Testing /explain endpoint...")

try:
    response = requests.post(
        "http://localhost:8001/explain",
        json=test_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Explain endpoint working!")
        
        # Show explanations
        explanations = result['explanations']
        
        print("\n📊 Feature Importance:")
        for feature, score in explanations['feature_importance'].items():
            print(f"   {feature}: {score:.2f}")
        
        print("\n🎯 Decision Factors:")
        for factor in explanations['decision_factors'][:5]:
            print(f"   • {factor}")
        
        print("\n💡 Improvement Suggestions:")
        for suggestion in explanations['improvement_suggestions']:
            print(f"   • {suggestion}")
            
        print("\n🔍 Confidence Breakdown:")
        conf = explanations['confidence_breakdown']
        print(f"   Model Agreement: {conf.get('model_agreement', 0):.1%}")
        print(f"   Pattern Confidence: {conf.get('pattern_confidence', 0):.1%}")
        print(f"   Overall Confidence: {conf.get('overall_confidence', 0):.1%}")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:200])
        
except Exception as e:
    print(f"Request error: {e}")
finally:
    process.terminate()
    process.wait()