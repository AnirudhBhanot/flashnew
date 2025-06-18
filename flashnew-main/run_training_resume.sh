#!/bin/bash
#
# Resume production training with optimized parameters
# Estimated time: 30-45 minutes (much faster than original)
#

echo "=========================================="
echo "RESUMING PRODUCTION MODEL TRAINING"
echo "=========================================="
echo ""
echo "Using optimized parameters for faster training"
echo "Estimated time: 30-45 minutes"
echo ""

# Create logs directory
mkdir -p training_logs

# Set log file with timestamp
LOG_FILE="training_logs/training_resume_$(date +%Y%m%d_%H%M%S).log"
PID_FILE="training_logs/training.pid"

echo "Starting optimized training process..."
echo "Log file: $LOG_FILE"
echo ""

# Run training in background
nohup python3 train_production_resume.py > "$LOG_FILE" 2>&1 &

# Capture PID
TRAINING_PID=$!
echo $TRAINING_PID > "$PID_FILE"

echo "Training started with PID: $TRAINING_PID"
echo ""
echo "To monitor progress:"
echo "  tail -f $LOG_FILE"
echo ""
echo "To check if training is still running:"
echo "  ps -p $TRAINING_PID"
echo ""
echo "To stop training:"
echo "  kill $TRAINING_PID"
echo ""

# Monitor for a few seconds
echo "Checking that training started successfully..."
sleep 5

if ps -p $TRAINING_PID > /dev/null; then
    echo "✅ Training is running successfully!"
    echo ""
    echo "First few lines of output:"
    echo "---"
    head -20 "$LOG_FILE"
    echo "---"
    echo ""
    echo "The optimized training will complete in 30-45 minutes."
else
    echo "❌ Training failed to start!"
    echo "Check the log file for errors:"
    echo "  cat $LOG_FILE"
    exit 1
fi