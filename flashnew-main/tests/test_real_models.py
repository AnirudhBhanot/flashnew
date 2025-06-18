#!/usr/bin/env python3
"""
Test the complete system with real models
"""

import requests
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_with_real_models():
    """Test API predictions with real models"""
    base_url = "http://localhost:8000"
    
    # Test data - realistic startup
    test_startup = {
        "startup_id": "test_001",
        "startup_name": "AI Vision Tech",
        "founding_year": 2021,
        "funding_stage": "Series A",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3500000,
        "monthly_burn_usd": 150000,
        "runway_months": 23,
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_percent": 250,
        "gross_margin_percent": 75,
        "burn_multiple": 0.125,
        "ltv_cac_ratio": 3.5,
        "investor_tier_primary": "Tier1",
        "has_debt": False,
        "patent_count": 3,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 8,
        "switching_cost_score": 7,
        "brand_strength_score": 6,
        "scalability_score": 9,
        "product_stage": "growth",
        "product_retention_30d": 85,
        "product_retention_90d": 72,
        "sector": "AI/ML",
        "tam_size_usd": 50000000000,
        "sam_size_usd": 5000000000,
        "som_size_usd": 500000000,
        "market_growth_rate_percent": 45,
        "customer_count": 150,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 180,
        "net_dollar_retention_percent": 125,
        "competition_intensity": 7,
        "competitors_named_count": 12,
        "dau_mau_ratio": 0.65,
        "founders_count": 3,
        "team_size_full_time": 25,
        "years_experience_avg": 12,
        "domain_expertise_years_avg": 8,
        "prior_startup_experience_count": 2,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 8,
        "advisors_count": 5,
        "team_diversity_percent": 40,
        "key_person_dependency": 3
    }
    
    try:
        # Test health endpoint
        logger.info("Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        health_data = response.json()
        logger.info(f"Health status: {health_data['status']}")
        logger.info(f"Models loaded: {health_data['models_loaded']}")
        
        # Test prediction
        logger.info("\nTesting prediction with real models...")
        start_time = time.time()
        response = requests.post(
            f"{base_url}/predict",
            json=test_startup,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Prediction successful!")
            logger.info(f"Response time: {(end_time - start_time)*1000:.2f}ms")
            logger.info(f"\nResults:")
            logger.info(f"- Success Probability: {result['success_probability']:.2%}")
            logger.info(f"- Confidence Interval: [{result['confidence_interval'][0]:.2%}, {result['confidence_interval'][1]:.2%}]")
            logger.info(f"- Risk Level: {result['risk_assessment']['risk_level']}")
            
            # Model contributions
            logger.info(f"\nModel Contributions:")
            for model, prob in result['model_contributions'].items():
                logger.info(f"  - {model}: {prob:.2%}")
            
            logger.info(f"\nModel Consensus: {result['model_consensus']:.2%}")
            
            # CAMP scores
            logger.info(f"\nCAMP Scores:")
            for pillar, score in result['camp_scores'].items():
                logger.info(f"  - {pillar}: {score:.2f}/100")
            
            # Top factors
            logger.info(f"\nTop Positive Factors:")
            for factor in result['shap_explanation']['top_positive_factors'][:3]:
                logger.info(f"  - {factor['feature']}: {factor['value']} (impact: {factor['shap_value']:.3f})")
            
            logger.info(f"\nTop Negative Factors:")
            for factor in result['shap_explanation']['top_negative_factors'][:3]:
                logger.info(f"  - {factor['feature']}: {factor['value']} (impact: {factor['shap_value']:.3f})")
                
        else:
            logger.error(f"Prediction failed: {response.status_code}")
            logger.error(response.text)
            
        # Test model performance endpoint
        logger.info("\n" + "="*50)
        logger.info("Testing model performance endpoint...")
        response = requests.get(f"{base_url}/model_performance")
        if response.status_code == 200:
            perf_data = response.json()
            logger.info("Model Performance Metrics:")
            for model, metrics in perf_data['model_metrics'].items():
                logger.info(f"\n{model}:")
                logger.info(f"  - Mean Probability: {metrics['mean_probability']:.3f}")
                logger.info(f"  - Std Deviation: {metrics['std_deviation']:.3f}")
                
        # Test A/B results
        logger.info("\n" + "="*50)
        logger.info("Testing A/B test results...")
        response = requests.get(f"{base_url}/ab_test_results")
        if response.status_code == 200:
            ab_data = response.json()
            logger.info("A/B Test Results:")
            logger.info(f"- Total Predictions: {ab_data['total_predictions']}")
            logger.info(f"- Average Time Saved: {ab_data['avg_time_saved_ms']:.2f}ms")
            
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to API server. Make sure it's running on port 8000")
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")

def test_model_loading():
    """Test direct model loading"""
    import joblib
    
    logger.info("\n" + "="*50)
    logger.info("Testing direct model loading...")
    
    models_to_test = [
        'models/dna_analyzer/dna_pattern_model.pkl',
        'models/temporal_prediction_model.pkl',
        'models/industry_specific_model.pkl',
        'models/startup_dna_analyzer.pkl'
    ]
    
    for model_path in models_to_test:
        try:
            model = joblib.load(model_path)
            logger.info(f"✓ Successfully loaded {model_path}")
            logger.info(f"  Model type: {type(model).__name__}")
        except Exception as e:
            logger.error(f"✗ Failed to load {model_path}: {str(e)}")

if __name__ == "__main__":
    # First test model loading
    test_model_loading()
    
    # Then test API if server is running
    logger.info("\n" + "="*50)
    logger.info("Note: Make sure the API server is running (python api_server.py)")
    logger.info("Waiting 2 seconds before testing API...")
    time.sleep(2)
    
    test_api_with_real_models()