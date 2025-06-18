#!/usr/bin/env python3
"""
Quick test for competitor analysis endpoint
"""

import requests
import json

BASE_URL = "http://localhost:8001"

SAMPLE_STARTUP_DATA = {
    "company_name": "TestStartup AI",
    "funding_stage": "seed",
    "sector": "saas",
    "annual_revenue_run_rate": 750000,
    "product_description": "AI-powered analytics platform",
    "target_market": "B2B SaaS companies"
}

def test_competitor_analysis():
    """Test competitor analysis endpoint"""
    url = f"{BASE_URL}/api/analysis/competitors/analyze"
    
    try:
        response = requests.post(
            url,
            json={
                "startup_data": SAMPLE_STARTUP_DATA,
                "top_n": 5
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nResponse Type: {data.get('type', 'unknown')}")
            print(f"Competitors Found: {len(data.get('competitors', []))}")
            
            for i, comp in enumerate(data.get('competitors', [])[:3]):
                print(f"\nCompetitor {i+1}:")
                print(f"  Name: {comp.get('name', 'N/A')}")
                print(f"  Description: {comp.get('description', 'N/A')[:100]}...")
                print(f"  Stage: {comp.get('stage', 'N/A')}")
                print(f"  Strengths: {comp.get('strengths', [])}")
                print(f"  Weaknesses: {comp.get('weaknesses', [])}")
                
            print(f"\nFull Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing competitor analysis: {e}")

if __name__ == "__main__":
    print("Testing Competitor Analysis Endpoint...")
    print("-" * 50)
    test_competitor_analysis()