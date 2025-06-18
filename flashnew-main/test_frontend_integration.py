#!/usr/bin/env python3
"""
Test frontend integration with the API
"""

import requests
import json
from datetime import datetime

# API endpoint
BASE_URL = "http://localhost:8001"

# Sample startup data that frontend would send
frontend_data = {
    # Capital features
    "total_capital_raised_usd": 5000000,
    "cash_on_hand_usd": 3000000,
    "monthly_burn_usd": 200000,
    "runway_months": 15,
    "burn_multiple": 2.5,
    "investor_tier_primary": "tier_1",
    "has_debt": False,
    
    # Advantage features
    "patent_count": 3,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4,
    "switching_cost_score": 3,
    "brand_strength_score": 3,
    "scalability_score": 4,
    
    # Market features
    "sector": "SaaS",
    "tam_size_usd": 10000000000,
    "sam_size_usd": 1000000000,
    "som_size_usd": 100000000,
    "market_growth_rate_percent": 30,
    "customer_count": 100,
    "customer_concentration_percent": 20,
    "user_growth_rate_percent": 25,
    "net_dollar_retention_percent": 120,
    "competition_intensity": 3,
    "competitors_named_count": 10,
    
    # People features
    "founders_count": 2,
    "team_size_full_time": 25,
    "years_experience_avg": 10,
    "domain_expertise_years_avg": 8,
    "prior_startup_experience_count": 2,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 4,
    "advisors_count": 5,
    "team_diversity_percent": 40,
    "key_person_dependency": False,
    
    # Product features
    "product_stage": 2,
    "product_retention_30d": 80,
    "product_retention_90d": 65,
    "dau_mau_ratio": 0.5,
    "annual_revenue_run_rate": 2000000,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "ltv_cac_ratio": 3.5,
    "funding_stage": "series_a"
}

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Server Status: {data['status']}")
            print(f"   Models Loaded: {data['models_loaded']}")
            return True
    except Exception as e:
        print(f"   Error: {e}")
    return False

def test_predict():
    """Test prediction endpoint"""
    print("\n🔮 Testing Prediction Endpoint...")
    try:
        # Add API key header for authentication
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": "dev-key-123"  # Development API key
        }
        response = requests.post(
            f"{BASE_URL}/predict",
            json=frontend_data,
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success Probability: {data.get('success_probability', 'N/A'):.1%}")
            print(f"   Verdict: {data.get('verdict', 'N/A')}")
            print(f"   Confidence: {data.get('confidence_interval', {}).get('lower', 0):.1%} - {data.get('confidence_interval', {}).get('upper', 0):.1%}")
            
            # Check CAMP scores
            if 'camp_scores' in data:
                print("\n   CAMP Scores:")
                for pillar, score in data['camp_scores'].items():
                    print(f"     {pillar}: {score:.1f}/100")
            return True
        else:
            print(f"   Error Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    return False

def test_validate():
    """Test validation endpoint"""
    print("\n✅ Testing Validation Endpoint...")
    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": "dev-key-123"
        }
        response = requests.post(
            f"{BASE_URL}/validate",
            json=frontend_data,
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Valid: {data.get('valid', False)}")
            if data.get('missing_fields'):
                print(f"   Missing Fields: {data['missing_fields']}")
            return True
    except Exception as e:
        print(f"   Error: {e}")
    return False

def test_frontend_aliases():
    """Test frontend-specific endpoint aliases"""
    print("\n🔗 Testing Frontend Aliases...")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "dev-key-123"
    }
    
    # Test predict_simple
    try:
        response = requests.post(
            f"{BASE_URL}/predict_simple",
            json=frontend_data,
            headers=headers
        )
        print(f"   /predict_simple: {response.status_code}")
    except Exception as e:
        print(f"   /predict_simple Error: {e}")
    
    # Test predict_advanced
    try:
        response = requests.post(
            f"{BASE_URL}/predict_advanced",
            json=frontend_data,
            headers=headers
        )
        print(f"   /predict_advanced: {response.status_code}")
    except Exception as e:
        print(f"   /predict_advanced Error: {e}")

def test_investor_profiles():
    """Test investor profiles endpoint"""
    print("\n👥 Testing Investor Profiles...")
    try:
        response = requests.get(f"{BASE_URL}/investor_profiles")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Profiles Available: {len(data.get('profiles', []))}")
            for profile in data.get('profiles', [])[:2]:
                print(f"   - {profile.get('name', 'Unknown')}: {profile.get('focus', 'N/A')}")
            return True
    except Exception as e:
        print(f"   Error: {e}")
    return False

def main():
    """Run all integration tests"""
    print("🧪 FLASH Frontend Integration Test")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run tests
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ Server health check failed. Is the API server running?")
        print("   Run: cd /Users/sf/Desktop/FLASH && python3 api_server_unified.py")
        return
    
    validate_ok = test_validate()
    predict_ok = test_predict()
    test_frontend_aliases()
    investor_ok = test_investor_profiles()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Integration Test Summary:")
    print(f"   ✅ Health Check: {'PASS' if health_ok else 'FAIL'}")
    print(f"   ✅ Validation: {'PASS' if validate_ok else 'FAIL'}")
    print(f"   ✅ Prediction: {'PASS' if predict_ok else 'FAIL'}")
    print(f"   ✅ Investor Profiles: {'PASS' if investor_ok else 'FAIL'}")
    
    if all([health_ok, validate_ok, predict_ok, investor_ok]):
        print("\n🎉 All integration tests passed! Frontend should work correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()