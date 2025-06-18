#!/usr/bin/env python3
"""
Test the newly integrated system with real models and research-based CAMP
"""

import requests
import json
import time

def test_prediction():
    """Test a prediction with the new system"""
    
    # Test data for a Series A startup
    test_data = {
        "total_capital_raised_usd": 10000000,
        "cash_on_hand_usd": 6000000,
        "monthly_burn_usd": 400000,
        "runway_months": 15,
        "burn_multiple": 1.8,
        "investor_tier_primary": "Tier 1",
        "has_debt": False,
        "patent_count": 5,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,
        "switching_cost_score": 4,
        "brand_strength_score": 3,
        "scalability_score": 5,
        "sector": "SaaS",
        "tam_size_usd": 10000000000,
        "sam_size_usd": 1000000000,
        "som_size_usd": 100000000,
        "market_growth_rate_percent": 45,
        "customer_count": 500,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 25,
        "net_dollar_retention_percent": 125,
        "competition_intensity": 3,
        "competitors_named_count": 15,
        "founders_count": 3,
        "team_size_full_time": 45,
        "years_experience_avg": 12,
        "domain_expertise_years_avg": 8,
        "prior_startup_experience_count": 4,
        "prior_successful_exits_count": 2,
        "board_advisor_experience_score": 4,
        "advisors_count": 6,
        "team_diversity_percent": 45,
        "key_person_dependency": False,
        "product_stage": "Growth",
        "product_retention_30d": 85,
        "product_retention_90d": 70,
        "dau_mau_ratio": 0.5,
        "annual_revenue_run_rate": 6000000,
        "revenue_growth_rate_percent": 180,
        "gross_margin_percent": 80,
        "ltv_cac_ratio": 4.2,
        "funding_stage": "Series A"
    }
    
    print("🚀 Testing FLASH with New Real Models")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8001/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test prediction
    print("\n2. Testing prediction with Series A startup...")
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Status: {response.status_code}")
            print("\n   Results:")
            print(f"   - Success Probability: {result.get('success_probability', 'N/A'):.1%}")
            print(f"   - Verdict: {result.get('verdict', 'N/A')}")
            print(f"   - Confidence: {result.get('confidence_score', 'N/A'):.1%}")
            
            # Check CAMP scores
            if 'camp_scores' in result:
                print("\n   CAMP Analysis:")
                scores = result['camp_scores']
                for pillar, score in scores.items():
                    print(f"   - {pillar.title()}: {score:.2f}")
            
            # Check if stage-specific weights are being used
            if 'camp_analysis' in result:
                analysis = result['camp_analysis']
                if 'stage_weights' in analysis:
                    print("\n   Stage-Specific Weights (Series A):")
                    for pillar, weight in analysis['stage_weights'].items():
                        print(f"   - {pillar.title()}: {weight:.0%}")
            
            # Show insights
            if 'insights' in result:
                print("\n   Key Insights:")
                for insight in result['insights'][:5]:
                    print(f"   - {insight}")
        else:
            print(f"   Error: Status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test CAMP endpoint directly
    print("\n3. Testing CAMP calculation...")
    try:
        # First check if the endpoint exists
        response = requests.post(
            "http://localhost:8001/calculate_camp",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ CAMP calculation endpoint working")
        elif response.status_code == 404:
            print("   ℹ️ CAMP calculation endpoint not found (expected)")
        else:
            print(f"   Status: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("\nKey things to verify:")
    print("1. ML models predict success probability (not hardcoded)")
    print("2. CAMP weights are stage-specific (Series A = Market focused)")
    print("3. No more hardcoded values in the response")

if __name__ == "__main__":
    test_prediction()