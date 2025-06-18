#!/usr/bin/env python3
"""
Test Suite for FLASH Improvements
Validates: accuracy, probability range, calibration, and performance
"""

import requests
import json
import time
import numpy as np
from datetime import datetime


def test_probability_range():
    """Test that predictions span full 0-100% range"""
    print("\n1. Testing Probability Range...")
    
    test_cases = [
        {
            "name": "Unicorn Profile",
            "data": {
                "total_capital_raised_usd": 50000000,
                "revenue_growth_rate_percent": 300,
                "burn_multiple": 1.2,
                "team_size_full_time": 100,
                "prior_successful_exits_count": 2,
                "net_dollar_retention_percent": 140,
                "funding_stage": "series_b"
            },
            "expected_range": (0.7, 1.0)
        },
        {
            "name": "Struggling Startup",
            "data": {
                "total_capital_raised_usd": 500000,
                "revenue_growth_rate_percent": -20,
                "burn_multiple": 15,
                "runway_months": 3,
                "customer_count": 5,
                "funding_stage": "seed"
            },
            "expected_range": (0.0, 0.3)
        },
        {
            "name": "Average Startup",
            "data": {
                "total_capital_raised_usd": 2000000,
                "revenue_growth_rate_percent": 100,
                "burn_multiple": 3,
                "team_size_full_time": 15,
                "funding_stage": "seed"
            },
            "expected_range": (0.3, 0.7)
        }
    ]
    
    for test in test_cases:
        response = requests.post(
            "http://localhost:8001/predict",
            json=test["data"]
        )
        
        if response.status_code == 200:
            result = response.json()
            prob = result['success_probability']
            
            in_range = test["expected_range"][0] <= prob <= test["expected_range"][1]
            status = "✅" if in_range else "❌"
            
            print(f"  {status} {test['name']}: {prob:.1%} "
                  f"(expected {test['expected_range'][0]:.0%}-{test['expected_range'][1]:.0%})")
            print(f"     Confidence interval: [{result['confidence_interval']['lower']:.1%}, "
                  f"{result['confidence_interval']['upper']:.1%}]")
        else:
            print(f"  ❌ {test['name']}: API error {response.status_code}")


def test_confidence_intervals():
    """Test that confidence intervals are meaningful"""
    print("\n2. Testing Confidence Intervals...")
    
    # Complete data - should have narrow interval
    complete_data = {f: 1 for f in [
        "total_capital_raised_usd", "cash_on_hand_usd", "monthly_burn_usd",
        "revenue_growth_rate_percent", "team_size_full_time", "customer_count"
    ]}
    complete_data["funding_stage"] = "seed"
    
    # Sparse data - should have wide interval
    sparse_data = {
        "total_capital_raised_usd": 1000000,
        "funding_stage": "seed"
    }
    
    for name, data in [("Complete Data", complete_data), ("Sparse Data", sparse_data)]:
        response = requests.post("http://localhost:8001/predict", json=data)
        
        if response.status_code == 200:
            result = response.json()
            interval_width = result['confidence_interval']['upper'] - result['confidence_interval']['lower']
            
            print(f"  {name}:")
            print(f"    Interval width: {interval_width:.1%}")
            print(f"    Uncertainty: {result['uncertainty_level']}")
            print(f"    Verdict confidence: {result['verdict_confidence']}")


def test_scenario_analysis():
    """Test what-if scenario functionality"""
    print("\n3. Testing Scenario Analysis...")
    
    base_startup = {
        "total_capital_raised_usd": 2000000,
        "monthly_burn_usd": 200000,
        "runway_months": 10,
        "revenue_growth_rate_percent": 50,
        "burn_multiple": 4,
        "team_size_full_time": 10,
        "funding_stage": "seed"
    }
    
    scenarios = [
        {
            "name": "Reduce burn by 50%",
            "changes": {"monthly_burn_usd": 100000, "burn_multiple": 2}
        },
        {
            "name": "Double growth rate",
            "changes": {"revenue_growth_rate_percent": 100}
        },
        {
            "name": "Hire senior team",
            "changes": {"prior_successful_exits_count": 2, "years_experience_avg": 15}
        }
    ]
    
    request_data = {
        "base_data": base_startup,
        "scenarios": scenarios
    }
    
    response = requests.post("http://localhost:8001/scenarios", json=request_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"  Base probability: {result['base_probability']:.1%}")
        print("\n  Scenario impacts:")
        
        for scenario in result['scenarios']:
            impact_sign = "+" if scenario['impact'] > 0 else ""
            print(f"    {scenario['scenario_name']}: "
                  f"{impact_sign}{scenario['impact_percent']:.1f}% "
                  f"→ {scenario['success_probability']:.1%}")
                  
        print("\n  Recommendations:")
        for rec in result['recommendations']:
            print(f"    • {rec}")


def test_performance():
    """Test API response time"""
    print("\n4. Testing Performance...")
    
    test_data = {
        "total_capital_raised_usd": 5000000,
        "revenue_growth_rate_percent": 150,
        "team_size_full_time": 25,
        "funding_stage": "series_a"
    }
    
    # Warm up
    requests.post("http://localhost:8001/predict", json=test_data)
    
    # Test response times
    times = []
    for i in range(10):
        start = time.time()
        response = requests.post("http://localhost:8001/predict", json=test_data)
        elapsed = (time.time() - start) * 1000  # ms
        
        if response.status_code == 200:
            times.append(elapsed)
            
    if times:
        avg_time = np.mean(times)
        p95_time = np.percentile(times, 95)
        
        print(f"  Average response time: {avg_time:.0f}ms")
        print(f"  95th percentile: {p95_time:.0f}ms")
        print(f"  Target: <200ms ({'✅ PASS' if avg_time < 200 else '❌ FAIL'})")


def test_feature_importance():
    """Test feature importance endpoint"""
    print("\n5. Testing Feature Importance...")
    
    response = requests.get("http://localhost:8001/features/importance")
    
    if response.status_code == 200:
        result = response.json()
        
        if 'top_20_overall' in result:
            print("  Top 5 most important features:")
            for i, feature in enumerate(result['top_20_overall'][:5]):
                print(f"    {i+1}. {feature['feature']}: {feature['importance']:.4f}")
                
            print(f"\n  Engineered features: {result['engineered_features_count']} "
                  f"out of {result['total_features']} total")
        else:
            print("  ⚠️  Feature importance not yet calculated")


def main():
    """Run all tests"""
    print("=" * 60)
    print("FLASH IMPROVEMENTS TEST SUITE")
    print("=" * 60)
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API is healthy")
            print(f"   Models loaded: {health['models_loaded']}")
            print(f"   Feature engineering: {health['feature_engineering']}")
        else:
            print("❌ API health check failed")
            return
    except:
        print("❌ API is not running. Start with: python3 api_server_improved.py")
        return
    
    # Run tests
    test_probability_range()
    test_confidence_intervals()
    test_scenario_analysis()
    test_performance()
    test_feature_importance()
    
    print("\n" + "=" * 60)
    print("Test suite complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()