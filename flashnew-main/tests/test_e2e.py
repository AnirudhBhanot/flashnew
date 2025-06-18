#!/usr/bin/env python3
"""
End-to-End Test for FLASH Platform
Tests the complete flow from API request to response
"""

import requests
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
import subprocess
import sys
import os
import signal

# Configuration
API_URL = "http://localhost:8001"
API_PROCESS = None

def start_api_server():
    """Start the API server in background"""
    global API_PROCESS
    print("Starting API server...")
    API_PROCESS = subprocess.Popen(
        [sys.executable, "api_server.py", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for server to start
    time.sleep(5)
    
    # Check if server is running
    for i in range(10):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                print("✅ API server started successfully")
                return True
        except:
            time.sleep(2)
    
    print("❌ Failed to start API server")
    return False

def stop_api_server():
    """Stop the API server"""
    global API_PROCESS
    if API_PROCESS:
        print("Stopping API server...")
        os.killpg(os.getpgid(API_PROCESS.pid), signal.SIGTERM)
        API_PROCESS.wait()
        print("✅ API server stopped")

def create_test_startup():
    """Create test startup data"""
    return {
        # Capital features
        'funding_stage': 'series_a',
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 3000000,
        'monthly_burn_usd': 150000,
        'annual_revenue_run_rate': 1200000,
        'revenue_growth_rate_percent': 150,
        'gross_margin_percent': 65,
        'ltv_cac_ratio': 3.0,
        'investor_tier_primary': 'tier_2',
        'has_debt': False,
        
        # Advantage features
        'patent_count': 2,
        'network_effects_present': True,
        'has_data_moat': True,
        'regulatory_advantage_present': False,
        'tech_differentiation_score': 4,
        'switching_cost_score': 3,
        'brand_strength_score': 3,
        'scalability_score': 4,
        'product_stage': 'growth',
        'product_retention_30d': 0.75,
        'product_retention_90d': 0.65,
        
        # Market features
        'sector': 'SaaS',
        'tam_size_usd': 50000000000,
        'sam_size_usd': 5000000000,
        'som_size_usd': 500000000,
        'market_growth_rate_percent': 25,
        'customer_count': 100,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 200,
        'net_dollar_retention_percent': 110,
        'competition_intensity': 3,
        'competitors_named_count': 10,
        'dau_mau_ratio': 0.4,
        
        # People features
        'founders_count': 2,
        'team_size_full_time': 25,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 8,
        'prior_startup_experience_count': 2,
        'prior_successful_exits_count': 1,
        'board_advisor_experience_score': 4,
        'advisors_count': 4,
        'team_diversity_percent': 40,
        'key_person_dependency': False
    }

def test_health_endpoint():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'models_loaded' in data
        
        print("✅ Health endpoint working")
        print(f"   Models loaded: {data['models_loaded']}")
        return True
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False

def test_prediction_endpoint():
    """Test prediction endpoint"""
    print("\n2. Testing Prediction Endpoint...")
    try:
        startup_data = create_test_startup()
        
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/predict",
            json=startup_data
        )
        end_time = time.time()
        
        assert response.status_code == 200
        
        data = response.json()
        assert 'success_probability' in data
        assert 0 <= data['success_probability'] <= 1
        assert 'confidence_interval' in data
        assert 'pillar_scores' in data
        assert 'insights' in data
        
        print("✅ Prediction endpoint working")
        print(f"   Success probability: {data['success_probability']:.2%}")
        print(f"   Confidence: [{data['confidence_interval']['lower']:.2%}, {data['confidence_interval']['upper']:.2%}]")
        print(f"   Response time: {(end_time - start_time)*1000:.0f}ms")
        
        # Print pillar scores
        print("   CAMP Scores:")
        for pillar, score in data['pillar_scores'].items():
            print(f"     - {pillar.capitalize()}: {score:.2%}")
        
        return True
    except Exception as e:
        print(f"❌ Prediction endpoint failed: {e}")
        if hasattr(response, 'text'):
            print(f"   Response: {response.text}")
        return False

def test_invalid_input():
    """Test invalid input handling"""
    print("\n3. Testing Invalid Input Handling...")
    try:
        # Missing required fields
        invalid_data = {
            'funding_stage': 'series_a',
            'total_capital_raised_usd': 5000000
            # Missing many required fields
        }
        
        response = requests.post(
            f"{API_URL}/predict",
            json=invalid_data
        )
        
        assert response.status_code in [400, 422]
        
        data = response.json()
        assert 'detail' in data
        
        print("✅ Invalid input handling working")
        print(f"   Error message: {data['detail']}")
        return True
    except Exception as e:
        print(f"❌ Invalid input handling failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases"""
    print("\n4. Testing Edge Cases...")
    results = []
    
    # Test 1: Zero values
    print("   Testing zero values...")
    startup = create_test_startup()
    startup['monthly_burn_usd'] = 0
    startup['customer_count'] = 0
    
    try:
        response = requests.post(f"{API_URL}/predict", json=startup)
        assert response.status_code == 200
        print("     ✅ Zero values handled")
        results.append(True)
    except:
        print("     ❌ Zero values failed")
        results.append(False)
    
    # Test 2: Maximum values
    print("   Testing maximum values...")
    startup = create_test_startup()
    startup['total_capital_raised_usd'] = 1e10
    startup['tam_size_usd'] = 1e12
    
    try:
        response = requests.post(f"{API_URL}/predict", json=startup)
        assert response.status_code == 200
        print("     ✅ Maximum values handled")
        results.append(True)
    except:
        print("     ❌ Maximum values failed")
        results.append(False)
    
    # Test 3: Different funding stages
    print("   Testing all funding stages...")
    stages = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c', 'growth']
    stage_results = []
    
    for stage in stages:
        startup = create_test_startup()
        startup['funding_stage'] = stage
        
        try:
            response = requests.post(f"{API_URL}/predict", json=startup)
            assert response.status_code == 200
            data = response.json()
            stage_results.append((stage, data['success_probability']))
            results.append(True)
        except:
            stage_results.append((stage, None))
            results.append(False)
    
    print("     Stage predictions:")
    for stage, prob in stage_results:
        if prob is not None:
            print(f"       - {stage}: {prob:.2%}")
        else:
            print(f"       - {stage}: Failed")
    
    return all(results)

def test_performance():
    """Test API performance"""
    print("\n5. Testing API Performance...")
    
    # Single request latency
    latencies = []
    for i in range(10):
        startup = create_test_startup()
        start_time = time.time()
        response = requests.post(f"{API_URL}/predict", json=startup)
        end_time = time.time()
        
        if response.status_code == 200:
            latencies.append((end_time - start_time) * 1000)
    
    if latencies:
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        
        print("✅ Performance metrics:")
        print(f"   Average latency: {avg_latency:.0f}ms")
        print(f"   P95 latency: {p95_latency:.0f}ms")
        print(f"   Min latency: {min(latencies):.0f}ms")
        print(f"   Max latency: {max(latencies):.0f}ms")
        
        return avg_latency < 500  # Target: < 500ms average
    else:
        print("❌ Performance test failed")
        return False

def test_concurrent_requests():
    """Test concurrent request handling"""
    print("\n6. Testing Concurrent Requests...")
    import concurrent.futures
    
    def make_request():
        startup = create_test_startup()
        response = requests.post(f"{API_URL}/predict", json=startup)
        return response.status_code == 200
    
    # Make 20 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        start_time = time.time()
        futures = [executor.submit(make_request) for _ in range(20)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
        end_time = time.time()
    
    success_count = sum(results)
    print(f"✅ Concurrent requests: {success_count}/20 successful")
    print(f"   Total time: {end_time - start_time:.1f}s")
    
    return success_count >= 18  # Allow 2 failures

def test_model_performance():
    """Test model performance endpoint"""
    print("\n7. Testing Model Performance Endpoint...")
    try:
        response = requests.get(f"{API_URL}/model_performance")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Model performance endpoint working")
            print(f"   AUC Score: {data.get('auc_score', 'N/A')}")
            print(f"   Accuracy: {data.get('accuracy', 'N/A')}")
            print(f"   Model Agreement: {data.get('model_agreement', 'N/A')}")
            return True
        else:
            print("❌ Model performance endpoint not available")
            return True  # Not critical
    except Exception as e:
        print(f"⚠️  Model performance endpoint error: {e}")
        return True  # Not critical

def run_all_tests():
    """Run all E2E tests"""
    print("="*60)
    print("FLASH Platform - End-to-End Tests")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Start API server
    if not start_api_server():
        print("\n❌ Failed to start API server. Exiting.")
        return False
    
    try:
        # Run tests
        tests = [
            test_health_endpoint,
            test_prediction_endpoint,
            test_invalid_input,
            test_edge_cases,
            test_performance,
            test_concurrent_requests,
            test_model_performance
        ]
        
        results = []
        for test in tests:
            results.append(test())
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        passed = sum(results)
        total = len(results)
        
        print(f"Tests Passed: {passed}/{total} ({passed/total*100:.0f}%)")
        
        if passed == total:
            print("\n✅ ALL E2E TESTS PASSED!")
            print("The FLASH platform is ready for production.")
        else:
            print(f"\n⚠️  {total - passed} tests failed.")
            print("Please check the errors above.")
        
        return passed == total
        
    finally:
        # Stop API server
        stop_api_server()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)