#!/usr/bin/env python3
"""
Temporarily disable authentication for development
Run this to start API without auth requirements
"""

import os
import sys

# Set environment variable to disable auth
os.environ['DISABLE_AUTH'] = 'true'

# Import and run the API server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_server_unified import app
import uvicorn

print("🚀 Starting API server with authentication DISABLED")
print("⚠️  WARNING: This is for development only!")
print("=" * 50)

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )