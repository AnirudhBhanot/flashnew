#!/bin/bash

echo "🔧 Restarting API with CORS Fix"
echo "================================"

# Step 1: Kill the current API server
API_PID=$(lsof -t -i:8001)
if [ ! -z "$API_PID" ]; then
    echo "Stopping current API server (PID: $API_PID)..."
    kill $API_PID
    sleep 2
fi

# Step 2: Create a temporary API server with fixed CORS
cat > api_server_cors_fixed.py << 'EOF'
#!/usr/bin/env python3
"""
Temporary API server with CORS fully open for development
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from api_server_unified import *
from fastapi.middleware.cors import CORSMiddleware

# Remove existing CORS middleware
for i, middleware in enumerate(app.user_middleware):
    if middleware.cls == CORSMiddleware:
        app.user_middleware.pop(i)
        break

# Add completely open CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
    max_age=3600,
)

print("⚠️  WARNING: CORS is fully open - development only!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
EOF

# Step 3: Start the fixed API server
echo ""
echo "Starting API server with open CORS..."
python3 api_server_cors_fixed.py &

echo ""
echo "✅ API server restarted with CORS fix"
echo "🔄 Please refresh your browser to test"
echo ""
echo "⚠️  Note: This has CORS fully open for development"
echo "   Do not use in production!"