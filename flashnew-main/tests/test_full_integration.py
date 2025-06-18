#!/usr/bin/env python3
"""
Comprehensive Integration Test for FLASH API
Tests all endpoints, type conversions, and response formats
"""

import requests
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8001"

# Sample data with mixed types (as frontend would send)
FRONTEND_DATA = {
    # Capital features - with boolean as boolean
    'funding_stage': 'series_a',
    'total_capital_raised_usd': 5000000,
    'cash_on_hand_usd': 3000000,
    'monthly_burn_usd': 200000,
    'runway_months': None,  # Optional field
    'annual_revenue_run_rate': 3000000,
    'revenue_growth_rate_percent': 150,
    'gross_margin_percent': 80,
    'burn_multiple': None,  # Optional field
    'ltv_cac_ratio': 3.5,
    'investor_tier_primary': 'tier_2',
    'has_debt': False,  # Boolean from frontend
    
    # Advantage features
    'patent_count': 2,
    'network_effects_present': False,  # Boolean
    'has_data_moat': True,  # Boolean
    'regulatory_advantage_present': False,  # Boolean
    'tech_differentiation_score': 4,
    'switching_cost_score': 3,
    'brand_strength_score': 3,
    'scalability_score': 4,
    'product_stage': 'growth',
    'product_retention_30d': 0.75,
    'product_retention_90d': 0.65,
    
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
    'dau_mau_ratio': 0.4,
    
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
    'key_person_dependency': False,  # Boolean
    
    # Extra frontend fields (should be removed)
    'team_cohesion_score': 4,
    'hiring_velocity_score': 3,
    'diversity_score': 4,
    'technical_expertise_score': 5
}


def test_health_check():
    """Test health endpoint"""
    logger.info("\n1. Testing Health Check...")
    
    try:
        response = requests.get(f"{API_URL}/health")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data['status'] in ['healthy', 'degraded']
        assert 'version' in data
        assert 'features' in data
        
        logger.info("✅ Health check passed")
        logger.info(f"   Status: {data['status']}")
        logger.info(f"   Version: {data['version']}")
        logger.info(f"   Features: {data['features']}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False


def test_prediction_endpoints():
    """Test all prediction endpoints"""
    logger.info("\n2. Testing Prediction Endpoints...")
    
    endpoints = ['/predict', '/predict_simple', '/predict_advanced', '/predict_enhanced']
    results = {}
    
    for endpoint in endpoints:
        logger.info(f"\n   Testing {endpoint}...")
        
        try:
            response = requests.post(f"{API_URL}{endpoint}", json=FRONTEND_DATA)
            
            if response.status_code != 200:
                logger.error(f"   ❌ {endpoint}: Status {response.status_code}")
                logger.error(f"      Response: {response.text}")
                results[endpoint] = False
                continue
            
            data = response.json()
            
            # Check required fields for frontend
            required_fields = [
                'success_probability',
                'confidence_interval',
                'risk_level',
                'key_insights',
                'pillar_scores',
                'recommendation',
                'timestamp',
                'verdict',
                'strength',
                'weighted_score',
                'critical_failures',
                'below_threshold',
                'stage_thresholds'
            ]
            
            missing_fields = [f for f in required_fields if f not in data]
            if missing_fields:
                logger.error(f"   ❌ {endpoint}: Missing fields: {missing_fields}")
                results[endpoint] = False
                continue
            
            # Validate field types and structure
            assert isinstance(data['success_probability'], (int, float))
            assert isinstance(data['confidence_interval'], dict)
            assert 'lower' in data['confidence_interval']
            assert 'upper' in data['confidence_interval']
            assert isinstance(data['pillar_scores'], dict)
            assert all(p in data['pillar_scores'] for p in ['capital', 'advantage', 'market', 'people'])
            assert data['verdict'] in ['PASS', 'FAIL', 'CONDITIONAL PASS']
            assert data['strength'] in ['STRONG', 'MODERATE', 'WEAK', 'CRITICAL']
            
            logger.info(f"   ✅ {endpoint}: All checks passed")
            logger.info(f"      Success probability: {data['success_probability']:.3f}")
            logger.info(f"      Verdict: {data['verdict']} ({data['strength']})")
            logger.info(f"      Risk level: {data['risk_level']}")
            
            results[endpoint] = True
            
        except Exception as e:
            logger.error(f"   ❌ {endpoint}: {e}")
            results[endpoint] = False
    
    return all(results.values())


def test_investor_profiles():
    """Test investor profiles endpoint"""
    logger.info("\n3. Testing Investor Profiles...")
    
    try:
        response = requests.get(f"{API_URL}/investor_profiles")
        assert response.status_code == 200
        
        data = response.json()
        assert 'profiles' in data
        assert len(data['profiles']) > 0
        assert 'default_profile' in data
        
        # Check profile structure
        for profile in data['profiles']:
            assert 'id' in profile
            assert 'name' in profile
            assert 'risk_tolerance' in profile
            assert 'preferred_metrics' in profile
            
        logger.info("✅ Investor profiles passed")
        logger.info(f"   Found {len(data['profiles'])} profiles")
        logger.info(f"   Default: {data['default_profile']}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Investor profiles failed: {e}")
        return False


def test_pattern_endpoints():
    """Test pattern-related endpoints"""
    logger.info("\n4. Testing Pattern Endpoints...")
    
    # Test pattern listing
    try:
        response = requests.get(f"{API_URL}/patterns")
        assert response.status_code == 200
        
        data = response.json()
        assert 'patterns' in data
        assert 'total' in data
        
        logger.info(f"✅ Pattern listing: {data['total']} patterns found")
        
        # Test pattern details if patterns exist
        if data['patterns'] and len(data['patterns']) > 0:
            pattern_name = data['patterns'][0]['name']
            response = requests.get(f"{API_URL}/patterns/{pattern_name}")
            assert response.status_code == 200
            logger.info(f"✅ Pattern details: Retrieved {pattern_name}")
        
        # Test pattern analysis
        response = requests.post(f"{API_URL}/analyze_pattern", json=FRONTEND_DATA)
        assert response.status_code == 200
        logger.info("✅ Pattern analysis: Success")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Pattern endpoints failed: {e}")
        return False


def test_type_conversion():
    """Test that type conversion is working"""
    logger.info("\n5. Testing Type Conversion...")
    
    # Create data with edge cases
    test_data = FRONTEND_DATA.copy()
    test_data['has_debt'] = True  # Boolean true
    test_data['network_effects_present'] = "true"  # String boolean
    test_data['runway_months'] = None  # Missing optional
    test_data['annual_revenue_run_rate'] = "5000000"  # String number
    
    try:
        response = requests.post(f"{API_URL}/predict", json=test_data)
        
        if response.status_code == 200:
            logger.info("✅ Type conversion: Handled all edge cases")
            return True
        else:
            logger.error(f"❌ Type conversion failed: {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Type conversion error: {e}")
        return False


def test_system_info():
    """Test system info endpoint"""
    logger.info("\n6. Testing System Info...")
    
    try:
        response = requests.get(f"{API_URL}/system_info")
        assert response.status_code == 200
        
        data = response.json()
        logger.info("✅ System info retrieved")
        logger.info(f"   API Version: {data.get('api_version')}")
        logger.info(f"   Feature Count: {data.get('feature_count')}")
        logger.info(f"   Available Endpoints: {len(data.get('endpoints', []))}")
        return True
        
    except Exception as e:
        logger.error(f"❌ System info failed: {e}")
        return False


def test_error_handling():
    """Test error handling"""
    logger.info("\n7. Testing Error Handling...")
    
    # Test with invalid data
    invalid_data = {'invalid': 'data'}
    
    try:
        response = requests.post(f"{API_URL}/predict", json=invalid_data)
        assert response.status_code in [400, 422]
        assert 'error' in response.json()
        logger.info("✅ Error handling: Invalid data rejected properly")
        
        # Test rate limiting (if we exceed limits)
        # This is commented out to avoid actually hitting rate limits
        # for i in range(60):
        #     requests.post(f"{API_URL}/predict", json=FRONTEND_DATA)
        # response = requests.post(f"{API_URL}/predict", json=FRONTEND_DATA)
        # assert response.status_code == 429
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error handling test failed: {e}")
        return False


def run_all_tests():
    """Run all integration tests"""
    logger.info("="*60)
    logger.info("FLASH Full Integration Test Suite")
    logger.info("="*60)
    logger.info(f"Testing API at: {API_URL}")
    logger.info(f"Start time: {datetime.now()}")
    
    # Wait for server to be ready
    logger.info("\nWaiting for server to start...")
    time.sleep(2)
    
    # Run tests
    test_results = {
        'health_check': test_health_check(),
        'prediction_endpoints': test_prediction_endpoints(),
        'investor_profiles': test_investor_profiles(),
        'pattern_endpoints': test_pattern_endpoints(),
        'type_conversion': test_type_conversion(),
        'system_info': test_system_info(),
        'error_handling': test_error_handling()
    }
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Test Summary")
    logger.info("="*60)
    
    passed = sum(1 for v in test_results.values() if v)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 All tests passed! Integration is complete!")
        logger.info("\nThe API is ready for frontend integration with:")
        logger.info("- Type conversion working")
        logger.info("- All endpoints available")
        logger.info("- Response format matching frontend expectations")
    else:
        logger.warning(f"\n⚠️  {total - passed} tests failed. Check logs above.")
    
    return passed == total


if __name__ == "__main__":
    # Note: Make sure to start the integrated server first:
    # python api_server_integrated.py
    
    success = run_all_tests()
    exit(0 if success else 1)