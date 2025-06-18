#!/bin/bash
# Monitor current training progress

PID=1742
LOG_FILE="training_logs/training_resume_20250604_103823.log"

echo "Monitoring optimized training (PID: $PID)"
echo "Started at: 10:38"
echo "Expected completion: 11:08-11:23 (30-45 min)"
echo ""

# Check if still running
if ps -p $PID > /dev/null; then
    echo "✅ Training is currently running"
    echo ""
    
    # Show progress
    echo "Latest progress:"
    echo "---"
    tail -20 "$LOG_FILE" | grep -E "(Results|AUC|minutes|TRAINING|Starting)"
    echo "---"
    echo ""
    
    # Show real-time monitoring
    echo "Monitoring live (Ctrl+C to stop)..."
    tail -f "$LOG_FILE" | grep -E "(Results|AUC|minutes|COMPLETE|ERROR|Failed)"
else
    echo "❌ Training has stopped"
    echo ""
    echo "Final status:"
    tail -50 "$LOG_FILE" | grep -E "(COMPLETE|ERROR|Results|AUC)"
fi