#!/usr/bin/env python3
import json
import requests
import time

# Test data for Progressive Deep Dive
flash_assessment_data = {
    "company_info": {
        "company_name": "FLASH Analytics",
        "industry": "ai-ml",
        "stage": "seed",
        "vision": "Democratize startup success prediction through AI",
        "current_strategy": "B2B SaaS for VCs and accelerators"
    },
    "context": {
        "market_position": "Early-stage AI analytics platform",
        "key_challenges": ["Low market awareness", "Limited resources", "Strong competition"],
        "opportunities": ["Growing VC market", "AI adoption surge", "Data-driven investing trend"]
    }
}

print('🚀 Testing Progressive Deep Dive System')
print('='*60)

# 1. Test Phase 1: Context Mapping
print('\n📊 Phase 1: Context Mapping')
print('-'*40)

# Test External Reality Check (Porter's Five Forces)
print('\n1.1 External Reality Check')
try:
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/phase1/analysis',
        json={
            "company_data": flash_assessment_data,
            "analysis_type": "external"
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Competitive Position: {result.get('position_assessment', {}).get('overall_rating', 'N/A')}")
        print(f"✓ Analysis completed successfully")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Internal Audit (CAMP Deep Dive)
print('\n1.2 Internal Audit (CAMP Deep Dive)')
try:
    camp_data = {
        "capital": {
            "total_raised": 2500000,
            "burn_rate": 150000,
            "runway_months": 12,
            "revenue": 2000000
        },
        "advantage": {
            "key_differentiators": ["AI/ML expertise", "Real startup data", "CAMP framework"],
            "moat_strength": "medium",
            "ip_assets": 2
        },
        "market": {
            "tam": 5000000000,
            "growth_rate": 35,
            "market_share": 0.1,
            "customer_count": 50
        },
        "people": {
            "team_size": 18,
            "founders_experience": 15,
            "key_hires_planned": 5,
            "culture_score": 4.5
        }
    }
    
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/phase1/camp',
        json={
            "camp_data": camp_data,
            "company_context": flash_assessment_data
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ CAMP Analysis completed")
        print(f"✓ Identified {len(result.get('improvement_areas', []))} improvement areas")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 2. Test Phase 2: Strategic Alignment
print('\n\n📊 Phase 2: Strategic Alignment')
print('-'*40)

# Test Vision-Reality Gap
print('\n2.1 Vision-Reality Gap Analysis')
try:
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/phase2/vision-gap',
        json={
            "vision": "Become the leading AI platform for startup evaluation globally",
            "current_reality": {
                "market_position": "Early-stage player",
                "resources": "Limited funding and team",
                "capabilities": "Strong ML, weak sales"
            },
            "company_data": flash_assessment_data
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Gap Score: {result.get('gap_analysis', {}).get('overall_gap_score', 'N/A')}")
        print(f"✓ Identified {len(result.get('gap_analysis', {}).get('key_gaps', []))} key gaps")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Ansoff Matrix
print('\n2.2 Ansoff Matrix Growth Strategy')
try:
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/phase2/ansoff',
        json={
            "current_products": ["FLASH Prediction Platform"],
            "current_markets": ["VCs", "Accelerators"],
            "company_data": flash_assessment_data,
            "growth_ambition": "aggressive"
        }
    )
    if response.status_code == 200:
        result = response.json()
        strategies = result.get('growth_strategies', [])
        print(f"✓ Generated {len(strategies)} growth strategies")
        if strategies:
            print(f"✓ Top strategy: {strategies[0].get('strategy_type', 'N/A')}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 3. Test Phase 3: Organizational Readiness
print('\n\n📊 Phase 3: Organizational Readiness (7S Framework)')
print('-'*40)
try:
    sevens_data = {
        "strategy": {"clarity": 4, "execution": 3, "alignment": 3.5},
        "structure": {"efficiency": 3, "flexibility": 4, "communication": 3.5},
        "systems": {"processes": 3, "technology": 4.5, "data_management": 4},
        "shared_values": {"culture_strength": 4, "mission_alignment": 4.5, "values_practice": 4},
        "skills": {"technical": 4.5, "business": 3, "leadership": 3.5},
        "style": {"management": 3.5, "decision_making": 4, "innovation": 4},
        "staff": {"talent_quality": 4, "engagement": 4, "retention": 3.5}
    }
    
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/phase3/sevens',
        json={
            "sevens_assessment": sevens_data,
            "company_data": flash_assessment_data
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Readiness Score: {result.get('readiness_analysis', {}).get('overall_readiness_score', 'N/A')}/5")
        print(f"✓ Critical gaps identified: {len(result.get('readiness_analysis', {}).get('critical_gaps', []))}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 4. Test Phase 4: Risk-Weighted Pathways
print('\n\n📊 Phase 4: Risk-Weighted Pathways')
print('-'*40)
try:
    scenarios = [
        {
            "name": "Aggressive Growth",
            "description": "Raise Series A, expand to 50+ employees",
            "investment_required": 10000000,
            "timeline_months": 18,
            "key_milestones": ["$10M ARR", "500 customers", "3 new products"]
        },
        {
            "name": "Steady Growth",
            "description": "Bootstrap with revenue, selective hiring",
            "investment_required": 0,
            "timeline_months": 24,
            "key_milestones": ["$5M ARR", "200 customers", "Profitability"]
        },
        {
            "name": "Strategic Partnership",
            "description": "Partner with major VC firm for distribution",
            "investment_required": 2000000,
            "timeline_months": 12,
            "key_milestones": ["$7M ARR", "Market leader partnership", "API platform"]
        }
    ]
    
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/phase4/scenarios',
        json={
            "scenarios": scenarios,
            "company_data": flash_assessment_data,
            "risk_tolerance": "moderate"
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Analyzed {len(scenarios)} scenarios")
        best = result.get('scenario_analysis', {}).get('recommended_scenario', {})
        print(f"✓ Recommended: {best.get('name', 'N/A')} (Score: {best.get('weighted_score', 'N/A')})")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# 5. Test Synthesis
print('\n\n📊 Phase 5: Synthesis & Executive Summary')
print('-'*40)
try:
    response = requests.post(
        'http://localhost:8001/api/analysis/deepdive/synthesis',
        json={
            "company_data": flash_assessment_data,
            "phase_results": {
                "phase1": {"position": "moderate", "camp_scores": {"capital": 0.44, "advantage": 0.025, "market": 0.32, "people": 0.11}},
                "phase2": {"vision_gap": 0.7, "growth_strategy": "market_penetration"},
                "phase3": {"readiness_score": 3.7, "critical_gaps": ["sales", "scaling"]},
                "phase4": {"recommended_scenario": "Steady Growth", "success_probability": 0.65}
            }
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Executive summary generated")
        print(f"✓ Strategic priorities: {len(result.get('synthesis', {}).get('strategic_priorities', []))}")
        print(f"✓ 90-day roadmap items: {len(result.get('synthesis', {}).get('implementation_roadmap', {}).get('next_90_days', []))}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print('\n' + '='*60)
print('✅ Progressive Deep Dive testing completed!')