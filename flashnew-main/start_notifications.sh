#!/bin/bash
#
# Start training notifications in background
#

echo "Starting training notifications..."
echo "You'll receive macOS notifications when each model completes."
echo ""
echo "To stop notifications, run: pkill -f monitor_with_notifications.py"
echo ""

# Run in background and detach
nohup python3 /Users/sf/Desktop/FLASH/monitor_with_notifications.py > /Users/sf/Desktop/FLASH/training_logs/notifications.log 2>&1 &

NOTIFY_PID=$!
echo "Notification monitor started with PID: $NOTIFY_PID"
echo "Log file: training_logs/notifications.log"
echo ""
echo "The monitor will:"
echo "  ✅ Send notifications when each model completes"
echo "  ⏱️ Show training time for each model"
echo "  🎉 Alert when all training is done"
echo "  ⚠️ Warn if training stops unexpectedly"
echo ""
echo "You can now close this terminal and continue working."