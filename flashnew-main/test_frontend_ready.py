#!/usr/bin/env python3
"""
Test that Phase 1 returns all required fields for frontend
"""

import requests
import json

# Test data matching what frontend uses
test_data = {
    "startup_data": {
        "startup_name": "CryptoEasy Trading",
        "sector": "technology", 
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 500000,
        "market_size_usd": 10000000000,
        "market_growth_rate_annual": 20,
        "competitor_count": 5,
        "market_share_percentage": 0.1,
        "team_size_full_time": 10,
        "customer_count": 10,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 10000,
        "monthly_active_users": 1000,
        "proprietary_tech": False,
        "patents_filed": 0,
        "founders_industry_experience_years": 5,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 50000,
        "monthly_burn_usd": 50000,
        "runway_months": 10,
        "product_stage": "beta",
        "investor_tier_primary": "tier_2",
        "revenue_growth_rate": 0,
        "gross_margin": 70,
        "annual_revenue_usd": 0
    },
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

print("Testing Frontend Compatibility...")
print("="*60)

url = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"
response = requests.post(url, json=test_data)

if response.status_code == 200:
    data = response.json()
    phase1 = data['phase1']
    
    print("✅ Phase 1 Response Structure:")
    
    # Check required fields
    required_checks = [
        ("executive_summary", "executive_summary" in phase1),
        ("bcg_matrix_analysis", "bcg_matrix_analysis" in phase1),
        ("bcg_matrix_analysis.position", "position" in phase1.get("bcg_matrix_analysis", {})),
        ("bcg_matrix_analysis.strategic_implications", "strategic_implications" in phase1.get("bcg_matrix_analysis", {})),
        ("porters_five_forces", "porters_five_forces" in phase1),
        ("swot_analysis", "swot_analysis" in phase1),
        ("swot_analysis.strengths", "strengths" in phase1.get("swot_analysis", {})),
        ("swot_analysis.weaknesses", "weaknesses" in phase1.get("swot_analysis", {})),
        ("swot_analysis.opportunities", "opportunities" in phase1.get("swot_analysis", {})),
        ("swot_analysis.threats", "threats" in phase1.get("swot_analysis", {})),
        ("swot_analysis.strategic_priorities", "strategic_priorities" in phase1.get("swot_analysis", {})),
        ("current_position_narrative", "current_position_narrative" in phase1)
    ]
    
    all_good = True
    for field, exists in required_checks:
        status = "✅" if exists else "❌"
        print(f"{status} {field}: {'Present' if exists else 'MISSING'}")
        if not exists:
            all_good = False
    
    if all_good:
        print("\n✅ All required fields present! Frontend should work.")
    else:
        print("\n❌ Some required fields missing. Frontend may have errors.")
    
    # Show strategic priorities
    if "strategic_priorities" in phase1.get("swot_analysis", {}):
        print("\nStrategic Priorities:")
        for i, priority in enumerate(phase1['swot_analysis']['strategic_priorities'], 1):
            print(f"{i}. {priority}")
    
else:
    print(f"❌ Request failed with status {response.status_code}")
    print("Error:", response.text)

print("\n" + "="*60)