#!/usr/bin/env python3
"""Test script to verify Michelin API fixes"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_michelin_api():
    """Test the Michelin API with a sample request"""
    
    # Test data
    test_data = {
        "startup_data": {
            "startup_name": "TestCo AI",
            "sector": "artificial_intelligence",
            "funding_stage": "series_a",
            "total_capital_raised_usd": 15000000,
            "cash_on_hand_usd": 12000000,
            "monthly_burn_usd": 400000,
            "runway_months": 30,
            "team_size_full_time": 25,
            "market_size_usd": 50000000000,
            "market_growth_rate_annual": 35.5,
            "competitor_count": 150,
            "market_share_percentage": 0.5,
            "customer_acquisition_cost_usd": 5000,
            "lifetime_value_usd": 50000,
            "monthly_active_users": 5000,
            "product_stage": "growth",
            "proprietary_tech": True,
            "patents_filed": 3,
            "founders_industry_experience_years": 10,
            "b2b_or_b2c": "b2b",
            "burn_rate_usd": 400000,
            "investor_tier_primary": "tier_1",
            "geographical_focus": "global",
            "revenue_growth_rate": 150,
            "gross_margin": 75,
            "annual_revenue_usd": 2000000
        },
        "include_financial_projections": True,
        "analysis_depth": "comprehensive"
    }
    
    url = "http://localhost:8000/api/michelin/analyze"
    
    async with aiohttp.ClientSession() as session:
        try:
            print(f"Testing Michelin API at {url}")
            print(f"Request data: {json.dumps(test_data, indent=2)}")
            
            async with session.post(url, json=test_data) as response:
                print(f"\nResponse status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("\n✅ SUCCESS! API returned valid response")
                    print(f"\nAnalysis for: {result['startup_name']}")
                    print(f"Date: {result['analysis_date']}")
                    print(f"\nExecutive Briefing Preview:")
                    print(result['executive_briefing'][:500] + "...")
                    
                    # Check if all required fields are present
                    required_fields = ['phase1', 'phase2', 'phase3', 'key_recommendations']
                    missing_fields = [f for f in required_fields if f not in result]
                    
                    if missing_fields:
                        print(f"\n⚠️  Warning: Missing fields: {missing_fields}")
                    else:
                        print("\n✅ All required fields present")
                        
                    # Save full response for inspection
                    with open('michelin_test_response.json', 'w') as f:
                        json.dump(result, f, indent=2)
                    print("\nFull response saved to michelin_test_response.json")
                    
                else:
                    error_text = await response.text()
                    print(f"\n❌ ERROR: {error_text}")
                    
        except aiohttp.ClientConnectorError:
            print("\n❌ ERROR: Could not connect to API. Make sure the server is running on port 8000")
        except Exception as e:
            print(f"\n❌ ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("Michelin API Fix Test")
    print("=" * 50)
    asyncio.run(test_michelin_api())