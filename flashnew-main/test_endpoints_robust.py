#!/usr/bin/env python3
"""
Robust test script for API endpoints with better error handling
"""

import requests
import json
import sys
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8001"

def print_test_header(test_name: str):
    """Print a formatted test header"""
    print(f"\n{'=' * 60}")
    print(f"  {test_name}")
    print(f"{'=' * 60}")

def print_result(success: bool, message: str):
    """Print test result with emoji"""
    emoji = "✅" if success else "❌"
    print(f"{emoji} {message}")

def make_request(method: str, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> tuple:
    """Make HTTP request with error handling"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.status_code, response.text, response.headers
    except requests.ConnectionError:
        return 0, "Connection refused - is the server running?", {}
    except Exception as e:
        return -1, str(e), {}

def test_server_health():
    """Test if server is running"""
    print_test_header("Server Health Check")
    
    status, content, _ = make_request("GET", "/health")
    if status == 200:
        print_result(True, f"Server is running (status: {status})")
        return True
    else:
        print_result(False, f"Server not accessible: {content}")
        return False

def test_framework_endpoints():
    """Test Framework Intelligence endpoints"""
    print_test_header("Framework Intelligence Endpoints")
    
    # Test 1: Categories endpoint
    print("\n1. Testing GET /api/frameworks/categories")
    status, content, _ = make_request("GET", "/api/frameworks/categories")
    if status == 200:
        try:
            data = json.loads(content)
            categories_count = len(data.get("categories", {}))
            total_frameworks = data.get("total_frameworks", 0)
            print_result(True, f"Categories endpoint working - {categories_count} categories, {total_frameworks} frameworks")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")
    
    # Test 2: Recommendation endpoint
    print("\n2. Testing POST /api/frameworks/recommend")
    request_data = {
        "company_stage": "mvp",
        "industry": "saas",
        "primary_challenge": "customer_acquisition",
        "team_size": 10,
        "resources": "limited",
        "timeline": "3 months",
        "goals": ["increase revenue", "improve retention"],
        "current_frameworks": []
    }
    
    status, content, _ = make_request("POST", "/api/frameworks/recommend", data=request_data)
    if status == 200:
        try:
            data = json.loads(content)
            recommendations = data.get("recommendations", [])
            print_result(True, f"Recommendations working - {len(recommendations)} frameworks recommended")
            if recommendations:
                print(f"   Top recommendation: {recommendations[0].get('framework_name', 'Unknown')}")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    elif status == 422:
        print_result(False, f"Validation error: {content}")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")
    
    # Test 3: Search endpoint
    print("\n3. Testing GET /api/frameworks/search")
    status, content, _ = make_request("GET", "/api/frameworks/search?query=swot")
    if status == 200:
        try:
            data = json.loads(content)
            results = data.get("results", [])
            print_result(True, f"Search working - {len(results)} results for 'swot'")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")

def test_deepdive_endpoints():
    """Test Progressive Deep Dive endpoints"""
    print_test_header("Progressive Deep Dive Endpoints")
    
    # Test 1: Phase 1 - Competitive Analysis
    print("\n1. Testing POST /api/analysis/deepdive/phase1/analysis")
    phase1_data = {
        "porters_five_forces": {
            "supplier_power": {"rating": "Medium", "factors": ["Limited suppliers"], "score": 6.5},
            "buyer_power": {"rating": "High", "factors": ["Many alternatives"], "score": 7.8},
            "competitive_rivalry": {"rating": "High", "factors": ["Many competitors"], "score": 8.2},
            "threat_of_substitution": {"rating": "Medium", "factors": ["Some alternatives"], "score": 5.5},
            "threat_of_new_entry": {"rating": "Low", "factors": ["High barriers"], "score": 3.2}
        },
        "internal_audit": {
            "strengths": ["Strong tech team", "Innovative product"],
            "weaknesses": ["Limited marketing", "Cash constraints"],
            "opportunities": ["Growing market", "Partnerships"],
            "threats": ["Economic uncertainty", "Regulation"]
        }
    }
    
    status, content, headers = make_request("POST", "/api/analysis/deepdive/phase1/analysis", data=phase1_data)
    if status == 200:
        try:
            data = json.loads(content)
            print_result(True, "Phase 1 analysis working")
            if "competitive_position" in data:
                print(f"   Competitive position analyzed")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    elif status == 404:
        print_result(False, "Endpoint not found - check if deep dive routes are registered")
    elif status == 405:
        print_result(False, "Method not allowed - endpoint may not be properly configured")
    elif status == 422:
        print_result(False, f"Validation error: {content}")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")
    
    # Test 2: Phase 2 - Vision-Reality Analysis
    print("\n2. Testing POST /api/analysis/deepdive/phase2/vision-reality")
    phase2_data = {
        "vision_statement": "To become the leading SaaS platform by 2027",
        "current_reality": {
            "market_share": "5%",
            "revenue": "$10M ARR",
            "customer_base": "50 clients"
        },
        "ansoff_matrix_position": "market_penetration"
    }
    
    status, content, _ = make_request("POST", "/api/analysis/deepdive/phase2/vision-reality", data=phase2_data)
    if status == 200:
        try:
            data = json.loads(content)
            print_result(True, "Phase 2 analysis working")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    elif status == 404:
        print_result(False, "Endpoint not found")
    elif status == 405:
        print_result(False, "Method not allowed")
    elif status == 422:
        print_result(False, f"Validation error: {content}")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")
    
    # Test 3: Check LLM status
    print("\n3. Testing GET /api/analysis/status")
    status, content, _ = make_request("GET", "/api/analysis/status")
    if status == 200:
        try:
            data = json.loads(content)
            llm_status = data.get("status", "unknown")
            print_result(True, f"LLM status endpoint working - Status: {llm_status}")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")

def test_standard_llm_endpoints():
    """Test standard LLM endpoints"""
    print_test_header("Standard LLM Endpoints")
    
    # Test dynamic recommendations
    print("\n1. Testing POST /api/analysis/recommendations/dynamic")
    rec_data = {
        "startup_data": {
            "funding_stage": "Seed",
            "sector": "SaaS",
            "annual_revenue_run_rate": 1000000
        },
        "scores": {
            "capital": 0.6,
            "advantage": 0.7,
            "market": 0.8,
            "people": 0.65,
            "success_probability": 0.7
        }
    }
    
    status, content, _ = make_request("POST", "/api/analysis/recommendations/dynamic", data=rec_data)
    if status == 200:
        try:
            data = json.loads(content)
            print_result(True, "Dynamic recommendations working")
        except json.JSONDecodeError:
            print_result(False, f"Invalid JSON response: {content[:100]}...")
    else:
        print_result(False, f"Status {status}: {content[:100]}...")

def main():
    """Main test function"""
    print("\n" + "="*60)
    print("  API Endpoint Test Suite")
    print("="*60)
    print(f"\nTesting server at: {BASE_URL}")
    
    # Check if server is running
    if not test_server_health():
        print("\n⚠️  Server is not running. Please start it with:")
        print("   ./start_fixed_system.sh")
        sys.exit(1)
    
    # Run all tests
    test_framework_endpoints()
    test_deepdive_endpoints()
    test_standard_llm_endpoints()
    
    print("\n" + "="*60)
    print("  Testing Complete")
    print("="*60)

if __name__ == "__main__":
    main()