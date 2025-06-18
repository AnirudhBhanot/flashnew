#!/usr/bin/env python3
"""
Integration tests for the fixed FLASH system
Tests all components working together without shortcuts
"""

import subprocess
import time
import requests
import json
import sys
import os

# Test cases with expected outcomes
TEST_CASES = [
    {
        "name": "Terrible Pre-seed Startup",
        "description": "Should get < 30% probability and FAIL verdict",
        "data": {
            "funding_stage": "pre_seed",
            "total_capital_raised_usd": 10000,
            "last_round_size_usd": 10000,
            "runway_months": 2,
            "burn_multiple": 10,
            "gross_margin_percent": -20,
            "revenue_growth_rate_percent": -50,
            "patent_count": 0,
            "proprietary_tech": 0,
            "network_effects_present": 0,
            "switching_costs_high": 0,
            "gross_margin_improvement_percent": -10,
            "technical_moat_score": 1,
            "time_to_revenue_months": 24,
            "scalability_score": 1,
            "tam_size_usd": 1000000,
            "sam_size_usd": 100000,
            "market_growth_rate_percent": 0,
            "market_maturity_score": 1,
            "competitive_intensity_score": 5,
            "customer_acquisition_cost_usd": 1000,
            "average_contract_value_usd": 100,
            "ltv_to_cac_ratio": 0.1,
            "payback_period_months": 99,
            "market_timing_score": 1,
            "regulatory_risk_score": 5,
            "team_size_full_time": 1,
            "technical_team_percent": 0,
            "founders_experience_score": 1,
            "advisors_score": 1,
            "board_strength_score": 1,
            "team_domain_expertise_score": 1,
            "previous_startup_experience": 0,
            "team_completeness_score": 1,
            "culture_fit_score": 1,
            "diversity_score": 0,
            "product_stage": "idea",
            "active_users": 0,
            "mrr_usd": 0,
            "feature_completeness_score": 1,
            "user_satisfaction_score": 1,
            "product_market_fit_score": 1,
            "innovation_score": 1,
            "time_to_market_score": 1,
            "iteration_speed_score": 1
        },
        "expected": {
            "max_probability": 0.35,
            "verdict": ["FAIL", "STRONG FAIL"],
            "avg_camp_score": 0.35
        }
    },
    {
        "name": "Mediocre Pre-seed (49% Case)",
        "description": "Should get ~45-50% probability and FAIL verdict",
        "data": {
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
        },
        "expected": {
            "min_probability": 0.40,
            "max_probability": 0.55,
            "verdict": ["FAIL", "CONDITIONAL PASS"],
            "avg_camp_score_range": [0.40, 0.50]
        }
    },
    {
        "name": "Excellent Series A",
        "description": "Should get > 70% probability and PASS verdict",
        "data": {
            "funding_stage": "series_a",
            "total_capital_raised_usd": 5000000,
            "last_round_size_usd": 3000000,
            "runway_months": 24,
            "burn_multiple": 1.2,
            "gross_margin_percent": 75,
            "revenue_growth_rate_percent": 200,
            "patent_count": 5,
            "proprietary_tech": 1,
            "network_effects_present": 1,
            "switching_costs_high": 1,
            "gross_margin_improvement_percent": 20,
            "technical_moat_score": 5,
            "time_to_revenue_months": 3,
            "scalability_score": 5,
            "tam_size_usd": 10000000000,
            "sam_size_usd": 1000000000,
            "market_growth_rate_percent": 50,
            "market_maturity_score": 4,
            "competitive_intensity_score": 2,
            "customer_acquisition_cost_usd": 100,
            "average_contract_value_usd": 10000,
            "ltv_to_cac_ratio": 4.5,
            "payback_period_months": 3,
            "market_timing_score": 5,
            "regulatory_risk_score": 1,
            "team_size_full_time": 25,
            "technical_team_percent": 80,
            "founders_experience_score": 5,
            "advisors_score": 5,
            "board_strength_score": 5,
            "team_domain_expertise_score": 5,
            "previous_startup_experience": 1,
            "team_completeness_score": 5,
            "culture_fit_score": 5,
            "diversity_score": 4,
            "product_stage": "growth",
            "active_users": 50000,
            "mrr_usd": 500000,
            "feature_completeness_score": 5,
            "user_satisfaction_score": 5,
            "product_market_fit_score": 5,
            "innovation_score": 5,
            "time_to_market_score": 5,
            "iteration_speed_score": 5
        },
        "expected": {
            "min_probability": 0.65,
            "verdict": ["PASS", "STRONG PASS"],
            "avg_camp_score": 0.60
        }
    }
]


def test_api_endpoint(base_url: str, test_case: dict) -> dict:
    """Test a single API endpoint with given data"""
    try:
        response = requests.post(
            f"{base_url}/predict_enhanced",
            json=test_case['data'],
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"Status {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def validate_result(result: dict, expected: dict, test_name: str) -> bool:
    """Validate that results match expectations"""
    passed = True
    issues = []
    
    # Check success probability
    prob = result['success_probability']
    
    if 'min_probability' in expected and prob < expected['min_probability']:
        issues.append(f"Probability {prob:.1%} below minimum {expected['min_probability']:.1%}")
        passed = False
    
    if 'max_probability' in expected and prob > expected['max_probability']:
        issues.append(f"Probability {prob:.1%} above maximum {expected['max_probability']:.1%}")
        passed = False
    
    # Check verdict
    if result['verdict'] not in expected['verdict']:
        issues.append(f"Verdict '{result['verdict']}' not in expected {expected['verdict']}")
        passed = False
    
    # Check CAMP scores
    camp_scores = result.get('pillar_scores', {})
    if camp_scores:
        avg_camp = sum(camp_scores.values()) / len(camp_scores)
        
        if 'avg_camp_score' in expected:
            if abs(avg_camp - expected['avg_camp_score']) > 0.1:
                issues.append(f"Average CAMP {avg_camp:.2f} differs from expected {expected['avg_camp_score']:.2f}")
                passed = False
        
        if 'avg_camp_score_range' in expected:
            min_camp, max_camp = expected['avg_camp_score_range']
            if avg_camp < min_camp or avg_camp > max_camp:
                issues.append(f"Average CAMP {avg_camp:.2f} outside range [{min_camp:.2f}, {max_camp:.2f}]")
                passed = False
    
    # Print results
    if passed:
        print(f"✅ {test_name}: PASSED")
        print(f"   Probability: {prob:.1%}, Verdict: {result['verdict']}")
        print(f"   CAMP avg: {avg_camp:.1%}")
    else:
        print(f"❌ {test_name}: FAILED")
        print(f"   Probability: {prob:.1%}, Verdict: {result['verdict']}")
        print(f"   CAMP avg: {avg_camp:.1%}")
        for issue in issues:
            print(f"   - {issue}")
    
    return passed


def main():
    """Run integration tests"""
    print("="*60)
    print("FLASH FIXED SYSTEM INTEGRATION TESTS")
    print("="*60)
    
    # Start the fixed API server
    print("\n1. Starting fixed API server...")
    server_process = subprocess.Popen(
        ["python3", "api_server_fixed.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("   Waiting for server initialization...")
    time.sleep(5)
    
    base_url = "http://localhost:8001"
    
    # Check if server is running
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("   ✅ Server is healthy")
        else:
            print("   ❌ Server health check failed")
            server_process.terminate()
            return
    except:
        print("   ❌ Could not connect to server")
        server_process.terminate()
        return
    
    # Run tests
    print("\n2. Running test cases...")
    print("-"*60)
    
    passed_tests = 0
    total_tests = len(TEST_CASES)
    
    for test_case in TEST_CASES:
        print(f"\nTest: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        
        # Make API call
        result = test_api_endpoint(base_url, test_case)
        
        if result['success']:
            # Validate results
            if validate_result(result['data'], test_case['expected'], test_case['name']):
                passed_tests += 1
        else:
            print(f"❌ API Error: {result['error']}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! The system is working correctly.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. System needs attention.")
    
    # Cleanup
    print("\n3. Stopping server...")
    server_process.terminate()
    server_process.wait()
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)