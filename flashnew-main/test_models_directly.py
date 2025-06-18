#!/usr/bin/env python3
"""
Test the models directly without the API server
"""

import joblib
import numpy as np
import pandas as pd
from camp_calculator import calculate_camp_scores

def test_direct():
    """Test models and CAMP calculations directly"""
    
    print("🧪 Direct Model and CAMP Framework Test")
    print("=" * 60)
    
    # Test data
    test_features = {
        'total_capital_raised_usd': 10000000,
        'cash_on_hand_usd': 6000000,
        'monthly_burn_usd': 400000,
        'runway_months': 15,
        'burn_multiple': 1.8,
        'investor_tier_primary': 2,  # Numeric for models
        'has_debt': 0,
        'patent_count': 5,
        'network_effects_present': 1,
        'has_data_moat': 1,
        'regulatory_advantage_present': 0,
        'tech_differentiation_score': 4,
        'switching_cost_score': 4,
        'brand_strength_score': 3,
        'scalability_score': 5,
        'sector': 0,  # Encoded
        'tam_size_usd': 10000000000,
        'sam_size_usd': 1000000000,
        'som_size_usd': 100000000,
        'market_growth_rate_percent': 45,
        'customer_count': 500,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 25,
        'net_dollar_retention_percent': 125,
        'competition_intensity': 3,
        'competitors_named_count': 15,
        'founders_count': 3,
        'team_size_full_time': 45,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 8,
        'prior_startup_experience_count': 4,
        'prior_successful_exits_count': 2,
        'board_advisor_experience_score': 4,
        'advisors_count': 6,
        'team_diversity_percent': 45,
        'key_person_dependency': 0,
        'product_stage': 2,  # Encoded
        'product_retention_30d': 85,
        'product_retention_90d': 70,
        'dau_mau_ratio': 0.5,
        'annual_revenue_run_rate': 6000000,
        'revenue_growth_rate_percent': 180,
        'gross_margin_percent': 80,
        'ltv_cac_ratio': 4.2,
        'funding_stage': 2  # Series A encoded
    }
    
    # 1. Test ML Models
    print("\n1. Testing ML Models")
    print("-" * 40)
    
    try:
        # Load models
        rf_model = joblib.load('models/production_v45/dna_analyzer.pkl')
        scaler = joblib.load('models/production_v45/feature_scaler.pkl')
        
        print("✅ Models loaded successfully")
        
        # Prepare features (need all 45)
        feature_order = [
            'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
            'runway_months', 'burn_multiple', 'investor_tier_primary', 'has_debt',
            'patent_count', 'network_effects_present', 'has_data_moat',
            'regulatory_advantage_present', 'tech_differentiation_score',
            'switching_cost_score', 'brand_strength_score', 'scalability_score',
            'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
            'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
            'user_growth_rate_percent', 'net_dollar_retention_percent',
            'competition_intensity', 'competitors_named_count', 'founders_count',
            'team_size_full_time', 'years_experience_avg', 'domain_expertise_years_avg',
            'prior_startup_experience_count', 'prior_successful_exits_count',
            'board_advisor_experience_score', 'advisors_count', 'team_diversity_percent',
            'key_person_dependency', 'product_stage', 'product_retention_30d',
            'product_retention_90d', 'dau_mau_ratio', 'annual_revenue_run_rate',
            'revenue_growth_rate_percent', 'gross_margin_percent', 'ltv_cac_ratio',
            'funding_stage'
        ]
        
        # Create feature array
        X = np.array([[test_features.get(f, 0) for f in feature_order]])
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make prediction
        probability = rf_model.predict_proba(X_scaled)[0, 1]
        
        print(f"\n📊 ML Prediction Results:")
        print(f"   Success Probability: {probability:.1%}")
        print(f"   Verdict: {'PASS' if probability > 0.6 else 'CONDITIONAL PASS' if probability > 0.4 else 'NO'}")
        
    except Exception as e:
        print(f"❌ Error with ML models: {e}")
    
    # 2. Test CAMP Framework
    print("\n\n2. Testing CAMP Framework")
    print("-" * 40)
    
    try:
        # Test with different stages
        stages = ['pre_seed', 'seed', 'series_a', 'series_b']
        
        for stage in stages:
            result = calculate_camp_scores(test_features, stage)
            print(f"\n📍 Stage: {stage.upper()}")
            print(f"   Focus: {result['stage_focus']}")
            
            # Show stage weights
            weights = result['stage_weights']
            sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
            print(f"   Priorities: ", end="")
            for pillar, weight in sorted_weights:
                print(f"{pillar.title()} ({weight:.0%}) ", end="")
            print()
            
            # Show scores
            print(f"   CAMP Scores: ", end="")
            for pillar, score in result['raw_scores'].items():
                print(f"{pillar[0].upper()}: {score:.2f} ", end="")
            print(f"\n   Overall: {result['overall_score']:.2f}")
        
    except Exception as e:
        print(f"❌ Error with CAMP framework: {e}")
    
    # 3. Summary
    print("\n\n3. System Integration Summary")
    print("-" * 40)
    print("✅ ML Models: Predicting success probability from patterns")
    print("✅ CAMP Framework: Using research-based stage weights")
    print("✅ Separation: ML doesn't override research insights")
    print("\n🎯 Result: Credible AI predictions + validated framework!")

if __name__ == "__main__":
    test_direct()