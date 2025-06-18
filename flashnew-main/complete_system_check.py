#!/usr/bin/env python3
"""
Complete system check for FLASH
"""

import subprocess
import requests
import json
import os
from datetime import datetime

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def check_process(name):
    """Check if process is running"""
    result = run_command(f"ps aux | grep {name} | grep -v grep")
    return bool(result)

def check_port(port):
    """Check if port is in use"""
    result = run_command(f"lsof -i :{port} | grep LISTEN")
    return bool(result)

def check_api_endpoint(url, headers=None):
    """Check if API endpoint is accessible"""
    try:
        response = requests.get(url, headers=headers, timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔍 FLASH Complete System Check")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. Check processes
    print("\n📋 Process Status:")
    processes = {
        "API Server": check_process("api_server"),
        "Python (API)": check_process("python3.*8001"),
        "React Dev Server": check_process("react-scripts"),
        "Node.js": check_process("node")
    }
    
    for name, status in processes.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {name}: {'Running' if status else 'Not Running'}")
    
    # 2. Check ports
    print("\n🔌 Port Status:")
    ports = {
        "3000 (Frontend)": check_port(3000),
        "8001 (API)": check_port(8001)
    }
    
    for name, status in ports.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} Port {name}: {'In Use' if status else 'Free'}")
    
    # 3. Check API endpoints
    print("\n🌐 API Endpoints:")
    api_base = "http://localhost:8001"
    headers = {"X-API-Key": "test-api-key-123"}
    
    endpoints = {
        "Health": f"{api_base}/health",
        "Features": f"{api_base}/features",
        "Config": f"{api_base}/config/all"
    }
    
    for name, url in endpoints.items():
        auth_required = name != "Health"
        status = check_api_endpoint(url, headers if auth_required else None)
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {name}: {url}")
    
    # 4. Check file system
    print("\n📁 File System:")
    important_files = {
        "API Server": "api_server_complete.py",
        "Frontend Config": "flash-frontend/src/config.ts",
        "Config Service": "flash-frontend/src/services/configService.ts",
        "Environment": "flash-frontend/.env",
        "Package.json": "flash-frontend/package.json"
    }
    
    for name, path in important_files.items():
        exists = os.path.exists(path)
        status_icon = "✅" if exists else "❌"
        print(f"  {status_icon} {name}: {path}")
    
    # 5. Check models
    print("\n🤖 ML Models:")
    model_dir = "models/production_v45"
    if os.path.exists(model_dir):
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.pkl')]
        print(f"  ✅ Found {len(model_files)} model files in {model_dir}")
    else:
        print(f"  ❌ Model directory not found: {model_dir}")
    
    # 6. Check databases
    print("\n💾 Databases:")
    db_files = {
        "Main DB": "flash.db",
        "Config DB": "flash_config.db"
    }
    
    for name, path in db_files.items():
        exists = os.path.exists(path)
        status_icon = "✅" if exists else "❌"
        size = os.path.getsize(path) / 1024 if exists else 0
        print(f"  {status_icon} {name}: {path} ({size:.1f} KB)")
    
    # 7. Test prediction
    print("\n🎯 Test Prediction:")
    test_data = {
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 200000,
        "runway_months": 15,
        "burn_multiple": 2,
        "investor_tier_primary": "Tier 2",
        "has_debt": False,
        "patent_count": 3,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,
        "switching_cost_score": 3,
        "brand_strength_score": 3,
        "scalability_score": 4,
        "sector": "SaaS",
        "tam_size_usd": 5000000000,
        "sam_size_usd": 500000000,
        "som_size_usd": 50000000,
        "market_growth_rate_percent": 35,
        "customer_count": 100,
        "customer_concentration_percent": 20,
        "user_growth_rate_percent": 25,
        "net_dollar_retention_percent": 115,
        "competition_intensity": 3,
        "competitors_named_count": 15,
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 10,
        "domain_expertise_years_avg": 7,
        "prior_startup_experience_count": 2,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,
        "advisors_count": 5
    }
    
    try:
        response = requests.post(
            f"{api_base}/predict",
            headers={"Content-Type": "application/json", "X-API-Key": "test-api-key-123"},
            json=test_data
        )
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Prediction successful:")
            print(f"     Success Probability: {result.get('success_probability', 0):.1%}")
            print(f"     Verdict: {result.get('verdict', 'N/A')}")
        else:
            print(f"  ❌ Prediction failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Prediction error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    
    api_ok = ports.get("8001 (API)", False)
    frontend_ok = ports.get("3000 (Frontend)", False)
    
    if api_ok and frontend_ok:
        print("✅ System is fully operational!")
        print("\n🚀 Access the application at: http://localhost:3000")
    else:
        print("⚠️  Issues detected:")
        if not api_ok:
            print("  - API server not running on port 8001")
            print("    Run: ./start_complete_api.sh")
        if not frontend_ok:
            print("  - Frontend not running on port 3000")
            print("    Run: cd flash-frontend && npm start")

if __name__ == "__main__":
    main()