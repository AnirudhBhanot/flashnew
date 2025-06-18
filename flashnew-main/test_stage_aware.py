#!/usr/bin/env python3
"""
Test script for stage-aware financial modeling
Demonstrates how the system handles different funding stages and revenue scenarios
"""

import requests
import json
from typing import Dict, Any

# API endpoint
API_URL = "http://localhost:8001/api/frameworks/deep-analysis"

def test_stage_aware_analysis(stage: str, revenue: int, description: str) -> Dict[str, Any]:
    """Test the stage-aware analysis with different scenarios"""
    
    # Base startup data
    startup_data = {
        "annual_revenue_run_rate": revenue,
        "monthly_burn_usd": 50000 if stage in ['pre_seed', 'seed'] else 200000,
        "runway_months": 12,
        "customer_count": 0 if revenue == 0 else max(10, revenue // 10000),
        "team_size_full_time": 3 if stage == 'pre_seed' else (10 if stage == 'seed' else 25),
        "funding_stage": stage,
        "sector": "ai-ml",
        "tam_size_usd": 50000000000,  # $50B
        "sam_size_usd": 5000000000,   # $5B
        "som_size_usd": 50000000,     # $50M
        "market_growth_rate_percent": 30,
        "competition_intensity": 3,
        "patent_count": 1 if stage == 'pre_seed' else 3,
        "prior_exits": 0 if stage in ['pre_seed', 'seed'] else 1,
        "domain_expertise_years": 5,
        "total_capital_raised_usd": 100000 if stage == 'pre_seed' else (2000000 if stage == 'seed' else 10000000),
        "cash_on_hand_usd": 600000 if stage == 'pre_seed' else (1800000 if stage == 'seed' else 8000000),
        "gross_margin_percent": 70,
        "ltv_cac_ratio": 0 if revenue == 0 else 2.5,
        "monthly_churn_rate": 0.05,
        "user_growth_rate_percent": 0 if revenue == 0 else 20,
        "switching_cost_score": 3,
        "customer_concentration_percent": 0 if revenue == 0 else 20,
        "competitors_named_count": 10
    }
    
    # Make API request
    response = requests.post(API_URL, json={
        "startup_data": startup_data,
        "analysis_depth": "comprehensive"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n{'='*80}")
        print(f"Test Case: {description}")
        print(f"Stage: {stage}, Revenue: ${revenue:,}")
        print(f"{'='*80}")
        
        # Extract key information
        exec_summary = result['executive_summary']
        print(f"\nSituation: {exec_summary['situation']}")
        print(f"\nKey Insights:")
        for insight in exec_summary['key_insights']:
            print(f"  • {insight}")
        
        print(f"\nRecommendation: {exec_summary['recommendation']}")
        print(f"Value at Stake: ${exec_summary['value_at_stake']:,.0f}")
        print(f"Confidence Level: {exec_summary['confidence_level']}%")
        
        # Show strategic options
        print(f"\nStrategic Options:")
        for option in result['strategic_options'][:3]:
            print(f"  • {option['title']}: NPV ${option['npv']:,.0f}, IRR {option['irr']}%")
        
        # Show financial projections
        print(f"\nFinancial Projections (Base Case):")
        for year_data in result['financial_projections']['base_case']:
            print(f"  Year {year_data['year']}: Revenue ${year_data['revenue']:,.0f}, EBITDA ${year_data['ebitda']:,.0f}")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return {}

def main():
    """Run test cases for different stages and revenue scenarios"""
    
    print("Testing Stage-Aware Financial Modeling")
    print("=====================================")
    
    # Test Case 1: Pre-seed with zero revenue (most common)
    test_stage_aware_analysis(
        stage="pre_seed",
        revenue=0,
        description="Pre-seed startup with zero revenue (typical scenario)"
    )
    
    # Test Case 2: Seed with zero revenue
    test_stage_aware_analysis(
        stage="seed",
        revenue=0,
        description="Seed startup with zero revenue (still building)"
    )
    
    # Test Case 3: Seed with some revenue
    test_stage_aware_analysis(
        stage="seed",
        revenue=120000,  # $120K ARR
        description="Seed startup with early revenue"
    )
    
    # Test Case 4: Series A (should have revenue)
    test_stage_aware_analysis(
        stage="series_a",
        revenue=1200000,  # $1.2M ARR
        description="Series A startup with solid revenue"
    )
    
    # Test Case 5: Edge case - Series A with zero revenue
    test_stage_aware_analysis(
        stage="series_a",
        revenue=0,
        description="Series A with zero revenue (unusual, e.g., pivoted)"
    )

if __name__ == "__main__":
    main()