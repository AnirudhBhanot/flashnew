#!/usr/bin/env python3
"""
Test why Porter's Five Forces isn't being selected
"""

import asyncio
import sys
sys.path.insert(0, '/Users/sf/Desktop/FLASH')

from framework_intelligence.framework_database import FRAMEWORKS
from strategic_context_engine import StrategicContextEngine
from intelligent_framework_selector import IntelligentFrameworkSelector

async def test_porters_selection():
    """Test Porter's Five Forces selection"""
    
    # Check if Porter's Five Forces exists
    print("Checking if Porter's Five Forces exists in database...")
    porters_exists = False
    for fid, framework in FRAMEWORKS.items():
        if "porter" in fid.lower() or "porter" in framework.name.lower():
            print(f"Found: {fid} - {framework.name}")
            porters_exists = True
    
    if not porters_exists:
        print("\n❌ Porter's Five Forces NOT found in database!")
        return
    
    # Test with company that should benefit from Porter's analysis
    print("\n\nTesting framework selection for competitive analysis scenario...")
    
    context_engine = StrategicContextEngine()
    framework_selector = IntelligentFrameworkSelector()
    
    # Create a company with competitive challenges
    test_data = {
        "startup_name": "CompetitiveTest",
        "sector": "saas_b2b",
        "stage": "series_a",
        "revenue": 5000000,
        "growth_rate": 80,
        "burn_rate": 500000,
        "competition_intensity": 5,  # High competition
        "key_challenges": ["Intense competition", "Market differentiation", "Competitive positioning"]
    }
    
    context = await context_engine.build_company_context(test_data)
    
    # Override key_challenges to ensure competitive focus
    context.key_challenges = ["Intense competition", "Market differentiation", "Competitive positioning"]
    
    # Get all framework scores
    print("\nCalculating scores for all frameworks...")
    all_scores = framework_selector._score_all_frameworks(context, [])
    
    # Find Porter's score
    porters_score = None
    for score in all_scores:
        if "porter" in score.framework_id.lower():
            porters_score = score
            break
    
    if porters_score:
        print(f"\nPorter's Five Forces Score:")
        print(f"  Total: {porters_score.total_score:.1f}")
        print(f"  Context: {porters_score.context_score:.1f}")
        print(f"  Pattern: {porters_score.pattern_score:.1f}")
        print(f"  Synergy: {porters_score.synergy_score:.1f}")
        print(f"  Complexity: {porters_score.complexity_fit:.1f}")
        print(f"  Rationale: {porters_score.rationale}")
    
    # Show top 10 frameworks
    print("\n\nTop 10 frameworks by score:")
    for i, score in enumerate(all_scores[:10], 1):
        framework = FRAMEWORKS.get(score.framework_id)
        if framework:
            print(f"{i}. {framework.name} - Score: {score.total_score:.1f}")
    
    # Now select frameworks normally
    print("\n\nRunning normal framework selection...")
    frameworks = await framework_selector.select_frameworks(context, max_frameworks=5)
    
    print(f"\nSelected {len(frameworks)} frameworks:")
    for i, fw in enumerate(frameworks, 1):
        print(f"{i}. {fw.base_framework.name} (ID: {fw.base_framework.id})")

if __name__ == "__main__":
    asyncio.run(test_porters_selection())