#!/usr/bin/env python3
"""
Test Suite for Unified FLASH System
Validates that all models work with 45 canonical features
No wrappers, no conversions - clean architecture
"""

import requests
import json
import time
import numpy as np
from pathlib import Path
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Test configuration
API_URL = "http://localhost:8001"

# Canonical test startup with all 45 features
TEST_STARTUP = {
    # Capital (7)
    "founding_year": 2021,
    "total_funding": 5000000,
    "num_funding_rounds": 2,
    "investor_tier_primary": "tier_2",
    "burn_rate": 200000,
    "runway_months": 15,
    "funding_stage": "series_a",
    
    # Advantage (8)
    "technology_score": 4,
    "has_patents": True,
    "patent_count": 3,
    "regulatory_advantage_present": True,
    "network_effects_present": True,
    "has_data_moat": True,
    "scalability_score": 4,
    "r_and_d_intensity": 0.25,
    
    # Market (11)
    "tam_size": 50000000000,
    "sam_percentage": 15,
    "market_share": 0.5,
    "market_growth_rate": 25,
    "competition_score": 3,
    "market_readiness_score": 4,
    "time_to_market": 6,
    "customer_acquisition_cost": 500,
    "ltv_cac_ratio": 3.5,
    "viral_coefficient": 1.2,
    "revenue_growth_rate": 2.5,
    
    # People (10)
    "founder_experience_years": 10,
    "team_size": 15,
    "technical_team_percentage": 0.6,
    "founder_education_tier": 3,
    "employees_from_top_companies": 0.4,
    "advisory_board_score": 4,
    "key_person_dependency": False,
    "location_quality": 3,
    "has_lead_investor": True,
    "has_notable_investors": True,
    
    # Product (9)
    "product_launch_months": 8,
    "product_market_fit_score": 4,
    "revenue_model_score": 4,
    "unit_economics_score": 3,
    "customer_retention_rate": 0.85,
    "burn_multiple": 2.0,
    "investor_concentration": 0.3,
    "has_debt": False,
    "debt_to_equity": 0.0
}


def test_api_health():
    """Test API health check"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        data = response.json()
        
        logger.info("✓ Health Check:")
        logger.info(f"  Status: {data['status']}")
        logger.info(f"  Models: {', '.join(data['models_loaded'])}")
        logger.info(f"  Pipeline: {'loaded' if data['pipeline_loaded'] else 'missing'}")
        logger.info(f"  Features: {data['n_features']}")
        
        return data['status'] == 'healthy'
    except Exception as e:
        logger.error(f"✗ Health check failed: {e}")
        return False


def test_feature_validation():
    """Validate all 45 features are recognized"""
    try:
        response = requests.get(f"{API_URL}/features", timeout=5)
        data = response.json()
        
        logger.info("\n✓ Feature Validation:")
        logger.info(f"  Total features: {data['total_features']}")
        logger.info(f"  Categories: {data['categories']}")
        
        # Verify count
        category_sum = sum(data['categories'].values())
        assert category_sum == 45, f"Feature count mismatch: {category_sum} != 45"
        
        logger.info("  All 45 canonical features validated!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Feature validation failed: {e}")
        return False


def test_prediction():
    """Test prediction with canonical features"""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=TEST_STARTUP,
            timeout=5
        )
        
        if response.status_code != 200:
            logger.error(f"✗ Prediction failed: {response.status_code}")
            logger.error(f"  Response: {response.text}")
            return False
            
        data = response.json()
        
        logger.info("\n✓ Prediction Results:")
        logger.info(f"  Success probability: {data['success_probability']:.2%}")
        logger.info(f"  Confidence: {data['confidence_score']:.2%}")
        logger.info(f"  Model agreement: {data['model_agreement']:.2%}")
        logger.info(f"  Processing time: {data['processing_time_ms']}ms")
        
        # Check model predictions
        logger.info("\n  Model Predictions:")
        for model, score in data['model_predictions'].items():
            logger.info(f"    {model}: {score:.4f}")
            
        # Verify all models ran
        expected_models = ['dna_analyzer', 'temporal_model', 'industry_model']
        for model in expected_models:
            assert model in data['model_predictions'], f"Missing {model} prediction"
            
        # Check interpretation
        logger.info(f"\n  Assessment: {data['interpretation']['assessment']}")
        logger.info(f"  Strongest: {data['interpretation']['strongest_signal']['model']} "
                   f"({data['interpretation']['strongest_signal']['score']:.4f})")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Prediction test failed: {e}")
        return False


def test_batch_prediction():
    """Test batch prediction endpoint"""
    try:
        # Create 3 test startups with variations
        startups = []
        for i in range(3):
            startup = TEST_STARTUP.copy()
            startup['team_size'] = 10 + i * 5
            startup['total_funding'] = 1000000 * (i + 1)
            startups.append(startup)
            
        response = requests.post(
            f"{API_URL}/batch_predict",
            json=startups,
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"✗ Batch prediction failed: {response.status_code}")
            return False
            
        data = response.json()
        
        logger.info("\n✓ Batch Prediction:")
        logger.info(f"  Processed: {data['count']} startups")
        
        for i, pred in enumerate(data['predictions']):
            logger.info(f"  Startup {i+1}: {pred['success_probability']:.2%}")
            
        return True
        
    except Exception as e:
        logger.error(f"✗ Batch prediction failed: {e}")
        return False


def test_feature_importance():
    """Test feature importance endpoint"""
    try:
        response = requests.get(f"{API_URL}/feature_importance", timeout=5)
        data = response.json()
        
        logger.info("\n✓ Feature Importance:")
        logger.info("  Top 10 most important features:")
        
        for i, (feature, importance) in enumerate(data['top_10_features'].items(), 1):
            logger.info(f"    {i}. {feature}: {importance:.4f}")
            
        return True
        
    except Exception as e:
        logger.error(f"✗ Feature importance failed: {e}")
        return False


def test_performance():
    """Test API performance"""
    try:
        logger.info("\n✓ Performance Test:")
        
        times = []
        for i in range(10):
            start = time.time()
            response = requests.post(
                f"{API_URL}/predict",
                json=TEST_STARTUP,
                timeout=5
            )
            end = time.time()
            
            if response.status_code == 200:
                times.append((end - start) * 1000)
            
        avg_time = np.mean(times)
        std_time = np.std(times)
        
        logger.info(f"  Average response: {avg_time:.0f}ms (±{std_time:.0f}ms)")
        logger.info(f"  Min: {min(times):.0f}ms, Max: {max(times):.0f}ms")
        
        # Performance should be better without wrappers
        assert avg_time < 200, f"Performance degraded: {avg_time}ms average"
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Performance test failed: {e}")
        return False


def test_no_wrappers():
    """Verify no wrappers exist in the system"""
    wrapper_files = [
        "fix_pillar_models.py",
        "stage_model_features.py", 
        "models/feature_wrapper.py",
        "type_converter.py",
        "fix_orchestrator_features.py"
    ]
    
    logger.info("\n✓ Wrapper Removal Verification:")
    all_removed = True
    
    for wrapper in wrapper_files:
        if Path(wrapper).exists():
            logger.error(f"  ✗ Wrapper still exists: {wrapper}")
            all_removed = False
        else:
            logger.info(f"  ✓ Removed: {wrapper}")
            
    return all_removed


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("FLASH Unified System Test Suite")
    logger.info("Testing clean architecture with 45 canonical features")
    logger.info("=" * 60)
    
    # Check if API is running
    try:
        requests.get(f"{API_URL}/", timeout=2)
    except:
        logger.error("\n❌ API server is not running!")
        logger.error("Start the clean API server with: python3 api_server_clean.py")
        return 1
    
    # Run tests
    tests = [
        ("Wrapper Removal", test_no_wrappers),
        ("API Health", test_api_health),
        ("Feature Validation", test_feature_validation),
        ("Single Prediction", test_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Feature Importance", test_feature_importance),
        ("Performance", test_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name}...")
        passed = test_func()
        results.append((test_name, passed))
        
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary:")
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"  {status}: {test_name}")
        
    logger.info(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        logger.info("\n✅ All tests passed!")
        logger.info("Clean architecture working perfectly!")
        logger.info("No wrappers, no conversions - just direct model calls!")
        return 0
    else:
        logger.error(f"\n❌ {total_count - passed_count} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())