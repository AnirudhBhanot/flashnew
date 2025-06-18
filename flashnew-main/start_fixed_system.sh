#!/bin/bash
# FLASH Fixed System Startup Script

echo "Starting FLASH Fixed System..."
echo "=============================="

# Clean any Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Start the fixed API server
echo ""
echo "Starting API server on port 8001..."
python3 api_server_fixed.py &
API_PID=$!

# Wait for server to start
sleep 3

# Test the server
echo ""
echo "Testing server health..."
curl -s http://localhost:8001/health | python3 -m json.tool

echo ""
echo "=============================="
echo "FLASH Fixed System is running!"
echo "API Server PID: $API_PID"
echo ""
echo "To stop the server, run:"
echo "kill $API_PID"
echo ""
echo "To run tests:"
echo "python3 test_fixed_system_integration.py"
