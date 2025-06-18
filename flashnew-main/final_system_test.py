#!/usr/bin/env python3
"""Final test of the complete FLASH system fix"""

import subprocess
import time
import requests
import json
import os

print("="*60)
print("FINAL FLASH SYSTEM TEST")
print("="*60)

# Start API server fresh
print("\n1. Starting API server with new models...")
server_process = subprocess.Popen(
    ["python3", "api_server_unified.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
print("   Waiting for server to initialize...")
time.sleep(5)

# Test the specific case mentioned
test_data = {
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 150000,
    "last_round_size_usd": 150000,
    "runway_months": 10,
    "burn_multiple": 3,
    "gross_margin_percent": 45,
    "revenue_growth_rate_percent": 80,
    
    "patent_count": 1,
    "proprietary_tech": 0,
    "network_effects_present": 0,
    "switching_costs_high": 0,
    "gross_margin_improvement_percent": 5,
    "technical_moat_score": 2,
    "time_to_revenue_months": 9,
    "scalability_score": 3,
    
    "tam_size_usd": 500000000,
    "sam_size_usd": 50000000,
    "market_growth_rate_percent": 15,
    "market_maturity_score": 3,
    "competitive_intensity_score": 4,
    "customer_acquisition_cost_usd": 800,
    "average_contract_value_usd": 2000,
    "ltv_to_cac_ratio": 2.0,
    "payback_period_months": 12,
    "market_timing_score": 3,
    "regulatory_risk_score": 3,
    
    "team_size_full_time": 4,
    "technical_team_percent": 50,
    "founders_experience_score": 2,
    "advisors_score": 2,
    "board_strength_score": 2,
    "team_domain_expertise_score": 2,
    "previous_startup_experience": 0,
    "team_completeness_score": 2,
    "culture_fit_score": 3,
    "diversity_score": 2,
    
    "product_stage": "mvp",
    "active_users": 100,
    "mrr_usd": 2000,
    "feature_completeness_score": 2,
    "user_satisfaction_score": 3,
    "product_market_fit_score": 2,
    "innovation_score": 3,
    "time_to_market_score": 3,
    "iteration_speed_score": 3
}

base_url = "http://localhost:8001"

print("\n2. Testing Pre-seed startup that should get ~49% and FAIL...")

try:
    response = requests.post(f"{base_url}/predict_enhanced", json=test_data, timeout=10)
    if response.ok:
        result = response.json()
        
        print("\n   RESULTS:")
        print("   " + "-"*40)
        
        # CAMP scores
        print("   CAMP Scores:")
        camp_avg = 0
        for pillar, score in result['pillar_scores'].items():
            print(f"     {pillar.capitalize()}: {score:.1%}")
            camp_avg += score
        camp_avg /= 4
        print(f"     Average: {camp_avg:.1%}")
        
        # Results
        print(f"\n   Success Probability: {result['success_probability']:.1%}")
        print(f"   Verdict: {result['verdict']}")
        
        # Analysis
        print("\n   ANALYSIS:")
        prob = result['success_probability']
        
        # Check if it's working correctly
        if camp_avg < 0.5 and prob < 0.5 and result['verdict'] == 'FAIL':
            print("   ✅ SYSTEM IS WORKING CORRECTLY!")
            print("   - Low CAMP average → Low probability → FAIL verdict")
        else:
            print("   ❌ SYSTEM STILL HAS ISSUES:")
            if camp_avg < 0.5 and prob > 0.5:
                print("   - Low CAMP but high probability (models overpredict)")
            if prob < 0.5 and result['verdict'] != 'FAIL':
                print("   - Low probability but wrong verdict")
                
    else:
        print(f"\n   Error: {response.status_code} - {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n   ❌ Could not connect to API server")
except Exception as e:
    print(f"\n   ❌ Error: {e}")

# Clean up
print("\n3. Stopping server...")
server_process.terminate()
server_process.wait()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)

# Summary
print("\nEXPECTED BEHAVIOR:")
print("- Pre-seed with mediocre metrics")
print("- CAMP average around 45-50%") 
print("- Success probability around 45-50%")
print("- Verdict: FAIL (< 50%)")

print("\nIF STILL SHOWING HIGH PROBABILITY:")
print("The models need to be retrained with better data or")
print("we should use CAMP scores directly as a temporary fix.")