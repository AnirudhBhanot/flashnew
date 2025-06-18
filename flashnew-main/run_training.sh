#!/bin/bash
# Run training in background and save output

echo "Starting hierarchical model training on full 100k dataset..."
echo "This will take approximately 15-30 minutes..."
echo "Check training.log for progress"

nohup python3 train_hierarchical_models_45features.py > training.log 2>&1 &
echo $! > training.pid

echo "Training started with PID: $(cat training.pid)"
echo "To check progress: tail -f training.log"
echo "To check if complete: ps -p $(cat training.pid)"