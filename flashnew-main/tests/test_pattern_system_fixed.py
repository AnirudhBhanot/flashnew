#!/usr/bin/env python3
"""
Test the pattern system with the newly trained 45-feature models
"""

import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API endpoint
BASE_URL = "http://localhost:8001"

# Test data - all 45 features
test_startup = {
    # Capital features (12)
    "funding_stage": "series_a",
    "total_capital_raised_usd": 15000000,
    "cash_on_hand_usd": 10000000,
    "monthly_burn_usd": 400000,
    "runway_months": 25,
    "annual_revenue_run_rate": 3000000,
    "revenue_growth_rate_percent": 150,
    "gross_margin_percent": 75,
    "burn_multiple": 1.6,
    "ltv_cac_ratio": 3.5,
    "investor_tier_primary": "tier_1",
    "has_debt": False,
    
    # Advantage features (11)
    "patent_count": 3,
    "network_effects_present": True,
    "has_data_moat": True,
    "regulatory_advantage_present": False,
    "tech_differentiation_score": 4.2,
    "switching_cost_score": 3.8,
    "brand_strength_score": 3.5,
    "scalability_score": 4.5,
    "product_stage": "growth",
    "product_retention_30d": 0.75,
    "product_retention_90d": 0.65,
    
    # Market features (12)
    "sector": "SaaS",
    "tam_size_usd": 10000000000,
    "sam_size_usd": 1000000000,
    "som_size_usd": 100000000,
    "market_growth_rate_percent": 35,
    "customer_count": 500,
    "customer_concentration_percent": 15,
    "user_growth_rate_percent": 120,
    "net_dollar_retention_percent": 125,
    "competition_intensity": 3,
    "competitors_named_count": 5,
    "dau_mau_ratio": 0.4,
    
    # People features (10)
    "founders_count": 3,
    "team_size_full_time": 45,
    "years_experience_avg": 12,
    "domain_expertise_years_avg": 8,
    "prior_startup_experience_count": 2,
    "prior_successful_exits_count": 1,
    "board_advisor_experience_score": 4.0,
    "advisors_count": 5,
    "team_diversity_percent": 40,
    "key_person_dependency": False
}


def test_health():
    """Test API health endpoint"""
    logger.info("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✅ Health check passed")
        logger.info(f"  Pattern support: {data.get('pattern_support', False)}")
        logger.info(f"  Pattern models loaded: {data.get('pattern_models_loaded', 0)}")
        logger.info(f"  Base models loaded: {data.get('base_models_loaded', 0)}")
        return True
    else:
        logger.error(f"❌ Health check failed: {response.status_code}")
        return False


def test_patterns_list():
    """Test patterns listing endpoint"""
    logger.info("\nTesting patterns list endpoint...")
    response = requests.get(f"{BASE_URL}/patterns")
    
    if response.status_code == 200:
        data = response.json()
        patterns = data.get('patterns', {})
        logger.info(f"✅ Found {len(patterns)} patterns")
        
        # Show first few patterns
        for name, info in list(patterns.items())[:3]:
            logger.info(f"  - {name}: {info.get('description', 'No description')}")
        
        return True
    else:
        logger.error(f"❌ Patterns list failed: {response.status_code}")
        logger.error(f"  Response: {response.text}")
        return False


def test_standard_prediction():
    """Test standard prediction endpoint"""
    logger.info("\nTesting standard prediction endpoint...")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=test_startup,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✅ Standard prediction successful")
        logger.info(f"  Success probability: {data['success_probability']:.2%}")
        logger.info(f"  Risk level: {data['risk_level']}")
        logger.info(f"  Verdict: {data['verdict']}")
        
        # Show pillar scores
        pillar_scores = data.get('pillar_scores', {})
        if pillar_scores:
            logger.info("  Pillar scores:")
            for pillar, score in pillar_scores.items():
                logger.info(f"    - {pillar}: {score:.2f}")
        
        return True
    else:
        logger.error(f"❌ Standard prediction failed: {response.status_code}")
        logger.error(f"  Response: {response.text}")
        return False


def test_enhanced_prediction():
    """Test enhanced prediction with pattern analysis"""
    logger.info("\nTesting enhanced prediction endpoint...")
    
    response = requests.post(
        f"{BASE_URL}/predict_enhanced",
        json=test_startup,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"✅ Enhanced prediction successful")
        logger.info(f"  Success probability: {data['success_probability']:.2%}")
        
        # Show pattern analysis
        pattern_analysis = data.get('pattern_analysis')
        if pattern_analysis:
            primary = pattern_analysis.get('primary_pattern', {})
            logger.info(f"\n  Primary pattern: {primary.get('name', 'Unknown')}")
            logger.info(f"  Pattern confidence: {primary.get('confidence', 0):.2%}")
            logger.info(f"  Expected success rate: {primary.get('expected_success_rate', 0):.2%}")
            
            # Similar companies
            similar = primary.get('similar_companies', [])
            if similar:
                logger.info(f"  Similar companies: {', '.join(similar[:3])}")
            
            # Pattern mixture
            mixture = pattern_analysis.get('pattern_mixture', {})
            if mixture:
                logger.info("\n  Pattern mixture:")
                for pattern, weight in sorted(mixture.items(), key=lambda x: x[1], reverse=True)[:3]:
                    logger.info(f"    - {pattern}: {weight:.2%}")
            
            # Tags
            tags = pattern_analysis.get('tags', [])
            if tags:
                logger.info(f"\n  Tags: {', '.join(tags)}")
        
        return True
    else:
        logger.error(f"❌ Enhanced prediction failed: {response.status_code}")
        logger.error(f"  Response: {response.text}")
        return False


def test_pattern_analysis():
    """Test pattern analysis endpoint"""
    logger.info("\nTesting pattern analysis endpoint...")
    
    response = requests.post(
        f"{BASE_URL}/analyze_pattern",
        json={"metrics": test_startup},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        matches = data.get('pattern_matches', [])
        logger.info(f"✅ Pattern analysis successful")
        logger.info(f"  Found {len(matches)} pattern matches")
        
        # Show top matches
        for match in matches[:3]:
            logger.info(f"\n  Pattern: {match['pattern_name']}")
            logger.info(f"  Confidence: {match['confidence']:.2%}")
            logger.info(f"  Match type: {match['match_type']}")
        
        return True
    else:
        logger.error(f"❌ Pattern analysis failed: {response.status_code}")
        logger.error(f"  Response: {response.text}")
        return False


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Testing FLASH Pattern System with 45-feature models")
    logger.info("=" * 60)
    
    # Check if API is running
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            logger.error("API server is not running. Please start it with:")
            logger.error("cd /Users/sf/Desktop/FLASH && python3 api_server_v2.py")
            return
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to API server at http://localhost:8001")
        logger.error("Please start the server with:")
        logger.error("cd /Users/sf/Desktop/FLASH && python3 api_server_v2.py")
        return
    
    # Run tests
    tests = [
        test_health,
        test_patterns_list,
        test_standard_prediction,
        test_enhanced_prediction,
        test_pattern_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            logger.error(f"Error in {test.__name__}: {e}")
            results.append((test.__name__, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 All tests passed! Pattern system is working correctly.")
    else:
        logger.info("\n⚠️  Some tests failed. Check the logs above for details.")


if __name__ == "__main__":
    main()