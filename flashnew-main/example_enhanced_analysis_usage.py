#!/usr/bin/env python3
"""
Example: Using the Enhanced Analysis API for Investment Decisions
"""

import requests
import json

# Example: Analyzing a Series A SaaS startup for investment decision
startup_profile = {
    "startup_name": "CloudSync Pro",
    "funding_stage": "Series A",
    "sector": "SaaS",
    
    # Strong metrics
    "revenue_growth_rate_percent": 220,
    "gross_margin_percent": 78,
    "net_dollar_retention_percent": 125,
    "product_retention_30d": 0.88,
    
    # Weak metrics  
    "burn_multiple": 2.8,  # High burn
    "runway_months": 14,   # Short runway
    "customer_concentration_percent": 35,  # High concentration
    
    # Other metrics
    "total_capital_raised_usd": 12000000,
    "cash_on_hand_usd": 5600000,
    "monthly_burn_usd": 400000,
    "annual_revenue_run_rate": 4800000,
    "ltv_cac_ratio": 3.2,
    "investor_tier_primary": "Tier 2",
    "has_debt": False,
    "patent_count": 3,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4,
    "switching_cost_score": 4,
    "brand_strength_score": 3,
    "scalability_score": 4,
    "product_stage": "GA",
    "product_retention_90d": 0.75,
    "tam_size_usd": 8000000000,
    "sam_size_usd": 800000000,
    "som_size_usd": 80000000,
    "market_growth_rate_percent": 45,
    "customer_count": 85,
    "user_growth_rate_percent": 180,
    "competition_intensity": 4,
    "competitors_named_count": 12,
    "dau_mau_ratio": 0.42,
    "founders_count": 2,
    "team_size_full_time": 32,
    "years_experience_avg": 14,
    "domain_expertise_years_avg": 10,
    "prior_startup_experience_count": 2,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 3,
    "advisors_count": 3,
    "team_diversity_percent": 38,
    "key_person_dependency": False
}


def analyze_for_investment(startup_data):
    """Analyze a startup and provide investment recommendation"""
    
    # First get prediction
    predict_response = requests.post(
        "http://localhost:8001/predict",
        json=startup_data,
        headers={"Content-Type": "application/json"}
    )
    
    if predict_response.status_code != 200:
        print(f"Prediction failed: {predict_response.text}")
        return
    
    prediction = predict_response.json()
    
    # Then get detailed analysis
    analyze_response = requests.post(
        "http://localhost:8001/analyze",
        json=startup_data,
        headers={"Content-Type": "application/json"}
    )
    
    if analyze_response.status_code != 200:
        print(f"Analysis failed: {analyze_response.text}")
        return
    
    analysis = analyze_response.json()["analysis"]
    
    # Generate investment memo
    print("=" * 70)
    print("INVESTMENT ANALYSIS MEMO")
    print("=" * 70)
    print(f"\nCompany: {startup_data['startup_name']}")
    print(f"Stage: {startup_data['funding_stage']}")
    print(f"Sector: {startup_data['sector']}")
    print(f"Revenue: ${startup_data['annual_revenue_run_rate']:,.0f} ARR")
    print(f"Growth Rate: {startup_data['revenue_growth_rate_percent']}%")
    
    print(f"\n📊 FLASH SCORE: {prediction['success_probability']:.1%}")
    print(f"Verdict: {prediction['verdict']}")
    print(f"Confidence: {prediction['confidence_interval']['lower']:.1%} - {prediction['confidence_interval']['upper']:.1%}")
    
    print("\n🎯 KEY STRENGTHS (Top Percentile Metrics)")
    print("-" * 50)
    strengths = []
    for metric, data in analysis['percentiles'].items():
        if isinstance(data, dict) and data.get('percentile', 0) > 75:
            strengths.append((metric, data))
    
    for metric, data in sorted(strengths, key=lambda x: x[1]['percentile'], reverse=True)[:5]:
        print(f"• {metric}: {data['percentile']:.0f}th percentile")
        print(f"  Value: {data['value']:.1f} (Industry median: {data.get('benchmark_median', 'N/A')})")
    
    print("\n⚠️  KEY RISKS (Bottom Percentile Metrics)")
    print("-" * 50)
    risks = []
    for metric, data in analysis['percentiles'].items():
        if isinstance(data, dict) and data.get('percentile', 100) < 40:
            risks.append((metric, data))
    
    for metric, data in sorted(risks, key=lambda x: x[1]['percentile'])[:5]:
        print(f"• {metric}: {data['percentile']:.0f}th percentile")
        print(f"  Value: {data['value']:.1f} (Industry median: {data.get('benchmark_median', 'N/A')})")
    
    print("\n💡 CRITICAL RECOMMENDATIONS")
    print("-" * 50)
    for i, rec in enumerate(analysis['recommendations'][:3], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['recommendation']}")
        print(f"   {rec['specific_action']}")
        print(f"   Expected Impact: {rec['impact']}")
    
    print("\n🔍 PATTERN ANALYSIS")
    print("-" * 50)
    if 'pattern_insights' in analysis and 'detected_patterns' in analysis['pattern_insights']:
        for pattern in analysis['pattern_insights']['detected_patterns']:
            print(f"• {pattern['pattern']} (confidence: {pattern['confidence']:.0%})")
            print(f"  Historical success rate: {pattern.get('success_rate', 0.35):.0%}")
    
    print("\n📈 GROWTH POTENTIAL")
    print("-" * 50)
    if 'improvement_opportunities' in analysis:
        total_lift = 0
        for opp in analysis['improvement_opportunities'][:3]:
            lift = float(opp.get('estimated_success_lift', '0%').strip('+%'))
            total_lift += lift
            print(f"• Improving {opp['metric']} to median: {opp['estimated_success_lift']} success lift")
        print(f"\nTotal potential success probability improvement: +{total_lift:.1f}%")
        print(f"Post-improvement success probability: {prediction['success_probability'] + total_lift/100:.1%}")
    
    print("\n🏁 INVESTMENT RECOMMENDATION")
    print("-" * 50)
    
    # Decision logic
    success_prob = prediction['success_probability']
    high_priority_risks = len([r for r in analysis['recommendations'] if r['priority'] == 'HIGH'])
    growth_rate = startup_data['revenue_growth_rate_percent']
    burn_multiple = startup_data['burn_multiple']
    
    if success_prob > 0.70 and high_priority_risks <= 1:
        recommendation = "STRONG BUY"
        rationale = "High success probability with manageable risks"
    elif success_prob > 0.60 and growth_rate > 150 and burn_multiple < 2.5:
        recommendation = "BUY"
        rationale = "Good fundamentals with strong growth and reasonable burn"
    elif success_prob > 0.50 and high_priority_risks <= 2:
        recommendation = "CONDITIONAL BUY"
        rationale = "Moderate success probability, contingent on addressing key risks"
    elif success_prob > 0.40 and growth_rate > 200:
        recommendation = "WATCH"
        rationale = "High growth but significant risks need addressing"
    else:
        recommendation = "PASS"
        rationale = "Risk-reward profile not favorable at current valuation"
    
    print(f"Recommendation: {recommendation}")
    print(f"Rationale: {rationale}")
    
    # Investment terms suggestion
    if recommendation in ["STRONG BUY", "BUY", "CONDITIONAL BUY"]:
        print("\n💰 SUGGESTED INVESTMENT TERMS")
        print("-" * 50)
        
        # Valuation discount based on risks
        base_valuation_multiple = 10  # 10x ARR for SaaS
        risk_discount = high_priority_risks * 0.5  # 0.5x per high priority risk
        growth_premium = (growth_rate - 100) / 100 * 2 if growth_rate > 100 else 0
        
        adjusted_multiple = base_valuation_multiple - risk_discount + growth_premium
        suggested_valuation = startup_data['annual_revenue_run_rate'] * adjusted_multiple
        
        print(f"Suggested pre-money valuation: ${suggested_valuation:,.0f}")
        print(f"Revenue multiple: {adjusted_multiple:.1f}x")
        
        if recommendation == "CONDITIONAL BUY":
            print("\nMilestone-based investment:")
            for i, rec in enumerate(analysis['recommendations'][:2], 1):
                print(f"{i}. {rec['recommendation']} - Release {25}% of funds")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("Running Enhanced Analysis for Investment Decision...")
    print("\nMake sure the API server is running on port 8001")
    print("Start it with: python api_server_unified.py\n")
    
    try:
        analyze_for_investment(startup_profile)
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server on port 8001")
        print("Please start the server first: python api_server_unified.py")
    except Exception as e:
        print(f"Error: {e}")