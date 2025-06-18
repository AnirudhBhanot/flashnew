#!/usr/bin/env python3
"""
Test script to verify Deep Dive and Framework Intelligence endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_framework_endpoints():
    """Test Framework Intelligence endpoints"""
    print("\n=== Testing Framework Intelligence Endpoints ===")
    
    # Test recommendation endpoint
    print("\n1. Testing /api/frameworks/recommend")
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
    
    try:
        response = requests.post(f"{BASE_URL}/api/frameworks/recommend", json=request_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Framework recommendations working")
            print(f"Recommendations: {len(response.json().get('recommendations', []))}")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test roadmap endpoint
    print("\n2. Testing /api/frameworks/roadmap")
    try:
        response = requests.post(f"{BASE_URL}/api/frameworks/roadmap", json=request_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Framework roadmap working")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")

def test_deepdive_endpoints():
    """Test Progressive Deep Dive endpoints"""
    print("\n=== Testing Progressive Deep Dive Endpoints ===")
    
    # Test Phase 1
    print("\n1. Testing Phase 1 - Competitive Analysis")
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
    
    try:
        response = requests.post(f"{BASE_URL}/api/analysis/deepdive/phase1/analysis", json=phase1_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Phase 1 analysis working")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    # Test Phase 2
    print("\n2. Testing Phase 2 - Vision-Reality Analysis")
    phase2_data = {
        "vision_statement": "To become the leading SaaS platform by 2027",
        "current_reality": {
            "market_share": "5%",
            "revenue": "$10M ARR",
            "customer_base": "50 clients"
        },
        "ansoff_matrix_position": "market_penetration"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/analysis/deepdive/phase2/vision-reality", json=phase2_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Phase 2 analysis working")
        else:
            print(f"✗ Error: {response.text}")
    except Exception as e:
        print(f"✗ Request failed: {e}")

if __name__ == "__main__":
    print("Testing API Endpoints...")
    print("Make sure the API server is running on http://localhost:8000")
    print("=" * 50)
    
    # Wait for user confirmation
    input("Press Enter to start tests...")
    
    test_framework_endpoints()
    test_deepdive_endpoints()
    
    print("\n" + "=" * 50)
    print("Testing completed!")
