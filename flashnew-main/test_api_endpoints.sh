#!/bin/bash
# Test LLM API endpoints

echo "🔍 Testing LLM API Endpoints"
echo "=============================="

# Base URL
BASE_URL="http://localhost:8001/api/analysis"

# Test 1: Check status
echo -e "\n1. Testing LLM Status Endpoint..."
curl -s "${BASE_URL}/status" | python3 -m json.tool

# Test 2: Test recommendations
echo -e "\n\n2. Testing Dynamic Recommendations..."
curl -s -X POST "${BASE_URL}/recommendations/dynamic" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {
      "funding_stage": "Seed",
      "sector": "FinTech",
      "annual_revenue_run_rate": 500000,
      "revenue_growth_rate_percent": 200,
      "monthly_burn_usd": 100000,
      "runway_months": 18,
      "team_size_full_time": 10,
      "customer_count": 20
    },
    "scores": {
      "capital": 0.45,
      "advantage": 0.50,
      "market": 0.60,
      "people": 0.45,
      "success_probability": 0.48
    }
  }' | python3 -m json.tool

# Test 3: Test what-if analysis
echo -e "\n\n3. Testing What-If Analysis..."
curl -s -X POST "${BASE_URL}/whatif/dynamic" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {
      "funding_stage": "Pre-seed",
      "sector": "E-commerce",
      "annual_revenue_run_rate": 100000
    },
    "current_scores": {
      "capital": 0.3,
      "advantage": 0.4,
      "market": 0.5,
      "people": 0.35,
      "success_probability": 0.38
    },
    "improvements": [
      {"id": "hire_tech_lead", "description": "Hire senior tech lead"},
      {"id": "increase_revenue", "description": "Double monthly revenue"}
    ]
  }' | python3 -m json.tool

echo -e "\n\n✅ API endpoint tests complete!"