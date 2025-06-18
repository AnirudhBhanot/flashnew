#!/usr/bin/env python3
"""
Test script to verify pillar model fix works end-to-end
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import logging
from models.unified_orchestrator_v3 import get_orchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_orchestrator_pillar_scores():
    """Test that the orchestrator properly returns pillar scores"""
    
    logger.info("Testing orchestrator with pillar scores...")
    
    # Initialize orchestrator
    orchestrator = get_orchestrator()
    
    # Test data
    test_features = {
        # Capital features
        'funding_stage': 'series_a',
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 2000000,
        'monthly_burn_usd': 150000,
        'runway_months': 13,
        'annual_revenue_run_rate': 2400000,
        'revenue_growth_rate_percent': 150,
        'gross_margin_percent': 75,
        'burn_multiple': 1.2,
        'ltv_cac_ratio': 3.5,
        'investor_tier_primary': 'top_tier',
        'has_debt': False,
        
        # Advantage features
        'patent_count': 3,
        'network_effects_present': True,
        'has_data_moat': True,
        'regulatory_advantage_present': False,
        'tech_differentiation_score': 4.5,
        'switching_cost_score': 4,
        'brand_strength_score': 3.5,
        'scalability_score': 4.5,
        'product_stage': 'scaling',
        'product_retention_30d': 0.85,
        'product_retention_90d': 0.70,
        
        # Market features
        'sector': 'B2B SaaS',
        'tam_size_usd': 50000000000,
        'sam_size_usd': 5000000000,
        'som_size_usd': 500000000,
        'market_growth_rate_percent': 40,
        'customer_count': 500,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 120,
        'net_dollar_retention_percent': 125,
        'competition_intensity': 3,
        'competitors_named_count': 8,
        'dau_mau_ratio': 0.6,
        
        # People features
        'founders_count': 3,
        'team_size_full_time': 45,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 10,
        'prior_startup_experience_count': 3,
        'prior_successful_exits_count': 2,
        'board_advisor_experience_score': 4.5,
        'advisors_count': 5,
        'team_diversity_percent': 45,
        'key_person_dependency': False
    }
    
    # Get enhanced prediction
    result = orchestrator.predict_enhanced(test_features)
    
    # Check results
    logger.info("\n" + "="*60)
    logger.info("PREDICTION RESULTS")
    logger.info("="*60)
    
    logger.info(f"Success Probability: {result['success_probability']:.1%}")
    logger.info(f"Confidence Score: {result['confidence_score']:.1%}")
    
    # Check if pillar scores are included
    if 'pillar_scores' in result:
        logger.info("\nPILLAR SCORES:")
        for pillar, score in result['pillar_scores'].items():
            logger.info(f"  {pillar.upper()}: {score:.1%}")
    else:
        logger.error("ERROR: No pillar_scores in result!")
        
    # Show components
    logger.info("\nPREDICTION COMPONENTS:")
    for component, score in result['prediction_components'].items():
        logger.info(f"  {component}: {score:.1%}")
    
    # Pattern analysis
    if result.get('pattern_analysis'):
        logger.info("\nPATTERN ANALYSIS:")
        patterns = result['pattern_analysis'].get('primary_patterns', [])
        for pattern in patterns[:3]:
            logger.info(f"  - {pattern['pattern']} ({pattern['confidence']:.0%})")
    
    logger.info("\n" + "="*60)
    
    return result


if __name__ == "__main__":
    test_orchestrator_pillar_scores()