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
