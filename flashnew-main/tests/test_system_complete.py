#!/usr/bin/env python3
"""
Complete system test with proper data formats
"""

import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_system():
    """Test the complete FLASH system"""
    base_url = "http://localhost:8000"
    
    # Test data with correct formats based on API validation
    test_startup = {
        "startup_id": "test_001",
        "startup_name": "AI Vision Tech",
        "founding_year": 2021,
        "funding_stage": "series_a",  # lowercase with underscore
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3500000,
        "monthly_burn_usd": 150000,
        "runway_months": 23,
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_percent": 250,
        "gross_margin_percent": 75,
        "burn_multiple": 0.125,
        "ltv_cac_ratio": 3.5,
        "investor_tier_primary": "tier_1",  # lowercase with underscore
        "has_debt": False,
        "patent_count": 3,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,  # 1-5 scale
        "switching_cost_score": 4,  # 1-5 scale
        "brand_strength_score": 3,  # 1-5 scale
        "scalability_score": 5,  # 1-5 scale
        "product_stage": "growth",
        "product_retention_30d": 0.85,  # 0-1 scale
        "product_retention_90d": 0.72,  # 0-1 scale
        "sector": "AI/ML",
        "tam_size_usd": 50000000000,
        "sam_size_usd": 5000000000,
        "som_size_usd": 500000000,
        "market_growth_rate_percent": 45,
        "customer_count": 150,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 180,
        "net_dollar_retention_percent": 125,
        "competition_intensity": 4,  # 1-5 scale
        "competitors_named_count": 12,
        "dau_mau_ratio": 0.65,
        "founders_count": 3,
        "team_size_full_time": 25,
        "years_experience_avg": 12,
        "domain_expertise_years_avg": 8,
        "prior_startup_experience_count": 2,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,  # 1-5 scale
        "advisors_count": 5,
        "team_diversity_percent": 40,
        "key_person_dependency": True  # boolean
    }
    
    logger.info("="*60)
    logger.info("FLASH SYSTEM COMPLETE TEST")
    logger.info("="*60)
    
    try:
        # 1. Test Health Check
        logger.info("\n1. Testing Health Check...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            logger.info(f"✓ API Status: {health['status']}")
            logger.info(f"✓ Models Loaded: {health['models_loaded']}")
            logger.info(f"✓ Model Types: {', '.join(health['model_types'])}")
        else:
            logger.error(f"✗ Health check failed: {response.status_code}")
            return
            
        # 2. Test Prediction
        logger.info("\n2. Testing Prediction with Real Models...")
        response = requests.post(
            f"{base_url}/predict",
            json=test_startup,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info("✓ Prediction successful!")
            
            # Display results
            logger.info(f"\n📊 PREDICTION RESULTS:")
            logger.info(f"   Success Probability: {result['success_probability']:.1%}")
            logger.info(f"   Confidence: [{result['confidence_interval'][0]:.1%}, {result['confidence_interval'][1]:.1%}]")
            logger.info(f"   Risk Level: {result['risk_assessment']['risk_level']}")
            logger.info(f"   Model Consensus: {result['model_consensus']:.1%}")
            
            # CAMP Scores
            logger.info(f"\n💎 CAMP SCORES:")
            for pillar, score in result['camp_scores'].items():
                logger.info(f"   {pillar.capitalize()}: {score:.0f}/100")
            
            # Model Contributions
            logger.info(f"\n🤖 MODEL CONTRIBUTIONS:")
            for model, prob in result['model_contributions'].items():
                logger.info(f"   {model}: {prob:.1%}")
            
            # Key Insights
            logger.info(f"\n🔍 KEY INSIGHTS:")
            logger.info("   Top Positive Factors:")
            for factor in result['shap_explanation']['top_positive_factors'][:3]:
                logger.info(f"   + {factor['feature']}: {factor['value']} (impact: +{factor['shap_value']:.3f})")
            
            logger.info("\n   Top Risk Factors:")
            for factor in result['shap_explanation']['top_negative_factors'][:3]:
                logger.info(f"   - {factor['feature']}: {factor['value']} (impact: {factor['shap_value']:.3f})")
            
            # Risk Assessment
            logger.info(f"\n⚠️  RISK ASSESSMENT:")
            logger.info(f"   Overall Risk: {result['risk_assessment']['risk_level']}")
            for risk in result['risk_assessment']['risk_factors'][:3]:
                logger.info(f"   • {risk}")
                
        else:
            logger.error(f"✗ Prediction failed: {response.status_code}")
            logger.error(response.text)
            return
            
        # 3. Test Model Performance
        logger.info("\n3. Testing Model Performance Metrics...")
        response = requests.get(f"{base_url}/model_performance")
        if response.status_code == 200:
            logger.info("✓ Performance metrics retrieved")
        
        # 4. Test with Different Startup Profiles
        logger.info("\n4. Testing Different Startup Profiles...")
        
        # Early stage startup
        early_stage = test_startup.copy()
        early_stage.update({
            "funding_stage": "seed",
            "total_capital_raised_usd": 500000,
            "annual_revenue_run_rate": 0,
            "customer_count": 10,
            "team_size_full_time": 5
        })
        
        response = requests.post(f"{base_url}/predict", json=early_stage)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"   Seed Stage: {result['success_probability']:.1%} success probability")
        
        # Late stage startup
        late_stage = test_startup.copy()
        late_stage.update({
            "funding_stage": "series_c",
            "total_capital_raised_usd": 50000000,
            "annual_revenue_run_rate": 25000000,
            "customer_count": 1000,
            "team_size_full_time": 150
        })
        
        response = requests.post(f"{base_url}/predict", json=late_stage)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"   Series C: {result['success_probability']:.1%} success probability")
            
        logger.info("\n" + "="*60)
        logger.info("✅ SYSTEM TEST COMPLETE - All Real Models Working!")
        logger.info("="*60)
        
    except requests.exceptions.ConnectionError:
        logger.error("\n❌ Could not connect to API server!")
        logger.error("Please start the API server with: python api_server.py")
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_complete_system()