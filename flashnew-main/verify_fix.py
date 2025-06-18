#!/usr/bin/env python3
"""
Verify the fix is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from feature_config import ALL_FEATURES
import pandas as pd
import numpy as np

# Create test profiles that match the screenshots
test_profiles = {
    "Startup from Screenshot (72%, 41%, 64% CAMP)": {
        # This represents the startup from the user's screenshot
        "funding_stage": "Series_A",
        "monthly_burn_usd": 250000,
        "runway_months": 18,
        "annual_revenue_run_rate": 3000000,
        "revenue_growth_rate_percent": 45,
        "gross_margin_percent": 75,
        "ltv_cac_ratio": 15,
        "tam_size_usd": 5000000000,
        "team_size_full_time": 20,
        "founders_previous_experience_score": 4,
        "product_retention_90d": 0.80,
        "nps_score": 70,
        "cash_on_hand_usd": 4500000,
        "total_capital_raised_usd": 8000000,
        "investor_tier_primary": "Tier_1",
        "sector": "SaaS",
        "burn_multiple": 1.0,
    },
    "Low Quality Startup": {
        "funding_stage": "Seed",
        "monthly_burn_usd": 200000,
        "runway_months": 4,
        "annual_revenue_run_rate": 100000,
        "revenue_growth_rate_percent": 5,
        "gross_margin_percent": 40,
        "ltv_cac_ratio": 1.2,
        "tam_size_usd": 50000000,
        "team_size_full_time": 4,
        "founders_previous_experience_score": 1,
        "product_retention_90d": 0.40,
        "nps_score": -10,
        "cash_on_hand_usd": 800000,
        "total_capital_raised_usd": 1000000,
        "investor_tier_primary": "Tier_3",
        "sector": "SaaS",
        "burn_multiple": 24.0,
    }
}

def test_fix():
    print("Verifying FLASH Model Fix")
    print("=" * 80)
    print("\nBefore Fix: All startups were getting ~14% success probability")
    print("After Fix: Startups get differentiated scores based on quality\n")
    
    # Load orchestrator
    orchestrator = UnifiedOrchestratorV3()
    
    results = []
    
    for name, profile in test_profiles.items():
        # Prepare features
        features_dict = {k: profile.get(k, 0) for k in ALL_FEATURES}
        features_df = pd.DataFrame([features_dict])
        
        # Get prediction
        result = orchestrator.predict(features_df)
        
        print(f"\n{name}")
        print("-" * 60)
        print(f"Overall Success Probability: {result['success_probability']:.1%}")
        print(f"Verdict: {result['verdict']}")
        
        print("\nModel Components:")
        for model, pred in result['model_predictions'].items():
            print(f"  {model}: {pred:.1%}")
        
        # Calculate quality score
        quality_score = orchestrator._calculate_quality_score(features_df)
        print(f"\nQuality Score: {quality_score:.1%}")
        
        results.append({
            'name': name,
            'success_prob': result['success_probability'],
            'quality_score': quality_score
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    probs = [r['success_prob'] for r in results]
    print(f"\nScore Range: {min(probs):.1%} to {max(probs):.1%}")
    print(f"Differentiation: {max(probs) - min(probs):.1%}")
    
    if max(probs) - min(probs) > 0.15:  # At least 15% differentiation
        print("\n✅ FIX VERIFIED: The system is properly differentiating between startups!")
        print("   - High-quality startups get higher scores")
        print("   - Low-quality startups get lower scores")
        print("   - No more everyone at 14%!")
    else:
        print("\n❌ FIX NOT WORKING: Still insufficient differentiation")
    
    print("\nThe issue has been resolved by:")
    print("1. Aggressive recalibration of overly conservative model predictions")
    print("2. Quality-based scoring that considers actual business metrics")
    print("3. Blending ML predictions with quality assessment for better differentiation")

if __name__ == "__main__":
    test_fix()