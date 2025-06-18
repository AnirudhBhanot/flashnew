#!/bin/bash
# Start FLASH API server in development mode with all fixes

echo "🚀 Starting FLASH API Server (Development Mode)"
echo "=============================================="
echo "✅ Integrity checks: DISABLED"
echo "✅ Authentication: DISABLED"
echo "✅ Models: 45-feature compatible"
echo ""

# Set environment variables
export ENVIRONMENT=development
export DISABLE_AUTH=true
export FLASH_SKIP_INTEGRITY_CHECK=true

# Start the server
cd /Users/sf/Desktop/FLASH
python3 api_server_unified.py