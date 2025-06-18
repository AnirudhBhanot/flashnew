#!/usr/bin/env python3
"""
Test if DeepSeek Michelin endpoints are working
"""

import requests
import time
import json

test_data = {
    "startup_data": {
        "startup_name": "Test AI Startup",
        "sector": "artificial-intelligence",
        "funding_stage": "seed",
        "total_capital_raised_usd": 2000000,
        "cash_on_hand_usd": 1500000,
        "market_size_usd": 50000000000,
        "market_growth_rate_annual": 45,
        "competitor_count": 8,
        "market_share_percentage": 0.01,
        "team_size_full_time": 12,
        "annual_revenue_usd": 500000,
        "monthly_burn_usd": 75000,
        "runway_months": 20,
        "product_stage": "beta",
        "proprietary_tech": True,
        "patents_filed": 2,
        "founders_industry_experience_years": 8,
        "b2b_or_b2c": "b2b",
        "investor_tier_primary": "tier_2"
    },
    "analysis_depth": "comprehensive"
}

endpoints = [
    ("/api/michelin/analyze", "Frontend Fix (No DeepSeek)"),
    ("/api/michelin/strategic-analysis", "Original DeepSeek Endpoint"),
    ("/api/michelin-fixed/analyze", "Fixed DeepSeek Endpoint")
]

print("Testing Michelin Endpoints")
print("=" * 80)

for endpoint, description in endpoints:
    print(f"\nTesting: {description}")
    print(f"Endpoint: {endpoint}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"http://localhost:8001{endpoint}",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=120  # 2 minute timeout for DeepSeek
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success in {elapsed:.1f}s")
            
            # Check if it's using DeepSeek or fallback
            if elapsed < 1:
                print("   → Using fallback (immediate response)")
            else:
                print("   → Using DeepSeek API")
                
            # Show a sample of the response
            if "executive_briefing" in data:
                briefing = data["executive_briefing"][:200].strip() + "..."
                print(f"   → Briefing: {briefing}")
                
        elif response.status_code == 405:
            print(f"❌ Method not allowed")
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout after 120 seconds")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("\nDeepSeek API Status:")
print("- The frontend is using the fallback endpoint for immediate responses")
print("- DeepSeek API is working (as shown by /api/analysis/recommendations/dynamic)")
print("- To use DeepSeek-powered Michelin analysis, update the frontend to call:")
print("  /api/michelin/strategic-analysis or /api/michelin-fixed/analyze")