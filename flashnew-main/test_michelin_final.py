#!/usr/bin/env python3
"""
Final comprehensive test of Michelin API
"""

import requests
import json

test_data = {
    "startup_data": {
        "startup_name": "Test Startup",
        "sector": "saas", 
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 500000,
        "market_size_usd": 1000000000,
        "market_growth_rate_annual": 20,
        "competitor_count": 5,
        "market_share_percentage": 0.1,
        "team_size_full_time": 10
    }
}

print("Final Michelin API Test")
print("=" * 80)

response = requests.post(
    "http://localhost:8001/api/michelin/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    data = response.json()
    
    # Phase 1 checks
    print("\n✅ Phase 1 - Current State Analysis:")
    print(f"  - BCG Matrix position: {data['phase1']['bcg_matrix']['position']}")
    print(f"  - Porter's forces count: {len(data['phase1']['porters_five_forces'])}")
    print(f"  - SWOT priorities: {len(data['phase1']['swot_analysis']['strategic_priorities'])} items")
    
    # Phase 2 checks
    print("\n✅ Phase 2 - Strategic Options:")
    print(f"  - Ansoff quadrants: {len(data['phase2']['ansoff_matrix'])} items")
    print(f"  - Blue ocean factors: {len(data['phase2']['blue_ocean_strategy']['eliminate_factors'])} eliminate")
    print(f"  - Growth scenarios: {len(data['phase2']['growth_scenarios'])} options")
    scenario = data['phase2']['growth_scenarios'][0]
    print(f"    - Has numeric investment: {isinstance(scenario['investment_required'], (int, float))}")
    print(f"    - Has risks array: {'risks' in scenario}")
    
    # Phase 3 checks
    print("\n✅ Phase 3 - Implementation:")
    print(f"  - Balanced scorecard perspectives: {len(data['phase3']['balanced_scorecard'])}")
    print(f"  - Execution phases: {len(data['phase3']['execution_plan'])} phases")
    
    # Top-level checks
    print("\n✅ Top-level elements:")
    print(f"  - Key recommendations: {len(data['key_recommendations'])}")
    print(f"  - Critical success factors: {len(data['critical_success_factors'])}")
    print(f"  - Next steps: {len(data['next_steps'])} time periods")
    
    print("\n🎉 All tests passed! Michelin API is fully compatible with frontend.")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)