"""
Framework Intelligence Engine Summary

This script provides a comprehensive summary of all frameworks in the database.
"""

from framework_database import FRAMEWORKS, FrameworkCategory, ComplexityLevel


def generate_framework_summary():
    """Generate a comprehensive summary of all frameworks"""
    
    print("=" * 80)
    print("FRAMEWORK INTELLIGENCE ENGINE - COMPLETE SUMMARY")
    print("=" * 80)
    
    # Total count
    total = len(FRAMEWORKS)
    print(f"\nTOTAL FRAMEWORKS: {total}")
    
    # By category
    print("\n" + "=" * 60)
    print("FRAMEWORKS BY CATEGORY:")
    print("=" * 60)
    
    categories = {}
    for fw in FRAMEWORKS.values():
        cat = fw.category.value
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(fw)
    
    for cat_name in sorted(categories.keys()):
        frameworks = categories[cat_name]
        print(f"\n{cat_name} ({len(frameworks)} frameworks):")
        print("-" * 40)
        for fw in sorted(frameworks, key=lambda x: x.name):
            print(f"  • {fw.name}")
            print(f"    {fw.description[:70]}...")
    
    # By complexity
    print("\n" + "=" * 60)
    print("FRAMEWORKS BY COMPLEXITY:")
    print("=" * 60)
    
    complexity_groups = {}
    for fw in FRAMEWORKS.values():
        comp = fw.complexity.name
        if comp not in complexity_groups:
            complexity_groups[comp] = []
        complexity_groups[comp].append(fw)
    
    for comp_name in ["BASIC", "INTERMEDIATE", "ADVANCED", "EXPERT"]:
        if comp_name in complexity_groups:
            frameworks = complexity_groups[comp_name]
            print(f"\n{comp_name} ({len(frameworks)} frameworks):")
            for fw in sorted(frameworks, key=lambda x: x.name)[:10]:  # Show first 10
                print(f"  • {fw.name} ({fw.category.value})")
    
    # Implementation times
    print("\n" + "=" * 60)
    print("IMPLEMENTATION TIMEFRAMES:")
    print("=" * 60)
    
    timeframes = {}
    for fw in FRAMEWORKS.values():
        time = fw.time_to_implement or "Not specified"
        if time not in timeframes:
            timeframes[time] = 0
        timeframes[time] += 1
    
    for time, count in sorted(timeframes.items()):
        print(f"  {time}: {count} frameworks")
    
    # Industry coverage
    print("\n" + "=" * 60)
    print("INDUSTRY COVERAGE:")
    print("=" * 60)
    
    industries = {}
    for fw in FRAMEWORKS.values():
        for ind in fw.industry_relevance:
            if ind not in industries:
                industries[ind] = 0
            industries[ind] += 1
    
    for ind, count in sorted(industries.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {ind}: {count} frameworks")
    
    # Key features
    print("\n" + "=" * 60)
    print("KEY FEATURES OF THE FRAMEWORK INTELLIGENCE ENGINE:")
    print("=" * 60)
    
    features = [
        "✓ Intelligent framework matching based on business context",
        "✓ Complexity assessment and prerequisite checking",
        "✓ Implementation roadmap generation",
        "✓ Synergistic framework combinations",
        "✓ Detailed implementation guides with customization",
        "✓ Risk assessment and impact estimation",
        "✓ Industry-specific recommendations",
        "✓ Stage-appropriate framework selection",
        "✓ Challenge-focused framework matching",
        "✓ Time-constrained implementation planning"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    # Sample use cases
    print("\n" + "=" * 60)
    print("SAMPLE USE CASES:")
    print("=" * 60)
    
    use_cases = [
        "Early-stage startup seeking product-market fit",
        "Growth-stage SaaS optimizing unit economics",
        "Enterprise undergoing digital transformation",
        "E-commerce company improving operational efficiency",
        "FinTech startup building scalable architecture",
        "Mature company driving innovation",
        "B2B company implementing account-based growth",
        "Consumer brand improving customer experience"
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"  {i}. {use_case}")
    
    print("\n" + "=" * 80)
    print("Note: This represents the initial 46 frameworks. The system is designed")
    print("to scale to 500+ frameworks across all business domains.")
    print("=" * 80)


if __name__ == "__main__":
    generate_framework_summary()