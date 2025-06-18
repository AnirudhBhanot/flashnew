#!/usr/bin/env python3
"""
Test Complete System with Pattern Integration
Verifies all models are working together properly
"""

import json
import pandas as pd
import numpy as np
import logging
import sys
from pathlib import Path

# Add models directory to path
sys.path.append(str(Path(__file__).parent))

from models.unified_orchestrator_v3 import UnifiedOrchestratorV3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_startup(scenario="average"):
    """Create test startup data for different scenarios"""
    
    scenarios = {
        "high_potential": {
            # Strong metrics across the board
            'funding_stage': 'Series B',
            'total_capital_raised_usd': 50000000,
            'cash_on_hand_usd': 30000000,
            'monthly_burn_usd': 1000000,
            'runway_months': 30,
            'annual_revenue_run_rate': 20000000,
            'revenue_growth_rate_percent': 150,
            'gross_margin_percent': 75,
            'burn_multiple': 0.8,
            'ltv_cac_ratio': 4.5,
            'investor_tier_primary': 'Tier 1',
            'has_debt': 0,
            'patent_count': 5,
            'network_effects_present': 1,
            'has_data_moat': 1,
            'regulatory_advantage_present': 0,
            'tech_differentiation_score': 4,
            'switching_cost_score': 4,
            'brand_strength_score': 4,
            'scalability_score': 5,
            'product_stage': 'Launched',
            'product_retention_30d': 0.8,
            'product_retention_90d': 0.7,
            'sector': 'SaaS',
            'tam_size_usd': 10000000000,
            'sam_size_usd': 1000000000,
            'som_size_usd': 100000000,
            'market_growth_rate_percent': 30,
            'customer_count': 500,
            'customer_concentration_percent': 15,
            'user_growth_rate_percent': 100,
            'net_dollar_retention_percent': 120,
            'competition_intensity': 3,
            'competitors_named_count': 5,
            'dau_mau_ratio': 0.6,
            'founders_count': 3,
            'team_size_full_time': 50,
            'years_experience_avg': 15,
            'domain_expertise_years_avg': 10,
            'prior_startup_experience_count': 2,
            'prior_successful_exits_count': 1,
            'board_advisor_experience_score': 4,
            'advisors_count': 5,
            'team_diversity_percent': 40,
            'key_person_dependency': 0
        },
        "average": {
            # Average startup metrics
            'funding_stage': 'Series A',
            'total_capital_raised_usd': 10000000,
            'cash_on_hand_usd': 5000000,
            'monthly_burn_usd': 300000,
            'runway_months': 16,
            'annual_revenue_run_rate': 2000000,
            'revenue_growth_rate_percent': 50,
            'gross_margin_percent': 60,
            'burn_multiple': 2.5,
            'ltv_cac_ratio': 2,
            'investor_tier_primary': 'Tier 2',
            'has_debt': 0,
            'patent_count': 1,
            'network_effects_present': 0,
            'has_data_moat': 0,
            'regulatory_advantage_present': 0,
            'tech_differentiation_score': 3,
            'switching_cost_score': 3,
            'brand_strength_score': 3,
            'scalability_score': 3,
            'product_stage': 'Beta',
            'product_retention_30d': 0.5,
            'product_retention_90d': 0.4,
            'sector': 'FinTech',
            'tam_size_usd': 5000000000,
            'sam_size_usd': 500000000,
            'som_size_usd': 50000000,
            'market_growth_rate_percent': 20,
            'customer_count': 100,
            'customer_concentration_percent': 30,
            'user_growth_rate_percent': 40,
            'net_dollar_retention_percent': 100,
            'competition_intensity': 4,
            'competitors_named_count': 10,
            'dau_mau_ratio': 0.4,
            'founders_count': 2,
            'team_size_full_time': 15,
            'years_experience_avg': 10,
            'domain_expertise_years_avg': 5,
            'prior_startup_experience_count': 1,
            'prior_successful_exits_count': 0,
            'board_advisor_experience_score': 3,
            'advisors_count': 3,
            'team_diversity_percent': 30,
            'key_person_dependency': 1
        },
        "low_potential": {
            # Weak metrics
            'funding_stage': 'Seed',
            'total_capital_raised_usd': 500000,
            'cash_on_hand_usd': 200000,
            'monthly_burn_usd': 50000,
            'runway_months': 4,
            'annual_revenue_run_rate': 100000,
            'revenue_growth_rate_percent': 10,
            'gross_margin_percent': 30,
            'burn_multiple': 8,
            'ltv_cac_ratio': 0.8,
            'investor_tier_primary': 'Other',
            'has_debt': 1,
            'patent_count': 0,
            'network_effects_present': 0,
            'has_data_moat': 0,
            'regulatory_advantage_present': 0,
            'tech_differentiation_score': 2,
            'switching_cost_score': 2,
            'brand_strength_score': 2,
            'scalability_score': 2,
            'product_stage': 'Pre-Launch',
            'product_retention_30d': 0.2,
            'product_retention_90d': 0.1,
            'sector': 'Other',
            'tam_size_usd': 100000000,
            'sam_size_usd': 10000000,
            'som_size_usd': 1000000,
            'market_growth_rate_percent': 5,
            'customer_count': 10,
            'customer_concentration_percent': 80,
            'user_growth_rate_percent': 5,
            'net_dollar_retention_percent': 80,
            'competition_intensity': 5,
            'competitors_named_count': 20,
            'dau_mau_ratio': 0.1,
            'founders_count': 1,
            'team_size_full_time': 3,
            'years_experience_avg': 3,
            'domain_expertise_years_avg': 1,
            'prior_startup_experience_count': 0,
            'prior_successful_exits_count': 0,
            'board_advisor_experience_score': 1,
            'advisors_count': 0,
            'team_diversity_percent': 0,
            'key_person_dependency': 1
        }
    }
    
    return scenarios.get(scenario, scenarios["average"])


def test_orchestrator():
    """Test the complete system with pattern integration"""
    logger.info("="*80)
    logger.info("TESTING COMPLETE SYSTEM WITH PATTERN INTEGRATION")
    logger.info("="*80)
    
    # Initialize orchestrator
    logger.info("\nInitializing orchestrator...")
    try:
        orchestrator = UnifiedOrchestratorV3()
        model_info = orchestrator.get_model_info()
        
        logger.info(f"Models loaded: {model_info['models_loaded']}")
        logger.info(f"Pattern system enabled: {model_info['pattern_system']}")
        logger.info(f"Total models: {model_info['total_models']}")
        logger.info(f"Pattern ensemble AUC: {model_info['pattern_performance']['ensemble_auc']:.4f}")
        logger.info(f"Patterns count: {model_info['pattern_performance']['patterns_count']}")
        
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        return
    
    # Test different scenarios
    scenarios = ["high_potential", "average", "low_potential"]
    results = {}
    
    for scenario in scenarios:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing {scenario.upper()} startup scenario")
        logger.info("="*60)
        
        # Create test data
        startup_data = create_test_startup(scenario)
        df = pd.DataFrame([startup_data])
        
        # Get prediction
        try:
            result = orchestrator.predict(df)
            results[scenario] = result
            
            # Display results
            logger.info(f"\nPrediction Results:")
            logger.info(f"  Success Probability: {result['success_probability']:.2%}")
            logger.info(f"  Verdict: {result['verdict']} ({result['verdict_strength']})")
            logger.info(f"  Model Agreement: {result['model_agreement']:.2%}")
            
            logger.info(f"\nModel Predictions:")
            for model, pred in result['model_predictions'].items():
                logger.info(f"  {model}: {pred:.3f}")
            
            logger.info(f"\nWeights Used:")
            for component, weight in result['weights_used'].items():
                logger.info(f"  {component}: {weight:.0%}")
                
            if result.get('pattern_insights'):
                logger.info(f"\nPattern Insights:")
                for insight in result['pattern_insights']:
                    logger.info(f"  - {insight}")
                    
        except Exception as e:
            logger.error(f"Prediction failed for {scenario}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    logger.info("\n" + "="*80)
    logger.info("SYSTEM TEST SUMMARY")
    logger.info("="*80)
    
    if results:
        # Calculate performance metrics
        high_score = results.get('high_potential', {}).get('success_probability', 0)
        avg_score = results.get('average', {}).get('success_probability', 0)
        low_score = results.get('low_potential', {}).get('success_probability', 0)
        
        # Check if system discriminates well
        discrimination = high_score - low_score
        
        logger.info(f"\nSuccess Probabilities:")
        logger.info(f"  High Potential: {high_score:.2%}")
        logger.info(f"  Average: {avg_score:.2%}")
        logger.info(f"  Low Potential: {low_score:.2%}")
        logger.info(f"\nDiscrimination Power: {discrimination:.2%}")
        
        # Verify pattern system contribution
        if 'pattern_analysis' in results.get('average', {}).get('model_predictions', {}):
            pattern_contribution = results['average']['weights_used']['pattern_analysis']
            logger.info(f"\nPattern System Contribution: {pattern_contribution:.0%} ✅")
        else:
            logger.warning("\nPattern System NOT contributing to predictions ❌")
        
        # Overall assessment
        if discrimination > 0.3 and pattern_contribution > 0.2:
            logger.info("\n✅ SYSTEM WORKING CORRECTLY!")
            logger.info("Pattern integration successful with good discrimination")
        else:
            logger.warning("\n⚠️  SYSTEM NEEDS ADJUSTMENT")
            logger.warning("Low discrimination or pattern contribution")
    
    logger.info("\n" + "="*80)


if __name__ == "__main__":
    test_orchestrator()