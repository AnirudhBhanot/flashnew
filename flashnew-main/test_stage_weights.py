#!/usr/bin/env python3
"""
Test that stage-specific weights are displayed correctly
"""

import requests
import json

# Test different funding stages
stages = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']

# Expected weights for each stage (from CAMP framework)
expected_weights = {
    'pre_seed': {'people': 0.40, 'advantage': 0.30, 'market': 0.20, 'capital': 0.10},
    'seed': {'people': 0.30, 'advantage': 0.30, 'market': 0.25, 'capital': 0.15},
    'series_a': {'market': 0.30, 'people': 0.25, 'advantage': 0.25, 'capital': 0.20},
    'series_b': {'market': 0.35, 'capital': 0.25, 'advantage': 0.20, 'people': 0.20},
    'series_c': {'capital': 0.35, 'market': 0.30, 'people': 0.20, 'advantage': 0.15}
}

print("Testing Stage-Specific Weights")
print("=" * 60)

for stage in stages:
    # Test data for each stage
    test_data = {
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 200000,
        "sector": "saas",
        "team_size_full_time": 25,
        "product_stage": "growth",
        "funding_stage": stage,
        "annual_revenue_run_rate": 2000000,
        "customer_count": 100
    }
    
    # Make API request
    response = requests.post(
        "http://localhost:8001/predict",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n{stage.upper()} Stage:")
        print(f"  Success Probability: {result['success_probability']:.1%}")
        
        # The expected most important factor for each stage
        weights = expected_weights[stage]
        most_important = max(weights.items(), key=lambda x: x[1])
        print(f"  Should prioritize: {most_important[0].capitalize()} ({most_important[1]:.0%})")
        
        # Check what the frontend would display
        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        print(f"  Expected order: {' > '.join([f'{k.capitalize()}' for k, v in sorted_weights])}")
        
    else:
        print(f"\n{stage.upper()} Stage: ERROR - {response.status_code}")

print("\n" + "=" * 60)
print("Summary:")
print("- Pre-seed/Seed: Should prioritize PEOPLE")
print("- Series A/B: Should prioritize MARKET")
print("- Series C: Should prioritize CAPITAL")
print("\nIf the frontend always shows Series A priorities (Market first),")
print("then the funding_stage is not being passed or used correctly.")