#!/usr/bin/env python3
"""
Test script for the enhanced analysis endpoint
"""

import requests
import json
from datetime import datetime

# Test startup data - a typical Series A SaaS company
test_startup = {
    "startup_name": "TechCo Analytics",
    "funding_stage": "Series A",
    "sector": "SaaS",
    
    # Capital metrics
    "total_capital_raised_usd": 15000000,
    "cash_on_hand_usd": 8000000,
    "monthly_burn_usd": 400000,
    "annual_revenue_run_rate": 3600000,
    "revenue_growth_rate_percent": 180,
    "gross_margin_percent": 72,
    "ltv_cac_ratio": 3.5,
    "investor_tier_primary": "Tier 1",
    "has_debt": False,
    
    # Advantage metrics  
    "patent_count": 2,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4,
    "switching_cost_score": 3,
    "brand_strength_score": 3,
    "scalability_score": 4,
    "product_stage": "GA",
    "product_retention_30d": 0.85,
    "product_retention_90d": 0.72,
    
    # Market metrics
    "tam_size_usd": 5000000000,
    "sam_size_usd": 500000000,
    "som_size_usd": 50000000,
    "market_growth_rate_percent": 35,
    "customer_count": 150,
    "customer_concentration_percent": 18,
    "user_growth_rate_percent": 120,
    "net_dollar_retention_percent": 115,
    "competition_intensity": 3,
    "competitors_named_count": 8,
    "dau_mau_ratio": 0.45,
    
    # People metrics
    "founders_count": 2,
    "team_size_full_time": 28,
    "years_experience_avg": 12,
    "domain_expertise_years_avg": 8,
    "prior_startup_experience_count": 3,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 4,
    "advisors_count": 4,
    "team_diversity_percent": 45,
    "key_person_dependency": False,
    
    # Calculated fields
    "runway_months": 20,
    "burn_multiple": 1.8
}

def test_analyze_endpoint():
    """Test the enhanced analysis endpoint"""
    url = "http://localhost:8001/analyze"
    
    headers = {
        "Content-Type": "application/json",
        # Add authentication header if needed
        # "Authorization": "Bearer YOUR_JWT_TOKEN"
    }
    
    print("Testing Enhanced Analysis Endpoint")
    print("=" * 50)
    print(f"Startup: {test_startup['startup_name']}")
    print(f"Stage: {test_startup['funding_stage']}")
    print(f"Sector: {test_startup['sector']}")
    print(f"Revenue: ${test_startup['annual_revenue_run_rate']:,.0f}")
    print(f"Growth: {test_startup['revenue_growth_rate_percent']}%")
    print("=" * 50)
    
    try:
        response = requests.post(url, json=test_startup, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['status'] == 'success':
                analysis = result['analysis']
                
                print("\n📊 PERCENTILE ANALYSIS")
                print("-" * 40)
                if 'percentiles' in analysis:
                    for metric, data in analysis['percentiles'].items():
                        if isinstance(data, dict) and 'percentile' in data:
                            print(f"{metric}: {data['percentile']}th percentile")
                            if 'value' in data and 'benchmark_median' in data:
                                print(f"  Your value: {data['value']:.1f}")
                                print(f"  Industry median: {data['benchmark_median']:.1f}")
                
                print("\n💡 TOP RECOMMENDATIONS")
                print("-" * 40)
                if 'recommendations' in analysis:
                    for i, rec in enumerate(analysis['recommendations'][:3], 1):
                        print(f"\n{i}. {rec['recommendation']} [{rec['priority']}]")
                        print(f"   {rec['specific_action']}")
                        print(f"   Impact: {rec['impact']}")
                
                print("\n🎯 STAGE-SPECIFIC INSIGHTS")
                print("-" * 40)
                if 'stage_insights' in analysis:
                    stage_info = analysis['stage_insights']
                    print(f"Current Stage: {stage_info['current_stage']}")
                    print("\nKey Success Factors:")
                    for factor in stage_info.get('success_factors', []):
                        print(f"  ✓ {factor}")
                    print("\nCommon Pitfalls:")
                    for pitfall in stage_info.get('common_pitfalls', []):
                        print(f"  ⚠️  {pitfall}")
                
                print("\n🏭 INDUSTRY COMPARISON")
                print("-" * 40)
                if 'industry_comparison' in analysis:
                    comp = analysis['industry_comparison']
                    print(f"Industry: {comp['industry']}")
                    if 'competitive_advantages' in comp:
                        print("\nCompetitive Advantages:")
                        for adv in comp['competitive_advantages']:
                            print(f"  ✓ {adv}")
                    if 'improvement_areas' in comp:
                        print("\nAreas for Improvement:")
                        for area in comp['improvement_areas']:
                            print(f"  • {area}")
                
                print("\n🔍 PATTERN INSIGHTS")
                print("-" * 40)
                if 'pattern_insights' in analysis:
                    patterns = analysis['pattern_insights']
                    if 'detected_patterns' in patterns:
                        print("Detected Patterns:")
                        for pattern in patterns['detected_patterns']:
                            print(f"  • {pattern['pattern']} (confidence: {pattern['confidence']:.0%})")
                
                print("\n📈 IMPROVEMENT OPPORTUNITIES")
                print("-" * 40)
                if 'improvement_opportunities' in analysis:
                    for opp in analysis['improvement_opportunities'][:3]:
                        print(f"\n{opp['metric']}:")
                        print(f"  Current: {opp['current_value']:.1f} ({opp['current_percentile']}th percentile)")
                        print(f"  Target: {opp['target_value']:.1f} (50th percentile)")
                        if 'estimated_success_lift' in opp:
                            print(f"  Success Impact: {opp['estimated_success_lift']}")
                
                print("\n✅ Analysis Complete!")
                
            else:
                print(f"Analysis failed: {result}")
                
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server")
        print("Make sure the server is running on port 8001")
    except Exception as e:
        print(f"Error: {e}")


def test_analyze_with_weak_startup():
    """Test with a startup that has weaknesses to see recommendations"""
    weak_startup = test_startup.copy()
    weak_startup.update({
        "startup_name": "StruggleTech",
        "funding_stage": "Seed",
        "revenue_growth_rate_percent": 50,  # Low growth
        "burn_multiple": 3.5,  # High burn
        "gross_margin_percent": 45,  # Low margin
        "ltv_cac_ratio": 1.5,  # Poor unit economics
        "customer_concentration_percent": 45,  # High concentration risk
        "runway_months": 8,  # Short runway
        "team_size_full_time": 5,  # Small team for stage
        "net_dollar_retention_percent": 85  # Poor retention
    })
    
    print("\n\n" + "=" * 70)
    print("TESTING WITH WEAK STARTUP METRICS")
    print("=" * 70)
    
    url = "http://localhost:8001/analyze"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=weak_startup, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                analysis = result['analysis']
                
                print("\n🚨 CRITICAL RECOMMENDATIONS FOR STRUGGLING STARTUP")
                print("-" * 50)
                if 'recommendations' in analysis:
                    for i, rec in enumerate(analysis['recommendations'], 1):
                        print(f"\n{i}. [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
                        print(f"   Action: {rec['specific_action']}")
                        print(f"   Impact: {rec['impact']}")
                        if 'benchmark' in rec:
                            print(f"   Benchmark: {rec['benchmark']}")
                
                print("\n📉 BELOW-MEDIAN METRICS")
                print("-" * 40)
                if 'percentiles' in analysis:
                    below_median = []
                    for metric, data in analysis['percentiles'].items():
                        if isinstance(data, dict) and 'percentile' in data:
                            if data['percentile'] < 50:
                                below_median.append((metric, data))
                    
                    for metric, data in sorted(below_median, key=lambda x: x[1]['percentile']):
                        print(f"{metric}: {data['percentile']}th percentile (value: {data['value']:.1f})")
                
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Test with a strong startup
    test_analyze_endpoint()
    
    # Test with a weak startup to see different recommendations
    test_analyze_with_weak_startup()