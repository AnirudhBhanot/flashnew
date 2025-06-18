#!/usr/bin/env python3
"""
Demo of the decomposed Michelin analysis approach
Shows how it provides reliable, high-quality strategic analysis
"""

import requests
import json
import time
from datetime import datetime

# Realistic startup data
startup_data = {
    "startup_name": "QuantumHealth",
    "sector": "healthcare",
    "funding_stage": "seed",
    "total_capital_raised_usd": 2000000,
    "cash_on_hand_usd": 1500000,
    "monthly_burn_usd": 100000,
    "runway_months": 15,
    "team_size_full_time": 8,
    "market_size_usd": 15000000000,  # $15B
    "market_growth_rate_annual": 28,
    "competitor_count": 120,
    "market_share_percentage": 0.05,
    "customer_acquisition_cost_usd": 1500,
    "lifetime_value_usd": 12000,
    "monthly_active_users": 25000,
    "product_stage": "beta",
    "proprietary_tech": True,
    "patents_filed": 2,
    "founders_industry_experience_years": 12,
    "b2b_or_b2c": "b2b",
    "burn_rate_usd": 100000,
    "investor_tier_primary": "tier_2",
    "customer_count": 30,
    "geographical_focus": "domestic",
    "revenue_growth_rate": 200,
    "gross_margin": 75,
    "net_promoter_score": 65,
    "technology_readiness_level": 7,
    "has_strategic_partnerships": False,
    "customer_concentration": 20,
    "annual_revenue_usd": 300000
}

def main():
    print("\n🚀 DECOMPOSED MICHELIN ANALYSIS DEMO")
    print("="*60)
    print(f"\nCompany: {startup_data['startup_name']}")
    print(f"Sector: {startup_data['sector'].title()}")
    print(f"Stage: {startup_data['funding_stage'].title()}")
    print(f"Market: ${startup_data['market_size_usd']/1e9:.0f}B @ {startup_data['market_growth_rate_annual']}% growth")
    print(f"LTV/CAC: {startup_data['lifetime_value_usd']/startup_data['customer_acquisition_cost_usd']:.1f}x")
    print(f"Runway: {startup_data['runway_months']} months")
    
    request_data = {
        "startup_data": startup_data,
        "include_financial_projections": True,
        "analysis_depth": "comprehensive"
    }
    
    print("\n" + "-"*60)
    
    # Phase 1
    print("\n📊 PHASE 1: Where Are We Now?")
    print("-"*30)
    
    url = "http://localhost:8001/api/michelin/decomposed/analyze/phase1"
    start = time.time()
    response = requests.post(url, json=request_data)
    elapsed = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        phase1 = data['phase1']
        
        print(f"✅ Analysis completed in {elapsed:.1f} seconds\n")
        
        print("Executive Summary:")
        print(f"{phase1['executive_summary']}\n")
        
        print(f"BCG Position: {phase1['bcg_matrix_analysis']['position']}")
        print(f"Strategic Implications: {phase1['bcg_matrix_analysis']['strategic_implications']}\n")
        
        print("Key Strengths:")
        for s in phase1['swot_analysis']['strengths'][:2]:
            print(f"• {s['point']}: {s['evidence']}")
        
        print("\nCritical Weaknesses:")
        for w in phase1['swot_analysis']['weaknesses'][:2]:
            print(f"• {w['point']}: {w['evidence']}")
        
        print("\nCompetitive Forces:")
        for force, details in phase1['porters_five_forces'].items():
            if isinstance(details, dict) and 'level' in details:
                print(f"• {force.replace('_', ' ').title()}: {details['level']}")
        
        # Phase 2
        print("\n" + "-"*60)
        print("\n📈 PHASE 2: Where Should We Go?")
        print("-"*30)
        
        phase2_request = {
            "startup_data": startup_data,
            "phase1_results": phase1
        }
        
        url = "http://localhost:8001/api/michelin/decomposed/analyze/phase2"
        start = time.time()
        response = requests.post(url, json=phase2_request)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            phase2 = data['phase2']
            
            print(f"✅ Analysis completed in {elapsed:.1f} seconds\n")
            
            print(f"Strategic Overview: {phase2['strategic_options_overview']}\n")
            
            print(f"Recommended Growth Strategy: {phase2['ansoff_matrix_analysis']['recommended_strategy']}")
            print(f"Rationale: {phase2['ansoff_matrix_analysis']['rationale']}\n")
            
            print("Blue Ocean Opportunities:")
            for opp in phase2['blue_ocean_strategy']['opportunities']:
                print(f"• {opp['opportunity']}: {opp['approach']}")
            
            print("\nGrowth Scenarios:")
            for scenario in phase2['growth_scenarios']:
                print(f"• {scenario['scenario_name']}: ${scenario['12_month_revenue_projection']:,} revenue")
            
            # Phase 3
            print("\n" + "-"*60)
            print("\n🎯 PHASE 3: How to Get There?")
            print("-"*30)
            
            phase3_request = {
                "startup_data": startup_data,
                "phase1_results": phase1,
                "phase2_results": phase2
            }
            
            url = "http://localhost:8001/api/michelin/decomposed/analyze/phase3"
            start = time.time()
            response = requests.post(url, json=phase3_request)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Analysis completed in {elapsed:.1f} seconds\n")
                
                print("EXECUTIVE BRIEFING:")
                print("-"*20)
                print(data['executive_briefing'])
                
                print("\nKEY RECOMMENDATIONS:")
                for i, rec in enumerate(data['key_recommendations'], 1):
                    print(f"{i}. {rec}")
                
                print("\nCRITICAL SUCCESS FACTORS:")
                for i, factor in enumerate(data['critical_success_factors'], 1):
                    print(f"{i}. {factor}")
                
                print("\nIMMEDIATE NEXT STEPS:")
                for step in data['next_steps']:
                    print(f"• {step['action']}")
                    print(f"  Timeline: {step['timeline']} | Owner: {step['owner']}")
                
                print("\n" + "="*60)
                print("✨ ANALYSIS COMPLETE - Ready for strategic decision making")
                print("="*60)

if __name__ == "__main__":
    main()