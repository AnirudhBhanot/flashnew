#!/usr/bin/env python3
"""
Test script for the intelligent framework recommendation API
"""

import requests
import json
from datetime import datetime

# API configuration
API_URL = "http://localhost:8001"
ENDPOINT = f"{API_URL}/api/frameworks/recommend"

# Test startup data
test_startup = {
    "company_name": "TechStart AI",
    "company_stage": "seed",
    "funding_stage": "seed",
    "industry": "SaaS",
    "sector": "B2B Software",
    
    # Team
    "team_size_full_time": 8,
    "technical_team_percent": 62.5,
    "founders_experience_years": 12,
    
    # Financial metrics
    "annual_revenue_run_rate": 240000,
    "revenue_growth_rate_percent": 50,
    "monthly_burn_usd": 80000,
    "runway_months": 15,
    "burn_multiple": 4.0,
    
    # Business metrics
    "customer_count": 15,
    "customer_acquisition_cost_usd": 3000,
    "customer_lifetime_value_usd": 12000,
    "net_dollar_retention_percent": 95,
    
    # Challenges and goals
    "primary_challenges": [
        "Finding product-market fit",
        "Customer acquisition",
        "Unit economics optimization"
    ],
    "goals": [
        "Reach $1M ARR within 12 months",
        "Improve LTV/CAC ratio to 5:1",
        "Build repeatable sales process"
    ],
    "pain_points": [
        "High burn rate relative to growth",
        "Limited runway",
        "Customer churn issues"
    ],
    
    # Additional context
    "business_model": "B2B SaaS",
    "target_market": "SMB Software Companies",
    "competitive_landscape": "Highly competitive with 10+ players",
    "unique_value_proposition": "AI-powered code review and optimization"
}

def test_framework_recommendation():
    """Test the framework recommendation endpoint"""
    print("=" * 60)
    print("Testing Intelligent Framework Recommendation API")
    print("=" * 60)
    print(f"\nEndpoint: {ENDPOINT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    print("\n📊 Startup Profile:")
    print(f"- Company: {test_startup['company_name']}")
    print(f"- Stage: {test_startup['company_stage']}")
    print(f"- Industry: {test_startup['industry']}")
    print(f"- Team Size: {test_startup['team_size_full_time']}")
    print(f"- Revenue: ${test_startup['annual_revenue_run_rate']:,}")
    print(f"- Runway: {test_startup['runway_months']} months")
    
    print("\n🎯 Primary Challenges:")
    for challenge in test_startup['primary_challenges']:
        print(f"  • {challenge}")
    
    try:
        # Make API request
        print("\n🚀 Sending request to API...")
        response = requests.post(
            ENDPOINT,
            json=test_startup,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ Success! Framework Analysis Complete")
            print("=" * 60)
            
            # Situation Analysis
            print("\n📋 SITUATION ANALYSIS:")
            print("-" * 40)
            print(data.get('situation_analysis', 'No analysis available'))
            
            # Strategic Priorities
            print("\n🎯 STRATEGIC PRIORITIES:")
            print("-" * 40)
            for i, priority in enumerate(data.get('strategic_priorities', []), 1):
                print(f"{i}. {priority}")
            
            # Framework Recommendations
            print("\n🛠️  RECOMMENDED FRAMEWORKS:")
            print("-" * 40)
            recommendations = data.get('recommendations', [])
            
            for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"\n{i}. {rec['framework_name']} ({rec['category']})")
                print(f"   📊 Relevance: {rec['relevance_score']*100:.0f}%")
                print(f"   ⏱️  Time to Value: {rec['time_to_value']}")
                print(f"   💡 Why: {rec['why_selected']}")
                print(f"   ⚡ Impact: {rec['expected_impact']}")
                
                if rec.get('specific_benefits'):
                    print("   ✨ Benefits:")
                    for benefit in rec['specific_benefits'][:2]:
                        print(f"      - {benefit}")
            
            # Implementation Roadmap
            print("\n📍 IMPLEMENTATION ROADMAP:")
            print("-" * 40)
            roadmap = data.get('implementation_roadmap', {})
            
            for phase_key, phase in roadmap.items():
                if isinstance(phase, dict) and 'name' in phase:
                    print(f"\n{phase['name']}:")
                    print(f"  Frameworks: {', '.join(phase.get('frameworks', []))}")
                    print(f"  Objectives:")
                    for obj in phase.get('objectives', [])[:2]:
                        print(f"    • {obj}")
            
            # Success Factors
            print("\n🌟 SUCCESS FACTORS:")
            print("-" * 40)
            for factor in data.get('success_factors', [])[:3]:
                print(f"• {factor}")
            
            # Summary Stats
            print("\n📊 ANALYSIS SUMMARY:")
            print("-" * 40)
            print(f"• Total frameworks analyzed: {data.get('total_frameworks_analyzed', 'N/A')}")
            print(f"• Frameworks recommended: {len(recommendations)}")
            print(f"• Selection method: {data.get('selection_rationale', 'AI-powered contextual analysis')}")
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the API server is running on http://localhost:8001")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def test_framework_analysis():
    """Test the framework analysis endpoint"""
    print("\n\n" + "=" * 60)
    print("Testing Framework Analysis (with insights)")
    print("=" * 60)
    
    analysis_endpoint = f"{API_URL}/api/frameworks/analyze-with-frameworks"
    
    try:
        print("\n🔍 Requesting framework-based analysis...")
        response = requests.post(
            analysis_endpoint,
            json=test_startup,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ Analysis Complete!")
            
            # Executive Summary
            if 'executive_summary' in data:
                print("\n📄 EXECUTIVE SUMMARY:")
                print("-" * 40)
                print(data['executive_summary'])
            
            # Framework Insights
            if 'framework_insights' in data:
                print("\n🔍 FRAMEWORK INSIGHTS:")
                print("-" * 40)
                
                for insight in data['framework_insights'][:3]:  # Show top 3
                    print(f"\n{insight['framework']} Analysis:")
                    print(f"  Category: {insight['category']}")
                    print(f"  Timeline: {insight['implementation_timeline']}")
                    print(f"  Analysis: {insight['analysis']}")
                    
                    if insight.get('action_items'):
                        print("  Action Items:")
                        for i, action in enumerate(insight['action_items'][:2], 1):
                            print(f"    {i}. {action}")
            
            # Next Steps
            if 'next_steps' in data:
                print("\n👣 NEXT STEPS:")
                print("-" * 40)
                for i, step in enumerate(data['next_steps'][:3], 1):
                    print(f"{i}. {step}")
        
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error testing analysis endpoint: {e}")

if __name__ == "__main__":
    # Test recommendation endpoint
    test_framework_recommendation()
    
    # Test analysis endpoint
    test_framework_analysis()
    
    print("\n\n✅ All tests completed!")
    print("=" * 60)