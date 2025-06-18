#!/usr/bin/env python3
"""
Test script for Deep Framework Analysis endpoint
Demonstrates enhanced strategic analysis with DeepSeek
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Test startup data
TEST_STARTUP = {
    "startup_name": "TechVenture AI",
    "sector": "SaaS",
    "funding_stage": "Series A",
    "total_capital_raised_usd": 5000000,
    "annual_revenue_usd": 2400000,
    "revenue_growth_rate_percent": 150,
    "monthly_burn_usd": 180000,
    "runway_months": 14,
    "team_size_full_time": 25,
    "tam_size_usd": 5000000000,
    "customer_count": 120,
    "net_dollar_retention_percent": 125,
    "gross_margin_percent": 75,
    "years_experience_avg": 8,
    "customer_concentration_percent": 15,
    "burn_multiple": 1.8
}

async def test_deep_analysis():
    """Test the deep framework analysis endpoint"""
    async with aiohttp.ClientSession() as session:
        # Endpoint URL
        url = "http://localhost:8001/api/frameworks/deep-analysis"
        
        # Request payload
        payload = {
            "startup_data": TEST_STARTUP,
            "framework_ids": ["bcg_matrix", "ansoff_matrix", "porters_five_forces"],
            "analysis_depth": "comprehensive",
            "include_implementation_plan": True,
            "include_metrics": True,
            "include_benchmarks": True
        }
        
        print(f"\n🚀 Testing Deep Framework Analysis for {TEST_STARTUP['startup_name']}")
        print(f"📊 Analyzing with frameworks: {', '.join(payload['framework_ids'])}")
        print("\n⏳ Sending request to API...")
        
        try:
            # Make the API call
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    print("\n✅ Analysis Complete!")
                    print("=" * 80)
                    
                    # Executive Summary
                    print(f"\n📋 EXECUTIVE SUMMARY")
                    print("-" * 40)
                    print(result.get("executive_summary", "No summary available"))
                    
                    # Framework Analyses
                    print(f"\n📊 FRAMEWORK ANALYSES")
                    print("-" * 40)
                    for analysis in result.get("framework_analyses", []):
                        print(f"\n🔍 {analysis['framework_name']} ({analysis['category']})")
                        print(f"   Position: {analysis['position']}")
                        print(f"   Score: {analysis['score']:.2f}")
                        
                        # Top recommendations
                        print(f"\n   Strategic Recommendations:")
                        for i, rec in enumerate(analysis.get("strategic_recommendations", [])[:3], 1):
                            print(f"   {i}. {rec}")
                        
                        # Key risks
                        if analysis.get("risk_factors"):
                            print(f"\n   Key Risks:")
                            for risk in analysis["risk_factors"][:2]:
                                print(f"   • {risk['risk']} (Impact: {risk['impact']})")
                        
                        # Expected outcomes
                        if analysis.get("expected_outcomes", {}).get("12_months"):
                            outcomes = analysis["expected_outcomes"]["12_months"]
                            print(f"\n   12-Month Projections:")
                            print(f"   • Revenue: {outcomes.get('revenue', 'N/A')}")
                            print(f"   • Team Size: {outcomes.get('team_size', 'N/A')}")
                            print(f"   • Confidence: {outcomes.get('confidence', 'N/A')}")
                    
                    # Integrated Insights
                    print(f"\n🔗 INTEGRATED INSIGHTS")
                    print("-" * 40)
                    integrated = result.get("integrated_insights", {})
                    
                    # Cross-framework patterns
                    if integrated.get("cross_framework_patterns"):
                        print("\nPatterns Across Frameworks:")
                        for pattern in integrated["cross_framework_patterns"]:
                            print(f"• {pattern}")
                    
                    # Critical decisions
                    if integrated.get("critical_decisions"):
                        print("\nCritical Decisions Required:")
                        for decision in integrated["critical_decisions"]:
                            print(f"• {decision['decision']} (Timeline: {decision['timeline']})")
                    
                    # Prioritized Actions
                    print(f"\n🎯 TOP PRIORITY ACTIONS")
                    print("-" * 40)
                    for i, action in enumerate(result.get("prioritized_actions", [])[:5], 1):
                        print(f"\n{i}. {action['action']}")
                        print(f"   Impact: {action['impact']} | Effort: {action['effort']}")
                        print(f"   Timeline: {action['timeline']} | Owner: {action['owner']}")
                        if action.get("success_metrics"):
                            print(f"   Success Metrics: {', '.join(action['success_metrics'][:2])}")
                    
                    # Implementation Roadmap
                    print(f"\n📅 IMPLEMENTATION ROADMAP")
                    print("-" * 40)
                    roadmap = result.get("implementation_roadmap", {})
                    for phase, details in roadmap.items():
                        if isinstance(details, dict):
                            print(f"\n{phase.replace('_', ' ').title()}: {details.get('timeline', '')}")
                            print(f"Focus: {details.get('focus', 'N/A')}")
                            if details.get("key_initiatives"):
                                print("Key Initiatives:")
                                for init in details["key_initiatives"][:2]:
                                    print(f"• {init}")
                    
                    # Success Probability
                    print(f"\n📈 SUCCESS ASSESSMENT")
                    print("-" * 40)
                    print(f"Overall Success Probability: {result.get('success_probability', 0)}%")
                    
                    # Success drivers
                    if result.get("success_drivers"):
                        print("\nKey Success Drivers:")
                        for driver in result["success_drivers"]:
                            print(f"• {driver}")
                    
                    # Key risks
                    if result.get("key_risks"):
                        print("\nMain Risk Factors:")
                        for risk in result["key_risks"][:3]:
                            print(f"• {risk['risk']} - {risk['mitigation']}")
                    
                    # Monitoring Plan
                    print(f"\n📊 MONITORING PLAN")
                    print("-" * 40)
                    monitoring = result.get("monitoring_plan", {})
                    if monitoring.get("weekly_metrics"):
                        print("Weekly Metrics to Track:")
                        for metric in monitoring["weekly_metrics"][:3]:
                            print(f"• {metric}")
                    
                    if monitoring.get("decision_triggers"):
                        print("\nDecision Triggers:")
                        for trigger in monitoring["decision_triggers"][:2]:
                            print(f"• {trigger['condition']} → {trigger['action']}")
                    
                    print("\n" + "=" * 80)
                    print("✅ Analysis complete! Full results saved to deep_analysis_result.json")
                    
                    # Save full results
                    with open("deep_analysis_result.json", "w") as f:
                        json.dump(result, f, indent=2)
                    
                else:
                    error_text = await response.text()
                    print(f"\n❌ Error {response.status}: {error_text}")
                    
        except Exception as e:
            print(f"\n❌ Request failed: {e}")

async def test_quick_insights():
    """Test the quick insights endpoint"""
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8001/api/frameworks/quick-insights/bcg_matrix"
        
        print(f"\n⚡ Testing Quick Insights for BCG Matrix")
        print("⏳ Sending request...")
        
        try:
            async with session.post(url, json=TEST_STARTUP) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    print("\n✅ Quick Insights:")
                    print(f"Framework: {result['framework']}")
                    print(f"Position: {result['position']} (Score: {result['score']:.2f})")
                    
                    print("\nTop Insights:")
                    for i, insight in enumerate(result.get("top_insights", []), 1):
                        print(f"{i}. {insight}")
                    
                    print("\nImmediate Actions:")
                    for i, action in enumerate(result.get("immediate_actions", []), 1):
                        print(f"{i}. {action['action']} (by {action['deadline']})")
                    
                else:
                    print(f"❌ Error {response.status}: {await response.text()}")
                    
        except Exception as e:
            print(f"❌ Request failed: {e}")

async def main():
    """Run all tests"""
    print("🚀 Deep Framework Analysis Test Suite")
    print("=" * 80)
    
    # Test comprehensive deep analysis
    await test_deep_analysis()
    
    # Test quick insights
    await test_quick_insights()

if __name__ == "__main__":
    asyncio.run(main())