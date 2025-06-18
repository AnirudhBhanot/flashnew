#!/bin/bash

echo "🔧 Fixing Frontend Connection Issues"
echo "===================================="

# Step 1: Check if frontend is running
FRONTEND_PID=$(lsof -t -i:3000)
if [ ! -z "$FRONTEND_PID" ]; then
    echo "✅ Frontend is running on port 3000 (PID: $FRONTEND_PID)"
else
    echo "❌ Frontend is not running"
    echo "   Please start it with: cd flash-frontend && npm start"
fi

# Step 2: Check if API is running
API_PID=$(lsof -t -i:8001)
if [ ! -z "$API_PID" ]; then
    echo "✅ API server is running on port 8001 (PID: $API_PID)"
else
    echo "❌ API server is not running"
    echo "   Please start it with: python3 api_server_unified.py"
fi

# Step 3: Test API endpoints
echo ""
echo "Testing API endpoints..."

# Test health endpoint
echo -n "Testing /health endpoint: "
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health)
if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ OK"
else
    echo "❌ Failed (HTTP $HEALTH_RESPONSE)"
fi

# Test config endpoint
echo -n "Testing /config/stage-weights endpoint: "
CONFIG_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/config/stage-weights)
if [ "$CONFIG_RESPONSE" = "200" ]; then
    echo "✅ OK"
else
    echo "❌ Failed (HTTP $CONFIG_RESPONSE)"
fi

# Test CORS preflight
echo -n "Testing CORS preflight: "
CORS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Origin: http://localhost:3000" \
    -H "Access-Control-Request-Method: POST" \
    -H "Access-Control-Request-Headers: Content-Type" \
    -X OPTIONS \
    http://localhost:8001/predict)
if [ "$CORS_RESPONSE" = "200" ]; then
    echo "✅ OK"
else
    echo "❌ Failed (HTTP $CORS_RESPONSE)"
fi

echo ""
echo "📝 Summary:"
echo "- Frontend config updated to use port 8001"
echo "- API has config endpoints on port 8001"
echo "- CORS should allow localhost:3000"
echo ""
echo "🔄 Please refresh your browser to load the updated configuration"