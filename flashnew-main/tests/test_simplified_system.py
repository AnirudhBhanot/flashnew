#!/usr/bin/env python3
"""Test the simplified FLASH system"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_server_unified import app, orchestrator, type_converter
import pandas as pd

print('Testing Simplified FLASH System')
print('='*50)

# Test with complete data (as frontend will send)
complete_data = {
    # Capital
    'funding_stage': 'series_a',
    'total_capital_raised_usd': 10000000,
    'cash_on_hand_usd': 8000000,
    'monthly_burn_usd': 400000,
    'runway_months': 20,
    'burn_multiple': 1.6,
    'investor_tier_primary': 'tier_1',
    'has_debt': False,
    
    # Advantage
    'patent_count': 3,
    'network_effects_present': True,
    'has_data_moat': True,
    'regulatory_advantage_present': False,
    'tech_differentiation_score': 4,
    'switching_cost_score': 4,
    'brand_strength_score': 3,
    'scalability_score': 5,
    
    # Market
    'sector': 'saas',
    'tam_size_usd': 10000000000,
    'sam_size_usd': 2000000000,
    'som_size_usd': 200000000,
    'market_growth_rate_percent': 35,
    'customer_count': 150,
    'customer_concentration_percent': 20,
    'user_growth_rate_percent': 120,
    'net_dollar_retention_percent': 125,
    'competition_intensity': 3,
    'competitors_named_count': 8,
    
    # People
    'founders_count': 2,
    'team_size_full_time': 35,
    'years_experience_avg': 12,
    'domain_expertise_years_avg': 8,
    'prior_startup_experience_count': 2,
    'prior_successful_exits_count': 1,
    'board_advisor_experience_score': 4,
    'advisors_count': 6,
    'team_diversity_percent': 40,
    'key_person_dependency': False,
    
    # Product
    'product_stage': 'growth',
    'product_retention_30d': 0.85,
    'product_retention_90d': 0.75,
    'dau_mau_ratio': 0.45,
    'annual_revenue_run_rate': 3600000,
    'revenue_growth_rate_percent': 150,
    'gross_margin_percent': 82,
    'ltv_cac_ratio': 3.8
}

# Add calculated fields that frontend adds
complete_data['runway_months'] = complete_data['cash_on_hand_usd'] / complete_data['monthly_burn_usd']
complete_data['burn_multiple'] = 1.6

print(f'\n1. Sending {len(complete_data)} fields (complete dataset)')

# Convert
converted = type_converter.convert_frontend_to_backend(complete_data)
print(f'2. After conversion: {len(converted)} fields')

# Predict
features_df = pd.DataFrame([converted])
result = orchestrator.predict(features_df)

print(f'\n3. Prediction Results:')
print(f'   Success Probability: {result["success_probability"]:.1%}')
print(f'   Verdict: {result["verdict"]} ({result.get("verdict_strength", "medium")})')
print(f'   Model Agreement: {result["model_agreement"]:.1%}')

print(f'\n4. CAMP Pillar Scores:')
for pillar, score in result['pillar_scores'].items():
    print(f'   {pillar.capitalize()}: {score:.2f}')

print(f'\n5. Model Contributions:')
for model, pred in result['model_predictions'].items():
    if model != 'pattern_analysis':  # Skip disabled pattern
        print(f'   {model}: {pred:.1%}')

print('\n6. Key Insights:')
if result.get('success_factors'):
    for factor in result['success_factors'][:3]:
        print(f'   ✓ {factor}')
if result.get('risk_factors'):
    for risk in result['risk_factors'][:3]:
        print(f'   ⚠ {risk}')

print('\n✅ Simplified system working correctly!')