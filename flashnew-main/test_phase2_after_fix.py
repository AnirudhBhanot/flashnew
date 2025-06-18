#!/usr/bin/env python3
"""
Test Phase 2 after applying timeout fixes
"""

import requests
import json
import time

# Test startup data
startup_data = {
    "startup_name": "TestStartup After Fix",
    "sector": "technology", 
    "funding_stage": "seed",
    "total_capital_raised_usd": 1000000,
    "cash_on_hand_usd": 800000,
    "monthly_burn_usd": 50000,
    "runway_months": 16,
    "team_size_full_time": 10,
    "market_size_usd": 10000000000,
    "market_growth_rate_annual": 25,
    "competitor_count": 50,
    "market_share_percentage": 0.5,
    "customer_acquisition_cost_usd": 1000,
    "lifetime_value_usd": 5000,
    "monthly_active_users": 10000,
    "product_stage": "beta",
    "proprietary_tech": True,
    "patents_filed": 2,
    "founders_industry_experience_years": 10,
    "b2b_or_b2c": "b2b",
    "burn_rate_usd": 50000,
    "investor_tier_primary": "tier_2",
    "customer_count": 100,
    "annual_revenue_usd": 500000,
    "geographical_focus": "domestic",
    "customer_concentration": 20
}

print("Testing Phase 2 after timeout fix")
print("="*50)

# Step 1: Get Phase 1 results
print("\n1. Getting Phase 1 results...")
phase1_url = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"

phase1_request = {
    "startup_data": startup_data,
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

try:
    start_time = time.time()
    phase1_response = requests.post(phase1_url, json=phase1_request, timeout=60)
    phase1_time = time.time() - start_time
    
    print(f"Phase 1 Status: {phase1_response.status_code}")
    print(f"Phase 1 Time: {phase1_time:.2f}s")
    
    if phase1_response.status_code != 200:
        print(f"Phase 1 Error: {phase1_response.text}")
        exit(1)
    
    phase1_data = phase1_response.json()
    print("✅ Phase 1 completed successfully")
    
except Exception as e:
    print(f"Phase 1 Exception: {e}")
    exit(1)

# Step 2: Test Phase 2
print("\n2. Testing Phase 2...")
phase2_url = "http://localhost:8001/api/michelin/decomposed/analyze/phase2"

phase2_request = {
    "startup_data": startup_data,
    "phase1_results": phase1_data["phase1"]
}

try:
    start_time = time.time()
    phase2_response = requests.post(phase2_url, json=phase2_request, timeout=120)
    phase2_time = time.time() - start_time
    
    print(f"Phase 2 Status: {phase2_response.status_code}")
    print(f"Phase 2 Time: {phase2_time:.2f}s")
    
    if phase2_response.status_code == 200:
        phase2_data = phase2_response.json()
        print("\n✅ Phase 2 completed successfully!")
        
        # Show summary
        if "phase2" in phase2_data:
            p2 = phase2_data["phase2"]
            print(f"\nStrategic Overview: {p2.get('strategic_options_overview', 'N/A')[:100]}...")
            
            if "ansoff_matrix_analysis" in p2:
                print(f"Recommended Strategy: {p2['ansoff_matrix_analysis'].get('recommended_strategy', 'N/A')}")
                
            if "growth_scenarios" in p2 and p2["growth_scenarios"]:
                print(f"Growth Scenarios: {len(p2['growth_scenarios'])}")
                
        print("\n✅ Phase 2 is now working correctly with timeout fixes!")
        
    else:
        print(f"\n❌ Phase 2 failed: {phase2_response.status_code}")
        print(f"Error: {phase2_response.text[:500]}")
        
except requests.exceptions.Timeout:
    print(f"\n⏱️ Phase 2 timed out after 120 seconds")
    print("The timeout fix may not be sufficient, or the API server needs restart")
    
except Exception as e:
    print(f"\n❌ Phase 2 Exception: {type(e).__name__}: {e}")

print("\n" + "="*50)
print("Test complete. If Phase 2 still times out, restart the API server.")