#!/usr/bin/env python3
import requests
import json
import time

# Test data
test_data = {
    "startup_data": {
        "startup_name": "TestStartup",
        "sector": "technology",
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 800000,
        "monthly_burn_usd": 50000,
        "runway_months": 16,
        "team_size_full_time": 5,
        "market_size_usd": 10000000000,
        "market_growth_rate_annual": 25,
        "competitor_count": 150,
        "market_share_percentage": 0.1,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 10000,
        "monthly_active_users": 100000,
        "product_stage": "beta",
        "proprietary_tech": False,
        "patents_filed": 0,
        "founders_industry_experience_years": 10,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 50000,
        "investor_tier_primary": "tier_2",
        "customer_count": 50,
        "geographical_focus": "domestic",
        "revenue_growth_rate": 150,
        "gross_margin": 70,
        "net_promoter_score": 8,
        "technology_readiness_level": 6,
        "has_strategic_partnerships": True,
        "customer_concentration": 15,
        "annual_revenue_usd": 100000
    },
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

print("Testing Decomposed Michelin Analysis - All Phases")
print("="*60)

# Phase 1
print("\n1. Testing Phase 1...")
url_phase1 = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"
start_time = time.time()
response1 = requests.post(url_phase1, json=test_data)
phase1_time = time.time() - start_time

if response1.status_code == 200:
    phase1_data = response1.json()
    print(f"✅ Phase 1 Success! ({phase1_time:.1f}s)")
    print(f"   BCG Position: {phase1_data['phase1']['bcg_matrix_analysis']['position']}")
    print(f"   SWOT items: S:{len(phase1_data['phase1']['swot_analysis']['strengths'])}, W:{len(phase1_data['phase1']['swot_analysis']['weaknesses'])}, O:{len(phase1_data['phase1']['swot_analysis']['opportunities'])}, T:{len(phase1_data['phase1']['swot_analysis']['threats'])}")
    
    # Phase 2
    print("\n2. Testing Phase 2...")
    phase2_request = {
        "startup_data": test_data["startup_data"],
        "phase1_results": phase1_data["phase1"]
    }
    
    url_phase2 = "http://localhost:8001/api/michelin/decomposed/analyze/phase2"
    start_time = time.time()
    response2 = requests.post(url_phase2, json=phase2_request)
    phase2_time = time.time() - start_time
    
    if response2.status_code == 200:
        phase2_data = response2.json()
        print(f"✅ Phase 2 Success! ({phase2_time:.1f}s)")
        print(f"   Ansoff Strategy: {phase2_data['phase2']['ansoff_matrix_analysis']['recommended_strategy']}")
        print(f"   Blue Ocean Opportunities: {len(phase2_data['phase2']['blue_ocean_strategy']['opportunities'])}")
        print(f"   Growth Scenarios: {len(phase2_data['phase2']['growth_scenarios'])}")
        
        # Phase 3
        print("\n3. Testing Phase 3...")
        phase3_request = {
            "startup_data": test_data["startup_data"],
            "phase1_results": phase1_data["phase1"],
            "phase2_results": phase2_data["phase2"]
        }
        
        url_phase3 = "http://localhost:8001/api/michelin/decomposed/analyze/phase3"
        start_time = time.time()
        response3 = requests.post(url_phase3, json=phase3_request)
        phase3_time = time.time() - start_time
        
        if response3.status_code == 200:
            phase3_data = response3.json()
            print(f"✅ Phase 3 Success! ({phase3_time:.1f}s)")
            print(f"   Balanced Scorecard perspectives: {len(phase3_data['phase3']['balanced_scorecard'])}")
            print(f"   OKR objectives: {len(phase3_data['phase3']['okr_framework']['objectives'])}")
            print(f"   Success metrics: {len(phase3_data['phase3']['success_metrics'])}")
            print(f"   Risk categories: {len(phase3_data['phase3']['risk_mitigation_plan'])}")
            
            # Show sample implementation roadmap
            print("\n📋 Implementation Roadmap Preview:")
            roadmap = phase3_data['phase3']['implementation_roadmap']
            print(f"   {roadmap[:200]}...")
            
            # Total time
            total_time = phase1_time + phase2_time + phase3_time
            print(f"\n⏱️  Total analysis time: {total_time:.1f} seconds")
            print(f"   Average per phase: {total_time/3:.1f} seconds")
            
        else:
            print(f"❌ Phase 3 Failed: {response3.status_code}")
            print(f"Error: {response3.text}")
    else:
        print(f"❌ Phase 2 Failed: {response2.status_code}")
        print(f"Error: {response2.text}")
else:
    print(f"❌ Phase 1 Failed: {response1.status_code}")
    print(f"Error: {response1.text}")

print("\n" + "="*60)
print("Test complete!")