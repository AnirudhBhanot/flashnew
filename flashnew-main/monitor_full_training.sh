#!/bin/bash
# Monitor full 324-parameter training

PID=1944
LOG_FILE="training_logs/training_20250604_110743.log"
START_TIME="11:07"

echo "=========================================="
echo "MONITORING FULL PRODUCTION TRAINING"
echo "=========================================="
echo "Started at: $START_TIME"
echo "Expected completion: 12:07-13:07 (1-2 hours)"
echo "Parameter combinations: 324 (vs 48 in optimized)"
echo ""

# Check if still running
if ps -p $PID > /dev/null; then
    echo "✅ Training is currently running"
    
    # Calculate elapsed time
    START_SECONDS=$(date -j -f "%H:%M" "$START_TIME" +%s 2>/dev/null || echo "0")
    CURRENT_SECONDS=$(date +%s)
    if [ "$START_SECONDS" != "0" ]; then
        ELAPSED=$((($CURRENT_SECONDS - $START_SECONDS) / 60))
        echo "⏱️  Elapsed time: $ELAPSED minutes"
    fi
    
    echo ""
    echo "Current status:"
    echo "---"
    tail -30 "$LOG_FILE" | grep -E "(TRAINING|Parameter combinations|Fitting|minutes|AUC|Results|DNA|Temporal|Industry|Ensemble)"
    echo "---"
    
    # Show live progress for GridSearchCV
    echo ""
    echo "GridSearchCV Progress (if available):"
    tail -5 "$LOG_FILE" | grep -E "Fitting|fit"
    
else
    echo "❌ Training has stopped"
    echo ""
    echo "Checking completion status..."
    if grep -q "TRAINING COMPLETE" "$LOG_FILE"; then
        echo "✅ Training completed successfully!"
        echo ""
        echo "Results summary:"
        grep -A5 "Average AUC" "$LOG_FILE"
    else
        echo "⚠️  Training stopped before completion"
        echo ""
        echo "Last entries:"
        tail -20 "$LOG_FILE"
    fi
fi