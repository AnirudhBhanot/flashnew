#!/usr/bin/env python3
"""
Test the Integrated FLASH System
Tests all components working together
"""

import requests
import json
import logging
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8001"

def test_health_check():
    """Test API health endpoint"""
    logger.info("Testing health check...")
    
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✓ API Status: {data['status']}")
            logger.info(f"  Version: {data['version']}")
            logger.info(f"  Models loaded: {data['models_loaded']}")
            logger.info(f"  Pattern system: {data['pattern_system']}")
            
            if 'feature_alignment' in data:
                logger.info(f"  Feature alignment: {data['feature_alignment']['status']}")
                logger.info(f"  Models needing alignment: {data['feature_alignment']['models_needing_alignment']}")
            
            return True
        else:
            logger.error(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ Cannot connect to API: {e}")
        return False

def test_pattern_list():
    """Test pattern listing endpoint"""
    logger.info("\nTesting pattern listing...")
    
    try:
        response = requests.get(f"{API_URL}/patterns")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✓ Patterns available: {data.get('total', 0)}")
            
            if 'patterns' in data and data['patterns']:
                logger.info("  Sample patterns:")
                for pattern in data['patterns'][:5]:
                    logger.info(f"    - {pattern}")
            
            return True
        else:
            logger.error(f"✗ Pattern listing failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ Pattern listing error: {e}")
        return False

def test_prediction():
    """Test main prediction endpoint"""
    logger.info("\nTesting prediction endpoint...")
    
    # Sample startup data
    test_data = {
        # Capital features
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 3000000,
        'monthly_burn_usd': 200000,
        'runway_months': 15,
        'burn_multiple': 2.5,
        'investor_tier_primary': 'tier_2',
        'has_debt': 0,
        
        # Advantage features
        'patent_count': 2,
        'network_effects_present': 0,
        'has_data_moat': 1,
        'regulatory_advantage_present': 0,
        'tech_differentiation_score': 4,
        'switching_cost_score': 3,
        'brand_strength_score': 3,
        'scalability_score': 4,
        
        # Market features
        'sector': 'enterprise_software',
        'tam_size_usd': 5000000000,
        'sam_size_usd': 1000000000,
        'som_size_usd': 100000000,
        'market_growth_rate_percent': 25,
        'customer_count': 150,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 120,
        'net_dollar_retention_percent': 125,
        'competition_intensity': 3,
        'competitors_named_count': 8,
        
        # People features
        'founders_count': 2,
        'team_size_full_time': 35,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 8,
        'prior_startup_experience_count': 2,
        'prior_successful_exits_count': 1,
        'board_advisor_experience_score': 4,
        'advisors_count': 5,
        'team_diversity_percent': 40,
        'key_person_dependency': 0,
        
        # Product features
        'product_stage': 'growth',
        'product_retention_30d': 0.75,
        'product_retention_90d': 0.65,
        'dau_mau_ratio': 0.4,
        'annual_revenue_run_rate': 3000000,
        'revenue_growth_rate_percent': 150,
        'gross_margin_percent': 80,
        'ltv_cac_ratio': 3.5,
        'funding_stage': 'series_a'
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            
            logger.info("✓ Prediction successful!")
            logger.info(f"  Success probability: {result['success_probability']:.3f}")
            logger.info(f"  Confidence score: {result['confidence_score']:.3f}")
            
            # Check components
            if 'prediction_components' in result:
                logger.info("  Model predictions:")
                for model, score in result['prediction_components'].items():
                    logger.info(f"    - {model}: {score:.3f}")
            
            # Check pattern analysis
            if 'pattern_analysis' in result:
                pattern = result['pattern_analysis']
                logger.info(f"  Pattern score: {pattern.get('pattern_score', 0):.3f}")
                logger.info(f"  Patterns detected: {pattern.get('total_patterns_detected', 0)}")
                
                if 'primary_patterns' in pattern and pattern['primary_patterns']:
                    logger.info("  Primary patterns:")
                    for p in pattern['primary_patterns'][:3]:
                        logger.info(f"    - {p['pattern']}: {p['confidence']:.2%}")
            
            # Check interpretation
            if 'interpretation' in result:
                interp = result['interpretation']
                logger.info(f"  Risk level: {interp['risk_level']}")
                logger.info(f"  Verdict: {interp['verdict']}")
                
                if 'main_factors' in interp:
                    logger.info("  Main factors:")
                    for factor in interp['main_factors']:
                        logger.info(f"    - {factor}")
            
            return True
        else:
            logger.error(f"✗ Prediction failed: {response.status_code}")
            logger.error(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Prediction error: {e}")
        return False

def test_system_info():
    """Test system info endpoint"""
    logger.info("\nTesting system info...")
    
    try:
        response = requests.get(f"{API_URL}/system_info")
        if response.status_code == 200:
            data = response.json()
            
            logger.info("✓ System info retrieved")
            
            # Check models
            if 'models' in data:
                logger.info("  Models:")
                for model_name, info in data['models'].items():
                    features = info.get('expected_features', '?')
                    needs_alignment = info.get('needs_alignment', False)
                    status = "needs alignment" if needs_alignment else "OK"
                    logger.info(f"    - {model_name}: {features} features ({status})")
            
            # Check feature alignment
            if 'feature_alignment' in data:
                logger.info(f"  Feature alignment needed: {data['feature_alignment']}")
            
            return True
        else:
            logger.error(f"✗ System info failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ System info error: {e}")
        return False

def run_all_tests():
    """Run all integration tests"""
    logger.info("="*60)
    logger.info("FLASH System Integration Tests")
    logger.info("="*60)
    
    # Check if API is running
    logger.info("\nNote: Make sure API server is running:")
    logger.info("  python api_server.py")
    logger.info("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    # Run tests
    results = {
        'health_check': test_health_check(),
        'pattern_list': test_pattern_list(),
        'prediction': test_prediction(),
        'system_info': test_system_info()
    }
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Test Summary")
    logger.info("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 All tests passed! System is fully integrated!")
    else:
        logger.warning(f"\n⚠️  {total - passed} tests failed. Check the logs above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)