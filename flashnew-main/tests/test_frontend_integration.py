#!/usr/bin/env python3
"""
Test Frontend-Backend Integration
Verifies that the API returns all fields expected by the frontend
"""

import requests
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API configuration
API_URL = "http://localhost:8001"

# Sample startup data as frontend would send it
FRONTEND_DATA = {
    "startup_name": "TechCo AI",
    "hq_location": "San Francisco",
    "vertical": "B2B SaaS",
    "founding_year": 2021,
    "founder_experience_years": 10,
    "team_size": 15,
    "total_funding": 5000000,
    "num_funding_rounds": 2,
    "investor_tier_primary": "tier_2",
    "technology_score": 4,
    "market_readiness_score": 4,
    "regulatory_advantage_present": True,  # Boolean from frontend
    "has_patents": True,
    "patent_count": 3,
    "burn_rate": 200000,
    "runway_months": 25,
    "revenue_growth_rate": 2.5,
    "customer_retention_rate": 0.85,
    "tam_size": 50000000000,
    "sam_percentage": 15,
    "market_share": 0.5,
    "time_to_market": 6,
    "market_growth_rate": 25,
    "competition_score": 3,
    "founder_education_tier": 3,
    "employees_from_top_companies": 0.4,
    "technical_team_percentage": 0.6,
    "advisory_board_score": 4,
    "key_person_dependency": False,  # Boolean from frontend
    "funding_stage": "series_a",
    "location_quality": 3,
    "has_lead_investor": True,
    "has_notable_investors": True,
    "investor_concentration": 0.3,
    "burn_multiple": 2.0,
    "product_launch_months": 8,
    "product_market_fit_score": 4,
    "revenue_model_score": 4,
    "unit_economics_score": 3,
    "scalability_score": 4,
    "r_and_d_intensity": 0.25,
    "network_effects_present": True,
    "viral_coefficient": 1.2,
    "customer_acquisition_cost": 500,
    "ltv_cac_ratio": 3.5,
    "has_data_moat": True,
    "has_debt": False,
    "debt_to_equity": 0.0
}


def check_required_fields(response: dict) -> list:
    """Check if response has all fields required by frontend"""
    required_fields = [
        # Core fields
        'success_probability',
        'confidence_score',
        'verdict',
        'strength_level',
        'risk_level',
        
        # Confidence interval
        'confidence_interval',
        'confidence_interval.lower',
        'confidence_interval.upper',
        
        # Pillar scores
        'pillar_scores',
        'pillar_scores.capital',
        'pillar_scores.advantage',
        'pillar_scores.market',
        'pillar_scores.people',
        'below_threshold',
        
        # Insights and factors
        'key_insights',
        'critical_failures',
        'success_factors',
        'risk_factors',
        'growth_indicators',
        
        # Pattern analysis
        'pattern_analysis',
        'pattern_insights',
        
        # Model information
        'model_predictions',
        'model_consensus',
        'modelConfidence',
        
        # Temporal predictions
        'temporal_predictions',
        'temporal_predictions.short_term',
        'temporal_predictions.medium_term',
        'temporal_predictions.long_term',
        
        # DNA pattern
        'dna_pattern',
        'dna_pattern.pattern_type',
        
        # Metadata
        'processing_time_ms',
        'timestamp',
        'model_version'
    ]
    
    missing = []
    for field in required_fields:
        if '.' in field:
            # Check nested fields
            parts = field.split('.')
            obj = response
            for part in parts:
                if isinstance(obj, dict) and part in obj:
                    obj = obj[part]
                else:
                    missing.append(field)
                    break
        else:
            if field not in response:
                missing.append(field)
    
    return missing


def test_predict_simple():
    """Test the predict_simple endpoint"""
    logger.info("\n" + "="*60)
    logger.info("Testing /predict_simple endpoint")
    logger.info("="*60)
    
    try:
        response = requests.post(
            f"{API_URL}/predict_simple",
            json=FRONTEND_DATA,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            missing = check_required_fields(data)
            
            if not missing:
                logger.info("✅ All required fields present!")
            else:
                logger.warning(f"❌ Missing {len(missing)} fields:")
                for field in missing:
                    logger.warning(f"   - {field}")
            
            # Display key results
            logger.info("\nKey Results:")
            logger.info(f"  Success Probability: {data.get('success_probability', 0):.1%}")
            logger.info(f"  Verdict: {data.get('verdict', 'N/A')}")
            logger.info(f"  Strength: {data.get('strength_level', 'N/A')}")
            logger.info(f"  Risk Level: {data.get('risk_level', 'N/A')}")
            
            # Check pillar scores
            if 'pillar_scores' in data:
                logger.info("\nPillar Scores:")
                for pillar, score in data['pillar_scores'].items():
                    logger.info(f"  {pillar.capitalize()}: {score:.1%}")
            
            # Check insights
            if 'key_insights' in data:
                logger.info(f"\nKey Insights: {len(data['key_insights'])}")
                for insight in data['key_insights'][:3]:
                    logger.info(f"  • {insight}")
            
            return True
            
        else:
            logger.error(f"❌ Request failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def test_predict_advanced():
    """Test the predict_advanced endpoint"""
    logger.info("\n" + "="*60)
    logger.info("Testing /predict_advanced endpoint")
    logger.info("="*60)
    
    try:
        response = requests.post(
            f"{API_URL}/predict_advanced",
            json=FRONTEND_DATA,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for advanced analysis flag
            if data.get('advanced_analysis'):
                logger.info("✅ Advanced analysis flag present")
            
            # Check pattern analysis
            if 'pattern_analysis' in data and data['pattern_analysis']:
                logger.info("\n✅ Pattern Analysis:")
                pattern = data['pattern_analysis'].get('primary_pattern', {})
                logger.info(f"  Pattern: {pattern.get('name', 'N/A')}")
                logger.info(f"  Confidence: {pattern.get('confidence', 0):.1%}")
                logger.info(f"  Expected Success: {pattern.get('expected_success_rate', 0):.1%}")
            
            return True
            
        else:
            logger.error(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def test_data_transformations():
    """Test that data transformations work correctly"""
    logger.info("\n" + "="*60)
    logger.info("Testing Data Transformations")
    logger.info("="*60)
    
    # Test with various boolean values
    test_cases = [
        ("Boolean true", {"has_patents": True}),
        ("Boolean false", {"has_patents": False}),
        ("String 'true'", {"has_patents": "true"}),
        ("String 'false'", {"has_patents": "false"}),
        ("Number 1", {"has_patents": 1}),
        ("Number 0", {"has_patents": 0}),
    ]
    
    all_passed = True
    
    for name, test_field in test_cases:
        test_data = FRONTEND_DATA.copy()
        test_data.update(test_field)
        
        try:
            response = requests.post(
                f"{API_URL}/predict_simple",
                json=test_data,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {name}: Processed successfully")
            else:
                logger.error(f"❌ {name}: Failed with {response.status_code}")
                all_passed = False
                
        except Exception as e:
            logger.error(f"❌ {name}: Error - {e}")
            all_passed = False
    
    return all_passed


def main():
    """Run all frontend integration tests"""
    logger.info("FLASH Frontend-Backend Integration Test")
    logger.info("Testing that API returns all fields expected by frontend")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code != 200:
            logger.error("❌ API is not healthy!")
            return 1
    except:
        logger.error("❌ API is not running!")
        logger.error("Start the API with: python3 api_server_clean.py")
        return 1
    
    # Run tests
    results = []
    results.append(("Simple Prediction", test_predict_simple()))
    results.append(("Advanced Prediction", test_predict_advanced()))
    results.append(("Data Transformations", test_data_transformations()))
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Test Summary:")
    logger.info("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n✅ Frontend-Backend integration is working correctly!")
        return 0
    else:
        logger.error(f"\n❌ {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    exit(main())