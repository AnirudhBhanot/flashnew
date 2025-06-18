#!/bin/bash
# Start FLASH Platform - API and Frontend

echo "🚀 Starting FLASH Platform"
echo "=========================="

# Function to check if port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "api_server_unified_final" 2>/dev/null
pkill -f "npm.*start" 2>/dev/null
sleep 2

# Start API server
echo "📡 Starting API server on port 8001..."
cd /Users/sf/Desktop/FLASH
DISABLE_AUTH=true python3 api_server_unified_final.py > api_server.log 2>&1 &
API_PID=$!

# Wait for API to start
echo "⏳ Waiting for API to start..."
for i in {1..10}; do
    if curl -s http://localhost:8001/health > /dev/null; then
        echo "✅ API server is running!"
        break
    fi
    sleep 1
done

# Start frontend
echo "🎨 Starting frontend on port 3000..."
cd /Users/sf/Desktop/FLASH/flash-frontend
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo ""
echo "✅ FLASH Platform Started!"
echo "=========================="
echo "📡 API Server: http://localhost:8001"
echo "🎨 Frontend: http://localhost:3000"
echo ""
echo "📝 Logs:"
echo "   API: /Users/sf/Desktop/FLASH/api_server.log"
echo "   Frontend: /Users/sf/Desktop/FLASH/frontend.log"
echo ""
echo "🛑 To stop: pkill -f 'api_server_unified_final' && pkill -f 'npm.*start'"
echo ""
echo "📊 Test the API:"
echo "   curl http://localhost:8001/health | jq ."
echo ""