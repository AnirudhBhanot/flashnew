"""
Example usage of the Framework Intelligence Engine

This file demonstrates how to use the framework selector and database
to get intelligent framework recommendations for startups.
"""

from framework_selector import (
    recommend_frameworks_for_startup,
    get_implementation_roadmap,
    get_framework_combinations,
    get_detailed_implementation_guide
)
from framework_database import (
    get_framework_statistics,
    get_frameworks_by_category,
    FrameworkCategory
)


def main():
    print("=" * 80)
    print("FRAMEWORK INTELLIGENCE ENGINE - EXAMPLE USAGE")
    print("=" * 80)
    
    # Example 1: Get framework statistics
    print("\n1. FRAMEWORK DATABASE STATISTICS:")
    print("-" * 40)
    stats = get_framework_statistics()
    print(f"Total frameworks: {stats['total_frameworks']}")
    print("\nFrameworks by category:")
    for category, count in stats['by_category'].items():
        print(f"  - {category}: {count}")
    print("\nFrameworks by complexity:")
    for complexity, count in stats['by_complexity'].items():
        print(f"  - {complexity}: {count}")
    
    # Example 2: Get recommendations for a B2B SaaS startup
    print("\n\n2. FRAMEWORK RECOMMENDATIONS FOR B2B SAAS STARTUP:")
    print("-" * 40)
    
    recommendations = recommend_frameworks_for_startup(
        stage="growth",
        industry="b2b_saas",
        team_size=25,
        funding_stage="Series A",
        challenges=["customer_acquisition", "retention", "scaling"],
        goals=[
            "Achieve $10M ARR",
            "Improve customer retention by 20%",
            "Scale operations efficiently"
        ],
        constraints=["Limited engineering resources", "6 month timeline"],
        existing_frameworks=["agile_methodology"]
    )
    
    print(f"\nTop {len(recommendations)} recommended frameworks:\n")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"{i}. {rec['framework_name']} (Score: {rec['relevance_score']})")
        print(f"   Category: {rec['category']}")
        print(f"   Impact: {rec['estimated_impact']}, Risk: {rec['risk_level']}")
        print(f"   Time: {rec['time_to_implement']}")
        print(f"   Rationale:")
        for reason in rec['rationale']:
            print(f"     - {reason}")
        print()
    
    # Example 3: Get implementation roadmap
    print("\n3. IMPLEMENTATION ROADMAP:")
    print("-" * 40)
    
    roadmap = get_implementation_roadmap(recommendations[:10])
    for phase, frameworks in roadmap.items():
        if frameworks:
            print(f"\n{phase}:")
            for fw in frameworks:
                print(f"  - {fw['framework_name']} ({fw['complexity']}, Impact: {fw['estimated_impact']})")
    
    # Example 4: Get framework combinations
    print("\n\n4. SYNERGISTIC FRAMEWORK COMBINATIONS:")
    print("-" * 40)
    
    combinations = get_framework_combinations(
        stage="growth",
        industry="b2b_saas",
        challenges=["customer_acquisition", "retention"],
        goals=["Scale efficiently", "Improve unit economics"]
    )
    
    for i, combo in enumerate(combinations[:3], 1):
        print(f"\nCombination {i}:")
        for fw in combo:
            print(f"  - {fw['framework_name']} ({fw['category']})")
    
    # Example 5: Get detailed implementation guide
    print("\n\n5. DETAILED IMPLEMENTATION GUIDE:")
    print("-" * 40)
    
    # Get guide for the top recommended framework
    if recommendations:
        top_framework_id = recommendations[0]['framework_id']
        guide = get_detailed_implementation_guide(
            framework_id=top_framework_id,
            stage="growth",
            industry="b2b_saas",
            team_size=25
        )
        
        print(f"\nImplementation Guide for: {guide['framework']}")
        print(f"Duration: {guide['estimated_duration']}")
        print(f"\nTeam Requirements:")
        print(f"  - Minimum size: {guide['team_requirements']['minimum_team_size']}")
        print(f"  - Recommended size: {guide['team_requirements']['recommended_team_size']}")
        print(f"  - Key roles: {', '.join(guide['team_requirements']['key_roles'])}")
        
        print(f"\nPreparation Steps:")
        for step in guide['preparation_steps']:
            print(f"  - {step}")
            
        print(f"\nImplementation Phases:")
        for phase in guide['implementation_phases']:
            print(f"\n  {phase['phase']} ({phase['duration']}):")
            for activity in phase['activities']:
                print(f"    - {activity}")
                
        print(f"\nCustomization Notes:")
        for note in guide['customization_notes']:
            print(f"  - {note}")
    
    # Example 6: Search for specific types of frameworks
    print("\n\n6. CATEGORY-SPECIFIC FRAMEWORKS:")
    print("-" * 40)
    
    growth_frameworks = get_frameworks_by_category(FrameworkCategory.GROWTH)
    print(f"\nGrowth Frameworks ({len(growth_frameworks)} total):")
    for fw in growth_frameworks[:5]:
        print(f"  - {fw.name}: {fw.description[:80]}...")
    
    # Example 7: Different startup scenarios
    print("\n\n7. FRAMEWORK RECOMMENDATIONS FOR DIFFERENT SCENARIOS:")
    print("-" * 40)
    
    scenarios = [
        {
            "name": "Early Stage FinTech Startup",
            "stage": "mvp",
            "industry": "fintech",
            "team_size": 8,
            "funding_stage": "Seed",
            "challenges": ["product_development", "market_entry", "funding"],
            "goals": ["Find product-market fit", "Secure Series A funding"]
        },
        {
            "name": "Scaling E-commerce Company",
            "stage": "scale",
            "industry": "ecommerce",
            "team_size": 100,
            "funding_stage": "Series B",
            "challenges": ["operational_efficiency", "cost_optimization", "competitive_pressure"],
            "goals": ["Improve margins by 15%", "Expand internationally"]
        },
        {
            "name": "Enterprise Software Company",
            "stage": "mature",
            "industry": "enterprise",
            "team_size": 500,
            "funding_stage": "Series D",
            "challenges": ["innovation", "digital_transformation", "culture"],
            "goals": ["Drive innovation", "Transform company culture"]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        recs = recommend_frameworks_for_startup(
            stage=scenario['stage'],
            industry=scenario['industry'],
            team_size=scenario['team_size'],
            funding_stage=scenario['funding_stage'],
            challenges=scenario['challenges'],
            goals=scenario['goals']
        )
        
        print(f"Top 3 recommendations:")
        for i, rec in enumerate(recs[:3], 1):
            print(f"  {i}. {rec['framework_name']} (Score: {rec['relevance_score']})")


if __name__ == "__main__":
    main()