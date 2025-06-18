#!/bin/bash
#
# Run production-grade training in background with monitoring
# This script will:
# 1. Start training in background
# 2. Monitor progress via log file
# 3. Send notification when complete (if possible)
#

echo "=========================================="
echo "PRODUCTION-GRADE MODEL TRAINING LAUNCHER"
echo "=========================================="
echo ""
echo "This training will take 1-2 hours to complete."
echo "The process will run in the background."
echo ""

# Create logs directory
mkdir -p training_logs

# Set log file with timestamp
LOG_FILE="training_logs/training_$(date +%Y%m%d_%H%M%S).log"
PID_FILE="training_logs/training.pid"

echo "Starting training process..."
echo "Log file: $LOG_FILE"
echo ""

# Run training in background, capturing all output
nohup python3 train_production_grade.py > "$LOG_FILE" 2>&1 &

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

# Optional: Monitor progress for a few seconds to ensure it started
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
    echo "The training will continue in the background."
    echo "Check the log file for progress updates."
else
    echo "❌ Training failed to start!"
    echo "Check the log file for errors:"
    echo "  cat $LOG_FILE"
    exit 1
fi

# Create a simple monitoring script
cat > training_logs/monitor_training.sh << 'EOF'
#!/bin/bash
# Simple training monitor

PID=$(cat training_logs/training.pid 2>/dev/null)
LOG_FILE=$(ls -t training_logs/training_*.log | head -1)

if [ -z "$PID" ]; then
    echo "No training PID found"
    exit 1
fi

echo "Monitoring training (PID: $PID)..."
echo "Press Ctrl+C to stop monitoring (training will continue)"
echo ""

while true; do
    if ps -p $PID > /dev/null; then
        # Still running - show progress
        echo -ne "\r$(date +%H:%M:%S) - Training in progress... "
        
        # Try to extract progress from log
        PROGRESS=$(grep -E "(completed|GridSearchCV|minutes)" "$LOG_FILE" | tail -1)
        if [ ! -z "$PROGRESS" ]; then
            echo -ne "$(echo $PROGRESS | cut -c1-60)..."
        fi
    else
        # Training finished
        echo -e "\n\n✅ Training completed!"
        echo ""
        echo "Final results:"
        tail -30 "$LOG_FILE" | grep -E "(AUC|complete|saved)"
        break
    fi
    sleep 10
done
EOF

chmod +x training_logs/monitor_training.sh

echo ""
echo "You can monitor training progress with:"
echo "  ./training_logs/monitor_training.sh"
echo ""
echo "=========================================="