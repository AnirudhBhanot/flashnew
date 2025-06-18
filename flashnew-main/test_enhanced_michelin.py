#!/usr/bin/env python3
"""
Test script for Enhanced Michelin Analysis
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Test data for a B2B SaaS startup
test_data = {
    "startup_name": "DataSync AI",
    "sector": "saas_b2b",
    "funding_stage": "seed",
    "total_capital_raised_usd": 1500000,
    "cash_on_hand_usd": 1200000,
    "monthly_burn_usd": 150000,
    "runway_months": 8,
    "team_size_full_time": 12,
    "market_size_usd": 5000000000,
    "market_growth_rate_annual": 25,
    "competitor_count": 8,
    "market_share_percentage": 0.1,
    "customer_acquisition_cost_usd": 5000,
    "lifetime_value_usd": 12500,
    "monthly_active_users": 250,
    "product_stage": "live",
    "proprietary_tech": True,
    "patents_filed": 2,
    "founders_industry_experience_years": 15,
    "b2b_or_b2c": "b2b",
    "burn_rate_usd": 150000,
    "investor_tier_primary": "tier_2",
    # Optional fields
    "revenue_growth_rate": 15,
    "gross_margin": 75,
    "customer_count": 25,
    "annual_revenue_usd": 600000
}

async def test_enhanced_phase1():
    """Test Phase 1 enhanced analysis"""
    async with aiohttp.ClientSession() as session:
        # Test enhanced approach
        url = "http://localhost:8001/api/michelin/enhanced/analyze/phase1"
        
        print("Testing Enhanced Michelin Phase 1 Analysis...")
        print(f"Company: {test_data['startup_name']}")
        print(f"Stage: {test_data['funding_stage']}")
        print(f"Sector: {test_data['sector']}")
        print("-" * 50)
        
        start_time = datetime.now()
        
        # Wrap in expected request format
        request_data = {
            "startup_data": test_data
        }
        
        try:
            async with session.post(url, json=request_data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                    print(f"✓ Success! Analysis completed in {elapsed_time:.1f} seconds")
                    print("\nPhase 1 Analysis Structure:")
                    
                    # Print top-level keys
                    for key in result.keys():
                        print(f"  - {key}")
                        
                    # Check for McKinsey-grade enhancements
                    if "bcg_matrix_analysis" in result:
                        bcg = result["bcg_matrix_analysis"]
                        print("\nBCG Matrix Analysis:")
                        print(f"  Position: {bcg.get('position', 'N/A')}")
                        if "customization" in bcg:
                            print(f"  Industry Customization: {bcg['customization']}")
                            
                    if "strategic_context" in result:
                        print("\nStrategic Context Found:")
                        context = result["strategic_context"]
                        print(f"  - Industry: {context.get('industry', 'N/A')}")
                        print(f"  - Current Inflection: {context.get('current_inflection', 'N/A')}")
                        
                    # Save to file for inspection
                    with open("enhanced_phase1_output.json", "w") as f:
                        json.dump(result, f, indent=2)
                    print("\nFull output saved to: enhanced_phase1_output.json")
                    
                else:
                    error_text = await response.text()
                    print(f"✗ Error {response.status}: {error_text}")
                    
        except Exception as e:
            print(f"✗ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_phase1())