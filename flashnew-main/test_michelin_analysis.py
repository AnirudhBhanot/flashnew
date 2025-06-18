#!/usr/bin/env python3
"""
Test script for Michelin-style LLM analysis endpoint
"""

import asyncio
import json
from datetime import datetime
from api_michelin_llm_analysis import get_michelin_engine, StartupData

async def test_michelin_analysis():
    """Test the Michelin analysis with a sample startup"""
    
    # Sample startup data - realistic SaaS company
    startup_data = StartupData(
        company_name="CloudSync AI",
        sector="SaaS",
        funding_stage="Series A",
        annual_revenue_run_rate=2400000,  # $2.4M ARR
        revenue_growth_rate_percent=180,   # 180% YoY growth
        monthly_burn_usd=150000,          # $150k/month burn
        runway_months=18,                 # 18 months runway
        team_size_full_time=25,           # 25 full-time employees
        customer_count=120,               # 120 customers
        net_dollar_retention_percent=125, # 125% NDR
        burn_multiple=0.75,               # Efficient burn
        target_market="Mid-market B2B companies needing AI-powered data synchronization",
        key_competitors=["Zapier", "Workato", "Tray.io", "Make.com"],
        unique_value_proposition="AI-driven intelligent data mapping that reduces integration time by 90%",
        business_model="Subscription-based SaaS with usage-based pricing tiers",
        key_partnerships=["AWS", "Google Cloud", "Salesforce"],
        technology_stack=["Python", "React", "PostgreSQL", "Kubernetes", "TensorFlow"]
    )
    
    # Get the engine
    engine = get_michelin_engine()
    
    try:
        print("🚀 Starting Michelin-style strategic analysis...")
        print(f"Company: {startup_data.company_name}")
        print(f"Sector: {startup_data.sector}")
        print(f"Stage: {startup_data.funding_stage}")
        print("-" * 80)
        
        # Perform the analysis
        start_time = datetime.now()
        result = await engine.analyze_startup(startup_data)
        end_time = datetime.now()
        
        print(f"\n✅ Analysis completed in {(end_time - start_time).total_seconds():.2f} seconds")
        print("\n" + "="*80)
        
        # Display results
        print("\n📊 EXECUTIVE BRIEFING")
        print("-" * 80)
        print(result.executive_briefing)
        
        print("\n\n📍 PHASE 1: WHERE ARE WE NOW?")
        print("-" * 80)
        print(f"\nExecutive Summary: {result.phase1.executive_summary}")
        print(f"\nBCG Matrix Position: {result.phase1.bcg_matrix_analysis.get('position')}")
        print(f"\nCurrent Position Narrative:\n{result.phase1.current_position_narrative}")
        
        print("\n\n🎯 PHASE 2: WHERE SHOULD WE GO?")
        print("-" * 80)
        print(f"\nStrategic Options: {result.phase2.strategic_options_overview}")
        print(f"\nRecommended Direction:\n{result.phase2.recommended_direction}")
        
        print("\n\n🚀 PHASE 3: HOW TO GET THERE?")
        print("-" * 80)
        print(f"\nImplementation Roadmap: {result.phase3.implementation_roadmap}")
        
        print("\n\n💡 KEY RECOMMENDATIONS")
        print("-" * 80)
        for i, rec in enumerate(result.key_recommendations, 1):
            print(f"{i}. {rec}")
        
        print("\n\n⚡ CRITICAL SUCCESS FACTORS")
        print("-" * 80)
        for i, factor in enumerate(result.critical_success_factors, 1):
            print(f"{i}. {factor}")
        
        print("\n\n📅 NEXT STEPS (30-60-90 DAY PLAN)")
        print("-" * 80)
        for step in result.next_steps:
            print(f"\n{step['timeline']}:")
            for action in step['actions']:
                print(f"  • {action}")
        
        # Save full results to file
        output_file = f"michelin_analysis_{startup_data.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result.dict(), f, indent=2)
        print(f"\n\n💾 Full analysis saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        await engine.close()
        print("\n✅ Analysis engine closed")

if __name__ == "__main__":
    print("🎯 Michelin Strategic Analysis Test")
    print("=" * 80)
    asyncio.run(test_michelin_analysis())