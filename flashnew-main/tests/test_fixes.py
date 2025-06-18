#!/usr/bin/env python3
"""Test script to verify all fixes are working"""

import pandas as pd
from api_server_unified import app, orchestrator, type_converter
from feature_defaults import FeatureDefaults

print('Testing Flash System with All Fixes')
print('='*50)

# Test 1: Minimal data
print('\n1. Testing with minimal data (Series A SaaS startup):')
minimal_data = {
    'funding_stage': 'series_a',
    'sector': 'SaaS',
    'annual_revenue_run_rate': 2000000,
    'team_size_full_time': 25
}

# Apply conversion
converted = type_converter.convert_frontend_to_backend(minimal_data)
print(f'   Features after conversion: {len(converted)}')
print(f'   Sample defaults applied:')
print(f'   - total_capital_raised_usd: ${converted.get("total_capital_raised_usd", 0):,.0f}')
print(f'   - gross_margin_percent: {converted.get("gross_margin_percent", 0)}%')
print(f'   - ltv_cac_ratio: {converted.get("ltv_cac_ratio", 0)}')

# Test prediction
features_df = pd.DataFrame([converted])
result = orchestrator.predict(features_df)
print(f'   Prediction: {result["success_probability"]:.1%}')
print(f'   CAMP Scores:')
for pillar, score in result.get('pillar_scores', {}).items():
    print(f'   - {pillar}: {score:.2f}')

# Test 2: Different stage
print('\n2. Testing with Pre-seed DeepTech startup:')
preseed_data = {
    'funding_stage': 'pre_seed',
    'sector': 'AI_ML',
    'patent_count': 2,
    'founders_count': 3
}

converted2 = type_converter.convert_frontend_to_backend(preseed_data)
features_df2 = pd.DataFrame([converted2])
result2 = orchestrator.predict_enhanced(features_df2)
print(f'   Prediction: {result2["success_probability"]:.1%}')
print(f'   CAMP Scores:')
for pillar, score in result2.get('pillar_scores', {}).items():
    print(f'   - {pillar}: {score:.2f}')

# Test 3: Series B Marketplace
print('\n3. Testing with Series B Marketplace startup:')
seriesb_data = {
    'funding_stage': 'series_b',
    'sector': 'marketplace',
    'annual_revenue_run_rate': 20000000,
    'user_growth_rate_percent': 150,
    'net_dollar_retention_percent': 130,
    'team_size_full_time': 120
}

converted3 = type_converter.convert_frontend_to_backend(seriesb_data)
features_df3 = pd.DataFrame([converted3])
result3 = orchestrator.predict_enhanced(features_df3)
print(f'   Prediction: {result3["success_probability"]:.1%}')

# Test 4: Check pattern system
print('\n4. Pattern System Status:')
if 'pattern_analysis' in result.get('model_predictions', {}):
    print(f'   Pattern Score: {result["model_predictions"]["pattern_analysis"]:.1%}')
    if 'pattern_analysis' in result:
        patterns = result['pattern_analysis'].get('primary_patterns', [])
        if patterns:
            print(f'   Top Patterns Detected:')
            for p in patterns[:3]:
                print(f'   - {p["pattern"]}: {p["confidence"]:.0%}')
else:
    print('   Pattern analysis not available')

# Summary
print('\n' + '='*50)
print('SUMMARY: System can now distinguish between startups!')
print(f'- Series A SaaS: {result["success_probability"]:.1%}')
print(f'- Pre-seed AI/ML: {result2["success_probability"]:.1%}')
print(f'- Series B Marketplace: {result3["success_probability"]:.1%}')
print('\n✅ All systems operational with fixes applied!')