#!/usr/bin/env python3
"""
Debug CAMP calculation issues
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v3_fixed import UnifiedOrchestratorV3Fixed
from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES

def debug_camp_calculation():
    """Debug the CAMP calculation process"""
    
    # Create test data
    test_data = {
        "total_capital_raised_usd": 10000000,
        "cash_on_hand_usd": 5000000,
        "monthly_burn_usd": 250000,
        "runway_months": 20,
        "burn_multiple": 2,
        "investor_tier_primary": "Tier 1",
        "has_debt": False,
        "patent_count": 5,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,
        "switching_cost_score": 4,
        "brand_strength_score": 3,
        "scalability_score": 4,
        "sector": "SaaS",
        "tam_size_usd": 10000000000,
        "sam_size_usd": 1000000000,
        "som_size_usd": 100000000,
        "market_growth_rate_percent": 40,
        "customer_count": 100,
        "customer_concentration_percent": 20,
        "user_growth_rate_percent": 30,
        "net_dollar_retention_percent": 120,
        "competition_intensity": 3,
        "competitors_named_count": 10,
        "founders_count": 2,
        "team_size_full_time": 40,
        "years_experience_avg": 10,
        "domain_expertise_years_avg": 7,
        "prior_startup_experience_count": 3,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,
        "advisors_count": 5,
        "strategic_partners_count": 3,
        "has_repeat_founder": True,
        "execution_risk_score": 2,
        "vertical_integration_score": 3,
        "time_to_market_advantage_years": 1,
        "partnership_leverage_score": 3,
        "company_age_months": 24,
        "cash_efficiency_score": 1.5,
        "operating_leverage_trend": 1,
        "predictive_modeling_score": 3
    }
    
    # Create orchestrator
    orchestrator = UnifiedOrchestratorV3Fixed()
    
    # Convert to DataFrame
    df = pd.DataFrame([test_data])
    
    print("📊 Debug CAMP Calculation")
    print("=" * 60)
    
    # Step 1: Check raw features
    print("\n1. Raw Features (sample):")
    for feat in ["total_capital_raised_usd", "runway_months", "tech_differentiation_score"]:
        if feat in df.columns:
            print(f"   {feat}: {df[feat].iloc[0]}")
    
    # Step 2: Normalize features
    normalized = orchestrator.normalize_features(df)
    print("\n2. Normalized Features (sample):")
    for feat in ["total_capital_raised_usd", "runway_months", "tech_differentiation_score"]:
        if feat in normalized.columns:
            print(f"   {feat}: {normalized[feat].iloc[0]:.3f}")
    
    # Step 3: Calculate CAMP scores
    camp_scores = orchestrator.calculate_camp_scores(df)
    print("\n3. CAMP Scores:")
    print(f"   Capital:   {camp_scores['capital_score'].iloc[0]:.3f}")
    print(f"   Advantage: {camp_scores['advantage_score'].iloc[0]:.3f}")
    print(f"   Market:    {camp_scores['market_score'].iloc[0]:.3f}")
    print(f"   People:    {camp_scores['people_score'].iloc[0]:.3f}")
    
    # Step 4: Check feature mappings
    print("\n4. Feature Mappings:")
    print(f"   Capital features: {len(CAPITAL_FEATURES)} features")
    print(f"   Available in data: {len([f for f in CAPITAL_FEATURES if f in df.columns])}")
    
    # Step 5: Full prediction
    result = orchestrator.predict(test_data)
    print("\n5. Full Prediction Results:")
    print(f"   Success Probability: {result['success_probability']:.1%}")
    print(f"   CAMP scores from result:")
    camp = result.get('camp_analysis', {})
    print(f"     Capital:   {camp.get('capital', 0):.1%}")
    print(f"     Advantage: {camp.get('advantage', 0):.1%}")
    print(f"     Market:    {camp.get('market', 0):.1%}")
    print(f"     People:    {camp.get('people', 0):.1%}")

if __name__ == "__main__":
    debug_camp_calculation()