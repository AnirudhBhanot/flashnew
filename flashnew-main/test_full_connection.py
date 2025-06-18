#!/usr/bin/env python3
"""
Comprehensive test of frontend-backend connection
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"

def test_api_health():
    """Test if API is running and healthy"""
    print("\n1. Testing API Health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API is running on port 8001")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Models loaded: {data.get('models_loaded', 0)}")
            return True
        else:
            print(f"   ❌ API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to API on port 8001")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    return False

def test_frontend_running():
    """Test if frontend is running"""
    print("\n2. Testing Frontend...")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Frontend is running on port 3000")
            return True
        else:
            print(f"   ❌ Frontend returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to frontend on port 3000")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    return False

def test_cors_headers():
    """Test CORS configuration"""
    print("\n3. Testing CORS Configuration...")
    try:
        # Simulate a request from the frontend
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        response = requests.options(f"{API_URL}/predict", headers=headers)
        
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers'),
        }
        
        print(f"   CORS Headers:")
        for key, value in cors_headers.items():
            if value:
                print(f"   - {key}: {value}")
        
        if cors_headers['access-control-allow-origin']:
            print(f"   ✅ CORS is properly configured")
            return True
        else:
            print(f"   ❌ CORS headers missing")
    except Exception as e:
        print(f"   ❌ Error testing CORS: {e}")
    return False

def test_prediction_endpoint():
    """Test the prediction endpoint with proper data"""
    print("\n4. Testing Prediction Endpoint...")
    
    # Corrected test data (matching API expectations)
    test_data = {
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
        
        # Product features (corrected format)
        "product_stage": "mvp",  # String, not number
        "product_retention_30d": 0.80,  # Decimal, not percentage
        "product_retention_90d": 0.65,  # Decimal, not percentage
        "dau_mau_ratio": 0.5,
        "annual_revenue_run_rate": 2000000,
        "revenue_growth_rate_percent": 150,
        "gross_margin_percent": 75,
        "ltv_cac_ratio": 3.5,
        "funding_stage": "series_a"
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            f"{API_URL}/predict",
            json=test_data,
            headers=headers,
            timeout=10
        )
        
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Prediction successful!")
            print(f"   Success Probability: {data.get('success_probability', 0)*100:.1f}%")
            print(f"   Verdict: {data.get('verdict', 'N/A')}")
            
            # Check for CAMP/pillar scores
            if 'pillar_scores' in data:
                print(f"   CAMP Scores Found:")
                for pillar, score in data['pillar_scores'].items():
                    print(f"     - {pillar}: {score:.1f}/100")
            elif 'camp_scores' in data:
                print(f"   CAMP Scores Found:")
                for pillar, score in data['camp_scores'].items():
                    print(f"     - {pillar}: {score:.1f}/100")
            
            return True
        else:
            print(f"   ❌ Prediction failed")
            print(f"   Error: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    return False

def test_model_loading():
    """Check if models are properly loaded"""
    print("\n5. Testing Model Loading...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            models_loaded = data.get('models_loaded', 0)
            
            if models_loaded > 0:
                print(f"   ✅ {models_loaded} models loaded successfully")
                return True
            else:
                print(f"   ⚠️  No models loaded - predictions may fail")
                print(f"   Check if model files exist in:")
                print(f"   - models/production_v45/")
                print(f"   - models/production_v45_fixed/")
        else:
            print(f"   ❌ Cannot check model status")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    return False

def main():
    """Run all connection tests"""
    print("=" * 60)
    print("FLASH Frontend-Backend Connection Test")
    print("=" * 60)
    
    results = {
        "API Running": test_api_health(),
        "Frontend Running": test_frontend_running(),
        "CORS Configured": test_cors_headers(),
        "Models Loaded": test_model_loading(),
        "Predictions Working": test_prediction_endpoint(),
    }
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = True
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test:.<30} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 All tests passed! Frontend and backend are properly connected.")
        print("\nYou can now:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Fill in the startup evaluation form")
        print("3. Submit to get predictions from the backend")
    else:
        print("⚠️  Some tests failed. Issues to resolve:")
        
        if not results["API Running"]:
            print("\n1. Start the API server:")
            print("   cd /Users/sf/Desktop/FLASH")
            print("   python3 api_server_unified_final.py")
        
        if not results["Frontend Running"]:
            print("\n2. Start the frontend:")
            print("   cd /Users/sf/Desktop/FLASH/flash-frontend")
            print("   npm start")
        
        if not results["Models Loaded"]:
            print("\n3. Check model files exist or run training:")
            print("   python3 train_minimal_models.py")
        
        if results["API Running"] and results["Frontend Running"] and not results["CORS Configured"]:
            print("\n4. CORS issue - check api_server_unified_final.py CORS middleware settings")

if __name__ == "__main__":
    main()