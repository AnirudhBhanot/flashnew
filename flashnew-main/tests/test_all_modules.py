#!/usr/bin/env python3
"""
Simple integration test for all FLASH modules
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from pathlib import Path


def create_test_data():
    """Create test startup data"""
    return pd.DataFrame([{
        # Capital features
        'funding_stage': 'series_a',
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 3000000,
        'monthly_burn_usd': 150000,
        'runway_months': 20,
        'annual_revenue_run_rate': 1200000,
        'revenue_growth_rate_percent': 150,
        'gross_margin_percent': 65,
        'burn_multiple': 1.5,
        'ltv_cac_ratio': 3.0,
        'investor_tier_primary': 'tier_2',
        'has_debt': 0,
        
        # Advantage features
        'patent_count': 2,
        'network_effects_present': 1,
        'has_data_moat': 1,
        'regulatory_advantage_present': 0,
        'tech_differentiation_score': 4,
        'switching_cost_score': 3,
        'brand_strength_score': 3,
        'scalability_score': 4,
        'product_stage': 'growth',
        'product_retention_30d': 0.75,
        'product_retention_90d': 0.65,
        
        # Market features
        'sector': 'SaaS',
        'tam_size_usd': 50000000000,
        'sam_size_usd': 5000000000,
        'som_size_usd': 500000000,
        'market_growth_rate_percent': 25,
        'customer_count': 100,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 200,
        'net_dollar_retention_percent': 110,
        'competition_intensity': 3,
        'competitors_named_count': 10,
        'dau_mau_ratio': 0.4,
        
        # People features
        'founders_count': 2,
        'team_size_full_time': 25,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 8,
        'prior_startup_experience_count': 2,
        'prior_successful_exits_count': 1,
        'board_advisor_experience_score': 4,
        'advisors_count': 4,
        'team_diversity_percent': 40,
        'key_person_dependency': 0
    }])


def test_stage_hierarchical():
    """Test Stage Hierarchical Model"""
    print("\n1. Testing Stage Hierarchical Model...")
    try:
        from stage_hierarchical_models import StageHierarchicalModel
        
        model = StageHierarchicalModel()
        # Use default model path
        model.load_models('models/stage_hierarchical')
        
        df = create_test_data()
        result = model.predict(df)
        
        assert 'prediction' in result
        assert 0 <= result['prediction'] <= 1
        print("✅ Stage Hierarchical Model works correctly")
        print(f"   Prediction: {result['prediction']:.2%}")
        return True
    except Exception as e:
        print(f"❌ Stage Hierarchical Model failed: {e}")
        return False


def test_dna_analyzer():
    """Test DNA Pattern Analyzer"""
    print("\n2. Testing DNA Pattern Analyzer...")
    try:
        from dna_pattern_analysis import StartupDNAAnalyzer
        
        analyzer = StartupDNAAnalyzer()
        analyzer.load_models()
        
        df = create_test_data()
        result = analyzer.analyze(df)
        
        assert 'success_probability' in result
        assert 0 <= result['success_probability'] <= 1
        print("✅ DNA Pattern Analyzer works correctly")
        print(f"   Success Probability: {result['success_probability']:.2%}")
        return True
    except Exception as e:
        print(f"❌ DNA Pattern Analyzer failed: {e}")
        return False


def test_temporal_model():
    """Test Temporal Prediction Model"""
    print("\n3. Testing Temporal Prediction Model...")
    try:
        from temporal_models import TemporalPredictionModel
        
        model = TemporalPredictionModel()
        model.load_models()
        
        df = create_test_data()
        result = model.predict_timeline(df)
        
        assert 'current_prediction' in result
        assert 0 <= result['current_prediction'] <= 1
        print("✅ Temporal Prediction Model works correctly")
        print(f"   Current Prediction: {result['current_prediction']:.2%}")
        return True
    except Exception as e:
        print(f"❌ Temporal Prediction Model failed: {e}")
        return False


def test_industry_model():
    """Test Industry Specific Model"""
    print("\n4. Testing Industry Specific Model...")
    try:
        from industry_specific_models import IndustrySpecificModel
        
        model = IndustrySpecificModel()
        model.load_models()
        
        df = create_test_data()
        result = model.predict(df)
        
        assert 'prediction' in result
        assert 0 <= result['prediction'] <= 1
        print("✅ Industry Specific Model works correctly")
        print(f"   Prediction: {result['prediction']:.2%}")
        print(f"   Industry: {result.get('industry', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Industry Specific Model failed: {e}")
        return False


def test_optimized_pipeline():
    """Test Optimized Model Pipeline"""
    print("\n5. Testing Optimized Model Pipeline...")
    try:
        from model_improvements_fixed import OptimizedModelPipeline
        
        pipeline = OptimizedModelPipeline()
        
        df = create_test_data()
        result = pipeline.predict_with_confidence(df)
        
        assert 'predictions' in result
        assert len(result['predictions']) > 0
        print("✅ Optimized Model Pipeline works correctly")
        print(f"   Predictions: {result['predictions']}")
        return True
    except Exception as e:
        print(f"❌ Optimized Model Pipeline failed: {e}")
        return False


def test_production_ensemble():
    """Test Production Ensemble"""
    print("\n6. Testing Production Ensemble...")
    try:
        from final_ensemble_integration import FinalProductionEnsemble
        
        ensemble = FinalProductionEnsemble()
        ensemble.load_models()
        
        df = create_test_data()
        result = ensemble.predict(df)
        
        assert 'success_probability' in result
        print("✅ Production Ensemble works correctly")
        print(f"   Success Probability: {result.get('success_probability', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Production Ensemble failed: {e}")
        return False


def test_shap_explainer():
    """Test SHAP Explainer"""
    print("\n7. Testing SHAP Explainer...")
    try:
        from shap_explainer import FLASHExplainer
        
        explainer = FLASHExplainer()
        
        df = create_test_data()
        result = explainer.explain_prediction(df, include_plots=False)
        
        assert 'ensemble_prediction' in result
        assert 0 <= result['ensemble_prediction'] <= 1
        print("✅ SHAP Explainer works correctly")
        print(f"   Ensemble Prediction: {result['ensemble_prediction']:.2%}")
        print(f"   Models Used: {list(result.get('model_predictions', {}).keys())}")
        return True
    except Exception as e:
        print(f"❌ SHAP Explainer failed: {e}")
        return False


def test_api_integration():
    """Test API Server Integration"""
    print("\n8. Testing API Server Integration...")
    try:
        # Test if we can import the API models
        from api_server_unified import StartupMetrics, PredictionResponse
        
        # Create test data using the API schema
        test_metrics = {
            'funding_stage': 'series_a',
            'total_capital_raised_usd': 5000000,
            'cash_on_hand_usd': 3000000,
            'monthly_burn_usd': 150000,
            'annual_revenue_run_rate': 1200000,
            'revenue_growth_rate_percent': 150,
            'gross_margin_percent': 65,
            'ltv_cac_ratio': 3.0,
            'investor_tier_primary': 'tier_2',
            'has_debt': False,
            'patent_count': 2,
            'network_effects_present': True,
            'has_data_moat': True,
            'regulatory_advantage_present': False,
            'tech_differentiation_score': 4,
            'switching_cost_score': 3,
            'brand_strength_score': 3,
            'scalability_score': 4,
            'product_stage': 'growth',
            'product_retention_30d': 0.75,
            'product_retention_90d': 0.65,
            'sector': 'SaaS',
            'tam_size_usd': 50000000000,
            'sam_size_usd': 5000000000,
            'som_size_usd': 500000000,
            'market_growth_rate_percent': 25,
            'customer_count': 100,
            'customer_concentration_percent': 15,
            'user_growth_rate_percent': 200,
            'net_dollar_retention_percent': 110,
            'competition_intensity': 3,
            'competitors_named_count': 10,
            'dau_mau_ratio': 0.4,
            'founders_count': 2,
            'team_size_full_time': 25,
            'years_experience_avg': 12,
            'domain_expertise_years_avg': 8,
            'prior_startup_experience_count': 2,
            'prior_successful_exits_count': 1,
            'board_advisor_experience_score': 4,
            'advisors_count': 4,
            'team_diversity_percent': 40,
            'key_person_dependency': False
        }
        
        # Validate with Pydantic model
        metrics = StartupMetrics(**test_metrics)
        
        print("✅ API Integration works correctly")
        print(f"   Validated {len(metrics.model_fields)} fields")
        return True
    except Exception as e:
        print(f"❌ API Integration failed: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("FLASH Platform - Module Integration Tests")
    print("="*60)
    
    tests = [
        test_stage_hierarchical,
        test_dna_analyzer,
        test_temporal_model,
        test_industry_model,
        test_optimized_pipeline,
        test_production_ensemble,
        test_shap_explainer,
        test_api_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! The FLASH platform is fully integrated.")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)