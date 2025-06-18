#!/usr/bin/env python3
"""
Debug script for Phase 2 Michelin Analysis
Tests the decomposed Phase 2 endpoint directly
"""

import requests
import json
import time

# Test startup data
startup_data = {
    "startup_name": "TestStartup Phase2 Debug",
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

print("Phase 2 Michelin Analysis Debug")
print("="*60)

# Step 1: Get Phase 1 results first
print("\n1. Getting Phase 1 results...")
phase1_url = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"

phase1_request = {
    "startup_data": startup_data,
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

try:
    phase1_response = requests.post(phase1_url, json=phase1_request)
    print(f"Phase 1 Status: {phase1_response.status_code}")
    
    if phase1_response.status_code != 200:
        print(f"Phase 1 Error: {phase1_response.text}")
        exit(1)
    
    phase1_data = phase1_response.json()
    print("✅ Phase 1 completed successfully")
    print(f"BCG Position: {phase1_data['phase1']['bcg_matrix_analysis']['position']}")
    
except Exception as e:
    print(f"Phase 1 Exception: {e}")
    exit(1)

# Step 2: Test Phase 2 with Phase 1 results
print("\n2. Testing Phase 2...")
phase2_url = "http://localhost:8001/api/michelin/decomposed/analyze/phase2"

phase2_request = {
    "startup_data": startup_data,
    "phase1_results": phase1_data["phase1"]
}

print(f"\nPhase 2 Request URL: {phase2_url}")
print(f"Phase 2 Request Body (truncated):")
print(json.dumps({
    "startup_data": {"startup_name": startup_data["startup_name"]},
    "phase1_results": {"executive_summary": phase1_data["phase1"]["executive_summary"][:100] + "..."}
}, indent=2))

try:
    start_time = time.time()
    phase2_response = requests.post(phase2_url, json=phase2_request, timeout=300)
    end_time = time.time()
    
    print(f"\nPhase 2 Status: {phase2_response.status_code}")
    print(f"Response Time: {end_time - start_time:.2f} seconds")
    
    if phase2_response.status_code == 200:
        phase2_data = phase2_response.json()
        print("\n✅ Phase 2 completed successfully!")
        
        # Display key results
        print("\nPhase 2 Results:")
        print("-" * 40)
        
        if "phase2" in phase2_data:
            phase2_content = phase2_data["phase2"]
            
            # Strategic options overview
            if "strategic_options_overview" in phase2_content:
                print(f"\nStrategic Options Overview:")
                print(phase2_content["strategic_options_overview"])
            
            # Ansoff Matrix
            if "ansoff_matrix_analysis" in phase2_content:
                ansoff = phase2_content["ansoff_matrix_analysis"]
                print(f"\nAnsoff Recommended Strategy: {ansoff.get('recommended_strategy', 'N/A')}")
                print(f"Rationale: {ansoff.get('rationale', 'N/A')}")
            
            # Blue Ocean
            if "blue_ocean_strategy" in phase2_content:
                blue_ocean = phase2_content["blue_ocean_strategy"]
                print(f"\nBlue Ocean Opportunities: {len(blue_ocean.get('opportunities', []))}")
                if blue_ocean.get('opportunities'):
                    print(f"First opportunity: {blue_ocean['opportunities'][0]}")
            
            # Growth Scenarios
            if "growth_scenarios" in phase2_content:
                scenarios = phase2_content["growth_scenarios"]
                print(f"\nGrowth Scenarios: {len(scenarios)}")
                for scenario in scenarios[:1]:  # Show first scenario
                    print(f"- {scenario.get('scenario_name', 'N/A')}: ${scenario.get('12_month_revenue_projection', 0):,.0f}")
            
            # Recommended direction
            if "recommended_direction" in phase2_content:
                print(f"\nRecommended Direction:")
                print(phase2_content["recommended_direction"])
        
        # Save full response for inspection
        with open("phase2_debug_response.json", "w") as f:
            json.dump(phase2_data, f, indent=2)
        print("\n💾 Full response saved to phase2_debug_response.json")
        
    else:
        print(f"\n❌ Phase 2 failed with status {phase2_response.status_code}")
        print(f"Error response:")
        print(phase2_response.text)
        
        # Try to parse error details
        try:
            error_data = phase2_response.json()
            print(f"\nError details: {json.dumps(error_data, indent=2)}")
        except:
            print("Could not parse error response as JSON")
            
except requests.exceptions.Timeout:
    print("\n⏱️ Phase 2 request timed out after 300 seconds")
    print("This suggests the API is hanging or taking too long to process")
    
except requests.exceptions.ConnectionError as e:
    print(f"\n🔌 Connection error: {e}")
    print("Is the API server running on port 8001?")
    
except Exception as e:
    print(f"\n❌ Phase 2 Exception: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Debug session complete")