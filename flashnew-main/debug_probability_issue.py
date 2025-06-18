#!/usr/bin/env python3
"""Debug why low scores give high probabilities"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3

# Create test data with terrible scores
test_data = {
    # Capital - all bad
    'total_capital_raised_usd': 10000,
    'cash_on_hand_usd': 5000,
    'monthly_burn_usd': 20000,
    'runway_months': 0.25,
    'burn_multiple': 10,
    'investor_tier_primary': 0,
    'has_debt': 1,
    
    # Advantage - all bad
    'patent_count': 0,
    'network_effects_present': 0,
    'has_data_moat': 0,
    'regulatory_advantage_present': 0,
    'tech_differentiation_score': 1,
    'switching_cost_score': 1,
    'brand_strength_score': 1,
    'scalability_score': 1,
    
    # Market - all bad
    'sector': 0,
    'tam_size_usd': 1000000,
    'sam_size_usd': 100000,
    'som_size_usd': 10000,
    'market_growth_rate_percent': 0,
    'customer_count': 1,
    'customer_concentration_percent': 100,
    'user_growth_rate_percent': -10,
    'net_dollar_retention_percent': 50,
    'competition_intensity': 5,
    'competitors_named_count': 20,
    
    # People - all bad
    'founders_count': 1,
    'team_size_full_time': 1,
    'years_experience_avg': 0,
    'domain_expertise_years_avg': 0,
    'prior_startup_experience_count': 0,
    'prior_successful_exits_count': 0,
    'board_advisor_experience_score': 1,
    'advisors_count': 0,
    'team_diversity_percent': 0,
    'key_person_dependency': 1,
    
    # Product features - all bad
    'product_stage': 0,
    'product_retention_30d': 10,
    'product_retention_90d': 5,
    'dau_mau_ratio': 0.05,
    'annual_revenue_run_rate': 0,
    'revenue_growth_rate_percent': -50,
    'gross_margin_percent': -20,
    'ltv_cac_ratio': 0.1,
    'funding_stage': 0
}

print("Testing with TERRIBLE startup data (all worst possible values)...\n")

# Initialize orchestrator
try:
    orchestrator = UnifiedOrchestratorV3()
    print("✅ Orchestrator initialized")
    
    # Check which models are loaded
    print(f"\nModels loaded: {list(orchestrator.models.keys())}")
    print(f"Pattern system: {'Yes' if orchestrator.pattern_system else 'No'}")
    
    # Create DataFrame
    features_df = pd.DataFrame([test_data])
    print(f"\nFeature shape: {features_df.shape}")
    
    # Try prediction
    print("\nAttempting prediction...")
    result = orchestrator.predict(features_df)
    
    print("\n🔍 RESULTS:")
    print(f"Success Probability: {result['success_probability']:.1%}")
    print(f"Verdict: {result.get('verdict', 'N/A')}")
    
    if 'model_predictions' in result:
        print("\nIndividual Model Predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  {model}: {pred:.1%}")
    
    if 'weights_used' in result:
        print("\nWeights Used:")
        for component, weight in result['weights_used'].items():
            print(f"  {component}: {weight:.0%}")
    
    # Check if fallback was used
    if result['success_probability'] == 0.65:
        print("\n⚠️ WARNING: Fallback prediction detected (65% is the hardcoded default)")
    
except Exception as e:
    print(f"\n❌ ERROR during prediction: {e}")
    import traceback
    traceback.print_exc()

# Also test CAMP score calculation
print("\n\nTesting CAMP score calculation...")
from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES

features_df = pd.DataFrame([test_data])
numeric_features = features_df.select_dtypes(include=['int', 'float', 'int64', 'float64'])

for name, feature_list in [
    ('Capital', CAPITAL_FEATURES),
    ('Advantage', ADVANTAGE_FEATURES),
    ('Market', MARKET_FEATURES),
    ('People', PEOPLE_FEATURES)
]:
    cols = [f for f in feature_list if f in numeric_features.columns]
    if cols:
        score = numeric_features[cols].mean(axis=1).fillna(0).iloc[0]
        print(f"{name}: {score:.1%} (from {len(cols)} features)")
    else:
        print(f"{name}: No features found!")