#!/usr/bin/env python3
"""
Test the framework system directly
"""

import asyncio
import sys
sys.path.insert(0, '/Users/sf/Desktop/FLASH')

from api_framework_intelligent import generate_dynamic_framework_analysis, enhanced_selector

async def test_framework_system():
    """Test framework selection and analysis"""
    
    print("Testing Framework System...")
    
    # Test company data
    test_company = {
        'company_name': 'TechStartup AI',
        'industry': 'artificial_intelligence',
        'stage': 'series_a',
        'challenges': ['scaling', 'competition', 'talent_acquisition'],
        'team_size': 25,
        'total_funding': 10000000
    }
    
    print(f"\nTest Company: {test_company['company_name']}")
    print(f"Industry: {test_company['industry']}")
    print(f"Stage: {test_company['stage']}")
    print(f"Challenges: {', '.join(test_company['challenges'])}")
    
    # Test 1: Framework Selection
    print("\n=== TEST 1: Framework Selection ===")
    try:
        recommendations = enhanced_selector.recommend_frameworks_enhanced(
            business_stage='growth',  # series_a maps to growth
            industry='technology',
            primary_challenge='scaling',
            company_size=25,
            budget_level='medium',
            time_horizon='medium',
            strategic_goals=['scaling', 'competition', 'talent_acquisition'],
            top_k=6
        )
        
        print(f"\nRecommended {len(recommendations)} frameworks:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['name']} (Score: {rec['score']:.2f})")
            print(f"   Reason: {rec['reason']}")
            print(f"   Category: {rec.get('category', 'Unknown')}")
            print()
            
    except Exception as e:
        print(f"Framework selection failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Framework Analysis
    print("\n=== TEST 2: Framework Analysis ===")
    try:
        # Test Ansoff Matrix analysis
        analysis = await generate_dynamic_framework_analysis(
            'ansoff_matrix',
            'Ansoff Matrix',
            test_company
        )
        
        print(f"\nAnsoff Matrix Analysis for {test_company['company_name']}:")
        print(f"Current State: {analysis.get('current_state', 'N/A')[:200]}...")
        print(f"\nKey Insights: {len(analysis.get('key_insights', []))} insights")
        for insight in analysis.get('key_insights', [])[:3]:
            print(f"  - {insight}")
        print(f"\nRecommendations: {len(analysis.get('recommendations', []))} recommendations")
        for rec in analysis.get('recommendations', [])[:3]:
            print(f"  - {rec}")
            
    except Exception as e:
        print(f"Framework analysis failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Check if same frameworks for different companies
    print("\n=== TEST 3: Different Companies Test ===")
    
    companies = [
        {
            'company_name': 'FinTech Startup',
            'industry': 'fintech',
            'stage': 'seed',
            'challenges': ['product_development', 'funding'],
            'team_size': 5
        },
        {
            'company_name': 'E-commerce Giant',
            'industry': 'ecommerce',
            'stage': 'series_c',
            'challenges': ['market_expansion', 'competition'],
            'team_size': 200
        }
    ]
    
    for company in companies:
        try:
            stage_map = {'seed': 'startup', 'series_c': 'expansion'}
            recs = enhanced_selector.recommend_frameworks_enhanced(
                business_stage=stage_map.get(company['stage'], 'growth'),
                industry=company['industry'],
                primary_challenge=company['challenges'][0],
                company_size=company['team_size'],
                budget_level='medium',
                time_horizon='medium',
                strategic_goals=company['challenges'],
                top_k=3
            )
            
            print(f"\n{company['company_name']} ({company['industry']}, {company['stage']}):")
            for rec in recs:
                print(f"  - {rec['name']} (Score: {rec['score']:.2f})")
                
        except Exception as e:
            print(f"  Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_framework_system())