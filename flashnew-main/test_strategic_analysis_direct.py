#!/usr/bin/env python3
"""
Direct test of the Michelin Strategic Analysis implementation
"""

import asyncio
import json
import sys
sys.path.insert(0, '.')

from api_michelin_strategic_analysis import (
    analyze_phase1_current_state,
    analyze_phase2_strategic_direction,
    analyze_phase3_implementation
)

async def test_strategic_analysis():
    """Test the strategic analysis functions directly"""
    
    # Test data
    startup_data = {
        "company_name": "TechVenture AI",
        "sector": "artificial-intelligence", 
        "funding_stage": "seed",
        "annual_revenue_run_rate": 500000,
        "revenue_growth_rate_percent": 150,
        "monthly_burn_usd": 75000,
        "runway_months": 18,
        "team_size_full_time": 12,
        "customer_count": 25,
        "tam_size_usd": 50000000000,
        "sam_size_usd": 5000000000,
        "som_size_usd": 500000000,
        "market_growth_rate_percent": 45,
        "competition_intensity": 4,
        "patent_count": 2,
        "domain_expertise_years": 8
    }
    
    print("=" * 80)
    print("Testing Michelin Strategic Analysis Functions")
    print("=" * 80)
    
    try:
        # Test Phase 1
        print("\n1. Testing Phase 1: Where Are We Now?")
        print("-" * 40)
        phase1 = await analyze_phase1_current_state(startup_data)
        print(f"✅ Phase 1 Complete")
        print(f"   BCG Position: {phase1.bcg_matrix.position}")
        print(f"   Industry Attractiveness: {phase1.porters_five_forces.overall_industry_attractiveness}")
        print(f"   Strategic Priorities: {len(phase1.swot_analysis.strategic_priorities)} identified")
        
        # Test Phase 2
        print("\n2. Testing Phase 2: Where Should We Go?")
        print("-" * 40)
        phase2 = await analyze_phase2_strategic_direction(startup_data, phase1)
        print(f"✅ Phase 2 Complete")
        print(f"   Recommended Strategy: {phase2.ansoff_matrix.recommended_strategy}")
        print(f"   Growth Scenarios: {len(phase2.growth_scenarios)} scenarios")
        
        # Test Phase 3
        print("\n3. Testing Phase 3: How to Get There?")
        print("-" * 40)
        phase3 = await analyze_phase3_implementation(startup_data, phase2)
        print(f"✅ Phase 3 Complete")
        print(f"   Balanced Scorecard Perspectives: {len(phase3.balanced_scorecard)}")
        print(f"   OKR Quarters: {len(phase3.okr_framework)}")
        print(f"   Risk Mitigation Items: {len(phase3.risk_mitigation_plan)}")
        
        # Save complete analysis
        complete_analysis = {
            "test_date": datetime.now().isoformat(),
            "startup_data": startup_data,
            "phase1": phase1.dict(),
            "phase2": phase2.dict(),
            "phase3": phase3.dict()
        }
        
        with open("strategic_analysis_test_result.json", "w") as f:
            json.dump(complete_analysis, f, indent=2)
        
        print("\n" + "=" * 80)
        print("✅ All tests passed successfully!")
        print("Complete analysis saved to: strategic_analysis_test_result.json")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(test_strategic_analysis())