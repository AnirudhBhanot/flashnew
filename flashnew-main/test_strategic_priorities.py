#!/usr/bin/env python3
"""
Test that strategic priorities are included in Phase 1 response
"""

import requests
import json

# Test data
test_data = {
    "startup_data": {
        "startup_name": "TestCo",
        "sector": "technology",
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 800000,
        "monthly_burn_usd": 100000,
        "runway_months": 8,  # Short runway to trigger priority
        "team_size_full_time": 5,
        "market_size_usd": 10000000000,
        "market_growth_rate_annual": 25,
        "competitor_count": 150,
        "market_share_percentage": 0.05,  # Low market share
        "customer_acquisition_cost_usd": 2000,
        "lifetime_value_usd": 5000,  # 2.5x LTV/CAC
        "monthly_active_users": 1000,
        "product_stage": "beta",
        "proprietary_tech": False,  # No proprietary tech
        "patents_filed": 0,
        "founders_industry_experience_years": 10,
        "b2b_or_b2c": "b2b",
        "burn_rate_usd": 100000,
        "investor_tier_primary": "tier_2",
        "customer_count": 10,
        "geographical_focus": "domestic",
        "revenue_growth_rate": 50,
        "gross_margin": 60,
        "net_promoter_score": 7,
        "technology_readiness_level": 6,
        "has_strategic_partnerships": False,
        "customer_concentration": 30,
        "annual_revenue_usd": 50000
    },
    "include_financial_projections": True,
    "analysis_depth": "comprehensive"
}

print("Testing Strategic Priorities in Phase 1...")
print("="*50)

url = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"
response = requests.post(url, json=test_data)

if response.status_code == 200:
    data = response.json()
    phase1 = data['phase1']
    
    print("✅ Phase 1 request successful!")
    print("\nSWOT Analysis structure:")
    print(f"- Strengths: {len(phase1['swot_analysis']['strengths'])} items")
    print(f"- Weaknesses: {len(phase1['swot_analysis']['weaknesses'])} items")
    print(f"- Opportunities: {len(phase1['swot_analysis']['opportunities'])} items")
    print(f"- Threats: {len(phase1['swot_analysis']['threats'])} items")
    
    # Check for strategic priorities
    if 'strategic_priorities' in phase1['swot_analysis']:
        print(f"\n✅ Strategic Priorities found! ({len(phase1['swot_analysis']['strategic_priorities'])} items)")
        print("\nStrategic Priorities:")
        for i, priority in enumerate(phase1['swot_analysis']['strategic_priorities'], 1):
            print(f"{i}. {priority}")
    else:
        print("\n❌ Strategic Priorities NOT FOUND in response!")
        print("Available keys in swot_analysis:", list(phase1['swot_analysis'].keys()))
    
    # Show sample SWOT items
    print("\nSample Weakness (should trigger priority):")
    if phase1['swot_analysis']['weaknesses']:
        weakness = phase1['swot_analysis']['weaknesses'][0]
        print(f"- {weakness['point']}: {weakness['evidence']}")
    
else:
    print(f"❌ Request failed with status {response.status_code}")
    print("Error:", response.text)

print("\n" + "="*50)