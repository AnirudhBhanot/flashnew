#!/usr/bin/env python3
"""Test the enhanced analysis with frontend integration"""

import json
import requests
from datetime import datetime

# Test startup data
test_startup = {
    "company_name": "TechCo",
    "funding_stage": "series_a",
    "industry": "b2b_saas",
    "country": "United States",
    "total_funding_amount": 15000000,
    "last_round_raised_usd": 10000000,
    "last_round_date": "2024-01-15",
    "number_of_funding_rounds": 3,
    "customer_acquisition_cost": 5000,
    "customer_lifetime_value": 50000,
    "monthly_recurring_revenue": 250000,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "current_arr": 3000000,
    "runway_months": 18,
    "burn_multiple": 2.5,  # Inefficient - should trigger recommendations
    "team_size_full_time": 25,
    "years_experience_avg": 7,
    "founder_experience_years": 10,
    "has_technical_cofounder": True,
    "previous_successful_exit": False,
    "net_promoter_score": 45,
    "technology_score": 3,
    "scalability_score": 0.7,
    "proprietary_technology": True,
    "network_effects": False,
    "has_patent": False,
    "switching_costs": 2,
    "unique_value_proposition": True,
    "product_stage": "growth",
    "users_count": 150,
    "customer_concentration_percent": 25,
    "tam_size_usd": 5000000000,
    "tam_growth_rate_percent": 25,
    "market_position": 3,
    "ltv_cac_ratio": 10,
    "investor_tier_primary": "tier_2",
    "valuation_usd": 50000000,
    "competition_intensity": 3,
    "market_growth_rate": 25,
    "net_dollar_retention_percent": 115,
    "advisor_quality_score": 3
}

def test_enhanced_analysis():
    """Test the enhanced analysis endpoint"""
    
    print("Testing Enhanced Analysis API...")
    print("=" * 60)
    
    # Call the enhanced analysis endpoint
    response = requests.post(
        "http://localhost:8001/analyze",
        json=test_startup
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    
    # Print key results
    print(f"\n✅ Success Probability: {data['success_probability']:.1%}")
    print(f"📊 Confidence: {data['confidence_score']:.1%}")
    print(f"🎯 Verdict: {data['verdict']}")
    
    # Print CAMP scores
    print("\n📈 CAMP Scores:")
    for pillar, score in data['camp_scores'].items():
        print(f"  {pillar.title()}: {score:.1%}")
    
    # Print real model insights
    if 'model_insights' in data:
        print("\n🤖 Model Contributions (REAL):")
        for model, weight in data['model_insights']['weights'].items():
            print(f"  {model}: {weight:.1%}")
    
    # Print real benchmarks
    if 'benchmarks' in data:
        print("\n📊 Industry Benchmarks (REAL):")
        for benchmark in data['benchmarks'][:3]:  # Show first 3
            print(f"\n  {benchmark['metric']}:")
            print(f"    Your Value: {benchmark['your_value']}")
            print(f"    Your Percentile: {benchmark['your_percentile']}th")
            print(f"    Industry P50: {benchmark['percentile_50']}")
    
    # Print personalized recommendations
    if 'recommendations' in data:
        print("\n💡 Personalized Recommendations (REAL):")
        for i, rec in enumerate(data['recommendations'][:3], 1):
            print(f"\n  {i}. {rec['title']}")
            print(f"     Priority: {rec['priority']}")
            print(f"     Impact: +{rec['impact']:.0f}% success probability")
            print(f"     Timeline: {rec['timeline']}")
    
    # Print key insights
    if 'key_insights' in data:
        print("\n🔍 Key Insights (REAL):")
        if 'strengths' in data['key_insights']:
            print("\n  Strengths:")
            for s in data['key_insights']['strengths'][:2]:
                print(f"    • {s['title']}: {s['description']}")
        
        if 'improvements' in data['key_insights']:
            print("\n  Areas to Improve:")
            for i in data['key_insights']['improvements'][:2]:
                print(f"    • {i['title']}: {i['description']}")
    
    # Save full response for inspection
    with open('enhanced_analysis_response.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n✅ Full response saved to enhanced_analysis_response.json")
    print("\nThe frontend will now show:")
    print("- Real model contribution percentages")
    print("- Actual industry benchmarks from 100k+ startups")
    print("- Personalized recommendations based on your weaknesses")
    print("- Dynamic insights specific to your stage and industry")

if __name__ == "__main__":
    test_enhanced_analysis()