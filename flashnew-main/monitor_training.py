#!/usr/bin/env python3
"""
Monitor the full quality training progress
"""

import time
import os
import subprocess
from datetime import datetime

def monitor_training():
    """Monitor training progress"""
    log_file = "full_training_log.txt"
    start_time = datetime.now()
    
    print("="*60)
    print("MONITORING FULL QUALITY MODEL TRAINING")
    print("="*60)
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: {log_file}")
    print("\nThis training includes:")
    print("- DNA Pattern Analyzer (200 estimators, PCA, clustering)")
    print("- Temporal Model (150 trees + 128x64x32 neural network)")
    print("- Industry-Specific Models (300 iterations CatBoost + XGBoost per industry)")
    print("\nExpected duration: 30-60 minutes")
    print("-"*60)
    
    last_lines = 0
    phase = "Starting"
    
    while True:
        # Check if process is still running
        result = subprocess.run(['pgrep', '-f', 'train_real_models_v2.py'], 
                               capture_output=True, text=True)
        
        if not result.stdout.strip():
            print("\n✅ Training completed!")
            break
            
        # Read log file
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                
            # Check for new content
            if len(lines) > last_lines:
                new_lines = lines[last_lines:]
                last_lines = len(lines)
                
                # Extract status
                for line in new_lines:
                    if "Training DNA Pattern Analyzer" in line:
                        phase = "DNA Pattern Analysis"
                    elif "Training temporal prediction model" in line:
                        phase = "Temporal Prediction"
                    elif "Training industry-specific model" in line:
                        phase = "Industry-Specific Models"
                    elif "AUC:" in line:
                        print(f"\n  📊 {line.strip()}")
                    elif "Training model for industry" in line:
                        print(f"  🏭 {line.strip()}")
                        
                # Update status
                elapsed = datetime.now() - start_time
                print(f"\r[{elapsed.seconds//60:02d}:{elapsed.seconds%60:02d}] Phase: {phase} | Lines: {len(lines)}", end='', flush=True)
        
        time.sleep(5)  # Check every 5 seconds
    
    # Final summary
    print("\n" + "-"*60)
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Training completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {duration.seconds//60} minutes {duration.seconds%60} seconds")
    
    # Check for results
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            content = f.read()
            
        # Extract final AUCs
        print("\n📊 FINAL RESULTS:")
        if "Model Training Complete!" in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "DNA Model AUC:" in line:
                    print(f"  {line.strip()}")
                elif "Temporal Model AUC:" in line:
                    print(f"  {line.strip()}")
                elif "Industry Model AUC:" in line:
                    print(f"  {line.strip()}")
                elif "All models have been trained" in line:
                    print(f"\n✅ {line.strip()}")

if __name__ == "__main__":
    monitor_training()