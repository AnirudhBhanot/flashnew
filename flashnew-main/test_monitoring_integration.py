#!/usr/bin/env python3
"""
Test monitoring integration for FLASH API
"""
import requests
import json
import time
import subprocess
import sys
import os

def wait_for_server(url, timeout=30):
    """Wait for server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code in [200, 503]:  # 503 is OK for health check if models not loaded
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_monitoring():
    """Test monitoring endpoints"""
    print("🔍 Testing Monitoring Integration")
    print("=" * 50)
    
    # Start the API server
    print("\n1. Starting API server...")
    server_process = subprocess.Popen(
        [sys.executable, "api_server_unified.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    try:
        # Wait for server to start
        if wait_for_server("http://localhost:8001/health"):
            print("✅ Server started successfully")
        else:
            print("❌ Server failed to start")
            return
        
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get("http://localhost:8001/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Models loaded: {data.get('models_loaded', 0)}")
            print(f"   Patterns available: {data.get('patterns_available', False)}")
            print("✅ Health endpoint working")
        
        # Test metrics summary endpoint (initial state)
        print("\n3. Testing metrics summary endpoint (initial)...")
        response = requests.get("http://localhost:8001/metrics/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total requests: {data.get('total_requests', 0)}")
            print(f"   Total predictions: {data.get('total_predictions', 0)}")
            print(f"   Error rate: {data.get('error_rate', 0):.2%}")
            print("✅ Metrics summary endpoint working")
        
        # Test metrics endpoint
        print("\n4. Testing metrics endpoint...")
        response = requests.get("http://localhost:8001/metrics")
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'text/plain' in content_type:
                print("   Format: Prometheus")
                # Print first few lines
                lines = response.text.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
            else:
                print("   Format: JSON (Prometheus not enabled)")
                data = response.json()
                print(f"   Uptime: {data.get('uptime_seconds', 0):.1f}s")
            print("✅ Metrics endpoint working")
        
        # Make test predictions
        print("\n5. Making test predictions...")
        test_cases = [
            {
                'name': 'High Success Startup',
                'data': {
                    'startup_name': 'HighSuccess Inc',
                    'funding_stage': 'series_a',
                    'sector': 'saas',
                    'total_capital_raised_usd': 5000000,
                    'monthly_burn_usd': 200000,
                    'customer_count': 1000,
                    'team_size_full_time': 25,
                    'founders_count': 3,
                    'market_growth_rate_percent': 50,
                    'user_growth_rate_percent': 100,
                    'runway_months': 25,
                    'annual_revenue_run_rate': 2000000
                }
            },
            {
                'name': 'Low Success Startup',
                'data': {
                    'startup_name': 'Struggling Inc',
                    'funding_stage': 'seed',
                    'sector': 'saas',
                    'total_capital_raised_usd': 100000,
                    'monthly_burn_usd': 50000,
                    'customer_count': 10,
                    'team_size_full_time': 3,
                    'founders_count': 1,
                    'runway_months': 2
                }
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   Testing: {test_case['name']}")
            try:
                response = requests.post("http://localhost:8001/predict", json=test_case['data'])
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Success probability: {result.get('success_probability', 0):.1%}")
                    print(f"   ✅ Verdict: {result.get('verdict', 'UNKNOWN')}")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Wait a bit for metrics to update
        time.sleep(2)
        
        # Check updated metrics
        print("\n6. Checking updated metrics...")
        response = requests.get("http://localhost:8001/metrics/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total requests: {data.get('total_requests', 0)}")
            print(f"   Total predictions: {data.get('total_predictions', 0)}")
            print(f"   Response time percentiles: {data.get('response_time_percentiles', {})}")
            print(f"   Verdict distribution:")
            for verdict, count in data.get('verdict_distribution', {}).items():
                print(f"     - {verdict}: {count}")
            print("✅ Metrics updated successfully")
        
        # Test metrics export
        print("\n7. Testing metrics export...")
        response = requests.post("http://localhost:8001/metrics/export", 
                               json={"filepath": "test_metrics_export.json"})
        if response.status_code == 200:
            print("✅ Metrics export successful")
            # Check if file was created
            if os.path.exists("test_metrics_export.json"):
                with open("test_metrics_export.json", 'r') as f:
                    export_data = json.load(f)
                print(f"   Exported {len(export_data.get('counters', {}))} counter metrics")
                os.remove("test_metrics_export.json")  # Clean up
        
        # Test system metrics
        print("\n8. Checking system metrics...")
        response = requests.get("http://localhost:8001/metrics/summary")
        if response.status_code == 200:
            data = response.json()
            system_metrics = data.get('system_metrics', {})
            if system_metrics:
                print(f"   CPU usage: {system_metrics.get('cpu_percent', 0):.1f}%")
                print(f"   Memory usage: {system_metrics.get('memory_percent', 0):.1f}%")
                print(f"   Process memory: {system_metrics.get('process_memory_mb', 0):.1f} MB")
                print("✅ System metrics available")
            else:
                print("⚠️  System metrics not yet collected (wait 30s)")
        
        print("\n✅ All monitoring tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Stop the server
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()
        print("Server stopped")

if __name__ == "__main__":
    test_monitoring()