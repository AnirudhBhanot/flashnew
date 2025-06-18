#!/usr/bin/env python3
"""
Test Phase 2 Strategic Analysis for FLASH Platform
Building on Phase 1 insights
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def analyze_flash_phase2():
    """Run Phase 2 analysis using Phase 1 results"""
    
    # Load Phase 1 results
    with open("flash_self_analysis.json", "r") as f:
        phase1_results = json.load(f)
    
    # Extract Phase 1 data
    phase1_data = phase1_results["phase1"]
    
    # Prepare Phase 2 request
    phase2_request = {
        "startup_data": {
            "startup_name": "FLASH Platform",
            "sector": "saas_b2b",
            "funding_stage": "seed",
            "total_capital_raised_usd": 2000000,
            "cash_on_hand_usd": 1500000,
            "monthly_burn_usd": 125000,
            "runway_months": 12,
            "team_size_full_time": 8,
            "market_size_usd": 50000000000,
            "market_growth_rate_annual": 15,
            "competitor_count": 12,
            "market_share_percentage": 0.01,
            "customer_acquisition_cost_usd": 10000,
            "lifetime_value_usd": 50000,
            "monthly_active_users": 50,
            "product_stage": "live",
            "proprietary_tech": True,
            "patents_filed": 0,
            "founders_industry_experience_years": 20,
            "b2b_or_b2c": "b2b",
            "burn_rate_usd": 125000,
            "investor_tier_primary": "tier_2",
            "revenue_growth_rate": 0,
            "gross_margin": 85,
            "customer_count": 5,
            "annual_revenue_usd": 0
        },
        "phase1_results": phase1_data
    }
    
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8001/api/michelin/enhanced/analyze/phase2"
        
        print("=" * 60)
        print("FLASH PLATFORM PHASE 2 STRATEGIC ANALYSIS")
        print("Where Should We Go?")
        print("=" * 60)
        
        start_time = datetime.now()
        
        try:
            async with session.post(url, json=phase2_request, timeout=120) as response:
                if response.status == 200:
                    result = await response.json()
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                    
                    print(f"\n✓ Phase 2 Analysis completed in {elapsed_time:.1f} seconds")
                    
                    phase2 = result.get("phase2", {})
                    
                    # Strategic Options Overview
                    print("\n" + "="*60)
                    print("STRATEGIC OPTIONS OVERVIEW")
                    print("="*60)
                    overview = phase2.get("strategic_options_overview", "")
                    print(overview.replace("**", ""))
                    
                    # Ansoff Matrix Analysis
                    print("\n" + "="*60)
                    print("ANSOFF MATRIX - GROWTH STRATEGIES")
                    print("="*60)
                    ansoff = phase2.get("ansoff_matrix_analysis", {})
                    
                    for strategy in ["market_penetration", "market_development", "product_development", "diversification"]:
                        if strategy in ansoff:
                            strat_data = ansoff[strategy]
                            print(f"\n{strategy.replace('_', ' ').upper()}:")
                            print(f"  Feasibility: {strat_data.get('feasibility', 'Unknown')}")
                            print(f"  Expected Impact: {strat_data.get('expected_impact', 'Unknown')}")
                            print(f"  Timeline: {strat_data.get('timeline', 'Unknown')}")
                            print(f"  Investment: {strat_data.get('investment_required', 'Unknown')}")
                    
                    print(f"\nRecommended Strategy: {ansoff.get('recommended_strategy', 'Unknown')}")
                    
                    # Blue Ocean Strategy
                    print("\n" + "="*60)
                    print("BLUE OCEAN OPPORTUNITIES")
                    print("="*60)
                    blue_ocean = phase2.get("blue_ocean_strategy", {})
                    print(f"Value Innovation Potential: {blue_ocean.get('value_innovation_potential', 'Unknown')}")
                    
                    if "four_actions" in blue_ocean:
                        actions = blue_ocean["four_actions"]
                        print(f"\nEliminate: {', '.join(actions.get('eliminate', []))}")
                        print(f"Reduce: {', '.join(actions.get('reduce', []))}")
                        print(f"Raise: {', '.join(actions.get('raise', []))}")
                        print(f"Create: {', '.join(actions.get('create', []))}")
                    
                    # Growth Scenarios
                    print("\n" + "="*60)
                    print("GROWTH SCENARIOS")
                    print("="*60)
                    scenarios = phase2.get("growth_scenarios", [])
                    for i, scenario in enumerate(scenarios[:3], 1):
                        print(f"\n{i}. {scenario.get('name', 'Scenario')}")
                        print(f"   Revenue (Year 3): {scenario.get('expected_revenue_year3', 'Unknown')}")
                        print(f"   Investment Needed: {scenario.get('investment_required', 'Unknown')}")
                        print(f"   Success Probability: {scenario.get('success_probability', 'Unknown')}")
                    
                    # Recommended Direction
                    print("\n" + "="*60)
                    print("RECOMMENDED STRATEGIC DIRECTION")
                    print("="*60)
                    direction = phase2.get("recommended_direction", "")
                    print(direction.replace("**", ""))
                    
                    # Save results
                    with open("flash_phase2_analysis.json", "w") as f:
                        json.dump(result, f, indent=2)
                    print(f"\n\nFull Phase 2 analysis saved to: flash_phase2_analysis.json")
                    
                else:
                    error_text = await response.text()
                    print(f"\n✗ Error {response.status}: {error_text}")
                    
        except Exception as e:
            print(f"\n✗ Exception: {e}")

if __name__ == "__main__":
    print("\nContinuing FLASH strategic analysis with Phase 2...")
    print("This will identify growth strategies and opportunities.\n")
    asyncio.run(analyze_flash_phase2())