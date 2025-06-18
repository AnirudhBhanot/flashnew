#!/bin/bash
# Production startup script for FLASH Platform

echo "🚀 Starting FLASH Platform in Production Mode"
echo "==========================================="

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs -0)
    echo "✅ Environment variables loaded"
else
    echo "❌ .env file not found!"
    echo "   Run ./setup_environment.sh first"
    exit 1
fi

# Check required services
echo ""
echo "🔍 Checking required services..."

# Check Redis
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis not running - caching will be disabled"
    echo "   Start with: brew services start redis (macOS)"
fi

# Check PostgreSQL (optional, using SQLite as fallback)
pg_isready > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL is running"
else
    echo "ℹ️  PostgreSQL not running - using SQLite"
fi

# Verify model checksums
echo ""
echo "🔐 Verifying model integrity..."
python3 -c "
from utils.model_integrity import verify_production_models
if verify_production_models():
    print('✅ All model checksums verified')
else:
    print('❌ Model integrity check failed!')
    exit(1)
"

# Create required directories
mkdir -p logs data

# Start the server
echo ""
echo "🚀 Starting FLASH API Server..."
echo "================================"
echo "Host: ${HOST:-0.0.0.0}"
echo "Port: ${PORT:-8001}"
echo "Workers: ${WORKERS:-4}"
echo "Log Level: ${LOG_LEVEL:-INFO}"
echo ""

# Use gunicorn for production with uvicorn workers
if command -v gunicorn &> /dev/null; then
    echo "Using Gunicorn with Uvicorn workers..."
    exec gunicorn api_server_unified:app \
        --workers ${WORKERS:-4} \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind ${HOST:-0.0.0.0}:${PORT:-8001} \
        --access-logfile logs/access.log \
        --error-logfile logs/error.log \
        --log-level ${LOG_LEVEL:-info} \
        --timeout 120 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 50
else
    echo "Gunicorn not found, using Uvicorn directly..."
    exec python3 -m uvicorn api_server_unified:app \
        --host ${HOST:-0.0.0.0} \
        --port ${PORT:-8001} \
        --workers ${WORKERS:-1} \
        --log-level ${LOG_LEVEL:-info} \
        --access-log
fi