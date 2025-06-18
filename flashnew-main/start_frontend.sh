#!/bin/bash
# Start the frontend server

echo "🚀 Starting FLASH Frontend..."
echo "================================"

# Check if API server is running
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ API server is running on port 8001"
else
    echo "⚠️  API server not running! Starting it..."
    cd /Users/sf/Desktop/FLASH
    DISABLE_AUTH=true python3 api_server_unified.py > api_server.log 2>&1 &
    sleep 3
fi

# Start frontend
cd /Users/sf/Desktop/FLASH/flash-frontend
echo "📦 Installing dependencies..."
npm install

echo "🌐 Starting frontend on http://localhost:3000"
npm start