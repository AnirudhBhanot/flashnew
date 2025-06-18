#!/usr/bin/env python3
"""
Simple test script for contractual models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.model_wrapper import ContractualModel
from core.feature_registry import feature_registry

# Load a model
print("Loading DNA Analyzer model...")
model = ContractualModel.load('models/contractual/dna_analyzer.pkl', feature_registry)

print(f"Model loaded: {model.metadata.model_name}")
print(f"Contract expects: {model.contract.feature_count} features")

# Create test data
test_data = {
    'funding_stage': 'seed',
    'revenue_growth_rate': 150.0,
    'team_size_full_time': 15,
    'total_capital_raised_usd': 2000000.0,
    'annual_recurring_revenue_millions': 1.0,
    'annual_revenue_run_rate': 1000000.0,
    'burn_multiple': 1.5,
    'market_tam_billions': 10.0,
    'market_growth_rate': 25.0,
    'market_competitiveness': 3,
    'customer_acquisition_cost': 200.0,
    'customer_lifetime_value': 2000.0,
    'customer_growth_rate': 100.0,
    'net_revenue_retention': 120.0,
    'average_deal_size': 5000.0,
    'sales_cycle_days': 45,
    'international_revenue_percent': 20.0,
    'target_enterprise': False,
    'product_market_fit_score': 4,
    'technology_score': 4,
    'scalability_score': 5,
    'has_patent': True,
    'research_development_percent': 20.0,
    'uses_ai_ml': True,
    'cloud_native': True,
    'mobile_first': False,
    'platform_business': True,
    'founder_experience_years': 12,
    'repeat_founder': True,
    'technical_founder': True,
    'employee_growth_rate': 150.0,
    'advisor_quality_score': 4,
    'board_diversity_score': 4,
    'team_industry_experience': 10,
    'key_person_dependency': 2,
    'top_university_alumni': True,
    'investor_tier_primary': 'tier_1',
    'active_investors': 5,
    'cash_on_hand_months': 24.0,
    'runway_months': 24.0,
    'time_to_next_funding': 12,
    'previous_exit': True,
    'industry_connections': 5,
    'media_coverage': 4,
    'regulatory_risk': 2
}

print("\nValidating input data...")
is_valid, errors = model.contract.validate_input(test_data)
print(f"Validation result: {is_valid}")
if not is_valid:
    print(f"Errors: {errors}")

print("\nMaking prediction...")
try:
    prediction, diagnostics = model.predict(test_data, return_diagnostics=True)
    print(f"Prediction: {prediction[0]:.4f}")
    print(f"Duration: {diagnostics['duration_ms']:.1f}ms")
    print(f"Features prepared: {diagnostics['features_prepared']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()