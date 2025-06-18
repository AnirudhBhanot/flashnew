#!/usr/bin/env python3
"""
Test frontend-backend integration after cleanup
"""

import requests
import json
import time
import subprocess
import os
import signal

def test_api_health():
    """Test if API is healthy"""
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✅ API Health Check: OK")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except:
        print("❌ API not reachable")
        return False

def test_prediction_endpoint():
    """Test prediction endpoint with sample data"""
    # Sample startup data
    test_data = {
        "funding_stage": "Series A",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 150000,
        "annual_revenue_run_rate": 1200000,
        "revenue_growth_rate_yoy": 150,
        "gross_margin": 75,
        "r_and_d_spend_percentage": 25,
        "sales_marketing_efficiency": 1.2,
        "customer_acquisition_cost": 5000,
        "lifetime_value": 25000,
        "months_to_profitability": 18,
        "investor_tier_primary": "Tier 1",
        "investor_experience_score": 85,
        "board_diversity_score": 70,
        "scalability_score": 4,
        "innovation_index": 80,
        "competitive_moat_score": 75,
        "technical_debt_ratio": 20,
        "team_size": 25,
        "engineering_ratio": 60,
        "founder_experience_years": 12,
        "repeat_founder": True,
        "team_completeness_score": 90,
        "advisory_board_strength": 85,
        "company_age_months": 24,
        "pivot_count": 1,
        "partnership_score": 70,
        "customer_concentration": 15,
        "international_presence": False,
        "esg_score": 65,
        "market_size_billions": 10,
        "market_growth_rate": 25,
        "market_competition_level": "medium",
        "regulatory_risk_score": 30,
        "technology_risk_score": 25,
        "ip_portfolio_strength": 70,
        "product_market_fit_score": 80,
        "viral_coefficient": 1.2,
        "weekly_active_users_growth": 10,
        "feature_adoption_rate": 65,
        "tech_stack_modernity": 85,
        "cybersecurity_score": 80,
        "data_privacy_compliance": 90,
        "platform_risk_score": 20
    }
    
    try:
        # Test /predict endpoint
        print("\n📊 Testing /predict endpoint...")
        response = requests.post("http://localhost:8001/predict", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"   - Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"   - Verdict: {result.get('verdict', 'N/A')}")
            print(f"   - Confidence: {result.get('confidence_interval', {}).get('lower', 0):.1%} - {result.get('confidence_interval', {}).get('upper', 0):.1%}")
            
            # Check CAMP scores
            camp_scores = result.get('camp_scores', {})
            if camp_scores:
                print("   - CAMP Scores:")
                for pillar, score in camp_scores.items():
                    print(f"     • {pillar}: {score:.2f}")
            
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing prediction: {str(e)}")
        return False

def test_pattern_endpoint():
    """Test pattern endpoints"""
    try:
        print("\n🔍 Testing /patterns endpoint...")
        response = requests.get("http://localhost:8001/patterns")
        
        if response.status_code == 200:
            patterns = response.json()
            print(f"✅ Pattern endpoint working: {len(patterns)} patterns available")
            return True
        else:
            print(f"❌ Pattern endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing patterns: {str(e)}")
        return False

def test_frontend_config():
    """Check frontend configuration"""
    print("\n🖥️  Checking frontend configuration...")
    
    config_path = "/Users/sf/Desktop/FLASH/flash-frontend/src/config.ts"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
            if "localhost:8001" in content:
                print("✅ Frontend configured for port 8001")
                return True
            else:
                print("❌ Frontend not configured for correct port")
                return False
    else:
        print("❌ Frontend config not found")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Testing Frontend-Backend Integration After Cleanup")
    print("="*60)
    
    # Start API server
    print("\n1️⃣ Starting API server...")
    api_process = subprocess.Popen(
        ["python3", "api_server_unified.py"],
        cwd="/Users/sf/Desktop/FLASH",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("   Waiting for server to initialize...")
    time.sleep(5)
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if test_api_health():
        tests_passed += 1
    
    if test_prediction_endpoint():
        tests_passed += 1
        
    if test_pattern_endpoint():
        tests_passed += 1
        
    if test_frontend_config():
        tests_passed += 1
    
    # Kill API server
    api_process.terminate()
    api_process.wait()
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All integration tests passed! System is working correctly.")
        print("\n🚀 To run the full system:")
        print("   1. Start API: cd /Users/sf/Desktop/FLASH && python3 api_server_unified.py")
        print("   2. Start Frontend: cd flash-frontend && npm start")
        print("   3. Open browser to http://localhost:3000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    exit(0 if main() else 1)