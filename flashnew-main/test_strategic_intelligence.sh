#!/bin/bash

echo "=== Strategic Intelligence Integration Test ==="
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base URL
API_URL="http://localhost:8001"

# Test data
TEST_DATA='{
  "total_capital_raised_usd": 2000000,
  "cash_on_hand_usd": 800000,
  "monthly_burn_usd": 75000,
  "runway_months": 11,
  "funding_stage": "seed",
  "investor_tier_primary": "tier_2",
  "product_stage": "mvp",
  "proprietary_tech": true,
  "patents_filed": 2,
  "monthly_active_users": 2500,
  "market_size_usd": 5000000000,
  "market_growth_rate_annual": 35,
  "competitor_count": 8,
  "market_share_percentage": 1.5,
  "team_size_full_time": 12,
  "founders_industry_experience_years": 8,
  "b2b_or_b2c": "b2b",
  "sector": "saas",
  "startup_name": "StrategicTest Inc"
}'

echo "1. Testing Framework Recommendation Endpoint..."
FRAMEWORK_RESPONSE=$(curl -s -X POST ${API_URL}/api/frameworks/recommend-for-startup \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

if [ $? -eq 0 ]; then
  FRAMEWORK_COUNT=$(echo "$FRAMEWORK_RESPONSE" | jq -r '.total_frameworks_available')
  RECOMMENDATION_COUNT=$(echo "$FRAMEWORK_RESPONSE" | jq -r '.frameworks | length')
  
  if [ "$FRAMEWORK_COUNT" = "554" ]; then
    echo -e "${GREEN}✓ Framework count correct: 554${NC}"
  else
    echo -e "${RED}✗ Framework count incorrect: $FRAMEWORK_COUNT${NC}"
  fi
  
  if [ "$RECOMMENDATION_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Received $RECOMMENDATION_COUNT framework recommendations${NC}"
    echo "  Top framework: $(echo "$FRAMEWORK_RESPONSE" | jq -r '.frameworks[0].framework_name')"
    echo "  Score: $(echo "$FRAMEWORK_RESPONSE" | jq -r '.frameworks[0].score')"
  else
    echo -e "${RED}✗ No framework recommendations received${NC}"
  fi
else
  echo -e "${RED}✗ Framework recommendation endpoint failed${NC}"
fi

echo
echo "2. Testing Roadmap Generation Endpoint..."
ROADMAP_DATA="{
  \"startup_data\": $TEST_DATA,
  \"selected_option\": \"vertical-focus\"
}"
ROADMAP_RESPONSE=$(curl -s -X POST ${API_URL}/api/frameworks/roadmap-for-startup \
  -H "Content-Type: application/json" \
  -d "$ROADMAP_DATA")

if [ $? -eq 0 ]; then
  PHASE_COUNT=$(echo "$ROADMAP_RESPONSE" | jq -r '.roadmap | length' 2>/dev/null || echo "0")
  
  if [ "$PHASE_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Received $PHASE_COUNT roadmap phases${NC}"
    echo "  Phase 1: $(echo "$ROADMAP_RESPONSE" | jq -r '.roadmap[0].title' 2>/dev/null || echo "N/A")"
  else
    echo -e "${RED}✗ No roadmap phases received${NC}"
  fi
else
  echo -e "${RED}✗ Roadmap generation endpoint failed${NC}"
fi

echo
echo "3. Testing Prediction Endpoint (for CAMP scores)..."
PREDICT_RESPONSE=$(curl -s -X POST ${API_URL}/predict \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

if [ $? -eq 0 ]; then
  SUCCESS_PROB=$(echo "$PREDICT_RESPONSE" | jq -r '.success_probability')
  CAPITAL_SCORE=$(echo "$PREDICT_RESPONSE" | jq -r '.camp_scores.capital')
  
  echo -e "${GREEN}✓ Prediction successful${NC}"
  echo "  Success probability: $(echo "scale=2; $SUCCESS_PROB * 100" | bc)%"
  echo "  CAMP scores available: $(echo "$PREDICT_RESPONSE" | jq -r '.camp_scores | keys | join(", ")')"
else
  echo -e "${RED}✗ Prediction endpoint failed${NC}"
fi

echo
echo "4. Checking API Health..."
HEALTH_RESPONSE=$(curl -s ${API_URL}/health)
MODELS_LOADED=$(echo "$HEALTH_RESPONSE" | jq -r '.models_loaded')

if [ "$MODELS_LOADED" -eq 4 ]; then
  echo -e "${GREEN}✓ All 4 models loaded successfully${NC}"
else
  echo -e "${RED}✗ Only $MODELS_LOADED models loaded${NC}"
fi

echo
echo "5. Testing Frontend Integration..."
if curl -s http://localhost:3000 | grep -q "FLASH"; then
  echo -e "${GREEN}✓ Frontend is running${NC}"
else
  echo -e "${RED}✗ Frontend not accessible${NC}"
fi

echo
echo "=== Test Summary ==="
echo "Strategic Intelligence integration includes:"
echo "- 554 business frameworks available"
echo "- AI-powered framework recommendations"
echo "- Implementation roadmap generation"
echo "- Pattern-based competitor analysis"
echo "- Michelin-style strategic report"
echo
echo "To see the full experience:"
echo "1. Go to http://localhost:3000"
echo "2. Complete an assessment (or use autofill)"
echo "3. View results page"
echo "4. Expand 'Strategic Intelligence' section"