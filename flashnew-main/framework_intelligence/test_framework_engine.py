#!/usr/bin/env python3
"""
Test suite for Framework Intelligence Engine
"""

import asyncio
import json
from framework_selector import FrameworkSelector
from framework_database import FRAMEWORK_DATABASE

def test_framework_recommendations():
    """Test framework recommendation functionality"""
    selector = FrameworkSelector(FRAMEWORK_DATABASE)
    
    # Test case 1: Early-stage startup seeking PMF
    print("\n=== Test 1: Early-stage Fintech seeking Product-Market Fit ===")
    context1 = {
        "business_stage": "seed",
        "industry": "fintech",
        "primary_challenge": "finding_product_market_fit",
        "team_size": 5,
        "resources": "limited",
        "timeline": "3-6 months",
        "goals": ["achieve_product_market_fit", "validate_business_model"],
        "current_frameworks": []
    }
    
    recommendations1 = selector.recommend_frameworks(context1, top_n=5)
    print(f"Top 5 recommendations for early-stage fintech:")
    for i, rec in enumerate(recommendations1, 1):
        print(f"{i}. {rec['framework'].name} (Score: {rec['score']:.2f})")
        print(f"   Category: {rec['framework'].category}")
        print(f"   Reason: {rec['reasons'][0] if rec['reasons'] else 'N/A'}")
    
    # Test case 2: Growth-stage SaaS scaling operations
    print("\n=== Test 2: Growth-stage SaaS scaling operations ===")
    context2 = {
        "business_stage": "series_a",
        "industry": "saas",
        "primary_challenge": "scaling_operations",
        "team_size": 50,
        "resources": "moderate",
        "timeline": "6-12 months",
        "goals": ["scale_revenue", "improve_efficiency", "expand_team"],
        "current_frameworks": ["OKRs", "Agile"]
    }
    
    recommendations2 = selector.recommend_frameworks(context2, top_n=5)
    print(f"Top 5 recommendations for scaling SaaS:")
    for i, rec in enumerate(recommendations2, 1):
        print(f"{i}. {rec['framework'].name} (Score: {rec['score']:.2f})")
    
    # Test case 3: Mature company facing disruption
    print("\n=== Test 3: Mature company facing market disruption ===")
    context3 = {
        "business_stage": "mature",
        "industry": "retail",
        "primary_challenge": "market_disruption",
        "team_size": 500,
        "resources": "abundant",
        "timeline": "12-24 months",
        "goals": ["digital_transformation", "maintain_market_share"],
        "current_frameworks": ["Balanced Scorecard", "Six Sigma"]
    }
    
    recommendations3 = selector.recommend_frameworks(context3, top_n=5)
    print(f"Top 5 recommendations for disrupted retail:")
    for i, rec in enumerate(recommendations3, 1):
        print(f"{i}. {rec['framework'].name} (Score: {rec['score']:.2f})")

def test_implementation_roadmap():
    """Test implementation roadmap generation"""
    selector = FrameworkSelector(FRAMEWORK_DATABASE)
    
    print("\n=== Test: Implementation Roadmap Generation ===")
    context = {
        "business_stage": "seed",
        "industry": "marketplace",
        "primary_challenge": "building_two_sided_marketplace",
        "team_size": 10,
        "resources": "limited",
        "timeline": "6-12 months",
        "goals": ["achieve_liquidity", "balance_supply_demand"]
    }
    
    roadmap = selector.create_implementation_roadmap(context, max_frameworks=6)
    
    print(f"Total estimated time: {roadmap['total_estimated_time']}")
    print(f"Overall complexity: {roadmap['overall_complexity']}")
    print(f"\nPhased implementation plan:")
    
    for phase in roadmap['phases']:
        print(f"\nPhase {phase['phase']} ({phase['duration']}):")
        print(f"  Frameworks: {[f.name for f in phase['frameworks']]}")
        print(f"  Focus: {phase['focus']}")
        print(f"  Objectives:")
        for obj in phase['objectives']:
            print(f"    - {obj}")

def test_framework_combinations():
    """Test synergistic framework combinations"""
    selector = FrameworkSelector(FRAMEWORK_DATABASE)
    
    print("\n=== Test: Framework Combinations ===")
    context = {
        "business_stage": "growth",
        "industry": "ecommerce",
        "primary_challenge": "customer_retention",
        "goals": ["increase_ltv", "reduce_churn", "improve_nps"]
    }
    
    combinations = selector.find_framework_combinations(context, max_combinations=3)
    
    print(f"Top {len(combinations)} synergistic combinations:")
    for i, combo in enumerate(combinations, 1):
        print(f"\n{i}. Combination (Synergy: {combo['synergy_score']:.2f}):")
        print(f"   Frameworks: {' + '.join(combo['frameworks'])}")
        print(f"   Combined benefit: {combo['combined_benefit']}")
        print(f"   Implementation order: {' → '.join(combo['implementation_order'])}")
        print(f"   Estimated impact: {combo['estimated_impact']}")

def test_custom_implementation_guide():
    """Test custom implementation guide generation"""
    selector = FrameworkSelector(FRAMEWORK_DATABASE)
    
    print("\n=== Test: Custom Implementation Guide ===")
    context = {
        "business_stage": "seed",
        "industry": "healthtech",
        "team_size": 8,
        "resources": "limited",
        "timeline": "3 months"
    }
    
    guide = selector.generate_implementation_guide("Lean Startup", context)
    
    print(f"Custom Implementation Guide for Lean Startup:")
    print(f"\nTimeline: {guide['timeline']}")
    print(f"\nCustomized steps:")
    for i, (step, details) in enumerate(guide['customized_steps'].items(), 1):
        print(f"{i}. {step}")
        print(f"   Details: {details}")
    
    print(f"\nResource allocation:")
    for resource, allocation in guide['resource_allocation'].items():
        print(f"  - {resource}: {allocation}")
    
    print(f"\nQuick wins:")
    for win in guide['quick_wins']:
        print(f"  - {win}")

def test_scoring_algorithm():
    """Test the scoring algorithm with different contexts"""
    selector = FrameworkSelector(FRAMEWORK_DATABASE)
    
    print("\n=== Test: Scoring Algorithm ===")
    
    # Get a sample framework
    lean_startup = next(f for f in FRAMEWORK_DATABASE if f.name == "Lean Startup")
    
    # Test different contexts
    contexts = [
        {
            "name": "Perfect fit",
            "context": {
                "business_stage": "seed",
                "industry": "tech",
                "primary_challenge": "finding_product_market_fit",
                "team_size": 5,
                "resources": "limited",
                "timeline": "3-6 months"
            }
        },
        {
            "name": "Poor fit",
            "context": {
                "business_stage": "mature",
                "industry": "manufacturing",
                "primary_challenge": "cost_reduction",
                "team_size": 1000,
                "resources": "abundant",
                "timeline": "24+ months"
            }
        }
    ]
    
    for test_case in contexts:
        score = selector._calculate_framework_score(lean_startup, test_case["context"])
        print(f"\n{test_case['name']} context:")
        print(f"  Framework: {lean_startup.name}")
        print(f"  Score: {score:.2f}")
        print(f"  Context: {json.dumps(test_case['context'], indent=4)}")

def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print("Framework Intelligence Engine Test Suite")
    print("=" * 80)
    
    test_framework_recommendations()
    test_implementation_roadmap()
    test_framework_combinations()
    test_custom_implementation_guide()
    test_scoring_algorithm()
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    run_all_tests()