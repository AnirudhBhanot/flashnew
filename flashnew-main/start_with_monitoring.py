#!/usr/bin/env python3
"""
Start API server with monitoring enabled
"""

import subprocess
import sys
import time
import requests
import os
import signal

def test_monitoring():
    """Test if monitoring is working"""
    print("\n" + "="*60)
    print("Testing FLASH API with Monitoring")
    print("="*60)
    
    # Start API server
    print("\n1. Starting API server on port 8001...")
    api_process = subprocess.Popen(
        [sys.executable, "api_server.py", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        preexec_fn=os.setsid
    )
    
    # Wait for server to start
    print("   Waiting for server to start...")
    time.sleep(5)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✅ API server started successfully")
            print(f"   Health status: {response.json()}")
        else:
            print("❌ API server health check failed")
            return
    except Exception as e:
        print(f"❌ Failed to connect to API server: {e}")
        return
    
    print("\n2. Testing monitoring endpoints...")
    
    # Test metrics endpoint
    try:
        response = requests.get("http://localhost:8001/metrics")
        if response.status_code == 200:
            print("✅ Metrics endpoint working")
            metrics = response.json()
            print(f"   Request stats: {metrics.get('request_stats', {}).get('total_requests', 0)} requests")
            print(f"   System health: {metrics.get('system_health', {}).get('status', 'unknown')}")
        else:
            print("❌ Metrics endpoint failed")
    except Exception as e:
        print(f"❌ Metrics endpoint error: {e}")
    
    print("\n3. Making test predictions...")
    
    # Make some test predictions
    test_startup = {
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
    
    # Make multiple predictions
    for i in range(5):
        try:
            response = requests.post("http://localhost:8001/predict", json=test_startup)
            if response.status_code == 200:
                result = response.json()
                print(f"   Prediction {i+1}: {result['success_probability']:.2%}")
            else:
                print(f"   Prediction {i+1} failed: {response.status_code}")
        except Exception as e:
            print(f"   Prediction {i+1} error: {e}")
        time.sleep(0.5)
    
    print("\n4. Checking updated metrics...")
    
    # Check metrics again
    try:
        response = requests.get("http://localhost:8001/metrics")
        if response.status_code == 200:
            metrics = response.json()
            request_stats = metrics.get('request_stats', {})
            print(f"✅ Metrics updated:")
            print(f"   Total requests: {request_stats.get('total_requests', 0)}")
            print(f"   Success rate: {request_stats.get('success_rate', 0)*100:.1f}%")
            print(f"   Avg latency: {request_stats.get('avg_latency_ms', 0):.0f}ms")
            print(f"   P95 latency: {request_stats.get('p95_latency_ms', 0):.0f}ms")
    except Exception as e:
        print(f"❌ Failed to get updated metrics: {e}")
    
    print("\n5. Checking monitoring dashboard...")
    print("   Dashboard URL: http://localhost:8001/monitoring")
    print("   (Open in browser to view real-time monitoring)")
    
    print("\n6. Checking log files...")
    
    # Check if log files were created
    log_files = ['logs/flash.log', 'logs/flash_json.log', 'logs/api.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            print(f"✅ {log_file}: {size} bytes")
            
            # Show last few lines
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"   Last entry: {lines[-1].strip()[:100]}...")
            except:
                pass
        else:
            print(f"❌ {log_file}: Not found")
    
    print("\n" + "="*60)
    print("Monitoring Test Complete!")
    print("="*60)
    print("\nAPI Server is running with monitoring enabled.")
    print("Access points:")
    print("  - API: http://localhost:8001")
    print("  - Monitoring Dashboard: http://localhost:8001/monitoring")
    print("  - Metrics: http://localhost:8001/metrics")
    print("  - Health: http://localhost:8001/health")
    print("\nPress Ctrl+C to stop the server...")
    
    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down API server...")
        os.killpg(os.getpgid(api_process.pid), signal.SIGTERM)
        api_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    test_monitoring()