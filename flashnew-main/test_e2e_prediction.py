#!/usr/bin/env python3
"""
Test end-to-end prediction flow
"""
import subprocess
import time
import requests
import json

print("Testing End-to-End Prediction Flow")
print("=" * 60)

# Start API server
process = subprocess.Popen(
    ["python3", "api_server_unified.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for startup
time.sleep(3)

if process.poll() is not None:
    print("❌ API server failed to start")
    stdout, stderr = process.communicate()
    print(stderr)
    exit(1)

print("✅ API server started")

# Test data - simulating frontend input
test_startup = {
    # Capital features
    "total_capital_raised_usd": 5000000,
    "funding_stage": "Series A",  # Frontend format
    "cash_on_hand_usd": 2000000,
    "monthly_burn_usd": 200000,
    
    # Advantage features  
    "tech_differentiation_score": 4,
    "has_strategic_partnerships": True,  # Boolean
    "patent_count": 2,
    "switching_cost_score": 3,
    
    # Market features
    "total_addressable_market_usd": 10000000000,
    "market_growth_rate_percent": 25,
    "sector": "Enterprise SaaS",  # Frontend format
    "user_growth_rate_percent": 150,
    
    # People features
    "founders_count": 2,
    "team_size_full_time": 25,
    "prior_successful_exits_count": 1,
    "years_experience_avg": 10,
    
    # Product features
    "product_stage": "Growth",  # Frontend format
    "product_retention_30d": 0.85,  # As decimal
    "revenue_growth_rate_percent": 200,
    "gross_margin_percent": 75,
    
    # Frontend-only fields
    "startup_name": "TestCorp",
    "hq_location": "San Francisco"
}

# Add all required fields with defaults
all_fields = {
    "sector": "enterprise_saas",
    "funding_stage": "series_a", 
    "total_capital_raised_usd": 5000000,
    "cash_on_hand_usd": 2000000,
    "monthly_burn_usd": 200000,
    "runway_months": 10,
    "burn_multiple": 2.5,
    "tech_differentiation_score": 4,
    "patent_count": 2,
    "has_strategic_partnerships": True,
    "switching_cost_score": 3,
    "has_network_effects": False,
    "brand_strength_score": 3,
    "scalability_score": 4,
    "total_addressable_market_usd": 10000000000,
    "serviceable_addressable_market_usd": 1000000000,
    "serviceable_obtainable_market_usd": 100000000,
    "market_growth_rate_percent": 25,
    "investor_tier_primary": "tier_1",
    "user_growth_rate_percent": 150,
    "customers_count": 100,
    "net_promoter_score": 45,
    "payback_period_months": 12,
    "time_to_revenue_months": 6,
    "customer_acquisition_cost": 1000,
    "net_dollar_retention_percent": 110,
    "competition_intensity": 3,
    "competitors_named_count": 5,
    "founders_count": 2,
    "team_size_full_time": 25,
    "years_experience_avg": 10,
    "domain_expertise_years_avg": 8,
    "prior_startup_experience_count": 2,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 4,
    "advisors_count": 3,
    "team_diversity_percent": 40,
    "key_person_dependency": False,
    "product_stage": "growth",
    "product_retention_30d": 0.85,
    "product_retention_90d": 0.75,
    "dau_mau_ratio": 0.6,
    "annual_revenue_run_rate": 2400000,
    "revenue_growth_rate_percent": 200,
    "gross_margin_percent": 75,
    "ltv_cac_ratio": 3.5
}

# Override with test data
all_fields.update(test_startup)

try:
    # Test prediction endpoint
    print("\nTesting /predict endpoint...")
    response = requests.post(
        "http://localhost:8001/predict",
        json=all_fields,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Prediction successful!")
        print(f"\nResults:")
        prob = result.get('success_probability', 'N/A')
        print(f"  Success Probability: {prob:.2%}" if isinstance(prob, (int, float)) else f"  Success Probability: {prob}")
        
        conf_interval = result.get('confidence_interval', {})
        if conf_interval:
            print(f"  Confidence Interval: [{conf_interval.get('lower', 0):.2%}, {conf_interval.get('upper', 0):.2%}]")
        
        print(f"  Verdict: {result.get('verdict', 'N/A')}")
        
        if 'camp_scores' in result:
            print(f"\nCAMP Scores:")
            for pillar, score in result['camp_scores'].items():
                print(f"  {pillar.capitalize()}: {score:.2f}")
        
        # Check if we're getting real predictions (not 0.5)
        prob = result.get('success_probability', 0.5)
        if 0.49 < prob < 0.51:
            print("\n⚠️  WARNING: Probability is exactly 0.5 - might be using fallback!")
        else:
            print("\n✅ Getting real predictions (not hardcoded 0.5)!")
            
    else:
        print(f"❌ Prediction failed with status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error making request: {e}")

finally:
    # Stop server
    process.terminate()
    process.wait()
    print("\n✅ API server stopped")

print("=" * 60)