#!/usr/bin/env python3
"""
Final integration test after cleanup
"""

import requests
import json
import time
import subprocess

def test_integration():
    """Test the complete system integration"""
    
    print("🧪 Testing FLASH System Integration")
    print("="*60)
    
    # Kill any existing API servers
    subprocess.run(["pkill", "-f", "api_server_unified"], capture_output=True)
    time.sleep(2)
    
    # Start API server
    print("\n1️⃣ Starting API server...")
    api_process = subprocess.Popen(
        ["python3", "api_server_unified.py"],
        cwd="/Users/sf/Desktop/FLASH",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for server to start
    print("   Waiting for initialization...")
    time.sleep(8)
    
    # Check health
    try:
        health = requests.get("http://localhost:8001/health", timeout=5)
        if health.status_code == 200:
            print("✅ API server is healthy")
        else:
            print("❌ API health check failed")
            api_process.terminate()
            return False
    except:
        print("❌ API server not responding")
        api_process.terminate()
        return False
    
    # Test with minimal valid data
    print("\n2️⃣ Testing prediction endpoint...")
    
    # Minimal complete data that should work
    test_data = {
        # Core fields
        "funding_stage": "series_a",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 150000,
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_yoy": 150,
        "gross_margin": 75,
        "team_size": 25,
        "founder_experience_years": 12,
        "market_size_billions": 10,
        "product_market_fit_score": 80,
        
        # Required fields with defaults
        "founding_year": 2021,
        "total_funding": 5000000,
        "num_funding_rounds": 2,
        "burn_rate": 150000,
        "runway": 20,
        "runway_months": 20,
        "burn_multiple": 2.0,
        
        # Boolean fields (as integers for backend)
        "repeat_founder": 1,
        "has_debt": 0,
        "international_presence": 0,
        "has_patents": 1,
        "network_effects_present": 1,
        "has_data_moat": 1,
        "regulatory_advantage_present": 0,
        "key_person_dependency": 0,
        
        # Additional required fields
        "r_and_d_spend_percentage": 25,
        "r_and_d_intensity": 0.25,
        "sales_marketing_efficiency": 1.2,
        "customer_acquisition_cost": 5000,
        "lifetime_value": 25000,
        "months_to_profitability": 18,
        "investor_tier_primary": "tier_1",
        "investor_count": 5,
        "investor_experience_score": 85,
        "investor_concentration": 20,
        "board_diversity_score": 70,
        "scalability_score": 0.8,  # 0-1 scale
        "innovation_index": 80,
        "competitive_moat_score": 75,
        "technical_debt_ratio": 20,
        "engineering_ratio": 60,
        "team_completeness_score": 90,
        "advisory_board_strength": 85,
        "company_age_months": 36,
        "pivot_count": 1,
        "partnership_score": 70,
        "customer_concentration": 15,
        "esg_score": 65,
        "market_growth_rate": 25,
        "market_competition_level": "medium",
        "regulatory_risk_score": 30,
        "technology_risk_score": 25,
        "technology_score": 85,
        "ip_portfolio_strength": 70,
        "patent_count": 3,
        "viral_coefficient": 1.2,
        "weekly_active_users_growth": 10,
        "feature_adoption_rate": 65,
        "tech_stack_modernity": 85,
        "cybersecurity_score": 80,
        "data_privacy_compliance": 90,
        "platform_risk_score": 20,
        "debt_to_equity": 0,
        
        # Market fields
        "tam_size": 10000000000,
        "tam_size_usd": 10000000000,
        "sam_size_usd": 1000000000,
        "sam_percentage": 10,
        "som_size_usd": 100000000,
        "market_share": 1,
        "market_growth_rate_percent": 25,
        "customer_count": 100,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 120,
        "net_dollar_retention_percent": 115,
        "competition_intensity": "medium",
        "competitors_named_count": 5,
        
        # Team fields  
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 8,
        "domain_expertise_years_avg": 6,
        "prior_startup_experience_count": 3,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 85,
        "c_suite_completeness_percent": 80,
        
        # Product fields
        "revenue_per_employee": 48000,
        "product_stage": "growth",
        "mvp_months_to_market": 6,
        "feature_completeness_percent": 85,
        "technical_complexity_score": 80,
        "api_integration_count": 15,
        "platform_dependency_score": 30,
        "code_quality_score": 85,
        "switching_cost_score": 70,
        "brand_strength_score": 65,
        "sector": "technology"
    }
    
    try:
        response = requests.post("http://localhost:8001/predict", json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"\n📊 Results:")
            print(f"   Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"   Verdict: {result.get('verdict', 'N/A')}")
            print(f"   Verdict Strength: {result.get('verdict_strength', 'N/A')}")
            
            # CAMP scores
            camp_scores = result.get('camp_scores', {})
            if camp_scores:
                print(f"\n   CAMP Scores:")
                for pillar, score in camp_scores.items():
                    print(f"     {pillar}: {score:.2f}")
            
            success = True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            try:
                error = response.json()
                print(f"   Error: {json.dumps(error, indent=2)}")
            except:
                print(f"   Response: {response.text}")
            success = False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        success = False
    
    # Test frontend availability
    print("\n3️⃣ Checking frontend...")
    try:
        frontend = requests.get("http://localhost:3000", timeout=5)
        if frontend.status_code == 200:
            print("✅ Frontend is running")
        else:
            print("⚠️  Frontend returned status:", frontend.status_code)
    except:
        print("⚠️  Frontend not accessible (may need to start with: cd flash-frontend && npm start)")
    
    # Cleanup
    api_process.terminate()
    api_process.wait()
    
    # Summary
    print("\n" + "="*60)
    if success:
        print("✅ Integration test PASSED! System is working correctly.")
        print("\n🚀 To use the full system:")
        print("   1. API is ready: cd /Users/sf/Desktop/FLASH && python3 api_server_unified.py")
        print("   2. Frontend is ready: cd flash-frontend && npm start")
        print("   3. Open: http://localhost:3000")
    else:
        print("❌ Integration test failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = test_integration()
    exit(0 if success else 1)