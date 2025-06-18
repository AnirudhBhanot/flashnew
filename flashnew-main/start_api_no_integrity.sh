#!/bin/bash
# Start FLASH API server with integrity checks disabled

echo "Starting FLASH API server with integrity checks disabled..."
echo "=================================================="

# Set environment variable to skip integrity checks
export FLASH_SKIP_INTEGRITY_CHECK=true

# Start the API server
python api_server_unified.py