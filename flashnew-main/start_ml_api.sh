#!/bin/bash
# Start FLASH API with complete ML infrastructure

echo "Starting FLASH ML API Server..."

# Ensure all systems are initialized
python3 setup_model_integrity.py
echo "✓ Model integrity system ready"

# Start the API server
python3 api_server_ml_complete.py
