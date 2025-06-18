#!/usr/bin/env python3
"""
Test script for Progressive Deep Dive LLM endpoints
"""

import asyncio
import json
from datetime import datetime
from api_llm_endpoints import (
    Phase1AnalysisRequest,
    Phase2VisionRealityRequest,
    Phase3OrganizationalRequest,
    Phase4ScenariosRequest,
    ScenarioDefinition,
    DeepDiveSynthesisRequest,
    analyze_competitive_position,
    analyze_vision_reality_gap,
    analyze_organizational_alignment,
    analyze_strategic_scenarios,
    synthesize_deep_dive_analysis,
    get_llm_engine
)

async def test_endpoints():
    """Test all deep dive endpoints"""
    
    # Initialize LLM engine
    engine = get_llm_engine()
    
    print("Testing Progressive Deep Dive Endpoints...")
    print("=" * 50)
    
    # Test Phase 1: Competitive Analysis
    print("\n1. Testing Phase 1 - Competitive Analysis")
    phase1_request = Phase1AnalysisRequest(
        porters_five_forces={
            "supplier_power": {
                "rating": "Medium",
                "factors": ["Limited suppliers", "High switching costs"],
                "score": 6.5
            },
            "buyer_power": {
                "rating": "High",
                "factors": ["Many alternatives", "Low switching costs"],
                "score": 7.8
            },
            "competitive_rivalry": {
                "rating": "High",
                "factors": ["Many competitors", "Low differentiation"],
                "score": 8.2
            },
            "threat_of_substitution": {
                "rating": "Medium",
                "factors": ["Some alternatives exist", "Different value propositions"],
                "score": 5.5
            },
            "threat_of_new_entry": {
                "rating": "Low",
                "factors": ["High barriers to entry", "Capital requirements"],
                "score": 3.2
            }
        },
        internal_audit={
            "strengths": [
                "Strong technical team",
                "Innovative product features",
                "Good customer relationships"
            ],
            "weaknesses": [
                "Limited marketing capabilities",
                "Cash flow constraints",
                "Lack of international presence"
            ],
            "opportunities": [
                "Growing market demand",
                "Partnership opportunities",
                "New geographic markets"
            ],
            "threats": [
                "Economic uncertainty",
                "Regulatory changes",
                "Technology disruption"
            ]
        }
    )
    
    try:
        phase1_result = await analyze_competitive_position(
            request=phase1_request,
            engine=engine
        )
        print("✓ Phase 1 completed successfully")
        print(f"  - Competitive position: {phase1_result.get('competitive_position', {}).get('overall_rating', 'N/A')}")
        print(f"  - Strategic gaps identified: {len(phase1_result.get('strategic_gaps', []))}")
    except Exception as e:
        print(f"✗ Phase 1 failed: {e}")
        phase1_result = {}
    
    # Test Phase 2: Vision-Reality Analysis
    print("\n2. Testing Phase 2 - Vision-Reality Analysis")
    phase2_request = Phase2VisionRealityRequest(
        vision_statement="To become the leading SaaS platform for enterprise automation by 2027",
        current_reality={
            "market_share": "5%",
            "revenue": "$10M ARR",
            "customer_base": "50 enterprise clients",
            "geographic_presence": "US only",
            "product_maturity": "MVP with core features"
        },
        ansoff_matrix_position="market_penetration"
    )
    
    try:
        phase2_result = await analyze_vision_reality_gap(
            request=phase2_request,
            engine=engine
        )
        print("✓ Phase 2 completed successfully")
        print(f"  - Gap size: {phase2_result.get('gap_analysis', {}).get('overall_gap_size', 'N/A')}")
        print(f"  - Bridging strategies: {len(phase2_result.get('bridging_strategies', []))}")
    except Exception as e:
        print(f"✗ Phase 2 failed: {e}")
        phase2_result = {}
    
    # Test Phase 3: Organizational Analysis
    print("\n3. Testing Phase 3 - Organizational Analysis")
    phase3_request = Phase3OrganizationalRequest(
        seven_s_framework={
            "strategy": {
                "description": "Focus on enterprise automation",
                "clarity": "High",
                "alignment": "Medium"
            },
            "structure": {
                "description": "Functional organization",
                "efficiency": "Medium",
                "flexibility": "Low"
            },
            "systems": {
                "description": "Basic operational systems",
                "automation": "Low",
                "integration": "Medium"
            },
            "shared_values": {
                "description": "Innovation and customer focus",
                "adoption": "High",
                "consistency": "Medium"
            },
            "skills": {
                "description": "Strong technical skills",
                "gaps": ["Sales", "Marketing"],
                "development": "Medium"
            },
            "style": {
                "description": "Collaborative leadership",
                "effectiveness": "High",
                "consistency": "Medium"
            },
            "staff": {
                "description": "25 FTEs",
                "retention": "High",
                "engagement": "Medium"
            }
        }
    )
    
    try:
        phase3_result = await analyze_organizational_alignment(
            request=phase3_request,
            engine=engine
        )
        print("✓ Phase 3 completed successfully")
        print(f"  - Overall alignment: {phase3_result.get('alignment_scores', {}).get('overall_alignment', 'N/A')}")
        print(f"  - Critical gaps: {len(phase3_result.get('critical_gaps', []))}")
    except Exception as e:
        print(f"✗ Phase 3 failed: {e}")
        phase3_result = {}
    
    # Test Phase 4: Scenario Analysis
    print("\n4. Testing Phase 4 - Scenario Analysis")
    phase4_request = Phase4ScenariosRequest(
        scenarios=[
            ScenarioDefinition(
                id="scenario_1",
                name="Aggressive Expansion",
                description="Rapid market expansion with heavy investment",
                assumptions=[
                    "Market demand continues to grow",
                    "Can raise $50M Series B",
                    "Can hire 100+ people in 12 months"
                ],
                investment_required=50000000,
                time_horizon_months=24
            ),
            ScenarioDefinition(
                id="scenario_2",
                name="Focused Growth",
                description="Steady growth in core market",
                assumptions=[
                    "Focus on existing market",
                    "Organic growth strategy",
                    "Minimal external funding"
                ],
                investment_required=10000000,
                time_horizon_months=36
            ),
            ScenarioDefinition(
                id="scenario_3",
                name="Platform Pivot",
                description="Transform into platform business model",
                assumptions=[
                    "Can build ecosystem",
                    "Partners will adopt platform",
                    "Technical feasibility confirmed"
                ],
                investment_required=25000000,
                time_horizon_months=18
            )
        ],
        market_data={
            "market_size": "$5B",
            "growth_rate": "25% CAGR",
            "competitive_landscape": "Fragmented",
            "customer_trends": "Increasing automation adoption"
        },
        company_capabilities={
            "technical": "Strong",
            "sales": "Developing",
            "marketing": "Weak",
            "operations": "Medium",
            "financial_resources": "$5M cash"
        }
    )
    
    try:
        phase4_result = await analyze_strategic_scenarios(
            request=phase4_request,
            engine=engine
        )
        print("✓ Phase 4 completed successfully")
        print(f"  - Scenarios analyzed: {len(phase4_result.get('scenario_assessments', []))}")
        print(f"  - Recommended scenario: {phase4_result.get('recommended_scenario', {}).get('scenario_name', 'N/A')}")
    except Exception as e:
        print(f"✗ Phase 4 failed: {e}")
        phase4_result = {}
    
    # Test Synthesis
    print("\n5. Testing Synthesis - Deep Dive Summary")
    synthesis_request = DeepDiveSynthesisRequest(
        phase1_data=phase1_result,
        phase2_data=phase2_result,
        phase3_data=phase3_result,
        phase4_data=phase4_result,
        ml_predictions={
            "success_probability": 0.72,
            "risk_score": 0.35,
            "growth_potential": 0.85
        }
    )
    
    try:
        synthesis_result = await synthesize_deep_dive_analysis(
            request=synthesis_request,
            engine=engine
        )
        print("✓ Synthesis completed successfully")
        print(f"  - Key findings: {len(synthesis_result.get('critical_insights', []))}")
        print(f"  - Action items: {len(synthesis_result.get('action_plan', []))}")
        
        # Print executive summary
        print("\nExecutive Summary:")
        print("-" * 30)
        summary = synthesis_result.get('executive_summary', {})
        if isinstance(summary, dict):
            for key, value in summary.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {summary}")
            
    except Exception as e:
        print(f"✗ Synthesis failed: {e}")
    
    # Cleanup
    await engine.close()
    
    print("\n" + "=" * 50)
    print("Testing completed!")

if __name__ == "__main__":
    asyncio.run(test_endpoints())