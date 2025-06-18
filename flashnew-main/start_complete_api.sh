#!/bin/bash

echo "🚀 Starting Complete FLASH API Server"
echo "===================================="

# Stop any existing API servers
echo "Stopping existing servers..."
for port in 8001 8002; do
    PID=$(lsof -t -i:$port)
    if [ ! -z "$PID" ]; then
        echo "  Stopping server on port $port (PID: $PID)"
        kill $PID
        sleep 1
    fi
done

# Clear old logs
echo "Clearing old logs..."
rm -f api_server*.log

# Start the complete API server
echo ""
echo "Starting complete API server..."
echo "  Port: 8001"
echo "  Authentication: API Key required"
echo "  CORS: Configured for localhost:3000"
echo ""

# Export environment variables
export JWT_SECRET="flash-secret-key-change-in-production"
export ALLOWED_ORIGINS="http://localhost:3000,http://localhost:3001"

# Start server
python3 api_server_complete.py

# Note: The script will stay running with the server
# Press Ctrl+C to stop