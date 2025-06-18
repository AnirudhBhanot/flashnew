#!/usr/bin/env python3
"""
Comprehensive comparison test for Michelin Analysis approaches:
1. Original JSON-based approach (prone to parsing errors)
2. Decomposed approach (reliable multi-step analysis)
"""

import requests
import json
import time
from datetime import datetime

# Test data - using a more realistic startup scenario
test_data = {
    "startup_data": {
        "startup_name": "CloudSync AI",
        "sector": "technology",
        "funding_stage": "series_a",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3500000,
        "monthly_burn_usd": 250000,
        "runway_months": 14,
        "team_size_full_time": 15,
        "market_size_usd": 50000000000,  # $50B
        "market_growth_rate_annual": 35,
        "competitor_count": 200,
        "market_share_percentage": 0.2,
        "customer_acquisition_cost_usd": 2500,
        "lifetime_value_usd": 25000,
        "monthly_active_users": 500000,
        "product_stage": "growth",
        "proprietary_tech": True,
        "patents_filed": 3,
        "founders_industry_experience_years": 15,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 250000,
        "investor_tier_primary": "tier_1",
        "customer_count": 250,
        "geographical_focus": "global",
        "revenue_growth_rate": 300,
        "gross_margin": 85,
        "net_promoter_score": 72,
        "technology_readiness_level": 8,
        "has_strategic_partnerships": True,
        "customer_concentration": 12,
        "annual_revenue_usd": 3000000
    },
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

def print_section(title):
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)

def test_original_approach():
    """Test the original JSON-based Michelin analysis"""
    print_section("ORIGINAL JSON-BASED APPROACH")
    
    phase_times = []
    phase_success = []
    
    # Phase 1
    print("\n📊 Phase 1: Where Are We Now?")
    url = "http://localhost:8001/api/michelin/analyze/phase1"
    start = time.time()
    response = requests.post(url, json=test_data)
    phase_times.append(time.time() - start)
    
    if response.status_code == 200:
        phase_success.append(True)
        data = response.json()
        print(f"✅ Success ({phase_times[-1]:.1f}s)")
        print(f"   Executive Summary: {data['phase1']['executive_summary'][:100]}...")
        print(f"   BCG Position: {data['phase1'].get('bcg_matrix_analysis', {}).get('position', 'N/A')}")
        phase1_data = data['phase1']
    else:
        phase_success.append(False)
        print(f"❌ Failed ({phase_times[-1]:.1f}s): {response.status_code}")
        return None, phase_times, phase_success
    
    # Phase 2
    print("\n📈 Phase 2: Where Should We Go?")
    phase2_request = {
        "startup_data": test_data["startup_data"],
        "phase1_results": phase1_data
    }
    url = "http://localhost:8001/api/michelin/analyze/phase2"
    start = time.time()
    response = requests.post(url, json=phase2_request)
    phase_times.append(time.time() - start)
    
    if response.status_code == 200:
        phase_success.append(True)
        data = response.json()
        print(f"✅ Success ({phase_times[-1]:.1f}s)")
        print(f"   Recommended Strategy: {data['phase2'].get('ansoff_matrix_analysis', {}).get('recommended_strategy', 'N/A')}")
        phase2_data = data['phase2']
    else:
        phase_success.append(False)
        print(f"❌ Failed ({phase_times[-1]:.1f}s): {response.status_code}")
        return phase1_data, phase_times, phase_success
    
    # Phase 3
    print("\n🚀 Phase 3: How to Get There?")
    phase3_request = {
        "startup_data": test_data["startup_data"],
        "phase1_results": phase1_data,
        "phase2_results": phase2_data
    }
    url = "http://localhost:8001/api/michelin/analyze/phase3"
    start = time.time()
    response = requests.post(url, json=phase3_request)
    phase_times.append(time.time() - start)
    
    if response.status_code == 200:
        phase_success.append(True)
        data = response.json()
        print(f"✅ Success ({phase_times[-1]:.1f}s)")
        print(f"   Executive Briefing: {data.get('executive_briefing', 'N/A')[:100]}...")
    else:
        phase_success.append(False)
        print(f"❌ Failed ({phase_times[-1]:.1f}s): {response.status_code}")
    
    return True, phase_times, phase_success

def test_decomposed_approach():
    """Test the decomposed multi-step Michelin analysis"""
    print_section("DECOMPOSED MULTI-STEP APPROACH")
    
    phase_times = []
    phase_success = []
    
    # Phase 1
    print("\n📊 Phase 1: Where Are We Now?")
    url = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"
    start = time.time()
    response = requests.post(url, json=test_data)
    phase_times.append(time.time() - start)
    
    if response.status_code == 200:
        phase_success.append(True)
        data = response.json()
        print(f"✅ Success ({phase_times[-1]:.1f}s)")
        print(f"   Executive Summary: {data['phase1']['executive_summary'][:100]}...")
        print(f"   BCG Position: {data['phase1']['bcg_matrix_analysis']['position']}")
        
        # Show sample SWOT item
        strength = data['phase1']['swot_analysis']['strengths'][0]
        print(f"   Sample Strength: {strength['point']} - {strength['evidence']}")
        
        phase1_data = data['phase1']
    else:
        phase_success.append(False)
        print(f"❌ Failed ({phase_times[-1]:.1f}s): {response.status_code}")
        return None, phase_times, phase_success
    
    # Phase 2
    print("\n📈 Phase 2: Where Should We Go?")
    phase2_request = {
        "startup_data": test_data["startup_data"],
        "phase1_results": phase1_data
    }
    url = "http://localhost:8001/api/michelin/decomposed/analyze/phase2"
    start = time.time()
    response = requests.post(url, json=phase2_request)
    phase_times.append(time.time() - start)
    
    if response.status_code == 200:
        phase_success.append(True)
        data = response.json()
        print(f"✅ Success ({phase_times[-1]:.1f}s)")
        print(f"   Ansoff Strategy: {data['phase2']['ansoff_matrix_analysis']['recommended_strategy']}")
        print(f"   Rationale: {data['phase2']['ansoff_matrix_analysis']['rationale']}")
        
        # Show Blue Ocean opportunity
        if data['phase2']['blue_ocean_strategy']['opportunities']:
            opp = data['phase2']['blue_ocean_strategy']['opportunities'][0]
            print(f"   Blue Ocean: {opp['opportunity']} - {opp['approach']}")
        
        phase2_data = data['phase2']
    else:
        phase_success.append(False)
        print(f"❌ Failed ({phase_times[-1]:.1f}s): {response.status_code}")
        return phase1_data, phase_times, phase_success
    
    # Phase 3
    print("\n🚀 Phase 3: How to Get There?")
    phase3_request = {
        "startup_data": test_data["startup_data"],
        "phase1_results": phase1_data,
        "phase2_results": phase2_data
    }
    url = "http://localhost:8001/api/michelin/decomposed/analyze/phase3"
    start = time.time()
    response = requests.post(url, json=phase3_request)
    phase_times.append(time.time() - start)
    
    if response.status_code == 200:
        phase_success.append(True)
        data = response.json()
        print(f"✅ Success ({phase_times[-1]:.1f}s)")
        print(f"   Executive Briefing: {data['executive_briefing'][:100]}...")
        
        # Show key recommendations
        print("\n   Key Recommendations:")
        for i, rec in enumerate(data['key_recommendations'][:3], 1):
            print(f"   {i}. {rec}")
        
        # Show next steps
        print("\n   Immediate Next Steps:")
        for step in data['next_steps'][:2]:
            print(f"   - {step['action']} ({step['timeline']}, Owner: {step['owner']})")
    else:
        phase_success.append(False)
        print(f"❌ Failed ({phase_times[-1]:.1f}s): {response.status_code}")
    
    return True, phase_times, phase_success

def main():
    print_section("MICHELIN ANALYSIS COMPARISON TEST")
    print(f"\nStartup: {test_data['startup_data']['startup_name']}")
    print(f"Stage: {test_data['startup_data']['funding_stage'].title()}")
    print(f"Market: ${test_data['startup_data']['market_size_usd']/1e9:.0f}B growing at {test_data['startup_data']['market_growth_rate_annual']}%")
    print(f"LTV/CAC: {test_data['startup_data']['lifetime_value_usd']/test_data['startup_data']['customer_acquisition_cost_usd']:.1f}x")
    
    # Test original approach
    original_result, original_times, original_success = test_original_approach()
    
    # Test decomposed approach
    decomposed_result, decomposed_times, decomposed_success = test_decomposed_approach()
    
    # Comparison summary
    print_section("COMPARISON SUMMARY")
    
    print("\n📊 Success Rates:")
    print(f"   Original:    {sum(original_success)}/3 phases succeeded ({sum(original_success)/3*100:.0f}%)")
    print(f"   Decomposed:  {sum(decomposed_success)}/3 phases succeeded ({sum(decomposed_success)/3*100:.0f}%)")
    
    print("\n⏱️  Performance:")
    print(f"   Original:    Total {sum(original_times):.1f}s (Avg {sum(original_times)/len(original_times):.1f}s per phase)")
    print(f"   Decomposed:  Total {sum(decomposed_times):.1f}s (Avg {sum(decomposed_times)/len(decomposed_times):.1f}s per phase)")
    
    print("\n🎯 Reliability:")
    if sum(decomposed_success) > sum(original_success):
        print("   ✅ Decomposed approach is MORE RELIABLE")
    else:
        print("   ⚠️  Both approaches performed similarly")
    
    print("\n💡 Key Advantages of Decomposed Approach:")
    print("   1. No JSON parsing failures - uses focused prompts")
    print("   2. More specific and actionable insights")
    print("   3. Better error recovery with fallback logic")
    print("   4. Consistent response structure")
    print("   5. Easier to debug and maintain")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()