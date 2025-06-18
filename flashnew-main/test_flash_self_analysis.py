#!/usr/bin/env python3
"""
Test Enhanced Michelin Analysis using FLASH itself as the subject
Meta-analysis: FLASH analyzing FLASH
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# FLASH platform data as a B2B SaaS startup
flash_data = {
    "startup_name": "FLASH Platform",
    "sector": "saas_b2b",  # B2B SaaS for startup evaluation
    "funding_stage": "seed",
    "total_capital_raised_usd": 2000000,  # Assumed seed funding
    "cash_on_hand_usd": 1500000,
    "monthly_burn_usd": 125000,  # Engineering team + infrastructure
    "runway_months": 12,
    "team_size_full_time": 8,  # Small engineering team
    "market_size_usd": 50000000000,  # VC/startup evaluation market
    "market_growth_rate_annual": 15,  # Growing with startup ecosystem
    "competitor_count": 12,  # SignalFire, NFX, other VC tools
    "market_share_percentage": 0.01,  # Early stage
    "customer_acquisition_cost_usd": 10000,  # Enterprise B2B sales
    "lifetime_value_usd": 50000,  # Annual contracts
    "monthly_active_users": 50,  # Early adopters (VCs, accelerators)
    "product_stage": "live",
    "proprietary_tech": True,  # ML models, strategic analysis
    "patents_filed": 0,  # Open source approach
    "founders_industry_experience_years": 20,  # Domain expertise
    "b2b_or_b2c": "b2b",
    "burn_rate_usd": 125000,
    "investor_tier_primary": "tier_2",
    
    # FLASH-specific metrics
    "revenue_growth_rate": 0,  # Pre-revenue
    "gross_margin": 85,  # SaaS margins
    "customer_count": 5,  # Early pilot customers
    "annual_revenue_usd": 0,  # Pre-revenue
    
    # Additional context
    "key_metrics": {
        "models_accuracy": 72.7,  # ML model AUC
        "analysis_endpoints": 20,  # Number of analysis types
        "framework_count": 500,  # Business frameworks
        "api_response_time": 250,  # milliseconds
        "deepseek_integration": 80  # % coverage
    }
}

async def analyze_flash_phase1():
    """Run Phase 1 analysis on FLASH platform"""
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8001/api/michelin/enhanced/analyze/phase1"
        
        print("=" * 60)
        print("FLASH PLATFORM SELF-ANALYSIS")
        print("Meta-Analysis: Using FLASH to analyze FLASH")
        print("=" * 60)
        print(f"\nCompany: {flash_data['startup_name']}")
        print(f"Description: AI-powered startup evaluation platform")
        print(f"Stage: {flash_data['funding_stage']}")
        print(f"Market: VC/Startup evaluation tools")
        print(f"Unique Value: McKinsey-grade analysis + ML predictions")
        print("-" * 60)
        
        # Wrap in expected request format
        request_data = {
            "startup_data": flash_data
        }
        
        start_time = datetime.now()
        
        try:
            async with session.post(url, json=request_data, timeout=120) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                    print(f"\n✓ Analysis completed in {elapsed_time:.1f} seconds")
                    
                    # Extract key insights
                    phase1 = result.get("phase1", {})
                    
                    print("\n" + "="*60)
                    print("EXECUTIVE SUMMARY")
                    print("="*60)
                    exec_summary = phase1.get("executive_summary", "Not available")
                    # Clean up the summary for display
                    exec_summary = exec_summary.replace("**", "").replace("\\n", "\n")
                    print(exec_summary)
                    
                    print("\n" + "="*60)
                    print("BCG MATRIX POSITION")
                    print("="*60)
                    bcg = phase1.get("bcg_matrix_analysis", {})
                    print(f"Position: {bcg.get('position', 'Unknown')}")
                    print(f"Market Growth: {bcg.get('market_growth_rate', 'Unknown')}")
                    print(f"Market Share: {bcg.get('relative_market_share', 'Unknown')}")
                    
                    print("\n" + "="*60)
                    print("COMPETITIVE LANDSCAPE (Porter's Five Forces)")
                    print("="*60)
                    porters = phase1.get("porters_five_forces", {})
                    for force, data in porters.items():
                        if isinstance(data, dict) and "level" in data:
                            print(f"- {force.replace('_', ' ').title()}: {data['level']}")
                    
                    print("\n" + "="*60)
                    print("SWOT ANALYSIS HIGHLIGHTS")
                    print("="*60)
                    swot = phase1.get("swot_analysis", {})
                    
                    print("\nStrengths:")
                    for s in swot.get("strengths", [])[:3]:
                        if isinstance(s, dict):
                            print(f"  • {s.get('point', 'N/A')}")
                    
                    print("\nWeaknesses:")
                    for w in swot.get("weaknesses", [])[:3]:
                        if isinstance(w, dict):
                            print(f"  • {w.get('point', 'N/A')}")
                    
                    print("\nStrategic Priorities:")
                    for p in swot.get("strategic_priorities", [])[:3]:
                        print(f"  • {p}")
                    
                    # Save full output
                    with open("flash_self_analysis.json", "w") as f:
                        json.dump(result, f, indent=2)
                    print(f"\n\nFull analysis saved to: flash_self_analysis.json")
                    
                else:
                    error_text = await response.text()
                    print(f"\n✗ Error {response.status}: {error_text}")
                    
        except asyncio.TimeoutError:
            print(f"\n✗ Analysis timed out after 120 seconds")
        except Exception as e:
            print(f"\n✗ Exception: {e}")

async def main():
    """Run the self-analysis"""
    print("\nStarting FLASH self-analysis...")
    print("This meta-analysis will reveal FLASH's strategic position")
    print("in the startup evaluation tools market.\n")
    
    await analyze_flash_phase1()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nKey Takeaways:")
    print("- FLASH is analyzing itself using its own enhanced Michelin framework")
    print("- The analysis provides McKinsey-grade strategic insights")
    print("- This demonstrates the platform's capability for deep strategic analysis")
    print("- The same analysis is available for any startup through the API")

if __name__ == "__main__":
    asyncio.run(main())