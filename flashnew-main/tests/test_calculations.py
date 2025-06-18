#!/usr/bin/env python3
"""
Test script to examine calculation logic and identify hardcoded/fallback values
"""

import json
import pandas as pd
import numpy as np
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_clean import TypeConverter

# Initialize components
orchestrator = UnifiedOrchestratorV3()
converter = TypeConverter()

# Test Case 1: Full data with proper values
print("=== Test Case 1: Full Data with Proper Values ===")
full_data = {
    'founding_year': 2020,
    'founder_experience_years': 10,
    'team_size': 25,
    'total_funding': 5000000,
    'num_funding_rounds': 2,
    'investor_tier_primary': 'tier_1',
    'technology_score': 4,
    'market_readiness_score': 4,
    'regulatory_advantage_present': True,
    'has_patents': True,
    'patent_count': 3,
    'burn_rate': 250000,
    'runway_months': 20.0,
    'revenue_growth_rate': 150.0,
    'customer_retention_rate': 95.0,
    'tam_size': 10000000000,
    'sam_percentage': 0.1,
    'market_share': 0.01,
    'time_to_market': 6,
    'market_growth_rate': 25.0,
    'competition_score': 3,
    'founder_education_tier': 4,
    'employees_from_top_companies': 0.4,
    'technical_team_percentage': 0.6,
    'advisory_board_score': 4,
    'key_person_dependency': False,
    'funding_stage': 'series_a',
    'location_quality': 4,
    'has_lead_investor': True,
    'has_notable_investors': True,
    'investor_concentration': 0.3,
    'burn_multiple': 1.5,
    'product_launch_months': 8,
    'product_market_fit_score': 4,
    'revenue_model_score': 4,
    'unit_economics_score': 4,
    'scalability_score': 4,
    'r_and_d_intensity': 0.3,
    'network_effects_present': True,
    'viral_coefficient': 1.2,
    'customer_acquisition_cost': 500,
    'ltv_cac_ratio': 3.5,
    'has_data_moat': True,
    'has_debt': False,
    'debt_to_equity': 0.0
}

# Convert and predict
converted_full = converter.convert_frontend_to_backend(full_data)
df_full = pd.DataFrame([converted_full])
result_full = orchestrator.predict(df_full)
print(f"Result: {json.dumps(result_full, indent=2)}")

# Test Case 2: Minimal data (to see fallbacks)
print("\n=== Test Case 2: Minimal Data (Testing Fallbacks) ===")
minimal_data = {
    'founding_year': 2022,
    'founder_experience_years': 5,
    'team_size': 10,
    'total_funding': 1000000,
    'num_funding_rounds': 1,
    'investor_tier_primary': 'tier_3',
    'technology_score': 3,
    'market_readiness_score': 3,
    'burn_rate': 100000,
    'revenue_growth_rate': 50.0,
    'customer_retention_rate': 80.0,
    'tam_size': 1000000000,
    'sam_percentage': 0.05,
    'market_share': 0.001,
    'time_to_market': 12,
    'market_growth_rate': 15.0,
    'competition_score': 3,
    'founder_education_tier': 3,
    'employees_from_top_companies': 0.2,
    'technical_team_percentage': 0.5,
    'advisory_board_score': 3,
    'funding_stage': 'seed',
    'location_quality': 3,
    'investor_concentration': 0.5,
    'product_launch_months': 12,
    'product_market_fit_score': 3,
    'revenue_model_score': 3,
    'unit_economics_score': 3,
    'scalability_score': 3,
    'r_and_d_intensity': 0.2,
    'viral_coefficient': 0.8,
    'customer_acquisition_cost': 1000,
    'ltv_cac_ratio': 2.0
}

converted_minimal = converter.convert_frontend_to_backend(minimal_data)
df_minimal = pd.DataFrame([converted_minimal])
result_minimal = orchestrator.predict(df_minimal)
print(f"Result: {json.dumps(result_minimal, indent=2)}")

# Test Case 3: Check CAMP score calculations specifically
print("\n=== Test Case 3: CAMP Score Calculation Details ===")

# Test with extreme values to see if actual calculations happen
extreme_data = full_data.copy()
extreme_data.update({
    # Capital extremes
    'total_funding': 50000000,  # Very high
    'burn_rate': 50000,  # Very low
    'runway_months': 100.0,  # Very high
    'ltv_cac_ratio': 10.0,  # Very high
    
    # Advantage extremes
    'patent_count': 20,  # Very high
    'network_effects_present': True,
    'has_data_moat': True,
    'scalability_score': 5,
    
    # Market extremes
    'tam_size': 100000000000,  # Very high
    'market_growth_rate': 100.0,  # Very high
    'customer_retention_rate': 99.0,  # Very high
    
    # People extremes
    'team_size': 100,  # Very high
    'founder_experience_years': 20,  # Very high
    'employees_from_top_companies': 0.8,  # Very high
})

converted_extreme = converter.convert_frontend_to_backend(extreme_data)
df_extreme = pd.DataFrame([converted_extreme])

# Access internal CAMP calculation
camp_features = orchestrator._prepare_dna_features(df_extreme)
print(f"CAMP Features columns: {list(camp_features.columns[-4:])}")
print(f"CAMP Scores: {camp_features[['capital_score', 'advantage_score', 'market_score', 'people_score']].iloc[0].to_dict()}")

result_extreme = orchestrator.predict(df_extreme)
print(f"Extreme values result: {json.dumps(result_extreme, indent=2)}")

# Test Case 4: Check for 0.5 fallbacks
print("\n=== Test Case 4: Checking for 0.5 Fallbacks ===")

# Count occurrences of 0.5 in predictions
def count_half_values(result):
    count = 0
    for key, value in result.get('model_predictions', {}).items():
        if abs(value - 0.5) < 0.001:
            count += 1
            print(f"  - {key}: {value} (likely fallback)")
    return count

print("Full data 0.5 values:")
count_full = count_half_values(result_full)

print("\nMinimal data 0.5 values:")
count_minimal = count_half_values(result_minimal)

print("\nExtreme data 0.5 values:")
count_extreme = count_half_values(result_extreme)

# Test Case 5: Test with missing models
print("\n=== Test Case 5: Model Loading Status ===")
model_info = orchestrator.get_model_info()
print(f"Models loaded: {model_info['models_loaded']}")
print(f"Pattern system: {model_info['pattern_system']}")
print(f"Total models: {model_info['total_models']}")

# Test Case 6: Test financial calculations
print("\n=== Test Case 6: Financial Metric Calculations ===")
financial_test = {
    'monthly_burn_usd': 250000,
    'cash_on_hand_usd': 5000000,
    'annual_revenue_run_rate': 3000000,
    'customer_acquisition_cost': 500,
    'customer_lifetime_value': 2000,
}

# Check if these are used in calculations
print(f"Expected runway: {financial_test['cash_on_hand_usd'] / financial_test['monthly_burn_usd']} months")
print(f"Expected LTV/CAC: {financial_test['customer_lifetime_value'] / financial_test['customer_acquisition_cost']}")
print(f"Expected burn multiple: {financial_test['monthly_burn_usd'] * 12 / financial_test['annual_revenue_run_rate']}")