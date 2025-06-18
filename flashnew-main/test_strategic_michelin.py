#!/usr/bin/env python3
"""
Test the Strategic Michelin Analysis implementation
"""

import requests
import json
import time

# Test data
test_data = {
    'startup_data': {
        'startup_name': 'NeuroPharma Innovations',
        'sector': 'healthcare',
        'funding_stage': 'seed',
        'total_capital_raised_usd': 2000000,
        'cash_on_hand_usd': 1500000,
        'market_size_usd': 50000000000,
        'market_growth_rate_annual': 15,
        'competitor_count': 20,
        'market_share_percentage': 0.05,
        'team_size_full_time': 15,
        'customer_count': 5,
        'customer_acquisition_cost_usd': 50000,
        'lifetime_value_usd': 500000,
        'monthly_active_users': 5,
        'proprietary_tech': True,
        'patents_filed': 3,
        'founders_industry_experience_years': 15,
        'b2b_or_b2c': 'b2b',
        'burn_rate_usd': 200000,
        'monthly_burn_usd': 200000,
        'runway_months': 8,
        'product_stage': 'beta',
        'investor_tier_primary': 'tier_2',
        'revenue_growth_rate': 0,
        'gross_margin': 80,
        'annual_revenue_usd': 100000
    },
    'include_financial_projections': True,
    'analysis_depth': 'comprehensive'
}

print('Testing Strategic Michelin Analysis')
print('='*60)
print()

# Test Phase 1
print('PHASE 1: Situational Analysis')
print('-'*30)

try:
    start_time = time.time()
    response = requests.post('http://localhost:8001/api/michelin/strategic/analyze/phase1', json=test_data)
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        phase1 = data['phase1']
        print(f'✅ Phase 1 completed in {elapsed:.1f}s')
        print(f'\nExecutive Summary: {phase1["executive_summary"][:200]}...')
        print(f'\nBCG Position: {phase1["bcg_matrix_analysis"]["position"]}')
        print(f'\nStrategic Priorities:')
        for i, priority in enumerate(phase1['swot_analysis']['strategic_priorities'][:3], 1):
            print(f'  {i}. {priority[:80]}...')
        
        # Save Phase 1 results for Phase 2
        phase1_results = phase1
        
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text[:500])
        exit(1)
        
except Exception as e:
    print(f'❌ Request failed: {e}')
    exit(1)

print()
print('PHASE 2: Strategic Options')
print('-'*30)

# Test Phase 2
phase2_data = {
    'startup_data': test_data['startup_data'],
    'phase1_results': phase1_results
}

try:
    start_time = time.time()
    response = requests.post('http://localhost:8001/api/michelin/strategic/analyze/phase2', json=phase2_data)
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        phase2 = data['phase2']
        print(f'✅ Phase 2 completed in {elapsed:.1f}s')
        print(f'\nStrategic Options Overview: {phase2["strategic_options_overview"][:200]}...')
        
        print(f'\nBlue Ocean Strategy:')
        print(f'  - Eliminate: {len(phase2["blue_ocean_strategy"]["eliminate"])} items')
        if phase2["blue_ocean_strategy"]["eliminate"]:
            print(f'    • {phase2["blue_ocean_strategy"]["eliminate"][0][:60]}...')
        print(f'  - Create: {len(phase2["blue_ocean_strategy"]["create"])} items')
        if phase2["blue_ocean_strategy"]["create"]:
            print(f'    • {phase2["blue_ocean_strategy"]["create"][0][:60]}...')
        
        print(f'\nGrowth Scenarios:')
        for scenario in phase2['growth_scenarios'][:3]:
            print(f'  - {scenario["name"]}: {int(scenario["success_probability"]*100)}% probability')
        
        # Save Phase 2 results for Phase 3
        phase2_results = phase2
        
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text[:500])
        exit(1)
        
except Exception as e:
    print(f'❌ Request failed: {e}')
    exit(1)

print()
print('PHASE 3: Implementation Roadmap')
print('-'*30)

# Test Phase 3
phase3_data = {
    'startup_data': test_data['startup_data'],
    'phase1_results': phase1_results,
    'phase2_results': phase2_results
}

try:
    start_time = time.time()
    response = requests.post('http://localhost:8001/api/michelin/strategic/analyze/phase3', json=phase3_data)
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        phase3 = data['phase3']
        print(f'✅ Phase 3 completed in {elapsed:.1f}s')
        
        print(f'\nImplementation Timeline:')
        for milestone in phase3['implementation_roadmap']['milestones'][:3]:
            print(f'  - {milestone["timeframe"]}: {milestone["title"][:60]}...')
        
        print(f'\nSuccess Metrics:')
        for metric in phase3['success_metrics']['metrics'][:3]:
            print(f'  - {metric["metric"]}: Target {metric["target"]} by {metric["timeframe"]}')
        
        print(f'\nKey Risks:')
        for risk in phase3['risk_mitigation']['risks'][:2]:
            print(f'  - {risk["risk"][:50]}... (Impact: {risk["impact"]})')
        
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text[:500])
        
except Exception as e:
    print(f'❌ Request failed: {e}')

print()
print('='*60)
print('Strategic Michelin Analysis Test Complete')