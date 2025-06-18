#!/usr/bin/env python3
"""Test what's actually working in the FLASH system"""
import json
import requests

print("🔍 Testing FLASH System Features")
print("="*60)

# Base URL
BASE_URL = "http://localhost:8001"

# Test health endpoint
print("\n1. API Health Check")
print("-"*40)
try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API is healthy")
        print(f"   Models loaded: {data.get('models_loaded', 0)}")
        print(f"   Patterns available: {data.get('patterns_available', False)}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test prediction endpoint
print("\n2. ML Prediction")
print("-"*40)
test_data = {
    "funding_stage": "seed",
    "sector": "saas",
    "total_capital_raised_usd": 2000000,
    "monthly_burn_usd": 150000,
    "runway_months": 12,
    "team_size_full_time": 18,
    "founders_count": 2,
    "market_size_usd": 5000000000,
    "revenue_growth_rate_percent": 100,
    "monthly_active_users": 1000,
    "customer_count": 50,
    "ltv_cac_ratio": 3.0,
    "annual_revenue_run_rate": 1000000
}

try:
    response = requests.post(f"{BASE_URL}/predict", json=test_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Prediction successful")
        print(f"   Success probability: {data.get('success_probability', 0)*100:.1f}%")
        print(f"   Verdict: {data.get('verdict', 'N/A')}")
        camp = data.get('camp_scores', {})
        if camp:
            print(f"   CAMP Scores:")
            print(f"     Capital: {camp.get('capital', 0)*100:.1f}%")
            print(f"     Advantage: {camp.get('advantage', 0)*100:.1f}%")
            print(f"     Market: {camp.get('market', 0)*100:.1f}%") 
            print(f"     People: {camp.get('people', 0)*100:.1f}%")
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test LLM recommendations
print("\n3. AI Recommendations")
print("-"*40)
rec_data = {
    "startup_data": test_data,
    "scores": {
        "success_probability": 0.5,
        "capital": 0.5,
        "advantage": 0.3,
        "market": 0.6,
        "people": 0.4
    }
}

try:
    response = requests.post(f"{BASE_URL}/api/analysis/recommendations/dynamic", json=rec_data)
    if response.status_code == 200:
        data = response.json()
        recs = data.get('recommendations', [])
        print(f"✅ Recommendations generated: {len(recs)} items")
        if recs:
            print(f"   Top recommendation: {recs[0].get('recommendation', 'N/A')}")
    else:
        print(f"❌ Recommendations failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test market insights
print("\n4. Market Insights")
print("-"*40)
market_data = {
    "startup_data": {
        "sector": "saas",
        "funding_stage": "seed",
        "annual_revenue_run_rate": 1000000,
        "tam_size_usd": 5000000000
    }
}

try:
    response = requests.post(f"{BASE_URL}/api/analysis/insights/market", json=market_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Market insights generated")
        trends = data.get('market_trends', [])
        if trends:
            print(f"   Market trends: {len(trends)} identified")
    else:
        print(f"❌ Market insights failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test competitor analysis
print("\n5. Competitor Analysis")
print("-"*40)
comp_data = {
    "startup_data": {
        "sector": "saas",
        "funding_stage": "seed",
        "annual_revenue_run_rate": 1000000,
        "tam_size_usd": 5000000000,
        "unique_advantages": ["Fast implementation", "Lower cost", "Better UX"]
    }
}

try:
    response = requests.post(f"{BASE_URL}/api/analysis/competitors/analyze", json=comp_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Competitor analysis completed")
        comps = data.get('competitors', [])
        if comps:
            print(f"   Competitors identified: {len(comps)}")
            print(f"   Competitive intensity: {data.get('competitive_intensity', 'N/A')}")
    else:
        print(f"❌ Competitor analysis failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test what-if analysis
print("\n6. What-If Analysis")
print("-"*40)
whatif_data = {
    "startup_data": test_data,
    "current_scores": {
        "success_probability": 0.5,
        "capital": 0.5,
        "advantage": 0.3,
        "market": 0.6,
        "people": 0.4
    },
    "improvements": [
        {
            "id": "increase_revenue",
            "description": "Double revenue",
            "camp_area": "market",
            "estimated_impact": 0.1
        }
    ]
}

try:
    response = requests.post(f"{BASE_URL}/api/analysis/whatif/dynamic", json=whatif_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ What-if analysis completed")
        new_prob = data.get('new_probability', {}).get('value', 0)
        print(f"   New success probability: {new_prob*100:.1f}%")
    else:
        print(f"❌ What-if analysis failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# List available endpoints
print("\n7. Available API Endpoints")
print("-"*40)
try:
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("✅ API documentation available at /docs")
    
    # Try OpenAPI schema
    response = requests.get(f"{BASE_URL}/openapi.json")
    if response.status_code == 200:
        data = response.json()
        paths = data.get('paths', {})
        print(f"✅ Total endpoints available: {len(paths)}")
        
        # Group by category
        categories = {}
        for path, methods in paths.items():
            category = path.split('/')[2] if len(path.split('/')) > 2 else 'core'
            if category not in categories:
                categories[category] = []
            categories[category].append(path)
        
        print("\n   Endpoints by category:")
        for cat, endpoints in sorted(categories.items()):
            print(f"   • {cat}: {len(endpoints)} endpoints")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Testing completed!")