#!/usr/bin/env python3
"""
Test the integrated pattern system
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from models.unified_orchestrator_v3 import get_orchestrator

def test_pattern_system():
    """Test the pattern system with example startups"""
    print("="*60)
    print("Testing Pattern System Integration")
    print("="*60)
    
    # Initialize orchestrator
    orchestrator = get_orchestrator()
    
    # Check pattern system status
    print("\n1. Pattern System Status:")
    print(f"   Pattern classifier loaded: {orchestrator.pattern_classifier is not None}")
    
    if orchestrator.pattern_classifier:
        patterns = orchestrator.list_patterns()
        print(f"   Patterns available: {len(patterns)}")
        
        # Show pattern distribution by category
        categories = {}
        for p in patterns:
            cat = p['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n   Patterns by category:")
        for cat, count in sorted(categories.items()):
            print(f"     - {cat}: {count} patterns")
    
    # Test cases
    test_cases = [
        {
            'name': 'High-Growth B2B SaaS',
            'features': {
                'revenue_growth_rate_percent': 300,
                'gross_margin_percent': 85,
                'ltv_cac_ratio': 5,
                'net_dollar_retention_percent': 130,
                'burn_multiple': 2.5,
                'tech_differentiation_score': 4,
                'team_size_full_time': 50,
                'total_capital_raised_usd': 20000000,
                'customer_count': 150,
                'annual_revenue_run_rate': 5000000,
                'funding_stage': 'series_a',
                'product_stage': 'growth',
                'scalability_score': 4,
                'brand_strength_score': 3,
                'board_advisor_experience_score': 4,
                'network_effects_present': 0,
                'has_data_moat': 1,
                'product_retention_30d': 0.75
            }
        },
        {
            'name': 'Struggling Hardware Startup',
            'features': {
                'revenue_growth_rate_percent': 20,
                'gross_margin_percent': 25,
                'patent_count': 3,
                'burn_multiple': 8,
                'runway_months': 6,
                'team_size_full_time': 15,
                'total_capital_raised_usd': 5000000,
                'tech_differentiation_score': 3,
                'scalability_score': 2,
                'funding_stage': 'seed',
                'product_stage': 'beta',
                'has_debt': 1,
                'brand_strength_score': 2,
                'board_advisor_experience_score': 3
            }
        },
        {
            'name': 'Profitable Bootstrap',
            'features': {
                'revenue_growth_rate_percent': 80,
                'gross_margin_percent': 75,
                'burn_multiple': 0.8,
                'annual_revenue_run_rate': 3000000,
                'team_size_full_time': 12,
                'total_capital_raised_usd': 100000,
                'customer_count': 500,
                'net_dollar_retention_percent': 105,
                'funding_stage': 'seed',
                'product_stage': 'mature',
                'tech_differentiation_score': 3,
                'scalability_score': 3,
                'brand_strength_score': 4,
                'board_advisor_experience_score': 3
            }
        }
    ]
    
    # Test each case
    for i, test_case in enumerate(test_cases):
        print(f"\n{i+2}. Testing: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Get enhanced prediction
            result = orchestrator.predict_enhanced(test_case['features'])
            
            # Display results
            print(f"   Success Probability: {result['success_probability']:.1%}")
            print(f"   Confidence Score: {result['confidence_score']:.2f}")
            print(f"   Model Agreement: {result['model_agreement']:.1%}")
            
            # Show component scores
            print("\n   Component Scores:")
            for component, score in result['prediction_components'].items():
                print(f"     - {component}: {score:.1%}")
            
            # Show pattern analysis
            if result.get('pattern_analysis'):
                pa = result['pattern_analysis']
                print(f"\n   Pattern Analysis:")
                print(f"     - Pattern Score: {pa.get('pattern_score', 0):.1%}")
                print(f"     - Patterns Detected: {pa.get('total_patterns_detected', 0)}")
                
                if pa.get('primary_patterns'):
                    print(f"\n     Primary Patterns:")
                    for p in pa['primary_patterns'][:3]:
                        print(f"       • {p['pattern']} ({p['confidence']:.0%} confidence)")
                        print(f"         Category: {p['category']}")
                
                if pa.get('pattern_insights'):
                    print(f"\n     Insights:")
                    for insight in pa['pattern_insights'][:2]:
                        print(f"       • {insight['message']}")
            
            # Show interpretation
            if result.get('interpretation'):
                interp = result['interpretation']
                print(f"\n   Interpretation:")
                print(f"     - Risk Level: {interp['risk_level']}")
                print(f"     - Success Probability: {interp['success_probability_text']}")
                
                if interp.get('main_factors'):
                    print(f"     - Main Factors:")
                    for factor in interp['main_factors']:
                        print(f"       • {factor}")
                
                if interp.get('recommendations'):
                    print(f"     - Recommendations:")
                    for rec in interp['recommendations']:
                        print(f"       • {rec}")
            
        except Exception as e:
            print(f"   ERROR: {str(e)}")
    
    # Test pattern details
    print("\n" + "="*60)
    print("3. Testing Pattern Details")
    print("-" * 40)
    
    # Get a specific pattern
    if patterns:
        test_pattern = patterns[0]['name']
        print(f"\n   Getting details for: {test_pattern}")
        
        try:
            details = orchestrator.get_pattern_details(test_pattern)
            
            print(f"   Name: {details['name']}")
            print(f"   Category: {details['category']}")
            print(f"   Description: {details['description']}")
            print(f"   Success Rate Range: {details['success_rate_range'][0]:.0%} - {details['success_rate_range'][1]:.0%}")
            print(f"   Example Companies: {', '.join(details['example_companies'][:3])}")
            
            if details.get('training_stats'):
                stats = details['training_stats']
                print(f"\n   Training Stats:")
                print(f"     - Examples in dataset: {stats.get('examples_in_dataset', 0):,}")
                print(f"     - Dataset percentage: {stats.get('dataset_percentage', 0):.1%}")
                print(f"     - Model accuracy: {stats.get('model_accuracy', 0):.1%}")
            
        except Exception as e:
            print(f"   ERROR: {str(e)}")
    
    print("\n" + "="*60)
    print("Pattern System Integration Test Complete!")
    print("="*60)


if __name__ == "__main__":
    test_pattern_system()