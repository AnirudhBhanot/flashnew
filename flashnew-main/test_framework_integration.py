#!/usr/bin/env python3
"""Test framework API integration"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import routers
from api_framework_endpoints import framework_router
from api_framework_analysis import analysis_router

# Create test app
app = FastAPI()
app.include_router(framework_router)
app.include_router(analysis_router)

# Create test client
client = TestClient(app)

# Test framework analysis endpoint
test_data = {
    "startup_data": {
        "startup_name": "TestStartup AI",
        "total_capital_raised_usd": 2000000,
        "market_growth_rate_annual": 25,
        "market_share_percentage": 0.5,
        "funding_stage": "seed",
        "sector": "saas"
    },
    "framework_ids": ["bcg_matrix", "swot_analysis"]
}

# Make test request
response = client.post("/api/frameworks/analyze", json=test_data)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("✅ Framework analysis endpoint is working!")
    result = response.json()
    print(f"Analyzed {len(result['analyses'])} frameworks")
    for analysis in result['analyses']:
        print(f"- {analysis['framework_name']}: {analysis['position']}")
else:
    print("❌ Framework analysis endpoint failed!")
    print(f"Error: {response.text}")