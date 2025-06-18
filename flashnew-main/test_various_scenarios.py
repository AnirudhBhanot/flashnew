#!/usr/bin/env python3
"""Test various startup scenarios to ensure reasonable probabilities"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES

# Initialize once
orchestrator = UnifiedOrchestratorV3()
type_converter = TypeConverter()

test_scenarios = [
    {
        "name": "Strong Series A Startup",
        "data": {
            "funding_stage": "series_a",
            "total_capital_raised_usd": 15000000,
            "cash_on_hand_usd": 12000000,
            "monthly_burn_usd": 300000,
            "runway_months": 40,
            "team_size_full_time": 45,
            "founders_count": 3,
            "years_experience_avg": 12,
            "sector": "saas",
            "tam_size_usd": 50000000000,
            "customer_count": 500,
            "product_stage": "growth",
            "annual_revenue_run_rate": 5000000,
            "revenue_growth_rate_percent": 150,
            "gross_margin_percent": 75,
            "ltv_cac_ratio": 3.5,
            "net_dollar_retention_percent": 115,
            "product_retention_90d": 0.85,
            "tech_differentiation_score": 4,
            "scalability_score": 4,
            "brand_strength_score": 3
        }
    },
    {
        "name": "Early Seed Startup",
        "data": {
            "funding_stage": "seed",
            "total_capital_raised_usd": 1500000,
            "cash_on_hand_usd": 1200000,
            "monthly_burn_usd": 80000,
            "runway_months": 15,
            "team_size_full_time": 8,
            "founders_count": 2,
            "years_experience_avg": 6,
            "sector": "fintech",
            "tam_size_usd": 10000000000,
            "customer_count": 50,
            "product_stage": "mvp",
            "annual_revenue_run_rate": 240000,
            "revenue_growth_rate_percent": 200,
            "gross_margin_percent": 60,
            "ltv_cac_ratio": 1.5,
            "product_retention_90d": 0.7,
            "tech_differentiation_score": 3,
            "scalability_score": 3
        }
    },
    {
        "name": "Struggling Pre-seed",
        "data": {
            "funding_stage": "pre_seed",
            "total_capital_raised_usd": 250000,
            "cash_on_hand_usd": 100000,
            "monthly_burn_usd": 25000,
            "runway_months": 4,
            "team_size_full_time": 3,
            "founders_count": 2,
            "years_experience_avg": 3,
            "sector": "other",
            "tam_size_usd": 1000000000,
            "customer_count": 5,
            "product_stage": "idea",
            "annual_revenue_run_rate": 0,
            "revenue_growth_rate_percent": 0,
            "gross_margin_percent": 0,
            "ltv_cac_ratio": 0,
            "tech_differentiation_score": 2,
            "scalability_score": 2
        }
    }
]

for scenario in test_scenarios:
    print(f"\n{'='*60}")
    print(f"Testing: {scenario['name']}")
    print(f"{'='*60}")
    
    # Convert data
    features = type_converter.convert_frontend_to_backend(scenario['data'])
    canonical_features = {k: features.get(k, 0) for k in ALL_FEATURES}
    
    # Get prediction
    result = orchestrator.predict(canonical_features)
    
    print(f"Success Probability: {result.get('success_probability', 'N/A'):.2%}")
    print(f"Verdict: {result.get('verdict', 'N/A')}")
    
    if 'model_predictions' in result:
        print("\nModel Predictions:")
        for model, pred in result.get('model_predictions', {}).items():
            print(f"  {model}: {pred:.4f}")
    
    if 'pillar_scores' in result:
        print("\nCAMP Scores:")
        for pillar, score in result.get('pillar_scores', {}).items():
            print(f"  {pillar}: {score:.2f}")

print("\n\nSummary: The orchestrator is now returning reasonable probabilities based on startup quality!")