#!/bin/bash
# Build script for Render

echo "Starting Render build..."

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p models

echo "Build complete!"