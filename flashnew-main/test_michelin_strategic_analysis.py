#!/usr/bin/env python3
"""
Test script for Michelin Strategic Analysis API
"""

import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8001/api/michelin/analyze"

# Test startup data
test_startup_data = {
    "startup_name": "TechVenture AI",
    "sector": "artificial-intelligence",
    "funding_stage": "seed",
    "total_capital_raised_usd": 2000000,
    "cash_on_hand_usd": 1500000,
    "market_size_usd": 50000000000,
    "market_growth_rate_annual": 45,
    "competitor_count": 8,
    "market_share_percentage": 0.01,
    "team_size_full_time": 12,
    "customer_count": 25,
    "customer_acquisition_cost_usd": 1000,
    "lifetime_value_usd": 10000,
    "monthly_active_users": 5000,
    "proprietary_tech": True,
    "patents_filed": 2,
    "founders_industry_experience_years": 8,
    "b2b_or_b2c": "b2b",
    "burn_rate_usd": 75000,
    "monthly_burn_usd": 75000,
    "runway_months": 20,
    "product_stage": "beta",
    "investor_tier_primary": "tier_2",
    # Optional fields
    "revenue_growth_rate": 150,
    "gross_margin": 70,
    "technology_readiness_level": 7,
    "has_strategic_partnerships": True,
    "customer_concentration": 20,
    "annual_revenue_usd": 500000
}

def test_michelin_analysis():
    """Test the Michelin Strategic Analysis endpoint"""
    
    print("=" * 80)
    print("Testing Michelin Strategic Analysis API")
    print("=" * 80)
    
    # First check if API is running
    try:
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ API server is not running. Please start it with: python api_server_unified.py")
            return
        print("✅ API server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Please start it with: python api_server_unified.py")
        return
    
    # Check Michelin endpoint status
    try:
        status_response = requests.get("http://localhost:8001/api/michelin/status", timeout=5)
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ Michelin Analysis Service Status: {status_data.get('status', 'unknown')}")
            print(f"   - Framework Analysis Available: {status_data.get('framework_analysis_available', False)}")
            print(f"   - DeepSeek Configured: {status_data.get('deepseek_configured', False)}")
            print(f"   - Version: {status_data.get('version', 'unknown')}")
        else:
            print("⚠️  Michelin service endpoint not responding properly")
    except Exception as e:
        print(f"⚠️  Could not check Michelin service status: {e}")
    
    print("\n" + "-" * 80)
    print("Sending analysis request...")
    print("-" * 80)
    
    # Prepare request
    request_data = {
        "startup_data": test_startup_data,
        "analysis_depth": "comprehensive"
    }
    
    # Send request
    try:
        start_time = datetime.now()
        response = requests.post(
            API_URL,
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # 60 second timeout for comprehensive analysis
        )
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"Response Status: {response.status_code}")
        print(f"Processing Time: {processing_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            
            # Display results
            print("\n" + "=" * 80)
            print("MICHELIN STRATEGIC ANALYSIS RESULTS")
            print("=" * 80)
            
            print(f"\nCompany: {data.get('startup_name', 'Unknown')}")
            print(f"Analysis Date: {data.get('analysis_date', 'Unknown')}")
            
            print("\n" + "-" * 80)
            print("EXECUTIVE BRIEFING")
            print("-" * 80)
            print(data.get('executive_briefing', 'No briefing available'))
            
            # Phase 1 Summary
            if 'phase1' in data:
                phase1 = data['phase1']
                print("\n" + "-" * 80)
                print("PHASE 1: WHERE ARE WE NOW?")
                print("-" * 80)
                
                if 'bcg_matrix' in phase1:
                    bcg = phase1['bcg_matrix']
                    print(f"\nBCG Matrix Position: {bcg.get('position', 'Unknown')}")
                    print(f"Market Growth: {bcg.get('market_growth', 0):.1f}%")
                    print(f"Relative Market Share: {bcg.get('relative_market_share', 0):.2f}%")
                
                if 'porters_five_forces' in phase1:
                    print(f"\nIndustry Attractiveness: {phase1['porters_five_forces'].get('overall_industry_attractiveness', 'Unknown')}")
                
                if 'swot_analysis' in phase1:
                    swot = phase1['swot_analysis']
                    print(f"\nStrategic Priorities:")
                    for priority in swot.get('strategic_priorities', [])[:3]:
                        print(f"  • {priority}")
            
            # Phase 2 Summary
            if 'phase2' in data:
                phase2 = data['phase2']
                print("\n" + "-" * 80)
                print("PHASE 2: WHERE SHOULD WE GO?")
                print("-" * 80)
                
                if 'ansoff_matrix' in phase2:
                    print(f"\nRecommended Strategy: {phase2['ansoff_matrix'].get('recommended_strategy', 'Unknown')}")
                
                print(f"\nRecommended Direction: {phase2.get('recommended_direction', 'No recommendation')}")
            
            # Phase 3 Summary
            if 'phase3' in data:
                phase3 = data['phase3']
                print("\n" + "-" * 80)
                print("PHASE 3: HOW TO GET THERE?")
                print("-" * 80)
                
                if 'resource_requirements' in phase3:
                    resources = phase3['resource_requirements']
                    if 'financial_resources' in resources:
                        financial = resources['financial_resources']
                        capital_needed = financial.get('total_capital_needed', 0)
                        print(f"\nTotal Capital Required: ${capital_needed:,.0f}")
                
                if 'okr_framework' in phase3 and len(phase3['okr_framework']) > 0:
                    print(f"\nFirst Quarter Objective: {phase3['okr_framework'][0]['objectives'][0]['objective']}")
            
            # Key Recommendations
            print("\n" + "-" * 80)
            print("KEY RECOMMENDATIONS")
            print("-" * 80)
            for i, rec in enumerate(data.get('key_recommendations', []), 1):
                print(f"{i}. {rec}")
            
            # Critical Success Factors
            print("\n" + "-" * 80)
            print("CRITICAL SUCCESS FACTORS")
            print("-" * 80)
            for factor in data.get('critical_success_factors', []):
                print(f"• {factor}")
            
            # Next Steps
            print("\n" + "-" * 80)
            print("IMMEDIATE NEXT STEPS")
            print("-" * 80)
            if 'next_steps' in data and len(data['next_steps']) > 0:
                for step in data['next_steps']:
                    print(f"\n{step.get('timeline', 'Unknown timeline')}:")
                    for action in step.get('actions', []):
                        print(f"  • {action}")
            
            # Save full response
            output_file = f"michelin_analysis_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n✅ Full analysis saved to: {output_file}")
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n❌ Request timed out. The analysis may take longer than expected.")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API server")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_michelin_analysis()