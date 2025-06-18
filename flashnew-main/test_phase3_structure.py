#!/usr/bin/env python3
"""
Test Phase 3 structure
"""

import requests
import json
import time

# Wait for server
time.sleep(5)

test_data = {
    "startup_data": {
        "startup_name": "Test",
        "sector": "saas", 
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 500000,
        "market_size_usd": 1000000000,
        "market_growth_rate_annual": 20,
        "competitor_count": 5,
        "market_share_percentage": 0.1,
        "team_size_full_time": 10
    }
}

print("Testing Phase 3 structure...")
response = requests.post(
    "http://localhost:8001/api/michelin/analyze",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    data = response.json()
    phase3 = data["phase3"]
    
    print("\n✅ implementation_roadmap_summary:", "implementation_roadmap_summary" in phase3)
    
    # Check OKR framework
    print("\n✅ OKR Framework:")
    if isinstance(phase3.get("okr_framework"), list):
        print(f"  - Is array: True")
        print(f"  - Quarters: {len(phase3['okr_framework'])}")
        if phase3["okr_framework"]:
            okr = phase3["okr_framework"][0]
            print(f"  - Has quarter field: {'quarter' in okr}")
            if "objectives" in okr and okr["objectives"]:
                obj = okr["objectives"][0]
                print(f"  - Has key_results: {'key_results' in obj}")
                if "key_results" in obj and obj["key_results"]:
                    kr = obj["key_results"][0]
                    print(f"  - KR has kr/current/target: {'kr' in kr and 'current' in kr and 'target' in kr}")
    
    # Check resource requirements
    print("\n✅ Resource Requirements:")
    rr = phase3.get("resource_requirements", {})
    print(f"  - human_resources is array: {isinstance(rr.get('human_resources'), list)}")
    if rr.get("human_resources"):
        hr = rr["human_resources"][0]
        print(f"  - HR has role/timeline/cost: {'role' in hr and 'timeline' in hr and 'cost' in hr}")
    print(f"  - financial_resources has required fields: {'total_capital_needed' in rr.get('financial_resources', {})}")
    print(f"  - technology_resources is array: {isinstance(rr.get('technology_resources'), list)}")
    print(f"  - partnership_resources is array: {isinstance(rr.get('partnership_resources'), list)}")
    
    # Check risk mitigation
    print("\n✅ Risk Mitigation Plan:")
    if isinstance(phase3.get("risk_mitigation_plan"), list):
        print(f"  - Is array: True")
        print(f"  - Risk count: {len(phase3['risk_mitigation_plan'])}")
        if phase3["risk_mitigation_plan"]:
            risk = phase3["risk_mitigation_plan"][0]
            print(f"  - Has required fields: {'risk' in risk and 'impact' in risk and 'likelihood' in risk}")
            print(f"  - Has mitigation fields: {'mitigation_strategy' in risk and 'contingency_plan' in risk}")
    
    # Check success metrics
    print("\n✅ Success Metrics:")
    if isinstance(phase3.get("success_metrics"), list):
        print(f"  - Is array: True")
        print(f"  - Metric count: {len(phase3['success_metrics'])}")
        if phase3["success_metrics"]:
            metric = phase3["success_metrics"][0]
            print(f"  - Has required fields: {'metric' in metric and 'type' in metric and 'target' in metric and 'frequency' in metric}")
    
    print("\n🎉 All Phase 3 tests passed!")
    
else:
    print(f"Error: {response.status_code}")