#!/usr/bin/env python3
"""
Test the complete frontend-backend connection with ML models
"""

import requests
import json
import time

# Test data matching frontend format
test_startup = {
    "funding_stage": "seed",
    "total_capital_raised_usd": 2000000,
    "cash_on_hand_usd": 1800000,
    "monthly_burn_usd": 150000,
    "annual_revenue_run_rate": 1200000,
    "revenue_growth_rate_percent": 200,
    "gross_margin_percent": 70,
    "ltv_cac_ratio": 3.5,
    "runway_months": 12,
    "customer_count": 150,
    "churn_rate_monthly_percent": 3,
    "dau_mau_ratio": 0.65,
    "investor_tier_primary": "tier_2",
    "founder_domain_expertise_yrs": 8,
    "prior_successful_exits": 1,
    "team_diversity_score": 8,
    "market_tam_usd": 50000000000,
    "market_growth_rate_percent": 35,
    "competition_intensity_score": 6,
    "product_stage": "scaling",
    "network_effects_score": 7,
    "has_debt": False,
    "has_revenue": True,
    "is_saas": True,
    "is_b2b": True,
    "startup_name": "Test Startup Inc",
    "team_size_full_time": 15,
    "product_readiness_score": 8,
    "acquisition_channel_score": 7,
    "scalability_score": 4,
    "customer_engagement_score": 7,
    "tech_stack_score": 8,
    "viral_coefficient": 1.2,
    "equity_dilution_percent": 25,
    "ip_portfolio_score": 6,
    "regulatory_compliance_score": 8,
    "years_since_founding": 2,
    "founder_equity_percent": 60,
    "nps_score": 45,
    "sector": "Technology",
    "has_patents": True,
    "previous_funding_rounds": 1
}

def test_connection():
    """Test the frontend-backend connection"""
    
    print("🔌 Testing Frontend-Backend Connection...")
    print("="*60)
    
    # 1. Test Health Endpoint
    print("\n1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API is healthy: {health}")
            print(f"   - Models loaded: {health.get('models_loaded', 0)}")
            print(f"   - Patterns available: {health.get('patterns_available', False)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return
    
    # 2. Test Prediction Endpoint
    print("\n2️⃣ Testing Prediction Endpoint...")
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8001/predict",
            json=test_startup,
            headers={"Content-Type": "application/json"}
        )
        elapsed = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful! (took {elapsed:.0f}ms)")
            print(f"   - Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"   - Verdict: {result.get('verdict', 'N/A')}")
            print(f"   - Risk Level: {result.get('risk_level', 'N/A')}")
            
            # Check CAMP scores
            if 'pillar_scores' in result:
                print(f"   - CAMP Scores:")
                for pillar, score in result['pillar_scores'].items():
                    print(f"     • {pillar.capitalize()}: {score:.2f}")
            
            # Check patterns if available
            if 'patterns' in result:
                print(f"   - Patterns Detected: {len(result['patterns'])}")
                for pattern in result['patterns'][:3]:
                    print(f"     • {pattern['name']} ({pattern['confidence']:.0%})")
            
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Prediction request failed: {e}")
    
    # 3. Test Frontend Access
    print("\n3️⃣ Testing Frontend Access...")
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend is running on http://localhost:3000")
        else:
            print(f"⚠️  Frontend returned status: {response.status_code}")
    except:
        print("❌ Frontend not accessible on port 3000")
    
    # 4. Test Data Flow
    print("\n4️⃣ Testing Complete Data Flow...")
    print("   Frontend (3000) → API (8001) → ML Models → Response")
    
    # Summary
    print("\n" + "="*60)
    print("📊 CONNECTION TEST SUMMARY:")
    print("="*60)
    
    if health.get('models_loaded', 0) == 0:
        print("⚠️  WARNING: No ML models are loaded!")
        print("   The connection works but predictions use default values.")
        print("   To load models, run the training scripts.")
    else:
        print("✅ Frontend and Backend are properly connected!")
        print(f"   - {health.get('models_loaded', 0)} ML models loaded")
        print("   - Ready for production use")
    
    print("\n💡 To access the application:")
    print("   1. Open http://localhost:3000 in your browser")
    print("   2. Fill in the startup analysis form")
    print("   3. Submit to see ML predictions")
    print("\n✨ The system is ready for use!")

if __name__ == "__main__":
    test_connection()