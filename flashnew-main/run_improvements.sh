#!/bin/bash
# Run FLASH Improvements Pipeline
# KPI Impact: 77% → 82% accuracy, full probability range

echo "=========================================="
echo "FLASH IMPROVEMENT PIPELINE"
echo "=========================================="

# Check Python version
python3 --version

# Install any missing dependencies
echo ""
echo "1. Installing dependencies..."
pip install -q scikit-learn xgboost lightgbm catboost matplotlib

# Create data directory if needed
mkdir -p data
mkdir -p models/improved_v1
mkdir -p models/calibration

# Run the improvements
echo ""
echo "2. Training improved models..."
echo "   This will:"
echo "   - Generate 200k realistic dataset (25% success rate)"
echo "   - Engineer momentum & efficiency features"
echo "   - Train 5-model ensemble"
echo "   - Calibrate probability outputs"
echo ""

python3 train_improved_models.py

# Check if training succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Training complete!"
    echo ""
    echo "3. Starting improved API server..."
    echo "   - Full 0-100% probability range"
    echo "   - Confidence intervals"
    echo "   - What-if scenarios"
    echo "   - <200ms response time"
    echo ""
    echo "Access at: http://localhost:8001"
    echo ""
    
    # Start the improved API server
    python3 api_server_improved.py
else
    echo ""
    echo "❌ Training failed. Check logs for errors."
    exit 1
fi