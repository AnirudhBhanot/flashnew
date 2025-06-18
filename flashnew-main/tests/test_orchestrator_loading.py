#!/usr/bin/env python3
"""Test script to verify orchestrator loads correctly"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_orchestrator_loading():
    """Test that the orchestrator loads all models correctly"""
    try:
        # Import orchestrator
        from models.unified_orchestrator_v3 import UnifiedOrchestratorV3
        
        logger.info("Initializing orchestrator...")
        orchestrator = UnifiedOrchestratorV3()
        
        # Check loaded models
        logger.info(f"Loaded models: {list(orchestrator.models.keys())}")
        
        # Check pattern classifier
        if orchestrator.pattern_classifier:
            logger.info("Pattern classifier loaded successfully")
        else:
            logger.warning("Pattern classifier not loaded")
            
        # Check pillar wrapper
        if orchestrator.pillar_wrapper:
            logger.info("Pillar wrapper loaded successfully")
        else:
            logger.warning("Pillar wrapper not loaded")
            
        # Test a prediction
        test_features = {
            'founding_year': 2021,
            'founder_experience_years': 10,
            'team_size': 15,
            'total_funding': 5000000,
            'num_funding_rounds': 2,
            'investor_tier_primary': 'tier_2',
            'technology_score': 4,
            'market_readiness_score': 4,
            'regulatory_advantage_present': 1,
            'has_patents': 1,
            'patent_count': 3,
            'burn_rate': 200000,
            'runway_months': 12,
            'revenue_growth_rate': 2.5,
            'customer_retention_rate': 0.85,
            'tam_size': 50000000000,
            'sam_percentage': 15,
            'market_share': 0.5,
            'time_to_market': 6,
            'market_growth_rate': 25,
            'competition_score': 3,
            'founder_education_tier': 3,
            'employees_from_top_companies': 0.4,
            'technical_team_percentage': 0.6,
            'advisory_board_score': 4,
            'key_person_dependency': 0,
            'funding_stage': 'series_a',
            'location_quality': 3,
            'has_lead_investor': 1,
            'has_notable_investors': 1,
            'investor_concentration': 0.3,
            'burn_multiple': 2.0,
            'product_launch_months': 8,
            'product_market_fit_score': 4,
            'revenue_model_score': 4,
            'unit_economics_score': 3,
            'scalability_score': 4,
            'r_and_d_intensity': 0.25,
            'network_effects_present': 1,
            'viral_coefficient': 1.2,
            'customer_acquisition_cost': 500,
            'ltv_cac_ratio': 3.5,
            'has_data_moat': 1,
            'has_debt': 0,
            'debt_to_equity': 0.0
        }
        
        logger.info("Testing prediction...")
        result = orchestrator.predict_enhanced(test_features)
        
        logger.info(f"Success probability: {result['success_probability']:.2%}")
        logger.info(f"Confidence score: {result['confidence_score']:.2%}")
        logger.info(f"Model agreement: {result['model_agreement']:.2%}")
        logger.info(f"Processing time: {result['processing_time_ms']}ms")
        
        # Check pillar scores
        pillar_scores = result.get('pillar_scores', {})
        logger.info("Pillar scores:")
        for pillar, score in pillar_scores.items():
            logger.info(f"  {pillar.capitalize()}: {score:.2%}")
        
        logger.info("\nOrchestrator loaded and working correctly!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading orchestrator: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_orchestrator_loading()
    sys.exit(0 if success else 1)