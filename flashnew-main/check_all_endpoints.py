#!/usr/bin/env python3
"""
Check all API endpoints to ensure everything is working
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"
API_KEY = "test-api-key-123"
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def check_endpoint(method, path, data=None, requires_auth=True):
    """Check a single endpoint"""
    url = f"{BASE_URL}{path}"
    headers = HEADERS if requires_auth else {"Content-Type": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            return f"❌ Unsupported method: {method}"
        
        status = "✅" if response.status_code == 200 else "❌"
        return f"{status} {method} {path} - {response.status_code}"
    except Exception as e:
        return f"❌ {method} {path} - Error: {str(e)}"

def main():
    print("🔍 Checking All FLASH API Endpoints")
    print("=" * 60)
    print(f"API Server: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ API Server is running")
    except:
        print("❌ API Server is not responding!")
        return
    
    print("\n📍 Main Endpoints:")
    endpoints = [
        ("GET", "/", False),
        ("GET", "/health", False),
        ("GET", "/features", True),
    ]
    
    for method, path, auth in endpoints:
        print(f"  {check_endpoint(method, path, requires_auth=auth)}")
    
    print("\n📍 Config Endpoints:")
    config_endpoints = [
        "/config/stage-weights",
        "/config/model-performance",
        "/config/company-examples",
        "/config/success-thresholds",
        "/config/model-weights",
        "/config/revenue-benchmarks",
        "/config/company-comparables",
        "/config/display-limits",
        "/config/all"
    ]
    
    for endpoint in config_endpoints:
        print(f"  {check_endpoint('GET', endpoint)}")
    
    print("\n📍 Prediction Endpoint:")
    # Test data for prediction
    test_data = {
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 200000,
        "runway_months": 15,
        "burn_multiple": 2,
        "investor_tier_primary": "Tier 2",
        "has_debt": False,
        "patent_count": 3,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,
        "switching_cost_score": 3,
        "brand_strength_score": 3,
        "scalability_score": 4,
        "sector": "SaaS",
        "tam_size_usd": 5000000000,
        "sam_size_usd": 500000000,
        "som_size_usd": 50000000,
        "market_growth_rate_percent": 35,
        "customer_count": 100,
        "customer_concentration_percent": 20,
        "user_growth_rate_percent": 25,
        "net_dollar_retention_percent": 115,
        "competition_intensity": 3,
        "competitors_named_count": 15,
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 10,
        "domain_expertise_years_avg": 7,
        "prior_startup_experience_count": 2,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,
        "advisors_count": 5,
        "team_diversity_percent": 40,
        "key_person_dependency": False,
        "product_stage": "growth",
        "product_retention_30d": 0.8,
        "product_retention_90d": 0.7,
        "dau_mau_ratio": 0.4,
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_percent": 100,
        "gross_margin_percent": 70,
        "ltv_cac_ratio": 3,
        "funding_stage": "series_a",
        "strategic_partners_count": 3,
        "has_repeat_founder": True,
        "execution_risk_score": 2,
        "vertical_integration_score": 3,
        "time_to_market_advantage_years": 1,
        "partnership_leverage_score": 3,
        "company_age_months": 24,
        "cash_efficiency_score": 1.5,
        "operating_leverage_trend": 1,
        "predictive_modeling_score": 3
    }
    
    result = check_endpoint("POST", "/predict", test_data)
    print(f"  {result}")
    
    # Try to get actual prediction result
    try:
        response = requests.post(f"{BASE_URL}/predict", headers=HEADERS, json=test_data)
        if response.status_code == 200:
            pred_data = response.json()
            print(f"\n  📊 Prediction Result:")
            print(f"     Success Probability: {pred_data.get('success_probability', 'N/A'):.1%}")
            print(f"     Verdict: {pred_data.get('verdict', 'N/A')}")
            print(f"     Risk Level: {pred_data.get('risk_level', 'N/A')}")
            
            camp = pred_data.get('camp_analysis', {})
            if camp:
                print(f"\n  🎯 CAMP Analysis:")
                print(f"     Capital:   {camp.get('capital', 0):.1%}")
                print(f"     Advantage: {camp.get('advantage', 0):.1%}")
                print(f"     Market:    {camp.get('market', 0):.1%}")
                print(f"     People:    {camp.get('people', 0):.1%}")
    except Exception as e:
        print(f"  ❌ Error getting prediction details: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Endpoint check complete")

if __name__ == "__main__":
    main()