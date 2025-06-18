#!/usr/bin/env python3
"""
Test Michelin API structure matches frontend expectations
"""

import requests
import json

# Test data
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

print("Testing Michelin API structure...")
print("=" * 80)

response = requests.post(
    "http://localhost:8001/api/michelin/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    data = response.json()
    
    # Check Phase 1 structure
    print("✅ Phase 1 Structure:")
    assert "bcg_matrix" in data["phase1"], "Missing bcg_matrix"
    assert "position" in data["phase1"]["bcg_matrix"], "Missing bcg_matrix.position"
    assert "market_growth" in data["phase1"]["bcg_matrix"], "Missing bcg_matrix.market_growth"
    assert "strategic_implications" in data["phase1"]["bcg_matrix"], "Missing bcg_matrix.strategic_implications"
    assert isinstance(data["phase1"]["bcg_matrix"]["strategic_implications"], list), "strategic_implications should be list"
    print("  - BCG Matrix: OK")
    
    assert "porters_five_forces" in data["phase1"], "Missing porters_five_forces"
    assert "threat_of_new_entrants" in data["phase1"]["porters_five_forces"], "Missing threat_of_new_entrants"
    assert "intensity" in data["phase1"]["porters_five_forces"]["threat_of_new_entrants"], "Missing intensity"
    assert "score" in data["phase1"]["porters_five_forces"]["threat_of_new_entrants"], "Missing score"
    assert "factors" in data["phase1"]["porters_five_forces"]["threat_of_new_entrants"], "Missing factors"
    print("  - Porter's Five Forces: OK")
    
    assert "swot_analysis" in data["phase1"], "Missing swot_analysis"
    assert "strengths" in data["phase1"]["swot_analysis"], "Missing strengths"
    assert all("item" in s for s in data["phase1"]["swot_analysis"]["strengths"]), "Missing item in strengths"
    assert all("item" in w for w in data["phase1"]["swot_analysis"]["weaknesses"]), "Missing item in weaknesses"
    print("  - SWOT Analysis: OK")
    
    # Check Phase 2 structure
    print("\n✅ Phase 2 Structure:")
    assert "ansoff_matrix" in data["phase2"], "Missing ansoff_matrix"
    assert "market_penetration" in data["phase2"]["ansoff_matrix"], "Missing market_penetration"
    assert "strategy" in data["phase2"]["ansoff_matrix"]["market_penetration"], "Missing strategy"
    assert "investment" in data["phase2"]["ansoff_matrix"]["market_penetration"], "Missing investment"
    assert isinstance(data["phase2"]["ansoff_matrix"]["market_penetration"]["investment"], (int, float)), "investment should be number"
    print("  - Ansoff Matrix: OK")
    
    assert "blue_ocean_strategy" in data["phase2"], "Missing blue_ocean_strategy"
    assert "eliminate_factors" in data["phase2"]["blue_ocean_strategy"], "Missing eliminate_factors"
    assert isinstance(data["phase2"]["blue_ocean_strategy"]["eliminate_factors"], list), "eliminate_factors should be list"
    print("  - Blue Ocean Strategy: OK")
    
    # Check Phase 3 structure
    print("\n✅ Phase 3 Structure:")
    assert "balanced_scorecard" in data["phase3"], "Missing balanced_scorecard"
    assert isinstance(data["phase3"]["balanced_scorecard"], list), "balanced_scorecard should be list"
    if data["phase3"]["balanced_scorecard"]:
        assert "perspective" in data["phase3"]["balanced_scorecard"][0], "Missing perspective"
        assert "objectives" in data["phase3"]["balanced_scorecard"][0], "Missing objectives"
    print("  - Balanced Scorecard: OK")
    
    print("\n✅ All structure tests passed!")
    print("\nThe Michelin API is now compatible with the frontend!")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)